# This is a sample Python script.
#26216a5f045682b83b9f0d351d639e4e
import sys
import requests
from PyQt5.QtWidgets import( QApplication, QWidget, QLabel, QLineEdit, QPushButton,
                             QVBoxLayout)


from PyQt5.QtCore import Qt
class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter city name", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)
        self.initUI()
    def initUI(self):
        self.setWindowTitle("Akram's Weather App")
        vbox = QVBoxLayout()
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)
        vbox.addWidget(self.get_weather_button)
        self.setLayout(vbox)
        # to center align them horizontally
        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)
        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")
        self.setStyleSheet("""
                QPushButton, QLabel{
                font-family: calibri;}
                QLabel#city_label {
                font-size: 40px;
                font-style: italic;
                }
                QLineEdit#city_input{
                font-size: 40px;}
                QPushButton#get_weather_button {
                font-size: 30px;
                font-weight: bold}
                QLabel#temperature_label {
                font-size: 75px;}
                QLabel#emoji_label {
                font-size: 100px;
                font-family: Segoe UI emoji;}
                QLabel#description_label {
                font-size: 50px;}
                """)
        self.get_weather_button.clicked.connect(self.get_weather)
    def get_weather(self):
        api_key = "26216a5f045682b83b9f0d351d639e4e"
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            #raises an exception if there are any http errors sice try doesnt usually catch those
            data = response.json()
            if data["cod"] == 200:
                self.display_weather(data)
        except requests.exceptions.HTTPError as err:
            if response.status_code == 400:
                self.display_error("please check your input")
            elif response.status_code == 401:
                self.display_error("Unauthorized\nInvalid api key")
            elif response.status_code == 403:
                self.display_error("Forbidden\n access denied")
            elif response.status_code == 404:
                self.display_error("city not found")
            elif response.status_code == 500:
                self.display_error("server error")
            elif response.status_code == 502:
                self.display_error("Bad gateway\nInvalid response from the server")
            elif response.status_code == 503:
                self.display_error("server is down\n Service unavailable")
            elif response == 504:
                self.display_error("Gateway timeout\nNo response from the server")
            else:
                self.display_error(f"HTTP error: {err}")
        except requests.exceptions.ConnectionError as err:
            self.display_error(f"Connection error, check your internet connection and try again later")
        except requests.exceptions.Timeout as err:
            self.display_error("The request timed out")
        except requests.exceptions.TooManyRedirects as err:
            self.display_error("Too many redirects")
        except requests.exceptions.RequestException as req_error:
            self.display_error(f"something went wrong:\n {req_error}")

    def display_error(self, message):
        self.temperature_label.setStyleSheet("font-size: 30px;")
        self.temperature_label.setText(message)
        self.emoji_label.clear()
        self.description_label.clear()
    def display_weather(self, data):
        #resetting the temp each time to make sure its printed correctly
        self.temperature_label.setStyleSheet("font-size: 75px;")
        temp_K = data['main']['temp']
        temp_c = temp_K - 273.15
        weather_id = data['weather'][0]['id']
        weather_desc = data['weather'][0]['description']
        self.temperature_label.setText(f"{temp_c:.1f}°C ")
        self.emoji_label.setText(self.weather_emoji(weather_id))
        self.description_label.setText(weather_desc)
    @staticmethod
    def weather_emoji(weather_id):
#based on the id of the weather key it belongs to a certain group of weather
        if 200 <= weather_id <= 232:
            return "⛈️"
        elif 300 <= weather_id <= 321:
            return "⛅"
        elif 500 <= weather_id <= 531:
            return "🌧️"
        elif 600 <= weather_id <= 622:
            return "🌨️"
        elif 701 <= weather_id <= 741:
            return "🌫️"
        elif weather_id == 762:
            return "🌋"
        elif weather_id == 771:
            return "💨"
        elif weather_id == 781:
            return "🌪️"
        elif weather_id == 800:
            return "🌞"
        elif 801 <= weather_id <= 804:
            return "☁️"
        else:
            return " "

if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())

