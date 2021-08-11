from gpiozero import LED, Button, OutputDevice
from time import sleep

# OutputDevice is a generic device, which we can use as the basis
# for a new class, which we will call "relay" and use to control it

# commented lines are for testing purposes


class Relay(OutputDevice):
    def __init__(self, pin, active_high):
        super(Relay, self).__init__(pin, active_high)


def pump_active():
    print("Running")
    led = LED(15)
    rly = Relay(12, False)
    sleep(10)
    led.on()
    rly.on()
    sleep(5)
    led.off()
    rly.off()
    btn_press_time = 5
    print('Button was pressed for %.2f seconds' % btn_press_time)
    return btn_press_time * 0.0275  # approximate calculation


def main():
    wtr = pump_active()
    print('water consumed %.2f L' % wtr)
    exit()


if __name__ == '__main__':
    main()
