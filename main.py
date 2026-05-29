import streamlit as st
import math
import random
import plotly.graph_objects as go
from collections import Counter

st.set_page_config(page_title="웹앱", page_icon="🧮", layout="wide")

# 사이드바에서 앱 선택
app_choice = st.sidebar.radio(
    "🔧 앱 선택",
    ["🧮 계산기", "🎲 확률 시뮬레이터"],
    index=0
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
        ),
        key="calc_operation"
    )
    
    # 사칙연산
    if operation == "사칙연산":
        num1 = st.number_input(
            "첫 번째 숫자",
            value=0.0,
            key="calc_num1"
        )
        
        num2 = st.number_input(
            "두 번째 숫자",
            value=0.0,
            key="calc_num2"
        )
        
        operator = st.selectbox(
            "연산자 선택",
            ("+", "-", "×", "÷"),
            key="calc_op"
        )
        
        if st.button("계산하기", key="calc_btn1"):
            result = None
            if operator == "+":
                result = num1 + num2
            elif operator == "-":
                result = num1 - num2
            elif operator == "×":
                result = num1 * num2
            elif operator == "÷":
                if num2 == 0:
                    st.error("0으로 나눌 수 없습니다.")
                    result = None
                else:
                    result = num1 / num2
            
            if result is not None:
                st.success(f"결과: {result}")
    
    # 모듈러 연산
    elif operation == "모듈러 연산":
        num1 = st.number_input(
            "숫자",
            value=0,
            step=1,
            key="mod_num1"
        )
        
        num2 = st.number_input(
            "나눌 값",
            value=1,
            step=1,
            key="mod_num2"
        )
        
        if st.button("계산하기", key="calc_btn2"):
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
            key="exp_base"
        )
        
        exponent = st.number_input(
            "지수",
            value=2.0,
            key="exp_exp"
        )
        
        if st.button("계산하기", key="calc_btn3"):
            result = base ** exponent
            st.success(f"결과: {result}")
    
    # 로그 연산
    elif operation == "로그 연산":
        number = st.number_input(
            "진수",
            value=10.0,
            min_value=0.000001,
            key="log_num"
        )
        
        base = st.number_input(
            "밑",
            value=10.0,
            min_value=0.000001,
            key="log_base"
        )
        
        if st.button("계산하기", key="calc_btn4"):
            if number <= 0 or base <= 0 or base == 1:
                st.error("올바른 로그 값을 입력하세요.")
            else:
                result = math.log(number, base)
                st.success(f"결과: {result}")

# ===============================================
# 확률 시뮬레이터 앱
# ===============================================
else:  # app_choice == "🎲 확률 시뮬레이터"
    st.title("🎲 확률 시뮬레이터")
    
    col1, col2 = st.columns(2)
    
    with col1:
        simulation_type = st.radio(
            "시뮬레이션 종류 선택",
            ["주사위", "동전"],
            key="sim_type"
        )
    
    with col2:
        trials = st.number_input(
            "시행 횟수",
            value=1000,
            min_value=1,
            step=100,
            key="sim_trials"
        )
    
    if st.button("시뮬레이션 실행", key="sim_btn"):
        st.write("")  # 공백
        
        # 주사위 시뮬레이션
        if simulation_type == "주사위":
            results = [random.randint(1, 6) for _ in range(trials)]
            result_counts = Counter(results)
            
            # 모든 면에 대한 카운트 (0이 아닌 경우도 포함)
            faces = list(range(1, 7))
            counts = [result_counts.get(face, 0) for face in faces]
            
            # 그래프 생성
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=[str(i) for i in faces],
                y=counts,
                marker=dict(
                    color='rgba(100, 150, 200, 0.8)',
                    line=dict(color='rgba(50, 100, 150, 1)', width=1)
                ),
                text=counts,
                textposition='auto',
                hovertemplate='<b>주사위 눈: %{x}</b><br>횟수: %{y}<extra></extra>'
            ))
            
            fig.update_layout(
                title=f"🎲 주사위 {trials}회 시뮬레이션 결과",
                xaxis_title="주사위 눈",
                yaxis_title="나온 횟수",
                height=500,
                showlegend=False,
                template="plotly_white"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # 통계 정보
            st.subheader("📊 통계")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("총 시행 횟수", trials)
            with col2:
                avg_val = sum(results) / len(results)
                st.metric("평균값", f"{avg_val:.2f}")
            with col3:
                st.metric("기댓값 (이론값)", "3.50")
            
            # 상세 결과
            st.subheader("📋 상세 결과")
            detail_list = []
            for face, count in zip(faces, counts):
                detail_list.append({
                    "주사위 눈": face,
                    "나온 횟수": count,
                    "확률 (%)": f"{(count/trials)*100:.2f}%"
                })
            
            st.table(detail_list)
        
        # 동전 시뮬레이션
        elif simulation_type == "동전":
            results = [random.choice([0, 1]) for _ in range(trials)]
            result_counts = Counter(results)
            
            sides = ["앞면", "뒷면"]
            counts = [result_counts.get(i, 0) for i in [0, 1]]
            colors = ['rgba(100, 200, 100, 0.8)', 'rgba(200, 100, 100, 0.8)']
            
            # 그래프 생성
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=sides,
                y=counts,
                marker=dict(
                    color=colors,
                    line=dict(color=['rgba(50, 150, 50, 1)', 'rgba(150, 50, 50, 1)'], width=1)
                ),
                text=counts,
                textposition='auto',
                hovertemplate='<b>%{x}</b><br>횟수: %{y}<extra></extra>'
            ))
            
            fig.update_layout(
                title=f"🪙 동전 {trials}회 시뮬레이션 결과",
                xaxis_title="동전 면",
                yaxis_title="나온 횟수",
                height=500,
                showlegend=False,
                template="plotly_white"
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
                st.metric("기댓값 (이론값)", "50.00%")
            
            # 상세 결과
            st.subheader("📋 상세 결과")
            detail_list = [
                {
                    "동전 면": "앞면",
                    "나온 횟수": counts[0],
                    "확률 (%)": f"{(counts[0]/trials)*100:.2f}%"
                },
                {
                    "동전 면": "뒷면",
                    "나온 횟수": counts[1],
                    "확률 (%)": f"{(counts[1]/trials)*100:.2f}%"
                }
            ]
            st.table(detail_list)
