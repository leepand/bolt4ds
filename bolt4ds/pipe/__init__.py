import bolt4ds.pipe.api as api
import bolt4ds.pipe.pipe as pipe
import bolt4ds.pipe.utils as utils

from bolt4ds.pipe.pipe import Pipe, PipeLocal
from bolt4ds.pipe.api import APIClient, APILocal
from bolt4ds.pipe.api import upsert_resource, upsert_pipe, upsert_permissions, upsert_pipe_json, list_profiles

print('Welcome to filepipe for ds!')# We hope you find it useful. If you run into any problems please raise an issue on github at https://github.com/d6t/d6tpipe')

import bolt4ds.collect as bolt4dscollect
bolt4dscollect.submit = False