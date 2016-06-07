class Seeding(object):

    @staticmethod
    def alzahrani_similarity(sentence_a, sentence_b, model):
        similarity = 0
        for word_a in sentence_a:
            if word_a in sentence_b:
                similarity += 1
            else:
                max_sim = 0
                for word_b in sentence_b:
                    if word_a in model and word_b in model:
                        sim = model.similarity(word_a, word_b);
                        if sim > max_sim:
                            max_sim = sim
                similarity += max_sim
        length = max(len(sentence_a), len(sentence_b))
        if length != 0:
            res = similarity / length
        else:
            res = 0
        return res
