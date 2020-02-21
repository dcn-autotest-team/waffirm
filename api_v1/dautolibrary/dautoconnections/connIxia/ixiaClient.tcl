set socketid [socket localhost 9927]
fconfigure $socketid -buffering line
#puts $socketid "print 123"
#puts $socketid "StartTransmit \[ list \[ list 1 3 5\] \]"
#puts $socketid "SetIxiaStream Host 172.16.1.253 Card 2 Port 2 StreamMode 0 StreamRate 85 Protocl ipv6 SouMac 00-00-00-00-00-02 DesMac 00-00-00-00-00-02 SouIpv6 2003:1:2:3::2 DesIpv6 ff1f:1:2:3::2 DesAddrModev6 IncrHost DesNumv6 10"
set strarg {}
foreach i  $argv {
#puts $i
append strarg " $i"
}
#puts "strarg,$strarg"
#puts $socketid
puts $socketid $strarg
gets $socketid msg
puts $msg