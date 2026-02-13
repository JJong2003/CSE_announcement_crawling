import MySQLdb
from config import db_config



def insert_posts_batch(posts: list):
    with MySQLdb.connect(**db_config) as conn:
        cursor = conn.cursor()
        
        for post in posts:
            category, title, date = post['category'], post['title'], post['date']
            
            check_sql = "SELECT COUNT(*) FROM post WHERE category = %s AND title = %s"
            cursor.execute(check_sql, (category, title))
            (count,) = cursor.fetchone()
            
            if count == 0:
                logging_new_post(post)
                
                insert_sql = "INSERT INTO post (title, posting_date, category) VALUES (%s, %s, %s)"
                cursor.execute(insert_sql, (title, date, category))
        
        conn.commit()

def logging_new_post(post: dict):
    with open("새로 올라온 공지글.txt", "a", encoding='utf-8') as file:
        file.write(f"[{post['category']}] {post['date']} {post['title']}\n")