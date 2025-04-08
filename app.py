import streamlit as st
import pandas as pd
import random

# 讀取 Excel
df = pd.read_excel("vocab.xlsx")

# 初始化 session_state
if "used_indices" not in st.session_state:
    st.session_state.used_indices = []
if "score" not in st.session_state:
    st.session_state.score = 0
if "total" not in st.session_state:
    st.session_state.total = 0
if "current_index" not in st.session_state:
    remaining_indices = list(set(range(len(df))) - set(st.session_state.used_indices))
    st.session_state.current_index = random.choice(remaining_indices)
    st.session_state.used_indices.append(st.session_state.current_index)

st.title("英文單字練習網站（看中文猜英文 + 計分）")
st.markdown(f"**目前分數：{st.session_state.score} / {st.session_state.total}**")

word = df.iloc[st.session_state.current_index]
english_word = word['English']
chinese_word = word['Chinese']
hint = f"{english_word[0]}___{english_word[-1]}"

st.subheader(f"中文：**{chinese_word}**（提示：{hint}）")
answer = st.text_input("請輸入英文單字：")
answered = False

if answer:
    st.session_state.total += 1
    answered = True
    if answer.strip().lower() == english_word.strip().lower():
        st.session_state.score += 1
        st.success("答對ㄌ！")
    else:
        st.error(f"答錯ㄌ，正確答案是：{english_word}")

if answered:
    if st.button("下一題"):
        if len(st.session_state.used_indices) == len(df):
            st.success("你已經練完所有單字一輪囉！分數會保留，準備下一輪～")
            st.session_state.used_indices = []
        remaining_indices = list(set(range(len(df))) - set(st.session_state.used_indices))
        st.session_state.current_index = random.choice(remaining_indices)
        st.session_state.used_indices.append(st.session_state.current_index)
        st.experimental_rerun()