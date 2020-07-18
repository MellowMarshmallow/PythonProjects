#!/usr/bin/env python

import subprocess
import time

def convert_to_seconds(amount, unit):
    if unit == "sec":
        return amount
    elif unit == "min":
        return amount * 60
    elif unit == "hour":
        return amount * 3600

    return None

def print_notification(amount, unit):
    if not unit in ["sec", "min", "hour"]:
        return

    if unit == "sec":
        unit = "seconds" if amount > 1 else "second"
    elif unit == "min":
        unit = "minutes" if amount > 1 else "minute"
    elif unit == "hour":
        unit = "hours"   if amount > 1 else "hour"

    print(f"Setting alarm for {amount} {unit}")

def call_sleep_method(seconds):
    time.sleep(seconds)

def output_sound():
    try:
        subprocess.run(["mpg123", "alarm_sound.mp3"], capture_output=False)
    except:
        print("Exception while outputting sound")

if __name__ == "__main__":
    while True:
        amount = input("Amount (integer/float value): ")
        unit = input("Unit (sec, min, or hour): ").lower()

        try:
            amount = float(amount)
        except ValueError:
            print("Enter an integer/float")
            continue

        if not unit in ["sec", "min", "hour"]:
            print("Enter 'sec', 'min', or 'hour'")
            continue

        seconds = convert_to_seconds(amount, unit)

        if seconds is not None:
            print_notification(amount, unit)
            call_sleep_method(seconds)
            output_sound()

        break
