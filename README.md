# estat-RAPIDS

- e-StatでAPIになっていないリソースを中心にAPI化してみた
- estat `R`esource `API` for `D`eveloper and `D`ata scientist use `S`imply
- すぐ使える = RAPID ともかけてます

## 実行方法

1. docker composeでコンテナ起動

``` shell
cd estat-RAPID
docker compose up -d
```

2. http://localhost:1236/docs/ にアクセス

![image](https://github.com/tsutomu-nagano/estat-sac/assets/59475213/b329031f-4946-4b81-8592-d0330ab88f21)

## 備考

- 市区町村の一覧はダウンロード用のURLのパスクエリーで取得されるデータがかわるので、APIのスキーマをそのパスクエリ―にあてはめればよいが確認するのがめんどい

## 機能

### 標準地域に関するもの

- e-Statの 統計関連情報 > 市区町村名・コード > 市区町村を探す からデータを取得 で取得できるデータを扱う
  ![image](https://github.com/tsutomu-nagano/estat-sac/assets/59475213/ca692b95-6828-4fa8-a00b-b3b3210219a7)

1. 日付（yyyymmdd）で指定してデータを取得できる
2. 今のところは全都道府県の市、区、町、村のデータのみ
