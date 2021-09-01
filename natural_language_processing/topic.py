import nltk

test_sentences = ["I want to learn physics",
                  "Teach me physics.",
                  "Help! I don't understand physics."]

sentence = test_sentences[0]
tokens = nltk.word_tokenize(sentence)
tagged = nltk.pos_tag(tokens)
entities = nltk.chunk.ne_chunk(tagged)

print(entities)