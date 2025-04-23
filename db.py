import pymongo
import os
import numpy as np
from textToVector import getEmbeddings
import json

# chan
uri = os.environ["DB_URI"] 

client = pymongo.MongoClient(uri,tls=True, tlsAllowInvalidCertificates=True)

db = client["DBDB"]
collection = db['WOWIRONBANK']

def addVectors(SentArr,embeddingArr,filename):
    for i in range(len(SentArr)):
        doc={
            "text": SentArr[i],
            "embeddings": np.array(embeddingArr[i]).tolist(), 
            "file": filename,
             }
        collection.insert_one(doc)
    print(f"pdf Done: {filename}")

def getTop5Document(question):
    query_vector = getEmbeddings([question])
    query_vector = np.array(query_vector[0]).tolist()
    pipeline = [
        {
    "$vectorSearch": {
      "index": "vector_index",
      "path": "embeddings",
      "queryVector": query_vector,
      "numCandidates": 1000,
      "limit": 5
            }
        }
    ]
    i = 0
    results = collection.aggregate(pipeline)
    ans = []
    for document in results:
        ans.append(document["text"])
        i += 1
        print(i)
    print("total documents found: ", i)
    return ans

# print(getTop5Document("What is the freedom of speech?"))