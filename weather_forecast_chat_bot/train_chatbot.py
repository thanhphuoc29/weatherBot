from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import chatterbot.corpus
import sys
import requests
import datetime
import json
from PIL import Image
from io import BytesIO

chatbot = ChatBot(
    'WeatherBot', storge_adapter="chatterbot.storage.SQLStorageAdapter")

trainer = ChatterBotCorpusTrainer(chatbot)

trainer.train("chatterbot.corpus.Jarvis")

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
    api_key = "fe8d8c65cf345889139d8e545f57819a"
    call_url = ow_url + "appid=" + api_key + "&q=" + city + "&units=metric"
    response = requests.get(call_url)
    data = response.json()
    content = ""
    if data["cod"] != "404":
        city_res = data["main"]
        current_temperature = city_res["temp"]
        current_pressure = city_res["pressure"]
        current_humidity = city_res["humidity"]
        now = datetime.datetime.now()
        content = """
        Hôm nay là ngày {day} tháng {month} năm {year}
        Nhiệt độ trung bình là {temp} độ C
        Áp lực không khí là {pressure} Pascals
        Độ ẩm là {humidity}%
        The sky is clear today. Scattered rain forecast in some places""".format(day=now.day, month=now.month, year=now.year,
                                                                                 temp=current_temperature, pressure=current_pressure, humidity=current_humidity)
    else:
        content = "Không tìm thấy địa chỉ theo yêu cầu"
    print(content)


def weatherForcast():
    api_key = "fe8d8c65cf345889139d8e545f57819a"

# Địa điểm và thời gian để lấy thông tin dự báo thời tiết
    city = input('Nhập thành phố: ')
    # Lấy thông tin dự báo thời tiết của 5 ngày tiếp theo

    # URL của OpenWeatherMap API để lấy thông tin dự báo thời tiết
    url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric'

    # Gọi API và lấy dữ liệu JSON
    response = requests.get(url)
    data = json.loads(response.text)

    # In ra thông tin dự báo thời tiết
    forecast = []

    for item in data['list']:
        dt_txt = item['dt_txt']
        if dt_txt.endswith('12:00:00'):
            weather = {
                'date': dt_txt[:10],
                'temp': item['main']['temp'],
                'description': item['weather'][0]['description'],
                'icon': item['weather'][0]['icon']
            }
            forecast.append(weather)

            # Hiển thị thông tin thời tiết kèm hình ảnh
    for weather in forecast:
        date = weather['date']
        temp = weather['temp']
        desc = weather['description']
        icon_url = f'http://openweathermap.org/img/w/{weather["icon"]}.png'
        icon_response = requests.get(icon_url)
        icon = Image.open(BytesIO(icon_response.content))

        print(f'{date}: {temp}°C - {desc}')
        icon.show()


if __name__ == "__main__":
    while True:
        request = input('Yêu cầu: ')
        if request == 'q':
            sys.exit(0)
        elif 'thời tiết' in request:
            weatherToday()
        elif 'dự báo' in request:
            weatherForcast()
        else:
            print('WeatherBot: ', getResponse(request))
