# Holds all the common variables and functions used by all the
# other functions.
#
# @author: Asanga Udugama (adu@comnets.uni-bremen.de)
# @date: 10-jun-2020
#
import _thread
import machine
import os
import ucollections
import network
import ubinascii
import socket
import utime
import settings


# logging related variables
logging_lock = None

# SD card variables
sd = None
sd_card_present = False

# queues and locks for communication between app and rrs layers
rrs_upper_in_q = None
app_lower_in_q = None
rrs_upper_in_lock = None
app_lower_in_lock = None

# queues and locks for communication between rrs and link layers
link_upper_in_q = None
rrs_lower_in_q = None
link_upper_in_lock = None
rrs_lower_in_lock = None

# LoRa interface parameters
lora = None

# node unique ID
node_long_id = 'None'
node_id = 'None'

# socket var
sock = None

# initialize
def initialize():
    global logging_lock
    global sd
    global sd_card_present
    global rrs_upper_in_q
    global app_lower_in_q
    global rrs_upper_in_lock
    global app_lower_in_lock
    global link_upper_in_q
    global rrs_lower_in_q
    global link_upper_in_lock
    global rrs_lower_in_lock
    global lora
    global node_long_id
    global node_id
    global sock

    # setup logging
    logging_lock = _thread.allocate_lock()
    sd_card_present = False

    # log start of init
    with logging_lock:
        log_activity('initialization started...')

    # mount SD card
    try:
        sd = machine.SD()
        os.mount(sd, '/sd')
        sd_card_present = True

    except:
        pass

    # queues and locks for communication between app and rrs layers
    rrs_upper_in_q = ucollections.deque((), settings.MAX_QUEUE_SIZE)
    app_lower_in_q = ucollections.deque((), settings.MAX_QUEUE_SIZE)
    rrs_upper_in_lock = _thread.allocate_lock()
    app_lower_in_lock = _thread.allocate_lock()

    # queues and locks for communication between rrs and link layers
    link_upper_in_q = ucollections.deque((), settings.MAX_QUEUE_SIZE)
    rrs_lower_in_q = ucollections.deque((), settings.MAX_QUEUE_SIZE)
    link_upper_in_lock = _thread.allocate_lock()
    rrs_lower_in_lock = _thread.allocate_lock()

    # init LoRa interface
    # initialise LoRa in LORA mode
    # Please pick the region that matches where you are using the device:
    # Asia = LoRa.AS923
    # Australia = LoRa.AU915
    # Europe = LoRa.EU868
    # United States = LoRa.US915
    # more params can also be given, like frequency, tx power and spreading factor
    lora = network.LoRa(mode=network.LoRa.LORA, region=network.LoRa.EU868)

    # get a unique ID
    # mac() and hexlify() gives 16 byte address, we take only last 4 bytes
    node_long_id = ubinascii.hexlify(lora.mac()).upper().decode('utf-8')
    node_id = node_long_id[12:]

    # setup the send, recv socket
    sock = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

    # log completion of init
    with logging_lock:
        log_activity('initialization completed')
        log_activity('node ID - long ' + node_long_id + ' - short ' + node_id)


# log activity given as string
# IMPORTANT: always call this function after holding common.logging_lock
def log_activity(info):

    # build log string
    log_str = str(utime.ticks_ms()) + ' ' + node_id +  ' ' + info

    # print to console
    if settings.MAINTAIN_CONSOLE_LOG:
        print(log_str)

    # if SD card present, write to log
    if sd_card_present and settings.MAINTAIN_WRITTEN_LOG:

        # write to log file
        try:
            logfp = open(settings.LOG_FILE_NAME, mode='a')
            logfp.write(log_str)
            logfp.write('\n')
            logfp.close()
        except:
            print('something wrong with the log file')
            print('could be - wrong path, log full')


# get a random item from a list (by Peter Hinch)
def pick_item(sequence):
    div = 0xffffff // len(sequence)
    return sequence[machine.rng() // div]
