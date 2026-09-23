# WeatherProjectwith_AIchatbot
# 🌦️ AI Weather Forecast & Prediction System

A Django-based intelligent weather application that provides real-time weather information, machine learning-based weather predictions, hourly forecasts, 5-day forecasts, and an AI Weather Assistant.

---

## 📌 Project Overview

The **AI Weather Forecast & Prediction System** is a web-based weather application developed using Python and Django.

The application fetches real-time weather data using the **OpenWeatherMap API** and combines it with Machine Learning models to provide additional weather predictions.

It also includes an **AI Weather Assistant** that allows users to ask questions about the current weather through an interactive chatbot.

---

## ✨ Features

- 🌍 Search weather by city
- 🌡️ Real-time temperature information
- 🤗 Feels-like temperature
- 💧 Humidity information
- 💨 Wind speed and direction
- ☁️ Cloud coverage
- 🌡️ Minimum and maximum temperature
- 🔽 Atmospheric pressure
- 👁️ Visibility
- 🌧️ Rain prediction using Machine Learning
- 📈 Future temperature prediction
- 💧 Future humidity prediction
- ⏰ 5-hour weather forecast
- 📅 5-day weather forecast
- 📊 Interactive temperature chart using Chart.js
- 🌦️ Dynamic weather backgrounds and animations
- 🤖 AI Weather Assistant
- 💬 Interactive weather chatbot
- 📱 Responsive and user-friendly interface

---

## 🤖 Machine Learning

The project uses Machine Learning models to generate weather predictions.

### 1. Rain Prediction

A **Random Forest Classifier** is used to predict whether rain is expected.

### Features used:

- Minimum Temperature
- Maximum Temperature
- Wind Direction
- Wind Speed
- Humidity
- Pressure
- Temperature

### 2. Temperature Prediction

A **Random Forest Regressor** is used to predict future temperature values.

### 3. Humidity Prediction

Another **Random Forest Regressor** is used to predict future humidity values.

---

## 💬 AI Weather Assistant

The project includes an interactive chatbot called:

**AI Weather Assistant**

Users can ask questions such as:

- What is the temperature?
- Should I carry an umbrella?
- What should I wear?
- Can I travel today?
- Is it good weather for cricket?
- What is the humidity?
- What is the wind speed?

The chatbot receives weather information from the application and generates weather-related responses.

---

## 🛠️ Technologies Used

### Frontend

- HTML5
- CSS3
- JavaScript
- Bootstrap Icons
- Chart.js

### Backend

- Python
- Django

### Machine Learning

- Scikit-learn
- Pandas
- NumPy

### API

- OpenWeatherMap API

### Database

- SQLite

### Development Tools

- Visual Studio Code
- Git
- GitHub

---

## 📂 Project Structure

📊 Machine Learning Workflow
Historical Weather Dataset
          ↓
Data Cleaning
          ↓
Data Preprocessing
          ↓
Feature Selection
          ↓
Train/Test Split
          ↓
Random Forest Models
          ↓
Weather Prediction
          ↓
Display Results
```text
MachineLearningProject/
│
└── weatherProject/
    │
    ├── forecast/
    │   ├── migrations/
    │   ├── static/
    │   │   └── js/
    │   │       ├── chatbot.js
    │   │       └── chat/
    │   │           └── Setup.js
    │   │
    │   ├── templates/
    │   │   └── weather.html
    │   │
    │   ├── urls.py
    │   ├── views.py
    │   └── ...
    │
    ├── weatherProject/
    │   ├── settings.py
    │   ├── urls.py
    │   └── ...
    │
    ├── weather.csv
    ├── db.sqlite3
    ├── manage.py
    └── README.md

▶️ Run the Project
##Steps
1. Open the project:
 cd weatherProject
2. Create a virtual environment:
python -m venv myenv
3. Activate the virtual environment:
myenv\Scripts\activate
4. Install dependencies:
pip install django requests pandas numpy scikit-learn pytz
5. Run the Django development server:
python manage.py runserver
6. Open the application in your browser:
http://127.0.0.1:8000/

🎯 Objectives
• Provide real-time weather information.
• Apply Machine Learning to weather prediction.
• Predict rainfall using historical weather data.
• Predict future temperature and humidity.
• Provide an interactive weather dashboard.
• Provide an AI-powered conversational weather assistant.
• Create an easy-to-use and responsive weather application.

🚀 Future Enhancements
🤖 Integration with an advanced LLM such as Gemini or OpenAI
🗣️ Voice-based weather assistant
📍 Automatic location detection
🌧️ More accurate rainfall prediction
🛰️ Weather alerts and notifications
📈 Advanced weather analytics
☁️ Cloud deployment
📱 Mobile application
🌍 Multi-city weather comparison

👩‍💻 Author
Kaushiki Rani
B.Tech – Computer Science & Engineering (AI & ML)
