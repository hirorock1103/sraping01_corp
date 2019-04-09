from selenium import webdriver    # さっきpip install seleniumで入れたseleniumのwebdriverというやつを使う
import time
import sqlite3

# 投稿LISTに対してuser名とハッシュタグをセットしていく
mode = ""

# connect database
con = sqlite3.connect('sample.db')
cursor = con.cursor()
query = "CREATE TABLE IF NOT EXISTS SampleGetPostList(" \
        "id integer primary key AUTOINCREMENT, " \
        "url text, " \
        "word text, " \
        "post_date text, " \
        "h_tags text, " \
        "post_user_id text)"
cursor.execute(query)

TOP_URL = "https://www.instagram.com"
fPath = r"C:\Users\USER\Desktop\data"

# targetList = list()
# # get data from file or database
# f = open(fPath + '/new_スタイル抜群_2019-04-05.txt', 'r')
# line = f.readline()
# while line:
#     line = f.readline()
#     # targetList.append(line)
# f.close()

driver = webdriver.Chrome(r"C:\Users\USER\Desktop\chromedriver_win32 (2)/chromedriver.exe") # さっきDLしたchromedriver.exeを使う
driver.set_page_load_timeout(600)   # ページロード最大600秒
# driver.get(TOP_URL)    # chrome起動→ログインページに移動
# time.sleep(2)

# start from database
cursor.execute('SELECT * FROM SampleGetPostList ORDER BY id ASC')
postNumberOfResult = 0
for row in cursor:

    dataId = (row[0])
    url = (row[1])
    title = (row[2])
    dataUserId = (row[4])

    print(dataUserId)
    if dataUserId is not None:
        print("userId is already set")
        continue

    print("\n\n -search start- " + url)
    driver.get(url)

    try:
        errormsg = driver.find_element_by_xpath("/html/body/div/div[1]/div/div/h2")
        print(errormsg.text)
        if errormsg.text == "このページはご利用いただけません。":
            print("ページが存在しないためcontinue")
            time.sleep(1)
            continue
    except:
        print("通常")

    time.sleep(2)
    if mode != "VIEW":

        # User を取得
        userTag = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/article/header/div[2]/div[1]/div[1]/h2/a')
        print(userTag.text)
        # ハッシュタグを取得
        hashTags = []
        elmDiv = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/article/div[2]')
        elmSpan = elmDiv.find_elements_by_tag_name("span")
        aTags = elmDiv.find_elements_by_tag_name("a")
        timeTags = elmDiv.find_element_by_tag_name("time")

        for link in aTags:
            if "#" in link.text:
                hashTags.append(link.text)

        if hashTags.__len__() > 0:
            # update record
            tags = ",".join(hashTags)
            dataId = dataId
            user = userTag.text
            print(tags)
            print(dataId)
            print(user)
            cursor2 = con.cursor()
            query = "update SampleGetPostList SET h_tags = ?, post_user_id = ?, post_date = ? WHERE id = ?"
            args = (tags, userTag.text, timeTags.text, dataId)
            cursor2.execute(query, args)
con.commit()