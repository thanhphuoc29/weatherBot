from flask import Flask, render_template, request, session
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
import random
from datetime import datetime, timedelta
import time
from flask_session import Session


app = Flask(__name__)
CORS(app)

chatbot = ChatBot(
    'WeatherBot', storage_adapter='chatterbot.storage.SQLStorageAdapter')

trainer = ChatterBotCorpusTrainer(chatbot)

trainer.train("chatterbot.corpus.weatherbot")
api_key = "fe8d8c65cf345889139d8e545f57819a"
location = "none"

dict_place = {}
list_survive = []

list_province = ['Hòa Bình', 'Sơn La', 'Điện Biên', 'Lai Châu', 'Lào Cai', 'Yên Bái', 'Phú Thọ',
                 'Hà Giang', 'Tuyên Quang', 'Cao Bằng', 'Bắc Kạn', 'Thái Nguyên', 'Lạng Sơn', 'Bắc Giang',
                 'Quảng Ninh', 'Hà Nội', 'Bắc Ninh', 'Hà Nam', 'Hải Dương', 'Hải Phòng', 'Hưng Yên',
                 'Nam Định', 'Thái Bình', 'Vĩnh Phúc', 'Ninh Bình', 'Thanh Hóa', 'Nghệ An', 'Hà Tĩnh',
                 'Quảng Bình', 'Quảng Trị', 'Huế', 'Đà Nẵng', 'Quảng Nam', 'Quảng Ngãi', 'Bình Định',
                 'Phú Yên', 'Khánh Hòa', 'Ninh Thuận', 'Bình Thuận', 'Kon Tum', 'Gia Lai', 'Đắk Lắk',
                 'Lâm Đồng', 'Đà Lạt', 'Hồ Chí Minh', 'Bà Rịa Vũng Tàu', 'Bình Dương', 'Bình Phước',
                 'Đồng Nai', 'Tây Ninh', 'An Giang', 'Bạc Liêu', 'Bến Tre', 'Cà Mau', 'Cần Thơ',
                 'Đồng Tháp', 'Hậu Giang', 'Kiên Giang', 'Long An', 'Sóc Trăng', 'Tiền Giang',
                 'Trà Vinh', 'Vĩnh Long']

