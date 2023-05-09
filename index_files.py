import os
import glob
import docx2txt
import openai
import pinecone

def get_openai_embedding(text):
    openai.api_key = os.environ.get('openai_api_key')
    try:
        response = openai.Embedding.create(
            model="text-embedding-ada-002",
            input=text
        )
        embedding = response['data'][0]['embedding']
        return embedding
    except Exception as e:
        print(f"Error generating embedding: {str(e)}")
        return None

def create_pinecone_index(index_name, api_key, dimension):
    pinecone.init(api_key=api_key, environment='us-east-1-aws')
    if index_name not in pinecone.list_indexes():
        pinecone.create_index(index_name, dimension=dimension, metric='cosine')
    else:
        print(f"Index '{index_name}' already exists.")

def index_document_in_pinecone(index_name, embedding,vector_id,api_key,file_name):
    pinecone.init(api_key=api_key, environment='us-east-1-aws')
    index = pinecone.Index(index_name)
    vectors= [{"id":vector_id,"metadata":{"file_name":file_name},"values":embedding}]
    try:
        #print(str(embedding), type(embedding))
        index.upsert( vectors=vectors, namespace='assignments')
    except Exception as e:
        print(f"Error indexing document: {str(e)}")

# Retrieve the Pinecone API key from the environment variable
api_key = os.environ.get('pinecone_api_key')

# Set the name for the Pinecone index
index_name = 'my-assignments2'

# Set the dimension of the embeddings compatible with OpenAI
dimension = 1536

# Set the folder path to scan for .docx files
folder_path = 'C:/Users/Oscar/OneDrive/'

# Scan for .docx files in the folder and its subfolders
docx_files = glob.glob(os.path.join(folder_path, '**/*.docx'), recursive=True)

# Create the Pinecone index if it doesn't exist
create_pinecone_index(index_name, api_key, dimension)
i = 0
# Process each .docx file and index its embedding in Pinecone
for docx_file in docx_files:
    try:
        text = docx2txt.process(docx_file)
        embedding = get_openai_embedding(text)
        if embedding:
            index_document_in_pinecone(index_name, embedding,vector_id=f"item_{i}", api_key = api_key, file_name=docx_file)
            print(f"Indexed document '{docx_file}' successfully.")
            i = i + 1
        else:
            print(f"Skipping document '{docx_file}' due to embedding generation error.")
    except Exception as e:
        print(f"Error processing file '{docx_file}': {str(e)}")

print('Documents indexed successfully.')
