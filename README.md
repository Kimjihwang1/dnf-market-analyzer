Markdown
# 📈 DNF 경매장 시세 분석 파이프라인

## 📌 프로젝트 개요
던전앤파이터 경매장 오픈 API를 활용한 데이터 파이프라인(ETL) 구축 프로젝트입니다. 
특정 아이템의 실거래 데이터를 수집하고, 요일별/시간대별 시세 변동 트렌드를 시각화합니다. 
데이터 수집과 분석 로직을 물리적으로 분리하였으며, 스케줄러를 통해 지속적인 데이터 자동 적재 환경을 구축했습니다.

## 🛠 사용 기술
- **Language:** Python 3
- **Library:** `requests` (API 통신), `pandas` (데이터 가공), `matplotlib` (시각화), `schedule` (자동화)

## 📂 핵심 구조
- **`collect.py`:** API 통신 ➔ JSON 파싱 ➔ 데이터 중복 검증(drop_duplicates) ➔ ticket_price_data.csv 안전 적재 (데이터 무결성 확보)
- **`auto_run.py` (New ✨):** `collect.py`를 백그라운드에서 1시간 주기로 자동 실행하는 스케줄러 모듈
- **`analysis.py`:** CSV 로드 ➔ Datetime 변환 및 요일 추출 ➔ 시세 데이터 전처리 및 시각화

## 🚀 실행 방법
1. 필요 패키지 설치

pip install requests pandas matplotlib schedule

2.collect.py 내부 API_KEY 변수에 본인의 네오플 오픈 API 키 입력

3.스케줄러를 통한 자동 데이터 수집 시작

python auto_run.py

4.수집된 데이터 분석 및 시각화 확인

python analysis.py


## ⚡ Trouble Shooting
👉 [요일별 상세 TIL & 트러블슈팅 정리 노트(Notion)](https://www.notion.so/Portfolio-36d3b284a476809e83ebd797b6bbc549)
