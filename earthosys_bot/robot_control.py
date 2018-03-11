import RPi.GPIO as GPIO
from ubidots import ApiClient
import time


AUTH_TOKEN = "A1E-UsywjfLkee7rmtKzWqIzCdUHE9n7YH"
BASE_URL = "https://things.ubidots.com/api/v1.6/"
POWER_ID = "5aa574bac03f976ead63ac3a"
LEFT_WHEEL_ID = "5a961dddc03f972cb843c63b"
RIGHT_WHEEL_ID = "5a9622b6c03f972f9cb5dfa5"

left_wheel, right_wheel, power = None, None, None


def init():
    global left_wheel, right_wheel, power, AUTH_TOKEN, BASE_URL, LEFT_WHEEL_ID, RIGHT_WHEEL_ID, POWER_ID
    api = ApiClient(token=AUTH_TOKEN, base_url=BASE_URL)

    left_wheel = api.get_variable(LEFT_WHEEL_ID)
    right_wheel = api.get_variable(RIGHT_WHEEL_ID)
    power = api.get_variable(POWER_ID)

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(4, GPIO.OUT)  # Left motor input A
    GPIO.setup(17, GPIO.OUT)  # Left motor input B
    GPIO.setup(27, GPIO.OUT)  # Right motor input A
    GPIO.setup(22, GPIO.OUT)  # Right motor input B
    GPIO.setup(5, GPIO.OUT)
    GPIO.setup(6, GPIO.OUT)

    # Motor stop/brake
    GPIO.output(4, GPIO.LOW)
    GPIO.output(17, GPIO.LOW)
    GPIO.output(27, GPIO.LOW)
    GPIO.output(22, GPIO.LOW)


def get_power():
    return power.get_values(1)[0]["value"]


def get_wheels_control():
    return left_wheel.get_values(1)[0]["value"], right_wheel.get_values(1)[0]["value"]


def activate():
    while True:
        _power = get_power()
        while _power == 1:
            GPIO.output(5, GPIO.HIGH)
            GPIO.output(6, GPIO.HIGH)
            _left_wheel, _right_wheel = get_wheels_control()
            if _left_wheel == 1:
                # Moving left wheel in forward direction
                GPIO.output(27, GPIO.HIGH)  # Left motor turns clockwise
                GPIO.output(22, GPIO.LOW)
            elif _left_wheel == 0:
                # Moving left wheel in backward direction
                GPIO.output(27, GPIO.LOW)  # Left motor turns anti-clockwise
                GPIO.output(22, GPIO.HIGH)
            if _right_wheel == 0:
                # Moving right wheel in backward direction
                GPIO.output(4, GPIO.HIGH)  # Right motor turns anti-clockwise
                GPIO.output(17, GPIO.LOW)
            elif _right_wheel == 1:
                # Moving right wheel in forward direction
                GPIO.output(4, GPIO.LOW)  # Right motor turns clockwise
                GPIO.output(17, GPIO.HIGH)
            time.sleep(2)
            #if _left_wheel == -1 or _right_wheel == -1:
            # Motor stop/brake
            GPIO.output(4, GPIO.LOW)
            GPIO.output(17, GPIO.LOW)
            GPIO.output(27, GPIO.LOW)
            GPIO.output(22, GPIO.LOW)

            _power = get_power()
            if _power == 0:  # To deactivate the robot
                GPIO.output(5, GPIO.HIGH)
                GPIO.output(6, GPIO.HIGH)
                GPIO.output(4, GPIO.LOW)
                GPIO.output(17, GPIO.LOW)
                GPIO.output(27, GPIO.LOW)
                GPIO.output(22, GPIO.LOW)
                time.sleep(2)


if __name__ == "__main__":
    init()
    activate()
