import spacy

statement = 'a male cactus can have 5 different pricks'

nlp = spacy.load('en_core_web_sm')
doc = nlp(statement)
typeLabels = [
    'ROOT', 'acl', 'acomp', 'advcl', 'advmod', 'agent', 'amod', 'appos', 'attr', 
    'aux', 'auxpass', 'case', 'cc', 'ccomp', 'compound', 'conj', 'cop', 'csubj', 
    'dative', 'dep', 'det', 'dobj', 'expl', 'intj', 'mark', 'meta', 'neg', 'nmod', 
    'npadvmod', 'nsubj', 'nsubjpass', 'nummod', 'oprd', 'parataxis', 'pcomp', 
    'pobj', 'poss', 'preconj', 'prep', 'prt', 'punct', 'quantmod', 'relcl', 'xcomp'
]
questionWords = ["what", "who", "where", "when", "how many", "how"]
questionTemplates = [
    ["What", "auxpass", "det", "nsubjpass", "prep", "pobj", "ROOT"],
    ["How many", "amod", "dobj", "aux", "det", "amod", "nsubj", "ROOT"],
    ["nsubj", "ROOT", "what"],
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

def getNextObject(position, template):
    object = ""
    objects = ["nsubj", "nsubjpass", "dobj"]
    for index, part in enumerate(template):
        if index > position and part in objects:
            object = part
            break
    return object

def getWordByType(wordType, nextObject):
    findings = []
    for token in doc:
        if token.dep_ == wordType:
            findings.append(token)
    for finding in findings:
        if finding.head.dep_ == nextObject:
            return finding.text
    if len(findings) > 0:
        return findings[0].text
    return None

def createQuestion():
    question = ""
    for template in questionTemplates:
        for index, wordType in enumerate(template):
            if wordType in typeLabels:
                found = getWordByType(wordType, getNextObject(index, template))
                if found is not None:
                    question += found + " "
                else:
                    question = ""
                    break
            elif wordType.lower() in questionWords:
                question += wordType + " "
            elif wordType == "subject":
                question += extractSubject() + " "
            elif wordType == "object":
                question += extractObject() + " "
            else:
                question = ""
                break
        question = question.strip()
        if len(template) == len(question.split(" ")):
            question += "?"
            break
    if question != "":
        question += "?"
        return question
    return ""

def listDependencies():
    for token in doc:
        print(token.text + " -> " + token.dep_ + " -> " + token.head.text + " -> " + token.head.dep_)
    print()

print()
print(createQuestion())
print()
