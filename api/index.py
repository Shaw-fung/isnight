from flask import Flask, render_template
from bs4 import BeautifulSoup
from datetime import datetime
from fake_useragent import UserAgent
import urllib3
import requests
import pytz

app = Flask(__name__)

user_agent = UserAgent().random
headers = {
    "User-Agent": user_agent
}

def get_html(url):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    # 指定要访问的网址
    url = "{}".format(url)
    # 发起 HTTP GET 请求并获取响应内容
    response = requests.get(url, headers = headers, verify=False)
    return(response.text)

@app.route('/')
def index():
    html_code = get_html('https://richuriluo.xuenb.com/1959.html')
    soup = BeautifulSoup(html_code, 'html.parser')
    table = soup.find('table')
    rows = table.find_all('tr')

    # 获取当前日期和时间
    tz = pytz.timezone('Asia/Shanghai')
    current_date = datetime.now(tz).strftime('%Y-%m-%d')
    current_time = datetime.now(tz).strftime('%H:%M')

    # 查找当天日期所在的行
    for row in rows:
        columns = row.find_all('td')
        if current_date in columns[0].text:
            sunrise = columns[4].text
            sunset = columns[5].text

            # 判断当前时刻是否在天亮时间和天黑时间之间
            if current_time < sunrise or current_time > sunset:
                result = True
            else:
                result = False
            return render_template('index.html', sunrise=sunrise, sunset=sunset, result=result, current_date=current_date, current_time=current_time)

    return render_template('index.html', sunrise="", sunset="", result="日期未找到", current_date=current_date, current_time=current_time)

@app.route('/isnight')
def isnight():
    html_code = get_html('https://richuriluo.xuenb.com/1959.html')
    soup = BeautifulSoup(html_code, 'html.parser')
    table = soup.find('table')
    rows = table.find_all('tr')

    # 获取当前日期和时间
    tz = pytz.timezone('Asia/Shanghai')
    current_date = datetime.now(tz).strftime('%Y-%m-%d')
    current_time = datetime.now(tz).strftime('%H:%M')

    # 查找当天日期所在的行
    for row in rows:
        columns = row.find_all('td')
        if current_date in columns[0].text:
            sunrise = columns[5].text
            sunset = columns[6].text

            # 判断当前时刻是否在天亮时间和天黑时间之间
            if current_time < sunrise or current_time > sunset:
                result = True
            else:
                result = False
            return render_template('isnight.html', result=result)

    return render_template('isnight.html', result="日期未找到")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
