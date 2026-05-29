import streamlit as st
import math
import random
import plotly.graph_objects as go
from collections import Counter

st.set_page_config(page_title="웹앱", page_icon="🧮", layout="wide")

# 사이드바에서 앱 선택
app_choice = st.sidebar.radio(
    "🔧 앱 선택",
    ["🧮 계산기", "🎲 확률 시뮬레이터"]
)

# ===============================================
# 계산기 앱
# ===============================================
if app_choice == "🧮 계산기":
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
    
    # 사칙연산
    if operation == "사칙연산":
        num1 = st.number_input(
            "첫 번째 숫자",
            value=0.0,
        )
        
        num2 = st.number_input(
            "두 번째 숫자",
            value=0.0,
        )
        
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
    
    # 모듈러 연산
    elif operation == "모듈러 연산":
        num1 = st.number_input(
            "숫자",
            value=0,
            step=1,
        )
        
        num2 = st.number_input(
            "나눌 값",
            value=1,
            step=1,
        )
        
        if st.button("계산하기"):
            if num2 == 0:
                st.error("0으로 나눌 수 없습니다.")
            else:
                result = num1 % num2
                st.success(f"나머지: {result}")
    
    # 지수 연산
    elif operation == "지수 연산":
        base = st.number_input(
            "밑",
            value=2.0,
        )
        
        exponent = st.number_input(
            "지수",
            value=2.0,
        )
        
        if st.button("계산하기"):
            result = base ** exponent
            st.success(f"결과: {result}")
    
    # 로그 연산
    elif operation == "로그 연산":
        number = st.number_input(
            "진수",
            value=10.0,
            min_value=0.000001,
        )
        
        base = st.number_input(
            "밑",
            value=10.0,
            min_value=0.000001,
        )
        
        if st.button("계산하기"):
            if number <= 0 or base <= 0 or base == 1:
                st.error("올바른 로그 값을 입력하세요.")
            else:
                result = math.log(number, base)
                st.success(f"결과: {result}")

# ===============================================
# 확률 시뮬레이터 앱
# ===============================================
elif app_choice == "🎲 확률 시뮬레이터":
    st.title("🎲 확률 시뮬레이터")
    
    col1, col2 = st.columns(2)
    
    with col1:
        simulation_type = st.selectbox(
            "시뮬레이션 종류 선택",
            ["주사위", "동전"]
        )
    
    with col2:
        trials = st.number_input(
            "시행 횟수",
            value=1000,
            min_value=1,
            step=100,
        )
    
    if st.button("시뮬레이션 실행", key="simulate"):
        # 주사위 시뮬레이션
        if simulation_type == "주사위":
            results = [random.randint(1, 6) for _ in range(trials)]
            result_counts = Counter(results)
            
            faces = sorted(result_counts.keys())
            counts = [result_counts[face] for face in faces]
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=[f"{i}" for i in faces],
                y=counts,
                marker_color='rgba(100, 150, 200, 0.7)',
                text=counts,
                textposition='auto',
                name='횟수'
            ))
            
            fig.update_layout(
                title=f"주사위 {trials}회 시뮬레이션 결과",
                xaxis_title="주사위 눈",
                yaxis_title="나온 횟수",
                height=500,
                showlegend=False,
                hovermode='x unified'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # 통계 정보
            st.subheader("📊 통계")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("총 시행 횟수", trials)
            with col2:
                st.metric("평균값", f"{sum(results) / len(results):.2f}")
            with col3:
                st.metric("기댓값 (이론값)", "3.5")
            
            # 상세 결과
            st.subheader("📋 상세 결과")
            detail_data = {
                "주사위 눈": [f"{i}" for i in faces],
                "나온 횟수": counts,
                "확률 (%)": [f"{(count/trials)*100:.2f}%" for count in counts]
            }
            st.dataframe(detail_data, use_container_width=True)
        
        # 동전 시뮬레이션
        elif simulation_type == "동전":
            results = [random.choice(["앞면", "뒷면"]) for _ in range(trials)]
            result_counts = Counter(results)
            
            sides = ["앞면", "뒷면"]
            counts = [result_counts.get(side, 0) for side in sides]
            colors = ['rgba(100, 200, 100, 0.7)', 'rgba(200, 100, 100, 0.7)']
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=sides,
                y=counts,
                marker_color=colors,
                text=counts,
                textposition='auto',
                name='횟수'
            ))
            
            fig.update_layout(
                title=f"동전 {trials}회 시뮬레이션 결과",
                xaxis_title="동전 면",
                yaxis_title="나온 횟수",
                height=500,
                showlegend=False,
                hovermode='x unified'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # 통계 정보
            st.subheader("📊 통계")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("총 시행 횟수", trials)
            with col2:
                front_prob = (counts[0] / trials) * 100
                st.metric("앞면 확률 (%)", f"{front_prob:.2f}%")
            with col3:
                st.metric("기댓값 (이론값)", "50%")
            
            # 상세 결과
            st.subheader("📋 상세 결과")
            detail_data = {
                "동전 면": sides,
                "나온 횟수": counts,
                "확률 (%)": [f"{(count/trials)*100:.2f}%" for count in counts]
            }
            st.dataframe(detail_data, use_container_width=True)
