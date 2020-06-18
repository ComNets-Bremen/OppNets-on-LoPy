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
import utime
import settings


# logging related variables
logging_lock = None

# SD card variables
sd = None
sd_card_present = False

# queues and locks for communication between app and fwd layers
fwd_upper_in_q = None
app_lower_in_q = None
fwd_upper_in_lock = None
app_lower_in_lock = None

# queues and locks for communication between fwd and link layers
link_upper_in_q = None
fwd_lower_in_q = None
link_upper_in_lock = None
fwd_lower_in_lock = None

# node unique ID
node_long_id = 'None'
node_id = 'None'

# initialize
def initialize():
    global logging_lock
    global sd
    global sd_card_present
    global fwd_upper_in_q
    global app_lower_in_q
    global fwd_upper_in_lock
    global app_lower_in_lock
    global link_upper_in_q
    global fwd_lower_in_q
    global link_upper_in_lock
    global fwd_lower_in_lock

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

    # queues and locks for communication between app and fwd layers
    fwd_upper_in_q = ucollections.deque((), settings.MAX_QUEUE_SIZE)
    app_lower_in_q = ucollections.deque((), settings.MAX_QUEUE_SIZE)
    fwd_upper_in_lock = _thread.allocate_lock()
    app_lower_in_lock = _thread.allocate_lock()

    # queues and locks for communication between fwd and link layers
    link_upper_in_q = ucollections.deque((), settings.MAX_QUEUE_SIZE)
    fwd_lower_in_q = ucollections.deque((), settings.MAX_QUEUE_SIZE)
    link_upper_in_lock = _thread.allocate_lock()
    fwd_lower_in_lock = _thread.allocate_lock()

    # log completion of init
    with logging_lock:
        log_activity('initialization completed')


# log activity given as string
# IMPORTANT: always call this function after holding common.logging_lock
def log_activity(info):
    global node_id

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
