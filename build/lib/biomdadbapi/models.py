# -*- encoding: utf-8 -*-
# @File: models.py

from sqlmodel import SQLModel, Field, PrimaryKeyConstraint

class Compound2cid(SQLModel, table=True):
    __tablename__ = "compound2cid"
    md5sum: str = Field(primary_key=True)
    cid: str

class Cid2ssimcid(SQLModel, table=True):
    __tablename__ = "cid2ssimcid"
    cid: str = Field(primary_key=True)
    ssimcid: str

class Protein2stringid(SQLModel, table=True):
    __tablename__ = "protein2stringid"
    __table_args__ = (PrimaryKeyConstraint('protein', 'id'),)
    protein: str = Field()
    id: str

class Disease2doid(SQLModel, table=True):
    __tablename__ = "disease2doid"
    doid: str = Field(primary_key=True)
    disease: str
    superclass: str
    ngene: int

class Doid2gene(SQLModel, table=True):
    __tablename__ = "disease2gene"
    doid: str = Field(primary_key=True)
    entrezid: str

class PPI(SQLModel, table=True):
    __tablename__ = "ppi"
    __table_args__ = (PrimaryKeyConstraint('node1', 'node2'),)
    node1: str
    node2: str
    experiment: int
    fusion: int
    neighborhood: int
    cooccurence: int
    coexpression: int
    database: int
    textmining: int
    score: int

class Pnode(SQLModel, table=True):
    __tablename__ = "pnode"
    id: str = Field(primary_key=True)
    name: str
    entrezid: str
    description: str


class TargetProtein(SQLModel, table=True):
    __tablename__ = "tgtp"
    __table_args__ = (PrimaryKeyConstraint('node1', 'node2'),)
    node1: str
    node2: str
    score: int

class CPI(SQLModel, table=True):
    __tablename__ = "cpi"
    __table_args__ = (PrimaryKeyConstraint('node1', 'node2'),)
    node1: str
    node2: str
    experiment: int
    prediction: int
    database: int
    textmining: int
    score: int

class CCI(SQLModel, table=True):
    __tablename__ = "cci"
    __table_args__ = (PrimaryKeyConstraint('node1', 'node2'),)
    node1: str
    node2: str
    experiment: int
    database: int
    textmining: int
    score: int

class Cnode(SQLModel, table=True):
    __tablename__ = "cnode"
    id: str = Field(primary_key=True)
    name: str
    description: str

# class Cid2doid(SQLModel, table=True):
#     __tablename__ = "cid2doid"
#     __table_args__ = (PrimaryKeyConstraint('cid', 'doid', 'evidence', 'source'),)
#     cid: str
#     doid: str
#     pubmedid: str
#     evidence: str
#     source: str