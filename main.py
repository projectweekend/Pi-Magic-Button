import actions
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


def main():
    try:
        actions.register_feedback_pins()
        actions.register_buttons()
        while True:
            pass
    except:
        GPIO.cleanup()


if __name__ == '__main__':
    main()
