from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

def getEmbeddings(sentenceArr):
    return model.encode(sentenceArr)