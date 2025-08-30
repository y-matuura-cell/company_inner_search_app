import sys
print("=== main.py 1行目到達 ===")
sys.stderr.write('=== STDERR main.py 1行目到達 ===\n')
"""
このファイルは、Webアプリのメイン処理が記述されたファイルです。
"""
print("main.py start")

############################################################
# 1. ライブラリの読み込み
############################################################
from dotenv import load_dotenv
import logging
import streamlit as st
import utils
from initialize import initialize
import components as cn
import constants as ct

st.set_page_config(page_title=ct.APP_NAME)
logger = logging.getLogger(ct.LOGGER_NAME)

print("main.py: initialize()直前")
initialize()
print("main.py: initialize()直後")

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

    # チャット入力欄と送信ボタン
    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_input("質問を入力してください", key="user_input")
        submitted = st.form_submit_button("送信")

    if submitted and user_input:
        # ユーザーの入力を会話ログに追加
        st.session_state.messages.append({"role": "user", "content": user_input})
        try:
            # AI応答生成
            with st.spinner("AIが回答中..."):
                ai_response = utils.get_llm_response(user_input)
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
        except Exception as e:
            import traceback
            logger.error(f"{ct.AI_ERROR_MESSAGE}\n{e}")
            st.error(utils.build_error_message(ct.AI_ERROR_MESSAGE), icon=ct.ERROR_ICON)
            st.error(str(e))
            print(f"AI ERROR: {str(e)}")
            print(traceback.format_exc())
