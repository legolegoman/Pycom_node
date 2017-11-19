""" OTAA Node example compatible with the LoPy Nano Gateway """

from network import LoRa
import socket
import binascii
import struct
import pycom
import time
import config
import machine
from machine import Pin


pycom.heartbeat(False)
pycom.rgbled(0x1f0000) # red

# initialize LoRa in LORAWAN mode.
lora = LoRa(mode=LoRa.LORAWAN)
lora.frequency(915000000)
lora.bandwidth(LoRa.BW_125KHZ)


# create an OTA authentication params
dev_eui = binascii.unhexlify('11 AA BB 22 33 44 FF 88'.replace(' ',''))
app_eui = binascii.unhexlify('70 B3 D5 7E D0 00 7C 77'.replace(' ',''))
app_key = binascii.unhexlify('77 E5 80 10 2E 70 5D 1D 59 AA AF 62 4E F7 98 72'.replace(' ',''))

# set the 3 default channels to the same frequency (must be before sending the OTAA join request)
#lora.add_channel(0, frequency=915000000, dr_min=0, dr_max=3)
#lora.add_channel(1, frequency=915000000, dr_min=0, dr_max=3)
#lora.add_channel(2, frequency=915000000, dr_min=0, dr_max=3)

# remove all the channels
for channel in range(0, 72):
    lora.remove_channel(channel)

time.sleep(0.5)

lora.add_channel(0, frequency=903900000, dr_min=0, dr_max=4)

# set all channels to the same frequency (must be before sending the OTAA join request)
for channel in range(0, 72):
    lora.add_channel(channel, frequency=config.LORA_FREQUENCY, dr_min=0, dr_max=3)
#    lora.add_channel(channel, frequency=903900000, dr_min=0, dr_max=3)

#lora.add_channel(0, frequency=config.LORA_FREQUENCY, dr_min=0, dr_max=3)


time.sleep(1)


# initialize button
button=machine.Pin("G17",machine.Pin.IN, pull=machine.Pin.PULL_UP)
led=machine.Pin('G16',machine.Pin.OUT)
led.toggle()

# join a network using OTAA
lora.join(activation=LoRa.OTAA, auth=(dev_eui, app_eui, app_key), timeout=0, dr=config.LORA_NODE_DR)


# remove all the non-default channels
#for i in range(1, 16):
#    lora.remove_channel(i)

time.sleep(3)

while not lora.has_joined():
    time.sleep(2)
    pycom.rgbled(0x1f0000) # red
    print('Not joined yet...')
    print(lora.frequency() , lora.bandwidth())
#    print(lora.stats())

print('Joined!')
pycom.rgbled(0x001f00) # green

# wait until the module has joined the network

#join_wait = 0
#while True:
#    time.sleep(2.5)
#    if not lora.has_joined():
#        print('Not joined yet...',join_wait)
#        pycom.rgbled(0x1f0000) # red
#        join_wait = join_wait + 1
#        if join_wait == 5:
#            lora.join(activation=LoRa.OTAA, auth=(dev_eui, app_eui, app_key), timeout=0, dr=config.LORA_NODE_DR)
#            join_wait = 0
#    else:
#        print('Joined!')
#        pycom.rgbled(0x001f00) # green
#        break

# create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# set the LoRaWAN data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, config.LORA_NODE_DR)

# make the socket blocking
s.setblocking(False)

time.sleep(5.0)

i = 0


while True:
#    s.send(bytes([0x01, 0x67, 0x00, i, 0x02, 0x00, 0x00, 0x00]))
#    i+=1
    if not button():
        s.send(bytes([0x01, 0x67, 0x00, i, 0x02, 0x00, 0x00, 0x00]))
        s.send(bytes([0x09, 0x09, 0x09]))
        print("help!")
        led.toggle()
        time.sleep(1)
        i = i + 1


#    s.send(b'PKT #' + bytes([0x01, 0x02, 0x03, i]))
#    time.sleep(4)
#    rx, port = s.recvfrom(256)
#    if rx:
#        print('Received: {}, on port: {}'.format(rx, port))
#    time.sleep(6)
