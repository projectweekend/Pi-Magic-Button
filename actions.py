import json
import yaml
import requests
import RPi.GPIO as GPIO
from time import sleep


REQUESTS = {
    "GET": requests.get,
    "POST": requests.post,
    "PUT": requests.put,
    "DELETE": requests.delete
}
SUCCESS_CODES = [200, 201, 204]


with open('./config.yml') as file_data:
    config = yaml.safe_load(file_data)


def flash_led(pin):
    GPIO.output(pin, GPIO.HIGH)
    sleep(3)
    GPIO.output(pin, GPIO.LOW)


def register_feedback_pins():
    try:
        GPIO.setup(config['success_pin'], GPIO.OUT)
        GPIO.setup(config['failure_pin'], GPIO.OUT)
    except KeyError:
        pass


def build_callback(url, method, data, use_json):

    if use_json:
        data = json.dumps(data)

    def action(pin):
        if method in ["POST", "PUT"]:
            response = REQUESTS[method](url, data=data)
        else:
            response = REQUESTS[method](url)

        if response.status_code in SUCCESS_CODES:
            flash_led(config['success_pin'])
        else:
            flash_led(config['failure_pin'])

    return action


def register_buttons():
    for a in config['actions']:
        button_pin = a['button_pin']
        api_url = a['api_url']
        api_method = a['api_method']
        api_data = a['api_data']
        try:
            use_json = a['use_json']
        except KeyError:
            use_json = False

        GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        callback = build_callback(api_url, api_method, api_data, use_json)

        GPIO.add_event_detect(button_pin, GPIO.FALLING, callback=callback, bouncetime=300)
