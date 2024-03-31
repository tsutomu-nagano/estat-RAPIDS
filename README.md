# estat-RAPIDS

- e-StatでAPIになっていないリソースを中心にAPI化してみた
- estat `R`esource `API` for `D`eveloper and `D`ata scientist use `S`imply
- すぐ使える = RAPID ともかけてます

## 実行方法

1. docker composeでコンテナ起動

    ``` shell
    cd estat-RAPIDS
    docker compose up -d
    ```

2. <http://localhost:1236/docs/> にアクセス

    ![image](https://github.com/tsutomu-nagano/estat-RAPIDS/assets/59475213/090c3622-da1a-44f5-a537-c57fcc3db5b0)

## 機能

### 🗾 標準地域に関する機能

- e-Statの 統計関連情報 > 市区町村名・コード > 市区町村を探す からデータを取得 で取得できるデータを扱う
  ![image](https://github.com/tsutomu-nagano/estat-sac/assets/59475213/ca692b95-6828-4fa8-a00b-b3b3210219a7)

1. 日付（yyyymmdd）で指定してデータを取得できる
2. 今のところは全都道府県の市、区、町、村のデータのみ

- 備考
  - 市区町村の一覧はダウンロード用のURLのパスクエリーで取得されるデータがかわるので、APIのスキーマをそのパスクエリ―にあてはめればよいが確認するのがめんどい

### :clipboard:  統計の一覧等に関する機能

- e-Statの お問い合わせ > お問い合わせ先一覧 のPDFから取得できるデータを扱う

1. 政府統計コード、政府統計名、府省名を取得できる

## その他

- renderにもデプロイしてます
- 🌐 <https://estat-rapids.onrender.com/docs>
- 無料枠なので動かない場合あるかも・・・ 😭