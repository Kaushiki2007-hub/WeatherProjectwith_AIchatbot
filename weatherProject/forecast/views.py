from django.shortcuts import render

# Create your views here. 
import requests  #This libraries helps us to fetch data from API
import pandas as pd #for handling and analysing data
import numpy as np #for numerical operations
from sklearn.model_selection import train_test_split #to split data into training and testing sets
from sklearn.preprocessing import LabelEncoder #to convert catogerical data into numerical values
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor #models for  classification and regression tasks
from sklearn.metrics import mean_squared_error #to measure the accuracy of our predictions
from datetime import datetime,timedelta #to handle date and time
import pytz
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

API_KEY ='9c3cd822dd53520af014bd66de3d9aa8' #replace with your actual API key
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather' #base url for making API requests

#1. Fetch Current Weather Data
def get_current_weather(city):
  url = (
      f"https://api.openweathermap.org/data/2.5/weather"
      f"?q={city}&appid={'9c3cd822dd53520af014bd66de3d9aa8'}&units=metric" #construct the API request URL
  )

  response = requests.get(url) # send the get request to API
  data = response.json()

  # ❗ SAFETY CHECK
  if response.status_code != 200:
      return None
  
  return {
      'city': data['name'],
      'country': data['sys']['country'],
      'current_temp': round(data['main']['temp']),
      'feels_like': round(data['main']['feels_like']),
      'temp_min': round(data['main']['temp_min']),
      'temp_max': round(data['main']['temp_max']),
      'humidity': round(data['main']['humidity']),
      'description': data['weather'][0]['description'],
      'country': data['sys']['country'],
      'wind_gust_dir': data['wind']['deg'],
      'pressure': data['main']['pressure'],
      'wind_speed': data['wind']['speed'],
      'wind_gust_speed': data['wind']['speed'],
      'clouds': data['clouds']['all'],
      'visibility': data.get('visibility', 'N/A'),
  }

def get_5day_forecast(city):
    url = (
        f"https://api.openweathermap.org/data/2.5/forecast"
        f"?q={city}&appid={API_KEY}&units=metric"
    )

    response = requests.get(url)
    data = response.json()

    if response.status_code != 200:
        return []

    daily = {}
    forecast = []

    for item in data['list']:
        date = item['dt_txt'].split(' ')[0]

        if date not in daily:
            daily[date] = {
                'date': date,
                'temp': round(item['main']['temp']),
                'humidity': item['main']['humidity'],
                'description': item['weather'][0]['description'],
                'icon': item['weather'][0]['icon'],
            }

        if len(daily) == 5:
            break

    return list(daily.values())

#2. Read Historical Data
def read_historical_data(filename):
  df = pd.read_csv(filename) #load csv file into dataFrame
  df = df.dropna() #remove rows wit missing values
  df = df.drop_duplicates()
  return df



#3. Prepare date for training
def prepare_data(data):
  le = LabelEncoder() #create a LabelEncoder instance
  data['WindGustDir'] = le.fit_transform(data['WindGustDir'])
  data['RainTomorrow'] = le.fit_transform(data['RainTomorrow'])

  #define the feature variables and target variables
  X = data[['MinTemp', 'MaxTemp', 'WindGustDir', 'WindGustSpeed', 'Humidity', 'Pressure', 'Temp']] #feature variables
  y = data['RainTomorrow'] # target variable

  return X, y, le #return feature variable, target variable and the lable encoder



#4. Train Rain Prediction Model
def train_rain_model(X,y):
  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
  model = RandomForestClassifier(n_estimators=100, random_state=42)
  model.fit(X_train, y_train) #train the model

  y_pred = model.predict(X_test) #to make prediction on test set

  print("Mean Squared Error for Rain Model")

  print(mean_squared_error(y_test, y_pred))

  return model


#5. Prepare regression data
def prepare_regression_date(data, feature):
  X, y = [], [] #initialize list for feature and target values

  for i in range(len(data) - 1):
    X.append(data[feature].iloc[i])
    y.append(data[feature].iloc[i+1])

  X = np.array(X).reshape(-1, 1)
  y = np.array(y)
  return X, y




