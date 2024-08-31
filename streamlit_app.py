import os

import streamlit as st
import google.generativeai as genai
import google.ai.generativelanguage as glm

# ================================================================================
# Google Gemini 1.5 Flashを利用するための設定
# ================================================================================
# # APIキーの設定
# genai.configure(api_key=os.getenv("GoogleAPIKEY"))

# ================================================================================
# ページ設定
# https://docs.streamlit.io/develop/api-reference/configuration/st.set_page_config
# ================================================================================
# ページ設定
st.set_page_config(page_title="Gemini Chatbot", page_icon=":whale:", layout="centered",initial_sidebar_state="auto",menu_items=None)

# ================================================================================
# Body
# ================================================================================
# サイドバーにGeminiのAPIキーの入力欄を設ける
with st.sidebar:
    gemini_api_key = st.text_input("Gemini API Key", key="chatbot_api_key", type="password")
    "[Get an Gemini API key](https://aistudio.google.com/app/apikey)"
 
st.title("Gemini Chatbot!")
st.caption("サイドバーにAPIキーを入れてから、下の入力欄にテキストを入力して使ってください。")
 
# セッションにチャット履歴がなければ初期化
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
 
# チャット履歴を表示
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
     
# ユーザーの入力が送信された際に実行される処理
if prompt := st.chat_input("ここにメッセージを入力してください。"):
 
    # APIキーのチェック
    if not gemini_api_key:
        # APIキーがない場合はエラー
        st.info("Please add your [Gemini API key](https://aistudio.google.com/app/apikey) to continue.")
        st.stop()
 
    # モデルのセットアップ
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
 
    # ユーザの入力をチャット履歴に追加し画面表示
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # これまでの会話履歴を取得
    messages = []
    for message in st.session_state.chat_history:
        messages.append(
            {
                "role": message["role"] if message["role"] == "user" else "model",
                'parts': message["content"]
            }
        )
 
    # Geminiへ問い合わせを行う
    response = model.generate_content(messages)
 
    # Geminiの返答をチャット履歴に追加し画面表示
    st.session_state.chat_history.append({"role": "assistant", "content": response.text})
    st.chat_message("assistant").write(response.text)