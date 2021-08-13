from gpiozero import LED, Button, OutputDevice
import pandas as pd
import time

# OutputDevice is a generic device, which we can use as the basis
# for a new class, which we will call "relay" and use to control it

# commented lines are for testing purposes


class Relay(OutputDevice):
	def __init__(self, pin, active_high):
		super(Relay, self).__init__(pin, active_high)


class Pump:

	def __init__(self):
		self.has_dispensed = False
		self.last_amount = 0.0
		
	def dispense_water(self, container, refil_bool):
		temp_amount = self.pump_active()
		print(temp_amount)
		
		if refil_bool == True:
			temp_amount -= 0.0825
		
		# pump_uid = container.get_card_uid()
		pump_uid = "734a266f" # For no hardware testing only
		
		df = pd.read_csv(container.file_path)
		
		row_num = df.index[df['card_uid'] == pump_uid].tolist()
		
		df.at[row_num[0], 'water_dispensed'] += temp_amount
		df.at[row_num[0], 'total_dispensed'] += temp_amount
		
		df.to_csv(container.file_path, index=False) 		# use? may or may not need
		self.has_dispensed = True
		self.last_amount = temp_amount
		
	def pump_active(self): 
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
	pump = Pump()
	wtr = pump.pump_active()
	print("Water consumed: {:.2f} L".format(wtr))
