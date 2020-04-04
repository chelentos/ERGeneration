import sys
import ufal.udpipe
import re
import os

import numpy as np

class Model:
    def __init__(self, path):
        """Load given model."""
        self.model = ufal.udpipe.Model.load(path)
        if not self.model:
            raise Exception("Cannot load UDPipe model from file '%s'" % path)

    def tokenize(self, text):
        """Tokenize the text and return list of ufal.udpipe.Sentence-s."""
        tokenizer = self.model.newTokenizer(self.model.DEFAULT)
        if not tokenizer:
            raise Exception("The model does not have a tokenizer")
        return self._read(text, tokenizer)

    def read(self, text, format):
        """Load text in the given format (conllu|horizontal|vertical) and return list of ufal.udpipe.Sentence-s."""
        input_format = ufal.udpipe.InputFormat.newInputFormat(format)
        if not input_format:
            raise Exception("Cannot create input format '%s'" % format)
        return self._read(text, input_format)

    def _read(self, text, input_format):
        input_format.setText(text)
        error = ufal.udpipe.ProcessingError()
        sentences = []

        sentence = ufal.udpipe.Sentence()
        while input_format.nextSentence(sentence, error):
            sentences.append(sentence)
            sentence = ufal.udpipe.Sentence()
        if error.occurred():
            raise Exception(error.message)

        return sentences

    def tag(self, sentence):
        """Tag the given ufal.udpipe.Sentence (inplace)."""
        self.model.tag(sentence, self.model.DEFAULT)

    def parse(self, sentence):
        """Parse the given ufal.udpipe.Sentence (inplace)."""
        self.model.parse(sentence, self.model.DEFAULT)

    def write(self, sentences, out_format):
        """Write given ufal.udpipe.Sentence-s in the required format (conllu|horizontal|vertical)."""

        output_format = ufal.udpipe.OutputFormat.newOutputFormat(out_format)
        output = ''
        for sentence in sentences:
            output += output_format.writeSentence(sentence)
        output += output_format.finishDocument()

        return output

        

print('Loading model...\n')
model = Model(os.path.join(os.path.dirname(__file__), './russian-syntagrus-ud-2.4-190531.udpipe'))
if not model:
    print("Cannot load model from file \n")
print('Model is loaded!\n')

pattern = r'.*(<NOUN>)+(<VERB>|<ADJ>)+.*(<NOUN>)+.*'

exceptionWords = ['система', 'приложение', 'возможность', 'бдо', 'бд', 'сервер', 'данные', 'авторизация', 'регистрация', 'функция', 'регистрироваться']

def getChild(id, sentence):
    child = object()
    for w in sentence.words[1:]:
        if (w.id == id):
            child = w
    return child

def getChildren(id, sentence):
    children = []
    for w in sentence.words[1:]:
        if (w.id == id):
            children = w.children
    return children

def getTokenConjs(token, sentence, isEnt=False):
    conjs = []
    for w in sentence.words[1:]:
        if (w.id in token.children and w.deprel == 'conj'):
            text = ""
            text += w.lemma
            for t in w.children:
                ch = getChild(t, sentence)
                if ch.deprel == "nmod" and ch.upostag != "PRON":
                    text += ' ' + ch.form
            conj = {
                'text': text,
                'num': getNum(w)
            }
            if not isEnt:
                conj['isKey'] = isKey(w, sentence)
            conjs.append(conj)
    return conjs

def isKey(token, sentence):
    for w in sentence.words[1:]:
        if (w.id in token.children and w.deprel == 'amod'
          and w.lemma in ['уникальный', 'персональный']) or token.lemma in ['идентификатор', 'айдь']:
            return True
    return False

def getRootVoice(root):
    if (root.upostag == "ADJ"):
        return 'Pass'
    else:
        feats = {}
        for feat in re.split('[|]', root.feats):
            feats[feat.split('=')[0]] = feat.split('=')[1]
        return feats['Voice']
        
def getNum(token):
    feats = {}
    for feat in re.split('[|]', token.feats):
        feats[feat.split('=')[0]] = feat.split('=')[1]
    if 'Number' in feats:
        return feats['Number']
    return 'Sing'

