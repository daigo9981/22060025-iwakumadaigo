
import streamlit as st
from pun_engine import make_puns, append_csv, read_csv, ensure_csv
import datetime
import io
import csv

st.set_page_config(page_title="ダジャレメーカー ✨", page_icon="🎎", layout="centered")

st.title("ダジャレメーカー 🎤")
st.caption("単語を入れるとダジャレ案を自動生成。キー不要APIのみ使用（Wikipedia / Datamuse）。")

# --- CSV "DB" paths (persist on Streamlit Cloud)
HIST_PATH = "data/history.csv"
FAV_PATH = "data/favorites.csv"
import os
os.makedirs("data", exist_ok=True)
ensure_csv(HIST_PATH, ["timestamp", "input", "lang", "pun"])
ensure_csv(FAV_PATH, ["timestamp", "input", "lang", "pun"])

with st.sidebar:
    st.header("設定")
    lang = st.radio("言語", ["日本語", "English"], index=0)
    n = st.slider("ダジャレ数", 3, 10, 5)
    st.markdown("---")
    uploaded = st.file_uploader("バッチ用の単語リスト（.txt）", type=["txt"])
    st.caption("1行1単語。英語は韻、和文はテンプレ系。")

tab1, tab2, tab3 = st.tabs(["生成", "履歴", "お気に入り"])

with tab1:
    word = st.text_input("単語を入力（例：カレー / pizza）", value="カレー")
    if st.button("生成！", type="primary"):
        hint = "ja" if lang == "日本語" else "en"
        result = make_puns(word.strip(), lang_hint=hint, n=n)
        st.subheader("結果")
        if result.get("summary"):
            with st.expander("Wikipediaの要約（キー不要API）"):
                st.write(result["summary"])

        for i, p in enumerate(result["puns"], 1):
            st.markdown(f"**{i}. {p}**")
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"履歴に保存 {i}", key=f"save_hist_{i}"):
                    append_csv(HIST_PATH, [datetime.datetime.utcnow().isoformat(), word, hint, p])
                    st.success("履歴に保存しました。")
            with col2:
                if st.button(f"★ お気に入り {i}", key=f"fav_{i}"):
                    append_csv(FAV_PATH, [datetime.datetime.utcnow().isoformat(), word, hint, p])
                    st.success("お気に入りに追加しました。")

    if uploaded is not None:
        st.subheader("バッチ生成結果")
        content = uploaded.read().decode("utf-8", errors="ignore")
        lines = [x.strip() for x in content.splitlines() if x.strip()]
        for w in lines[:50]:  # safety cap
            res = make_puns(w, lang_hint=("ja" if lang=="日本語" else "en"), n=3)
            st.markdown(f"### {w}")
            for p in res["puns"]:
                st.write("・", p)
                append_csv(HIST_PATH, [datetime.datetime.utcnow().isoformat(), w, ("ja" if lang=="日本語" else "en"), p])

with tab2:
    st.subheader("履歴")
    rows = read_csv(HIST_PATH)
    if len(rows) <= 1:
        st.info("まだ履歴がありません。")
    else:
        # skip header
        for r in rows[1:][-200:]:
            st.write(f"- [{r[0]}] `{r[1]}` ({r[2]}): {r[3]}")

with tab3:
    st.subheader("お気に入り")
    rows = read_csv(FAV_PATH)
    if len(rows) <= 1:
        st.info("お気に入りは空です。")
    else:
        for r in rows[1:]:
            st.write(f"★ [{r[0]}] `{r[1]}` ({r[2]}): {r[3]}")
        # Export favorites
        export = st.button("お気に入りをCSVダウンロード")
        if export:
            buf = io.StringIO()
            writer = csv.writer(buf)
            for rr in rows:
                writer.writerow(rr)
            st.download_button("Download favorites.csv", data=buf.getvalue(), file_name="favorites.csv", mime="text/csv")
