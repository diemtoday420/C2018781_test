import requests
from bs4 import BeautifulSoup as bs
import telegram
import schedule
import time

# 새로운 네이버 뉴스 기사 링크를 받아오는 함수
def get_new_links(query):
    # (주의) 네이버에서 키워드 검색 - 뉴스 탭 클릭 - 최신순 클릭 상태의 url
    url = f'https://search.naver.com/search.naver?where=news&query={query}&sm=tab_opt&sort=1&photo=0&field=0&pd=0&ds=&de=&docid=&related=0&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so%3Add%2Cp%3Aall&is_sug_officeid=0'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Referer': 'https://www.google.com'
    } # 간헐적 403 에러 방지용
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
        response = requests.get(link)
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

# 텔레그램 봇 설정
bot_token = '6475089075:AAF8WNH8f74V-BK-k7QTIxEXupveQO62mWE'  # 텔레그램 봇 토큰 입력
bot = telegram.Bot(token=bot_token)
chat_id = '614924343'  # 채팅 ID 입력

# 검색할 키워드 설정
queries = ["신용카드", "제휴카드", "카드사 제휴계약", "카드사 전략적제휴", "신용카드 상품", "신용카드 서비스", "PLCC", "카드사 MOU"]

# 각 키워드별로 스케줄링 설정
for query in queries:
    schedule.every().day.at("07:00").do(send_links, query)

# 스케줄러 실행
while True:
    schedule.run_pending()
    time.sleep(1)