def getErFromText(text):
  allEnts = []
  tables = []
  sentences = model.tokenize(text)
  for s in sentences:
      model.tag(s)
      model.parse(s)
      
  for sentence in sentences:
      swords = []
      k = False
      for token in sentence.words[1:]:
          swords.append(token.lemma.lower())
      for word in swords:
          if word in exceptionWords:
              k = True
      if k:
          continue
      posString = ""
      depList = []
      rootDepList = []
      root = None
      subroot = None
      subrootChildren = []
      for token in sentence.words[1:]:
          print(token.id, "-->", token.form, "-->", token.lemma, "-->", token.deprel, "-->", token.upostag, "-->", token.feats)
          posString += "<" + token.upostag + ">"
          depList.append(token.deprel)
          if (token.deprel == "root"):
              root = token
      print("\n")
      print("String with pos tags:", posString)
      for m in re.compile(pattern).finditer(posString):
          
          numTokensInGroup = m.group().count('<')
          
          if (numTokensInGroup > 0):
              if (depList.count("obl") > 0 or depList.count("obj") > 0):
                dependency = None
                objects = {}
                subjects = {}
                dependencyT = ""
                for token in sentence.words[1:]:
                    if (token.deprel == "root"):
                        dependencyT += token.form
                        for t in token.children:
                            ch = getChild(t, sentence)
                            if (ch.deprel == "xcomp"):
                                subroot = ch
                                for t in ch.children:
                                    subrootChildren.append(t)
                                    cch = getChild(t, sentence)
                                    if (cch.deprel == "aux:pass"):
                                        dependencyT +=  ' ' + cch.form
                                dependencyT += ' ' + ch.form
                                if token.lemma == 'должен':
                                    dependency = {
                                        'text': dependencyT,
                                        'mandatory': True
                                    }
                                else:
                                    dependency = {
                                        'text': dependencyT,
                                        'mandatory': False
                                    }
                        if not dependency:
                            dependency = {
                                'text': dependencyT,
                                'mandatory': True
                            }
                    for token in sentence.words[1:]:
                        if token.id in root.children:
                            rootDepList.append(token.deprel)
                    if subroot:
                        for token in sentence.words[1:]:
                            if token.id in subroot.children:
                                rootDepList.append(token.deprel)
                for token in sentence.words[1:]:
                    if (token.deprel == "obl" or token.deprel == "obj") and (token.id in root.children or token.id in subrootChildren):
                        if subroot and depList.count("subj") == 0 and depList.count("nsubj") == 0:
                            if token.deprel == "obl":
                                objects['type'] = 'ent'
                                objects['objects'] = []
                                objects['objects'].append({
                                    'text': token.lemma,
                                    'num': getNum(token),
                                })
                                objects['objects'] += getTokenConjs(token, sentence, True)
                            else:
                                attr = ""
                                attr += token.lemma
                                for t in token.children:
                                    ch = getChild(t, sentence)
                                    if ch.deprel == "nmod" and ch.upostag != "PRON":
                                        attr += ' ' + ch.form
                                subjects['type'] = 'atr'
                                subjects['subjects'] = []
                                subjects['subjects'].append({
                                    'text': attr,
                                    'num': getNum(token),
                                    'isKey': isKey(token, sentence)
                                })
                                subjects['subjects'] += getTokenConjs(token, sentence)
                            continue
                        if rootDepList.count("obl") > 0 and rootDepList.count("obj") > 0:
                            if token.deprel == "obj":
                                print(token.lemma)
                                if (getRootVoice(subroot if subroot else root) in ['Pass', 'Mid']) or root.lemma in ['быть', 'образовывать', 'создавать', 'формировать']:
                                    objects['type'] = 'ent'
                                    objects['objects'] = []
                                    objects['objects'].append({
                                        'text': token.lemma,
                                        'num': getNum(token),
                                    })
                                    objects['objects'] += getTokenConjs(token, sentence, True)
                                else:   
                                    attr = ""
                                    attr += token.lemma
                                    for t in token.children:
                                        ch = getChild(t, sentence)
                                        if ch.deprel == "nmod" and ch.upostag != "PRON":
                                            attr += ' ' + ch.form
                                    objects['type'] = 'atr'
                                    objects['objects'] = []
                                    objects['objects'].append({
                                        'text': attr,
                                        'num': getNum(token),
                                        'isKey': isKey(token, sentence)
                                    })
                                    objects['objects'] += getTokenConjs(token, sentence)
                            continue
                        if (getRootVoice(subroot if subroot else root) in ['Pass', 'Mid']) or root.lemma in ['быть', 'образовывать', 'создавать', 'формировать']:
                            objects['type'] = 'ent'
                            objects['objects'] = []
                            objects['objects'].append({
                                'text': token.lemma,
                                'num': getNum(token),
                            })
                            objects['objects'] += getTokenConjs(token, sentence, True)
                        else:   
                            attr = ""
                            attr += token.lemma
                            for t in token.children:
                                ch = getChild(t, sentence)
                                if ch.deprel == "nmod" and ch.upostag != "PRON":
                                    attr += ' ' + ch.form
                            objects['type'] = 'atr'
                            objects['objects'] = []
                            objects['objects'].append({
                                'text': attr,
                                'num': getNum(token),
                                'isKey': isKey(token, sentence)
                            })
                            objects['objects'] += getTokenConjs(token, sentence)
                    elif (token.deprel == "nsubj") or (token.deprel == "nsubj:pass" and (token.id in root.children or token.id in subrootChildren)):
                        if (getRootVoice(subroot if subroot else root) == 'Act' and root.lemma not in ['быть', 'образовывать', 'создавать', 'формировать']):                          
                            subjects['type'] = 'ent'
                            subjects['subjects'] = []
                            subjects['subjects'].append({
                                'text': token.lemma,
                                'num': getNum(token),
                            })
                            subjects['subjects'] += getTokenConjs(token, sentence, True)
                        else:
                            attr = ""
                            attr += token.lemma
                            for t in token.children:
                                ch = getChild(t, sentence)
                                if ch.deprel == "nmod" and ch.upostag != "PRON":
                                    attr += ' ' + ch.form
                            subjects['type'] = 'atr'
                            subjects['subjects'] = []
                            subjects['subjects'].append({
                                'text': attr,
                                'num': getNum(token),
                                'isKey': isKey(token, sentence)
                            })
                            subjects['subjects'] += getTokenConjs(token, sentence)
                            if (token.deprel in ["nsubj", "nsubj:pass"] ):
                                subjects['subjects'] += getTokenConjs(token, sentence)
                            else:
                                subjects['subjects'] += getTokenConjs(root, sentence)
                objects['objects'] = list({o['text']:o for o in objects['objects']}.values())
                subjects['subjects'] = list({s['text']:s for s in subjects['subjects']}.values())
                if objects['type'] == 'ent':
                    for obj in objects['objects']:
                        allEnts.append(obj['text'])
                if subjects['type'] == 'ent':
                    for subj in subjects['subjects']:
                        allEnts.append(subj['text'])
                tables.append({
                    'dep': dependency,
                    'objs': objects,
                    'subjs': subjects,
                    'sentence_text': sentence.getText(),
                })
  for table in tables:
    if table['objs']['type'] == 'atr':
        for obj in table['objs']['objects']:
            if obj['text'] in allEnts:
                table['objs']['type'] = 'ent'
    if table['subjs']['type'] == 'atr':
        for subj in table['subjs']['subjects']:
            if subj['text'] in allEnts:
                table['subjs']['type'] = 'ent'
  return tables

