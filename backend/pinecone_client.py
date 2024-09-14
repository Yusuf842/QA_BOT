import pinecone
from tqdm.auto import tqdm

class PineconeClient:
  def __init__(self, api_key, data, environment):
    print("Creating Pinecone Client....")
    self.data = data
    self.dimension = len(self.data[0]['encoding'])
    self.client = pinecone.Pinecone(api_key=api_key, environment=environment)

  def get_index(self, name):
    print("Creating Pinecone Index....")
    if not name in self.client.list_indexes().names():
      self.client.create_index(name=name, dimension=self.dimension)
    self.index = self.client.Index(name)
    upserts = [(v['id'], v['encoding']) for v in self.data]
    for i in tqdm(range(0, len(upserts), 50)):
        i_end = i + 50
        if i_end > len(upserts): i_end = len(upserts)
        self.index.upsert(vectors=upserts[i:i_end])
    return self.index