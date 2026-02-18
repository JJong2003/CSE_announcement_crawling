import streamlit as st
import pandas as pd
import sys
import os
from datetime import datetime
from sqlalchemy import create_engine

# ---------------------------------------------------------
# 전역변수
# ---------------------------------------------------------
search_bound = 7

# ---------------------------------------------------------
# 경로 설정: functions 폴더를 파이썬이 인식하도록 추가
# ---------------------------------------------------------
current_dir = os.path.dirname(os.path.abspath(__file__))
functions_dir = os.path.join(current_dir, 'functions') 
sys.path.append(functions_dir)

# config.py 불러오기
try:
    import config
    # config 모듈 안의 db_config 변수를 가져옵니다.
    db_settings = getattr(config, 'db_config', None)
except ImportError:
    st.error(f"⚠️ 설정 파일을 찾을 수 없습니다. 경로를 확인해주세요: {functions_dir}")
    st.stop()

# ---------------------------------------------------------
# DB 연결 및 데이터 조회 함수
# ---------------------------------------------------------
def get_recent_posts(days=7):
    try:
        if db_settings is None:
            st.error("config.py 파일 안에 'db_config' 변수가 없습니다.")
            return pd.DataFrame()

        user = db_settings['user']
        passwd = db_settings['passwd']
        host = db_settings['host']
        db = db_settings['db']
        
        # 연결 문자열 생성
        engine_url = f"mysql+mysqldb://{user}:{passwd}@{host}/{db}?charset=utf8mb4"
        engine = create_engine(engine_url)
        
        query = f"""
        SELECT category, title, posting_date, url
        FROM post
        WHERE DATEDIFF(CURDATE(), posting_date) <= {days}
        ORDER BY posting_date DESC, id DESC;
        """
        df = pd.read_sql(query, engine)
        return df
        
    except Exception as e:
        st.error(f"DB 연결 오류: {e}")
        return pd.DataFrame()

# ---------------------------------------------------------
# Streamlit 화면 구성 (UI)
# ---------------------------------------------------------
st.set_page_config(page_title="충남대 컴퓨터공학 공지", layout="wide")

st.title("📢 충남대 컴퓨터융합학부 최신 공지")
st.caption(f"최근 {search_bound}일 이내에 올라온 공지사항만 모아봅니다. (기준: {datetime.now().strftime('%Y-%m-%d %H:%M')})")

if st.button("🔄 데이터 새로고침"):
    print("새로고침")
    from functions.crawling import crawl
    crawl()
    st.rerun()

df = get_recent_posts(search_bound)

option = st.number_input('탐색 범위를 설정하세요. 기본값은 7 입니다.', 1, 31)
if option != search_bound:
    df = get_recent_posts(option)
    search_bound = option

if df.empty:
    st.info(f"최근 {search_bound}일간 올라온 공지사항이 없거나, DB 연결에 실패했습니다. 😎")
else:
    st.info(f"최근 {search_bound}일간 올라온 {len(df)}개의 공지사항을 확인하세요. 😉")
    df.index = df.index + 1
    
    st.dataframe(
        df,
        column_config={
            "category": st.column_config.TextColumn("카테고리", width="small"),
            "title": st.column_config.TextColumn("제목", width="large"),
            "posting_date": st.column_config.DatetimeColumn("작성일", format="YYYY-MM-DD"),
            "url": st.column_config.LinkColumn(
                "바로가기",
                help="클릭하면 해당 공지사항으로 이동합니다.",
                validate="^https://.*",
                display_text="링크 이동 🔗"
            ),
        },
        hide_index=False,
        use_container_width=True
    )