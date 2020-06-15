# Holds all the settings used by other modules.
#
# @author: Asanga Udugama (adu@comnets.uni-bremen.de)
# @date: 10-jun-2020
#

# general settings
BROADCAST_ADDRESS = 'FFFF'
MAX_QUEUE_SIZE = 50
MAINTAIN_CONSOLE_LOG = True
MAINTAIN_WRITTEN_LOG = False
LOG_FILE_NAME = '/sd/log.txt'

# application settings
DATA_GEN_INTERVAL_SEC = 13

# RRS settings
CACHE_ITEM_LIMIT = 50
BROADCAST_RRS = False
DATA_SEND_INTERVAL_SEC = 8

# link settings
HELLO_INTERVAL_SEC = 5
MISSED_HELLOS = 3
SEND_BLINK_COLOUR = 'blue'
RECV_BLINK_COLOUR = 'green'
