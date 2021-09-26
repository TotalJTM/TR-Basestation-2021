from controller import joy_device
from robot_communications import commands
from network import network_sock
from inputs import devices
from timer import Timer
import time

host_ip = '192.168.1.5'
server_port = 12345

class TR_Augerbot_Control:

	def __init__(self):
		self.joystick_max_val = 32767
		self.speed_limit = 10
		self.deadzone = 2

		#Button codes for a logitech gamepad
		#Trigger buttons: BTN_TL, BTN_TR, ABS_Z, ABS_RZ
		#Gamepad buttons: BTN_WEST, BTN_NORTH, BTN_SOUTH, BTN_EAST
		#Select/start 	: BTN_SELECT, BTN_START
		#Joy Pad 		: ABS_HAT0X, ABS_HAT0Y
		#Joysticks		: ABS_X, ABS_Y, ABS_RX, ABS_RY

		self.left_drive_stick = 'ABS_Y'
		self.right_drive_stick = 'ABS_RY'
		self.auger_lift_btn = 'BTN_TR'
		self.auger_slide_btn = 'BTN_NORTH'
		self.auger_drive_btn = 'BTN_EAST'
		self.belt_lift_btn = 'BTN_SOUTH'
		self.belt_drive_btn = 'BTN_WEST'
		self.up_down_btn = 'ABS_HAT0Y'
		self.stop_btn = 'ABS_HAT0X'
		#self._btn = ''

		self.left_drive_stick_val = 0
		self.right_drive_stick_val = 0
		self.auger_lift_btn_val = 0
		self.auger_slide_btn_val = 0
		self.auger_drive_btn_val = 0
		self.belt_lift_btn_val = 0
		self.belt_drive_btn_val = 0
		self.up_btn_val = 0
		self.down_btn_val = 0
		self.stop_btn_val = 0
		#self._val = 0

		self.left_drive_state = 0
		self.right_drive_state = 0
		self.auger_lift_state = 0
		self.auger_slide_state = 0
		self.auger_drive_state = 0
		self.belt_lift_state = 0
		self.belt_drive_state = 0

	def normalize_joy(self, val):
	    #NewValue = (((OldValue - OldMin) * (NewMax - NewMin)) / (OldMax - OldMin)) + NewMin
	    newval = (((val+self.joystick_max_val)*(self.speed_limit*2))/(2*self.joystick_max_val))-self.speed_limit
	    #print(newval)
	    if -self.deadzone < newval < self.deadzone:
	        return 0
	    else:
	        return newval

	#function to generate JSON message from new controller input
	#takes an array of controller values, returns an empty arr (if no new string necessary) or a formatted string
	#that can be sent to the robot
	def generate_JSON_from_controller_input(self, new_button_vals):
		pay_pack = []

		#move through the new button values
		for event in new_button_vals:

			if event["event"] == self.left_drive_stick:
				self.left_drive_stick_val = self.normalize_joy(int(event["value"]))
				self.left_drive_state = self.left_drive_stick_val
				for item in commands.motor(left_motor_val=self.left_drive_stick_val):
					pay_pack.append(item)

			if event["event"] == self.right_drive_stick:
				self.right_drive_stick_val = self.normalize_joy(int(event["value"]))
				self.right_drive_state = self.right_drive_stick_val
				for item in commands.motor(right_motor_val=self.right_drive_stick_val):
					pay_pack.append(item)

			if event["event"] == self.auger_lift_btn:
				self.auger_lift_btn_val = event["value"]
				if self.auger_lift_btn_val == 1:
					if self.stop_btn_val == 1:
						self.auger_lift_state = 0
					elif self.up_btn_val == 1:
						self.auger_lift_state = 1
					elif self.down_btn_val == 1:
						self.auger_lift_state = 2
					else:
						pass

					for item in commands.auger_lift(self.auger_lift_state):
						pay_pack.append(item)

			if event["event"] == self.auger_slide_btn:
				self.auger_slide_btn_val = event["value"]
				if self.auger_slide_btn_val == 1:
					if self.stop_btn_val == 1:
						self.auger_slide_state = 0
					elif self.up_btn_val == 1:
						self.auger_slide_state = 2
					elif self.down_btn_val == 1:
						self.auger_slide_state = 1
					else:
						pass

					for item in commands.auger_slide(self.auger_slide_state):
						pay_pack.append(item)

			if event["event"] == self.auger_drive_btn:
				self.auger_drive_btn_val = event["value"]
				if self.auger_drive_btn_val == 1:
					if self.stop_btn_val == 1:
						self.auger_drive_state = 0
					elif self.up_btn_val == 1:
						self.auger_drive_state = 1
					elif self.down_btn_val == 1:
						self.auger_drive_state = 2
					else:
						pass

					for item in commands.auger_drive(self.auger_drive_state):
						pay_pack.append(item)

			if event["event"] == self.belt_lift_btn:
				self.belt_lift_btn_val = event["value"]
				if self.belt_lift_btn_val == 1:
					if self.stop_btn_val == 1:
						self.belt_lift_state = 0
					elif self.up_btn_val == 1:
						self.belt_lift_state = 1
					elif self.down_btn_val == 1:
						self.belt_lift_state = 2
					else:
						pass

					for item in commands.belt_lift(self.belt_lift_state):
						pay_pack.append(item)

			if event["event"] == self.belt_drive_btn:
				self.belt_drive_btn_val = event["value"]
				if self.belt_drive_btn_val == 1:
					if self.stop_btn_val == 1:
						self.belt_drive_state = 0
					elif self.up_btn_val == 1:
						self.belt_drive_state = 1
					elif self.down_btn_val == 1:
						self.belt_drive_state = 2
					else:
						pass

					for item in commands.belt_drive(self.belt_drive_state):
						pay_pack.append(item)

			if event["event"] == self.up_down_btn:
				if event["value"] == 0:
					self.up_btn_val = 0
					self.down_btn_val = 0
				if event["value"] == 1:
					self.up_btn_val = 1
					self.down_btn_val = 0
				if event["value"] == -1:
					self.up_btn_val = 0
					self.down_btn_val = 1

			if event["event"] == self.stop_btn:
				if event["value"] == 0:
					self.stop_btn_val = 0
				if event["value"] == -1:
					self.stop_btn_val = 1

		return pay_pack


