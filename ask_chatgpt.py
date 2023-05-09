import os
import openai
import docx2txt
import pinecone

def ask_gpt3(query):
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=query,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.7
    )

    if response['choices'][0]['text']:
        return response['choices'][0]['text'].strip()
    else:
        return "No response from the API."

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

def query_pinecone_index(embedding_vector):
    index = pinecone.Index(index_name=index_name)
    response = index.query(namespace=namespace,queries=[embedding_vector],top_k=2, include_metadata=True)
    results = response.results[0]['matches']
    return results
 




index_name = 'my-assignments2'
namespace = 'assignments'
openai.api_key = os.getenv("openai_api_key")
pinecone_api_key = os.getenv("pinecone_api_key")
pinecone.init(api_key=pinecone_api_key, environment='us-east-1-aws')

query = "What is an ethical way to distribute the burdens of climate change?"
query = "Who is Marychu Dayao"


embedding_vector = get_openai_embedding (query)
candidates = query_pinecone_index(embedding_vector)
selected_file = candidates[0]['metadata']['file_name']
print(f'File candidates:\n{candidates}')

my_context = text = docx2txt.process(selected_file)

response_no_context = ask_gpt3(query)
response_with_context = ask_gpt3(f"Answer this question: {query} using the following document as context only if appropriate: {my_context}")

print(f"Response with NO context:\n{response_no_context}")
print('-------------------')
print(f"Response with context:\n{response_with_context}")







