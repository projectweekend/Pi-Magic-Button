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


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
with open('./config.yml') as file_data:
    config = yaml.safe_load(file_data)


def report_success():
    GPIO.output(config['success_pin'], GPIO.HIGH)
    sleep(3)
    GPIO.output(config['success_pin'], GPIO.LOW)


def report_failure():
    GPIO.output(config['failure_pin'], GPIO.HIGH)
    sleep(3)
    GPIO.output(config['failure_pin'], GPIO.LOW)


def call_api():
    api_url = config['api_url']
    api_method = config['api_method']
    response = REQUESTS[api_method](api_url)
    if response.status_code in SUCCESS_CODES:
        report_success()
    else:
        report_failure()


def main():
    GPIO.setup(config['success_pin'], GPIO.OUT)
    GPIO.setup(config['failure_pin'], GPIO.OUT)
    GPIO.setup(config['button_pin'], GPIO.IN, pull_up_down=GPIO.PUD_UP)
    while True:
        GPIO.wait_for_edge(config['button_pin'], GPIO.FALLING)
        call_api()


if __name__ == '__main__':
    main()
