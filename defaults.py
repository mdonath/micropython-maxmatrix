from machine import Pin, SPI
from maxmatrix.font import FONT
from maxmatrix.matrix import Matrix8x8
from maxmatrix.scroller import Scroller


class DefaultScroller(Scroller):
	def __init__(self,maxInUse=5,delay=0):
		spi = SPI(-1, 10000000, miso=Pin(12), mosi=Pin(13), sck=Pin(14))
        	display = Matrix8x8(spi, Pin(2), maxInUse)
        	display.clear()

		Scroller.__init__(self,display,FONT,delay)

