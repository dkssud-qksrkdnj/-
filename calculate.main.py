import streamlit as st
import math

st.set_page_config(page_title="공학 계산기", page_icon="🧮")

st.title("🧮 계산기 웹앱")

operation = st.selectbox(
    "연산을 선택하세요",
    (
        "사칙연산",
        "모듈러 연산",
        "지수 연산",
        "로그 연산"
    )
)

# -----------------------------
# 사칙연산
# -----------------------------
if operation == "사칙연산":

    num1 = st.number_input("첫 번째 숫자", value=0.0)
    num2 = st.number_input("두 번째 숫자", value=0.0)

    operator = st.selectbox(
        "연산자 선택",
        ("+", "-", "×", "÷")
    )

    if st.button("계산하기"):

        if operator == "+":
            result = num1 + num2

        elif operator == "-":
            result = num1 - num2

        elif operator == "×":
            result = num1 * num2

        elif operator == "÷":
            if num2 == 0:
                st.error("0으로 나눌 수 없습니다.")
            else:
                result = num1 / num2

        if operator != "÷" or num2 != 0:
            st.success(f"결과: {result}")

# -----------------------------
# 모듈러 연산
# -----------------------------
elif operation == "모듈러 연산":

    num1 = st.number_input("숫자", value=0, step=1)
    num2 = st.number_input("나눌 값", value=1, step=1)

    if st.button("계산하기"):

        if num2 == 0:
            st.error("0으로 나눌 수 없습니다.")
        else:
            result = num1 % num2
            st.success(f"나머지: {result}")

# -----------------------------
# 지수 연산
# -----------------------------
elif operation == "지수 연산":

    base = st.number_input("밑", value=2.0)
    exponent = st.number_input("지수", value=2.0)

    if st.button("계산하기"):
        result = base ** exponent
        st.success(f"결과: {result}")

# -----------------------------
# 로그 연산
# -----------------------------
elif operation == "로그 연산":

    number = st.number_input("진수", value=10.0, min_value=0.000001)
    base = st.number_input("밑", value=10.0, min_value=0.000001)

    if st.button("계산하기"):

        if number <= 0 or base <= 0 or base == 1:
            st.error("올바른 로그 값을 입력하세요.")
        else:
            result = math.log(number, base)
            st.success(f"결과: {result}")
