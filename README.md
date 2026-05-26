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

## 📝 TIL & 트러블슈팅

**1. JSON 다중 구조 파싱**
- `Dict -> List -> Dict`로 꼬인 응답 데이터 파싱 문제.
- `data["rows"][0]["itemId"]` 형태로 순차적 인덱싱 및 키 접근법 적용.

**2. `.get()`을 통한 예외 처리**
- API 응답 누락 시 발생하는 KeyError 방어.
- `row.get("price", 0)`을 사용해 데이터 누락 시 프로그램이 뻗지 않도록 기본값 처리.

**3. CSV 데이터 누적 적재**
- 코드 실행 시마다 기존 파일이 덮어씌워지는 현상 발생.
- Pandas `to_csv(mode='a', header=False)` 옵션을 주어 기존 데이터 밑에 이어 붙이도록(Append) 해결.

**4. PermissionError (파일 점유)**
- CSV를 엑셀로 열어둔 상태에서 코드 실행 시 I/O 충돌 발생. 
- 프로세스의 파일 점유(Lock) 개념 확인.

**5. 모듈 분리 (수집/시각화)**
- 백그라운드 자동화 시 차트 팝업창이 프로세스를 막는 문제 사전 차단.
- 수집기(`collect.py`)와 분석기(`analysis.py`)로 아키텍처 완전 분리.
