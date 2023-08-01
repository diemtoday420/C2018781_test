# step1.라이브러리 불러오기
import requests
from bs4 import BeautifulSoup as bs
import telegram

# ... (기존의 코드)

def send_links(query):
    # 함수 내에서 처리된 리스트를 함수 외부에서 참조하기 위함
    global old_links_dict

    # Retrieve the old links list specific to the keyword
    old_links = old_links_dict.get(query, [])

    # 위에서 정의했던 함수 실행
    new_links = get_new_links(query, old_links)

    # 새로운 메시지가 있으면 링크 전송
    if new_links:
        bot.sendMessage(chat_id=chat_id, text='방금 업데이트 된 ' + f"{query} 주제의 크롤링입니다.")
        for link in new_links:
            bot.sendMessage(chat_id=chat_id, text=link)

    # 없으면 패스
    else:
        pass

    # 기존 링크를 계속 축적하기 위함
    old_links_dict[query] = old_links + new_links.copy()

# 실제 프로그램 구동
if __name__ == '__main__':
    # ... (기존의 코드)

    # 검색할 키워드 설정
    queries = ["삼성카드", "신한카드", "현대카드", "국민카드", "신용카드", "금융감독원"]

    # 각 키워드에 대해 한 번씩 실행
    for query in queries:
        send_links(query)
    
    # 프로그램이 끝났음을 알리기 위한 메시지 전송
    bot.sendMessage(chat_id=chat_id, text='크롤링이 완료되었습니다.')

# 프로그램 종료
