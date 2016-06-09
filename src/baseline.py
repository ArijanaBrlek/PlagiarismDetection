#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import os
import sys

from gensim.models import Word2Vec

from constants import LENGTH
from extension import Extension
from filtering import Filtering
from helpers import serialize_features
from helpers import serialize_to_json
from preprocessing import Preprocessing
from seeding import Seeding

""" The following class implement a very basic baseline comparison, which
aims at near duplicate plagiarism. It is only intended to show a simple
pipeline your plagiarism detector can follow.
Replace the single steps with your implementation to get started.
"""

class Baseline:
    def __init__(self, susp, src, outdir, model):
        self.susp = susp
        self.src = src
        self.susp_file = os.path.split(susp)[1]
        self.src_file = os.path.split(src)[1]
        self.susp_id = os.path.splitext(susp)[0]
        self.src_id = os.path.splitext(src)[0]
        self.output = self.susp_id + '-' + self.src_id + '.xml'
        self.detections = None
        self.outdir = outdir

        self.th1 = 0.6
        self.th2 = 0.33
        self.th3 = 0.33
        self.src_gap = 4
        self.src_gap_least = 2
        self.susp_gap = 4
        self.susp_gap_least = 2
        self.src_size = 1
        self.susp_size = 1
        self.min_sentlen = 3
        self.min_plaglen = 150
        self.rssent = 'no'
        self.tf_idf_p = 'yes'
        self.rem_sw = 'no'

        self.src_offsets = []
        self.susp_offsets = []
        self.src_sents = []
        self.susp_sents = []
        self.model = model

    def process(self):
        """ Process the plagiarism pipeline. """
        self.preprocess()
        self.detections = self.compare()
        self.postprocess()

    def preprocess(self):
        """ Preprocess the suspicious and source document. """
        susp_fp = codecs.open(self.susp, 'r', 'utf-8')
        self.susp_text = susp_fp.read()
        self.susp_bow = Preprocessing.tokenize(self.susp_text, self.susp_offsets, self.susp_sents)
        Preprocessing.ss_treat(self.susp_bow, self.susp_offsets, self.min_sentlen, self.rssent)
        susp_fp.close()

        src_fp = codecs.open(self.src, 'r', 'utf-8')
        self.src_text = src_fp.read()
        self.src_bow = Preprocessing.tokenize(self.src_text, self.src_offsets, self.src_sents)
        Preprocessing.ss_treat(self.src_bow, self.src_offsets, self.min_sentlen, self.rssent)
        src_fp.close()


    def compare(self):
        """ Test a suspicious document for near-duplicate plagiarism with regards to
        a source document and return a feature list.
        """
        ps = []
        detections = []
        susp_sent = []

        for i in range(len(self.susp_bow)):
            for j in range(len(self.src_bow)):
                alza_sim = Seeding.alzahrani_similarity(self.susp_bow[i], self.src_bow[j], self.model)
                if alza_sim > self.th1:
                    # print "***"
                    # print alza_sim
                    # print self.susp_bow[i]
                    # print self.src_bow[j]
                    ps.append((i, j))

        # extend faza
        (plags, psr) = Extension.integrate_cases(ps, self.src_gap, self.susp_gap, self.src_size, self.susp_size)
        (plags2, psr2) = Extension.integrate_cases(ps, self.src_gap + 20, self.susp_gap + 20, self.src_size, self.susp_size)


        plags = Extension.similarity3(plags, psr, self.src_bow, self.susp_bow, self.src_gap, self.src_gap_least, self.susp_gap,
                            self.susp_gap_least, self.src_size, self.susp_size, self.th3, self.model)
        plags2 = Extension.similarity3(plags2, psr2, self.src_bow, self.susp_bow, self.src_gap + 20, self.src_gap_least,
                             self.susp_gap + 20, self.susp_gap_least, self.src_size, self.susp_size, self.th3, self.model)

        plags = Filtering.remove_overlap3(self.src_bow, self.susp_bow, plags, self.model)
        plags2 = Filtering.remove_overlap3(self.src_bow, self.susp_bow, plags2, self.model)

        sum_src = 0
        sum_susp = 0
        for plag in plags2:
            arg1 = (self.src_offsets[plag[0][0]][0], self.src_offsets[plag[0][1]][0] + self.src_offsets[plag[0][1]][1])
            arg2 = (
            self.susp_offsets[plag[1][0]][0], self.susp_offsets[plag[1][1]][0] + self.susp_offsets[plag[1][1]][1])
            sum_src = sum_src + (arg1[1] - arg1[0])
            sum_susp = sum_susp + (arg2[1] - arg2[0])

        if sum_src >= 3 * sum_susp:
            for plag in plags2:
                arg1 = (
                self.src_offsets[plag[0][0]][0], self.src_offsets[plag[0][1]][0] + self.src_offsets[plag[0][1]][1])
                arg2 = (
                self.susp_offsets[plag[1][0]][0], self.susp_offsets[plag[1][1]][0] + self.susp_offsets[plag[1][1]][1])
                if arg1[1] - arg1[0] >= self.min_plaglen and arg2[1] - arg2[0] >= self.min_plaglen:
                    detections.append([arg1, arg2])
        else:
            for plag in plags:
                arg1 = (
                self.src_offsets[plag[0][0]][0], self.src_offsets[plag[0][1]][0] + self.src_offsets[plag[0][1]][1])
                arg2 = (
                self.susp_offsets[plag[1][0]][0], self.susp_offsets[plag[1][1]][0] + self.susp_offsets[plag[1][1]][1])
                if arg1[1] - arg1[0] >= self.min_plaglen and arg2[1] - arg2[0] >= self.min_plaglen:
                    detections.append([arg1, arg2])
        return detections

    def postprocess(self):
        """ Postprocess the results. """
        serialize_features(self.susp_file, self.src_file, self.detections, self.outdir)
        serialize_to_json(self.susp_file, self.src_file, self.detections, self.outdir)


