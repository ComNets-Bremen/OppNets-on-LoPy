# A simple  program that implements the functionality of an opportunistic
# networking node on a PyCom (LoPy with LoRa) using the RRS forwarding
# protocol. It consist of the following modules (protocol layers).
#
# - app - application layer
# - rrs - RRS forwarding layer
# - link - link based on LoRa
#
# @author: Asanga Udugama (adu@comnets.uni-bremen.de)
# @date: 10-jun-2020
#

import pycom
import gc
import os
import _thread
import machine
import common
import app
import rrs
import link
import time
import settings

# basic initializations
time.sleep(2)
gc.enable()
pycom.heartbeat(False)

# initialize environment
common.initialize()
app.initialize()
rrs.initialize()
link.initialize()

# activate all layers
app.start()
rrs.start()
link.start()

# wait endlessly while the threads do their work
while True:

    # loop with a pause
    time.sleep(5)
