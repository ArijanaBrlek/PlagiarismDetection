# -*- coding: utf-8 -*-

import re

import nltk

from constants import contractions, QUANTIFIERS
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


class Preprocessing(object):

    @staticmethod
    def tokenize(text, offsets=[], sents=[]):
        contractions_re = re.compile('(%s)' % '|'.join(contractions.keys()))

        def expand_contractions(s, contractions=contractions):
            def replace(match):
                return contractions[match.group(0)]

            return contractions_re.sub(replace, s)

        sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
        sents.extend(sent_detector.tokenize(text))
        raw = text.lower()
        #raw = expand_contractions(raw)
        sentences = sent_detector.tokenize(raw)

        offsets.extend([a, b - a] for (a, b) in sent_detector.span_tokenize(raw))

        sentences_tokenized = []
        for sentence in sentences:
            # za pretvorbu npr. car's -> car
            sentence = re.sub(r"'\w*", "", sentence)
            sentence = re.sub(r'’\w*', '', sentence)
            # da ostanu samo alfanumericki znakovi i razmak
            sentence = re.sub(r'([^\s\w]|_)+', ' ', sentence)

            # uklanjanje brojeva - mozda ce biti bolje i bez ovoga, ima naznaka da w2v bolje radi ako se ne maknu stopwords i brojevi
            sentence = re.sub(r'\s[0-9]+\s', " ", sentence)

            tokenizer = RegexpTokenizer(r'\w+')
            sentence_tokens = tokenizer.tokenize(sentence)

            wordnet_lemmatizer = WordNetLemmatizer()
            sentence_tokenized = []
            for word in sentence_tokens:
                if word in QUANTIFIERS:
                    sentence_tokenized.append(word)
                else:
                    if word not in stopwords.words('english'):
                        sentence_tokenized.append(wordnet_lemmatizer.lemmatize(word))
            sentences_tokenized.append(sentence_tokenized)

        return sentences_tokenized

    # za spajanje malih recenica
    @staticmethod
    def ss_treat(list_dic, offsets, min_sentlen, rssent):
        if rssent=='no':
            i=0
            range_i=len(list_dic)-1
            while i<range_i:
                if len(list_dic[i]) < min_sentlen:

                    list_dic[i].extend(list_dic[i+1])
                    #sum_vect(list_dic[i+1],list_dic[i])
                    del list_dic[i+1]
                    offsets[i+1]=(offsets[i][0],offsets[i+1][1]+offsets[i][1])
                    del offsets[i]
                    range_i-=1

                else:
                    i=i+1
        else:
            i=0
            range_i=len(list_dic)-1
            while i<range_i:
                if sum(list_dic[i].values())<min_sentlen:
                    del list_dic[i]
                    del offsets[i]
                    range_i-=1
                else:
                    i=i+1

