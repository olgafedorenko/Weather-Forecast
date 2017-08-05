import json
import requests
from datetime import datetime, timedelta
from pytz import timezone
from pytz import all_timezones

KEY = '748a3d038c69fce696cce47a0060be59'

def run():
    while True:
        city = input('Enter city name: ')
        action = input('What do you like to know: ')
        format_temp =input('Celsius(C) or Fahrenheit(F)?')
        if action == 'today weather':
            d = current_weather(city, format_temp)
            for key, value in d.items():
                print("key, ")

        elif action == 'weather for 5 next days':
            while n_days not in range(1, 5):
                n_days = int(input("Enter Number:"))
            week(city,  format_temp, n_days)
        else:
            print ('Try again')


def convert_to_C(temp):
    return temp - 273


def convert_to_F(temp):
    return 32 + (9 / 5) *(temp)


def convert_clouds(clouds, name):
    if clouds >= 90:
        return 'Now cloudy in {}'.format(name)
    elif clouds >= 70:
        return 'Now mostly cloudy in {}'.format(name)
    elif clouds >= 30:
        return 'Partly Cloudy / Partly Sunny in {}'.format(name)
    elif clouds >= 10:
        return 'Mostly Clear / Mostly Sunny in {}'.format(name)
    else:
        return 'Clear / Sunny in {}'.format(name)

def convert_wind(wind, name):
    if wind >= 40:
        return 'Now Strong, High, Damaging in {}. Twigs and small branches are broken from trees, ' \
               'walking is difficult.Moderately large waves with blown foam.'.format(name)
    elif wind >= 25:
        return 'Now Strong Breeze in {}. Large tree branches move,  telephone wires begin to "whistle", umbrellas are difficult to keep under control.' \
               'Larger waves form, whitecaps prevalent, spray.'.format(name)
    elif wind >= 15:
        return 'Now is so windy in {}. Small branches move, raises dust, leaves and paper. ' \
               'Small waves develop, becoming longer, whitecaps.'.format(name)
    elif wind >= 8:
        return 'Gentle Breeze in {}. Leaves and small twigs move, light weight flags extend. ' \
               'Large wavelets, crests start to break, some whitecaps.'.format(name)
    elif wind >= 4:
        return 'Light Breeze in {}. Leaves rustle, can feel wind on your face, wind vanes begin to move. ' \
               'Small wavelets develop, crests are glassy.'.format(name)
    elif wind > 1.1:
        return 'Light Air in {}. Rising smoke drifts, wind vane is inactive. ' \
               'Small ripples appear on water surface.'.format(name)
    else:
        return 'Calm in {}. Still, calm air, smoke will rise vertically. ' \
               'Water is mirror-like'.format(name)

def get_timezone(lon, lat, dt):
    #time_r=requests.get('https://maps.googleapis.com/maps/api/timezone/json?location={},{}&timestamp={}&sensor=false'.format(lat, lon, dt))
    time_r = requests.get(
        'https://maps.googleapis.com/maps/api/timezone/json?location={},{}&timestamp={}&sensor=false&key=AIzaSyCPKFIh9tid-AFIdXR1HaMIeIKVlscx3o0'.format(
            lat, lon, dt))
    time_data=time_r.json()
    tzid_1=time_data['timeZoneId']
    return tzid_1

