# generate_response.py
import logging
import openai
import os
from dotenv import load_dotenv
load_dotenv()
from ml.query_retrieval import retrieve_context

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Azure OpenAI Configuration
openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")
openai.api_type = os.getenv("AZURE_API_TYPE")  
openai.azure_endpoint = os.getenv("AZURE_ENDPOINT")  
openai.api_version = os.getenv("AZURE_API_VERSION")

def generate_response(query, context, deployment_name="gpt-4", max_tokens=4000, temperature=0.7):
    try:
        messages = [
            {"role": "system", "content": "You are an AI assistant specializing in DORA compliance."},
            {"role": "user", "content": f"Query: {query}\nContext: {context}\nProvide a detailed response based on the context."}
        ]

        logging.info("Sending request to ChatCompletion API...")
        response = openai.chat.completions.create(
            model=deployment_name,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature
        )
        logging.info("Response received from ChatCompletion API.")
        return response.choices[0].message.content.strip()

    except openai.OpenAIError as e:
        logging.error(f"OpenAI API Error: {e}")
        return f"Error generating response: {e}"
    except Exception as e:
        logging.error(f"Unexpected Error: {e}")
        return f"Error: {e}"

if __name__ == "__main__":
    query = input("Enter your query: ").strip()
    context = retrieve_context(query, "embeddings/dora_index1")
    deployment_name = "gpt-4" 
    max_tokens = 4000
    temperature = 0.7
    logging.info("Generating response...")
    response = generate_response(query, context, deployment_name, max_tokens, temperature)
    print("\nGenerated Response:")
    print(response)
