

import streamlit as st
import os
from dotenv import load_dotenv
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# .envからAPIキーを取得
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
llm = OpenAI(temperature=0.7, openai_api_key=OPENAI_API_KEY)

def get_expert_system_message(expert_type):
    if expert_type == "医療":
        return "あなたは優秀な医師です。医学的な知識に基づいて、分かりやすく丁寧に回答してください。"
    elif expert_type == "IT":
        return "あなたはIT分野の専門家です。技術的な内容を分かりやすく説明してください。"
    else:
        return "あなたは優秀な専門家です。分かりやすく丁寧に回答してください。"

def get_llm_response(input_text, expert_type):
    system_message = get_expert_system_message(expert_type)
    prompt = PromptTemplate(
        input_variables=["user_input"],
        template=f"{system_message}\nユーザーからの質問: {{user_input}}"
    )
    chain = LLMChain(llm=llm, prompt=prompt)
    response = chain.run(user_input=input_text)
    return response

st.title("専門家LLM相談アプリ")
st.markdown("""
このアプリは、医療・ITの専門家に相談するように、AI（LLM）から回答を得ることができます。\
以下の手順でご利用ください：
1. 相談したい専門家の種類を選択してください。
2. 質問内容を入力し、「送信」ボタンを押してください。
3. AIによる専門的な回答が画面に表示されます。
""")

expert_type = st.radio("相談したい専門家の種類を選択してください：", ("医療", "IT"))
input_text = st.text_area("質問内容を入力してください：", height=100)

if st.button("送信"):
    if input_text.strip():
        with st.spinner("AIが回答中です..."):
            answer = get_llm_response(input_text, expert_type)
        st.markdown("#### 回答")
        st.write(answer)
    else:
        st.warning("質問内容を入力してください。")