# Implementation of the RRS forwarding layer.
#
# @author: Asanga Udugama (adu@comnets.uni-bremen.de)
# @date: 10-jun-2020
#

import ucollections
import _thread
import machine
import os
import common
import time
import utime
import settings

# lists to hold cache and neighbours
cache = None
neigh_list = None

# locks for handling updates
cache_lock = None
neigh_list_lock = None


# initialize RRS layer
def initialize():
    global cache
    global neigh_list
    global cache_lock
    global neigh_list_lock

    # initialize lists
    # self.cache = ucollections.OrderedDict()
    # self.neigh_list = ucollections.OrderedDict()
    cache = {}
    neigh_list = {}

    # initialize locks
    cache_lock = _thread.allocate_lock()
    neigh_list_lock = _thread.allocate_lock()


# start the RRS activity threads
def start():

    _thread.start_new_thread(receive_from_app, ())
    _thread.start_new_thread(send_data_to_neighbours, ())
    _thread.start_new_thread(receive_from_link, ())


# get data from application
def receive_from_app():

    # operate in an endless loop
    while True:

        # pause for some time
        time.sleep(1)

        # lock common queue and pop message from application
        # format: D:3FD1-200:456
        with common.rrs_upper_in_lock:
            try:
                # get data from the queue
                msg = common.rrs_upper_in_q.popleft()
                with common.logging_lock:
                    common.log_activity('rrs   < app   | ' + msg)
            except:
                msg = None

        # is there a message?
        if not msg:
            continue

        # split message
        items = msg.split(':')

        # valid message?
        if len(items) < 3:
            continue

        # insert (update) cache
        update_cache(items[1], items[2])


# send data periodically to neighbours
def send_data_to_neighbours():
    global cache
    global neigh_list
    global cache_lock
    global neigh_list_lock

    # send in an endless loop
    while True:

        # pause until time to send
        time.sleep(settings.DATA_SEND_INTERVAL_SEC)

        # pick a random neighbour to send or broadcast
        with neigh_list_lock:

            # are there neighbours?
            if len(neigh_list) == 0:
                continue

            # broadcast set?
            if settings.BROADCAST_RRS:
                # sent to all neighbours
                dest = settings.BROADCAST_ADDRESS
            else:
                # select a random neighbour
                dest = common.pick_item(list(neigh_list))


        # get a random data item to send
        with cache_lock:
            if len(cache) == 0:
                continue

            key = common.pick_item(list(cache))
            value = cache[key]

        # build message
        # format: 56E1:D:3FD1-200:456
        # format: FFFF:D:3FD1-200:456
        msg = dest + ':D:' + key + ':' + value

        # queue message to send
        with common.link_upper_in_lock:
            try:
                common.link_upper_in_q.append(msg)
                with common.logging_lock:
                    common.log_activity('rss   > link  | ' + msg)
            except:
                pass


# receive data from link layer
def receive_from_link():

    # operate in an endless loop
    while True:

        # pause for some time
        time.sleep(1)

        # lock common queue and pop message from link layer
        with common.rrs_lower_in_lock:
            try:
                # get message from the queue
                msg = common.rrs_lower_in_q.popleft()
                with common.logging_lock:
                    common.log_activity('rrs   < link  | ' + msg)
            except:
                msg = None

        # message available?
        if not msg:
            continue

        # split into components
        items = msg.split(':')

        # valid message?
        if len(items) < 2:
            continue

        # neighbour list?
        if items[0] == 'H':
            # update neighbours
            # format: H:5F1D:341A:6732
            # format: H:none
            update_neighbours(list(items[1:]))

        # data?
        elif items[0] == 'D':
            # update cache
            # format: D:3FD1-245300:2167853
            update_cache(items[1], items[2])

            # send data to application
            data = 'D:' + items[1] + ':' + items[2]
            try:
                with common.app_lower_in_lock:
                    common.app_lower_in_q.append(data)
                    with common.logging_lock:
                        common.log_activity('rrs   > app   | ' + data)
            except:
                pass

        # unknown type of message
        else:
            pass


# update neighbour list
def update_neighbours(new_neigh_list):
    global cache
    global neigh_list
    global cache_lock
    global neigh_list_lock

    with neigh_list_lock:

        # remove all neighbours from list
        for key in list(neigh_list):
            del neigh_list[key]

        # all neighbours dissapeared?
        if new_neigh_list[0] == 'none':
            return

        # insert neighbours into list
        for neigh in new_neigh_list:
            neigh_list[neigh] = utime.ticks_ms()


# update cache
def update_cache(key, value):
    global cache
    global neigh_list
    global cache_lock
    global neigh_list_lock

    # lock cache and insert (update) data
    with cache_lock:

        # update cache item
        # key: 3FD1-200:
        # value: 213
        cache[key] = value
        with common.logging_lock:
            common.log_activity('rrs   > cache | ' + key + ':' + value)

        # remove an entry if cache has exceeded limit
        if len(cache) > settings.CACHE_ITEM_LIMIT:
            rkey = list(cache)[0]
            rvalue = cache[rkey]
            with common.logging_lock:
                common.log_activity('rrs   ! cache | ' + rkey + ':' + rvalue)
            del cache[rkey]
