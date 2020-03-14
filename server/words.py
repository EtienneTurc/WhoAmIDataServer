"""
Utility wrappers for Redis interaction.

For test purpose, you can add a word to fake sessions 'session' by just calling python3 words.py word_to_add
"""

import redis
import sys

r = redis.Redis()


def addWordToSession(word, session):
    r.rpush(session, word)


def addWordsToSession(words, session):
    for word in words:
        addWordToSession(word, session)


if __name__ == "__main__":
    addWordsToSession(
        sys.argv[1:], "session")
