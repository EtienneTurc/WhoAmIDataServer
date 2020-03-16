"""
Utility wrappers for Redis interaction.

For test purpose, you can add a word to fake sessions 'session' by just calling python3 words.py word_to_add
"""

import redis
import sys

r = redis.Redis(decode_responses=True)


def addWordToSession(word, session):
    r.rpush(session, word)


def addWordsToSession(words, session):
    for word in words:
        addWordToSession(word, session)


def addWordDictToSession(session, words):
    # print("ADDDING WORDS", words)
    return r.hmset(session, words)


def getWordDictFromSession(session, delete=True):
    words = r.hgetall(session)
    if delete:
        r.delete(session)
    return words


if __name__ == "__main__":
    addWordsToSession(
        sys.argv[1:], "session")
