# 5 Below drone reverse engineering

## Packet capture

### What didn't work

* Connecting to the drone's network with another device while my phone was connected
  - The idea was to be promiscuous to see the packets
  - As far as I can tell, the drone only allows one device to connect at a time (fair!)

### What worked

#### Capture

* Wireshark on OSX, putting the wireless interface into monitor mode, and capturing packets.
  - Lot of trial and error regarding the channel, ended up getting an Android app to show the wifi channel I was on, so I could monitor the same channel
* airmon-ng and tcpdump on Linux
  - Same process as above, tried to filter but couldn't get one working, so we captured the world and processed in Wireshark.

#### Analysis

* As far as I can tell, we send a 4-byte UDP packet (`0xef000400`) to `192.168.169.2:8800` and then the drone starts sending video frames via UDP to that same socket. Sending that same payload from another socket tells the drone to send that video data there?
* There appear to be control data packets sent regularly, though they have a variable length. 4 byte-length appear to be the "here I am, send me the data" and there's also regularly 40-byte, 60-byte, and 96-byte (and randomly other lengths). The packets maybe aren't too wild to decipher?

40-byte packets look like

...