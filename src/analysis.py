import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

# ======================================================
# 1. 그래프 설정
# ======================================================
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# ======================================================
# 2. 파일 로드
# ======================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_name = os.path.join(BASE_DIR, "data", "ticket_price_data.csv")

if not os.path.exists(file_name):
    print("❌ 데이터 파일 없음")
    exit()

df = pd.read_csv(file_name, encoding='utf-8-sig')

print(df["Item"].value_counts())
print(df["Date"].min(), df["Date"].max())

# ======================================================
# 3. 전처리
# ======================================================
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
df = df.dropna(subset=['Date'])

df['DayNum'] = df['Date'].dt.dayofweek

if "CrawledAt" in df.columns:
    df = df.drop(columns=["CrawledAt"])

df = df.sort_values(["Item", "Date"])

print("\n=== 최신 날짜 ===")
print(df["Date"].max())

print("\n=== 요일 분포 ===")
print(df["Date"].dt.dayofweek.value_counts().sort_index())

print("\n=== 마지막 20개 데이터 ===")
print(df.tail(20))

# ======================================================
# 📊 4. 인기 아이템 TOP (거래량)
# ======================================================
popular_items = df.groupby("Item")["Count"].sum().sort_values(ascending=False)

top_item = popular_items.index[0]
top_item_count = popular_items.iloc[0]

# ======================================================
# 📈 5. 급등 TOP 3 (핵심 수정 부분)
# ======================================================
df["PrevPrice"] = df.groupby("Item")["Price"].shift(1)
df["ChangeRate"] = (df["Price"] - df["PrevPrice"]) / df["PrevPrice"] * 100

top_change = (
    df.dropna()
    .groupby("Item")["ChangeRate"]
    .max()
    .sort_values(ascending=False)
    .head(3)
)

# ======================================================
# 📉 6. 이동평균 (추세)
# ======================================================
df["MA3"] = df.groupby("Item")["Price"].transform(
    lambda x: x.rolling(3).mean()
)

# ======================================================
# 📊 7. 요일별 평균
# ======================================================
grouped = df.groupby(['Item', 'DayNum'])['Price'].mean().unstack()

grouped = grouped.reindex(columns=[0,1,2,3,4,5,6])
grouped.columns = ['월','화','수','목','금','토','일']

grouped = grouped.ffill().bfill()

# ======================================================
# 📊 8. 시각화
# ======================================================
fig, ax = plt.subplots(figsize=(12, 6))

for item in grouped.index:
    ax.plot(
        grouped.columns,
        grouped.loc[item],
        marker='o',
        linewidth=2,
        label=item
    )

# y축 포맷
ax.yaxis.set_major_formatter(
    mtick.FuncFormatter(lambda x, _: f'{x:,.0f}')
)

# ======================================================
# 📌 9. 그래프 안 정보 표시 (핵심)
# ======================================================
info_text = f"""📊 TOP 거래 아이템
- {top_item} ({top_item_count:,})

📈 급등 TOP 3
"""

for item, value in top_change.items():
    info_text += f"- {item} ({value:.2f}%)\n"

ax.text(
    0.02, 0.98,
    info_text,
    transform=ax.transAxes,
    verticalalignment='top',
    fontsize=10,
    bbox=dict(boxstyle="round", facecolor="white", alpha=0.85)
)

# ======================================================
# 10. 꾸미기
# ======================================================
ax.set_title("아이템별 요일 평균 시세 + 분석 대시보드", fontsize=15)
ax.set_xlabel("요일", fontsize=12)
ax.set_ylabel("평균 가격 (골드)", fontsize=12)

ax.grid(True, linestyle='--', alpha=0.6)
ax.legend()

plt.show()