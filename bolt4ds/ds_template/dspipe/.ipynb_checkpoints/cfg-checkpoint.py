do_preprocess = True

import datetime
dt_start = datetime.date(2020,6,1)
dt_end = datetime.date(2020,12,1)

# load protected credentials
try:
    import d6tpipe
    uri = d6tpipe.utils.loadyaml('.creds.yaml').get('uri')
except:
    pass