""" OTAA Node example compatible with the LoPy Nano Gateway """

from network import LoRa
import socket
import binascii
import struct
import pycom
import time
import config


pycom.heartbeat(False)
pycom.rgbled(0x7f0000) # red

# initialize LoRa in LORAWAN mode.
lora = LoRa(mode=LoRa.LORAWAN)

# create an OTA authentication params
dev_eui = binascii.unhexlify('11 AA BB 22 33 44 FF 88'.replace(' ',''))
app_eui = binascii.unhexlify('70 B3 D5 7E D0 00 7C 77'.replace(' ',''))
app_key = binascii.unhexlify('AF 45 15 46 6D 73 8D B7 46 98 46 68 54 22 65 EE'.replace(' ',''))

# remove all the channels
for channel in range(0, 72):
    lora.remove_channel(channel)

# set all channels to the same frequency (must be before sending the OTAA join request)
for channel in range(0, 72):
    lora.add_channel(channel, frequency=config.LORA_FREQUENCY, dr_min=0, dr_max=3)

# join a network using OTAA
lora.join(activation=LoRa.OTAA, auth=(dev_eui, app_eui, app_key), timeout=0, dr=config.LORA_NODE_DR)

# wait until the module has joined the network
join_wait = 0
while True:
    time.sleep(2.5)
    if not lora.has_joined():
        print('Not joined yet...')
        join_wait += 1
        if join_wait == 5:
            lora.join(activation=LoRa.OTAA, auth=(dev_eui, app_eui, app_key), timeout=0, dr=config.LORA_NODE_DR)
            join_wait = 0
    else:
        print('Joined!')
        pycom.rgbled(0x00ff00) # green
        break

# create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# set the LoRaWAN data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, config.LORA_NODE_DR)

# make the socket blocking
s.setblocking(False)

time.sleep(5.0)

for i in range (200):
    s.send(bytes([0x00, 0x67, 0x00, i, 0x01, 0x00, 0x00, 0x00]))
#    s.send(b'PKT #' + bytes([0x01, 0x02, 0x03, i]))
    time.sleep(4)
    rx, port = s.recvfrom(256)
    if rx:
        print('Received: {}, on port: {}'.format(rx, port))
    time.sleep(6)
