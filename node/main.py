# A simple  program that implements the functionality of an opportunistic
# networking node on a PyCom (LoPy with LoRa) using a 3-layer protocol
# architecture. It consist of the following protocol layers.
#
# - app - application layer (e.g., simpleapp)
# - fwd - forwarding layer (e.g., rss)
# - link - link layer (e.g., lora)
#
# All layer modules and the parameters have to be defined in the
# lib/settings.py module.
#
# @author: Asanga Udugama (adu@comnets.uni-bremen.de)
# @date: 10-jun-2020
#

import pycom
import gc
import os
import _thread
import machine
import time
import common
import settings

# basic initializations
time.sleep(2)
gc.enable()
pycom.heartbeat(False)

# setup the environment
try:

    # load modules of the configured 3-layer protocol stack
    app = __import__(settings.APP_LAYER)
    fwd = __import__(settings.FWD_LAYER)
    link = __import__(settings.LINK_LAYER)

    # initialize common environment
    common.initialize()

    # initialize all layers
    app.initialize()
    fwd.initialize()
    link.initialize()

    # activate all layers
    app.start()
    fwd.start()
    link.start()

    # wait endlessly while the threads do their work
    while True:

        # loop with a pause
        time.sleep(5)

except Exception as e:
    print(e)
