import RPi.GPIO as GPIO
import time
from twilio.rest import Client 
import HelpKeys


def CriticalInterrupt():
    client = Client(HelpKeys.account_sid, HelpKeys.twilio_auth_token)
    message = client.messages.create(
        body = "Urgent Care Requirement",
        from_ = "+1909274092",
        to = "+12268999842",
        )
    print(message.body)

    account_sid = ""
    twilio_auth_token =""

    twilio_number = ""
    desired_receiving_number = ""



ULTRASONIC = {
    "LEFT": {"TRIG": 18, "ECHO": 19},
    "RIGHT": {"TRIG": 22, "ECHO": 23},
    "FRONT": {"TRIG": 24, "ECHO":26},
    "REAR": {"TRIG": 29, "ECHO": 32}
}

BUZZER_PIN = 33

CriticalGyroscopicEventPin = 2

GPIO.setmode(GPIO.BOARD)

GPIO.setup(BUZZER_PIN, GPIO.OUT)


print("GPIO MODE IS SET")


for direction, pins in ULTRASONIC.items():
    print("INSIDE THE ULTRASONIC CONFIG")
    GPIO.setup(pins["TRIG"], GPIO.OUT)
    GPIO.setup(pins["ECHO"], GPIO.IN)

def get_distance(trig_pin, echo_pin):
    GPIO.output(trig_pin, True)
    time.sleep(0.01)
    GPIO.output(trig_pin, False)
    start_time = time.time()
    while(GPIO.input(echo_pin) == 0):
        if(GPIO.input(echo_pin) == 1):
            break
    stop_time = time.time()    
    total_time = stop_time - start_time
    distance = (total_time * 34300) / 2

    return distance


def audioBuzz(delay):
    GPIO.output(BUZZER_PIN, GPIO.HIGH)  # Buzzer on
    time.sleep(delay)
    GPIO.output(BUZZER_PIN, GPIO.LOW)   # Buzzer off
    time.sleep(delay)


def my_callback(CriticalGyroscopicEventPin):


try:
    while True:
        dict= {}
        for direction, pins in ULTRASONIC.items():
            min_dist = 0
            distance = get_distance(pins["TRIG"], pins["ECHO"])
            # Adjust this threshold as required
            print("Checking " + direction + " direction " + " distance: ", distance)
            dict[direction] = distance
            if distance <min_dist:
                distance = min_dist

        direction_least = min(dict, key=dict.get)

        if distance < 10:
            if direction_least == "LEFT":
                audioBuzz(0.1)
            elif direction_least == "RIGHT":
                audioBuzz(0.2)
            elif direction_least == "FRONT":
                audioBuzz(0.3)
            elif direction_least == "REAR":
                audioBuzz(0.4)

        GPIO.setup(pin_number, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        GPIO.add_event_detect(pin_number, GPIO.FALLING, callback=my_callback, bouncetime=200)



        time.sleep(0.1)

except KeyboardInterrupt:
    print("Program stopped by user.")
    GPIO.cleanup()
