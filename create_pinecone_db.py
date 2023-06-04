import os
import pinecone

def create_pinecone_index(index_name, api_key, dimension):
    pinecone.init(api_key=api_key, environment='us-east-1-aws')
    pinecone.create_index(index_name, dimension=dimension, metric='cosine')

# Retrieve the Pinecone API key from the environment variable
api_key = os.environ.get('pinecone_api_key')

# Set the name for the Pinecone index
index_name = 'my-assignments'

# Set the dimension of the embeddings compatible with OpenAI
dimension = 768

create_pinecone_index(index_name, api_key, dimension)
