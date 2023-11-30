import spacy

# Load the English language model
nlp = spacy.load('en_core_web_sm')

# Example sentence
sentence = 'I ate a huge car.'
doc = nlp(sentence)
typeLabels = [
    'ROOT', 'acl', 'acomp', 'advcl', 'advmod', 'agent', 'amod', 'appos', 'attr', 
    'aux', 'auxpass', 'case', 'cc', 'ccomp', 'compound', 'conj', 'cop', 'csubj', 
    'dative', 'dep', 'det', 'dobj', 'expl', 'intj', 'mark', 'meta', 'neg', 'nmod', 
    'npadvmod', 'nsubj', 'nsubjpass', 'nummod', 'oprd', 'parataxis', 'pcomp', 
    'pobj', 'poss', 'preconj', 'prep', 'prt', 'punct', 'quantmod', 'relcl', 'xcomp'
]
questionTemplates = [
    ["What", "auxpass", "subject", "ROOT"]
]

def extractSubject():
    subject = ""
    for token in doc:
        if token.dep_ == "nsubj" or token.dep_ == "nsubjpass":
            subject = " ".join([t.text for t in token.subtree])
            break
    return subject

def extractObject():
    object = ""
    for token in doc:
        if token.dep_ == "dobj":
            object = " ".join([t.text for t in token.subtree])
            break
    return object

def getWordByType(wordType):
    for token in doc:
        if token.dep_ == wordType:
            return token

def createQuestion():
    question = ""
    for template in questionTemplates:
        for wordType in template:
            try:
                print(wordType)
                if wordType not in typeLabels:
                    question += wordType + " "
                elif wordType == "subject":
                    question += extractSubject() + " "
                elif wordType == "object":
                    question += extractObject() + " "
                else:
                    found = getWordByType(wordType)
                    if found is not None:
                        question += found + " "
                    else:
                        continue
            except:
                pass
    return question

print(createQuestion())
