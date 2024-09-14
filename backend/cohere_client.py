from cohere import Client
import pandas as pd

class CohereClient:
    def __init__(self, api_key, data):
        print("Creating CohereClient....")
        self.cohere_client = Client(api_key=api_key)
        self.df = pd.DataFrame(data)
    
    def generate(self, index, top_k, generator_model_name, max_tokens, transformer_model, query):
        xq = transformer_model.encode([query]).tolist()
        xc = index.query(vector=xq, top_k=top_k)

        if not xc['matches']:
            return "No relevant information found."
        context_list = []
        for match in xc['matches']:
            top_result_id = match['id']
            context = self.df[self.df['id'] == top_result_id]['context'].values[0]
            context_list.append(context)
        combined_context = "\n\n".join(context_list)
        prompt = f"Context: {combined_context}\n\nQuestion: {query}\n\nAnswer:"
        print(prompt)
        response = self.cohere_client.generate(
            model=generator_model_name,
            prompt=prompt,
            max_tokens=max_tokens
        )
        return response.generations[0].text
