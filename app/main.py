
from typing import List
from fastapi import Depends, FastAPI, File, UploadFile, Form, HTTPException, Query
from pydantic import BaseModel
from fastapi.responses import StreamingResponse, PlainTextResponse, FileResponse, JSONResponse
from fastapi.encoders import jsonable_encoder

from pathlib import Path
import tempfile
import re
import csv

import requests
import fitz
import pandas as pd


tags_metadata = [
    {
        "name": "sac",
        "description": "標準地域の機能"
    },
    {
        "name": "catalog",
        "description": "統計の一覧等の機能"
    }

]


app = FastAPI(
    title="e-Stat RAPIDS",
    description="e-Statのリソースを取得するAPI",
    version="0.0.1",
    openapi_tags=tags_metadata
)



@app.get("/simple.csv", tags = ["sac"], response_class=StreamingResponse)
def get_simple_csv(search_date: str): 

    destFileName = f"sac_{search_date}.csv"

    yyyy = int(search_date[0:4])
    mm = int(search_date[4:6])
    dd = int(search_date[6:8])

    # page = 1

    url = f"https://www.e-stat.go.jp/municipalities/cities/areacode?date_year={yyyy}&date_month={mm}&date_day={dd}&prefecture_all=on&pf%5B1%5D=1&pf%5B2%5D=2&pf%5B3%5D=3&pf%5B4%5D=4&pf%5B5%5D=5&pf%5B6%5D=6&pf%5B7%5D=7&pf%5B8%5D=8&pf%5B9%5D=9&pf%5B10%5D=10&pf%5B11%5D=11&pf%5B12%5D=12&pf%5B13%5D=13&pf%5B14%5D=14&pf%5B15%5D=15&pf%5B16%5D=16&pf%5B17%5D=17&pf%5B18%5D=18&pf%5B19%5D=19&pf%5B20%5D=20&pf%5B21%5D=21&pf%5B22%5D=22&pf%5B23%5D=23&pf%5B24%5D=24&pf%5B25%5D=25&pf%5B26%5D=26&pf%5B27%5D=27&pf%5B28%5D=28&pf%5B29%5D=29&pf%5B30%5D=30&pf%5B31%5D=31&pf%5B32%5D=32&pf%5B33%5D=33&pf%5B34%5D=34&pf%5B35%5D=35&pf%5B36%5D=36&pf%5B37%5D=37&pf%5B38%5D=38&pf%5B39%5D=39&pf%5B40%5D=40&pf%5B41%5D=41&pf%5B42%5D=42&pf%5B43%5D=43&pf%5B44%5D=44&pf%5B45%5D=45&pf%5B46%5D=46&pf%5B47%5D=47&ht=&city_nm=&city_kd%5B4%5D=4&city_kd%5B5%5D=5&city_kd%5B6%5D=6&city_kd%5B7%5D=7&keyword_kd=code&item%5B%5D=htCode&item%5B%5D=todoNm&item%5B%5D=parentCityNm&item%5B%5D=parentCityKana&item%5B%5D=selfCityNm&item%5B%5D=selfCityKana&item%5B%5D=htCodeSDate&item%5B%5D=jiyuId&sort%5B%5D=htCode-asc&choices_to_show%5B%5D=cityType&choices_to_show%5B%5D=kasoFlg&choices_to_show%5B%5D=htCodeKokujiDate&choices_to_show%5B%5D=htCodeKokujiNo&choices_to_show%5B%5D=htCodeEDate&choices_to_sort%5B%5D=kasoFlg&choices_to_sort%5B%5D=htCodeSDate&choices_to_sort%5B%5D=htCodeEDate&choices_to_sort%5B%5D=htCodeKokujiDate&choices_to_sort%5B%5D=htCodeKokujiNo&choices_to_sort_value%5B%5D=htCode-desc&choices_to_sort_value%5B%5D=kasoFlg-asc&choices_to_sort_value%5B%5D=kasoFlg-desc&choices_to_sort_value%5B%5D=htCodeSDate-asc&choices_to_sort_value%5B%5D=htCodeSDate-desc&choices_to_sort_value%5B%5D=htCodeEDate-asc&choices_to_sort_value%5B%5D=htCodeEDate-desc&choices_to_sort_value%5B%5D=htCodeKokujiDate-asc&choices_to_sort_value%5B%5D=htCodeKokujiDate-desc&choices_to_sort_value%5B%5D=htCodeKokujiNo-asc&choices_to_sort_value%5B%5D=htCodeKokujiNo-desc&form_id=city_areacode_form&source=setup&page=&file_format=csv&charset=UTF-8&bom=1&op=download"

    res = requests.get(url)

    return StreamingResponse(iter([res.content]), media_type="text/csv; charset=utf-8-sig")




@app.get("/statlist.csv", tags = ["catalog"], response_class=StreamingResponse)
def get_statlist_csv(): 

    domains = [
        "防衛省",
        "総務省",
        "環境省",
        "内閣府",
        "内閣官房",
        "人事院",
        "国土交通省",
        "中小企業庁",
        "資源エネルギー庁",
        "経済産業省",
        "農林水産省",
        "林野庁",
        "こども家庭庁",
        "厚生労働省",
        "海上保安庁",
        "観光庁",
        "特許庁",
        "水産庁",
        "文部科学省",
        "国税庁",
        "財務省",
        "消防庁",
        "法務省",
        "中央労働委員会",
        "公害等調整委員会",
        "文化庁",
        "外務省",
        "個人情報保護委員会",
        "警察庁",
        "公正取引委員会",
        "消費者庁",
        "スポーツ庁"
    ]

    statkinds = [
        "一般統計業務統計",
        "基幹統計・加工統計",
        "基幹統計",
        "一般統計",
        "業務統計",
        "加工統計",
        "その他"
    ]


    domain_ptn = f"({'|'.join(domains)})"
    statkind_ptn = f"({'|'.join(statkinds)})"


    url = "https://www.e-stat.go.jp/estat/html/tokei_itiran.pdf"

    res = requests.get(url)

    with  tempfile.NamedTemporaryFile(dir = "/code/app", suffix=".csv") as tf:
        with open (tf.name,mode = "wb") as f:
            f.write(res.content)

        doc = fitz.open(tf.name)

        datas = []
        for page in doc:

            text = page.get_text("text")
            text = re.sub("([0-9]{8})", "\r\n\\1", text)

            for t in re.split("\r\n", text):
                values = t.split("\n")

                statcode = values[0]

                s = re.sub(f"{domain_ptn}+" ,"\\1", "".join(values[1:]))

                if not re.match("^(政府統計)?コード",s):

                    values = re.split(domain_ptn, s)
                    values = [v  for index, v in enumerate(values) if v.strip() != ""]

                    if re.match(domain_ptn, values[0]):
                        temp = values[0] + values[1]
                        values = [temp] + values[2:]

                    statname = values[0]
                    organization = values[1]

                    # data = values[2]
                    # values = re.split(statkind_ptn, data)
                    # contact = values[0]
                    # statkind = values[1]

                    datas.append({
                        "statcode": statcode,
                        "statname": statname,
                        "organization": organization
                        # "contact": contact,
                        # "data": data
                        })


        df = pd.DataFrame(datas)
        df = df[df["statcode"].str.match("[0-9]{8}")]

        return StreamingResponse(iter([df.to_csv(index = False, quoting=csv.QUOTE_ALL)]), media_type="text/csv; charset=utf-8-sig")


@app.get("/statdata.csv", tags = ["search"], response_class=JSONResponse)
def get_statdata():

    return JSONResponse({"TEST": "HOGE"}) 
