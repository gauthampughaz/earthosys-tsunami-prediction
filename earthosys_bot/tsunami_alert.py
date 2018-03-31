from ubidots import ApiClient
from gtts import gTTS
import os

AUTH_TOKEN = "A1E-Jzxt1BSuMNBTwfRcKt0swcS5pJY2FP"
BASE_URL = "http://things.ubidots.com/api/v1.6/"
TSUNAMI_ID = "5aae46c0c03f972c1f33077b"
ALERT_MESSAGE = "A tsunamigenic earthquake is approaching us, please turn to safer place."
FILE_NAME = "./alert.mp3"
LANGUAGE = "en-au"

tsunami_alert = None


def init():
    global AUTH_TOKEN, BASE_URL, TSUNAMI_ID, tsunami_alert, ALERT_MESSAGE, FILE_NAME, LANGUAGE
    api = ApiClient(token=AUTH_TOKEN, base_url=BASE_URL)

    tsunami_alert = api.get_variable(TSUNAMI_ID)
    tts_message = gTTS(text=ALERT_MESSAGE, lang=LANGUAGE)
    tts_message.save(FILE_NAME)


def check_tsunami_status():
    _val = int(tsunami_alert.get_values(1)[0]["value"])
    print(_val)

    if _val == 1:
        os.system("mpg123 " + FILE_NAME)
        tsunami_alert.save_value({"value": 0})



if __name__ == "__main__":
    init()