from utils import clean_and_tokenize


categories = ['sport', 'education', 'alimentation']
vocab = []
vocab_concept = []

for cat in categories:
    with open('vocabulary/'+cat+'_all.txt', 'r') as f:
        words = f.read().split('\n')
        while("" in words):
            words.remove("")
        vocab += words
    with open('vocabulary/'+cat+'_concept.txt', 'r') as f:
        concept = f.read().split('\n')
        while("" in concept):
            concept.remove("")
        vocab += concept
        vocab_concept.append(concept)


def lookup(word_list):
    count = 0
    for x in word_list:
        if x in vocab:
            count += 1
    return count


def see_words(text):
    L = []
    for el in text:
        if el in vocab:
            L += [el]
    return L


def addToFound(words_found, words):
    for w in words:
        if w in words_found:
            words_found[w] += 1
        else:
            words_found[w] = 1
    return words_found


def getExtractedWords(bow):
    if not len(bow):
        return {}
    last = bow[0]
    words_found = addToFound({}, last)
    for i in range(1, len(bow)):
        new = False
        for j in range(len(bow[i])):
            if bow[i][j] not in last:
                new = True
                break
        if new:
            last = bow[i]
            words_found = addToFound(words_found, last)
    return words_found


def getWords(df):
    df['clean_text_tok'] = df.body.apply(clean_and_tokenize)
    df['words'] = df['clean_text_tok'].apply(see_words)
    df['count'] = df['clean_text_tok'].apply(lookup)

    return getExtractedWords(df.loc[df['count'] > 0].words.values.tolist())
