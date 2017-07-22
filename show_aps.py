from time import sleep_ms
from defaults import DefaultScroller as Scroller

def show_accesspoints():
	scroller = Scroller()

	import network

	sleep_ms(2000)
	wlan = network.WLAN(network.STA_IF)
	wlan.active(True)
	
	while True:
		scroller.scroll("scan...")
		list = wlan.scan()
		scroller.clear_down()
		scroller.scroll("found: "+ str(len(list)))
		sleep_ms(1000)
		scroller.clear_down()

		for idx, network in enumerate(list):
			scroller.scroll(str(idx+1) + ": "+network[0].decode('ascii'))
			sleep_ms(1000)
			scroller.clear_up()

