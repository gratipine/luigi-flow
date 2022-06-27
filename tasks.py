import luigi
import pandas as pd

## Load data
class LoadData(luigi.Task):
    param = luigi.Parameter(42)

    def requires(self):
        None
    
    def run():
        data = pd.read_feather("data/data_in")
    
    def output(self):
        return luigi.LocalTarget(f"cache/data_out_{param}")

## Transform data
class TransformData(luigi.Task):

    def requires(self):
        return LoadData(self.date)
    
    def run():
        data = pd.read_feather("data/data_in")
    
    def output(self):
        data.to_feather(f"cache/data_tranformed_{param}")
        return luigi.LocalTarget(f"cache/data_tranformed_{param}")

## Train
class Train(luigi.Task):

    def requires(self):
        return TransformData(self.date)
    
    def run():
        data = pd.read_feather(f"cache/data_tranformed_{param}")
        model = algo.Model()
        model.train(data)
    
    def output(self):
        model.to_pickle(f"cache/model_{param}")
        return luigi.LocalTarget(f"cache/model_{param}")

## create output
class Predict(luigi.Task):

    def requires(self):
        return Train(self.date)
    
    def run():
        model = algo.Model()
        model.train()
    
    def output(self):
        data.to_feather(f"cache/data_tranformed_{param}")
        return luigi.LocalTarget(f"cache/data_tranformed_{param}")

## Wrap
class Tasks(luigi.Task):
    def requires(self):
        return Predict(self.date)