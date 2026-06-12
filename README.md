# Cyber Routine Recommender

## 프로젝트 소개

Cyber Routine Recommender는 사용자의 보안 습관을 입력받아 개인 맞춤형 사이버 보안 루틴을 추천하는 웹 애플리케이션입니다.

이 프로젝트는 Streamlit 프론트엔드, FastAPI 백엔드, Docker 컨테이너, AWS EC2 배포 구조로 구현되었습니다.

## 주요 기능

- 사용자 보안 습관 입력
- FastAPI 백엔드로 추천 요청 전송
- 보안 위험 점수 계산
- 위험 등급 출력
- 맞춤형 보안 루틴 추천
- 이번 주 실천 계획 제공
- FastAPI JSON 응답 확인

## 기술 스택

- Frontend: Streamlit
- Backend: FastAPI
- Container: Docker, Docker Compose
- Deployment: AWS EC2

## 실행 방법

```bash
docker compose up --build -d