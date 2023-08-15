import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.jungle

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://movie.daum.net/ranking/boxoffice/yearly?date=2021', headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')

movies = list(soup.select(".list_movieranking > li"))
db.movies.drop();

for movie in movies:
    title = movie.select_one(".thumb_cont .link_txt").text
    detail_url = "https://movie.daum.net" +movie.select_one(".thumb_cont .link_txt")["href"]
    if movie.select_one("img"):
        poster_url = movie.select_one("img")["src"]
    else:
        poster_url = ""
    open_info = movie.select_one(".info_txt").findChild(string=False, recursive=False).text
    open_year, open_month, open_day = open_info.split(".")
    views_text = movie.select_one(".info_txt:nth-child(2)").findChild(string=True,recursive=False)
    views_num = int(views_text.replace(",","").replace("명",""))
    
    movie_data = {
        "title" : title,
        "detail_url" : detail_url,
        "poster_url" : poster_url,
        "open_year" : int(open_year)+2000,
        "open_month" : int(open_month),
        "open_day" : int(open_day),
        "views_text" : views_text,
        "views_num" : int(views_num),
        "likes" : 0,
        "deleted" : False,
    }
    db.movies.insert_one(movie_data)

print("✨ Scrapping is done")


#<li>
#     <div class="item_poster">
#         <div class="thumb_item">
#             <div class="poster_movie">
#                     <img src="https://img1.daumcdn.net/thumb/C408x596/?fname=https%3A%2F%2Ft1.daumcdn.net%2Fmovie%2Febd9587dcdcc56548b5a476bf109f87d5a6098a5" class="img_thumb" alt="스파이더맨: 노 웨이 홈">
#                 <span class="rank_num">1</span>
#                     <span class="txt_tag">
#                         <span class="ico_movie ico_see see12">12세이상관람가</span>
#                     </span>
#             </div>
#             <div class="poster_info">
#                 <a href="/moviedb/main?movieId=146656" class="link_story">
#                     ‘미스테리오’의계략으로세상에정체가탄로난스파이더맨‘피터파커’는하루아침에평범한일상을잃게된다.문제를해결하기위해‘닥터스트레인지’를찾아가도움을청하지만뜻하지않게멀티버스가열리면서각기다른차원의불청객들이나타난다.‘닥터옥토퍼스’를비롯해스파이더맨에게깊은원한을가진숙적들의강력한공격에‘피터파커’는사상최악의위기를맞게되는데…
#                 </a>
#             </div>
#         </div>
#         <div class="thumb_cont">
#             <strong class="tit_item"><a href="/moviedb/main?movieId=146656" class="link_txt">스파이더맨: 노 웨이 홈</a></strong>
#             <span class="txt_info">
#                     <span class="info_txt">개봉<span class="txt_num">21.12.15</span></span>
#                     <span class="info_txt"><span class="screen_out">관객수</span>7,551,990명</span>
#             </span>
#         </div>
#     </div>
# </li>