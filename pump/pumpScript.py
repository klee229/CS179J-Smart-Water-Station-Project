from gpiozero import LED, Button, OutputDevice
from time import time

# OutputDevice is a generic device, which we can use as the basis
# for a new class, which we will call "relay" and use to control it

#commented lines are for testing purposes

class Relay(OutputDevice):
	def __init__(self, pin, active_high):
		super(Relay, self).__init__(pin, active_high)

def pumpActive(): 
#	print("Running")
	button = Button(14)
	led = LED(15)
	rly = Relay(12,False)
	#print("The button was pressed!")
	button.wait_for_press()
	pushed = time.time()
	led.on()
	rly.on()
	button.wait_for_release()
	led.off()
	rly.off()
	btnPressTime = time.time() - pushed
#	print 'Button was pressed for %.2f seconds' % btnPressTime
	return btnPressTime * 0.0275 # approximate calculation

#def main():
#	wtr = pumpActive()
#	print 'water consumed %.2f L' % wtr
#	exit()

#if __name__ == "__main__":
#    main()
