# -*- encoding: utf-8 -*-
# @File : database.py

from sqlmodel import create_engine
from .config import get_config

conf_opt = get_config()
sqlite_file_name = conf_opt.get('db')
sqlite_url = f"sqlite:///{sqlite_file_name}"
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)