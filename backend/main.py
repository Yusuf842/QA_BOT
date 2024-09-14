import warnings
warnings.filterwarnings("ignore")
from .dataset import Dataset
from .cohere_client import CohereClient
from .pinecone_client import PineconeClient
from sentence_transformers import SentenceTransformer

class QA:
    def qa_setup(self, PINECONE_API_KEY, COHERE_API_KEY, transformer_model=SentenceTransformer('multi-qa-MiniLM-L6-cos-v1'), dataset_path='data/data.json', context = 'context', enviroment='YOUR_ENV', name='qa-index'):
        self.transformer_model = transformer_model
        self.data = Dataset(dataset_path=dataset_path, transformer_model=self.transformer_model, context=context).data
        self.index = PineconeClient(api_key=PINECONE_API_KEY, data=self.data, environment=enviroment).get_index(name=name)
        self.cohere_client = CohereClient(api_key=COHERE_API_KEY, data=self.data)

    def answer(self, query='Where did Super Bowl 50 take place?', top_k= 3, generator_model_name='command', max_tokens=150):
        return self.cohere_client.generate(index=self.index, top_k = top_k,generator_model_name=generator_model_name, max_tokens=max_tokens, transformer_model=self.transformer_model,query=query)