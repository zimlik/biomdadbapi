# -*- encoding: utf-8 -*-
# @File: utilities.py

def row_to_dict(tbl, sql):
    row2dict = [{column.name: getattr(row, column.name) for column in
                 tbl.__table__.columns} for row in sql]
    return row2dict