class Seeding(object):

    @staticmethod
    def alzahrani_similarity(s1, s2, model):
        string_similarity = []
        for ws1 in s1:
            max_word_similarity = 0
            max_similar_word    = u""
            for ws2 in s2:
                if(ws1 in model and ws2 in model):
                    similarity = model.similarity(ws1, ws2)
                    if similarity > max_word_similarity:
                        max_word_similarity = similarity
                        max_similar_word    = ws2
            if max_word_similarity > 0:
                string_similarity.append( max_word_similarity )
        try:
            return sum(string_similarity) / len(string_similarity)
        except Exception as exc:
            print exc
            for x in s1:
                print "".join(y for y in x if ord(y) < 128),
            for x in s2:
                print "".join(y for y in x if ord(y) < 128),
            print "\n"
            return 0
