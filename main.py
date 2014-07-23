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


def flash_led(pin):
    GPIO.output(pin, GPIO.HIGH)
    sleep(3)
    GPIO.output(pin, GPIO.LOW)


def register_actions():
    for k, v in config['actions'].iteritems():
        GPIO.setup(v['button_pin'], GPIO.IN, pull_up_down=GPIO.PUD_UP)

        def call_api(pin):
            api_url = v['api_url']
            api_method = v['api_method']
            api_data = v['api_data']

            if api_method in ["POST", "PUT"]:
                response = REQUESTS[api_method](api_url, data=api_data)
            else:
                response = REQUESTS[api_method](api_url)

            if response.status_code in SUCCESS_CODES:
                flash_led(config['success_pin'])
            else:
                flash_led(config['failure_pin'])

        GPIO.add_event_detect(v['button_pin'], GPIO.FALLING, callback=call_api, bouncetime=300)



def main():
    try:
        GPIO.setup(config['success_pin'], GPIO.OUT)
        GPIO.setup(config['failure_pin'], GPIO.OUT)
        register_actions()

        while True:
            pass
    except:
        GPIO.cleanup()


if __name__ == '__main__':
    main()
