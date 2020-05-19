from bolt4ds.flow.tasks import TaskData
from bolt4ds.flow.targets.dt import DatatableTarget

class TaskDatatable(TaskData):
    """
    Task which saves to H2O data.table
    """
    target_class = DatatableTarget
    target_ext = 'nff'