from playwright.sync_api import sync_playwright
import psycopg2 

class Create_Dataset(): # Creating class that hepls to collect data
    def __init__(self, link, topic, length_of_data):
        self.link = link
        self.topic = topic
        self.length_of_data = length_of_data
    def save_to_db(self):
        like_count, retweet_count, comments_count = self._get_data(self.link)
        self._insert_to_psql(self.link, self.topic, like_count, retweet_count, comments_count)
    
    def _insert_to_psql(self,link,topic,like_count, reposts_count, comments_count):
        
        conn = psycopg2.connect(host='localhost', port=5432, database="dataset", user='postgres', password='postgres')
        cur = conn.cursor()
        for n in range(self.length_of_data):
            cur.execute(""" INSERT INTO Xinfo (link,topic, likes, repostscount, commentcount) VALUES (%s,%s, %s, %s, %s)""",
                        (link,topic, like_count,reposts_count, comments_count))
        conn.commit()
        cur.close()
        conn.close()

    def _get_data(self,link):
            with sync_playwright() as p:
               browser = p.firefox.launch()
               page = browser.new_page()
               if link.startswith(('https://x.com/', 'http://x.com/')): 
                   page.goto(link)
                   page.wait_for_selector("[data-testid='like']")
                   page.wait_for_selector("[data-testid='reply']")
                   page.wait_for_selector("[data-testid='retweet']")
                   like_count = page.inner_text("[data-testid='like']")
                   reply_count = page.inner_text("[data-testid='reply']")
                   retweet_count = page.inner_text("[data-testid='retweet']")
                   return like_count, retweet_count, reply_count
               else:
                   raise ValueError("Wrong type of link")

dataset = Create_Dataset(
    link = "https://x.com/BBCSport/status/2019674930774958543",
    topic=1,
    length_of_data = 1
)
dataset.save_to_db()