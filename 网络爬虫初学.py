import csv
from lxml import html
import requests
import os
import re
#设置网站常量
URL_MAIN_PAGE = "https://www.themoviedb.org/"
URL_TOP_PAGE_1 = "https://www.themoviedb.org/movie/top-rated"
URL_TOP_PAGE_2 = "https://www.themoviedb.org/discover/movie/items"

if not os.path.exists("./movie.data"):
    os.makedirs("./movie.data")
def get_movie_data(movie_https):
        movie_data = html.fromstring(requests.get(movie_https).text)
        movie_title = movie_data.xpath("//section[@class = 'header poster']//h2/a/text()")
        movie_release_time = movie_data.xpath("//section[@class = 'header poster']//span[@class = 'release']/text()")
        movie_release_topics = ", ".join(movie_data.xpath(".//section[@class = 'header poster']//span[@class='genres']/a/text()"))
        movie_release_runtime = movie_data.xpath("//section[@class = 'header poster']//span[@class = 'runtime']/text()")
        result = re.findall(r'(\d+)h (\d+)m',movie_release_runtime[0].strip()  if movie_release_runtime else "未知")
        if result:
            runtime = int(result[0][0]) * 60 + int(result[0][1])
        else:
            runtime = "未知"
        movie_rating = movie_data.xpath("//section[@class = 'header poster']//div[@data-percent]/@data-percent")
        movie_director = movie_data.xpath("//section[@class = 'header poster']//a[contains(@href,'/person/')]/text()")
        movie_content_profile= movie_data.xpath("//section[@class = 'header poster']//div[@class = 'overview']/p/text()")
        movie_info={'电影名字':movie_title[0].strip() if movie_title else "未知",
                    '电影上映时间':re.findall(r'\d{4}-\d{2}-\d{2}',movie_release_time[0].strip() if movie_release_time else "未知")[0] if re.findall(r'\d{4}-\d{2}-\d{2}',movie_release_time[0].strip() if movie_release_time else "未知") else "未知",
                    '电影主题':movie_release_topics.strip() if movie_release_topics else "未知",
                    '电影时长':str(runtime) +  "m" if runtime != "未知" else "未知",
                    '电影评分':movie_rating[0].strip() + "%" if movie_rating else "未知",
                    '电影导演':movie_director[0].strip() if movie_director else "未知",
                    '电影内容简介':movie_content_profile[0].strip() if movie_content_profile else "未知"
                    }
        return movie_info
def get():
    # 发送请求获得网站页面代码
    info_list = []
    for page_num in range(1,6):
        if page_num ==1:
            response = requests.get(URL_TOP_PAGE_1,timeout=60)
        if page_num > 1:
            response = requests.post(URL_TOP_PAGE_2,data=f"air_date.gte=&air_date.lte=&certification=&certification_country=KR&debug=&first_air_date.gte=&first_air_date.lte=&include_adult=false&include_softcore=false&latest_ceremony.gte=&latest_ceremony.lte=&page={page_num}&primary_release_date.gte=&primary_release_date.lte=&region=&release_date.gte=&release_date.lte=2027-03-08&show_me=everything&sort_by=vote_average.desc&vote_average.gte=0&vote_average.lte=10&vote_count.gte=300&watch_region=KR&with_genres=&with_keywords=&with_networks=&with_origin_country=&with_original_language=&with_watch_monetization_types=&with_watch_providers=&with_release_type=&with_runtime.gte=0&with_runtime.lte=400",timeout=60)
        document = html.fromstring(response.text)
        # 获得网站数据列表
        movie_list = document.xpath(f"//div[@id='page_{page_num}']//div[contains(@class,'rounded-xl') and contains (@class,'border')]")
        if movie_list:
            for movie in movie_list:
                movie.https = movie.xpath("./div/div/a/@href")
                movie_URL = URL_MAIN_PAGE + movie.https[0]
                print(f"正在爬取第{page_num}页的{movie_URL}")
                info_list.append(get_movie_data(movie_URL))
    return info_list
def data_save():
    info_list = get()
    with open("./movie.data/movie.csv","w",newline='',encoding='utf-8') as f:
        writer = csv.DictWriter(f,fieldnames=['电影名字','电影上映时间','电影主题','电影时长','电影评分','电影导演','电影内容简介'])
        writer.writeheader()
        for info in info_list:
            writer.writerow(info)
    f.close()
data_save()




