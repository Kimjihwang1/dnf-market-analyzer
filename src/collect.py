#1. 라이브러리 및 변수 세팅 (준비 단계)
import requests
import pandas as pd
import os
import matplotlib.pyplot as plt
from DNF_ITEM_ANALYZE.src.config import API_KEY

# 윈도우 환경 기준 한글 폰트 설정 (맥은 'AppleGothic' 사용)
plt.rcParams['font.family'] = 'Malgun Gothic'
# 마이너스 기호 깨짐 방지
plt.rcParams['axes.unicode_minus'] = False

ITEM_NAME = "닳아버린 순례의 증표"

print("=======================================================")

#2. Phase 1: 아이템 이름으로 고유 ID 찾기
print(f"[{ITEM_NAME}] 고유 ID를 서버에 요청합니다...")

search_url = f"https://api.neople.co.kr/df/items?itemName={ITEM_NAME}&wordType=match&apikey={API_KEY}"

response = requests.get(search_url)  #requests.get() 은 모듈 안의 함수를 . 으로 접근!

search_data = response.json()

print(search_data)

if "rows" in search_data and len(search_data["rows"]) > 0:
    item_id = search_data["rows"][0]["itemId"]
    print(f"아이템 ID 획득 성공: {item_id}\n")
else:
    print("아이템을 찾을수 없음")
    exit()

print("=======================================================")
    
#3. Phase 2: 고유 ID로 최근 거래 내역 가져오기
print("최근 경매장 거래 내역을 불러옵니다...")

auction_url =f"https://api.neople.co.kr/df/auction-sold?itemId={item_id}&limit=10&apikey={API_KEY}"

auction_response = requests.get(auction_url)
auction_data = auction_response.json()

print("=======================================================")

#4. Phase 3: 데이터 파싱 및 CSV 누적 저장

if "rows" in auction_data:
    print("---최근 거래 내역 TOP 10---")
    
    empty_data =[]
    
    for idx,row in enumerate(auction_data["rows"]):
        sold_date = row.get("soldDate","날짜 없음")
        price = row.get("unitPrice",0)
        count = row.get("count",0)
        
        print(f"{idx +1}. 거래일시: {sold_date} | 단가:{price:,}골드 | 수량: {count}개")
        
        empty_data.append({
            "Date" : sold_date,
            "Price" : price,
            "Count" : count
        })
        
    
  # ------------------ 파일 저장 로직 ------------------
    df = pd.DataFrame(empty_data)
    
    # 💡 핵심 수정: collect.py 파일이 있는 곳의 정확한 주소를 알아냅니다.
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # 무조건 collect.py 옆에 있는 파일에만 적도록 주소를 강제로 묶어버립니다.
    file_name = os.path.join(BASE_DIR,"data", "ticket_price_data.csv")
    
    if not os.path.exists(file_name):
        df.to_csv(file_name, index=False, mode='w', encoding="utf-8-sig")
    else:
        df.to_csv(file_name, index=False, mode='a', header=False, encoding="utf-8-sig")
        
    print(f"\n✅ 데이터가 '{file_name}'에 성공적으로 적재 되었습니다")
            
        
else:
    print("거래 내역을 불러오는데 실패 했습니다")