if __name__ == "__main__":
	try:
		s = network_sock()
		s.connect(host=host_ip, port=server_port)

		print(f'Connected to {host_ip}')
	except:
		print(f'Could not connect to {host_ip}')

	cmd_line_timer = Timer(0.25)
	cmd_line_timer.start()
	try:
		joy = joy_device(devices.gamepads[0])
		joy.start_gamepad_thread()
	except:
		print("No gamepads connected")

	trac = TR_Augerbot_Control()

	try:

		while s.sock != None:

			events = joy.pop_gamepad_queue()
			#print(len(events))
			#print(events)

			pay_pack = trac.generate_JSON_from_controller_input(events)

			#print(pay_pack)
			if len(pay_pack) > 0:
				#print(commands.format_arr(pay_pack))
				s.send(commands.format_arr(pay_pack))

			time.sleep(.0001)

			if cmd_line_timer.check_timer():
				print(f'Speed L:{trac.left_drive_state} R:{trac.right_drive_state}, Auger Lift: {trac.auger_lift_state}, Auger Slide: {trac.auger_slide_state}, Auger Drive: {trac.auger_drive_state}, Belt Lift: {trac.belt_lift_state}, Belt Drive: {trac.belt_drive_state}')
				cmd_line_timer.start()


	except:  # this never happens KeyboardInterrupt
		print("Script aborted")
		joy.stop_thread()
		print("joy stopped")
		abcd_1234()
		s.send(commands.format_arr(commands.stop()))
		print("socket sent")
		s.close()
		print("socket close")
		
		#sys.exit(0)
		terminate()
		print("reached end")
		abcd_1234()