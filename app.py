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
    st.session_state.current_index = None
if "show_answer" not in st.session_state:
    st.session_state.show_answer = False
if "next_clicked" not in st.session_state:
    st.session_state.next_clicked = True  # 一開始就可以出題

# 換下一題（不會用 rerun）
if st.session_state.next_clicked:
    remaining = list(set(range(len(df))) - set(st.session_state.used_indices))
    if not remaining:
        st.success("恭喜你完成所有單字的一輪測驗～分數會保留，進入下一輪 🥳")
        st.session_state.used_indices = []
        remaining = list(range(len(df)))
    st.session_state.current_index = random.choice(remaining)
    st.session_state.used_indices.append(st.session_state.current_index)
    st.session_state.show_answer = False
    st.session_state.next_clicked = False

# 題目內容
word = df.iloc[st.session_state.current_index]
english_word = word['English']
chinese_word = word['Chinese']
hint = f"{english_word[0]}___{english_word[-1]}"

st.title("英文單字練習網站（看中文猜英文 + 計分）")
st.markdown(f"**目前分數：{st.session_state.score} / {st.session_state.total}**")
st.subheader(f"中文：**{chinese_word}**（提示：{hint}）")

answer = st.text_input("請輸入英文單字：")

if st.button("提交答案") and not st.session_state.show_answer:
    st.session_state.total += 1
    st.session_state.show_answer = True
    if answer.strip().lower() == english_word.strip().lower():
        st.session_state.score += 1
        st.success("答對ㄌ！")
    else:
        st.error(f"答錯ㄌ，正確答案是：{english_word}")

if st.session_state.show_answer:
    if st.button("下一題"):
        st.session_state.next_clicked = True
