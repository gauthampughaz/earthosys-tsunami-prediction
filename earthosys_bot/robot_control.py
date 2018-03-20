import RPi.GPIO as GPIO
import asyncio
from ubidots import ApiClient


AUTH_TOKEN = "A1E-Jzxt1BSuMNBTwfRcKt0swcS5pJY2FP"
BASE_URL = "http://things.ubidots.com/api/v1.6/"
POWER_ID = "5aae4046c03f97238ee514ca"
BOT_ACTION = "5ab1045cc03f972533944dd7"

bot_action, power = None, None


def init():
    global bot_action, power, AUTH_TOKEN, BASE_URL, BOT_ACTION, POWER_ID
    api = ApiClient(token=AUTH_TOKEN, base_url=BASE_URL)

    bot_action = api.get_variable(BOT_ACTION)
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


async def get_power():
    return power.get_values(1)[0]["value"]


async def get_bot_action():
    return bot_action.get_values(1)[0]["value"]


async def activate():
    while True:
        _power = await get_power()
        while _power == 1:
            GPIO.output(5, GPIO.HIGH)
            GPIO.output(6, GPIO.HIGH)
            _bot_action = await get_bot_action()
            print(_bot_action)
            if _bot_action == 1:
                # Moving right wheel in forward direction
                GPIO.output(4, GPIO.LOW)  # Right motor turns clockwise
                GPIO.output(17, GPIO.HIGH)
                # Moving left wheel in forward direction
                GPIO.output(27, GPIO.HIGH)  # Left motor turns clockwise
                GPIO.output(22, GPIO.LOW)
            elif _bot_action == 2:
                # Moving left wheel in forward direction
                GPIO.output(27, GPIO.HIGH)  # Left motor turns clockwise
                GPIO.output(22, GPIO.LOW)
                # Motor stop/brake
                GPIO.output(4, GPIO.LOW)
                GPIO.output(17, GPIO.LOW)
            elif _bot_action == 3:
                # Moving left wheel in backward direction
                GPIO.output(27, GPIO.LOW)  # Left motor turns anti-clockwise
                GPIO.output(22, GPIO.HIGH)
                # Moving right wheel in backward direction
                GPIO.output(4, GPIO.HIGH)  # Right motor turns anti-clockwise
                GPIO.output(17, GPIO.LOW)
            elif _bot_action == 4:
                # Moving right wheel in forward direction
                GPIO.output(4, GPIO.LOW)  # Right motor turns clockwise
                GPIO.output(17, GPIO.HIGH)
                # Stopping left wheel
                GPIO.output(27, GPIO.LOW)
                GPIO.output(22, GPIO.LOW)
            elif _bot_action == -1:
                # Motor stop/brake
                GPIO.output(4, GPIO.LOW)
                GPIO.output(17, GPIO.LOW)
                GPIO.output(27, GPIO.LOW)
                GPIO.output(22, GPIO.LOW)

            _power = await get_power()
            if _power == 0:  # To deactivate the robot
                GPIO.output(5, GPIO.HIGH)
                GPIO.output(6, GPIO.HIGH)
                GPIO.output(4, GPIO.LOW)
                GPIO.output(17, GPIO.LOW)
                GPIO.output(27, GPIO.LOW)
                GPIO.output(22, GPIO.LOW)


if __name__ == "__main__":
    init()
    event_loop = asyncio.get_event_loop()
    tasks = [activate(), get_power(), get_bot_action()]
    event_loop.run_until_complete(asyncio.gather(*tasks))
    event_loop.close()
