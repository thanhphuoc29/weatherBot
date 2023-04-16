from flask import Flask, render_template, request
from flask_cors import CORS
import json
from flask import jsonify
# chat
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import chatterbot.corpus
import sys
import requests
import json
from PIL import Image
from io import BytesIO
from datetime import datetime, timedelta
import time

app = Flask(__name__)
CORS(app)

chatbot = ChatBot(
    'WeatherBot', storage_adapter='chatterbot.storage.SQLStorageAdapter')

trainer = ChatterBotCorpusTrainer(chatbot)

trainer.train("chatterbot.corpus.Jarvis")
api_key = "fe8d8c65cf345889139d8e545f57819a"
location = "none"


def getResponse(rq):
    res = chatbot.get_response(rq)
    return str(res)


def weatherToday(location):
    # global location
    # if location == "none":
    #     location = input('Bạn muốn xem thời tiết ở đâu ạ: ')
    ow_url = "http://api.openweathermap.org/data/2.5/weather?"
    if not location:
        pass
    call_url = ow_url + "appid=" + api_key + "&q=" + location + "&units=metric"
    response = requests.get(call_url)
    data = response.json()
    # print(data)
    data = json.loads(response.text)
    content = "Thời tiết ngày hôm nay tại "+location + \
        "<br>-----------------------------<br>"
    if data["cod"] != "404":
        city_res = data["main"]
        c_temperature = data['main']['temp']  # nhiệt độ
        c_humidity = data['main']['humidity']  # độ ẩm
        c_wind_speed = data['wind']['speed']  # tốc độ gió
        c_wind_direction = data['wind']['deg']  # hướng gió
        c_feels_like = data['main']['feels_like']  # nhiệt độ cảm nhận
        c_pressure = data['main']['pressure']  # áp suất khí quyển
        c_clouds = data['clouds']['all']  # mức độ mây
        now = datetime.now()
        content += """
        Hôm nay là ngày {day} tháng {month} năm {year}<br>
        Nhiệt độ trung bình là {temp} độ C<br>
        Độ ẩm là {humidity}%<br>
        Tốc độ gió là {wind_speed}m/s<br>
        Hướng gió là {wind_direction}°<br>
        Nhiêt độ cảm nhận là {feels_like} độ C<br>
        Áp suất khí quyển là {pressure} Pascals<br>
        Mức độ mây là {clouds}%<br>
        """.format(day=now.day, month=now.month, year=now.year,
                   temp=c_temperature, pressure=c_pressure, humidity=c_humidity,
                   wind_speed=c_wind_speed, wind_direction=c_wind_direction, feels_like=c_feels_like,
                   clouds=c_clouds)
    else:
        content = "Không tìm thấy địa chỉ theo yêu cầu"
    return content


def PastWeather(location, num):
    # global location
    # if location == "none":
    #     location = input('Bạn muốn xem thời tiết ở đâu ạ: ')
    # num = input('Bạn muốn xem thời tiết cách đây mấy ngày ạ ^^!: ')
    today = datetime.now()
    past_date = today - timedelta(days=int(num))
    timestamp = int(past_date.timestamp())
    url = f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric&dt={timestamp}'
    response = requests.get(url)
    data = response.json()
    content = 'Thời tiết tại '+location + \
        '<br>-------------------------------------<br>'
    if response.status_code == 200:
        api_data = response.json()
        weather = api_data["weather"][0]["description"]
        temp = api_data["main"]["temp"]
        pressure = api_data["main"]["pressure"]
        humidity = api_data["main"]["humidity"]
        content += f"Thời tiết ngày {past_date.strftime('%d-%m-%Y')} tại {location}:<br>Nhiệt độ trung bình là {temp}°C<br>Áp suất không khí là {pressure} hPa<br>Độ ẩm là {humidity}%."
    else:
        content = "Không tìm thấy địa chỉ theo yêu cầu"
    return content


def weatherFocast(location, num_days):
    # global location
    # if location == "none":
    #     location = input('Bạn muốn xem thời tiết ở đâu ạ: ')
    # while True:
    #     num = input("Nhập số ngày dự đoán: ")
    #     if num.isdigit():
    #         num_days = int(num)
    #         if num_days < 0 or num_days > 5:
    #             print(
    #                 'Xin lỗi số ngày quá lớn em không dự đoán được, hãy thử nhập lại số ngày nhỏ hơn 6 giúp em nha')
    #         else:
    #             break
    #     else:
    #         print(
    #             'Ui số ngày nhập phải bằng số em mới hiểu được ạ, vui lòng nhập lại giúp em')

    complete_api_link = "https://api.openweathermap.org/data/2.5/forecast?q=" + \
        location+"&appid="+api_key
    api_link = requests.get(complete_api_link)
    api_data = api_link.json()
    content = ''
    if api_data['cod'] == '404':
        print('Không tìm thấy địa điểm: {}, hãy kiểm tra lại.'.format(location))
    else:
        content += "Dự báo thời tiếp tại {} trong {} ngày tới:".format(
            location, num_days)
        content += "<br>---------------------------------------------------------------------<br>"
        date_format = "%Y-%m-%d %H:%M:%S"
        today = datetime.now()
        for i in range(1, num_days+1):
            forecast_date = today + timedelta(days=i)
            forecast_date_str = forecast_date.strftime('%d-%m-%Y')
            for j in range(len(api_data['list'])):
                date_time_str = api_data['list'][j]['dt_txt']
                date_time = datetime.strptime(date_time_str, date_format)
                if date_time.strftime('%d-%m-%Y') == forecast_date_str:
                    content += "Ngày :{}\nNhiệt độ trung bình {:.2f}°C<br>Áp lực không khí là {} Pascals<br>Độ ẩm là {}%<br>Thời tiết: {}<br>---------------------------------------------------------------------<br>".format(
                        forecast_date_str, api_data['list'][j]['main']['temp'] - 273.15,
                        api_data['list'][j]['main']['pressure'], api_data['list'][j]['main']['humidity'],
                        api_data['list'][j]['weather'][0]['description']
                    )
                    break
    return content


