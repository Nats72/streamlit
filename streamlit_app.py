import os

import streamlit as st
import google.generativeai as genai
import google.ai.generativelanguage as glm


# ================================================================================
# Google Gemini 1.5 Flashを利用するための設定
# ================================================================================
# APIキーの設定
genai.configure(api_key=os.getenv("GoogleAPIKEY"))

# Geminiモデルの設定
model = genai.GenerativeModel('gemini-1.5-flash')

# ================================================================================
# ページ設定
# https://docs.streamlit.io/develop/api-reference/configuration/st.set_page_config
# ================================================================================
# ページ設定
st.set_page_config(page_title="Gemini Chatbot", page_icon=":whale:", layout="centered",initial_sidebar_state="auto",menu_items="None")

# タイトル生成
st.title("Geminiでチャットボット作ってみた")

# ヘッダー&サブヘッダー
st.header('へっだー')
st.subheader('This is a subheader')


# ================================================================================
# chat
# ================================================================================
# 定数定義
USER_NAME = "user"
ASSISTANT_NAME = "assistant"
MODEL_NAME = "model"

# セッションにチャット履歴がなければ初期化
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []

if "chat_log" not in st.session_state:
    st.session_state.chat_log = model.start_chat(history=[
        glm.Content(role=USER_NAME, parts=[glm.Part(text="あなたは優秀なAIアシスタントです。できるだけ簡潔に回答してください。")]),
        glm.Content(role=MODEL_NAME, parts=[glm.Part(text="わかりました。")])
    ])
    st.session_state.chat_log = []

user_msg = st.chat_input("ここにメッセージを入力")

if user_msg:
    # 以前のチャットログを表示
    for chat in st.session_state.chat_log:
        with st.chat_message(chat["name"]):
            st.write(chat["msg"])

    # 最新のメッセージを表示
    with st.chat_message(USER_NAME):
        st.write(user_msg)

    # アシスタントのメッセージを表示
    response = model.generate_content(user_msg)
    with st.chat_message(ASSISTANT_NAME):
        assistant_msg = response.text
        st.write(assistant_msg)

    # セッションにチャットログを追加
    st.session_state.chat_log.append({"name": USER_NAME, "msg": user_msg})
    st.session_state.chat_log.append({"name": ASSISTANT_NAME, "msg": assistant_msg})

# チャット履歴を表示
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
 
# # チャットボットの返答を作成
# def generate_response(user_input):
#     if "こんにちは" in user_input:
#         return "こんにちは！今日はどうされましたか？"
#     elif "ありがとう" in user_input:
#         return "どういたしまして！お役に立てて嬉しいです。"
#     elif "さようなら" in user_input:
#         return "さようなら！またお話ししましょう。"
#     else:
#         return f"ご質問ありがとうございます。『{user_input}』についてはお答えできませんが、他にお困りのことはありますか？"
 
# # ユーザーの入力が送信された際に実行される処理
# if prompt := st.chat_input("何かお困りですか？"):
 
#     # ユーザの入力を表示
#     with st.chat_message("user"):
#         st.markdown(prompt)
#     # ユーザの入力をチャット履歴に追加
#     st.session_state.chat_history.append({"role": "user", "content": prompt})
 
#     # チャットボットの返答を表示
#     response = generate_response(prompt)
#     with st.chat_message("assistant"):
#         st.markdown(response)
#     # チャットボットの返答をチャット履歴に追加
#     st.session_state.chat_history.append({"role": "assistant", "content": response})

# input_num = st.number_input('Input a number', value=0)

# result = input_num ** 2

# st.write('Result: ', result)