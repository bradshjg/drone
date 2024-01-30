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

#### UDP Analysis

* As far as I can tell, we send a 4-byte UDP packet (`0xef000400`) to `192.168.169.1:8800` and then the drone starts sending video frames via UDP to that same socket. Sending that same payload from another socket tells the drone to send that video data there?
* There appear to be control data packets sent regularly, though they have a variable length. 4 byte-length appear to be the "here I am, send me the data" and there's also regularly 40-byte, 60-byte, and 96-byte (and randomly other lengths). The packets maybe aren't too wild to decipher?

4-byte packets look like

`ef000400`
`ef000400`

8-byte packet (only one) looks ike

`ef08080001000000`

40-byte packets look like

`ef022800020200010000000000000000000000000000000000000000000000000000000000000000`

60-byte packets look like

`ef023c000202000101000000000000000000000000000000000000000000000001000000000000000100000014000000ffffffff0000000000000000`
`ef023c000202000101000000000000000000000000000000000000000000000002000000000000000100000014000000ffffffff0000000000000000`
`ef023c00020200010100000001000000640000000000000000000000000000000f000000000000000100000014000000ffffffff0000000000000000`

Notice the byte that was 0, then 1, 2 (and then `0f` later)...that regularly increments, but maybe not _always_?

some 76-byte packets

`ef024c000202000102000000010000006400000000000000000000000000000096000000000000000100000014000000ffffffff970000000000000003000000100000000000000000000000`
`ef024c000202000102000000010000006400000000000000000000000000000099000000000000000100000014000000ffffffff9a0000000000000003000000100000000000000000000000`

some 80-byte packets

`ef0250000202000102000000010000006400000000000000000000000000000036000000000000000100000014000000ffffffff370000000000000000000000140000003f0080ff0000000000000000`
`ef0250000202000102000000010000006400000000000000000000000000000037000000000000000100000014000000ffffffff38000000000000000000000014000000ffff07ff0000000000000000`

some 96-byte packets

`ef0260000202000103000000010000006400000000000000000000000000000011000000000000000100000014000000ffffffff10000000000000000100000014000000ffffffff120000000000000003000000100000000000000000000000`
`ef0260000202000103000000010000006400000000000000000000000000000011000000000000000100000014000000ffffffff12000000000000000100000014000000ffffffff130000000000000003000000100000000000000000000000`
`ef0260000202000103000000010000006400000000000000000000000000000025000000000000000100000014000000ffffffff24000000000000000100000014000000ffffffff260000000000000003000000100000000000000000000000`

the packet length is the 3rd byte, the first is always the same. My guess is the command is the second?

I'll need to play around with the UI to see what sort of packet shapes might come out!

##### Timing

We send UDP packets _really_ regularly, with almost none arriving more than 50 ms apart.

#### TCP analysis

We regularly send TCP SYN packets to `192.168.1.1:7070` but they're never ACKed and we never get any farther than that. What I _think_ is happening is that the phone app is configured with that address...but there's not a TCP server listening. My guess is that we're decoding the UDP packets received directly, but maybe it's possible that some TCP keepalive is happening just with unanswered SYN packets???

##### Timing

We send a TCP SYN packet about ever 1 second