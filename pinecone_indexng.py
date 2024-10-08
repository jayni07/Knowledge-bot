from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import SentenceTransformerEmbeddings
import pinecone
from langchain.vectorstores import Pinecone
directory = '/content/data'

def load_docs(directory):
  loader = DirectoryLoader(directory)
  documents = loader.load()
  return documents

documents = load_docs(directory)
len(documents)


def split_docs(documents,chunk_size=500,chunk_overlap=20):
  text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
  docs = text_splitter.split_documents(documents)
  return docs

docs = split_docs(documents)
print(len(docs))


embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
query_result = embeddings.embed_query("Hello world")
len(query_result)


# initialize pinecone
pinecone.init(
    api_key="",  # find at app.pinecone.io
    environment="us-east-1-aws"  # next to api key in console
)

index_name = "langchain-chatbot"

index = Pinecone.from_documents(docs, embeddings, index_name=index_name)

def get_similiar_docs(query,k=1,score=False):
  if score:
    similar_docs = index.similarity_search_with_score(query,k=k)
  else:
    similar_docs = index.similarity_search(query,k=k)
  return similar_docs

query = "How is India economy"
similar_docs = get_similiar_docs(query)
similar_docs