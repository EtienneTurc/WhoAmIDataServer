import json
import os

import redis


redis_client = redis.Redis(os.getenv("REDIS_HOST", "127.0.0.1"),
                           os.getenv("REDIS_PORT", 6379))


def setData(token, path, value):
    try:
        return redis_client.execute_command(
            "JSON.SET", "{}".format(token), ".{}".format(path), "{}".format(json.dumps(value)))
    except Exception as ex:
        print(ex)


def getData(token, path):
    res = redis_client.execute_command(
        "JSON.GET", "{}".format(token), ".{}".format(path))
    if res:
        res = json.loads(res.decode("utf-8"))
    return res


def addToList(token, path, value):
    try:
        return redis_client.execute_command(
            "JSON.ARRAPPEND", "{}".format(token), ".{}".format(path), "{}".format(json.dumps(value)))
    except Exception as ex:
        print(ex)


def flushAllData():
    redis_client.flushall()


if __name__ == "__main__":
    print(getData(redis_client, "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjoiZXRpZW5uZS50dXJjQGdtYWlsLmNvbSIsImlhdCI6MTU4NDk2NTM3Mn0.kykkN6BVmSMKzzXUAU6Snnq7K87aL19Ua7YY0yYvtUg", "raw.google.mail.received"))
