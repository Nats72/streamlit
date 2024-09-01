# import os

import streamlit as st

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import ConfigurableField

import google.generativeai as genai


def init_page():
    # # APIキーの設定
    # genai.configure(api_key=os.getenv("GoogleAPIKEY"))

    # Page Settings
    st.set_page_config(
        page_title="Gemini Chatbot",
        page_icon=":whale:",
        layout="centered",
        initial_sidebar_state="auto",
        menu_items=None
        )
    
    # Sidebar Settings
    st.sidebar.title("Options")
    # サイドバーにGeminiのAPIキーの入力欄を設ける
    with st.sidebar:
        gemini_api_key = st.text_input("Gemini API Key", key="chatbot_api_key", type="password")
        "[Get an Gemini API key](https://aistudio.google.com/app/apikey)"
    
def init_messages():
    # メッセージ履歴を消すボタンを設置
    clear_button = st.sidebar.button("Clear Conversaton",key="clear")
    # クリアボタンを押すか、メッセージが存在しない場合に初期化する処理
    if clear_button or "message_history" not in st.session_state:
        system_prompt = (
            "Your purpose is to answer questions about specific documents only. "
            "Please answer the user's questions based on what you know about the document. "
            "If the question is outside scope of the document, please politely decline. "
            "If you don't know the answer, say `I don't know`. "
        )
        st.session_state.message_history = [
            # system promptを設定
            {"role": "system", "content": system_prompt},
            {"role": "assistant", "content": "何か気になることはありますか？"}
            ]

def select_model():
    # tempratureを変更できるスライダーを設置
    temperature = st.sidebar.slider(
        "Temperature:", min_value=0.0, max_value=2.0, value=1.0, step=0.1
    )

    # モデル選択できるラジオボタンを設置
    models = ("Gemini")
    model = st.sidebar.radio("Choose a model:", models)
    if model == "Gemini":
        st.session_state.model_name = "gemini-1.5-flash"
        # モデル生成
        configurable_model = ChatGoogleGenerativeAI(
            temperature=temperature,
            model=st.session_state.model_name
        )
        configurable_model.configurable_fields(
            model_name=ConfigurableField(id="model"),
            default_key="gemini-1.5-flash"
        )
        return configurable_model
    
def init_chain():
    llm = select_model()
    # ユーザーの入力をモデルに渡すためのテンプレートを定義
    prompt = ChatPromptTemplate.from_messages([
        *st.session_state.message_history,
        ("user", "{user_input}"),
    ])
    # モデルからの返答から必要な情報を抽出
    output_parser = StrOutputParser()
    return prompt | llm | output_parser

def main():
    init_page()
    init_messages()
    chain = init_chain()

    st.title("Gemini Chatbot!")
    st.caption("サイドバーにAPIキーを入れてから、下の入力欄にテキストを入力して使ってください。")
    
    # # セッションにチャット履歴がなければ初期化（message_historyを作成）
    # if "message_history" not in st.session_state:
    #     system_prompt = (
    #         "Your purpose is to answer questions about specific documents only. "
    #         "Please answer the user's questions based on what you know about the document. "
    #         "If the question is outside scope of the document, please politely decline. "
    #         "If you don't know the answer, say `I don't know`. "
    #     )
    #     st.session_state.message_history = [
    #         # system promptを設定
    #         {"role": "system", "content": system_prompt},
    #         {"role": "assistant", "content": "何か気になることはありますか？"}
    #         ]
    
    # チャット履歴を表示
    for message in st.session_state.message_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
        
    # ユーザーの入力が送信された際に実行される処理
    # chat_input()で、チャットUIでユーザの入力を待ち受けする
    if user_input := st.chat_input("ここにメッセージを入力してください。"):
    
        # APIキーのチェック
        if not gemini_api_key:
            # APIキーがない場合はエラー
            st.info("Please add your [Gemini API key](https://aistudio.google.com/app/apikey) to continue.")
            st.stop()
    
        # モデルの設定
        generation_config = {
            "temperature": 0.9,  # 生成するテキストのランダム性を制御
            "top_p": 1,          # 生成に使用するトークンの累積確率を制御
            "top_k": 1,          # 生成に使用するトップkトークンを制御
            "max_output_tokens": 2048,  # 最大出力トークン数を指定
        }
        # セーフティ設定
        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",  # ハラスメントに関する内容を制御
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"     # 中程度以上のハラスメントをブロック
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",  # ヘイトスピーチに関する内容を制御
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"      # 中程度以上のヘイトスピーチをブロック
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",  # 性的に露骨な内容を制御
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"            # 中程度以上の性的内容をブロック
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",  # 危険な内容を制御
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"            # 中程度以上の危険な内容をブロック
            }
        ]
        # モデルの初期化
        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            generation_config=generation_config,
            safety_settings=safety_settings
            )
    
        # ユーザの入力をチャット履歴に追加し画面表示
        # st.session_state.message_history.append({"role": "user", "content": user_input})
        # st.chat_message("user").write(user_input)

        # これまでの会話履歴を取得
        messages = []
        for message in st.session_state.message_history:
            messages.append(
                {
                    "role": message["role"] if message["role"] == "user" else "model",
                    'parts': message["content"]
                }
            )
    
        # Geminiへ問い合わせを行う
        # with st.spinner("Gemini is typing..."):
        #     response = model.generate_content(messages)
        
        # LLMの返答をStream表示させる
        with st.chat_message('ai'):
            # LCELのstreaming関数(chain.stream)をstreamlitのst.write_streamで表示させている
            response = st.write_stream(chain.stream({"user_input":user_input}))
    
        # チャット履歴に追加する
        st.session_state.message_history.append({"role": "user", "content": user_input})
        st.session_state.message_history.append({"role": "ai", "content": response})

        # Geminiの返答をチャット履歴に追加し画面表示
        # st.session_state.message_history.append({"role": "assistant", "content": response.text})
        # st.chat_message("assistant").write(response.text)

if __name__ == '__main__':
    main()