import nltk


def topic(sentence):
    """
    Chunk Natural Language Text into noun phrases, no named entity recognition
    :param sentence: str Natural Language Text
    :return: List representing NLTK tree
    """
    tokens = nltk.word_tokenize(sentence)
    tagged = nltk.pos_tag(tokens)
    grammar = "NP: {<JJ>*<NN>*<NNS>}"
    cp = nltk.RegexpParser(grammar)
    return cp.parse(tagged)


def get_noun_phrase(t, noun_phrase=""):
    """
    Find Noun Phrases in Sentence
    :param t: Tree result from chunking
    :param noun_phrase: noun_phrase currently found
    :return: str noun_phrase
    """
    for child in t:
        try:
            node_type = t.label()
            if node_type == "NP":
                noun_phrase = " ".join([child[0] for child in t])
            else:
                noun_phrase = get_noun_phrase(child, noun_phrase)
        except AttributeError as err:
            pass
    return noun_phrase


# test code
test_sentences = ["I want to learn physics",
                  "I don't understand astro physics.",
                  "Teach me algebra"]
for sentence in test_sentences:
    chunked = topic(sentence)
    noun_phrase = get_noun_phrase(chunked)
    print(f"{noun_phrase != ''} {sentence} --- {chunked} --- {noun_phrase}")

# pretty print and draw full tree
# output.pprint()
# topic(test_sentences[0]).draw()

