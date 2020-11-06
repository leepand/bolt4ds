from pathlib import Path, PurePosixPath
from .common.appdirs import AppDirs

props_dict ={"user_data_dir":"user_data_dir",
             "user_config_dir":"user_config_dir",
             "user_cache_dir":"user_cache_dir",
             "user_state_dir":"user_state_dir",
             "user_log_dir":"user_log_dir",
             "site_data_dir":"site_data_dir",
             "site_config_dir":"site_config_dir"}

appname="algolink"
appauthor="algolink"
print("-- app dirs (with optional 'version')")
dirs = AppDirs(appname, appauthor, version="1.0")

DATA_DIR=getattr(dirs,props_dict["user_data_dir"])
CONFIG_DIR=getattr(dirs,props_dict["user_config_dir"])

CACHE_DIR = getattr(dirs,props_dict["user_cache_dir"])

REPOSITORY_CACHE_DIR = Path(CACHE_DIR) / "cache" / "repositories"