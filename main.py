"""
このファイルは、Webアプリのメイン処理が記述されたファイルです。
"""
print("main.py start")

############################################################
# 1. ライブラリの読み込み
############################################################
# 「.env」ファイルから環境変数を読み込むための関数
from dotenv import load_dotenv
# ログ出力を行うためのモジュール
import logging
# streamlitアプリの表示を担当するモジュール
import streamlit as st
# （自作）画面表示以外の様々な関数が定義されているモジュール
import utils
# （自作）アプリ起動時に実行される初期化処理が記述された関数
from initialize import initialize
# （自作）画面表示系の関数が定義されているモジュール
import components as cn
# （自作）変数（定数）がまとめて定義・管理されているモジュール
import streamlit as st
import logging
import utils
from initialize import initialize
import components as cn
import constants as ct

st.set_page_config(page_title=ct.APP_NAME)
logger = logging.getLogger(ct.LOGGER_NAME)

try:
    initialize()
except Exception as e:
    logger.error(f"{ct.INITIALIZE_ERROR_MESSAGE}\n{e}")
    st.error(utils.build_error_message(ct.INITIALIZE_ERROR_MESSAGE), icon=ct.ERROR_ICON)
    st.error(str(e))
    print(f"INITIALIZE ERROR: {str(e)}")
    st.stop()

if "initialized" not in st.session_state:
    st.session_state.initialized = True
    logger.info(ct.APP_BOOT_MESSAGE)

# サイドバー（利用目的・説明）
cn.display_sidebar()

# メインエリア（containerで明示的に分割）
main_area = st.container()
with main_area:
    cn.display_app_title()
    cn.display_initial_ai_message()

    # 会話ログの表示（st.markdownで自作表示）
    if "messages" not in st.session_state:
        st.session_state.messages = []
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(
                f"<div style='text-align:right; background:#e3f2fd; border-radius:8px; padding:0.5em 1em; margin-bottom:0.3em; color:#222;'><b>あなた：</b> {message['content']}</div>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"<div style='text-align:left; background:#f0f4fa; border-radius:8px; padding:0.5em 1em; margin-bottom:0.3em; color:#222;'><b>AI：</b> {message['content']}</div>",
                unsafe_allow_html=True,
            )

    # チャット入力の受け付け（text_input＋buttonで自作）
    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_input(ct.CHAT_INPUT_HELPER_TEXT, key="chat_input")
        submitted = st.form_submit_button("送信")

    if submitted and user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        logger.info({"message": user_input, "application_mode": st.session_state.mode})
        with st.spinner(ct.SPINNER_TEXT):
            pass