@app.route("/")
def home():
    return render_template("index.html")


TYPE_SET_LOCATION = 0
TYPE_SET_FOCAST = 0
TYPE_SET_PAST = 0
TYPE_SET_TODAY = 0


@app.route('/respone', methods=['POST'])
def sendRespone():
    global TYPE_SET_TODAY
    global TYPE_SET_FOCAST
    global TYPE_SET_PAST
    global TYPE_SET_LOCATION
    global location
    day_future = 0
    day_past = 0
    data = request.get_json()
    text = data['text'].lower()
    respone = ''
    print('địa điểm: ' + location)
    # --------------------Xem thời tiết hôm nay------------------------------
    if ('thời tiết' in text or 'hôm nay' in text) or TYPE_SET_TODAY == 1:
        if TYPE_SET_TODAY == 1:
            location = text
            respone = weatherToday(location)
            TYPE_SET_TODAY = 0
        elif location == 'none':
            respone = 'Bạn muốn xem thời tiết ở đâu ạ ^^! (nhập mỗi tên địa điểm giúp iem)'
            TYPE_SET_TODAY = 1
        elif location != 'none':
            respone = weatherToday(location)
    # --------------------Xem thời tiết tương lai------------------------------
    elif ('ngày mai' in text or 'tương lai' in text) or TYPE_SET_FOCAST == 1 or TYPE_SET_FOCAST == 2:
        if TYPE_SET_FOCAST == 1:
            if location == 'none':
                location = text
            respone = 'Bạn muốn dự báo thời tiết trong mấy ngày tới ạ ^^ (nhập số ngày giúp iem)'
            TYPE_SET_FOCAST = 2
        elif TYPE_SET_FOCAST == 2:
            if text.isdigit():
                day_future = int(text)
                if day_future < 0 or day_future > 5:
                    respone = 'Số ngày quá lớn em không đoán được, nhập lại nhỏ nhỏ giúp em >.<'
                    TYPE_SET_FOCAST = 1
                else:
                    respone = weatherFocast(location, day_future)
                    TYPE_SET_FOCAST = 0
        elif location == 'none':
            respone = 'Bạn muốn xem thời tiết ở đâu ạ ^^! (nhập mỗi tên địa điểm giúp iem)'
            TYPE_SET_FOCAST = 1
        elif location != 'none' and day_future == 0:
            respone = 'Bạn muốn dự báo thời tiết trong mấy ngày tới ạ ^^ (nhập số ngày giúp iem)'
            TYPE_SET_FOCAST = 2
        elif location != 'none' and day_future != 0:
            respone = weatherFocast(location, day_future)
    # --------------------Xem thời tiết quá khứ------------------------------
    elif ('hôm qua' in text or 'quá khứ' in text) or TYPE_SET_PAST == 1 or TYPE_SET_PAST == 2:
        if TYPE_SET_PAST == 1:
            if location == 'none':
                location = text
            respone = 'Bạn muốn xem lại thời tiết cách đây mấy ngày ạ ^^ (nhập số ngày giúp iem)'
            TYPE_SET_PAST = 2
        elif TYPE_SET_PAST == 2:
            if text.isdigit():
                day_past = int(text)
                if day_past < 0 or day_past > 10:
                    respone = 'Số ngày quá lớn em không xem được, nhập lại nhỏ nhỏ giúp em >.<'
                    TYPE_SET_PAST = 1
                else:
                    respone = PastWeather(location, day_future)
                    TYPE_SET_PAST = 0
        elif location == 'none':
            respone = 'Bạn muốn xem thời tiết ở đâu ạ ^^! (nhập mỗi tên địa điểm giúp iem)'
            TYPE_SET_PAST = 1
        elif location != 'none' and day_past == 0:
            respone = 'Bạn muốn xem lại thời tiết cách đây mấy ngày ạ ^^ (nhập số ngày giúp iem)'
            TYPE_SET_PAST = 2
    # --------------------Thay đổi địa điểm xem thời tiết-------------------------------
    elif 'nơi khác' in text:
        respone = 'Bạn muốn xem thời tiết ở đâu ạ ^^!'
    # --------------------Trả lời theo trainning-------------------------------
    else:
        respone = getResponse(text)
    return jsonify({'respone': respone})


if __name__ == "__main__":
    app.run()
