# Implementation of the link layer that handles sending and receiving of
# messages thru the LoRa interface.
#
# @author: Asanga Udugama (adu@comnets.uni-bremen.de)
# @date: 10-jun-2020
#
import pycom
import ucollections
import _thread
import machine
import os
import common
import time
import socket
import utime
import settings

# current neighbour list
neigh_list = None

# used locks
socket_lock = None
neigh_list_lock = None
LED_blink_lock = None

# neighbour list renewal flag
neigh_list_updated = False


# initialize link layer
def initialize():

    global neigh_list
    global socket_lock
    global neigh_list_lock
    global LED_blink_lock
    global neigh_list_updated

    # init neighbour list
    # self.neigh_list = ucollections.OrderedDict()
    neigh_list = {}

    # init locks
    socket_lock = _thread.allocate_lock()
    neigh_list_lock = _thread.allocate_lock()
    LED_blink_lock = _thread.allocate_lock()

    # neighbour list renewal flag
    neigh_list_updated = False


# start link layer activity threads
def start():

    _thread.start_new_thread(send_msg, ())
    _thread.start_new_thread(recv_msg, ())
    _thread.start_new_thread(send_neigh_list, ())
    _thread.start_new_thread(send_hello, ())


# send queued messages out
def send_msg():
    global neigh_list
    global socket_lock
    global neigh_list_lock
    global LED_blink_lock
    global neigh_list_updated

    # endless loop to check in queue and send messages out
    while True:

        # pause for some time
        time.sleep(1)

        # lock common queue and pop message from RRS
        with common.link_upper_in_lock:
            try:
                msg = common.link_upper_in_q.popleft()
                with common.logging_lock:
                    common.log_activity('link  < rrs   | ' + msg)
            except:
                msg = None

        # message to send?
        if not msg:
            continue

        # prepend source (my) address to message
        # format: 3FD1:FFFF:D:3FD1:129
        # format: 3FD1:4DA6:D:3FD1:129
        msg = common.node_id + ':' + msg
        with common.logging_lock:
            common.log_activity('link  > LoRa  | ' + msg)

        # send the packet out
        common.sock.send(msg)

        # light LED
        with LED_blink_lock:
            blink_LED(settings.SEND_BLINK_COLOUR)


# receive messages sent by neighbours
def recv_msg():
    global neigh_list
    global socket_lock
    global neigh_list_lock
    global LED_blink_lock
    global neigh_list_updated

    # endless loop to receive messages
    while True:

        # pause for some time
        time.sleep(1)

        # get message
        common.sock.setblocking(True)
        dbytes = common.sock.recv(64)

        # some bytes received?
        if not (len(dbytes) > 0):
            continue

        # convert to string
        try:
            msg = dbytes.decode("utf-8")
        except:
            continue

        # split to parts
        items = msg.split(':')

        # is valid message? (at least 4 components must be there)
        if len(items) < 4:
            continue

        # log received msg
        with common.logging_lock:
            common.log_activity('link  < LoRa  | ' + msg)

        # HELLO message received?
        if items[2] == 'H':

            # malformed HELLO message
            if len(items) != 4:
                continue

            # light LED
            with LED_blink_lock:
                blink_LED(settings.RECV_BLINK_COLOUR)

            # lock and insert neighbour
            with neigh_list_lock:
                neigh_list[items[3]] = utime.ticks_ms()
                neigh_list_updated = True

        # data message received?
        elif items[2] == 'D':

            # malformed data message
            if len(items) != 5:
                continue

            # is it destined to me?
            if not (items[1] == settings.BROADCAST_ADDRESS \
                or items[1] == common.node_id):
                continue

            # light LED
            with LED_blink_lock:
                blink_LED(settings.RECV_BLINK_COLOUR)

            # create message to send to RRS (without source & dest)
            # format: D:3FD1:129
            nmsg = ':'.join(items[2:])

            # push message to queue with RRS
            with common.rrs_lower_in_lock:
                try:
                    common.rrs_lower_in_q.append(nmsg)
                    with common.logging_lock:
                        common.log_activity('link  > rrs   | ' + nmsg)
                except:
                    pass

        # unknown message received
        else:
            pass


# send the current neighbour list to the RRS layer
def send_neigh_list():
    global neigh_list
    global socket_lock
    global neigh_list_lock
    global neigh_list_updated

    # endless loop to check and inform about neighbours
    while True:

        # pause for some time
        time.sleep(1)

        # remove neighbours that left neighbourhood
        with neigh_list_lock:
            for key in list(neigh_list):
                exptime = neigh_list[key] \
                        + (settings.HELLO_INTERVAL_SEC * 1000 * settings.MISSED_HELLOS)
                if exptime < utime.ticks_ms():
                    del neigh_list[key]
                    neigh_list_updated = True

        # did the neighbourhood change?
        if not neigh_list_updated:
            continue

        # build message
        # format: H:5F1D:341A:6732
        # format: H:none
        msg = 'H:' + ':'.join(neigh_list) \
                    if len(neigh_list) > 0 else 'H:none'

        # push message into queue with RRS
        with common.rrs_lower_in_lock:
            try:
                common.rrs_lower_in_q.append(msg)
                with common.logging_lock:
                    common.log_activity('link  > rrs   | ' + data)
            except:
                pass

        # reset flag
        neigh_list_updated = False


# send HELLO messeages to inform about being in neighbourhood
def send_hello():
    global neigh_list
    global socket_lock
    global neigh_list_lock
    global LED_blink_lock
    global neigh_list_updated

    # endless loop that broadcast HELLOs
    while True:

        # pause for the interval
        time.sleep(settings.HELLO_INTERVAL_SEC)

        # build message and log activity
        # format: 3FD1:FFFF:H:3FD1
        msg = common.node_id + ':' + settings.BROADCAST_ADDRESS + ':H:' + common.node_id
        with common.logging_lock:
            common.log_activity('link  > LoRa  | ' + msg)

        # send HELLO out
        common.sock.send(msg)

        # light LED
        with LED_blink_lock:
            blink_LED(settings.SEND_BLINK_COLOUR)


# blink LED for given color
# IMPORTANT: always use LED_blink_lock to access this function
def blink_LED(color):

    # convert color name to code
    if color == 'red':
        rgb = 0xFF0000
    elif color == 'green':
        rgb = 0x00FF00
    elif color == 'blue':
        rgb = 0x0000FF
    else:
        rgb = 0x008000

    # blink LED with given code
    pycom.rgbled(rgb)
    time.sleep(0.20)
    pycom.rgbled(0x000000)
