import os
import pandas as pd
import matplotlib.pyplot as plt

# 1. 그래프 한글 깨짐 방지 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 💡 쇠말뚝 박기: analysis.py가 있는 폴더 주소를 알아내서 그 옆에 있는 엑셀을 찾게 함
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_name = os.path.join(BASE_DIR, "data", "ticket_price_data.csv")

# 파일이 있는지 검사할 때도 file_name 사용
if not os.path.exists(file_name):
    print("❌ 'ticket_price_data.csv' 파일이 없습니다. 수집기(collect.py)를 먼저 실행하세요.")
    exit() # 프로그램 종료


# 2. 데이터 로드 및 전처리
df = pd.read_csv(file_name, encoding='utf-8-sig')
df['Date'] = pd.to_datetime(df['Date'], format='mixed')
df['DayNum'] = df['Date'].dt.dayofweek

# 3. 요일별 평균 시세 계산
avg_price = df.groupby('DayNum')['Price'].mean()

# 숫자로 된 인덱스를 한글 요일로 변경
day_labels = {0: '월', 1: '화', 2: '수', 3: '목', 4: '금', 5: '토', 6: '일'}
avg_price.index = [day_labels[x] for x in avg_price.index]

print("--- 요일별 평균 데이터 ---")
print(avg_price)

# 4. 시각화 (바 차트)
plt.figure(figsize=(10, 6))
#plt.bar(avg_price.index, avg_price.values, color='steelblue')
plt.plot(avg_price.index, avg_price.values, marker ='o', color ='red', linewidth =2,markersize= 8)

plt.title('요일별 닳아버린 순례의 증표 평균 시세 분석', fontsize=15)
plt.xlabel('요일', fontsize=12)
plt.ylabel('평균 가격 (골드)', fontsize=12)

plt.ylim(240000,290000)

# Y축 천 단위 콤마 포맷
current_values = plt.gca().get_yticks()
plt.gca().set_yticklabels(['{:,.0f}'.format(x) for x in current_values])

plt.grid(True,linestyle ='--' , alpha =0.6)

plt.show()