def getErFromERSents(sents):
  ents = {}
  for sent in sents:
    if sent['subjs']['type'] == 'ent':
        for subj in sent['subjs']['subjects']:
            if subj['text'] not in ents:
                ents[subj['text']] = {}
                ents[subj['text']]['rels'] = []
                ents[subj['text']]['attrs'] = []
            if sent['objs']['type'] == 'atr':
                for obj in sent['objs']['objects']:
                    entObj = obj
                    entObj['dep'] = sent['dep']
                    ents[subj['text']]['attrs'].append(entObj)
            else:
                for obj in sent['objs']['objects']:
                    if obj['text'] not in ents:
                        ents[obj['text']] = {}
                        ents[obj['text']]['attrs'] = []
                        ents[obj['text']]['rels'] = []
                    ents[subj['text']]['rels'].append({
                        'rel': sent['dep'],
                        'to': obj['text'],
                        'toNum': obj['num'],
                        'fromNum': subj['num'],
                        'isBetweeAttrs': False,
                    })
                    print(ents[subj['text']]['rels'])
    elif sent['objs']['type'] == 'ent':
        for obj in sent['objs']['objects']:
            if obj['text'] not in ents:
                ents[obj['text']] = {}
                ents[obj['text']]['attrs'] = []
                ents[obj['text']]['rels'] = []
            for subj in sent['subjs']['subjects']:
                entSubj = subj
                entSubj['dep'] = sent['dep']
                ents[obj['text']]['attrs'].append(entSubj)

  for entName, ent in ents.items():
    for atr in ent['attrs']:
        if len(atr['text'].split(' ')) > 1:
            tokens = model.tokenize(atr['text'])
            for t in tokens:
                    model.tag(t)
                    model.parse(t)
            for token in tokens:
                root = None
                nmod = None
                for t in token.words[1:]:
                    if t.deprel == 'root':
                        root = t
                    elif t.deprel == 'nmod':
                        nmod = t
                if root and nmod:
                    for entName2, ent2 in ents.items():
                        if entName2 == nmod.lemma:
                            for atr2 in ent2['attrs']:
                                if atr2['text'] == root.lemma:
                                    ent2['rels'].append({
                                        'rel': atr['dep'],
                                        'to': entName,
                                        'toNum': 'Sing',
                                        'fromNum': atr['num'],
                                        'isBetweenAttrs': True,
                                        'fromAtr': atr2['text'],
                                    })
  return ents