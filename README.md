# 📈 DNF 경매장 시세 분석 파이프라인

## 📌 프로젝트 개요
던전앤파이터 경매장 오픈 API를 활용한 데이터 파이프라인(ETL) 구축 프로젝트입니다. 
특정 아이템의 실거래 데이터를 수집하고, 요일별/시간대별 시세 변동 트렌드를 시각화합니다. 
데이터 수집과 분석 로직을 물리적으로 분리하였으며, 스케줄러를 통해 지속적인 데이터 자동 적재 환경을 구축했습니다.

## 🛠 사용 기술
- **Language:** Python 3
- **Library:** `requests` (API 통신), `pandas` (데이터 가공), `matplotlib` (시각화), `schedule` (자동화)

## 📂 핵심 구조
- **`collect.py`:** API 통신 ➔ JSON 파싱 ➔ `ticket_price_data.csv` 누적(Append) 적재
- **`auto_run.py` (New ✨):** `collect.py`를 백그라운드에서 1시간 주기로 자동 실행하는 스케줄러 모듈
- **`analysis.py`:** CSV 로드 ➔ Datetime 변환 및 요일 추출 ➔ 시세 데이터 전처리 및 시각화

---

## ⚡ Trouble Shooting

### 📅 5/26 (수집/분석 모듈화)
- JSON 다중 구조 파싱 및 `.get()`을 활용한 예외 처리
- CSV Append 모드 저장 처리
- PermissionError (File Lock) 해결을 위한 파일 입출력 로직 개선
- 수집 모듈과 분석 모듈의 물리적 분리 완료

### 📅 5/27 (자동화 파이프라인 구축 및 경로/파싱 버그 수정)
- **자동화 스케줄러(`auto_run.py`) 도입**
  - 수동으로 돌리던 수집 코드를 `schedule` 라이브러리를 활용해 1시간 주기 무인 자동화로 격상.
  - 잦은 API 호출로 인한 디도스 차단(IP Block)을 방지하기 위해 서버 친화적인 수집 주기로 최적화.
- **상대 경로의 저주 (파일 분리 현상) 해결**
  - 스케줄러 실행 위치에 따라 CSV 파일이 엉뚱한 곳에 생성되는 버그 발생.
  - `os.path.abspath(__file__)`를 활용해 수집기 파일 기준의 **절대 경로(Base Directory)**를 고정하여 완벽히 해결.
- **Pandas 날짜 변환(to_datetime) ValueError 해결**
  - API 데이터 중 초(Second) 단위 포맷이 섞여 들어오며 파싱 에러로 프로그램이 중단되는 현상 발생.
  - `format='mixed'` 파라미터를 추가하여 판다스 엔진이 다양한 시간 포맷을 자동 추론 및 방어하도록 조치.

---
👉 [상세 TIL & 트러블슈팅 정리 노트 (Notion)](https://www.notion.so/4-RE-36c3b284a47680c8946fdf96529ed340)
