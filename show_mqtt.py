from time import sleep_ms
from umqtt.simple import MQTTClient

from defaults import DefaultScroller as Scroller

scroller = None

def mqtt_cb(topic, msg):
	topic = topic.decode('ASCII')
	msg = msg.decode('ASCII')

	if topic == 'led-scroller/brightness':
		scroller.brightness(int(msg))
	elif topic == 'led-scroller/scroll':
		scroller.scroll(msg)
		scroller.clear_left()
	elif topic == 'led-scroller/message':
		scroller.scroll(msg)
	elif topic == 'stat/switch2/POWER':
		scroller.scroll('lamp ' + str(msg))
		scroller.clear_down()

def show_mqtt():
	global scroller
	scroller = Scroller()

	mqtt = MQTTClient(b"scroller", b"mqtt")
	try:
		mqtt.connect()
	except:
		scroller.scroll("MQTT connect failed")
		return

	mqtt.set_callback(mqtt_cb)
	mqtt.subscribe(b"#")

	scroller.scroll("started")
	scroller.clear_up()
	try:
		while True:
			mqtt.wait_msg()
	finally:
		mqtt.disconnect()

