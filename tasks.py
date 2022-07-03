import luigi
import pandas as pd
import src.algo as algo
import src.data_in as dt_in
from setup import token
import pickle
import src.data_prep as prep
import os

## Load data
class LoadData(luigi.Task):
    param = luigi.Parameter(default=42)

    def requires(self):
        None
    
    def run(self):
        tweet_fields = "tweet.fields=text,author_id,created_at"
        since = "start_time=2022-06-26T19:16:12.000Z"
        query="from: ECONdailycharts"

        out = dt_in.search_twitter(query, tweet_fields, since, token)
        filehandler = open(f"cache\data_out_{self.param}.pkl", 'wb') 
        pickle.dump(out, filehandler)
    
    def output(self):
        return luigi.LocalTarget(f"cache\data_out_{self.param}.pkl")

## Transform data
class TransformData(luigi.Task):
    param = luigi.Parameter(42)
    def requires(self):
        return LoadData(self.param)
    
    def run(self):
        filehandler = open(f"cache\data_out_{self.param}.pkl", 'rb') 
        out = pickle.load(filehandler)

        out_df, tokens_list = prep.transform_data(out)
        out_df.to_feather(f"cache/data_tranformed_{self.param}")
        
        filehandler = open(f"cache/tokens_list_{self.param}.pkl", 'wb') 
        pickle.dump(tokens_list, filehandler)
        
    def output(self):
        return luigi.LocalTarget(f"cache/data_tranformed_{self.param}")


## create output
class Predict(luigi.Task):
    param = luigi.Parameter(42)

    def requires(self):
        return TransformData(self.date)
    
    def run(self):
        model = algo.Model()
        model.train()
    
    def output(self):
        return luigi.LocalTarget(f"cache/data_tranformed_{param}")

## Wrap
class Tasks(luigi.Task):
    def requires(self):
        return Predict(self.date)