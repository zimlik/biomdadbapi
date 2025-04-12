# -*- encoding: utf-8 -*-
# @File: main.py

import uvicorn
from fastapi import FastAPI, HTTPException, Form
from . import crud
from .config import get_config

description = """
## Description

Building APIs for BioMDA Database via FastAPI framwork.

## Author

-   [Li Zhan](https://orcid.org/0009-0003-7470-7586) Creator & Maintainer
-   [Prof. Guangchuang Yu](https://orcid.org/0000-0002-6485-8781) Contributor

**YuLab** <https://yulab-smu.top/>

**Department of Bioinformatics, School of Basic Medical Sciences, Southern Medical University.**

-   [Dr. Huimin Zheng](https://orcid.org/0000-0003-3489-0964) Contributor

**Central Laboratory of the Medical Research Center, The First Affiliated Hospital of Ningbo University.**

## Contributing

We welcome any contributions! By participating in this project you agree
to abide by the terms outlined in the [Contributor Code of
Conduct](https://github.com/zimlik/biomdadbapi/blob/main/CONDUCT.md).

## Feedback
"""

app = FastAPI(
    title='biomdadbapi',
    summary='Building APIs for BioMDA Database via FastAPI framwork.',
    description=description,
    version='0.9.9',
    contact={
            'author': 'Li Zhan',
            'email': 'smu18575877413@gmail.com',
            'url': 'https://github.com/zimlik/biomdadbapi/issues',
    },
    license_info={'name': 'MIT',
                  'url': 'https://github.com/zimlik/biomdadbapi/blob/main/LICENSE'}
)

@app.get("/")
def read_root():
    return {'Title': 'biomdadbapi',
            'Author': 'Li Zhan',
            'Email': 'smu18575877413@gmail.com',
            'Description': 'Building APIs for BioMDA Database via FastAPI framwork.',
            'URL': 'https://github.com/zimlik/biomdadbapi'}

@app.post('/c2cid/')
async def biomdadb_compound2cid(md5sum: list[str]=Form()):
    res = await crud.sel_compound2cid(md5sum=md5sum)
    if (res is None):
        raise HTTPException(status_code=404)
    else:
        return res

@app.post('/cid2info/')
async def biomdadb_cid2info(cid: list[str]=Form()):
    res = await crud.sel_cid2info(cid=cid)
    if (res is None):
        raise HTTPException(status_code=404)
    else:
        return res

@app.post('/stringid2info/')
async def biomdadb_stringid2info(stringid: list[str]=Form()):
    res = await crud.sel_stringid2info(stringid=stringid)
    if (res is None):
        raise HTTPException(status_code=404)
    else:
        return res

@app.post('/cid2ssimcid/')
async def biomdadb_cid2ssimcid(cid: list[str]=Form()):
    res = await crud.sel_cid2ssimcid(cid=cid)
    if (res is None):
        raise HTTPException(status_code=404)
    else:
        return res

@app.post('/disease2doid/')
async def biomdadb_disease2doid(disease: str=Form(), fixed: bool=Form()):
    res = await crud.sel_disease2doid(disease=disease, fixed=fixed)
    if (res is None):
        raise HTTPException(status_code=404)
    else:
        return res

@app.post('/doid2gene/')
async def biomdadb_doid2gene(doid: str=Form()):
    res = await crud.sel_doid2gene(doid=doid)
    if (res is None):
        raise HTTPException(status_code=404)
    else:
        return res

@app.post('/protein2stringid/')
async def biomdadb_protein2stringid(protein: list[str]=Form()):
    res = await crud.sel_protein2stringid(protein=protein)
    if (res is None):
        raise HTTPException(status_code=404)
    else:
        return res

@app.post('/stringppi/v12/')
async def biomdadb_string_ppi(stringid: list[str]=Form(), score: int=Form()):
    res = await crud.sel_string_ppi(stringid=stringid, score=score)
    if (res is None):
        raise HTTPException(status_code=404)
    else:
        return res

@app.post('/targetcpi/v5/')
async def biomdadb_expt_cpi(cid: list[str]=Form(), score: int=Form()):
    res = await crud.sel_tgtp_cpi(cid=cid, score=score)
    if (res is None):
        raise HTTPException(status_code=404)
    else:
        return res

@app.post('/stitchcpi/v5/')
async def biomdadb_stitch_cpi(cid: list[str]=Form(), score: int=Form()):
    res = await crud.sel_stitch_cpi(cid=cid, score=score)
    if (res is None):
        raise HTTPException(status_code=404)
    else:
        return res

def main():
    conf_opt = get_config()
    host = conf_opt.get('host')
    port = conf_opt.get('port')
    port = int(port)
    uvicorn.run(app='biomdadbapi.main:app', host=host, port=port)