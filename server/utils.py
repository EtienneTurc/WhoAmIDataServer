"""
		Utils compiles utility scripts for the analysis of the emails
"""

from unidecode import unidecode
import re


def tag_mail(header):
    """
    tag_mail will tag if the mail is in the list of structured emails

    input:
    header : is the header of the email
    output:
    name of the category, or 'no_cat' if non were find

    usage example: df['cat'] = df.headers.apply(tag_mail)
    """
    comp_list = ['linkedin', 'facebook', 'lydia', 'spotify', 'sncf', 'twitter', 'tinder', 'deezer', 'itunes',
                             'apple', 'google', 'uber', 'ubereats', 'doctolib', 'instagram', 'amazon']

    if header == []:
        return None
    for k in header:
        if k['name'] == 'From':
            L_cat = [el * (el in k['value']) for el in comp_list]
            L_cat = list(filter(lambda x: x != '', L_cat))
            if L_cat == []:
                return None
            elif len(L_cat) > 2:
                print(L_cat)
                return L[cat[0]]
            elif len(L_cat) == 1:
                return L_cat[0]
            else:
                return None


def format_mail(text):
    text = text.lower()
    text = unidecode(text)
    return text


def clean_and_tokenize(text):
    """
    Cleaning a document with:
        - Lowercase
        - Removing numbers with regular expressions
        - Removing punctuation with regular expressions
        - Removing other artifacts
    And separate the document into words by simply splitting at spaces
    Params:
        text (string): a sentence or a document
    Returns:
        tokens (list of strings): the list of tokens (word units) forming the document
    """
    # Lowercase
    text = text.lower()
    # Remove numbers
    text = re.sub(r"[0-9]+", "", text)
    # Remove punctuation
    REMOVE_PUNCT = re.compile("[.;:!\'?,\"()\[\]]")
    text = REMOVE_PUNCT.sub("", text)
    # Remove small words (1 and 2 characters)
    text = re.sub(r"\b\w{1,2}\b", "", text)
    # Remove HTML artifacts specific to the corpus we're going to work with
    REPLACE_HTML = re.compile("(<br\s*/><br\s*/>)|(\-)|(\/)")
    text = REPLACE_HTML.sub(" ", text)

    tokens = text.split()
    return tokens
