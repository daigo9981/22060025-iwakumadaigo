# 22060025-iwakumadaigo

ダジャレメーカー（Streamlit）

APIキー不要で動く、単語→ダジャレ生成アプリ

概要

単語を入力するとダジャレ案を自動生成するStreamlitアプリです。
外部APIはキー不要のものだけ（Wikipedia REST / Datamuse）を使用し、UIのコード（app.py）とロジック（pun_engine/）を分離しています。
CSVを使った**履歴・お気に入りの保存（簡易DB）**にも対応（加点要件）。

アプリの特徴

入力：単語（日本語/英語）、または.txt（1行1単語）をアップロードしてバッチ生成

出力：

日本語…テンプレ＋語感いじりで軽量ダジャレ

英語…Datamuseで韻を取得して軽めのダジャレを生成

Wikipedia RESTで用語の要約を表示（任意）

CSVデータベース（加点）

履歴：data/history.csv

お気に入り：data/favorites.csv（CSVダウンロード可）

UIとロジックを別ファイルに分割

使用しているAPI（APIキー不要）

Wikipedia REST API（Ja/En）

用語の要約取得に使用

例：https://ja.wikipedia.org/api/rest_v1/page/summary/カレー

Datamuse API（En）

英語の韻・近似音取得に使用

例：https://api.datamuse.com/words?rel_rhy=pizza

どちらも認証不要の公開APIです。今回の課題の要件を満たしています。

システム設計図 & コード説明図

システム設計図（自分のソフトウェア/外部サービスの関係が分かる図）


コード説明図（ファイル・主要関数の関係が分かる図）


PDF版：

assets/system_design.pdf

assets/code_layout.pdf

ディレクトリ構成
.
├─ app.py                  # Streamlit UI（入出力、タブ、CSV保存）
├─ pun_engine/             # ロジック層（API呼び出し・日本語ユーティリティ・CSVユーティリティ）
│  ├─ __init__.py
│  ├─ generator.py         # make_puns(), Wikipedia/Datamuse呼び出し, CSVヘルパー
│  └─ jp_utils.py          # 日本語判定/ひらがな→カタカナ変換
├─ assets/
│  ├─ system_design.png    # システム設計図（PNG）
│  ├─ system_design.pdf    # システム設計図（PDF）
│  ├─ code_layout.png      # コード説明図（PNG）
│  └─ code_layout.pdf      # コード説明図（PDF）
├─ data/                   # 実行時に作成（履歴/お気に入りのCSV）
│  ├─ history.csv
│  └─ favorites.csv
├─ requirements.txt
└─ README.md

セットアップ & 実行（ローカル）
# 1) 依存パッケージのインストール
pip install -r requirements.txt

# 2) アプリ起動
streamlit run app.py


ブラウザで http://localhost:8501 が開きます

data/配下にCSVが自動生成されます（権限が必要なので書き込み可能な場所で実行してください）

動作確認環境

Python 3.9+

Streamlit 1.34+

requests 2.31+

デプロイ（Streamlit Community Cloud）

GitHubでpublicレポジトリを作成

レポジトリ名：学籍番号_苗字_AIプログラミング課題2（例：2301201_山本_AIプログラミング課題2）

本プロジェクト一式をコミット＆プッシュ

Streamlit Community Cloud
 にログイン
→ New app → 対象レポジトリ/ブランチを選択 → Deploy

表示されたアプリURLを控える（提出用）

注意：Streamlit Cloudの永続ストレージはコンテナ再作成で消えることがあります。CSVは永続性を過信せず、必要に応じて手元にダウンロードしてください。

課題３
https://github.com/daigo9981/22060025-iwakumadaigo/blob/main/improvenemt.md