def current_weather(city, format_temp):
    d=dict()
    request = 'http://api.openweathermap.org/data/2.5/weather?q={}&APPID={}&units=metric'.format(city, KEY)
    city_r = requests.get(request)
    city_data = city_r.json()
    print(city_data)
    name = city_data['name']
    if format_temp == 'C':
        d['temp']='Current temperature in '+ name+' is ' +'{:0.1f}'.format(city_data['main']['temp'])+ ' °C'
        d['temp_min']='The minimum temperature today is '+'{:0.1f}'.format(city_data['main']['temp_min'])+' °C'
        d['temp_max']='The maximum temperature today is '+'{:0.1f}'.format(city_data['main']['temp_max'])+' °C'

    else:
        d['temp']='Current temperature in '+ name+' is ' + '{:0.1f}'.format(convert_to_F((city_data['main']['temp'])))+ ' °F'
        d['temp_min']='The minimum temperature today is '+'{:0.1f}'.format(convert_to_F((city_data['main']['temp_min'])))+ ' °F'
        d['temp_max']='The maximum temperature today is '+ '{:0.1f}'.format(convert_to_F((city_data['main']['temp_max'])))+ ' °F'


    sunrise = city_data['sys']['sunrise']
    sunset = city_data['sys']['sunset']
    wind = city_data['wind']['speed']
    clouds = city_data['clouds']['all']

    tzid=get_timezone(city_data['coord']['lon'], city_data['coord']['lat'], city_data['dt'])
    datetime_tz = datetime.fromtimestamp(sunset, timezone(tzid))
    d['sunset2'] = 'Sunset at ' + datetime_tz.strftime("%H:%M:%S ")
    d['sunrise2'] = 'Sunrise at ' + datetime.fromtimestamp(sunrise, timezone(tzid)).strftime("%H:%M:%S")


    d['clouds'] = convert_clouds(clouds, name)
    d['humidity'] = 'Humidity = {} %'.format(city_data['main']['humidity'])
    d['wind'] = 'Wind = {}  mph. {}.'.format(wind, convert_wind(wind, name))


    print(d)
    return d

def week(city, format_temp, n_days):
    week_r=requests.get('http://api.openweathermap.org/data/2.5/forecast?q={},us&mode=json&APPID={}&units=metric'.format(city, KEY))
    week_data = week_r.json()
    city_name = week_data['city']['name']
    dicts = []
    for i in week_data['list']:
            m = i['dt_txt']
            tzid2 = get_timezone(week_data['city']['coord']['lon'], week_data['city']['coord']['lat'], i['dt'])
            #forecast_time = datetime.strptime(i['dt'], '%Y-%m-%d %H:%M:%S')
            forecast_time_str = datetime.utcfromtimestamp(i['dt']).strftime("%H:%M:%S")
            forecast_time = datetime.strptime(forecast_time_str, '%H:%M:%S')
            if forecast_time.hour != 18:
                continue
            forecast_date_int= datetime.fromtimestamp(float(i['dt']), timezone(tzid2)).strftime('%Y-%m-%d %H:%M:%S')

            forecast_date = datetime.strptime(forecast_date_int, '%Y-%m-%d %H:%M:%S')
            delta = timedelta(days=n_days)
            #delta2=timedelta(days=1)
            today = datetime.today()
            end_date = today + delta #+ delta2


            if forecast_date > end_date:
                break

            d = {}
            d['city_name'] = city_name
            if format_temp == 'C' :
                d['date']= forecast_date.isoformat()
                d['temp']= 'Current temperature in {} {:0.1f} °C'.format(city_name, i['main']['temp'])
                wind = i['wind']['speed']
                clouds = i['clouds']['all']

                d['clouds']=convert_clouds(clouds, city_name)
                d['humidity']= 'Humidity = {} %'.format(i['main']['humidity'])
                d['wind']='Wind = {} {} mph'.format(wind, convert_wind(wind, city_name))

            elif format_temp == 'F':
                d['date']=  forecast_date
                d['temp']= 'Current temperature in ' + city_name +' is '+ '{:0.1f}'.format(convert_to_F((i['main']['temp']))) + ' °F'
                wind = i['wind']['speed']
                clouds = i['clouds']['all']

                d['clouds']=  convert_clouds(clouds, city_name)
                d['humidity']= 'Humidity = {}%'.format(i['main']['humidity'])
                d['wind']=   'Wind = {} mph. {}.'.format(wind, convert_wind(wind, city_name))
            dicts.append(d)
    return dicts

