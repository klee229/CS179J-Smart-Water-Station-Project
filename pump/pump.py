from gpiozero import LED, Button, OutputDevice
import time

# OutputDevice is a generic device, which we can use as the basis
# for a new class, which we will call "relay" and use to control it

# commented lines are for testing purposes


class Relay(OutputDevice):
	def __init__(self, pin, active_high):
		super(Relay, self).__init__(pin, active_high)


def pump_active(): 
	print("Running")
	button = Button(14)
	led = LED(15)
	rly = Relay(12, False)
	# print("The button was pressed!")
	button.wait_for_press()
	pushed = time.time()
	led.on()
	rly.on()
	button.wait_for_release()
	led.off()
	rly.off()
	btn_press_time = time.time() - pushed
	print('Button was pressed for {:.2f} seconds'.format(btn_press_time))
	return btn_press_time * 0.0275  # approximate calculation


if __name__ == '__main__':
	wtr = pump_active()
	print("Water consumed: {:.2f} L".format(wtr))
