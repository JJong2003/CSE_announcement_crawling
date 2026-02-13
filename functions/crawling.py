import requests
from bs4 import BeautifulSoup
import re
import myDB

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
urls = ['https://computer.cnu.ac.kr/computer/notice/bachelor.do',   #학사공지
        'https://computer.cnu.ac.kr/computer/notice/notice.do',     #교내일반소식
        'https://computer.cnu.ac.kr/computer/notice/job.do',        #교외활동∙인턴∙취업
        'https://computer.cnu.ac.kr/computer/notice/project.do'    #사업단소식
        ]

def crawl():
    for url in urls:
        try:
            data = requests.get(url, headers=headers)
            soup = BeautifulSoup(data.text, 'html.parser')

            titles = soup.select("td.b-td-left > div > a")
            posting_dates = soup.select("#item_body > div > div > div.content-wrap > div.sub-content > div > div > div.bn-list-common01.type01.bn-common > table > tbody > tr > td:nth-child(5)")
            category_tag = soup.select("#item_body > div > div > div.content-wrap > div.title-box > div > h3")
            category = str(category_tag[0])[4:len(category_tag)-6]

            posts = []
            for raw_title, raw_date in zip(titles, posting_dates):
                title = raw_title.text.strip().split('\n')[0]
                date = raw_date.text.strip()
                js_link = raw_title.get('href', '')
                article_no_match = re.search(r"articleNo=(\d+)", js_link) #정규표현식
                
                if article_no_match:
                    article_no = article_no_match.group(1)
                    # URL 조립 (offset 등은 기본값으로 세팅)
                    real_link = f"{url}?mode=view&articleNo={article_no}&article.offset=0&articleLimit=10"
                else:
                    real_link = url # 추출 실패 시 목록 페이지로 연결

                post = {'category' : category,
                        'title' : title,
                        'date' : date,
                        'url': real_link
                        }
                posts.append(post)

            myDB.insert_posts_batch(posts)
            print(f"{category} was crawled successfully")

        except Exception as e:
            print(f"Error at {url}: {e}")

if __name__ == '__main__':
    crawl()