#  Copyright (c) 2024. Yoppy Yunhasnawa, Politeknik Negeri Malang.
#  This software is available under the MIT License.
#  Contact me at: yunhasnawa@polinema.ac.id.

from MacScanner import MacScanner
import time
import RPi.GPIO as GPIO

scanner: MacScanner

# Initialize RGB LED pins
RED_PIN = 4
GREEN_PIN = 27
BLUE_PIN = 22
GPIO.setmode(GPIO.BCM)
GPIO.setup(RED_PIN, GPIO.OUT)
GPIO.setup(GREEN_PIN, GPIO.OUT)
GPIO.setup(BLUE_PIN, GPIO.OUT)

def update_status(status):
    if status == "Scanning":
        GPIO.output(RED_PIN, GPIO.HIGH)
        GPIO.output(GREEN_PIN, GPIO.LOW)
        GPIO.output(BLUE_PIN, GPIO.LOW)
    elif status == "Uploading":
        GPIO.output(RED_PIN, GPIO.LOW)
        GPIO.output(GREEN_PIN, GPIO.HIGH)
        GPIO.output(BLUE_PIN, GPIO.LOW)
    elif status == "Idle":
        GPIO.output(RED_PIN, GPIO.LOW)
        GPIO.output(GREEN_PIN, GPIO.LOW)
        GPIO.output(BLUE_PIN, GPIO.HIGH)
    elif status == "Error":
        GPIO.output(RED_PIN, GPIO.HIGH)
        GPIO.output(GREEN_PIN, GPIO.LOW)
        GPIO.output(BLUE_PIN, GPIO.HIGH)

def setup():
    endpoint = 'https://asia-southeast2-lecturer-attending.cloudfunctions.net/pymacscannerEndpoint'
    ip_range = '192.168.66.0/24'
    global scanner
    scanner = MacScanner(endpoint, ip_range)

def loop():
    update_status("Scanning")
    scan_output = scanner.scan()
    if scan_output == 0:
        update_status("Uploading")
        upload_output = scanner.upload()
        if upload_output == 0:
            update_status("Idle")
            print(scanner.upload_result)
        else:
            update_status("Error")
            print("[ERROR] Upload failed!")
    else:
        update_status("Error")
        print("[ERROR] Scan failed!")
    wait(10000)

def wait(ms):
    print("Waiting for {} ms".format(ms))
    time.sleep(ms / 1000)

def main():
    setup()
    while True:
        loop()

if __name__ == "__main__":
    main()
