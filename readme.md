# CNZZ ICP domain crawler


## Install
``` bash
pip3 install -r requirements.txt
```

## Usage
```
python3 ./get.py -h
usage: get.py [-h] -d DATABASE -s STARTDATE [-p PROVINCE]

optional arguments:
  -h, --help            show this help message and exit
  -d DATABASE, --database DATABASE
                        SQLite database name
  -s STARTDATE, --startdate STARTDATE
                        start date (YYYYMMDD)
  -p PROVINCE, --province PROVINCE
                        the province to get, if not assigned crawl all
```