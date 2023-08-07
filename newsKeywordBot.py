#step1.라이브러리 불러오기
import  requests
from  bs4  import  BeautifulSoup  as  bs
import  telegram
import  schedule
import  time

# step2.새로운 네이버 뉴스 기사 링크를 받아오는 함수
def get_new_links(query):

    # (주의) 네이버에서 키워드 검색 - 뉴스 탭 클릭 - 최신순 클릭 상태의 url
    url = f'https://search.naver.com/search.naver?where=news&query={query}&sm=tab_opt&sort=1&photo=0&field=0&pd=0&ds=&de=&docid=&related=0&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so%3Add%2Cp%3Aall&is_sug_officeid=0'

    # html 문서 받아서 파싱(parsing)
    #response = requests.get(url, headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')
    
    # status_code 200(정상)이 아닌경우, 검색 url 제공
    if(response.status_code != 200)
        bot.sendMessage(chat_id=chat_id, text='response 조회결과' + f"{response.status_code}")    
        bot.sendMessage(chat_id=chat_id, text='url 조회결과' + f"{url}")
    
    # 해당 페이지의 뉴스기사 링크가 포함된 html 요소 추출
    news_titles = soup.select('a.news_tit')

    # 요소에서 링크만 추출해서 리스트로 저장
    list_links = [i.attrs['href'] for i in news_titles]

    return list_links

def send_links(query):

    # 위에서 정의했던 함수 실행
    new_links = get_new_links(query)

    # 새로운 메시지가 있으면 링크 전송
    if new_links:
        bot.sendMessage(chat_id=chat_id, text='방금 업데이트 된 ' + f"{query} 주제의 크롤링입니다.")
        for link in new_links:
            bot.sendMessage(chat_id=chat_id, text=link)

    # 없으면 패스
    else:
        bot.sendMessage(chat_id=chat_id, text='검색 실패 된 ' + f"{query} 주제의 크롤링입니다. {new_links}")
        pass

# 실제 프로그램 구동
if __name__ == '__main__':
    # 토큰을 변수에 저장
    bot_token = '6661130983:AAEcYAWW-kKDIBHnKE4e9YovFvMbanYN8tQ'
    bot = telegram.Bot(token=bot_token)

    # 가장 최근에 온 메세지의 정보 중, chat id만 가져옴 (이 chat id는 사용자(나)의 계정 id임)
    chat_id = bot.getUpdates()[-1].message.chat.id # 6250265022

    # 검색할 키워드 설정
    queries = ["삼성카드", "신한카드", "현대카드", "국민카드", "신용카드", "금융감독원"]

    # 각 키워드에 대해 한 번씩 실행
    for query in queries:
        send_links(query)
        time.sleep(1)
    
    # 프로그램이 끝났음을 알리기 위한 메시지 전송
    bot.sendMessage(chat_id=chat_id, text='크롤링이 완료되었습니다.')

# 프로그램 종료
