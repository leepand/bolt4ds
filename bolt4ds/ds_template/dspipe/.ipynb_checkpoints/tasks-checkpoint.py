#import d6tflow
import bolt4ds.flow as d6tflow
import bolt4ds.flow.tasks
import luigi
import sklearn, sklearn.datasets
from sklearn.ensemble import RandomForestClassifier
import pandas as pd


import cfg

# define workflow
class TaskGetData(d6tflow.tasks.TaskPqPandas):  # save dataframe as parquet, see https://d6tflow.readthedocs.io/en/latest/targets.html
    dt_start = luigi.DateParameter(default=cfg.dt_start) # workflow parameters. See https://d6tflow.readthedocs.io/en/latest/advparam.html
    dt_end = luigi.DateParameter(default=cfg.dt_end)
    scheduler_host = luigi.Parameter(
        default='localhost',
        description='Hostname of machine running remote scheduler',
        config_path=dict(section='core', name='default-scheduler-host'))
    scheduler_port = luigi.IntParameter(
        default=8082,
        description='Port of remote scheduler api process',
        config_path=dict(section='core', name='default-scheduler-port'))

    def run(self):
        iris = sklearn.datasets.load_iris()
        df_train = pd.DataFrame(iris.data,columns=['feature{}'.format(i) for i in range(4)])
        df_train['y'] = iris.target
        # optional: df_train[df_train['date']>=self.dt_start]
        self.save(df_train) # quickly save dataframe

@d6tflow.requires(TaskGetData) # define dependency. See https://d6tflow.readthedocs.io/en/latest/tasks.html
class TaskPreprocess(d6tflow.tasks.TaskPqPandas):
    do_preprocess = luigi.BoolParameter(default=cfg.do_preprocess) # parameter for preprocessing yes/no

    def run(self):
        df_train = self.input().load() # quickly load required data, see https://d6tflow.readthedocs.io/en/latest/tasks.html#load-input-data
        if self.do_preprocess:
            df_train.iloc[:,:-1] = sklearn.preprocessing.scale(df_train.iloc[:,:-1])
        self.save(df_train) # save task output, see https://d6tflow.readthedocs.io/en/latest/tasks.html#save-output-data

@d6tflow.requires(TaskPreprocess) # define dependency. See https://d6tflow.readthedocs.io/en/latest/tasks.html
class TaskTrain(d6tflow.tasks.TaskPickle): # save output as pickle

    def run(self):
        df_train = self.input().load()
        model = RandomForestClassifier(n_jobs=2, random_state=0)
        model.fit(df_train.iloc[:,:-1], df_train['y'])
        self.save(model)