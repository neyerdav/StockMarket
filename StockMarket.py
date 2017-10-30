from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import MySQLdb
import datetime
from time import sleep

OPENING = datetime.datetime.strptime("9:30", "%H:%M").strftime("%H:%M")
CLOSING = datetime.datetime.strptime("16:00","%H:%M").strftime("%H:%M")
conn = MySQLdb.connect(host= "localhost",
                  user="user",
                  passwd="root")
x = conn.cursor()
sql = """CREATE DATABASE IF NOT EXISTS StockMarket"""
x.execute(sql)
sql = """USE StockMarket"""
x.execute(sql)
sql = """CREATE TABLE IF NOT EXISTS StockMarket(company VARCHAR(255), value float, date VARCHAR(255), time VARCHAR(255))"""
x.execute(sql)

weekday = datetime.datetime.today().weekday()
if weekday is 5 or weekday is 6:
    print("Weekend")
    sleep(60)
else:
    date = datetime.datetime.now().strftime("%B %d, %Y")
    time = datetime.datetime.now()
    t = time.strftime("%-I:%-M %p")
    time = time.strftime("%H:%M")
    print(time)
    print(OPENING)
    print(CLOSING)
    if time > OPENING and time < CLOSING:
        print("passed")
        request = Request('https://www.investing.com/equities/StocksFilter?noconstruct=1&smlID=0&sid=&tabletype=price&index_id=166')
        request.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')
        request.add_header('Accept', '*/*')
        request.add_header('Accept-Language', 'en-US,en;q=0.5')
        request.add_header('Referer', 'https://www.investing.com/equities/')
        request.add_header('X-Requested-With', 'XMLHttpRequest')
        request.add_header('Connection', 'close')
        try:
            html = urlopen(request).read().decode('utf-8')
            soup = BeautifulSoup(html, 'lxml')
            tbody = soup.find("tbody")
            print(tbody)
            for tr in tbody.find_all('tr'):
                name = tr.contents[1].text
                value = tr.contents[2].text
                try:
                    x.execute("""INSERT INTO StockMarket VALUES (%s,%s, %s, %s)""",(name, value, date, t))
                    conn.commit()
                    print(name)
                    print("Commit")

                except Exception as e:
                    print(e)
                    conn.rollback()
            sleep(60)
        except Exception as e:
            print(e)
            sleep(60)
    else:
        print("Out of time")
        sleep(60)
