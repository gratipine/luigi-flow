import luigi
import pandas as pd
import src.algo as algo
import src.data_in as dt_in
from setup import token
import pickle
import src.data_prep as prep
import os
import datetime
import logging

logger = logging.Logger("__main__")

## Load data
class LoadData(luigi.Task):
    last_date_of_report = luigi.Parameter(default=datetime.date.today())

    def requires(self):
        None
    
    def run(self):
        tweet_fields = "tweet.fields=text,author_id,created_at"
        print(self.last_date_of_report - datetime.timedelta(days=6))
        since = f"start_time={str(self.last_date_of_report - datetime.timedelta(days=6))}T19:16:12.000Z"
        query="from: ECONdailycharts"

        out = dt_in.search_twitter(query, tweet_fields, since, token)
        filehandler = open(self.output().path, 'wb') 
        pickle.dump(out, filehandler)
    
    def output(self):
        return luigi.LocalTarget(f"cache\data_out_{self.last_date_of_report}.pkl")

## Transform data
class TransformData(luigi.Task):
    last_date_of_report = luigi.Parameter(default=datetime.date.today())

    def requires(self):
        return LoadData(self.last_date_of_report)
    
    def run(self):
        filehandler = open(f"cache\data_out_{self.last_date_of_report}.pkl", 'rb') 
        out = pickle.load(filehandler)

        out_df, tokens_list = prep.transform_data(out)
        out_df.to_feather(self.output().path)
        
        filehandler = open(f"cache/tokens_list_{self.last_date_of_report}.pkl", 'wb') 
        pickle.dump(tokens_list, filehandler)
        
    def output(self):
        return luigi.LocalTarget(f"cache/data_transformed_{self.last_date_of_report}")


## create output
class Render(luigi.Task):
    last_date_of_report = luigi.Parameter(default=datetime.date.today())

    def requires(self):
        return TransformData(self.last_date_of_report)
    
    def run(self):
        command = (
            f"""papermill -p date "{str(self.last_date_of_report)}" scripts/template.ipynb cache/parametrized.ipynb"""
        )
        os.system(f'cmd /c {command}')
        
        command = (
            """jupyter nbconvert --to pdf cache/parametrized.ipynb""" + 
            f""" --output {self.output().path} --TagRemovePreprocessor.enabled=True""" +
            """ --TagRemovePreprocessor.remove_cell_tags remove-cell""" + 
            """ --TagRemovePreprocessor.remove_input_tags input-cell"""
        )
        os.system(f'cmd /c {command}')

    def output(self):
        return luigi.LocalTarget(f"template.pdf")

## Wrap
class Tasks(luigi.Task):
    def requires(self):
        return Render(self.date)

if __name__ == "main":
    luigi.run()