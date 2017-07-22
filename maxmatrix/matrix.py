_NOOP=const(0)
_DIGIT0=const(1)
_DIGIT1=const(2)
_DIGIT2=const(3)
_DIGIT3=const(4)
_DIGIT4=const(5)
_DIGIT5=const(6)
_DIGIT6=const(7)
_DIGIT7=const(8)
_DECODEMODE=const(9)
_INTENSITY=const(10)
_SCANLIMIT=const(11)
_SHUTDOWN=const(12)
_DISPLAYTEST=const(15)

class Matrix8x8:
	def __init__(self,spi,cs,num):
		self.spi=spi
		self.cs=cs
		self.cs.init(cs.OUT,True)
		self.num=num
		self.buffer=bytearray(80)
		self.init()

	def init(self):
		for cmd,data in (
			(_SCANLIMIT,7),
			(_DECODEMODE,0),
			(_SHUTDOWN,1),
			(_DISPLAYTEST,0),
		):
			self._cmd(cmd,data)
		self.clear()
		self.intensity(0)

	def intensity(self,val):
		if not 0<=val<=15:
			raise ValueError("Brightness out of range")
		self._cmd(_INTENSITY,val)

	def clear(self):
		for i in range(8):
			self.columnAll(i,0x00)
		for i in range(80):
			self.buffer[i]=0
	
	def column(self,col,val):
		n=int(col/8)
		c=int(col%8)
		self._start()
		for i in range(self.num):
			if i==n:
				self._write(c+1,val)
			else:
				self._write(0,0)
		self._stop()
		self.buffer[col]=val

	def columnAll(self,col,val):
		self._start()
		for i in range(self.num):
			self._write(col+1,val)
			self.buffer[col*i]=val
		self._stop()

	def dot(self,col,row,val):
		self._bitwrite(col,row,val)
		n=int(col/8)
		c=int(col%8)
		self._start()
		for i in range(self.num):
			if i==n:
				self._write(c+1,self.buffer[col])
			else:
				self._write(0,0)
		self._stop()

	def sprite(self,x,y,spr):
		w=spr[0]
		h=spr[1]
		if h==8 and y==0:
			for i in range(w):
				c=x+i
				if 0<=c<80:
					self.column(c,spr[i+2])
		else:
			for i in range(w):
				for j in range(h):
					c=x+i
					r=y+j
					if 0<=c<80 and 0<=r<8:
						self.dot(c,r,(spr[i+2]>>j)&0x01)

	def reload(self):
		for i in range(8):
			col=i
			self._start()
			for j in range(self.num):
				self._write(i+1,self.buffer[col])
				col+=8
			self._stop()

	def shift_left(self,rotate=False,fill_zero=False):
		old=self.buffer[0]
		for i in range(79):
			self.buffer[i]=self.buffer[i+1]
		if rotate:
			self.buffer[self.num*8-1]=old
		elif fill_zero:
			self.buffer[self.num*8-1]=0
		self.reload()

	def shift_right(self,rotate=False,fill_zero=False):
		last=self.num*8-1
		old=self.buffer[last]
		for i in range(79,0,-1):
			self.buffer[i]=self.buffer[i-1]
		if rotate:
			self.buffer[0]=old
		elif fill_zero:
			self.buffer[0]=0
		self.reload()

	def shift_up(self,rotate=False):
		for i in range(self.num*8):
			b=self.buffer[i] & 0x01
			self.buffer[i]>>=1
			if rotate:
				self._bitwrite(i,7,b)
		self.reload()

	def shift_down(self,rotate=False):
		for i in range(self.num*8):
			b=self.buffer[i]&0x80
			self.buffer[i]<<=1
			if rotate:
				self._bitwrite(i,0,b)
		self.reload()

	def _cmd(self,cmd,val):
		self._start()
		for i in range(self.num):		
			self._write(cmd,val)
		self._stop()

	def _start(self):
		self.cs.off()

	def _stop(self):
		self.cs.off()
		self.cs.on()

	def _write(self,cmd,val):
		self.spi.write(bytearray([cmd,val]))

	def _bitwrite(self,col,row,val):
		if val:
			self.buffer[col] |= 1 << row
		else:
			self.buffer[col] &= ~(1 << row)

