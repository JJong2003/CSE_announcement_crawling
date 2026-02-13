# 공지사항 통합 대시보드

학과 홈페이지의 공지사항을 자동으로 수집하고, 최근 소식을 한눈에 볼 수 있는 웹 대시보드(Streamlit)를 제공합니다.

## 주요 기능
* **크롤링**: 학사공지, 일반소식, 취업/교외활동, 사업단소식 등 4개 카테고리의 게시글을 수집합니다.
* **DB 저장 및 중복 방지**: MySQL(8.0+) 데이터베이스에 데이터를 저장하며, 이미 존재하는 글은 중복해서 저장하지 않습니다.
* **웹 대시보드**: Streamlit을 활용해 최근 7일간 올라온 공지사항을 깔끔한 UI로 시각화합니다.

## 사용한 언어 및 자원
* **Language**: Python 3.10+
* **Web Framework**: Streamlit
* **Libraries**:
  * `BeautifulSoup4`: 웹 크롤링
  * `SQLAlchemy` & `MySQLdb`: 데이터베이스 연동
  * `Pandas`: 데이터 처리 및 가공

## 프로젝트 구조
```bash
Python Projects/
└── announcement_crawl/     # 크롤링 및 DB 로직 폴더
    ├── .venv/              # Python 가상환경
    ├── app.py              # Streamlit 웹 애플리케이션 메인 파일
    ├── requirements.txt    # 의존성 패키지 목록
    ├── functions/          # 기능 모듈 폴더
    │   ├── config.py       # DB 설정 파일 (git 제외)
    │   ├── crawling.py     # 크롤링 실행 스크립트
    │   └── myDB.py         # DB 연결 및 쿼리 처리 모듈
