import os
import schedule
import time
import subprocess
from datetime import datetime

# 💡 핵심 추가: 현재 auto_run.py 파일이 있는 폴더의 절대 경로를 알아냅니다.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# 그 폴더 안에 있는 collect.py의 정확한 주소를 만듭니다.
COLLECT_FILE = os.path.join(BASE_DIR, "collect.py")

def run_collect():
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"\n🔄 [{current_time}] 자동으로 던파 경매장 데이터를 수집합니다...")
    print(f"📂 실행하는 파일 위치: {COLLECT_FILE}") # 위치 확인용 출력
    
    # 수정: 그냥 "collect.py" 대신, 정확한 주소(COLLECT_FILE)를 넣어서 실행합니다.
    result = subprocess.run(["python", COLLECT_FILE], capture_output=True, text=True,encoding="utf-8")
    
    if result.stdout:
        print(result.stdout.strip())
    if result.stderr:
        print(f"❌ 에러 발생: {result.stderr.strip()}")
        
# 1시간 주기 세팅 (API 차단 방지 및 실데이터 누적용)
schedule.every(1).hours.do(run_collect)

print("🚀 던파 경매장 자동 수집 프로그램이 시작되었습니다. (10초 주기)")
print("정지하려면 터미널에서 Ctrl + C를 누르세요.\n")

while True:
    schedule.run_pending()
    time.sleep(1)