from gpiozero import Button
from time import sleep

# Raspberry Pi BCM gpio pin number
dispense_pin = 14

dispense_btn = Button(dispense_pin)


def press_button():
    for x in range(100):
        if dispense_btn.is_pressed:
            print("dispense button pressed")
        else:
            print("dispense button NOT pressed")

        sleep(0.1)


if __name__ == '__main__':
    press_button()