#6. Train Regression Model
def train_regression_model(X, y):
  model = RandomForestRegressor(n_estimators=100, random_state=42)
  model.fit(X, y)
  return model

#7. Predict Future
def predict_future(model, current_value):
  predictions = [current_value]

  for i in range(5):
    next_value = model.predict(np.array([[predictions[-1]]]))

    predictions.append(next_value[0])

  return predictions[1:]


#Weather Analysis Function
def weather_view(request):
    if request.method == 'POST':
        city = request.POST.get('city')
        current_weather = get_current_weather(city)
        
        # print(current_weather)

        if not current_weather:
            return render(request, 'weather.html', {
                'error': 'City not found',
                'descreption': 'clear'
            })

        five_day_forecast = get_5day_forecast(city)


        #load historical data
        csv_path = os.path.join(BASE_DIR, 'weather.csv')
        historical_data = read_historical_data(csv_path)

        #prepare and train the rain prediction model

        X, y, le = prepare_data(historical_data)

        rain_model = train_rain_model(X, y)

        # map wind direction to campass points
        wind_deg = current_weather['wind_gust_dir'] % 360
        compass_points = [
            ("N", 0, 11.25), ("NNE", 11.25, 33.75), ("NE", 33.75, 56.25),
            ("ENE", 56.25, 78.75), ("E", 78.75, 101.25), ("ESE", 101.25, 123.75),
            ("SE", 123.75, 146.25), ("SSE", 146.25, 168.75), ("S", 168.75, 191.25),
            ("SSW", 191.25, 213.75), ("SW", 213.75, 236.25), ("WSW", 236.25, 258.75),
            ("W", 258.75, 281.25), ("WNW", 281.25, 303.75), ("NW", 303.75, 326.25),
            ("NNW", 326.25, 348.75)
        ]
        compass_direction = next((point for point, start, end in compass_points if start <= wind_deg < end), "N")


        compass_direction_encoded = le.transform([compass_direction])[0] if compass_direction in le.classes_ else -1


        current_data = {
            'MinTemp': current_weather['temp_min'],
            'MaxTemp': current_weather['temp_max'],
            'WindGustDir': compass_direction_encoded,
            'WindGustSpeed': current_weather['wind_gust_speed'],
            'Humidity': current_weather['humidity'],
            'Pressure': current_weather['pressure'],
            'Temp': current_weather['current_temp'],
        }

        current_df = pd.DataFrame([current_data])

        #rain prediction

        rain_prediction = rain_model.predict(current_df)[0]

        #prepare regression model for temperature and humidity

        X_temp, y_temp = prepare_regression_date(historical_data, 'Temp')

        X_hum, y_hum = prepare_regression_date(historical_data, 'Humidity')

        temp_model = train_regression_model(X_temp, y_temp)

        hum_model = train_regression_model(X_hum, y_hum)

        #predict future temperature and humidity

        future_temp = predict_future(temp_model, current_weather['temp_min'])

        future_humidity = predict_future(hum_model, current_weather['humidity'])

        #prepare time for future predictions

        timezone = pytz.timezone('Asia/Kolkata')
        current_time = datetime.now(timezone)
        next_hour = current_time + timedelta(hours=1)
        next_hour = next_hour.replace(minute=0, second=0, microsecond=0)

        future_times = [(next_hour + timedelta(hours=i)).strftime("%H:00") for i in range(5)]

        #store each value seperately

        time1, time2, time3, time4, time5 = future_times
        temp1, temp2, temp3, temp4, temp5 = future_temp
        hum1, hum2, hum3, hum4, hum5 = future_humidity

        # pass data to template 
        weather = current_weather['description'].lower()

        if "clear" in weather:
            weather_bg = "clear"

        elif "cloud" in weather:
            weather_bg = "cloudy"

        elif "overcast" in weather:
            weather_bg = "overcast"

        elif "drizzle" in weather:
            weather_bg = "drizzle"

        elif "rain" in weather:
            weather_bg = "rain"

        elif "shower" in weather:
            weather_bg = "showers"

        elif "mist" in weather:
            weather_bg = "mist"

        elif "fog" in weather:
            weather_bg = "fog"

        elif "snow" in weather:
            weather_bg = "snow"

        elif "thunder" in weather:
            weather_bg = "thunder"

        else:
            weather_bg = "clear"

        context = {
            'current_weather': current_weather,
            'forecast_5days': five_day_forecast,
            'location': city,
            'current_tem': current_weather['current_temp'],
            'MinTemp': current_weather['temp_min'],
            'MaxTemp': current_weather['temp_max'],
            'feels_like': current_weather['feels_like'],
            'humidity': current_weather['humidity'],
            'clouds': current_weather['clouds'],
            'description': current_weather['description'],
            'description_bg': weather_bg,
            'city': current_weather['city'],
            'country': current_weather['country'], 
            'time': datetime.now(),
            'date': datetime.now().strftime("%B %d, %Y"),
            'wind': current_weather['wind_gust_speed'],
            'pressure': current_weather['pressure'],
            'visibility': current_weather.get('visibility', 'N/A'),

            'time1': time1,
            'time2': time2,
            'time3': time3,
            'time4': time4,
            'time5': time5,

            'temp1': f"{round(temp1, 1)}",
            'temp2': f"{round(temp2, 1)}",
            'temp3': f"{round(temp3, 1)}",
            'temp4': f"{round(temp4, 1)}",
            'temp5': f"{round(temp5, 1)}",

            'hum1': f"{round(hum1, 1)}",
            'hum2': f"{round(hum2, 1)}",
            'hum3': f"{round(hum3, 1)}",
            'hum4': f"{round(hum4, 1)}",
            'hum5': f"{round(hum5, 1)}",
          }

        return render(request, 'weather.html', context)
      
    return render(request, 'weather.html', {'description_bg': 'clear'})

