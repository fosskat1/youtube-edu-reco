# one time required for tokenization:
# select: punkt, averaged_perceptron_tagger, maxent_ne_chunker, words
import nltk
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download()