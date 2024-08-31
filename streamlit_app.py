import os

import streamlit as st
import google.generativeai as genai
import google.ai.generativelanguage as glm

def main():
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
    st.set_page_config(
        page_title="Gemini Chatbot",
        page_icon=":whale:",
        layout="centered",
        initial_sidebar_state="auto",
        menu_items=None
        )

    # ================================================================================
    # Body
    # ================================================================================
    # サイドバーにGeminiのAPIキーの入力欄を設ける
    with st.sidebar:
        gemini_api_key = st.text_input("Gemini API Key", key="chatbot_api_key", type="password")
        "[Get an Gemini API key](https://aistudio.google.com/app/apikey)"
    
    st.title("Gemini Chatbot!")
    st.caption("サイドバーにAPIキーを入れてから、下の入力欄にテキストを入力して使ってください。")
    
    # セッションにチャット履歴がなければ初期化（message_historyを作成）
    if "message_history" not in st.session_state:
        st.session_state.message_history = [
            # system promptを設定
            ("system","日本語で回答してください。")
            ]
    
    # チャット履歴を表示
    for message in st.session_state.message_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
        
    # ユーザーの入力が送信された際に実行される処理
    # chat_input()は、チャットUIでユーザの入力を待ち受けする
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
        st.session_state.message_history.append({"role": "user", "content": user_input})
        st.chat_message("user").write(user_input)

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
        with st.spinner("Gemini is typing..."):
            response = model.generate_content(messages)
    
        # Geminiの返答をチャット履歴に追加し画面表示
        st.session_state.message_history.append({"role": "assistant", "content": response.text})
        st.chat_message("assistant").write(response.text)

if __name__ == '__main__':
    main()