from django.http import JsonResponse
import json


def ai_chat(request):

    if request.method != "POST":
        return JsonResponse({
            "reply": "Please send a message using the chatbot."
        })

    try:

        data = json.loads(request.body)

        message = data.get("message", "").lower()

        weather = data.get("weather", {})

        description = weather.get("description", "").lower()
        temp = weather.get("temp", 0)
        humidity = weather.get("humidity", 0)
        wind = weather.get("wind", 0)

        # Umbrella
        if "umbrella" in message:

            if "rain" in description or "drizzle" in description:
                reply = "☔ Yes! You should carry an umbrella because rain is expected."

            else:
                reply = "🌤️ No umbrella is needed today."

        # Clothes
        elif "wear" in message or "clothes" in message:

            if temp >= 35:
                reply = "👕 It's hot today. Wear light cotton clothes and stay hydrated."

            elif temp >= 25:
                reply = "🙂 Comfortable casual clothes are perfect."

            else:
                reply = "🧥 Carry a light jacket."

        # Travel
        elif "travel" in message or "trip" in message:

            if "rain" in description or "drizzle" in description:
                reply = "🚗 Travel is possible, but expect rain and slippery roads."

            else:
                reply = "✅ Weather looks good for travelling."

        # Sports
        elif (
            "cricket" in message
            or "football" in message
            or "sports" in message
            or "play" in message
        ):

            if "rain" in description or "drizzle" in description:
                reply = "⚽ Outdoor sports may be affected by rain."

            else:
                reply = "🏏 Great weather for outdoor activities."

        # Temperature
        elif "temperature" in message or "temp" in message:

            reply = f"🌡️ The current temperature is {temp}°C."

        # Humidity
        elif "humidity" in message:

            reply = f"💧 The current humidity is {humidity}%."

        # Wind
        elif "wind" in message:

            reply = f"💨 The current wind speed is {wind} km/h."

        # General weather
        elif (
            "weather" in message
            or "condition" in message
            or "outside" in message
        ):

            reply = (
                f"🌤️ Current weather is {description}, "
                f"temperature is {temp}°C, "
                f"humidity is {humidity}%, "
                f"and wind speed is {wind} km/h."
            )

        # Default response
        else:

            reply = (
                f"🌤️ Current weather is {description} "
                f"with {temp}°C."
            )

        return JsonResponse({
            "reply": reply
        })

    except Exception as e:

        print("AI CHAT ERROR:", e)

        return JsonResponse({
            "reply": "❌ Sorry, something went wrong while processing your message."
        }, status=500)