# Main
# run: python src/baseline.py data/mypairs data/src/ data/susp/ data/out/
# ====
if __name__ == "__main__":
    """ Process the commandline arguments. We expect three arguments: The path
    pointing to the pairs file and the paths pointing to the directories where
    the actual source and suspicious documents are located.
    """
    if len(sys.argv) == 5:
	datasetdir = sys.argv[1]
        srcdir = sys.argv[2]
        suspdir = sys.argv[3]
        outdir = sys.argv[4]
        model = Word2Vec.load_word2vec_format('data/model/GoogleNews-vectors-negative300.bin', binary=True)

	subfolders = ['none', 'random', 'summary', 'translation']

        if datasetdir[-1] != "/":
            datasetdir += "/"

        for subfolder in subfolders:
            print subfolder
            for t1 in [x * 0.1 for x in range(3, 9)]:
                for t3 in [x * 0.1 for x in range(3, 9)]:
                    print 't1={}, t3={}'.format(t1, t3)
                    outdir = datasetdir + 'out/' + subfolder + '_t1_' + str(t1).replace('.', '') + '_t3_' + str(t3).replace('.','') + '/'	
                    if not os.path.exists(outdir):
                        os.makedirs(outdir)
	            lines = open(datasetdir + subfolder + '/pairs', 'r').readlines()
                    print len(lines)

                    for (i, line) in enumerate(lines):
                        print "{}/{}".format(i + 1, len(lines))
			susp, src = line.split()
			baseline = Baseline(os.path.join(suspdir, susp), os.path.join(srcdir, src), outdir, model)
			baseline.th1 = t1
                        baseline.th3 = t3
                        baseline.process()
    else:
        print('\n'.join(["Unexpected number of commandline arguments.",
                         "Usage: ./pan12-plagiarism-text-alignment-example.py {pairs} {src-dir} {susp-dir} {out-dir}"]))
