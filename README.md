# OppNets-on-LoPy


Opportunistic Networking (OppNets) is a type of wireless networking acrchitecture where nodes communicate directly with other nodes to exchange information, without using any networking infrastructure such as wireless base stations or access points. This repository, OppNets-on-LoPy provides a collection of source code that implements operations of OppNets nodes for LoPy4 (PyCom) devices.

A node implementation consist of a 3-layer protocol architecture.

- Application layer - implements an application that generates data periodically
- Forwarding layer - implements the forwarding protocol to disseminate data
- Link layer - implements the direct communications and neighbourhood management



## Running the Implementation (on a LoPy Device)

The `Atom IDE`, one of the IDEs recommnded ([link](https://docs.pycom.io/pymakr/installation/atom/)) by the makers of the LoPy4 device was used to develop this implementation and to load it to the LoPy device. Simply open the `./node` folder as a project in the `Atom IDE` and follow the instructions given to upload the code into the LoPy4 device.



## Current Implementation Status

This is an on-going work and below are the important aspects of this implementation.

- Uses LoRa for direct communications between nodes
- Uses the Randomized Rumour Spreading (RRS) forwarding protocol
- Has a simple application that generates periodic data 



## Implementation Details

The implementation is distributed in multiple source files. The following high-level folders contain spacific parts of the implementation.

- `./node` - all the micro-python code implementing a LoPy4 based OppNets node
- `./parsers` - all the activity log parsers

A brief description of each of these high-level folders are given below.

### RRS-LoRa Node Implementation (`./node` folder)

The following source files implements the functionality of an OppNets node that uses the RRS forwarding protocol and the LoRa link layer.

- `main.py` - initiates all operations
- `lib/settings.py` - contains all the parameters used by other source files
- `lib/common.py` - contains all the common variables (e.g., queues) used by other source files
- `lib/app.py` - contains code that implements the application
- `lib/rrs.py` - contains the code that implements the RRS based forwarding layer functionality
- `lib/rrs.py` - contains the code that implements the RRS functionality


### Parsers (`./parsers` folder)

Currently contains only a place holder file.



## Message Formats

Protocol layers exchange information using messages. Here are the formats of those messages. Information in each message is separated by a colon (`:`)

### Application Layer and Forwarding Layer

- `Application Layer <-> Forwarding Layer` - `D:3B0C-9187043:10950513`
  - `D` - a data message
  - `3B0C-9187043` - data name
  - `10950513` - data

### Forwarding Layer and Link Layer

- `Forwarding Layer -> Link Layer` - `E820:D:3B0C-16336283:10330829`
  - `E820` - destination node (FFFF if broadcast RRS)
  - `D` - a data message
  - `3B0C-16336283` - data name
  - `10330829` - data
- `Link Layer -> Forwarding Layer` - `D:E820-9162187:10807013`
  - `D` - a data message
  - `E820-9162187` - data name
  - `10807013` - data
- `Link Layer -> Forwarding Layer` - `H:E820:F213`
  - `H` - neighbour list message
  - `E820:F213` 2 neighbours

### Link Layer and LoRa

- `Link Layer <-> LoRa` - `E820:FFFF:H:E820'
  - `E820` - source address
  - `FFFF` - destination address (FFFF is broadcast)
  - `H` - neighbour (hello) alive message
  - `E820` - neighbour whose alive

- `Link layer <-> LoRa` - `3B0C:E820:D:3B0C-2925294:1462647`
  - `3B0C` - source address
  - `E820` - destination address (FFFF is broadcast)
  - `D` - a data message
  - `3B0C-2925294` - data name
  - `1462647` - data



## Implemented Forwarders

Currently, only the Randomized Rumour Spreading (RRS) forwarding protocol is implemented. 

### Randomized Rumour Spreading (RRS)

The RRS protocol selects a random data item from the cache and send it to all the neighbours (if Broadcast-RRS) or one random neighbour in the nighbourhood.



## Activity Logging

All activities can be looged to the console and/or the log file. These have to be configured in the `settings.py` file. If the log file logging is enabled, a Micro SD card must be inserted to the LoPy4. Below is a sample of a log.

```
1536792 3B0C link  > LoRa  | 3B0C:FFFF:H:3B0C
1537327 3B0C rss   > link  | E820:D:3B0C-9895291:11173565
1537361 3B0C link  < rrs   | E820:D:3B0C-9895291:11173565
1537370 3B0C link  > LoRa  | 3B0C:E820:D:3B0C-9895291:11173565
1539026 3B0C link  < LoRa  | E820:FFFF:H:E820
1540267 3B0C rrs   < link  | H:E820
```


## Settings

All configurable parameters are listed in the `settings.py` file. The current settings are as follows.

### General Settings

```
BROADCAST_ADDRESS = 'FFFF'
MAX_QUEUE_SIZE = 50
MAINTAIN_CONSOLE_LOG = True
MAINTAIN_WRITTEN_LOG = False
```

### Application Settings

```
DATA_GEN_INTERVAL_SEC = 13
```

### RRS Settings

```
CACHE_ITEM_LIMIT = 50
BROADCAST_RRS = False
DATA_SEND_INTERVAL_SEC = 8
```


### Link Settings

```
HELLO_INTERVAL_SEC = 5
MISSED_HELLOS = 3
SEND_BLINK_COLOUR = 'blue'
RECV_BLINK_COLOUR = 'green'
```


## Firmware Versions

This version of the modules has been tested on the following LoPy4 firmware version.

- `Pycom MicroPython 1.20.0.rc13 [v1.9.4-94bb382] on 2019-08-22; LoPy4 with ESP32`



## Questions or Comments

If you have any questions or comments, please write to any one of us listed below using ops@comnets.uni-bremen.de

  - Asanga Udugama
  - Jens Dede
  - Vishnupriya Parimalam
  - Anna Förster

