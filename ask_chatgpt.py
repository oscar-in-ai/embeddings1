import os
import openai
import docx2txt

api_key = os.getenv("openai_api_key")
openai.api_key = api_key

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


query = "What is an ethical way to distribute the burdens of climate change?"


response_no_context = ask_gpt3(query)
embedding_vector = get_openai_embedding (query)



import os
import pinecone

pinecone_api_key = os.getenv("pinecone_api_key")
pinecone.init(api_key=pinecone_api_key, environment='us-east-1-aws')

index_name = 'my-assignments2'
namespace = 'assignments'

def query_pinecone_index(embedding_vector):
    index = pinecone.Index(index_name=index_name)
    response = index.query(namespace=namespace,queries=[embedding_vector],top_k=2, include_metadata=True)
    results = response.results[0]['matches']
    

    # Assuming you have stored some metadata along with the embeddings,
    # you can retrieve it using the `results.ids` and `results.distances` attributes.


    return results

candidates = query_pinecone_index(embedding_vector)
selected_file = candidates[0]['metadata']['file_name']
print(selected_file)

my_context = text = docx2txt.process(selected_file)

response_with_context = ask_gpt3(f"Answer this question: {query} using the following document as context only if appropriate: {my_context}")

print(response_no_context)
print('-------------------')
print(response_with_context)







