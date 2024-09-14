import json
import datasets
import pandas as pd
class Dataset:
    def __init__(self,  dataset_path, transformer_model, context):
        print("Accessing Data....")
        try:
            with open(dataset_path, 'r') as f:
                self.data = datasets.Dataset.from_pandas(pd.DataFrame(json.load(f)))
        except:
            self.data = datasets.load_dataset('squad', split='validation')
        if self.data is None:
            self.data = datasets.load_dataset('squad', split='validation')
        self.data = self.data.map(lambda x: {'encoding': transformer_model.encode(x[context]).tolist()}, batched=True, batch_size=32)