weather_dict = {
    'clear sky': 'trời quang đãng',
    'few clouds': 'trời ít mây',
    'scattered clouds': 'trời rải rác mây',
    'broken clouds': 'trời nhiều mây',
    'overcast clouds': 'trời âm u',
    'mist': 'trời sương mù',
    'smoke': 'trời có khói bụi',
    'haze': 'trời có sương mù nhẹ',
    'dust': 'trời bụi bẩn',
    'fog': 'trời có sương mù dày đặc',
    'sand': 'trời có cát bão',
    'volcanic ash': 'tro núi lửa',
    'squalls': 'trời có gió mạnh',
    'tornado': 'trời có lốc xoáy',
    'thunderstorm with light rain': 'trời có giông bão kèm mưa nhẹ',
    'thunderstorm with rain': 'trời có giông bão kèm mưa',
    'thunderstorm with heavy rain': 'trời có giông bão kèm mưa lớn',
    'light thunderstorm': 'trời có giông nhẹ',
    'thunderstorm': 'trời có giông bão',
    'heavy thunderstorm': 'trời có giông bão lớn',
    'ragged thunderstorm': 'trời có giông bão kèm mưa rào',
    'thunderstorm with light drizzle': 'trời có giông bão kèm mưa phùn nhẹ',
    'thunderstorm with drizzle': 'trời có giông bão kèm mưa phùn',
    'thunderstorm with heavy drizzle': 'trời có giông bão kèm mưa phùn lớn',
    'light intensity drizzle': 'trời có mưa phùn nhẹ',
    'drizzle': 'trời có mưa phùn',
    'heavy intensity drizzle': 'trời có mưa phùn lớn',
    'light intensity drizzle rain': 'trời có mưa phùn nhẹ kèm mưa nhỏ',
    'drizzle rain': 'trời có mưa phùn kèm mưa nhỏ',
    'heavy intensity drizzle rain': 'trời có mưa phùn lớn kèm mưa nhỏ',
    'shower rain and drizzle': 'trời có mưa phùn và mưa nhỏ',
    'heavy shower rain and drizzle': 'trời có mưa phùn và mưa lớn',
    'shower drizzle': 'trời có mưa phùn',
    'light rain': 'trời có mưa nhỏ',
    'moderate rain': 'trời có mưa vừa',
    'heavy intensity rain': 'trời có mưa to',
    'very heavy rain': 'trời có mưa rất to',
    'extreme rain': 'trời có mưa cực to',
    'freezing rain': 'trời có mưa đá',
    'light intensity shower rain': 'trời có mưa nhỏ rải rác',
    'shower rain': 'trời có mưa rải rác',
    'heavy intensity shower rain': 'trời có mưa lớn rải rác',
    'torrential shower rain': 'trời có mưa lớn rải rác',
    'light snow': 'trời có tuyết nhẹ',
    'snow': 'trời có tuyết',
    'heavy snow': 'trời có tuyết to',
    'sleet': 'trời có mưa tuyết',
    'shower sleet': 'trời có mưa tuyết rải rác',
    'light rain and snow': 'trời có mưa nhỏ kèm tuyết nhẹ',
    'rain and snow': 'trời có mưa kèm tuyết',
    'light shower snow': 'trời có mưa tuyết rải rác nhẹ',
    'shower snow': 'trời có mưa tuyết rải rác',
    'heavy shower snow': 'trời có mưa tuyết rải rác to',
    'mist': 'trời có sương mù',
    'smoke': 'trời có khói bụi',
    'sand/ dust whirls': 'trời có gió xoáy cát/bụi',
    'fog': 'trời có sương mù',
    'sand': 'trời có cát bão',
    'dust': 'trời có bụi bặm',
    'volcanic ash': 'trời có tro núi lửa',
    'squalls': 'trời có gió mạnh',
    'tornado': 'trời có lốc xoáy',
    'clear sky': 'trời quang đãng',
    'few clouds': 'trời có ít mây',
    'scattered clouds': 'trời có rải rác mây',
    'broken clouds': 'trời có nhiều mây',
    'overcast clouds': 'trời âm u'
}


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
        c_description = data['weather'][0]['description']
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
        Nhìn chung: {description}
        """.format(day=now.day, month=now.month, year=now.year,
                   temp=c_temperature, pressure=c_pressure, humidity=c_humidity,
                   wind_speed=c_wind_speed, wind_direction=c_wind_direction, feels_like=c_feels_like,
                   clouds=c_clouds, description=weather_dict[c_description])
        content += getOutFit(c_temperature, c_humidity, c_wind_speed)
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
        c_wind_speed = data['wind']['speed']  # tốc độ gió
        c_description = data['weather'][0]['description']
        content += f"Thời tiết ngày {past_date.strftime('%d-%m-%Y')} tại {location}:<br>Nhiệt độ trung bình là {temp}°C<br>Áp suất không khí là {pressure} hPa<br>Độ ẩm là {humidity}%<br>Tốc độ gió {c_wind_speed} m/s<br> Nhìn chung {weather_dict[c_description]}"
    else:
        content = "Không tìm thấy địa chỉ theo yêu cầu"
    return content


def weatherFocast(location, num_days):
    complete_api_link = "https://api.openweathermap.org/data/2.5/forecast?q=" + \
        location+"&appid="+api_key
    api_link = requests.get(complete_api_link)
    api_data = api_link.json()
    content = ''
    if api_data['cod'] == '404':
        content = 'Không tìm thấy địa điểm: {}, hãy kiểm tra lại.'.format(
            location)
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
                    content += "Ngày :{}\nNhiệt độ trung bình {:.2f}°C<br>Áp lực không khí là {} Pascals<br>Độ ẩm là {}%<br>Tốc độ gió {} m/s<br>Nhiệt độ cảm nhận {:.2f}°C<br>Nhìn chung: {}<br>---------------------------------------------------------------------<br>".format(
                        forecast_date_str, api_data['list'][j]['main']['temp'] - 273.15,
                        api_data['list'][j]['main']['pressure'], api_data['list'][j]['main']['humidity'],
                        api_data['list'][j]['wind']['speed'],
                        api_data['list'][j]['main']['feels_like'] - 273.15,
                        weather_dict[api_data['list'][j]
                                     ['weather'][0]['description']]
                    )
                    break
    return content


def list_recommended_place():
    print('collector recommend')
    ow_url = "http://api.openweathermap.org/data/2.5/weather?"
    for i in range(20):
        city = list_province[i]
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
            if current_temperature < 25:
                continue
            current_pressure = city_res["pressure"]
            current_humidity = city_res["humidity"]
            now = datetime.now()
            content = """
            Ngày {day} tháng {month} năm {year}<br>
            Nhiệt độ trung bình là {temp} độ C<br>
            Áp lực không khí là {pressure} Pascals<br>
            Độ ẩm là {humidity}%<br>
            """.format(day=now.day, month=now.month, year=now.year,
                       temp=current_temperature, pressure=current_pressure, humidity=current_humidity)
        else:
            continue
        list_survive.append(i)
        dict_place[list_province[i]] = content


list_recommended_place()


def recommended_place():
    n = []
    content = ''
    for i in range(3):
        val = random.choice(list_survive)
        while val in n:
            val = random.choice(list_survive)
        n.append(val)
        content += '-------------------------------<br>'
        content += list_province[val] + ':<br>'
        content += dict_place[list_province[val]] + '<br>'
    return content


def getOutFit(temperature, humidity, win_speed):
    content = ''
    if temperature < 10:
        content += 'thời tiết bên ngoài rất là lạnh bạn nên mặc áo khoác ấm, đội mũ len, quàng khăn và đi giày ấm nhé'
    elif temperature >= 10 and temperature <= 20:
        content = "thòi tiết hơi se lạnh đó bạn nên mặc áo khoác nhẹ, áo len và giày bảo vệ đôi chân nha"
    elif temperature > 20 and temperature <= 30:
        content = "Thời tiết nay khá là dễ chịu bạn nên mặc áo phông, quần short và giày thể thao nha"
    else:
        content = "Trời hôm nay khá là nóng bức bạn nên mặc những bộ quần áo mát mẻ, thoải mái và uống nước đầy đủ đó <3"

    if humidity > 60:
        content += '<br>Độ ẩm không khí khá là cao khả năng sẽ có mưa đó, khi ra ngoài nhớ mang theo ô hay áo mưa đóoo'
    if win_speed > 20:
        content += '<br>Hôm nay gió khá là lớn hãy tránh những trang phục bồng bềnh nha'
    return content


@app.route('/')
def home():

    return render_template("index.html")


TYPE_SET_LOCATION = 0
TYPE_SET_FOCAST = 0
TYPE_SET_PAST = 0
TYPE_SET_TODAY = 0
today = ['bây giờ', 'hiện tại', 'ở đây', 'nay', 'hn', 'hôm nay']
past = ['trước', 'qua', 'quá khứ', 'xưa',
        'đã', 'cách đây', 'ký ức', 'từng', 'cũ']
future = ['tương lai', 'sau', 'ngày mai', 'kia', 'tiếp theo',
          'sắp', 'sẽ', 'dự kiến', 'dự đoán', 'dự tính']
pos = ['nơi khác', 'địa điểm', 'chỗ khác', 'khu vực khác']

travel = ['du lịch', 'đi chơi', 'đi phượt', 'bay lắc']


def analysisMessage(list, message):
    for text in list:
        if text in message:
            return True
    return False


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
    if analysisMessage(today, text) or TYPE_SET_TODAY == 1:
        if TYPE_SET_TODAY == 1:
            location = text
            respone = weatherToday(location)
            if 'Không tìm thấy địa' in respone:
                respone = 'không tìm thấy địa chỉ theo yêu cầu, anh/chị nhập lại mỗi tên địa điểm giúp em ạ'
                TYPE_SET_TODAY = 1
            else:
                TYPE_SET_TODAY = 0
        elif location == 'none':
            respone = 'Bạn muốn xem thời tiết ở đâu ạ ^^! (nhập mỗi tên địa điểm giúp iem)'
            TYPE_SET_TODAY = 1
        elif location != 'none':
            respone = weatherToday(location)
            if 'Không tìm thấy địa' in respone:
                respone = 'không tìm thấy địa chỉ theo yêu cầu, anh/chị nhập lại mỗi tên địa điểm giúp em ạ'
                TYPE_SET_TODAY = 1
            else:
                TYPE_SET_TODAY = 0
    # --------------------Xem thời tiết tương lai------------------------------
    elif analysisMessage(future, text) or TYPE_SET_FOCAST == 1 or TYPE_SET_FOCAST == 2:
        if TYPE_SET_FOCAST == 1:
            # if location == 'none':
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
                    if 'không tìm thấy địa' in respone.lower():
                        respone = 'không tìm thấy địa chỉ theo yêu cầu, anh/chị nhập lại mỗi tên địa điểm giúp em ạ'
                        TYPE_SET_FOCAST = 1
                    else:
                        TYPE_SET_FOCAST = 0
            else:
                respone = 'số ngày này trông hơi lạ nhập lại giúp em -.-'
                TYPE_SET_FOCAST = 1
        elif location == 'none':
            respone = 'Bạn muốn xem thời tiết ở đâu ạ ^^! (nhập mỗi tên địa điểm giúp iem)'
            TYPE_SET_FOCAST = 1
        elif location != 'none' and day_future == 0:
            respone = 'Bạn muốn dự báo thời tiết trong mấy ngày tới ạ ^^ (nhập số ngày giúp iem)'
            TYPE_SET_FOCAST = 2
        elif location != 'none' and day_future != 0:
            respone = weatherFocast(location, day_future)
    # --------------------Xem thời tiết quá khứ------------------------------
    elif analysisMessage(past, text) or TYPE_SET_PAST == 1 or TYPE_SET_PAST == 2:
        if TYPE_SET_PAST == 1:
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
                    respone = PastWeather(location, day_past)
                    if 'Không tìm thấy địa' in respone:
                        respone = 'không tìm thấy địa chỉ theo yêu cầu, anh/chị nhập lại mỗi tên địa điểm giúp em ạ'
                        TYPE_SET_PAST = 1
                    else:
                        TYPE_SET_PAST = 0
            else:
                respone = 'số ngày này trông hơi lạ nhập lại giúp em -.-'
                TYPE_SET_PAST = 1
        elif location == 'none':
            respone = 'Bạn muốn xem thời tiết ở đâu ạ ^^! (nhập mỗi tên địa điểm giúp iem)'
            TYPE_SET_PAST = 1
        elif location != 'none' and day_past == 0:
            respone = 'Bạn muốn xem lại thời tiết cách đây mấy ngày ạ ^^ (nhập số ngày giúp iem)'
            TYPE_SET_PAST = 2
    # --------------------Thay đổi địa điểm xem thời tiết-------------------------------
    elif analysisMessage(pos, text) or TYPE_SET_LOCATION == 1:
        if TYPE_SET_LOCATION == 0:
            respone = 'Bạn muốn xem thời tiết ở đâu ạ ^^! (nhập mỗi tên địa điểm giúp iem)'
            TYPE_SET_LOCATION = 1
        else:
            location = text
            respone = 'Anh/chị muốn xem dự báo thời tiết sắp tới hay là thời tiết hôm nay ở ' + location + ' ạ'
            TYPE_SET_LOCATION = 0
    # ----------------------------------recommend địa điểm du lịch
    elif analysisMessage(travel, text):
        respone = 'Sau đây là một vài địa điểm du lịch có thời tiết khá là dễ chịu mà em tìm được ^^<br>'
        respone += recommended_place()
        respone += '------------------------------<br>'
        respone += 'Đây đều là những nơi có thời tiết rất là mát mẻ phù hợp để đi chơi, đi phượt, đi chill ><'

        # --------------------Trả lời theo trainning-------------------------------
    elif 'thời tiết ở ' in text:
        if location == 'none':
            respone = 'Xin lỗi anh/chị vui lòng nhập mỗi tên địa chỉ giúp em ạ ^^!'
            TYPE_SET_LOCATION = 1
        else:
            respone = 'Anh/chị muốn xem dự báo thời tiết sắp tới hay là thời tiết hôm nay ở ' + location + ' ạ'
    else:
        respone = getResponse(text)
    return jsonify({'respone': respone})


if __name__ == "__main__":
    app.run()
