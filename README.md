# biomdadbapi
## :newspaper: Description
Building APIs for BioMDA Database via FastAPI framwork.
## :writing_hand: Author

-   [Li Zhan](https://orcid.org/0009-0003-7470-7586) Creator & Maintainer
-   [Prof. Guangchuang Yu](https://orcid.org/0000-0002-6485-8781) Contributor

**YuLab** <https://yulab-smu.top/>

**Department of Bioinformatics, School of Basic Medical Sciences, Southern Medical University.**

-   [Dr. Huimin Zheng](https://orcid.org/0000-0003-3489-0964) Contributor

**Central Laboratory of the Medical Research Center, The First Affiliated Hospital of Ningbo University.**



## Program Dependencies: Installation

Python3: https://www.python.org (version >= 3.12)

To install the biomdaapi package in python3, simply type.

Shell:
```bash
git clone https://github.com/zimlik/biomdadbapi
cd biomdadbapi
python3 setup.py install
```

## :arrow_double_down: Run APIs of biomdadbapi and access to BioMDA database

To add path of BioMDA database for config.

Shell:
```bash
biomdadb-show-config
## [defualt]
## database = 
## host = 127.0.0.1
## port = 8000
## 
## ******
## Execute biomdadb-add-config to add options for defualt config.
## biomdadb-add-config -h
## ******

biomdadb-add-config -d ~/Databases/BioMDA.db
## Add options for section[defualt] in /root/Softwares/Python-3.12.3/lib/python3.12/site-packages/biomdadbapi/BioMDA-DB.cfg
## Add database: ~/Databases/BioMDA.db
## Add database: 127.0.0.1
## Add database: 8000
```

To build APIs.

Shell:
```bash
biomdadb-api
## INFO:     Started server process [170043]
## INFO:     Waiting for application startup.
## INFO:     Application startup complete.
## INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

To accesse BioMDA database using HTTP POST method in R.

Interactive R session:
``` r
# install.packages(c("RCurl", "jsonlite"))
library(RCurl)
library(jsonlite)

uri <- "http://127.0.0.1:8000/protein2stringid/"
protein <- c("PTCH1", "TP53", "BRCA1", "BRCA2")
resp <- postForm(uri = uri, .params = list(protein = protein)) |>
  fromJSON()
resp
## $p2string
##   protein       stringv12
## 1    TP53 ENSP00000269305
## 2   PTCH1 ENSP00000332353
## 3   BRCA2 ENSP00000369497
## 4   BRCA1 ENSP00000418960
```

## :sparkling_heart: Contributing

We welcome any contributions! By participating in this project you agree
to abide by the terms outlined in the [Contributor Code of
Conduct](CONDUCT.md).