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


def register_buttons():
    for a in config['actions']:
        GPIO.setup(a['button_pin'], GPIO.IN, pull_up_down=GPIO.PUD_UP)

        def action(pin):
            api_url = a['api_url']
            api_method = a['api_method']
            api_data = a['api_data']

            print(api_data)

            if api_method in ["POST", "PUT"]:
                try:
                    if a['use_json']:
                        api_data = json.dumps(api_data)
                except KeyError:
                    pass
                response = REQUESTS[api_method](api_url, data=api_data)
            else:
                response = REQUESTS[api_method](api_url)

            if response.status_code in SUCCESS_CODES:
                flash_led(config['success_pin'])
            else:
                flash_led(config['failure_pin'])

        GPIO.add_event_detect(a['button_pin'], GPIO.FALLING, callback=action, bouncetime=300)
