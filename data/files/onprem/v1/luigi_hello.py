from bolt4ds import flow as d6tflow
import bolt4ds.flow.tasks
import luigi
import pandas as pd

# define 2 tasks that load raw data
class Task1(d6tflow.tasks.TaskPqPandas):
    
    def run(self):
        df = pd.DataFrame({'a':range(3)})
        self.save(df) # quickly save dataframe

class Task2(Task1):
    pass

# define another task that depends on data from task1 and task2
@d6tflow.requires(Task1,Task2)
class Task3(d6tflow.tasks.TaskPqPandas):
    multiplier = luigi.IntParameter(default=2)
    
    def run(self):
        df1 = self.input()[0].load() # quickly load input data
        df2 = self.input()[1].load() # quickly load input data
        df = df1.join(df2, lsuffix='1', rsuffix='2')
        df['b']=df['a1']*self.multiplier # use task parameter
        self.save(df)

# Execute task including all its dependencies
d6tflow.run(Task3())
'''
* 3 ran successfully:
    - 1 Task1()
    - 1 Task2()
    - 1 Task3(multiplier=2)
'''

Task3().outputLoad() # quickly load output data. Task1().outputLoad() also works
'''
   a1  a2  b
0   0   0  0
1   1   1  2
2   2   2  4
'''

# Intelligently rerun workflow after changing parameters
d6tflow.preview(Task3(multiplier=3))
'''
└─--[Task3-{'multiplier': '3'} (PENDING)] => this changed and needs to run
   |--[Task1-{} (COMPLETE)] => this doesn't change and doesn't need to rerun
   └─--[Task2-{} (COMPLETE)] => this doesn't change and doesn't need to rerun
'''
