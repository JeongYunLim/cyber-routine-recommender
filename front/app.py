import os
import requests
import streamlit as st


BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")


st.set_page_config(
    page_title="Cyber Routine Recommender",
    page_icon="🔐",
    layout="centered"
)

st.title("개인 맞춤형 사이버 보안 루틴 추천 서비스")
st.caption("Streamlit + FastAPI + Docker + AWS EC2 기반 추천 웹 애플리케이션")

st.markdown("""
이 서비스는 사용자의 보안 습관을 입력받아  
FastAPI 백엔드에서 위험 점수를 계산하고,  
개인에게 맞는 사이버 보안 루틴을 추천합니다.
""")

st.divider()

st.subheader("1. 사용자 정보 입력")

user_type = st.selectbox(
    "사용자 유형을 선택하세요.",
    ["대학생", "개발자", "취업 준비생", "일반 사용자"]
)

main_concern = st.selectbox(
    "가장 걱정되는 보안 위협은 무엇인가요?",
    ["피싱", "계정 탈취", "악성코드", "개인정보 유출"]
)

st.subheader("2. 보안 습관 설문")

password_reuse = st.radio(
    "비밀번호를 여러 사이트에서 재사용하나요?",
    [
        "사이트마다 다른 비밀번호를 사용한다",
        "일부 사이트에서만 재사용한다",
        "여러 사이트에서 같은 비밀번호를 사용한다"
    ]
)

mfa_usage = st.radio(
    "MFA 또는 2단계 인증을 사용하나요?",
    [
        "대부분의 중요 계정에서 사용한다",
        "일부 계정에서만 사용한다",
        "사용하지 않는다"
    ]
)

suspicious_link = st.radio(
    "문자나 이메일의 의심스러운 링크를 클릭하는 편인가요?",
    [
        "거의 클릭하지 않는다",
        "가끔 클릭한다",
        "자주 클릭하는 편이다"
    ]
)

update_frequency = st.radio(
    "운영체제나 프로그램 업데이트는 얼마나 자주 하나요?",
    [
        "자동 업데이트를 사용한다",
        "가끔 한다",
        "거의 하지 않는다"
    ]
)

public_wifi = st.radio(
    "카페, 학교, 공항 등 공용 Wi-Fi를 자주 사용하나요?",
    [
        "거의 사용하지 않는다",
        "가끔 사용한다",
        "자주 사용한다"
    ]
)

github_public = st.radio(
    "GitHub 공개 저장소나 개인 블로그를 운영하나요?",
    [
        "공개 저장소를 운영하지 않는다",
        "공개 저장소를 운영한다"
    ]
)

st.divider()

if st.button("보안 루틴 추천받기", type="primary"):
    payload = {
        "user_type": user_type,
        "password_reuse": password_reuse,
        "mfa_usage": mfa_usage,
        "suspicious_link": suspicious_link,
        "update_frequency": update_frequency,
        "public_wifi": public_wifi,
        "github_public": github_public,
        "main_concern": main_concern
    }

    try:
        response = requests.post(
            f"{BACKEND_URL}/recommend",
            json=payload,
            timeout=10
        )

        if response.status_code == 200:
            result = response.json()

            st.success("FastAPI 백엔드에서 추천 결과를 성공적으로 받았습니다.")

            st.subheader("3. 보안 위험 진단 결과")

            col1, col2 = st.columns(2)
            with col1:
                st.metric("보안 점수", f"{result['score']}점")
            with col2:
                st.metric("위험 등급", result["risk_level"])

            score = result["score"]

            if score >= 85:
                st.progress(score)
            elif score >= 65:
                st.progress(score)
                st.warning(result["risk_description"])
            else:
                st.progress(score)
                st.error(result["risk_description"])

            st.info(f"추천 방향: {result['focus_area']}")

            st.subheader("4. 주요 취약 습관")
            for weakness in result["main_weaknesses"]:
                st.write(f"- {weakness}")

            st.subheader("5. 맞춤형 추천 보안 루틴")
            for rec in result["recommendations"]:
                st.write(f"- {rec}")

            st.subheader("6. 이번 주 실천 계획")
            for plan in result["weekly_plan"]:
                st.write(f"- {plan}")

            with st.expander("FastAPI JSON 응답 확인"):
                st.json(result)

        else:
            st.error("FastAPI 서버에서 오류 응답을 받았습니다.")
            st.write(response.text)

    except requests.exceptions.RequestException as e:
        st.error("FastAPI 백엔드에 연결할 수 없습니다.")
        st.write(f"오류 내용: {e}")

st.divider()

st.caption("본 서비스는 교육용 추천 웹 애플리케이션입니다.")