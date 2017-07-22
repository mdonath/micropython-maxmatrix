from time import sleep_ms

class Scroller:
	def __init__(self,display,font,maxInUse=4,delay=0):
		self.display=display
		self.font=font
		self.delay=delay
		self.maxInUse=maxInUse
		self.maxNumber=maxInUse*8

	def brightness(self,value):
		self.display.intensity(value)
		self.scroll(str(value))
		sleep_ms(500)
		self.clear_down()

	def scroll(self,s):
		for c in s:
		    self.scroll_char(c)

	def clear(self):
		self.display.clear()

	def clear_left(self):
		for i in range(self.maxNumber):
			sleep_ms(self.delay)
			self.display.shift_left()

	def clear_up(self):
		for i in range(8):
			sleep_ms(self.delay)
			self.display.shift_up()

	def clear_down(self):
		for i in range(8):
			sleep_ms(self.delay)
			self.display.shift_down()

	def scroll_char(self,c):
		ch=ord(c)-32
		if ch<0 or ch>=len(self.font):
		    return
		buffer=self.font[ch]
		self.display.sprite(self.maxNumber,0,buffer)
		width=buffer[0]
		self.display.column(self.maxNumber+width,0)
		for i in range(width+1):
			sleep_ms(self.delay)
			self.display.shift_left()

