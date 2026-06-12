from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


app = FastAPI(
    title="Cyber Routine Recommender API",
    description="사용자의 보안 습관을 기반으로 개인 맞춤형 사이버 보안 루틴을 추천하는 API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SecurityInput(BaseModel):
    user_type: str
    password_reuse: str
    mfa_usage: str
    suspicious_link: str
    update_frequency: str
    public_wifi: str
    github_public: str
    main_concern: str


@app.get("/")
def root():
    return {
        "message": "Cyber Routine Recommender API is running.",
        "status": "ok"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "FastAPI backend"
    }


@app.post("/recommend")
def recommend_security_routine(data: SecurityInput):
    score = 100
    weaknesses = []
    recommendations = []
    weekly_plan = []

    # 1. 비밀번호 재사용 평가
    if data.password_reuse == "여러 사이트에서 같은 비밀번호를 사용한다":
        score -= 25
        weaknesses.append("비밀번호 재사용")
        recommendations.append("중요 계정부터 서로 다른 비밀번호로 변경하세요.")
        recommendations.append("비밀번호 관리자를 사용하여 계정별 비밀번호를 분리하세요.")
        weekly_plan.append("1일차: 이메일, GitHub, 은행, 학교 계정의 비밀번호를 각각 다르게 변경하기")

    elif data.password_reuse == "일부 사이트에서만 재사용한다":
        score -= 12
        weaknesses.append("일부 계정의 비밀번호 재사용")
        recommendations.append("자주 사용하는 계정부터 비밀번호 재사용을 줄이세요.")
        weekly_plan.append("1일차: 자주 사용하는 5개 계정의 비밀번호 중복 여부 확인하기")

    # 2. MFA 사용 평가
    if data.mfa_usage == "사용하지 않는다":
        score -= 25
        weaknesses.append("MFA 미사용")
        recommendations.append("이메일, GitHub, 클라우드 계정부터 MFA를 활성화하세요.")
        weekly_plan.append("2일차: 이메일과 GitHub에 MFA 설정하기")

    elif data.mfa_usage == "일부 계정에서만 사용한다":
        score -= 10
        weaknesses.append("MFA 적용 범위 부족")
        recommendations.append("중요 계정 전체에 MFA를 확대 적용하세요.")
        weekly_plan.append("2일차: 자주 사용하는 서비스의 MFA 설정 상태 확인하기")

    # 3. 의심 링크 클릭 습관 평가
    if data.suspicious_link == "자주 클릭하는 편이다":
        score -= 20
        weaknesses.append("피싱 링크 노출 위험")
        recommendations.append("링크를 클릭하기 전 URL 도메인과 발신자를 먼저 확인하세요.")
        recommendations.append("긴급 결제, 계정 정지, 택배 주소 변경 메시지는 특히 주의하세요.")
        weekly_plan.append("3일차: 최근 받은 문자와 이메일 중 의심 링크 사례 정리하기")

    elif data.suspicious_link == "가끔 클릭한다":
        score -= 10
        weaknesses.append("의심 링크 확인 습관 부족")
        recommendations.append("의심 링크는 바로 누르지 말고 공식 앱이나 공식 홈페이지에서 직접 확인하세요.")
        weekly_plan.append("3일차: 피싱 메시지의 특징 3가지 정리하기")

    # 4. 업데이트 습관 평가
    if data.update_frequency == "거의 하지 않는다":
        score -= 15
        weaknesses.append("보안 업데이트 부족")
        recommendations.append("운영체제, 브라우저, 백신, 주요 앱의 자동 업데이트를 켜세요.")
        weekly_plan.append("4일차: Windows Update와 브라우저 업데이트 상태 확인하기")

    elif data.update_frequency == "가끔 한다":
        score -= 7
        weaknesses.append("불규칙한 업데이트")
        recommendations.append("최소 주 1회 업데이트 확인 루틴을 만드세요.")
        weekly_plan.append("4일차: 자주 사용하는 프로그램 업데이트 확인하기")

    # 5. 공용 Wi-Fi 사용 평가
    if data.public_wifi == "자주 사용한다":
        score -= 10
        weaknesses.append("공용 Wi-Fi 사용 위험")
        recommendations.append("공용 Wi-Fi에서는 금융, 결제, 관리자 페이지 접속을 피하세요.")
        weekly_plan.append("5일차: 공용 Wi-Fi 사용 시 주의할 서비스 목록 만들기")

    elif data.public_wifi == "가끔 사용한다":
        score -= 5
        weaknesses.append("공용 네트워크 노출 가능성")
        recommendations.append("공용 Wi-Fi에서는 HTTPS 여부와 접속 서비스를 확인하세요.")
        weekly_plan.append("5일차: 자주 접속하는 사이트의 HTTPS 여부 확인하기")

    # 6. GitHub 공개 여부 평가
    if data.github_public == "공개 저장소를 운영한다":
        score -= 8
        weaknesses.append("공개 저장소 정보 노출 가능성")
        recommendations.append(".env, API key, 토큰, 비밀번호 파일이 GitHub에 올라가지 않았는지 확인하세요.")
        recommendations.append(".gitignore 파일을 점검하고 민감 정보는 환경 변수로 분리하세요.")
        weekly_plan.append("6일차: GitHub 저장소에서 .env, key, token 문자열 검색하기")

    # 점수 보정
    if score < 0:
        score = 0

    # 위험 등급 산정
    if score >= 85:
        risk_level = "안전"
        risk_description = "현재 보안 습관이 비교적 안정적입니다."
    elif score >= 65:
        risk_level = "주의"
        risk_description = "일부 습관에서 계정 탈취나 개인정보 노출 위험이 있습니다."
    elif score >= 40:
        risk_level = "위험"
        risk_description = "여러 보안 습관에서 개선이 필요합니다."
    else:
        risk_level = "매우 위험"
        risk_description = "계정 탈취, 피싱, 악성코드 감염 위험이 높습니다."

    # 사용자 관심 위협별 맞춤 추천
    if data.main_concern == "피싱":
        recommendations.append("의심 메시지는 링크를 누르지 말고 공식 앱에서 직접 확인하세요.")
        focus_area = "피싱 대응 중심 루틴"
    elif data.main_concern == "계정 탈취":
        recommendations.append("비밀번호 변경, MFA 설정, 로그인 기록 확인을 우선 수행하세요.")
        focus_area = "계정 보호 중심 루틴"
    elif data.main_concern == "악성코드":
        recommendations.append("출처가 불분명한 실행 파일을 열지 말고 백신 검사를 주기적으로 수행하세요.")
        focus_area = "악성코드 예방 중심 루틴"
    else:
        recommendations.append("개인정보가 포함된 파일과 계정 공개 범위를 점검하세요.")
        focus_area = "개인정보 보호 중심 루틴"

    # 약점이 없는 경우
    if not weaknesses:
        weaknesses.append("큰 취약 습관 없음")
        recommendations.append("현재 습관을 유지하되, 월 1회 계정 보안 점검을 수행하세요.")
        weekly_plan.append("이번 주: 주요 계정 로그인 기록과 연결된 기기 확인하기")

    # 중복 제거
    recommendations = list(dict.fromkeys(recommendations))
    weekly_plan = list(dict.fromkeys(weekly_plan))

    return {
        "score": score,
        "risk_level": risk_level,
        "risk_description": risk_description,
        "user_type": data.user_type,
        "focus_area": focus_area,
        "main_weaknesses": weaknesses,
        "recommendations": recommendations,
        "weekly_plan": weekly_plan,
        "api_message": "FastAPI에서 추천 결과를 생성했습니다."
    }