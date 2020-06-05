import bolt4ds.flow as d6tflow
import cfg, tasks, visualize

# Check task dependencies and their execution status
d6tflow.preview(tasks.TaskTrain())

# Execute the model training task including dependencies. See https://d6tflow.readthedocs.io/en/latest/run.html
d6tflow.run(tasks.TaskTrain())
#d6tflow.run(GetLoginData(),scheduler_host="52.221.203.159",scheduler_port=1261,local_scheduler=False)

# use output
visualize.accuracy()
visualize.plot_importances()

# change parameter and rerun, see https://d6tflow.readthedocs.io/en/latest/advparam.html
d6tflow.run(tasks.TaskTrain(do_preprocess=False))
visualize.accuracy(do_preprocess=False) # task output is parameter specific

# rerun flow after code changes
import importlib
importlib.reload(cfg)
importlib.reload(tasks)

# say you changed TaskGetData, reset all tasks depending on TaskGetData
d6tflow.invalidate_downstream(tasks.TaskGetData(), tasks.TaskTrain())

d6tflow.preview(tasks.TaskTrain())
d6tflow.run(tasks.TaskTrain())