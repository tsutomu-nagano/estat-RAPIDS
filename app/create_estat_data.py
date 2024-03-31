

import requests
import pandas as pd
import csv
import re
import sys
from pathlib import Path

def class2df(classobj):

    df = pd.json_normalize(classobj["CLASS"])

    df["classname"] = classobj["@name"]
    df["type"] = re.sub("[0-9]+", "", classobj["@id"])

    return(df)

def db2df(appid, statsdataid):
    url = f"http://api.e-stat.go.jp/rest/3.0/app/json/getMetaInfo?appId={appid}&statsDataId={statsdataid}"
    res = requests.get(url)
    meta = pd.concat([class2df(classobj) for classobj in res.json()["GET_META_INFO"]["METADATA_INF"]["CLASS_INF"]["CLASS_OBJ"]])
    meta["statsdataid"] = statsdataid
    return(meta)

def create_estat_data(statcode, appid, dest_dir):

    url = f"http://api.e-stat.go.jp/rest/3.0/app/json/getStatsList?appId={appid}&statsCode={statcode}&searchKind=1"

    res = requests.get(url)

    df = pd.concat([pd.json_normalize(tableinf) for tableinf in res.json()["GET_STATS_LIST"]["DATALIST_INF"]["TABLE_INF"]])

    dest = Path(dest_dir) / "datalist.csv"
    df.to_csv(str(dest), index = None, quoting = csv.QUOTE_ALL)

    meta = pd.concat([db2df(appid, statsdataid) for statsdataid in df["@id"]]).drop_duplicates()
    
    dest = Path(dest_dir) / "meta.csv"
    meta.to_csv(str(dest), index = None, quoting = csv.QUOTE_ALL)


if __name__ == "__main__": 
    args = sys.argv
    statcode = args[1]
    appid = args[2]
    dest_dir = args[3]
    create_estat_data(statcode, appid, dest_dir)

