from seeding import Seeding

class Filtering(object):

    @staticmethod
    def remove_overlap3(src_bow, susp_bow, plags, model):
        plags.sort(key=lambda tup: tup[1][0])
        res = []
        flag = 0
        i = 0
        while i < len(plags):
            cont_ol = 0
            if flag == 0:
                for k in range(i + 1, len(plags)):
                    if plags[k][1][0] - plags[i][1][1] <= 0:
                        cont_ol += 1
            else:
                for k in range(i + 1, len(plags)):
                    if plags[k][1][0] - res[-1][1][1] <= 0:
                        cont_ol += 1
            if cont_ol == 0:
                if flag == 0:
                    res.append(plags[i])
                else:
                    flag = 0
                i += 1
            else:
                ind_max = i
                higher_sim = 0.0
                for j in range(1, cont_ol + 1):
                    if flag == 0:
                        sents_i = range(plags[i][1][0], plags[i][1][1] + 1)
                        range_i = range(plags[i][0][0], plags[i][0][1] + 1)
                    else:
                        sents_i = range(res[-1][1][0], res[-1][1][1] + 1)
                        range_i = range(res[-1][0][0], res[-1][0][1] + 1)
                    sents_j = range(plags[i + j][1][0], plags[i + j][1][1] + 1)
                    sim_i_ol = 0.0
                    sim_j_ol = 0.0
                    sim_i_nol = 0.0
                    sim_j_nol = 0.0
                    cont_ol_sents = 0
                    cont_i_nol_sents = 0
                    cont_j_nol_sents = 0
                    for sent in sents_i:
                        sim_max = 0.0
                        for k in range_i:
                            #sim = 1 - spatial.distance.cosine(susp_bow[sent], src_bow[k])
                            sim = Seeding.alzahrani_similarity(susp_bow[sent], src_bow[k], model)
                            if sim > sim_max:
                                sim_max = sim
                        if sent in sents_j:
                            sim_i_ol += sim_max
                            cont_ol_sents += 1
                        else:
                            sim_i_nol += sim_max
                            cont_i_nol_sents += 1
                    range_j = range(plags[i + j][0][0], plags[i + j][0][1] + 1)
                    for sent in sents_j:
                        sim_max = 0.0
                        for k in range_j:
                            #sim = 1 - spatial.distance.cosine(susp_bow[sent], src_bow[k])
                            sim = Seeding.alzahrani_similarity(susp_bow[sent], src_bow[k], model)
                            if sim > sim_max:
                                sim_max = sim
                        if sent in sents_i:
                            sim_j_ol += sim_max
                        else:
                            sim_j_nol += sim_max
                            cont_j_nol_sents += 1
                    sim_i = sim_i_ol / cont_ol_sents
                    if cont_i_nol_sents != 0:
                        sim_i = sim_i + (1 - sim_i) * sim_i_nol / float(cont_i_nol_sents)
                    sim_j = sim_j_ol / cont_ol_sents
                    if cont_j_nol_sents != 0:
                        sim_j = sim_j + (1 - sim_j) * sim_j_nol / float(cont_j_nol_sents)
                    if sim_i > 0.99 and sim_j > 0.99:
                        if len(sents_j) > len(sents_i):
                            if sim_j > higher_sim:
                                ind_max = i + j
                                higher_sim = sim_j
                    elif sim_j > sim_i:
                        if sim_j > higher_sim:
                            ind_max = i + j
                            higher_sim = sim_j
                if flag == 0:
                    res.append(plags[ind_max])
                elif ind_max != i:
                    del res[-1]
                    res.append(plags[ind_max])
                i = i + cont_ol
                flag = 1
        return res