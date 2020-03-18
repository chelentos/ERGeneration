import pickle
import os

import spacy
import spacy_udpipe

from sklearn.feature_extraction.text import CountVectorizer

print('initialising model...')
udpipe_model = spacy_udpipe.UDPipeModel('ru')
nlp = spacy.load(os.path.join(os.path.dirname(__file__), 'udpipe-spacy-model-ru'), udpipe_model=udpipe_model)
print('model is initialised')

class CustomVectorizer(CountVectorizer): 
    
    # overwrite the build_analyzer method, allowing one to
    # create a custom analyzer for the vectorizer
    def build_analyzer(self):
        # load stop words using CountVectorizer's built in method
        stop_words = self.get_stop_words()
        
        # create the analyzer that will be returned by this method
        def analyser(doc):
            lemmatized_tokens = []
            for token in nlp(doc):
                if token.like_num:
                    lemmatized_tokens.append('ЧИСЛО')
                    print(token.lemma_)
                    continue
                if not token.is_punct:
                    lemmatized_tokens.append(token.lemma_)
            # use CountVectorizer's _word_ngrams built in method
            # to remove stop words and extract n-grams
            return(self._word_ngrams(lemmatized_tokens, stop_words))
        return(analyser)

def classifyReqs(reqs):
  with open(os.path.join(os.path.dirname(__file__), 'req_classifier.pkl'), 'rb') as file:
    classifier = pickle.load(file)
    reqsTypes = classifier.predict(reqs)
    classifiedReqs = []
    for req, rType in zip(reqs, reqsTypes):
      cReq = {}
      cReq['text'] = req
      cReq['type'] = rType
      classifiedReqs.append(cReq)
    return classifiedReqs