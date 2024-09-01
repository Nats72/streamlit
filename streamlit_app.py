import streamlit as st

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

import google.generativeai as genai


def init_page():

    # Page Settings
    st.set_page_config(
        page_title="Gemini Chatbot",
        page_icon=":whale:",
        layout="centered",
        initial_sidebar_state="auto",
        menu_items=None
        )

def init_messages():
    # Sidebar Settings
    st.sidebar.title("Options")
    # サイドバーにGeminiのAPIキーの入力欄を設ける
    gemini_api_key = st.sidebar.text_input("Gemini API Key", key="chatbot_api_key", type="password")

    # メッセージ履歴を消すボタンを設置
    clear_button = st.sidebar.button("Start/Reset",key="clear")
    
    # 初期状態の表示をする
    if "message_history" not in st.session_state:
        st.session_state.message_history = [
            {"role": "assistant", "content": "サイドバーにAPIキーを入れてから、Start/Resetボタンで開始します。"}
            ]
        
    # クリアボタンを押すと初期化
    if clear_button and gemini_api_key:
        # GEMINIのAPIキーを登録
        genai.configure(api_key=gemini_api_key)

        # システムプロンプト（初期プロンプト）を定義
        system_prompt = (
            "日本語で回答してください。"
            "質問の答えが分からない場合は、分からない旨を回答してください。"
        )
        # プロンプトを設定
        st.session_state.message_history = [
            {"role": "system", "content": system_prompt},
            {"role": "assistant", "content": "上記プロンプトを設定しました。気軽に質問してください。"}
            ]

def select_model():
    # tempratureを変更できるスライダーを設置
    temperature = st.sidebar.slider(
        "Temperature:", min_value=0.0, max_value=2.0, value=1.0, step=0.1
    )

    # モデル選択できるラジオボタンを設置
    models = ("Gemini")
    model = st.sidebar.radio("Choose a model:", models)

    # モデル生成
    if model == "Gemini":
        st.session_state.model_name = "gemini-1.5-flash"
        configurable_model = ChatGoogleGenerativeAI(
            temperature=temperature,
            model=st.session_state.model_name
        )
        return configurable_model
    
def init_chain():
    st.session_state.llm = select_model()
    # ユーザーの入力をモデルに渡すためのテンプレートを定義
    prompt = ChatPromptTemplate.from_messages([
        ("user", "{user_input}")
    ])
    # モデルからの返答から必要な情報を抽出
    output_parser = StrOutputParser()
    # LCELの書き方でプロンプトとモデル(llm)とoutput_parserを繋ぐ
    init_chain = prompt | st.session_state.llm | output_parser
    return init_chain

def main():
    init_page()
    init_messages()
    chain = init_chain()

    # タイトルとキャプション
    st.title("Gemini Chatbot!")
    st.caption("サイドバーにAPIキーを入れてから、Start/Resetボタンで開始します。")
    
    # チャット履歴を表示
    for message in st.session_state.message_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
    # ユーザーの入力が送信された際に実行される処理
    # chat_input()で、チャットUIでユーザの入力を待ち受けする
    if user_input := st.chat_input("ここにメッセージを入力してください。"):
    
        # ユーザの入力をチャット履歴に追加し画面表示
        st.chat_message("user").markdown(user_input)

        # LLMの返答をStream表示させる
        with st.chat_message('ai'):
            # LCELのstreaming関数(chain.stream)をstreamlitのst.write_streamで表示させている
            response = st.write_stream(chain.stream({"user_input":user_input}))
    
        # チャット履歴に追加する
        st.session_state.message_history.append({"role": "user", "content": user_input})
        st.session_state.message_history.append({"role": "ai", "content": response})

if __name__ == '__main__':
    main()