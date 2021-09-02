import nltk

test_sentences = ["I want to learn physics",
                  "Teach me physics.",
                  "Help! I don't understand physics."]


def topic(sentence):
    tokens = nltk.word_tokenize(sentence)
    tagged = nltk.pos_tag(tokens)
    grammar = "NP: {<JJ>*<NN>*<NNS>}"
    cp = nltk.RegexpParser(grammar)
    return cp.parse(tagged)


topic(test_sentences[0]).pprint()
# topic(test_sentences[0]).draw()
