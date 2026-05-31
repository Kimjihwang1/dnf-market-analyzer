#1. 라이브러리 및 변수 세팅 (준비 단계)
import requests
import pandas as pd
import os
import matplotlib.pyplot as plt

from datetime import datetime
from config import API_KEY

# 윈도우 환경 기준 한글 폰트 설정 (맥은 'AppleGothic' 사용)
plt.rcParams['font.family'] = 'Malgun Gothic'
# 마이너스 기호 깨짐 방지
plt.rcParams['axes.unicode_minus'] = False


# =========================
# 2. 여러 아이템 설정
# =========================

ITEM_LIST =[
    "닳아버린 순례의 증표",
    "광휘의 소울 결정",
    "에픽 소울 결정"
    
]
print("=======================================================")

all_data =[]

# =========================
# 3. 아이템 반복 수집
# =========================

for ITEM_NAME in ITEM_LIST:
    print(f"[{ITEM_NAME}] 데이터 수집 시작")
    
    search_url = f"https://api.neople.co.kr/df/items?itemName={ITEM_NAME}&wordType=match&apikey={API_KEY}"
    response = requests.get(search_url)  #requests.get() 은 모듈 안의 함수를 . 으로 접근!
    search_data = response.json()

    if "rows" not in search_data or len(search_data["rows"]) ==0:
        print(f"{ITEM_NAME}을 찾을 수 없음")
        continue
    
    item_id = search_data["rows"][0]["itemId"]

    auction_url =f"https://api.neople.co.kr/df/auction-sold?itemId={item_id}&limit=10&apikey={API_KEY}"
    auction_response =requests.get(auction_url)
    auction_data =auction_response.json()
    
    if "rows" not in auction_data:
        print(f"{ITEM_NAME} 거래 데이터 없음")
        continue
    
    # =========================
    # 4. 데이터 파싱 + 날짜시간 추가
    # =========================
    for row in auction_data["rows"]:
        sold_date = row.get("soldDate")
        price = row.get("unitPrice", 0)
        count = row.get("count", 0)

        all_data.append({
            "Item": ITEM_NAME,
            "Date": datetime.now().strftime("%Y-%m-%d"),
            "Price": price,
            "Count": count,
            "CrawledAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

# =========================
# 5. DataFrame 생성
# =========================
COLUMNS = ["Item", "Date", "Price", "Count", "CrawledAt"]

df = pd.DataFrame(all_data, columns=COLUMNS)

df = df.drop_duplicates(subset=["Item", "Date", "Price", "Count"])

if df.empty:
    print("❌ 수집된 데이터 없음")
    exit()

# =========================
# 6. 최고가 / 최저가 계산
# =========================
summary = df.groupby("Item")["Price"].agg(["max", "min"])

print("\n==============================")
print("📊 아이템별 최고가 / 최저가")
print("==============================")

for item, row in summary.iterrows():
    print(f"{item}")
    print(f"  🔺 최고가: {row['max']:,} 골드")
    print(f"  🔻 최저가: {row['min']:,} 골드\n")

# =========================
# 7. CSV 저장
# =========================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_name = os.path.join(BASE_DIR, "data", "ticket_price_data.csv")

if not os.path.exists(file_name):
    df.to_csv(file_name, index=False, encoding="utf-8-sig")
else:
    df.to_csv(file_name, index=False, mode="a", header=False, encoding="utf-8-sig")

print(f"✅ 데이터 저장 완료: {file_name}")
    














