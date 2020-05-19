from bolt4ds.flow.tasks import TaskData
from bolt4ds.flow.targets.h5 import H5PandasTarget, H5KerasTarget

class TaskH5Pandas(TaskData):
    """
    Task which saves to HDF5
    """
    target_class = H5PandasTarget
    target_ext = 'hdf5'

class TaskH5Keras(TaskData):
    """
    Task which saves to HDF5
    """
    target_class = H5KerasTarget
    target_ext = 'hdf5'