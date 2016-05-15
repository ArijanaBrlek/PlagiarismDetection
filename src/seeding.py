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
                        if model.similarity(word_a, word_b) > max_sim:
                            max_sim = model.similarity(word_a, word_b)
                similarity += max_sim
        res = similarity / max(len(sentence_a), len(sentence_b))
        return res
