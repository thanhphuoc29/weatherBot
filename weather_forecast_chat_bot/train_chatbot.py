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

chatbot = ChatBot(
    'WeatherBot', storge_adapter="chatterbot.storage.SQLStorageAdapter")

trainer = ChatterBotCorpusTrainer(chatbot)

trainer.train("chatterbot.corpus.Jarvis")
api_key = "fe8d8c65cf345889139d8e545f57819a"

# print(chatterbot.corpus.__file__)


def getResponse(rq):
    res = chatbot.get_response(rq)
    return str(res)


def weatherToday():
    ow_url = "http://api.openweathermap.org/data/2.5/weather?"
    print('Nhập địa điểm:...')
    city = input()
    if not city:
        pass
    call_url = ow_url + "appid=" + api_key + "&q=" + city + "&units=metric"
    response = requests.get(call_url)
    data = response.json()
    # print(data)
    data = json.loads(response.text)
    content = ""
    if data["cod"] != "404":
        city_res = data["main"]
        c_temperature = data['main']['temp']  # nhiệt độ
        c_humidity = data['main']['humidity']  # độ ẩm
        c_wind_speed = data['wind']['speed']  # tốc độ gió
        c_wind_direction = data['wind']['deg']  # hướng gió
        c_feels_like = data['main']['feels_like']  # nhiệt độ cảm nhận
        c_pressure = data['main']['pressure']  # áp suất khí quyển
        c_clouds = data['clouds']['all']  # mức độ mây
        c_sunrise = data['sys']['sunrise']  # mặt trời mọc
        c_sunset = data['sys']['sunset']  # mặt trời lặn
        now = datetime.now()
        content = """
        Hôm nay là ngày {day} tháng {month} năm {year}
        Nhiệt độ trung bình là {temp} độ C
        Độ ẩm là {humidity}%
        Tốc độ gió là {wind_speed}m/s
        Hướng gió là {wind_direction}°
        Nhiêt độ cảm nhận là {feels_like} độ C  
        Áp suất khí quyển là {pressure} Pascals
        Mức độ mây là {clouds}%
        """.format(day=now.day, month=now.month, year=now.year,
                   temp=c_temperature, pressure=c_pressure, humidity=c_humidity,
                   wind_speed=c_wind_speed, wind_direction=c_wind_direction, feels_like=c_feels_like,
                   clouds=c_clouds)
    else:
        content = "Không tìm thấy địa chỉ theo yêu cầu"
    print(content)
# def weatherToday():
#     ow_url = "http://api.openweathermap.org/data/2.5/weather?"
#     print('Nhập địa điểm:...')
#     city = input()
#     if not city:
#         pass
#     call_url = ow_url + "appid=" + api_key + "&q=" + city + "&units=metric"
#     response = requests.get(call_url)
#     data = response.json()
#     content = ""
#     if data["cod"] != "404":
#         city_res = data["main"]
#         current_temperature = city_res["temp"]
#         current_pressure = city_res["pressure"]
#         current_humidity = city_res["humidity"]
#         now = datetime.now()
#         content = """
#         Hôm nay là ngày {day} tháng {month} năm {year}
#         Nhiệt độ trung bình là {temp} độ C
#         Áp lực không khí là {pressure} Pascals
#         Độ ẩm là {humidity}%
#         The sky is clear today. Scattered rain forecast in some places""".format(day=now.day, month=now.month, year=now.year,
#                                                                                  temp=current_temperature, pressure=current_pressure, humidity=current_humidity)
#     else:
#         content = "Không tìm thấy địa chỉ theo yêu cầu"
#     print(content)


def PastWeather():
    location = input('Nhập tên thành phố: ')
    num = input('Bạn muốn xem thời tiết cách đây mấy ngày ạ ^^!: ')
    today = datetime.now()
    past_date = today - timedelta(days=int(num))
    timestamp = int(past_date.timestamp())
    url = f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric&dt={timestamp}'
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        api_data = response.json()
        weather = api_data["weather"][0]["description"]
        temp = api_data["main"]["temp"]
        pressure = api_data["main"]["pressure"]
        humidity = api_data["main"]["humidity"]
        print(f"Thời tiết ngày {past_date.strftime('%d-%m-%Y')} tại {location}:\nNhiệt độ trung bình là {temp}°C\nÁp suất không khí là {pressure} hPa\nĐộ ẩm là {humidity}%.")
    else:
        print("Không tìm thấy địa chỉ theo yêu cầu")


def weatherFocast():
    location = input("Nhập tên thành phố: ")
    while True:
        num = input("Nhập số ngày dự đoán: ")
        if num.isdigit():
            num_days = int(num)
            if num_days < 0 or num_days > 5:
                print(
                    'Xin lỗi số ngày quá lớn em không dự đoán được, hãy thử nhập lại số ngày nhỏ hơn 6 giúp em nha')
            else:
                break
        else:
            print(
                'Ui số ngày nhập phải bằng số em mới hiểu được ạ, vui lòng nhập lại giúp em')

    complete_api_link = "https://api.openweathermap.org/data/2.5/forecast?q=" + \
        location+"&appid="+api_key
    api_link = requests.get(complete_api_link)
    api_data = api_link.json()
    if api_data['cod'] == '404':
        print('Không tìm thấy địa điểm: {}, hãy kiểm tra lại.'.format(location))
    else:
        print("Dự báo thời tiếp tại {} trong {} ngày tới:".format(location, num_days))
        print("---------------------------------------------------------------------")
        date_format = "%Y-%m-%d %H:%M:%S"
        today = datetime.now()
        for i in range(1, num_days+1):
            forecast_date = today + timedelta(days=i)
            forecast_date_str = forecast_date.strftime('%d-%m-%Y')
            for j in range(len(api_data['list'])):
                date_time_str = api_data['list'][j]['dt_txt']
                date_time = datetime.strptime(date_time_str, date_format)
                if date_time.strftime('%d-%m-%Y') == forecast_date_str:
                    print("Ngày: ", forecast_date_str)
                    print("Nhiệt độ trung bình {:.2f}°C".format(
                        api_data['list'][j]['main']['temp'] - 273.15))
                    print("Áp lực không khí là {} Pascals\nĐộ ẩm là {}%".format(
                        api_data['list'][j]['main']['pressure'], api_data['list'][j]['main']['humidity']))
                    print("Thời tiết: ", api_data['list']
                          [j]['weather'][0]['description'])
                    print(
                        "---------------------------------------------------------------------")
                    time.sleep(1)
                    break


today = ['thời tiết', 'aaaa', 'aaa']


if __name__ == "__main__":
    while True:
        request = input('Yêu cầu: ')
        if request == 'q':
            sys.exit(0)
        elif 'thời tiết' in request or 'hôm nay' in request:
            weatherToday()
        elif 'dự báo' in request or 'ngày mai' in request:
            weatherFocast()
        elif 'quá khứ' in request:
            PastWeather()
        else:
            print('WeatherBot: ', getResponse(request))
