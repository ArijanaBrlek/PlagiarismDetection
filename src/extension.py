from helpers import sum_vect
from scipy import spatial

class Extension(object):

    @staticmethod
    def integrate_cases(ps, src_gap, susp_gap, src_size, susp_size):
        ps.sort(key=lambda tup: tup[0])
        pss = []
        sub_set = []
        for pair in ps:
            if len(sub_set) == 0:
                sub_set.append(pair)
            else:
                if Extension.adjacent(pair[0], sub_set[-1][0], susp_gap):
                    sub_set.append(pair)
                else:
                    if len(sub_set) >= susp_size:
                        pss.append(sub_set)
                    sub_set = [pair]
        if len(sub_set) >= susp_size:
            pss.append(sub_set)
        psr = []
        for pss_i in pss:
            pss_i.sort(key=lambda tup: tup[1])
            sub_set = []
            for pair in pss_i:
                if len(sub_set) == 0:
                    sub_set.append(pair)
                else:
                    if  Extension.adjacent(pair[1], sub_set[-1][1], src_gap):
                        sub_set.append(pair)
                    else:
                        if len(sub_set) >= src_size:
                            psr.append(sub_set)
                        sub_set = [pair]
            if len(sub_set) >= src_size:
                psr.append(sub_set)
        plags = []
        for psr_i in psr:
            plags.append([(min([x[1] for x in psr_i]), max([x[1] for x in psr_i])),
                          (min([x[0] for x in psr_i]), max([x[0] for x in psr_i]))])
        return plags, psr

    @staticmethod
    def adjacent(a, b, th):
        if abs(a - b) - th - 1 <= 0:
            return True
        else:
            return False

    @staticmethod
    def similarity3(plags, psr, src_bow, susp_bow, src_gap, src_gap_least, susp_gap, susp_gap_least, src_size,
                    susp_size, th3):
        res = []
        i = 0
        range_i = len(plags)
        while i < range_i:
            src_d = []
            for j in range(plags[i][0][0], plags[i][0][1] + 1):
                src_d = sum_vect(src_d, src_bow[j])
            susp_d = []
            for j in range(plags[i][1][0], plags[i][1][1] + 1):
                susp_d = sum_vect(susp_d, susp_bow[j])

            # if dice_coeff(src_d,susp_d)<=th3:# or cosine_measure(src_d,susp_d)<=0.40:
            if (1 - spatial.distance.cosine(src_d, susp_d)) <= th3:
                if src_gap - src_gap_least > 0 and susp_gap - susp_gap_least > 0:  # Do until substraction +1
                    (temp1, temp2) = Extension.integrate_cases(psr[i], src_gap - 1, susp_gap - 1, src_size, susp_size)
                    if len(temp1) == 0:
                        return []
                    res2 = Extension.similarity3(temp1, temp2, src_bow, susp_bow, src_gap - 1, src_gap_least, susp_gap - 1,
                                       susp_gap_least, src_size, susp_size, th3)
                    if len(res2) != 0:
                        res.extend(res2)
                i += 1
            else:
                res.append(plags[i])
                i += 1
        return res
