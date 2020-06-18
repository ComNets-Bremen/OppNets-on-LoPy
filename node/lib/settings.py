# Holds all the settings used by other modules.
#
# @author: Asanga Udugama (adu@comnets.uni-bremen.de)
# @date: 10-jun-2020
#

# general settings
BROADCAST_ADDRESS = 'FFFF'
MAX_QUEUE_SIZE = 50
MAINTAIN_CONSOLE_LOG = True
MAINTAIN_WRITTEN_LOG = True
LOG_FILE_NAME = '/sd/log.txt'

# app layer settings
APP_LAYER = 'simpleapp'
DATA_GEN_INTERVAL_SEC = 13

# fwd layer settings
FWD_LAYER = 'rrs'
CACHE_ITEM_LIMIT = 50
BROADCAST_RRS = False
DATA_SEND_INTERVAL_SEC = 8

# link layer settings
LINK_LAYER = 'lora'
HELLO_INTERVAL_SEC = 5
MISSED_HELLOS = 3
SEND_BLINK_COLOUR = 'blue'
RECV_BLINK_COLOUR = 'green'
