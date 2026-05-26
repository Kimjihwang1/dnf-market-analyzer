#JSON헀을때 "rows" =key값 형태를 간단하게 하면
# search_data ={"rows": [{~~~}, {~~~}]}
# 즉 딕셔너리 → 리스트 → 딕셔너리 3중 구조!!!(매우 복잡함!)
# {
#   "rows": [
#     {
#       "auctionNo": 12345678,
#       "regDate": "2026-05-26 19:00:00",
#       "soldDate": "2026-05-26 19:17:26",
#       "itemId": "어쩌구저쩌구",
#       "itemName": "닳아버린 순례의 증표",
#       "count": 3,
#       "price": 810000,
#       "unitPrice": 270000
#     },
#     {
#       "auctionNo": 12345679,
#       "regDate": "...",
#       "soldDate": "2026-05-26 19:16:56",
#       "count": 5,
#       "unitPrice": 277776
#     }
#   ]
# }


# auction_data = {
#     "rows": [          # 리스트
#         {              # 첫번째 딕셔너리
#             "auctionNo": 12345678,
#             "soldDate": "2026-05-26 19:17:26",
#             "unitPrice": 270000,
#             "count": 3
#         },
#         {              # 두번째 딕셔너리
#             "auctionNo": 12345679,
#             "soldDate": "2026-05-26 19:16:56",
#             "unitPrice": 277776,
#             "count": 5
#         }
#     ]
# }


#반복문 첫 번째 돌 때 row에 담겨있는 데이터
# row = {
#   "auctionNo": 12345678,
#   "regDate": "2026-05-26 19:00:00",
#   "soldDate": "2026-05-26 19:17:26",
#   "itemId": "어쩌구저쩌구",
#   "itemName": "닳아버린 순례의 증표",
#   "count": 3,
#   "price": 810000,
#   "unitPrice": 270000
# }

# enumerate 없이도 가능 인덱스 번호붙이려고 쓴거
# for row in auction_data["rows"]:
#     sold_date = row.get("soldDate", "날짜 없음")
#     price = row.get("unitPrice", 0)
#     count = row.get("count", 0)
#     print(f"거래일시: {sold_date} | 단가:{price:,}골드 | 수량: {count}개")