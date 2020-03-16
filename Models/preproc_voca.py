import unicodedata
from os import listdir
from os.path import isfile, join


def strip_accents(text):
    try:
        text = unicode(text, 'utf-8')
    except NameError:  # unicode is a default on python 3
        pass

    text = unicodedata.normalize('NFD', text).encode(
        'ascii', 'ignore').decode("utf-8")

    return str(text)


folder = "vocabulary"
filename = 'finance.txt'
allFolder = True

onlyfiles = [filename]
if allFolder:
    onlyfiles = [f for f in listdir(folder) if isfile(join(folder, f))]

for file in onlyfiles:
    with open(folder + "/unclean/" + file, encoding="utf-8") as f:
        vocab = f.read()

    vocab = strip_accents(vocab)
    vocab = vocab.lower()
    vocab = vocab.replace('-', '')
    vocab = vocab.replace("'", " ")

    if len(vocab.split('\n')) > 10:
        vocab = vocab.split('\n')
    elif len(vocab.split(',')) > 10:
        vocab = vocab.split(',')
    else:
        print('wrong separator')

    vocab = [v for v in vocab if v]
    vocab = list(set(vocab))
    vocab.sort()

    with open(folder + "/clean/" + file, 'w') as f:
        for item in vocab:
            f.write("%s\n" % item)
