import os
import streamlit as st
import json
from datetime import datetime
from openai import OpenAI
def session_load():
    session_list=[]
    if os.path.exists("./sessions"):
        for file in os.listdir("./sessions"):
            session_list.append(file[:-5])
    return session_list
def data_load(session_name):
    if os.path.exists(f"./sessions/{session_name}.json"):
        with open(f"./sessions/{session_name}.json","r",encoding="utf-8") as f:
            session_data=json.load(f)
            st.session_state.messages=session_data["messages"]
            st.session_state.nick_name=session_data["nick_name"]
            st.session_state.nature=session_data["nature"]
            st.session_state.current_name=session_data["name"]
def delete_conversation(session_name):
    if os.path.exists(f"./sessions/{session_name}.json"):
        os.remove(f"./sessions/{session_name}.json")
def generate_name():
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
def save_conversation():
    conversation_data = {
        "messages": st.session_state.messages,
        "nick_name": st.session_state.nick_name,
        "nature": st.session_state.nature,
        "name": st.session_state.current_time
    }
    if not os.path.exists("sessions"):
        os.makedirs("sessions")
    with open(f"sessions/{st.session_state.current_time}.json", "w", encoding="utf-8") as f:
        json.dump(conversation_data, f, ensure_ascii=False, indent=2)


st.set_page_config(page_title="智能伴侣",page_icon="😶‍🌫️",layout="wide",initial_sidebar_state="expanded")
st.title("AI智能伴侣")
st.logo("😶‍🌫️")
system_prompt="""你叫%s，现在是用户的真实伴侣，请完全代入伴侣角色
规则:
    1.每次只回1条消息
    3.匹配用户的语言
    2.禁止任何场景或状态描述性文字
    4.回复简短，像微信聊天一样
    5.有需要的话可以用等emoji表情
    伴侣性格:
    6.用符合伴侣性格的方式对话
    7.回复的内容，要充分体现伴侣的性格特征- %s你必须严格遵守上述规则来回复用户"""
if "messages" not in st.session_state:
    st.session_state.messages = []
if "nick_name" not in st.session_state:
    st.session_state.nick_name = "小甜甜"
if "nature" not in st.session_state:
    st.session_state.nature = "温柔体贴的东北姑娘"
if "current_time" not in st.session_state:
    st.session_state.current_time = generate_name()
for message in st.session_state.messages:
    st.chat_message(message["role"]).write(message["content"])
client = OpenAI(api_key=os.environ.get('DEEPSEEK_API_KEY'), base_url="https://api.deepseek.com")
with st.sidebar:
    st.subheader("伴侣设置")
    if st.button("新建会话",width="stretch"):
        if st.session_state.messages:
            save_conversation()
            st.session_state.current_time = generate_name()
            st.session_state.messages = []
            save_conversation()
            st.rerun()
    coin1,coin2=st.columns([4,1])
    session_list=session_load()
    for session in session_list:
        with coin1:
            if st.button(session,width="stretch",key=f"load_{session}",type="primary" if st.session_state.current_time==session else "secondary"):
                data_load(session)
                st.rerun()
        with coin2:
            if st.button("",icon="❌",width="stretch",key=f"delete_{session}"):
                delete_conversation(session)
                st.rerun()


    st.subheader("伴侣昵称")
    nick_name=st.text_input("请输入伴侣昵称",placeholder="输入不能为空!",value=st.session_state.nick_name)
    if nick_name:
        st.session_state.nick_name = nick_name
    st.subheader("伴侣性格")
    nature=st.text_input("请输入伴侣性格",placeholder="输入不能为空!",value=st.session_state.nature)
    if nature:
        st.session_state.nature = nature
prompt=st.chat_input("请输入你要询问的问题")
if prompt:
    st.session_state.messages.append({"role":"user","content":prompt})
    st.chat_message("user").write(prompt)
    response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": system_prompt%(st.session_state.nick_name, st.session_state.nature)},
        *st.session_state.messages
    ],
    stream=True,
    )
    response_message=st.empty()
    full_message=""
    for chunk in response:
        if chunk.choices and chunk.choices[0].delta.content:
            full_message+=chunk.choices[0].delta.content
            response_message.chat_message("assistant").write(full_message)
    st.session_state.messages.append({"role":"assistant","content":full_message})
