# OppNets-on-LoPy


Opportunistic Networking (OppNets) is a type of wireless networking acrchitecture where nodes communicate directly with other nodes to exchange information, without using any networking infrastructure such as wireless base stations or access points. This repository, OppNets-on-LoPy provides a collection of source code that implements the functionality to operate OppNets nodes for LoPy4 (PyCom) devices.

A node implementation consist of a 3-layer protocol architecture.

- Application layer - implements an application that generates data periodically
- Forwarding layer - implements the forwarding protocol to disseminate data
- Link layer - implements the direct communications and neighbourhood management

Depending on the requirement, each layer can be configured to use different implementations.

## Loading, Configuring and Running (on a LoPy Device)

The `Atom IDE`, one of the IDEs recommnded ([link](https://docs.pycom.io/pymakr/installation/atom/)) by the makers of the LoPy4 device was used to develop this implementation and to load it to the LoPy device. To load, configure and run, follow the instructions below.


1. Download this repository to a computer where the `Atom IDE` is installed
2. Open the `./node` folder as a project (`Add Project Folder`) in the `Atom IDE`
3. Setup the protocol stack (`APP_LAYER`, `FWD_LAYER`, `LINK_LAYER`) and the parmeters in the `lib/settings.py` (or leave as is to use the default settings)
4. Press the `Upload project to device` button to upload the code into the LoPy4 device

There are also other code available to perform different tasks related to the implementation. They could be code to run on LoPy devices (like manage the the SD card) or parsers run on your computer to pass a log. All these are made available under `./tools` or `./parsers`



## Current Implementation Status

This is an on-going work. Below is a list of the status of the current implementation.

- Uses LoRa for direct communications between nodes (in `./node/lib/lora.py` module)
- Uses the Randomized Rumour Spreading (RRS) forwarding protocol (in `./node/lib/rrs.py` module)
- Has a simple application that generates periodic data (in `./node/lib/simpleapp.py` module)



## Implementation Details

The implementation is distributed in multiple source files. The following high-level folders contain spacific parts of the implementation.

- `./node` - contains micro-python code implementing a LoPy4 based OppNets node
- `./tools` - contains micro-python or other code that manages different aspects (e.g., manage SD card in a LoPy)
- `./parsers` - contains parsers written to extract information (e.g., from the log created by the LoPy)

A brief description of each of these high-level folders are given below.


### Node Implementation 

The following source files (in `./node` folder) implements the functionality of an OppNets node that is configured based on the diferent protocol layer implementations required.

- `main.py` - initiates all operations
- `lib/settings.py` - contains the protocol layer configurations and all the parameters used
- `lib/common.py` - contains all the common variables (e.g., queues) used by other source files
- `lib/simpleapp.py` - contains code that implements a simple data injection application
- `lib/rrs.py` - contains the code that implements the RRS based forwarding functionality
- `lib/lora.py` - contains the code that implements LoRa based communications


### Parsers

This folder (`./parsers`) holds all the parsers to extract data from the log. Currently contains only a place holder file.


### Tools

This folder (`./tools`) contains programs required for managing different components of the environment.

#### Manage SD Card

The `sd-check` tool is to manage the contents of an SD card plugged in to a LoPy (e.g., remove the log, dump the log).



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


### Link Layer and Wireless Interface (e.g., LoRa)

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



## Implemented Protocol Layers

Here is a description of the different protocol layers currently available in the implementation. We are updating this reqpository with new protocll layers when they become available.

### Simple Data Injection Application

This application generates data with random values and passes it on to the forwarding layer to inject to the network.


### Randomized Rumour Spreading (RRS)

The Randomized Rumour Spreading (RRS) is a forwarding protocol that selects data randomly from a cache and sends to nodes in the communication range of that node. When sending, it can decide either to broadcast (for every neighbour to receive) or send it to a specific node.


### LoRa 

This link protocol uses LoRa to perform direct communications with nodes in a neighbourhood. Using a hello message mechanism, it keeps track of the neighbours in a node's neighbourhood.



## Activity Logging

All activities can be looged to the console and/or the log file. These have to be configured in the `lib/settings.py` file. If the log file writing is enabled, a Micro SD card must be inserted in the LoPy4. Below is a sample of a log.

```
1536792 3B0C link  > LoRa  | 3B0C:FFFF:H:3B0C
1537327 3B0C rss   > link  | E820:D:3B0C-9895291:11173565
1537361 3B0C link  < rrs   | E820:D:3B0C-9895291:11173565
1537370 3B0C link  > LoRa  | 3B0C:E820:D:3B0C-9895291:11173565
1539026 3B0C link  < LoRa  | E820:FFFF:H:E820
1540267 3B0C rrs   < link  | H:E820
```


## Settings

All configurable parameters are listed in the `lib/settings.py` file. The current settings are as follows.

### General Settings

```
BROADCAST_ADDRESS = 'FFFF'
MAX_QUEUE_SIZE = 50
MAINTAIN_CONSOLE_LOG = True
MAINTAIN_WRITTEN_LOG = True
LOG_FILE_NAME = '/sd/log.txt'

```

### Application Layer Settings

```
APP_LAYER = 'simpleapp'
DATA_GEN_INTERVAL_SEC = 13

```

### Forwarding Layer Settings

```
FWD_LAYER = 'rrs'
CACHE_ITEM_LIMIT = 50
BROADCAST_RRS = False
DATA_SEND_INTERVAL_SEC = 8

```


### Link Layer Settings

```
LINK_LAYER = 'lora'
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

