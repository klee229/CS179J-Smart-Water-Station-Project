from gpiozero import Button
print("Running")
button = Button(8)
button.wait_for_press()
print("The button was pressed!")
exit()
