import json

def getJSON(data):
    if data is None:
        return json.dumps(dict())
    return json.dumps(data)
    # return json.dumps([dict(row) for row in data], ensure_ascii=False).encode('utf8').decode()

def parseJSONArray(data):
    return json.loads(data)

