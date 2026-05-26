# DNF 경매장 시세 분석 파이프라인

## 📌 프로젝트 개요
던전앤파이터 경매장 오픈 API를 활용한 데이터 파이프라인(ETL) 구축 프로젝트. 
특정 아이템의 거래 데이터를 수집하고, 요일별 시세 변동을 시각화합니다. 
차후 스케줄러 자동화를 위해 데이터 수집과 분석 로직을 물리적으로 분리했습니다.

## 🛠 사용 기술
- **Language:** Python 3
- **Library:** `requests`(API 통신), `pandas`(데이터 가공), `matplotlib`(시각화)

## 📂 핵심 구조
- **`collect.py`:** API 통신 -> JSON 파싱 -> `ticket_price_data.csv` 누적(Append) 적재
- **`analysis.py`:** CSV 로드 -> Datetime 변환 및 요일 추출 -> 평균가 계산 -> 바 차트 시각화

---

⚡ Trouble Shooting(5/26)
JSON 다중 구조 파싱
.get()을 활용한 예외 처리
CSV Append 저장 처리
PermissionError(File Lock) 해결
수집/분석 모듈 분리

👉 상세 TIL & 트러블슈팅 정리
[(https://www.notion.so/4-RE-36c3b284a47680c8946fdf96529ed340)]

