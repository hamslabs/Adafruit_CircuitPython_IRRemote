# Circuit Playground Express Demo Code
# Adjust the pulseio 'board.PIN' if using something else
import time
import pulseio
import board
import digitalio
import adafruit_irremote

pulsein = pulseio.PulseIn(board.REMOTEIN, maxlen=120, idle_state=True)
decoder = adafruit_irremote.GenericDecode()

led = digitalio.DigitalInOut(board.D13)
led.switch_to_output()

button = digitalio.DigitalInOut(board.BUTTON_A)
button.switch_to_input(pull=digitalio.Pull.DOWN)


try:
	with open("/irData", 'w') as fp:
		done = False
		while not done:
			try:
				pulses = decoder.read_pulses(pulsein)
			except adafruit_irremote.IRDecodeException as e:
				print('failed read_pulses with ', e)
			else:
				fp.write("Heard {} pulses {}\n".format(len(pulses), pulses))
	
			try:
				code = decoder.decode_bits(pulses)
			except adafruit_irremote.IRDecodeException as e:
				print('failed decode_bits with ', e)
			else:
				fp.write("bits: {}\n".format(code))
	
			try:
				data = decoder.bin_data(pulses)
			except adafruit_irremote.IRDecodeException as e:
				print('failed bin_data with ', e)
			else:
				fp.write("data: {}\n".format(data))

			led.value = True
			time.sleep(0.3)
			led.value = False

			fp.flush()

			if button.value:
				done = True

except OSError as e:
	delay = 1.0
	if e.args[0] == 28:
		delay = 0.5
	while True:
		led.value = not led.value
		time.sleep(delay)


while True:
	led.value = not led.value
	time.sleep(0.1)

