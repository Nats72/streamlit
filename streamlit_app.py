import streamlit as st

# タイトル生成
st.title("Geminiでチャットボット作ってみた")

# セッションにチャット履歴がなければ初期化
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
 
# チャット履歴を表示
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
 
# チャットボットの返答を作成
def generate_response(user_input):
    if "こんにちは" in user_input:
        return "こんにちは！今日はどうされましたか？"
    elif "ありがとう" in user_input:
        return "どういたしまして！お役に立てて嬉しいです。"
    elif "さようなら" in user_input:
        return "さようなら！またお話ししましょう。"
    else:
        return f"ご質問ありがとうございます。『{user_input}』についてはお答えできませんが、他にお困りのことはありますか？"
 
# ユーザーの入力が送信された際に実行される処理
if prompt := st.chat_input("何かお困りですか？"):
 
    # ユーザの入力を表示
    with st.chat_message("user"):
        st.markdown(prompt)
    # ユーザの入力をチャット履歴に追加
    st.session_state.chat_history.append({"role": "user", "content": prompt})
 
    # チャットボットの返答を表示
    response = generate_response(prompt)
    with st.chat_message("assistant"):
        st.markdown(response)
    # チャットボットの返答をチャット履歴に追加
    st.session_state.chat_history.append({"role": "assistant", "content": response})

# input_num = st.number_input('Input a number', value=0)

# result = input_num ** 2

# st.write('Result: ', result)