# Implementation of the application layer. It is a simple application that
# regularly send data out.
#
# @author: Asanga Udugama (adu@comnets.uni-bremen.de)
# @date: 10-jun-2020
#
import _thread
import machine
import os
import common
import time
import settings

# initialize application layer
def initialize():
    pass


# start the application threads
def start():
    _thread.start_new_thread(generate_data, ())
    _thread.start_new_thread(receive_from_RRS, ())


# application thread to send data periodically (to RRS layer)
def generate_data():

    # operate in an endless loop
    while True:

        # pause for some time
        time.sleep(settings.DATA_GEN_INTERVAL_SEC)

        # create message to send
        # format: D:3FD1-200:213
        data_name = common.node_id + '-' + str(int(machine.rng()))
        data_payload = str(int(machine.rng()))

        data = 'D:' + data_name + ':' + data_payload

        # lock common queue and insert message for RRS to pop
        with common.rrs_upper_in_lock:
            try:
                common.rrs_upper_in_q.append(data)
                with common.logging_lock:
                    common.log_activity('app   > rrs   | ' + data)
            except:
                pass


# application thread to receive data from RRS layer
def receive_from_RRS():

    # operate in an endless loop
    while True:

        # pause for some time
        time.sleep(1)

        # lock common queue and pop message from RRS
        # format: D:3FD1-200:456
        with common.app_lower_in_lock:
            try:
                data = common.app_lower_in_q.popleft()
                with common.logging_lock:
                    common.log_activity('app   < rrs   | ' + data)
            except:
                pass
