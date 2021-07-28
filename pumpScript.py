from gpiozero import LED, Button, OutputDevice
from signal import pause

# OutputDevice is a generic device, which we can use as the basis
# for a new class, which we will call "relay" and use to control it

class Relay(OutputDevice):
	def __init__(self, pin, active_high):
		super(Relay, self).__init__(pin, active_high)


print("Running")
button = Button(8)
led = LED(7)
rly = Relay(12,False)
#button.wait_for_press()
#print("The button was pressed!")
button.when_pressed = led.on
button.when_pressed = rly.on
button.when_released = led.off
button.when_released = rly.off
print('Button was pressed for', button.held_time)
pause()
