import requests
from bs4 import BeautifulSoup as bs
import telegram
import schedule
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Referer': 'https://www.google.com'
} # 간헐적 403 에러 방지용

# 새로운 네이버 뉴스 기사 링크를 받아오는 함수
def get_new_links(query):
    # (주의) 네이버에서 키워드 검색 - 뉴스 탭 클릭 - 최신순 클릭 상태의 url
    url = f'https://search.naver.com/search.naver?where=news&query={query}&sm=tab_opt&sort=1&photo=0&field=0&pd=0&ds=&de=&docid=&related=0&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so%3Add%2Cp%3Aall&is_sug_officeid=0'

    response = requests.get(url, headers=headers)
    soup = bs(response.text, 'html.parser')
    
    # status_code 200(정상)이 아닌경우, 검색 url 제공
    if response.status_code != 200 :
        bot.sendMessage(chat_id=chat_id, text=f"{response.status_code}"+' 에러로 파싱실패. 아래 URL을 통해 이용해주세요.')    
        bot.sendMessage(chat_id=chat_id, text='url 조회결과' + f"{url}")

    # 해당 페이지의 뉴스기사 링크가 포함된 html 요소 추출
    news_titles = soup.select('a.news_tit')

    # 요소에서 링크만 추출해서 리스트로 저장
    list_links = [i.attrs['href'] for i in news_titles]

    return list_links

def send_links(query):
    # 위에서 정의했던 함수 실행
    new_links = get_new_links(query)
    
    if not new_links:
        return  # 새로운 링크가 없으면 함수 종료
    
    # 가장 많은 클릭수를 가진 기사를 찾기 위한 변수 초기화
    max_clicks = 0
    best_link = None

    for link in new_links:
        response = requests.get(f'https://www.viva100.com/main/view.php?key=20230917010004756', headers=headers)
        soup = bs(response.text, 'html.parser')

        # 각 기사의 클릭수 정보 추출
        clicks = soup.select_one('.tomain_info span.u_cnt')
        
        if clicks:
            clicks = int(clicks.text.replace(",", ""))  # 클릭수에서 쉼표 제거 후 정수로 변환

            # 가장 많은 클릭수를 가진 기사를 찾음
            if clicks > max_clicks:
                max_clicks = clicks
                best_link = link

    if best_link:
        bot.sendMessage(chat_id=chat_id, text=f'방금 업데이트 된 "{query}" 주제의 크롤링입니다.')
        bot.sendMessage(chat_id=chat_id, text=best_link)

# 실제 프로그램 구동
if __name__ == '__main__':
    # 토큰을 변수에 저장
    bot_token = '6661130983:AAEcYAWW-kKDIBHnKE4e9YovFvMbanYN8tQ'  # 수정1 예) 6661130983:BBKcYAWW-kKDIBHnKE4e9YovFvMbanYN8tQ
    bot = telegram.Bot(token=bot_token)

    # 가장 최근에 온 메세지의 정보 중, chat id만 가져옴 (이 chat id는 사용자(나)의 계정 id임)
    chat_id = '6250265022' # bot.getUpdates()[-1].message.chat.id # 수정2 예) '6250265022'와 같이 숫자로된 10글자 ID 

    # 검색할 키워드 설정
    queries = ["신용카드", "제휴카드", "카드사 제휴계약", "카드사 전략적제휴", "신용카드 상품", "신용카드 서비스", "PLCC", "카드사 MOU"]

    # 각 키워드에 대해 한 번씩 실행
    for query in queries:
        send_links(query)
        time.sleep(1)
    
    # 프로그램이 끝났음을 알리기 위한 메시지 전송
    bot.sendMessage(chat_id=chat_id, text='크롤링이 완료되었습니다.')

# 프로그램 종료
