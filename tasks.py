import luigi
import pandas as pd
import src.algo as algo


## Load data
class LoadData(luigi.Task):
    param = luigi.Parameter(default=42)

    def requires(self):
        None
    
    def run(self):
        data = pd.read_csv("data/data_in.csv")
    
    def output(self):
        return luigi.LocalTarget(f"cache/data_out_{self.param}")

## Transform data
class TransformData(luigi.Task):
    param = luigi.Parameter(42)
    def requires(self):
        return LoadData(self.date)
    
    def run(self):
        data = pd.read_feather("data/data_in")
    
    def output(self):
        data.to_feather(f"cache/data_tranformed_{param}")
        return luigi.LocalTarget(f"cache/data_tranformed_{param}")

## Train
class Train(luigi.Task):
    param = luigi.Parameter(42)
    
    def requires(self):
        return TransformData(self.date)
    
    def run(self):
        data = pd.read_feather(f"cache/data_tranformed_{param}")
        model = algo.Model()
        model.train(data)
    
    def output(self):
        model.to_pickle(f"cache/model_{param}")
        return luigi.LocalTarget(f"cache/model_{param}")

## create output
class Predict(luigi.Task):
    param = luigi.Parameter(42)

    def requires(self):
        return Train(self.date)
    
    def run(self):
        model = algo.Model()
        model.train()
    
    def output(self):
        data.to_feather(f"cache/data_tranformed_{param}")
        return luigi.LocalTarget(f"cache/data_tranformed_{param}")

## Wrap
class Tasks(luigi.Task):
    def requires(self):
        return Predict(self.date)