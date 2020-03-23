import redis
import json


r = redis.Redis("localhost", 6379)


def setData(client, token, path, value):
    return client.execute_command(
        "JSON.SET", f"{token}", f".{path}", f"{json.dumps(value)}")


def getData(client, token, path):
    return json.loads(client.execute_command("JSON.GET", f"{token}", f".{path}"))


if __name__ == "__main__":
    print(getData(r, "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjoiZXRpZW5uZS50dXJjQGdtYWlsLmNvbSIsImlhdCI6MTU4NDg3NTEzOH0.F2_L6q_VKcqyFEl3_Lf6nvB89MThwo8fk3DxzjuQ-oE", "raw.google.mail.received"))
