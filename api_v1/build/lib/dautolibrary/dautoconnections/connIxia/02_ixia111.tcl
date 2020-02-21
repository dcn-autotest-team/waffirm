#*********************************************************************
# 02_ixia.tcl - Proc of Basic Management
# 
# Author:      (liangdong@digitalchina.com)
#
# Version 2.0.0
#
# Copyright (c) 2004-2008 Digital China Networks Co. Ltd 
#
# Features: 
#           written based on chapter 1 of dcn manual 
# 
#*********************************************************************
# Change log:
#     - 2009.7.2  modified by liangdong
#
#*********************************************************************

#Package

#Globals Definition

#Source files

#Procedure Definition
#################################################################################################

package provide DcnTestP 1.1

#**************************************************************#
#                                                              #
#                       命令配置函数                           #
#                                                              #
#**************************************************************#

##################################################################################
# 
# SetIxiaStream:配置某一个端口的某一条流
#
# args:
#	  Host : 100.1.1.222
#	  Card : 8
#	  Port : 1
#	  RateMode auto : auto/10half/10full/100half/100full/1ghalf/1gfull
#     FlowControl false : ixia端口是否开启流控功能，默认false
#	  StreamMode 0 : 0:contine   1:stop after send  2:more than one stream on one port  默认为0
#     StreamNum 1 ：ixia端口模拟多条流时，各流的编号
#     LastStreamFlag true ：ixia端口模拟多条流时，该流是否为最后一条流
#     ReturnToId 1 ：ixia端口模拟多条流时，最后一条流的下一条流的编号
#	  StreamRateMode : PercentRate/Fps/Bps
#     StreamRate : 100/148810/76190476
#	  NumFrames : 100
#
#	  SouMac : 00-00-00-00-00-01
#     SouMask: ff-ff-ff-ff-ff-ff
#	  SouNum : 1
#     SouMode: increment/idle
#	  DesMac : 00-00-00-00-00-02
#     DesMac : ff-ff-ff-ff-ff-ff
#	  DesNum : 1
#     DesMode: increment/idle
#	  FrameSize : 128
#     FrameErrors 0 : 0(streamErrorGood),1(streamErrorAlignment),2(streamErrorDribble),
#	                  3(streamErrorBadCRC),4(streamErrorNoCRC)
#	
#     UDF1Flag,Offset1,Length1,Value1,ContinueFlag1,Repeat1
#     UDF2Flag,Offset2,Length2,Value2,ContinueFlag2,Repeat2
#     UDF3Flag,Offset3,Length3,Value3,ContinueFlag3,Repeat3
#     UDF4Flag,Offset4,Length4,Value4,ContinueFlag4,Repeat4 : 用户自定义字段，可以用来构造各种复杂的包
#
#	  VlanTagFlag : 0   0:no vlan tag  1:exist one vlan tag  2:exist two vlan tag
#	  VlanId : 3
#     Tpid : 8100
#	  UserPriority : 5
#     VlanMode  vIdle   : vIdle/vIncrement/vDecrement 默认vIdle
#     VlanNum   1   :变化的vlan数目
#     VlanStep  1   :变化步长
#     IfTpid  0 ：是否含有多层TAG
#     Tpid1 : 9100
#     VlanId1 : 2
#     Tpid2 : 9200
#     VlanId2 : 3
#     
#	  Protocl none : none/ipv4/arp/ipv6/ipv6ipv4  默认为none
#	  EthernetType noType : noType/ethernetII/ieee8023snap/ieee8023/ieee8022  默认为noType
#     EthernetTypeFlag 0 :是否使用协议编号
#     EthernetTypeNum 0 ：协议编号
#	
#     SouIp 1.1.1.1
#	  SouMask 255.255.255.0
#	  SouClassMode classC :noClass/classA/classB/classC/classD  默认为classC
#	  SouIpMode ipIncrHost :ipIdle/ipIncrHost/ipDecrHost/ipContIncrHost/ipContDecrHost
#                           ipIncrNetwork/ipDecrNetwork/ipContIncrNetwork/ipContDecrNerwork/ipRandom
#	  SouIpNum 1
#	  DesIp 2.2.2.2
#	  DesMask 255.255.255.0
#	  DesClassMode classC
#	  DesIpMode ipIncrHost
#	  DesIpNum 1
#	  Fragment 0   :是否分片
#	  LastFragment 0 :是否分片的最后一片
#	  FragmentOffset 0 ：帧偏移
#
#	  ProtoclEx none ：tcp/udp/icmp/igmp
#	  SPort 0
#	  DPort 0
#	  SequenceNum 0
#	  HeaderLength 5
#	  Type 0
#	  Code 0
#	  IgmpVersion 2
#	  IgmpGroupAddress 0.0.0.0
#	  IgmpSourceIpAddress 0.0.0.0
#	  IgmpMode igmpIdle
#	  IgmpRepeat 1
#	  ACK false
#	  FIN false
#	  PSH false
#	  RST false
#	  URG false
#	  SYN false	
#
#     ArpOperation  1 :  1 request 2 reply
#	  SenderMac  00-00-00-00-00-01
#	  SenderMacNum  1
#	  TargetMac  00-00-00-00-00-02
#	  TargetMacNum 1
#	  SenderIp  1.1.1.1
#	  SenderIpNum  1
#	  TargetIp  2.2.2.2
#	  TargetIpNum 1 
#
#     SouIpv6    2003:0001:0002:0003:0000:0000:0000:0003
#	  SouAddrModev6 Fixed : Fixed/IncrHost/IncrNetwork
#	  SouNumv6   1
#	  SouNetworkv6 64
#	  DesIpv6    2003:0001:0002:0003:0000:0000:0000:0004
#	  DesAddrModev6 Fixed   
#	  DesNumv6   1
#	  DesNetworkv6 64	  
#
#	  PriorityFlag 1  ;#1:Dscp 0:Tos 2:Ipprecedence 3:Ipprecedence&Tos
#	  Dscp 41
#	  Tos 4
#	  Ipprecedence 7
#	  TrafficClass 3
#	  FlowLabel 0
#     NextHeader ipV6NoNextHeader
# 
# return:
# 
# addition:
#     -liangdong 2008.8.11
#     -gaowei 2005.7.21
# 
# examples:
#     SetIxiaStream Host 100.1.1.222 Card 8 Port 2 StreamMode 1 StreamRate 99 NumFrames 3 
#            SouMac 00-00-00-00-00-01 DesMac 00-00-00-00-00-02
#     SetIxiaStream Host 100.1.1.222 Card 8 Port 1 RateMode 100full StreamMode 0 StreamRate 50 
#            NumFrames 122 SouMac 00-00-00-00-00-01 SouNum 3 DesMac 00-00-00-00-00-02 DesNum 4 
#            FrameSize 255 VlanTagFlag 1 VlanId 3 UserPriority 5 Protocl ipv4 SouIp 1.1.1.1 
#            SouMask 255.0.0.0 SouNum 3 DesIp 2.2.2.2 DesMask 255.255.255.0 DesNum 55 
#            PriorityFlag 1 Dscp 41 Tos 4
#     SetIxiaStream Host 100.1.1.117 Card 8 Port 1 StreamMode 0 StreamRate 10 Protocl ipv6 \
#                   SouMac 00-00-00-00-00-01 DesMac 00-00-00-00-00-02 \
#                   SouIpv6 2003:1:2:3::2 DesIpv6 2004:1:2:3::2 DesAddrModev6 IncrHost DesNumv6 10 DesNetworkv6 96
#        
#     SetIxiaStream Host 100.1.1.117 Card 8 Port 1 StreamMode 0 StreamRate 10 Protocl ipv6 \
#                   SouMac 00-00-00-00-00-01 DesMac 00-00-00-00-00-02 \
#                   SouIpv6 2003:1:2:3::2 DesIpv6 ff1f:1:2:3::2 DesAddrModev6 IncrHost DesNumv6 10
#
#        1、配置目标端口二层流量，源mac（00-00-00-00-00-01），目的mac（00-00-00-00-00-02），以99%的线速，发送3个包。
#        SetIxiaStream Host 100.1.1.222 Card 8 Port 2 StreamMode 1 StreamRateMode PercentRate \
#                    StreamRate 99 NumFrames 3 \
#                    SouMac 00-00-00-00-00-01 DesMac 00-00-00-00-00-02
#        2、配置目标端口二层流量，源mac（00-00-00-00-00-01），目的mac（00-00-00-00-00-02），以100FPS的速率，连续发包。
#        SetIxiaStream Host 100.1.1.222 Card 8 Port 2 StreamMode 0 StreamRateMode Fps \
#                    StreamRate 100 \
#                    SouMac 00-00-00-00-00-01 DesMac 00-00-00-00-00-02
#        3、配置目标端口二层流量，第一条流量：源mac（00-00-00-00-00-01），目的mac（00-00-00-00-00-02），50BPS的速率；第二条流量：源mac（00-00-00-00-00-01），目的mac（00-00-00-00-00-05），50BPS的速率。每条流发送100个包后发送下一条流，依次循环。
#        SetIxiaStream Host 100.1.1.222 Card 8 Port 2 StreamMode 2 LastStreamFlag false 
#                    StreamNum 1 StreamRateMode Bps StreamRate 50 \
#                    SouMac 00-00-00-00-00-01 DesMac 00-00-00-00-00-02
#        SetIxiaStream Host 100.1.1.222 Card 8 Port 2 StreamMode 2 LastStreamFlag true \
#                    ReturnToId 1 StreamNum 2 StreamRateMode Bps StreamRate 50 \
#                    SouMac 00-00-00-00-00-01 DesMac 00-00-00-00-00-05
#        4、配置目标端口二层流量，源mac（00-00-00-00-00-01），目的mac（00-00-00-00-00-02），以99%的线速，发送3个包，并开启流控。
#        SetIxiaStream Host 100.1.1.222 Card 8 Port 2 StreamMode 1 StreamRateMode PercentRate \
#                    StreamRate 99 NumFrames 3 FlowControl true \
#                    SouMac 00-00-00-00-00-01 DesMac 00-00-00-00-00-02
#        5、配置目标端口二层流量，源mac（00-00-00-00-00-01 incr 10），目的mac（00-00-00-00-00-02 incr 10），以100%的线速连续发包，。
#        SetIxiaStream Host 100.1.1.222 Card 8 Port 2 StreamMode 0 StreamRateMode PercentRate \
#                    StreamRate 100 \
#                    SouMac 00-00-00-00-00-01 SouNum 10 \
#                    DesMac 00-00-00-00-00-02 DesNum 10
#        6、配置目标端口二层流量，源mac（00-00-00-00-00-01），目的mac（00-00-00-00-00-02），以100%的线速连续发包，错误包类型为：ErrorNoCRC。
#        SetIxiaStream Host 100.1.1.222 Card 8 Port 2 StreamMode 0 StreamRateMode PercentRate \
#                    StreamRate 100 \
#                    SouMac 00-00-00-00-00-01 DesMac 00-00-00-00-00-02 FrameErrors 4
#        FrameErrors: 0(streamErrorGood)、1(streamErrorAlignment)、2(streamErrorDribble)、
#        	       3(streamErrorBadCRC)、4(streamErrorNoCRC)
#        7、配置目标端口二层流量，源mac（00-00-00-00-00-01），目的mac（00-00-00-00-00-02），以100%的线速连续发包，包大小为128字节。
#        SetIxiaStream Host 100.1.1.222 Card 8 Port 2 StreamMode 0 StreamRateMode PercentRate \
#                    StreamRate 100 FrameSize 128 \
#                    SouMac 00-00-00-00-00-01 DesMac 00-00-00-00-00-02
#        8、配置目标端口二层流量，源mac（00-00-00-00-00-01 incr 10），目的mac（00-00-00-00-00-02 incr 10），源ip（10.1.1.2 incr 10），目的ip（20.1.1.2 incr 10）以100%的线速连续发包，。
#        SetIxiaStream Host 100.1.1.222 Card 8 Port 2 StreamMode 0 StreamRateMode PercentRate \
#                    StreamRate 100 \
#                    SouMac 00-00-00-00-00-01 SouNum 10 \
#                    DesMac 00-00-00-00-00-02 DesNum 10 \
#                    Protocl ipv4 \
#                    SouIp 10.1.1.2 SouMask 255.255.255.0 SouIpNum 10 \
#                    DesIp 20.1.1.2 DesMask 255.255.255.0 DesIpNum 10
#
##################################################################################
#原来的使用方法还可以使用：
#SetIxiaStream Host $host Card $Card1 Port $Port1 StreamRateMode Fps StreamRate 10 \
#              SouMac 00-01-0f-01-00-01 DesMac 00-01-0f-03-00-01 \
#	      Protocl ipv4 EthernetType ethernetII \
#	      SouIp 10.1.1.2 DesIp 225.10.10.1 \
#	      ProtoclEx igmp IgmpVersion 2 Type 22 IgmpGroupAddress 225.10.10.1 IgmpMode igmpIncrement IgmpRepeat 5
#
#SetIxiaStream Host $host Card $Card1 Port $Port1 StreamRateMode Fps StreamRate 10 \
#              SouMac 00-01-0f-01-00-01 DesMac 01-00-5E-0A-0A-01 \
#	      Protocl ipv4 EthernetType ethernetII \
#	      SouIp 10.1.1.2 DesIp 225.10.10.1 \
#	      ProtoclEx igmp IgmpVersion 3 Type 34 IgmpSourceIpAddress 30.1.1.2 IgmpGroupAddress 225.10.10.1
#今后编写脚本请使用如下方法：
#SetIxiaStream Host $host Card $Card1 Port $Port1 StreamRateMode Fps StreamRate 10 \
#              SouMac 00-01-0f-01-00-01 DesMac 01-00-5e-0a-0a-01 \
#	      Protocl ipv4 EthernetType ethernetII \
#	      SouIp 10.1.1.2 DesIp 225.10.10.1 \
#	      ProtoclEx igmp IgmpVersion 1 Type report IgmpGroupAddress 225.10.10.1 IgmpMode igmpIncrement IgmpRepeat 5
#SetIxiaStream Host $host Card $Card1 Port $Port1 StreamRateMode Fps StreamRate 10 \
#              SouMac 00-01-0f-01-00-01 DesMac 01-00-5e-0a-0a-01 \
#	      Protocl ipv4 EthernetType ethernetII \
#	      SouIp 10.1.1.2 DesIp 225.10.10.1 \
#	      ProtoclEx igmp IgmpVersion 1 Type query IgmpGroupAddress 225.10.10.1 IgmpMode igmpIncrement IgmpRepeat 5
#
#SetIxiaStream Host $host Card $Card1 Port $Port1 StreamRateMode Fps StreamRate 10 \
#              SouMac 00-01-0f-01-00-01 DesMac 01-00-5e-0a-0a-01 \
#	      Protocl ipv4 EthernetType ethernetII \
#	      SouIp 10.1.1.2 DesIp 225.10.10.1 \
#	      ProtoclEx igmp IgmpVersion 2 Type report IgmpGroupAddress 225.10.10.1 IgmpMode igmpIncrement IgmpRepeat 5
#SetIxiaStream Host $host Card $Card1 Port $Port1 StreamRateMode Fps StreamRate 10 \
#              SouMac 00-01-0f-01-00-01 DesMac 00-01-0f-03-00-01 \
#	      Protocl ipv4 EthernetType ethernetII \
#	      SouIp 10.1.1.2 DesIp 225.10.10.1 \
#	      ProtoclEx igmp IgmpVersion 2 Type query IgmpGroupAddress 225.10.10.1 IgmpMode igmpIncrement IgmpRepeat 5
#SetIxiaStream Host $host Card $Card1 Port $Port1 StreamRateMode Fps StreamRate 10 \
#              SouMac 00-01-0f-01-00-01 DesMac 01-00-5e-0a-0a-01 \
#	      Protocl ipv4 EthernetType ethernetII \
#	      SouIp 10.1.1.2 DesIp 225.10.10.1 \
#	      ProtoclEx igmp IgmpVersion 2 Type leave IgmpGroupAddress 225.10.10.1 IgmpMode igmpIncrement IgmpRepeat 5
#
#SetIxiaStream Host $host Card $Card1 Port $Port1 StreamRateMode Fps StreamRate 10 \
#              SouMac 00-01-0f-01-00-01 DesMac 01-00-5E-0A-0A-01 \
#	      Protocl ipv4 EthernetType ethernetII \
#	      SouIp 10.1.1.2 DesIp 225.10.10.1 \
#	      ProtoclEx igmp IgmpVersion 3 Type query IgmpSourceIpAddress "30.1.1.2 30.1.1.3" IgmpGroupAddress 225.10.10.1 IgmpRepeat 5
#SetIxiaStream Host $host Card $Card1 Port $Port1 StreamRateMode Fps StreamRate 10 \
#              SouMac 00-01-0f-01-00-01 DesMac 01-00-5E-0A-0A-01 \
#	      Protocl ipv4 EthernetType ethernetII \
#	      SouIp 10.1.1.2 DesIp 225.10.10.1 \
#	      ProtoclEx igmp IgmpVersion 3 Type report IgmpGroupRecord {{225.10.10.1 include "30.1.1.2 30.1.1.3"} \
#                    {225.10.10.2 exclude "30.1.1.2 30.1.1.3"} {225.10.10.3 toinclude "30.1.1.2 30.1.1.3"} \
#                    {225.10.10.4 toexclude "30.1.1.2 30.1.1.3"} {225.10.10.5 allow "30.1.1.2 30.1.1.3"} \
#                    {225.10.10.6 block "30.1.1.2 30.1.1.3"}}
#普通查询格式
#SetIxiaStream Host $host Card $Card1 Port $Port1 StreamRateMode Fps StreamRate 10 \
#              SouMac $vlanmac DesMac 33-33-00-00-00-01 \
#              Protocl ipv6 EthernetType ethernetII \
#              SouIpv6 :: DesIpv6 ff02::1 \
#              ProtoclEx mld MldVersion 1 Type query MldGroupAddress ::
#
#指定组查询格式
#SetIxiaStream Host $host Card $Card1 Port $Port1 StreamRateMode Fps StreamRate 10 \
#              SouMac $vlanmac DesMac 33-33-00-00-00-01 \
#              Protocl ipv6 EthernetType ethernetII \
#              SouIpv6 :: DesIpv6 ff02::1 \
#              ProtoclEx mld MldVersion 1 Type query MldGroupAddress ff3f::1
#
#v1版本的report
#SetIxiaStream Host $host Card $Card1 Port $Port1 StreamRateMode Fps StreamRate 10 \
#              SouMac $clientmac DesMac 33-33-00-00-00-01 \
#              Protocl ipv6 EthernetType ethernetII \
#              SouIpv6 [GetLinkLocalAddress $clientmac] DesIpv6 ff3f::1 \
#              ProtoclEx mld MldVersion 1 Type report MldGroupAddress ff3f::1
#SetIxiaStream Host $host Card $Card1 Port $Port1 StreamRateMode Fps StreamRate 10 \
#              SouMac $clientmac DesMac 33-33-00-00-00-01 DesNum 300 \
#              Protocl ipv6 EthernetType ethernetII \
#              SouIpv6 [GetLinkLocalAddress $clientmac] DesIpv6 ff3f::1 DesAddrModev6 IncrHost DesNetworkv6 96 DesNumv6 300 \
#              ProtoclEx mld MldVersion 1 Type report MldGroupAddress ff3f::1 MldGroupNum 300
#
#v1版本的done
#SetIxiaStream Host $host Card $Card1 Port $Port1 StreamRateMode Fps StreamRate 10 \
#              SouMac $clientmac DesMac 33-33-00-00-00-01 \
#              Protocl ipv6 EthernetType ethernetII \
#              SouIpv6 [GetLinkLocalAddress $clientmac] DesIpv6 ff02::2 \
#              ProtoclEx mld MldVersion 1 Type done MldGroupAddress ff3f::1
#
#指定组源查询格式
#SetIxiaStream Host $host Card $Card1 Port $Port1 StreamRateMode Fps StreamRate 10 \
#              SouMac $vlanmac DesMac 33-33-00-00-00-01 \
#              Protocl ipv6 EthernetType ethernetII \
#              SouIpv6 :: DesIpv6 ff02::1 \
#              ProtoclEx mld MldVersion 2 Type query MldGroupAddress ff3f::1 MldSourceIpAddress "3000::1 3000::2"
#
#v2版本的report
#一个组，多个源，最多带88个源
#SetIxiaStream Host $host Card $Card1 Port $Port1 StreamRateMode Fps StreamRate 10 \
#              SouMac $clientmac DesMac 33-33-00-00-00-16 \
#              Protocl ipv6 EthernetType ethernetII \
#              SouIpv6 [GetLinkLocalAddress $clientmac] DesIpv6 ff02::16 \
#              ProtoclEx mld MldVersion 2 Type report MldGroupRecord {{ff3f::1 include "3000::1 3000::2"} \
#              {ff3f::2 exclude "3000::1 3000::2"} {ff3f::3 toinclude "3000::1 3000::2"} \
#              {ff3f::4 toexclude "3000::1 3000::2"} {ff3f::5 allow "3000::1 3000::2"} \
#              {ff3f::6 block "3000::1 3000::2"}}
#端口环路检测报文:  要求板卡如果在08的机器上，必须在前4个槽位
#SetIxiaStream Host $host Card $Card1 Port $Port1 StreamRateMode Fps StreamRate 1 \
#              SouMac $cpumac DesMac ff-ff-ff-ff-ff-ff EthernetType loopback \
#              LoopbackDetectionInfo {10 Ethernet1/1}
#SetIxiaStream Host $host Card $Card1 Port $Port1 StreamRateMode Fps StreamRate 1 \
#              SouMac $cpumac DesMac ff-ff-ff-ff-ff-ff EthernetType loopback \
#              LoopbackDetectionInfo {10 Ethernet1/1 0x1234}
#SetIxiaStream Host $host Card $Card1 Port $Port1 StreamRateMode Fps StreamRate 1 \
#              SouMac $cpumac DesMac ff-ff-ff-ff-ff-ff EthernetType loopback \
#              LoopbackDetectionInfo {10 Ethernet1/1 0xDC09 128}
#同时发送多种流量
#SetIxiaStream Host 172.16.1.253 Card 4 Port 1 StreamMode 0 LastStreamFlag false \
#              StreamNum 1 StreamRateMode Bps StreamRate 50 TransmitMode advancedstreams \
#              SouMac 00-00-00-00-00-01 DesMac 00-00-00-00-00-02
#SetIxiaStream Host 172.16.1.253 Card 4 Port 1 StreamMode 0 LastStreamFlag true \
#              StreamNum 2 StreamRateMode Bps StreamRate 100 TransmitMode advancedstreams \
#              SouMac 00-00-00-00-00-01 DesMac 00-00-00-00-00-05
#Mrpp报文:
#1、mrpp hello报文：可以修改目的mac、control-vlan、mrpp-type
#2、linkdown报文：可以修改目的mac、control-vlan
#3、ring-up-flush-fdb报文：可以修改目的mac、control-vlan
#4、ring-down-flush-fdb：可以修改目的mac、control-vlan
#SetIxiaStream Host $host Card $Card1 Port $Port1 StreamRateMode Fps StreamRate 1 \
#              SouMac $cpumac DesMac 00-03-0f-00-00-06 EthernetType mrpp \
#              MrppPacketInfo {health 100 $cpumac 1 3 idle}
#SetIxiaStream Host $host Card $Card1 Port $Port1 StreamRateMode Fps StreamRate 1 \
#              SouMac $cpumac DesMac 00-03-0f-00-00-06 EthernetType mrpp \
#              VlanTagFlag 1 VlanId 3 UserPriority 5 \
#              MrppPacketInfo {health 100 $cpumac 1 3 idle}
#MrppPacketInfo : {MrppType CtrlVlanId SystemMacAddr HelloTimer FailTimer State}
#mrpptype : health/ring-up-flush-fdb/ring-down-flush-fdb/link-down
#state : idle/complete/failed/link-up/link-down/pre-forwarding
#
#Gre隧道报文配置举例:
#1.ipv6封装ipv4 tcp报文，内层tcp源端口23，目的端口24:
#SetIxiaStream Host 172.16.1.251 Card 3 Port 3 Protocl ipv6 ProtoclEx gre \
#			 GreInnerProtocol ipv4 GreInnerSouIp 100.1.1.10 GreInnerDesIp 200.1.1.1 \
#			 GreInnerProtocolEx tcp greSPort 23 greDPort 24 \
#			 SouIpv6 2001::1 DesIpv6 2003::2
#
#2.ipv6封装ipv6 udp报文，内层udp源端口67，目的端口68:
#SetIxiaStream Host 172.16.1.251 Card 3 Port 3 Protocl ipv6 ProtoclEx gre \
#              GreInnerProtocol ipv6 GreInnerSouIpv6 2020::2 GreInnerDesIpv6 2050::3 \
#              GreInnerProtocolEx udp greSPort 67 greDPort 68 \
#		SouIpv6 2001::1 DesIpv6 2003::2
#
#3.ipv4封装ipv4 icmp报文，内层icmp type为8：
#SetIxiaStream Host 172.16.1.251 Card 3 Port 3 Protocl ipv4 ProtoclEx gre \
#              GreInnerProtocol ipv4 GreInnerSouIp 10.1.1.1 GreInnerDesIp 20.1.1.133 \
#		GreInnerProtocolEx icmp greType 8
#
#4.ipv4封装ipv6 icmp报文，内层icmp type为128：
#SetIxiaStream Host 172.16.1.251 Card 3 Port 3 Protocl ipv4 ProtoclEx gre \
#              GreInnerProtocol ipv6 GreInnerSouIpv6 2001::1 GreInnerDesIpv6 2002::1 \
#              GreInnerProtocolEx icmpv6 GreInnerIcmpv6Type 128

proc SetIxiaStream { args } {	
	set Host 100.1.1.222
	set Card 8
	set Port 1
	#########---Control---######################
	set StreamNum 1
	set LastStreamFlag true
	set ReturnToId 1
	set RateMode auto
	set FlowControl false	
	set TransmitMode packetstreams   ;#packetstreams   advancedstreams   echo
	set StreamMode 0                 ;#0:contine   1:stop after send    2:more than one stream on one port
	set StreamRateMode PercentRate   ;#PercentRate/Fps/Bps
	set StreamRate 100               ;#100/148810/76190476
	set NumFrames 100
	#########---Layer-2---######################
	set SouMac 00-00-00-00-00-01
	set SouMask ff-ff-ff-ff-ff-ff
	set SouNum 1
	set SouMode increment
	set DesMac 00-00-00-00-00-02
	set DesMask ff-ff-ff-ff-ff-ff
	set DesNum 1
	set DesMode increment
	set FrameSizeType fixed  ;#fixed / random / incr / auto
	set FrameSize 128
	set FrameSizeStep 1
	set FrameSizeMin 64
	set FrameSizeMax 1518
	set FrameErrors 0      ;#0(streamErrorGood),1(streamErrorAlignment),2(streamErrorDribble),
	                       ;#3(streamErrorBadCRC),4(streamErrorNoCRC)	
	set PatternType incrByte   ;#incrByte,incrWord,decrByte,decrWord,patternTypeRandom,repeat,nonRepeat
	set DataPattern x00010203  ;#dataPatternRandom,allOnes,allZeroes,xAAAA,x5555,x7777,xDDDD,xF0F0,x0F0F,
	                           ;#xFF00FF00,x00FF00FF,xFFFF0000,x0000FFFF,x00010203,x00010002,xFFFEFDFC,
	                           ;#xFFFFFFFE,x7E7E7E7E,x4747476B,userpattern
	set Pattern "00 01 02 03"
	set FrameType ""
	#########---User-DEF---######################
	set UDF1Flag 0
	set Offset1 12
	set Length1 1
	set Value1 0
	set ContinueFlag1 false
	set Repeat1 1
	set Step1 1
	set IncreaseMode1 up
	set UDF2Flag 0
	set Offset2 12
	set Length2 1
	set Value2 0
	set ContinueFlag2 false
	set Repeat2 1
	set Step2 1
	set IncreaseMode2 up
	set UDF3Flag 0
	set Offset3 12
	set Length3 1
	set Value3 0
	set ContinueFlag3 false
	set Repeat3 1
	set Step3 1
	set IncreaseMode3 up
	set UDF4Flag 0
	set Offset4 12
	set Length4 1
	set Value4 0
	set ContinueFlag4 false
	set Repeat4 1
	set Step4 1
	set IncreaseMode4 up
	#########---Vlan---######################
	#VlanTagFlag 0:no vlan tag  1:exist one vlan tag  2:exist two vlan tag
	set VlanTagFlag 0
	set VlanId 3
	set Tpid 8100
	set UserPriority 5
	set VlanMode vIdle     ;#vIdle/vIncrement/vDecrement
	set VlanNum 1
	set VlanStep 1
	set IfTpid 0
	set Tpid1 9100
	set VlanId1 2
	set Tpid2 9200
	set VlanId2 3
	#########---mpls---######################
	#MplsTagFlag MplsLabel MplsBottom MplsExp MplsTtl
	set MplsTagFlag 0
	set MplsLabel 40
	set MplsBottom true    ;#true/false
	set MplsExp 7
	set MplsTtl 64 
	#########---Protocol---######################
	set Protocl none          ;#ipv4/arp/ipv6/ipv6ipv4
	set EthernetType noType   ;#ethernetII/ieee8023snap/ieee8023/ieee8022          loopback/mrpp/stp/rstp/mstp/cluster
	set EthernetTypeFlag 0
	set EthernetTypeNum 0
	#########---Protocol-IP---######################
	set SouIp 1.1.1.1
	set SouMask 255.255.255.0
	set SouClassMode classC
	set SouIpMode ipIncrHost
	set SouIpNum 1
	set DesIp 2.2.2.2
	set DesMask 255.255.255.0
	set DesClassMode classC
	set DesIpMode ipIncrHost
	set DesIpNum 1
	set Fragment 0
	set LastFragment 0
	set FragmentOffset 0
	set LengthOverride false
	set TTL 64
	set TotalLength [expr $FrameSize - 18]
	set ValidChecksum true
	#########---advanced protocl---######################
	set ProtoclEx none  ;#none/tcp/udp/icmp/igmp/mld/gre/Ipv4vrrp
	set SPort 0
	set DPort 0

	#added by zhangfank,2010.7.9
	set greSPort 0
	set greDPort 0
	#end
	
	set SequenceNum 0
	set HeaderLength 5
	set Type 0
	set Code 0

	#added by zhangfank,2010.7.9
	set greType 0
	set greCode 0
	#end
	
	set IgmpVersion 2
	set IgmpGroupAddress 0.0.0.0
	set IgmpSourceIpAddress 0.0.0.0
	set IgmpMode igmpIdle
	set IgmpRepeat 1
	set IgmpGroupRecord NULL
	set ValidChecksum true
	set MaxResponseTime 100
	set QQIC 0
	set QRV 0
	set EnableS false
	set ACK false
	set FIN false
	set PSH false
	set RST false
	set URG false
	set SYN false
	
	set greACK false
	set greFIN false
	set grePSH false
	set greRST false
	set greURG false
	set greSYN false
	
	set MldVersion 1
	set MldMaxResponseDelay 2710
	set MldGroupAddress ::
	set MldGroupNum 1
	set MldSourceIpAddress ::
	set MldGroupRecord NULL 
	#########---loopbackdetection#####
	set LoopbackDetectionInfo NULL
	#########---mrpp-packet#####
	set MrppPacketInfo NULL
	set LLDPPacketInfo NULL
	set ULDPPacketInfo NULL
	#########---Arp---######################
	set ArpOperation 1    ;#1 request 2 reply
	set SenderMac 00-00-00-00-00-01
	set SenderMacMode Increment
	set SenderMacNum 1
	set TargetMac 00-00-00-00-00-02
	set TargetMacMode Increment
	set TargetMacNum 1
	set SenderIp 1.1.1.1
	set SenderIpNum 1
	set SenderIpMode increment
	set TargetIp 2.2.2.2
	set TargetIpNum 1
	set TargetIpMode increment
	#########---IPv6---######################
	set SouIpv6    2003:0001:0002:0003:0000:0000:0000:0003
	set SouAddrModev6 Fixed    ;#Fixed/IncrHost/IncrSiteNetwork/IncrNextLevelNetwork/IncrTopLevelNetwork
	                           ;#DecrHost/DecrSiteNetwork/DecrNextLevelNetwork/DecrTopLevelNetwork
	set SouStepSizev6 1
	set SouNumv6   1
	set SouNetworkv6 64
	set DesIpv6    2003:0001:0002:0003:0000:0000:0000:0004
	set DesAddrModev6 Fixed    ;#Fixed/IncrHost/IncrSiteNetwork/IncrNextLevelNetwork/IncrTopLevelNetwork
	                           ;#DecrHost/DecrSiteNetwork/DecrNextLevelNetwork/DecrTopLevelNetwork
	set DesStepSizev6 1
	set DesNumv6   1
	set DesNetworkv6 64
	#########---Other---######################
	set PriorityFlag 1  ;#1:Dscp 0:Tos 2:Ipprecedence 3:Ipprecedence&Tos
	set Dscp 0
	set Tos 4
	set Ipprecedence 7
	set TrafficClass 3
	set FlowLabel 0
	set HopLimit 255
    set NextHeader ipV6NoNextHeader
    set Action set
	########---dhcp---###################
    set OpCode dhcpBootReply
    set HardwareAddressLength 6
    set Hops 0
    set TransactionID 0
	set YourIpAddr 10.1.1.4
	set ClientHwAddr "00 00 00 00 00 01 00 00 00 00 00 00 00 00 00 00"
	set DhcpMessageType 2
	set DhcpSvrIdentifier 10.1.1.1
	set DhcpIPAddrLeaseTime 120
	set DhcpRenewalTimeValue 60
	set DhcpRebindingTimeValue 105
	set DhcpSubnetMask 255.255.255.0
	set ClientIpAddr 10.1.1.4
	set DhcpClientId "01 00 00 00 00 00 01"
	set DhcpParamRequestList "01 03 3A 3B"
	set DhcpRequestedIPAddr 10.1.1.4
	#under this line && upon the line which is "add by liangdong" == add by qiaoyua
	set Ipv6NdpNaPacketInfo NULL
	set Ipv6NdpNsPacketInfo NULL
	set Ipv6NdpNaMaxPacketInfo NULL
	set Ipv6NdpRedirectPacketInfo NULL
	set Sequence 0
	set RipCommand 1
	set RipVersion 2
	set RipRoute ""
	set RipngCommand 1
	set RipngRoute ""
	#ipv6 ra -- add by liangdong
	set Ipv6RAPacketInfo NULL
	#ipv6 rs --- add by zouleia
	set Ipv6RSPackteInfo NULL

	##################### GRE ####################
	set GreInnerProtocol "00 00"	;#ipv4,ipv6
	set GreInnerProtocolEx none
	set GreInnerIcmpv6Type 1
	set GreInnerSouIp 1.1.1.1
	set GreInnerSouMask 255.255.255.0
	set GreInnerDesIp 2.2.2.2
	set GreInnerDesMask 255.255.255.0

	set GreInnerSouIpv6 2003:0001:0002:0003:0000:0000:0000:0001
	set GreInnerSouMaskv6 64
	set GreInnerDesIpv6 2003:0001:0002:0003:0000:0000:0000:0002
	set GreInnerDesMaskv6 64
	
	set GreHeaderReserved0 "00 00"
	
	####参数解析部分#############################################
	array set arrArgs $args 	
  	foreach {para value} [array get arrArgs] {
		#puts "para=$para"
		#puts "value =$value"  	
		switch -exact -- $para {
		    Host {
		    	set Host $value
		    }
		    Card {
		   		set Card $value
		   	}
		   	Port { 
		   		set Port $value
		   	}
		   	StreamNum {
		   	    set StreamNum $value
		   	}
		   	LastStreamFlag {
		   	    set LastStreamFlag $value
		   	}
		   	ReturnToId {
		   	    set ReturnToId $value
		   	}
		   	RateMode { 
		   		set RateMode $value
		   	}
		   	FlowControl {
		   	    set FlowControl $value
		   	}
		   	TransmitMode {
		   		set TransmitMode $value
		   	}
		   	StreamMode { 
				set StreamMode $value
		   	}
		   	StreamRateMode {
		   	    set StreamRateMode $value
		   	}
		   	StreamRate {
		   		set StreamRate $value  
		   	}
		   	NumFrames {
		   		set NumFrames $value
		   	}
		   	SouMac { 
		   		set SouMac $value
		   	}
		   	SouMask {
		   		set SouMask $value
		   	}
		   	SouNum { 
		   		set SouNum $value  
		   	}
		   	SouMode {
		   		set SouMode $value
		   	}
		   	DesMac { 
		   		set DesMac $value
		   	}
		   	DesMask {
		   		set DesMask $value
		   	}
		   	DesNum { 
		   		set DesNum $value
		   	}
		   	DesMode {
		   		set DesMode $value
		   	}
		   	FrameSizeType {
		   		set FrameSizeType $value
		   	}
		   	FrameSize {
		   		set FrameSize  $value
		   	}
		   	FrameSizeStep {
		   		set FrameSizeStep $value
		   	}
		   	FrameSizeMin {
		   		set FrameSizeMin $value
		   	}
		   	FrameSizeMax {
		   		set FrameSizeMax $value
		   	}
		   	FrameErrors {
		   	    set FrameErrors $value
		   	}
		   	PatternType {
		   		set PatternType $value
		    }
		    DataPattern {
		    	set DataPattern $value
		    }
		    Pattern {
		    	set Pattern $value
		    }
		   	UDF1Flag {
		   		set UDF1Flag  $value
		   	}
		   	Offset1 {
		   		set Offset1  $value
		   	}
		   	Length1 {
		   		set Length1  $value
		   	}
		   	Value1 {
		   		set Value1  $value
		   	}
		   	ContinueFlag1 {
		   	    set ContinueFlag1 $value
		   	}
		   	Repeat1 {
		   	    set Repeat1 $value
		   	}
		   	Step1 {
		   		set Step1 $value
		   	}
		   	IncreaseMode1 {
		   		set IncreaseMode1 $value
		   	}
		   	UDF2Flag {
		   		set UDF2Flag  $value
		   	}
		   	Offset2 {
		   		set Offset2  $value
		   	}
		   	Length2 {
		   		set Length2  $value
		   	}
		   	Value2 {
		   		set Value2  $value
		   	}
		   	ContinueFlag2 {
		   	    set ContinueFlag2 $value
		   	}
		   	Repeat2 {
		   	    set Repeat2 $value
		   	}
		   	Step2 {
		   		set Step2 $value
		   	}
		   	IncreaseMode2 {
		   		set IncreaseMode2 $value
		   	}
		   	UDF3Flag {
		   		set UDF3Flag  $value
		   	}
		   	Offset3 {
		   		set Offset3  $value
		   	}
		   	Length3 {
		   		set Length3  $value
		   	}
		   	Value3 {
		   		set Value3  $value
		   	}
		   	ContinueFlag3 {
		   	    set ContinueFlag3 $value
		   	}
		   	Repeat3 {
		   	    set Repeat3 $value
		   	}
		   	Step3 {
		   		set Step3 $value
		   	}
		   	IncreaseMode3 {
		   		set IncreaseMode3 $value
		   	}
		   	UDF4Flag {
		   		set UDF4Flag  $value
		   	}
		   	Offset4 {
		   		set Offset4  $value
		   	}
		   	Length4 {
		   		set Length4  $value
		   	}
		   	Value4 {
		   		set Value4  $value
		   	}
		   	ContinueFlag4 {
		   	    set ContinueFlag4 $value
		   	}
		   	Repeat4 {
		   	    set Repeat4 $value
		   	}
		   	Step4 {
		   		set Step4 $value
		   	}
		   	IncreaseMode4 {
		   		set IncreaseMode4 $value
		   	}
		   	VlanTagFlag {
		   		set VlanTagFlag  $value
		   	}
		   	VlanId {
		   		set VlanId  $value
		   	}
		   	Tpid {
		   		set Tpid $value
		   		set IfTpid 1
		   	}
		   	UserPriority {
		   		set UserPriority  $value
		   	}
		   	VlanMode {
		   	    set VlanMode $value
		   	}
		   	VlanNum {
		   	    set VlanNum $value
		   	}
		   	VlanStep {
		   	    set VlanStep $value
		   	}
		   	Tpid1 {
		   		set Tpid1 $value
		   	}
		   	VlanId1 {
		   		set VlanId1 $value
		   	}
		   	Tpid2 {
		   		set Tpid2 $value
		   	}
		   	VlanId2 {
		   		set VlanId2 $value
		   	}

		   	MplsTagFlag {
		   		set MplsTagFlag $value
		   	}
		   	MplsLabel {
		   		set MplsLabel $value
		   	}
		   	MplsBottom {
		   		set MplsBottom $value
		   	}
		   	MplsExp {
		   		set MplsExp $value
		   	}
		   	MplsTtl {
		   		set MplsTtl $value
		   	}		   	
		   	Protocl {
		   		set Protocl   $value
		   	}
		   	EthernetType {
		   		set EthernetType $value
		   	}
		   	EthernetTypeFlag {
		   		set EthernetTypeFlag $value
		   	}
		   	EthernetTypeNum {
		   		set EthernetTypeNum $value
		   	}
		   	SouIp {
		   		set SouIp   $value
		   	}
		   	SouMask {
		   		set SouMask   $value
		   	}
		   	SouClassMode {
		   		set SouClassMode $value
		   	}
		   	SouIpMode {
		   		set SouIpMode $value
		   	}
		   	SouIpNum {
		   		set SouIpNum   $value
		   	}		   
		   	DesIp {
		   		set DesIp $value
		   	}
		   	DesMask {
		   		set DesMask $value
		   	}
		   	DesClassMode {
		   		set DesClassMode $value
		   	}
		   	DesIpMode {
		   		set DesIpMode $value
		   	}
		   	DesIpNum { 
				set DesIpNum $value
			}
			Fragment {
			    set Fragment $value
			}
			LastFragment {
			    set LastFragment $value
			}
			FragmentOffset {
			    set FragmentOffset $value
			}
			LengthOverride {
			    set LengthOverride $value
			}
			TTL {
				set TTL $value
			}
			TotalLength {
			    set TotalLength $value
			}
			ValidChecksum {
				set ValidChecksum $value
			}
			ProtoclEx {
				set ProtoclEx $value
			}
			SPort {
				set SPort $value
			}
			greSPort {
				set greSPort $value
			}	
			DPort {
				set DPort $value
			}
			greDPort {
				set greDPort $value
			}	
			SequenceNum {
			    set SequenceNum $value
			}
			HeaderLength {
			    set HeaderLength $value
			}
			Type {
				set Type $value
			}
			greType {
				set greType $value
			}	
			Code {
				set Code $value
			}
			greCode {
				set greCode $value
			}	
			IgmpVersion {
				set IgmpVersion $value
			}
			IgmpGroupAddress {
				set IgmpGroupAddress $value
			}
			IgmpSourceIpAddress {
			    set IgmpSourceIpAddress $value
			}
			IgmpMode {
			    set IgmpMode $value
			}
			IgmpRepeat {
			    set IgmpRepeat $value
			}
			IgmpGroupRecord {
			    set IgmpGroupRecord $value
			}
			ValidChecksum {
			    set ValidChecksum $value
			}
			MaxResponseTime {
			    set MaxResponseTime $value
			}
			QQIC {
			    set QQIC $value
			}
			QRV {
			    set QRV $value
			}
			EnableS {
			    set EnableS $value
			}
			ACK {
				set ACK $value
			}
			greACK {
				set greACK $value
			}	
			FIN {
				set FIN $value
			}
			greFIN {
				set greFIN $value
			}	
			PSH {
				set PSH $value
			}
			grePSH {
				set grePSH $value
			}	
			RST {
				set RST $value
			}
			greRST {
				set greRST $value
			}	
			URG {
				set URG $value
			}
			greURG {
				set greURG $value
			}	
			SYN {
				set SYN $value
			}
			greSYN {
				set greSYN $value
			}	
			MldVersion {
				set MldVersion $value
			}
			Icmpv6CheckSum {
				set Icmpv6CheckSum $value
			}
			MldMaxResponseDelay {
				set MldMaxResponseDelay $value
			}
			MldGroupAddress {
				set MldGroupAddress $value
			}
			MldGroupNum {
				set MldGroupNum $value
			}
			MldSourceIpAddress {
				set MldSourceIpAddress $value
			}
			MldGroupRecord {
				set MldGroupRecord $value
			}
			LoopbackDetectionInfo {
				set LoopbackDetectionInfo $value
			}
			MrppPacketInfo {
				set MrppPacketInfo $value
			}
			StpPacketInfo {
				set StpPacketInfo $value
			}
			MstpPacketInfo {
				set MstpPacketInfo $value
			}
			RstpPacketInfo {
				set RstpPacketInfo $value
			}
			ClusterPacketInfo {
				set ClusterPacketInfo $value
			}
		   	PriorityFlag { 
		   		set PriorityFlag $value
		   	}
		   	Dscp { 
		   		set Dscp $value
		   	}
		   	Tos { 
		   		set Tos $value
		   	}
		   	Ipprecedence {
		   		set Ipprecedence $value
		   	}
		   	ArpOperation { 
		   		set ArpOperation $value
		   	} 
		   	SenderMac { 
		   		set SenderMac $value
		   	} 
		   	SenderMacMode {
		   		set SenderMacMode $value
		   	}
		   	SenderMacNum { 
		   		set SenderMacNum $value
		   	}
		   	TargetMac { 
		   		set TargetMac $value
		   	}
		   	TargetMacMode {
		   		set TargetMacMode $value
		   	}
		   	TargetMacNum { 
		   		set TargetMacNum $value
		   	}
		   	SenderIp { 
		   		set SenderIp $value
		   	}
		   	SenderIpMode {
		   		set SenderIpMode $value
		   	}
		   	SenderIpNum { 
		   		set SenderIpNum $value
		   	}
		   	TargetIp { 
		   		set TargetIp $value
		   	}
		   	TargetIpMode {
		   		set TargetIpMode $value
		   	}
		   	TargetIpNum { 
		   		set TargetIpNum $value
		   	}
		   	SouIpv6 { 
		   	    set SouIpv6 [ FormatIpv6 $value ]
		   	}
		   	SouAddrModev6 { 
		   		set SouAddrModev6 $value
		   	}
		   	SouStepSizev6 {
		   		set SouStepSizev6 $value
		   	}
		   	SouNumv6 { 
		   		set SouNumv6 $value
		   	}
		   	SouNetworkv6 {
		   	    set SouNetworkv6 $value
		   	}
		   	DesIpv6 { 
		   		set DesIpv6 [ FormatIpv6 $value ]
		   	}
		   	DesAddrModev6 { 
		   		set DesAddrModev6 $value
		   	}
		   	DesStepSizev6 {
		   		set DesStepSizev6 $value
		   	}
		   	DesNumv6 { 
		   		set DesNumv6 $value
		   	}
		   	DesNetworkv6 {
		   	    set DesNetworkv6 $value
		   	}
		   	TrafficClass { 
		   		set TrafficClass $value
		   	}
		   	FlowLabel { 
		   		set FlowLabel $value
		   	}
		   	HopLimit {
		   		set HopLimit $value
		    }
		   	NextHeader { 
		   		set NextHeader $value
		   	}	
		   	Action {
		   	    set Action $value
		   	}
		   	OpCode {
		   	    set OpCode $value
		   	}
		   	HardwareAddressLength {
		   	    set HardwareAddressLength $value
		   	}
		   	Hops {
		   	    set Hops $value
		   	}
		   	TransactionID {
		   	    set TransactionID $value
		   	}
		   	ClientIpAddr {
		   	    set ClientIpAddr $value
		   	}
		   	DhcpClientId {
		   	    set DhcpClientId $value
		   	}
		   	YourIpAddr {
		   	    set YourIpAddr $value
		   	}
		   	ClientHwAddr {
		   	    set ClientHwAddr $value
		   	}
		   	DhcpMessageType {
		   	    set DhcpMessageType $value
		   	}
		   	DhcpSvrIdentifier {
		   	    set DhcpSvrIdentifier $value
		   	}
		   	DhcpParamRequestList {
		   	    set DhcpParamRequestList $value
		   	}
		   	DhcpIPAddrLeaseTime {
		   	    set DhcpIPAddrLeaseTime $value
		   	}
		   	DhcpRenewalTimeValue {
		   	    set DhcpRenewalTimeValue $value
		   	}
		   	DhcpRebindingTimeValue {
		   	    set DhcpRebindingTimeValue $value
		   	}
		   	DhcpSubnetMask {
		   	    set DhcpSubnetMask $value
		   	}
		   	Ipv6CheckSum {
		   	#添加Ipv6CheckSum变量,add by zhangfank
		   	    set Ipv6CheckSum $value
            }
            #under this line && upon the line which is "Ipv6RAPacketInfo" == add by qiaoyua
		   	Ipv6NdpNaPacketInfo {
            #添加NDP NA报文选项
				set Ipv6NdpNaPacketInfo $value
            }
            Ipv6NdpNaMaxPacketInfo {
            #添加NDP NA单流打满表项的选项
                set Ipv6NdpNaMaxPacketInfo $value
            }
            Sequence {
            #添加Icmp报文中的sequence选项
            	set Sequence $value
            }
            RipCommand {
            #添加Rip报文中的命令选项
            	set RipCommand $value
            }
            RipVersion {
            #添加Rip报文中的版本选项
            	set RipVersion $value
            }
            RipRoute {
            #添加Rip报文中的路由条目的选项
            	set RipRoute $value
            }
            RipngCommand {
            #添加Ripng报文中的命令选项
            	set RipngCommand $value
            }
            RipngRoute {
            #添加Ripng报文中的路由条目的选项
            	set RipngRoute $value
            }
            Ipv6NdpNsPacketInfo {
            #添加NDP NS报文选项
				set Ipv6NdpNsPacketInfo $value
            }
            Ipv6NdpRedirectPacketInfo {
            #添加NDP Redirect报文选项
				set Ipv6NdpRedirectPacketInfo $value
            }
            Ipv6RAPacketInfo {
            	set Ipv6RAPacketInfo $value
            }
            #NDP RS,add by zouleia
            Ipv6RSPacketInfo {
				set Ipv6RSPacketInfo $value
            }
            LLDPPacketInfo {
            	set LLDPPacketInfo $value
            }
            ULDPPacketInfo {
            	set ULDPPacketInfo $value
            }
            GreInnerProtocol {
            	set GreInnerProtocol $value
            }
            GreInnerProtocolEx {
            	set GreInnerProtocolEx $value
            }	
            GreInnerSouIp {
            	set GreInnerSouIp $value
            }
            GreInnerSouMask {
            	set GreInnerSouMask $value
            }
            GreInnerDesIp {
            	set GreInnerDesIp $value
            }
            GreInnerDesMask {
            	set GreInnerDesMask $value
            }
            GreHeaderReserved0 {
            	set GreHeaderReserved0 $value
            }
            GreInnerSouIpv6 {
            	set GreInnerSouIpv6 $value
            }
            GreInnerDesIpv6 {
            	set GreInnerDesIpv6 $value
            }
            GreInnerSouMaskv6 {
            	set GreInnerSouMaskv6 $value
            }
            GreInnerDesMaskv6 {
            	set GreInnerDesMaskv6 $value
            }
            GreInnerIcmpv6Type {
            	set GreInnerIcmpv6Type $value
            }
            Ipv4VrrpInfo {
                set Ipv4VrrpInfo $value
            }
            Ipv6VrrpInfo {
                set Ipv6VrrpInfo $value
            }
		   	default {
		   		puts "Wrong para name:$para "
		   		return -1	
		   	}
		}  			
	}

############################# 添加icmpv6-fragment1 ############################################
##added by zhangfank,2009-05-05
##用于icmpv6分片报文的第一片的配置，需要有icmpv6的头
    if { $ProtoclEx == "icmpv6-fragment1" } {
        set TrafficClass 3
        set HopLimit 255
        set FrameSize $FrameSize
        set n1 [ string range $Ipv6CheckSum 0 1 ]
        set n2 [ string range $Ipv6CheckSum 2 3 ]
        #set Icmpv6CheckSum [FormatHex [CalcIcmpv6CheckSum $SouIpv6 $DesIpv6 [expr 8 + ($FrameSize - 74] "82 00 00 00 00 00 00 00 [string repeat {AA } [expr $FrameSize - 75]] AA"]]
		#由于checksum的计算需要考虑整个数据包的DATA，所以不能仅根据第一个分片计算
        set UDF1Flag 1
        set Offset1 62
        set Length1 1
        set Value1 80
        set ContinueFlag1 false
        set Repeat1 1
        #修改校验和
        set UDF2Flag 1
        set Offset2 64
        set Length2 2
        set Value2 "$n1 $n2"
        #set Value2 $Icmpv6CheckSum
#        puts $Value2
        set ContinueFlag2 false
        set Repeat2 1
        set PatternType repeat
        set DataPattern userpattern
        set Pattern "AA"
#        puts $Pattern
    }        
############################# 添加icmpv6-fragment2 ############################################
##added by zhangfank,2009-05-06
##用于icmpv6分片报文的非第一分片的配置，不包含icmpv6头，需要修改数据部分，与第一分片一致。
    if { $ProtoclEx == "icmpv6-fragment2" } {
        set PatternType repeat
        set DataPattern userpattern
        set Pattern "AA"
#        puts $Pattern
        set UDF1Flag 1
        set Offset1 54
        set Length1 1
        set Value1 3B 
#        puts $Value1
        set ContinueFlag1 false
        set Repeat1 1
    } 
    
    
################################添加ipv6ndpna################################
#added by qiaoyua, 2009-08-13
#用于构造Ipv6 NDP NA报文(由于IXIA没有提供icmpv6内部具体配置的接口，只能采用构造
#	icmpv6 type为1的报文，然后按照实际报文格式手动编写后续数据，最后以数据的形
#	式传入报文
#SetIxiaStream Host $testerip Card $Card1 Port $Port1 StreamRateMode Fps StreamRate 1 Action change \
#              SouMac 00-00-00-00-00-10 DesMac $vlanmacs1 \
#              Protocl ipv6 SouIpv6 2001::10 SouNetworkv6 64 DesIpv6 2001::1 DesNetworkv6 64 \
#              ProtoclEx ipv6ndpna Ipv6NdpNaPacketInfo [list FlagR 0 FlagS 1 FlagO 1 Ipv6Addr 2001::10 Mac 00-00-00-00-00-10 NoOption 0]
    if { $ProtoclEx == "ipv6ndpna" && $Ipv6NdpNaPacketInfo != "NULL" } {
		#将ProtoclEx设置回icmpV6，使ipv6报文nextheader字段变为58(icmpv6)
		set ProtoclEx icmpV6

        array set arr $Ipv6NdpNaPacketInfo

		set FrameSize 90
		#如果NoOption为1，则报文长度为82(NoOption为1表示NA报文不携带Destination Link-layer Option)
		if [info exists arr(NoOption)] {
			if {$arr(NoOption) == 1} {
				set FrameSize 82
			}
		}
		
   	 	if [info exist arr(FlagR)] {
    		set r $arr(FlagR)
    	} else {
			return -1
    	}
    	if [info exist arr(FlagS)] {
    		set s $arr(FlagS)
    	} else {
			return -1
    	}
    	if [info exist arr(FlagO)] {
    		set o $arr(FlagO)
    	} else {
			return -1
    	}
    	#三个标志位组合，得出具体值
		set rso [format %02X [expr ($r << 7) + ($s << 6) + ($o << 5)]]
		set UDF2Flag 1
   	 	set Offset2 58
   		set Length2 4
    	set Value2 "$rso 00 00 00"
    	set ContinueFlag2 false
		set Repeat2 1 
		#调用FormatIpv6NdpNaSegment函数填写数据字段
		set PatternType nonRepeat
		set DataPattern userpattern
		set Pattern [FormatIpv6NdpNaSegment arr]
		#UDF1设置icmpv6 type值为0x88(十进制为136)
        set UDF1Flag 1
    	set Offset1 54
    	set Length1 4
    	set Icmpv6CheckSum [FormatHex [CalcIcmpv6CheckSum $SouIpv6 $DesIpv6 [expr 8 + ([string length $Pattern] + 1) / 3] "88 00 00 00 $Value2 $Pattern"]]
    	set Value1 "88 00 $Icmpv6CheckSum"
		set ContinueFlag1 false
		set Repeat1 1 
	}
	
################################添加ipv6ndpna################################
#added by qiaoyua, 2009-09-3
#ipv6ndpnamax选项目的是为打满ipv6 neighbors表项，由于通过创建ipv6 interface发送RS报文对updateprotect
#命令不起作用，故采用此选项采取的构造大量连续NA报文来达到目的。
#实际使用参数为 
#SetIxiaStream Host 172.16.1.253 Card 2 Port 1 StreamRateMode Fps StreamRate 100 Action change \
#              SouMac 00-00-00-00-00-10 SouNum 16500 DesMac 00-03-0F-0E-43-2B \
#              Protocl ipv6 SouIpv6 2001:1111:1111:1111:1111:1111:1111:10 DesIpv6 2001::1 \
#              ProtoclEx ipv6ndpnamax Ipv6NdpNaMaxPacketInfo [list Ipv6Addr 2001:1111:1111:1111:1111:1111:1111:10 Mac 00-00-00-00-00-10 Ipv6Last16Bit "00 10" MacLast16Bit "00 10" Num 16500]
#SetIxiaStream Host 172.16.1.253 Card 2 Port 1 StreamRateMode Fps StreamRate 100 Action change \
#              SouMac 00-00-00-00-00-10 SouNum 16500 DesMac 00-03-0F-0E-43-2B \
#              Protocl ipv6 SouIpv6 2001:1111:1111:1111:1111:1111:1111:10 DesIpv6 2001::1 \
#              ProtoclEx ipv6ndpnamax Ipv6NdpNaMaxPacketInfo [list Num 16500]
#解释:由于有CPU限速，每秒100个报文是zoma默认设置的值，发送速率定位100每秒。Ipv6源目的地址不要改动，这是
#因为ixia不提供icmpv6的脚本支持，所以Icmpv6报头的checksum值需要我们自己设置。而NA报文的checksum与Ipv6源
#目的地址均相关，在实际实现中根据Icmpv6报头中的Ipv6地址以及mac自动算出
#Ipv6NdpNaMaxPacketInfo后面的参数:Ipv6Addr Icmpv6报头中需要填写的Ipv6地址
#                                 Mac Icmpv6报头中可选字段Destination Link Layer中需要填写的Mac地址
#                                 Ipv6Last16Bit Ipv6源地址最后16bit的16进制数字 用于修改Ipv6Addr 
#                                 MacLast16Bit Icmpv6报头中可选字段Destination Link Layer中Mac地址最后16bit的16进制数字 用于修改Mac
#                                 Num 需要交换机学到neighbors的最大数量，交换机最大学习16384(实际中最多学到16383)
#需要CPU端口
	if { $ProtoclEx == "ipv6ndpnamax" && $Ipv6NdpNaMaxPacketInfo != "NULL" } {
		#将ProtoclEx设置为icmpV6，使ipv6报文nextheader字段变为58(icmpv6)
		set ProtoclEx icmpV6
		if { $VlanTagFlag == 0 } {
			set FrameSize 90
	        array set arr $Ipv6NdpNaMaxPacketInfo
	    	#UDF2设置NA报文的Router,Solicited,Override三个标志位及后面24bit的保留位(始终为0)
	    	set UDF2Flag 1
	   	 	set Offset2 58
	   		set Length2 4
	    	set Value2 "60 00 00 00"
	    	set ContinueFlag2 false
			set Repeat2 1
			set IncreaseMode2 up
			#调用FormatIpv6NdpNaSegment函数填写数据字段
			set PatternType nonRepeat
			set DataPattern userpattern
			if ![info exist arr(Ipv6Addr)] {
				set arr(Ipv6Addr) $SouIpv6
			}
			if ![info exist arr(Mac)] {
				set arr(Mac) SouMac
			}
			set Pattern [FormatIpv6NdpNaSegment arr]
			#UDF1设置icmpv6 type值为0x88(十进制为136)，后面接checksum(checksum每个包减少2，因为Ipv6地址及mac均被修改)
	        set UDF1Flag 1
	    	set Offset1 54
	    	set Length1 4
	    	set Icmpv6CheckSum [FormatHex [CalcIcmpv6CheckSum $SouIpv6 $DesIpv6 [expr 8 + ([string length $Pattern] + 1) / 3] "88 00 00 00 $Value2 $Pattern"]]
	    	set Value1 "88 00 $Icmpv6CheckSum"
			set ContinueFlag1 false
			if [info exist arr(Num)] {
	    		set Repeat1 $arr(Num)
	    	} else {
				return -1
	    	}
	    	set Step1 2   ;#如果报文的源ipv6地址变化，则这里应该是减3，所以配置流的时候要求源地址不变，只需要变化icmpv6头里的地址即可
	    	set IncreaseMode1 down
			#UDF3设置NA报文Icmpv6报头中的Ipv6 address(只修改最后16bit)
			set UDF3Flag 1
	   	 	set Offset3 76
	   		set Length3 2
	   		set Value3 [string range [FormatHexIpv6 $arr(Ipv6Addr)] end-4 end]
	    	set ContinueFlag3 false
			set Repeat3 $arr(Num)
			#UDF4设置NA报文Icmpv6报头中的可选字段的mac address(只修改最后16bit)
			set UDF4Flag 1
	   	 	set Offset4 84
	   		set Length4 2
	   		set Value4 "[string range $arr(Mac) end-4 end-3] [string range $arr(Mac) end-1 end]"
	    	set ContinueFlag4 false
			set Repeat4 $arr(Num)
			
			#UDF5保留，用于Ipv6源地址的递增，由ixia自动设置
		} else {
			set FrameSize 94
	        array set arr $Ipv6NdpNaMaxPacketInfo
	    	#UDF2设置NA报文的Router,Solicited,Override三个标志位及后面24bit的保留位(始终为0)
	    	set UDF2Flag 1
	   	 	set Offset2 62
	   		set Length2 4
	    	set Value2 "60 00 00 00"
	    	set ContinueFlag2 false
			set Repeat2 1
			set IncreaseMode2 up
			#调用FormatIpv6NdpNaSegment函数填写数据字段
			set PatternType nonRepeat
			set DataPattern userpattern
			if ![info exist arr(Ipv6Addr)] {
				set arr(Ipv6Addr) $SouIpv6
			}
			if ![info exist arr(Mac)] {
				set arr(Mac) SouMac
			}
			set Pattern [FormatIpv6NdpNaSegment arr]
			#UDF1设置icmpv6 type值为0x88(十进制为136)，后面接checksum(checksum每个包减少2，因为Ipv6地址及mac均被修改)
	        set UDF1Flag 1
	    	set Offset1 58
	    	set Length1 4
	    	set Icmpv6CheckSum [FormatHex [CalcIcmpv6CheckSum $SouIpv6 $DesIpv6 [expr 8 + ([string length $Pattern] + 1) / 3] "88 00 00 00 $Value2 $Pattern"]]
	    	set Value1 "88 00 $Icmpv6CheckSum"
			set ContinueFlag1 false
			if [info exist arr(Num)] {
	    		set Repeat1 $arr(Num)
	    	} else {
				return -1
	    	}
	    	set Step1 2   ;#如果报文的源ipv6地址变化，则这里应该是减3，所以配置流的时候要求源地址不变，只需要变化icmpv6头里的地址即可
	    	set IncreaseMode1 down
			#UDF3设置NA报文Icmpv6报头中的Ipv6 address(只修改最后16bit)
			set UDF3Flag 1
	   	 	set Offset3 80
	   		set Length3 2
	   		set Value3 [string range [FormatHexIpv6 $arr(Ipv6Addr)] end-4 end]
	    	set ContinueFlag3 false
			set Repeat3 $arr(Num)
			#UDF4设置NA报文Icmpv6报头中的可选字段的mac address(只修改最后16bit)
			set UDF4Flag 1
	   	 	set Offset4 88
	   		set Length4 2
	   		set Value4 "[string range $arr(Mac) end-4 end-3] [string range $arr(Mac) end-1 end]"
	    	set ContinueFlag4 false
			set Repeat4 $arr(Num)
			
			#UDF5保留，用于Ipv6源地址的递增，由ixia自动设置
		}
	}

#add by qiaoyua
#用于构造rip response报文，限制报文长度，避免报文过长将数组字段当做Rip路由条目发送
#添加RipRoute中Num选项，表示连续发送Rip响应报文，每个报文携带一条路由信息，地址依次递增1
#如要打多条Rip路由条目，在设置SetIxiaStream时请只设置RipRoute为一条表项(多了不报错，但无用)
#目前仅支持C类地址递增，且递增包括255网段以及0网段
#需要使用CPU口
#例子: RipRoute {{Ip 121.1.1.0 Mask 255.255.255.0 Nexthot 0.0.0.0 Metric 5 Num 10 Checksum 8E}}
#		表示连续打入10条Rip路由，地址是从110.1.1.0/24-110.1.10.0/24
	if {$ProtoclEx == "rip"} {
		set ripnum [llength $RipRoute]
		if {$ripnum == 0} {
			set FrameSize 64
		} else {
			set FrameSize [expr {50 + 20 * $ripnum}]
			set position [lsearch [lindex $RipRoute 0] "Num"]
			if {$position != -1} {
				set UDF1Flag 1
		   	 	set Offset1 50
		   		set Length1 3
		   		set ripmaxroute [FormatIptoHex [lindex [lindex $RipRoute 0] [expr {[lsearch [lindex $RipRoute 0] "Ip"]+1}]]]
				set Value1 [string range $ripmaxroute 0 7]
		    	set ContinueFlag1 false
				set Repeat1 [lindex [lindex $RipRoute 0] [expr {$position+1}]]
				set IncreaseMode1 up
			}
		}
		set TotalLength [expr $FrameSize - 18]
	}

################################添加Ipv6 Ripng response################################
	#added by qiaoyua, 2009.12.17
	#用于构造ipv6 ripng response报文。用于ixia不支持Ipv6 Ripng报文，故采用使用ixia接口
	#配置到UDP，剩下的部分采用数据字段来进行配置
	#可以在一条流中发送多条ripng路由信息，采用的是发送多个报文，每个报文携带
	#一个路由信息，仅支持在第一条路由条目处添加Num字段，携带有Num字段的路由
	#条目前缀需要是十六的整倍数(实现方便，不是十六整倍数的未处理)
	#例子: SetIxiaStream Host 172.16.1.253 Card 1 Port 3 Action change \
    #      SouMac 00-00-00-00-00-03 DesMac 00-12-cf-30-b8-e0 \
    #      Protocl ipv6 SouIpv6 FE80::212:CFFF:FE30:B8E0 DesIpv6 FE02::9 \
    #      ProtoclEx ripng RipngCommand 2 RipngRoute {{Ipv6 2040:1:1:: Tag 0 Prefix 64 Metric 1} {Ipv6 2030:2:2:: Tag 23 Prefix 64 Metric 3}}
	if {$ProtoclEx == "ripng"} {
		set ProtoclEx udp
		set SPort 521
		set DPort 521
		#配置命令字段，1为request，2为response，后三个八位字段01 00 00为版本字段以及保留字段
		if {$RipngCommand == 1} {
			append segement "01 01 00 00 "
		} else {
			append segement "02 01 00 00 "
		}
		for {set j 0} {$j < [llength $RipngRoute]} {incr j} {
			set ripng [lindex $RipngRoute $j]
			#Ipv6 address
			set position [lsearch $ripng "Ipv6"]
			if {$position != -1} {
				append segement "[FormatHexIpv6 [lindex $ripng [expr {$position+1}]]] "
			} else {
				PrintRes Print "!set Ipv6 Ripng Ipv6 address error!"
			}
			#Tag
			set position [lsearch $ripng "Tag"]
			if {$position != -1} {
				set ripngtag [format %0*x 4 [lindex $ripng [expr {$position+1}]]]
				if {[string length $ripngtag] != 4} {
					PrintRes Print "!set Ipv6 Ripng tag too large, error!"
				}
				append segement "[string replace $ripngtag 0 1 "[string range $ripngtag 0 1] "] "
			} else {
				PrintRes Print "!set Ipv6 Ripng tag error!"
			}
			#Prefix
			set position [lsearch $ripng "Prefix"]
			if {$position != -1} {
				set ripngprefix [format %0*x 2 [lindex $ripng [expr {$position+1}]]]
				if {[string length $ripngprefix] != 2} {
					PrintRes Print "!set Ipv6 Ripng prefix too large, error!"
				}
				append segement "$ripngprefix "
			} else {
				PrintRes Print "!set Ipv6 Ripng prefix error!"
			}
			#Metric
			set position [lsearch $ripng "Metric"]
			if {$position != -1} {
				set ripngmetric [format %0*x 2 [lindex $ripng [expr {$position+1}]]]
				if {[string length $ripngmetric] != 2} {
					PrintRes Print "!set Ipv6 Ripng metric too large, error!"
				}
				if {$j == [expr {[llength $RipngRoute]-1}]} {
					append segement "$ripngmetric"
				} else {
					append segement "$ripngmetric "
				}
			} else {
				PrintRes Print "!set Ipv6 Ripng metric error!"
			}
			#Num
			set position [lsearch $ripng "Num"]
			if {$position != -1} {
				set ripngnum [lindex $ripng [expr {$position+1}]]
				set UDF1Flag 1
				set numprefix [lsearch $ripng "NumPrefix"]
				if {$numprefix != -1} {
					#设置多条ripng路由时，要求前缀为十六的整倍数。不是十六整倍数情况未处理
					set numprefix [expr {[lindex $ripng [expr {$numprefix+1}]]/8}]
				} else {
					PrintRes Print "!set Ipv6 Ripng num error!"
				}
		   	 	set Offset1 [expr {65+$numprefix-1}]
		   		set Length1 2
		   		set position [lsearch $ripng "Ipv6"]
				if {$position != -1} {
					set numvalue [FormatHexIpv6 [lindex $ripng [expr {$position+1}]]]
					set numvalue [split $numvalue " "]
					set Value1 [lindex $numvalue [expr {$numprefix-2}]]
					append Value1 " [lindex $numvalue [expr {$numprefix-1}]]"
				} else {
					PrintRes Print "!set Ipv6 Ripng num value error!"
				}
		    	set ContinueFlag1 false
				set Repeat1 $ripngnum
				set IncreaseMode1 up
			}
		}
		set FrameSize [expr {70 + 20 * [llength $RipngRoute]}]
		set TotalLength [expr $FrameSize - 18]
		set PatternType nonRepeat
		set DataPattern userpattern
		set Pattern $segement
	}

################################添加ipv6ndpns################################
#added by qiaoyua, 2010-01-28
#用于构造Ipv6 NDP NS报文
#SetIxiaStream Host $testerip Card $Card1 Port $Port1 StreamRateMode Fps StreamRate 1 Action change \
#              SouMac 00-00-00-00-00-10 DesMac $vlanmacs1 \
#              Protocl ipv6 SouIpv6 2001::10 SouNetworkv6 64 DesIpv6 2001::1 DesNetworkv6 64 \
#              ProtoclEx ipv6ndpns Ipv6NdpNsPacketInfo [list TargetAddr 2001::10 Mac 00-00-00-00-00-10 DAD 0]
    if { $ProtoclEx == "ipv6ndpns" && $Ipv6NdpNsPacketInfo != "NULL" } {
    
		set ProtoclEx icmpV6
        array set arr $Ipv6NdpNsPacketInfo
		set FrameSize 90
		#如果DAD为1，则NS报文为DAD报文，不包括Source Link-layer Option
		if [info exists arr(DAD)] {
			if {$arr(DAD) == 1} {
				set FrameSize 82
			}
		}
		if {$VlanTagFlag == 1} {
			set FrameSize [expr {$FrameSize + 4}]
		}
		#调用FormatIpv6NdpNsSegment函数填写数据字段
		set PatternType nonRepeat
		set DataPattern userpattern
		set Pattern [FormatIpv6NdpNsSegment arr]
		#UDF1设置icmpv6 type值为0x87(十进制为135)
        set UDF1Flag 1
        if {$VlanTagFlag == 1} {
        	set Offset1 58
        } else {
    		set Offset1 54
    	}
    	set Length1 4
    	set Icmpv6CheckSum [FormatHex [CalcIcmpv6CheckSum $SouIpv6 $DesIpv6 [expr 8 + ([string length $Pattern] + 1) / 3] "87 00 00 00 00 00 00 00 $Pattern"]]
    	set Value1 "87 00 $Icmpv6CheckSum"
		set ContinueFlag1 false
		set Repeat1 1 
	}

################################添加ipv6ndpRedirect################################
#added by qiaoyua, 2010-02-01
#用于构造Ipv6 NDP Redirect报文
#SetIxiaStream Host $testerip Card $Card1 Port $Port1 StreamRateMode Fps StreamRate 1 Action change \
#              SouMac 00-00-00-00-00-10 DesMac $vlanmacs1 \
#              Protocl ipv6 SouIpv6 2001::10 SouNetworkv6 64 DesIpv6 2001::1 DesNetworkv6 64 \
#              ProtoclEx ipv6ndpredirect Ipv6NdpRedirectPacketInfo [list TargetAddr 2001::10 Mac 00-00-00-00-00-10 DAD 0]
    if { $ProtoclEx == "ipv6ndpredirect" && $Ipv6NdpRedirectPacketInfo != "NULL" } {
    
		set ProtoclEx icmpV6
        array set arr $Ipv6NdpNsPacketInfo
		set FrameSize 218
		#调用FormatIpv6NdpNsSegment函数填写数据字段
		set PatternType nonRepeat
		set DataPattern userpattern
		set Pattern [FormatIpv6NdpRedirectSegment arr]
		#UDF1设置icmpv6 type值为0x89(十进制为137)
        set UDF1Flag 1
        set Offset1 54
    	set Length1 4
    	set Icmpv6CheckSum [FormatHex [CalcIcmpv6CheckSum $SouIpv6 $DesIpv6 [expr 8 + ([string length $Pattern] + 1) / 3] "89 00 00 00 00 00 00 00 $Pattern"]]
    	set Value1 "87 00 $Icmpv6CheckSum"
		set ContinueFlag1 false
		set Repeat1 1 
	}


################################添加ipv6 rs报文################################
#added by zouleia, 2009-11-6
#用于构造Ipv6  RS报文
#SetIxiaStream Host $testerip Card $Card1 Port $Port1 StreamRateMode Fps StreamRate 1 Action change \
#              SouMac 00-00-00-00-00-10 DesMac $vlanmacs1 \
#              Protocl ipv6 SouIpv6 2001::10 SouNetworkv6 64 DesIpv6 2001::1 DesNetworkv6 64 \
#              ProtoclEx ipv6rs Ipv6RSPacketInfo [list Mac 00-00-00-00-00-01]
    if { $ProtoclEx == "ipv6rs" && $Ipv6RSPacketInfo != "NULL" } {
		#将ProtoclEx设置回icmpV6，使ipv6报文nextheader字段变为58(icmpv6)
		set ProtoclEx icmpV6

		array set arr $Ipv6RSPacketInfo
		
		set FrameSize 74
		#如果NoOption为1，则NS报文不包括Source Link-layer Option
		if [info exists arr(NoOption)] {
			if {$arr(NoOption) == 1} {
				set FrameSize 66
			}
		}
		set UDF2Flag 1
   	 	set Offset2 58
   		set Length2 4
    	set Value2 "00 00 00 00"
    	set ContinueFlag2 false
		set Repeat2 1 
		#调用FormatIpv6RSSegment函数填写数据字段
		if {([info exists arr(NoOption)] == 0) || ($arr(NoOption) == 0)} {
			set PatternType nonRepeat
			set DataPattern userpattern
			set Pattern [FormatIpv6RSSegment arr]
		}
		#UDF1设置icmpv6 type值为0x85(十进制为133)
        set UDF1Flag 1
    	set Offset1 54
    	set Length1 4
    	if {([info exists arr(NoOption)] == 0) || ($arr(NoOption) == 0)} {
	    	set Icmpv6CheckSum [FormatHex [CalcIcmpv6CheckSum $SouIpv6 $DesIpv6 [expr 8 + ([string length $Pattern] + 1) / 3] "85 00 00 00 $Value2 $Pattern"]]
    	} else {
			set Icmpv6CheckSum [FormatHex [CalcIcmpv6CheckSum $SouIpv6 $DesIpv6 8 "85 00 00 00 $Value2"]]
    	}
    	set Value1 "85 00 $Icmpv6CheckSum"
		set ContinueFlag1 false
		set Repeat1 1 
	}
#############################################################################################################

	#checksum未修改，使用时需注意   2009.10.29
	if { $ProtoclEx == "icmpV6-request" } {
		set TrafficClass 0
		set HopLimit 1
		set FrameSize 94
		set UDF1Flag 1
		set Offset1 62
		set Length1 1
		set Value1 82
		set ContinueFlag1 false
		set Repeat1 1
		set UDF2Flag 1
		set Offset2 66
		set Length2 2
		set Value2 2710
		set ContinueFlag2 false
		set Repeat2 1
		set PatternType nonRepeat
		set DataPattern userpattern
		set Pattern "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00"
	}
	#checksum未修改，使用时需注意   2009.10.29
	if { $ProtoclEx == "icmpV6-report" } {
		set TrafficClass 192
		set HopLimit 1
		set FrameSize 94
		set UDF1Flag 1
		set Offset1 62
		set Length1 1
		set Value1 83
		set ContinueFlag1 false
		set Repeat1 1
		set UDF2Flag 1
		set Offset2 66
		set Length2 2
		set Value2 0000
		set ContinueFlag2 false
		set Repeat2 1
		set PatternType nonRepeat
		set DataPattern userpattern
		set Pattern "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00"
    }
    if { $ProtoclEx == "mld" } {
    	switch $Type {
    		query {
    			set TrafficClass 0
				#Type
				set UDF1Flag 1
				if { $VlanTagFlag == 0 } {
					set Offset1 62
				} else {
					set Offset1 66
				}
				set Length1 4
				if { $MldVersion == 1 } {
					set Icmpv6CheckSum [FormatHex [CalcIcmpv6CheckSum $SouIpv6 $DesIpv6 24 "82 00 00 00 $MldMaxResponseDelay 00 00 [FormatHexIpv6 $MldGroupAddress]"]]
				}
				if { $MldVersion == 2 } {
					set icmpv6segment "[FormatHexIpv6 $MldGroupAddress] 02 7D [FormatHex [format %04x [llength $SourceRecord]]]"
					set SourceRecord [split $MldSourceIpAddress " "]
					for {set i 0} {$i < [llength $SourceRecord]} {incr i} {
						append icmpv6segment " [FormatHexIpv6 [lindex $SourceRecord $i]]"
					}
					set Icmpv6CheckSum [FormatHex [CalcIcmpv6CheckSum $SouIpv6 $DesIpv6 [expr 8 + ([string length $icmpv6segment] + 1) / 3] "82 00 00 00 $MldMaxResponseDelay 00 00 $icmpv6segment"]]
				}
				set Value1 "82 00 $Icmpv6CheckSum"
				set ContinueFlag1 false
				set Repeat1 1
				#MaxResponseDelay/MaxResponseCode
				set UDF2Flag 1
				if { $VlanTagFlag == 0 } {
					set Offset2 66
				} else {
					set Offset2 70
				}
				set Length2 2
				set Value2 $MldMaxResponseDelay
				set ContinueFlag2 false
				set Repeat2 1
				#Reserved
				set UDF3Flag 1
				if { $VlanTagFlag == 0 } {
					set Offset3 68
				} else {
					set Offset3 72
				}
				set Length3 2
				set Value3 0000
				set ContinueFlag3 false
				set Repeat3 1
    		}
    		report {
    			set TrafficClass 192
    			if { $MldVersion == 1 } {
					#Type Code CheckSum
    				set UDF1Flag 1
					if { $VlanTagFlag == 0 } {
						set Offset1 62
					} else {
						set Offset1 66
					}
					set Length1 4
					set Icmpv6CheckSum [FormatHex [CalcIcmpv6CheckSum $SouIpv6 $DesIpv6 24 "83 00 00 00 00 00 00 00 [FormatHexIpv6 $MldGroupAddress]"]]
					#puts $Icmpv6CheckSum
					set Value1 "83 00 $Icmpv6CheckSum"
					set ContinueFlag1 false
					set IncreaseMode1 down
					set Repeat1 $MldGroupNum
					set Step1 2
					#MaxResponseDelay
					set UDF2Flag 1
					if { $VlanTagFlag == 0 } {
						set Offset2 66
					} else {
						set Offset2 70
					}
					set Length2 4
					set Value2 0
					set ContinueFlag2 false
					set Repeat2 1
#					#Reserved
#					set UDF3Flag 1
#					if { $VlanTagFlag == 0 } {
#						set Offset3 68
#					} else {
#						set Offset3 72
#					}
#					set Length3 2
#					set Value3 0000
#					set ContinueFlag3 false
#					set Repeat3 1
					if { $MldGroupNum != 1 } {
						set UDF3Flag 1
						if { $VlanTagFlag == 0 } {
							set Offset3 84
						} else {
							set Offset3 88
						}
						set Length3 2
						set Value3 [string range [FormatIpv6 $MldGroupAddress] end-3 end]
						set ContinueFlag3 false
						set Repeat3 $MldGroupNum
					}
				}
				if { $MldVersion == 2 } {
					#Type
    				set UDF1Flag 1
					if { $VlanTagFlag == 0 } {
						set Offset1 62
					} else {
						set Offset1 66
					}
					set Length1 4
					set icmpv6segment ""
					for {set i 0} {$i < [llength $MldGroupRecord]} {incr i} {
						set GroupRecord [lindex $MldGroupRecord $i]
						set SourceRecord [split [lindex $GroupRecord 2] " "]
						switch [lindex $GroupRecord 1] {
							include {append icmpv6segment "01"}
							exclude {append icmpv6segment "02"}
							toinclude {append icmpv6segment "03"}
							toexclude {append icmpv6segment "04"}
							allow {append icmpv6segment "05"}
							block {append icmpv6segment "06"}
						}
						append icmpv6segment " 00 "
						append icmpv6segment [FormatHex [format %04x [llength $SourceRecord]]]
						append icmpv6segment " [FormatHexIpv6 [lindex $GroupRecord 0]]"
						for {set j 0} {$j < [llength $SourceRecord]} {incr j} {
							if { $j == [expr [llength $SourceRecord] - 1] } {
								append icmpv6segment " [FormatHexIpv6 [lindex $SourceRecord $j]] "
							} else {
								append icmpv6segment " [FormatHexIpv6 [lindex $SourceRecord $j]]"
							}
						}
					}
					set Icmpv6CheckSum [FormatHex [CalcIcmpv6CheckSum $SouIpv6 $DesIpv6 [expr 8 + ([string length $icmpv6segment] + 1) / 3] "8F 00 00 00 00 00 [FormatHex [format %04X [llength $MldGroupRecord]]] $icmpv6segment"]]
					set Value1 "8f 00 $Icmpv6CheckSum"
					#set Length1 1
					#set Value1 8f
					set ContinueFlag1 false
					set Repeat1 1 
					#Reserved
					set UDF2Flag 1
					if { $VlanTagFlag == 0 } {
						set Offset2 66
					} else {
						set Offset2 70
					}
					set Length2 2
					set Value2 0000
					set ContinueFlag2 false
					set Repeat2 1
					#Number of MldGroupRecord
					set UDF3Flag 1
					if { $VlanTagFlag == 0 } {
						set Offset3 68
					} else {
						set Offset3 72
					}
					set Length3 2
					set Value3 [format %04x [llength $MldGroupRecord]]
					set ContinueFlag3 false
					set Repeat3 1
				}
    		}
    		done {
    			set TrafficClass 192
				#Type
    			set UDF1Flag 1
				if { $VlanTagFlag == 0 } {
					set Offset1 62
				} else {
					set Offset1 66
				}
				set Length1 4
				set Icmpv6CheckSum [FormatHex [CalcIcmpv6CheckSum $SouIpv6 $DesIpv6 24 "84 00 00 00 00 00 00 00 [FormatHexIpv6 $MldGroupAddress]"]]
				set Value1 "84 00 $Icmpv6CheckSum"
				set ContinueFlag1 false
				set Repeat1 1 
				#MaxResponseDelay
				set UDF2Flag 1
				if { $VlanTagFlag == 0 } {
					set Offset2 66
				} else {
					set Offset2 70
				}
				set Length2 2
				set Value2 0000
				set ContinueFlag2 false
				set Repeat2 1
				#Reserved
				set UDF3Flag 1
				if { $VlanTagFlag == 0 } {
					set Offset3 68
				} else {
					set Offset3 72
				}
				set Length3 2
				set Value3 0000
				set ContinueFlag3 false
				set Repeat3 1
    		}
    	}
		set HopLimit 1
		set PatternType nonRepeat
		set DataPattern userpattern
		set Pattern [FormatIcmpv6Segment $MldVersion $Type $MldGroupAddress $MldSourceIpAddress $MldGroupRecord]
		if { $VlanTagFlag == 1 } {
			set FrameSize [expr 62 + 8 + [regsub -all " " $Pattern {} ignore] + 1 + 4 + 4]
		} else {
			set FrameSize [expr 62 + 8 + [regsub -all " " $Pattern {} ignore] + 1 + 4]
		}
	}
	if { $EthernetType == "loopback" && $LoopbackDetectionInfo != "NULL" } {
		set EthernetTypeFlag 1
		if { [llength $LoopbackDetectionInfo] >= 3 } {
			set EthernetTypeNum [lindex $LoopbackDetectionInfo 2]
		} else {
			set EthernetTypeNum 56329
		}
		if { $VlanTagFlag == 1 } {
			set FrameSize 68
		} else {
			set FrameSize 64
		}
		set PatternType nonRepeat
		set DataPattern userpattern
		set Pattern [FormatLoopbackSegment $LoopbackDetectionInfo]
	}
	if { $EthernetType == "mrpp" && $MrppPacketInfo != "NULL" } {
		set EthernetType noType
		if { $VlanTagFlag == 1 } {
			set FrameSize 94
		} else {
			set FrameSize 90
		}
		set PatternType nonRepeat
		set DataPattern userpattern
		set Pattern [FormatMrppSegment $MrppPacketInfo]
	}
	if { $EthernetType == "rstp" && $RstpPacketInfo != "NULL" } {
		set EthernetType noType
		set FrameSize 64
		set PatternType nonRepeat
		set DataPattern userpattern
		set Pattern [FormatRstpSegment $RstpPacketInfo] 
	}
	if { $EthernetType == "stp" && $StpPacketInfo != "NULL" } {
		set EthernetType noType
		set FrameSize 64
		set PatternType nonRepeat
		set DataPattern userpattern
		set Pattern [FormatStpSegment $StpPacketInfo] 
	}
	if { $EthernetType == "mstp" && $MstpPacketInfo != "NULL" } {
		set EthernetType noType
		set position [lsearch $MstpPacketInfo "MstpOtherInfo"]
		if { $position != -1 } {
			set otherinfonum [llength [lindex $MstpPacketInfo [expr $position + 1]]]
			set FrameSize [expr 124 + 26 * $otherinfonum]
		} else {
			set FrameSize 124
		}
		set PatternType nonRepeat
		set DataPattern userpattern
		set Pattern [FormatMstpSegment $MstpPacketInfo] 
	}
	if { $EthernetType == "lldp" && $LLDPPacketInfo != "NULL" } {
		set EthernetType noType
		set PatternType nonRepeat
		set DataPattern userpattern
		set Pattern [FormatLLDPSegment $LLDPPacketInfo]
		if { $VlanTagFlag == 1 } {
			set FrameSize [expr ([string length $Pattern] + 1) / 3 + 12 + 4 + 4]
			if { $FrameSize < 64 } {
				set FrameSize 64
			}
		} else {
			set FrameSize [expr ([string length $Pattern] + 1) / 3 + 12 + 4]
			if { $FrameSize < 64 } {
				set FrameSize 64
			}
		}
	}
#格式为 SetIxiaStream Host $host Card $Card1 Port $Port1 StreamRateMode Fps StreamRate 1 \
#                     SouMac $cpumac DesMac 33-33-00-00-00-01 Protocl ipv6 \
#                     SouIpv6 [GetLinkLocalAddress $cpumac] DesIpv6 FF02::1 ProtoclEx ipv6ra \
#                     Ipv6RAPacketInfo [list CheckSum "B5 6F" CurHopLimit 0 FlagM 0 FlagO 0 RouterLifeTime 12 ReachableTime 0 RetransTimer 0 \
#                     SourceLinkLayer [list Type 1 Length 1 LinkLayerAddress $cpumac] \
#                     MTU [list Type 5 Length 1 MTU 1500] \
#                     PrefixInformation [list Type 3 Length 4 PrefixLength 64 FlagLink 1 FlagAutonomous 1 FlagNotRouterAddress 0 \
#                                        FlagSitePrefix 1 ValidLifeTime 0 PreferredLifeTime 0 Prefix 2321::]]
#2009.10.29 modify by liangdong 已经可以自动计算checksum
	##################add by liangdong ipv6 RA
    if { $ProtoclEx == "ipv6ra" && $Ipv6RAPacketInfo != "NULL" } {
		#将ProtoclEx设置回icmpV6，使ipv6报文nextheader字段变为58(icmpv6)
		set ProtoclEx icmpV6
        array set ra $Ipv6RAPacketInfo
        #UDF1设置icmpv6 type值为0x86 00(十进制为134) checksum "xx xx"
#        if [info exist ra(CheckSum)] {
#	        set UDF1Flag 1
#	    	set Offset1 54
#	    	set Length1 4
#	    	set Value1 "86 00 $ra(CheckSum)"   ;#CheckSum "xx xx"
#			set ContinueFlag1 false
#			set Repeat1 1 
#		} else {
#			return -1
#    	}
		#UDF2设置Cur Hop Limit, M, O, Reserved, Router Life time
		if [info exist ra(CurHopLimit)] {
    		set curhoplimit $ra(CurHopLimit)
    	} else {
			set curhoplimit 0
    	}
    	if [info exist ra(FlagM)] {
    		set flagm $ra(FlagM)
    	} else {
			set flagm 0
    	}
    	if [info exist ra(FlagO)] {
    		set flago $ra(FlagO)
    	} else {
			set flago 0
    	}
    	if [info exist ra(RouterLifeTime)] {
    		set routerlifetime $ra(RouterLifeTime)
    	} else {
			set routerlifetime 12
    	}
       	set UDF2Flag 1
    	set Offset2 58
    	set Length2 4
    	set Value2 "[format %02x $curhoplimit] [format %02x [expr $flagm << 7 + $flago << 6]] [format %02x [expr $routerlifetime / 256]] [format %02x [expr $routerlifetime % 256]]"
    	set ContinueFlag2 false
		set Repeat2 1 		
		set FrameSize 74
		if [info exist ra(SourceLinkLayer)] {
			set FrameSize [expr $FrameSize + 8]
		}
		if [info exist ra(MTU)] {
			set FrameSize [expr $FrameSize + 8]
		}
		if [info exist ra(PrefixLength)] {
			set FrameSize [expr $FrameSize + 32]
		}
		if [info exist ra(RedirectHeader)] {
			set FrameSize [expr $FrameSize + 8]
		}
		#调用FormatIpv6NdpNaSegment函数填写数据字段
		set PatternType nonRepeat
		set DataPattern userpattern
		set Pattern [FormatIpv6RASegment $Ipv6RAPacketInfo]

		set UDF1Flag 1
		set Offset1 54
		set Length1 4
		set Icmpv6CheckSum [FormatHex [CalcIcmpv6CheckSum $SouIpv6 $DesIpv6 [expr 8 + ([string length $Pattern] + 1) / 3] "86 00 00 00 $Value2 $Pattern"]]
		set Value1 "86 00 $Icmpv6CheckSum"
		set ContinueFlag1 false
		set Repeat1 1		
	}
	if { $EthernetType == "uldp" && $ULDPPacketInfo != "NULL"} {
		set EthernetType noType
		set PatternType nonRepeat
		set DataPattern userpattern
		set Pattern [FormatULDPSegment $ULDPPacketInfo] 
		if { $VlanTagFlag == 1 } {
			set FrameSize [expr ([string length $Pattern] + 1) / 3 + 12 + 4 + 4]
			if { $FrameSize < 64 } {
				set FrameSize 64
			}
		} else {
			set FrameSize [expr ([string length $Pattern] + 1) / 3 + 12 + 4]
			if { $FrameSize < 64 } {
				set FrameSize 64
			}
		}
	}
	if { $EthernetType == "cluster" && $ClusterPacketInfo != "NULL"} {
		set EthernetType noType
		set position [lsearch $ClusterPacketInfo "ClusterType"]
		if { $position != -1 } {
			set ClusterType [lindex $ClusterPacketInfo [expr $position + 1]]
			if { $ClusterType == "DP" } {
				set FrameSize 64 
				set PatternType nonRepeat
				set DataPattern userpattern
				if { $VlanTagFlag == 1 } {
					set Pattern [FormatClusterSegment $ClusterPacketInfo [expr $FrameSize - 12 - 4 - 4]]
				} else {
					set Pattern [FormatClusterSegment $ClusterPacketInfo [expr $FrameSize - 12 - 4]]
				}
			}
			if { $ClusterType == "DR" } {
				set FrameSize 116 
				set PatternType nonRepeat
				set DataPattern userpattern
				if { $VlanTagFlag == 1 } {
					set Pattern [FormatClusterSegment $ClusterPacketInfo [expr $FrameSize - 12 - 4 - 4]]
				} else {
					set Pattern [FormatClusterSegment $ClusterPacketInfo [expr $FrameSize - 12 - 4]]
				} 
			}
			if { $ClusterType == "CP" } {
				set position [lsearch $ClusterPacketInfo "SubOp"]   
				set SubOp [lindex $ClusterPacketInfo [expr $position + 1]]
				if { $SubOp == "0001" || $SubOp == "0002" } {
					set FrameSize 70 
				} elseif { $SubOp == "0003" || $SubOp == "0004" } {
					#这种类型的报文实际有效字节长度为42
					set FrameSize 64
				}
				set PatternType nonRepeat
				set DataPattern userpattern
				if { $VlanTagFlag == 1 } {
					set Pattern [FormatClusterSegment $ClusterPacketInfo [expr $FrameSize - 12 - 4 - 4]]
				} else {
					set Pattern [FormatClusterSegment $ClusterPacketInfo [expr $FrameSize - 12 - 4]]
				}   
			}
		} else {
			set FrameSize 64 
			set PatternType nonRepeat
			set DataPattern userpattern
			if { $VlanTagFlag == 1 } {
				set Pattern [FormatClusterSegment $ClusterPacketInfo [expr $FrameSize - 12 - 4 - 4]]
			} else {
				set Pattern [FormatClusterSegment $ClusterPacketInfo [expr $FrameSize - 12 - 4]]
			}
		}
	}
	if { $ProtoclEx == "dhcpoffer" } {
		set SPort 67
		set DPort 68
		set OpCode dhcpBootReply
		set YourIpAddr $YourIpAddr
		set ClientHwAddr $ClientHwAddr
		set DhcpMessageType 2
		set DhcpSvrIdentifier $DhcpSvrIdentifier
		set DhcpIPAddrLeaseTime $DhcpIPAddrLeaseTime
		set DhcpRenewalTimeValue $DhcpRenewalTimeValue
		set DhcpRebindingTimeValue $DhcpRebindingTimeValue
		set DhcpSubnetMask $DhcpSubnetMask
	}
	if { $ProtoclEx == "dhcpack" } {
		set SPort 67
		set DPort 68
		set OpCode dhcpBootReply
		set YourIpAddr $YourIpAddr
		set ClientHwAddr $ClientHwAddr
		set DhcpMessageType 5
		set DhcpSvrIdentifier $DhcpSvrIdentifier
		set DhcpIPAddrLeaseTime $DhcpIPAddrLeaseTime
		set DhcpRenewalTimeValue $DhcpRenewalTimeValue
		set DhcpRebindingTimeValue $DhcpRebindingTimeValue
		set DhcpSubnetMask $DhcpSubnetMask
	}
	if { $ProtoclEx == "dhcprelease" } {
		set SPort 68
		set DPort 67
		set OpCode dhcpBootRequest
		set ClientIpAddr $ClientIpAddr
		set ClientHwAddr $ClientHwAddr
		set DhcpMessageType 7
		set DhcpClientId $DhcpClientId
		set DhcpSvrIdentifier $DhcpSvrIdentifier
	}
	if { $ProtoclEx == "dhcpdiscover" } {
		set SPort 68
		set DPort 67
		set OpCode dhcpBootRequest
		set ClientHwAddr $ClientHwAddr
		set DhcpMessageType 1
		set DhcpParamRequestList $DhcpParamRequestList
		set DhcpClientId $DhcpClientId
	}
	if { $ProtoclEx == "dhcprequest" } {
		set SPort 68
		set DPort 67
		set OpCode dhcpBootRequest
		set ClientHwAddr $ClientHwAddr
		set DhcpMessageType 3
		set DhcpParamRequestList $DhcpParamRequestList
		set DhcpClientId $DhcpClientId
		set DhcpSvrIdentifier $DhcpSvrIdentifier
		set DhcpRequestedIPAddr $DhcpRequestedIPAddr
	}
	if { $ProtoclEx == "dhcperror" } {
		set SPort $SPort
		set DPort $DPort
		set OpCode $OpCode
		set HardwareAddressLength $HardwareAddressLength
		set Hops $Hops
		set TransactionID $TransactionID
		set YourIpAddr $YourIpAddr
		set ClientHwAddr $ClientHwAddr
        set DhcpMessageType $DhcpMessageType
		set DhcpSvrIdentifier $DhcpSvrIdentifier
		set DhcpIPAddrLeaseTime $DhcpIPAddrLeaseTime
		set DhcpRenewalTimeValue $DhcpRenewalTimeValue
		set DhcpRebindingTimeValue $DhcpRebindingTimeValue
		set ClientHwAddr $ClientHwAddr
		set DhcpSubnetMask $DhcpSubnetMask
	}
###############################################################################
#added by lixiaa 2010.7.13
    if { $ProtoclEx == "ipv6vrrp" } {
    	set PatternType nonRepeat
		set DataPattern userpattern
		set Pattern [FormatIpv6VrrpSegment $SouIpv6 $DesIpv6 $Ipv6VrrpInfo]
		if { $VlanTagFlag == 1 } {
			set FrameSize [expr ([string length $Pattern]) / 2 + 54 + 4 + 4]
			if { $FrameSize < 64 } {
				set FrameSize 64
			}
		} else {
			set FrameSize [expr ([string length $Pattern] + 1) / 2 + 54 + 4]
			if { $FrameSize < 64 } {
				set FrameSize 64
			}
		}
        set UDF1Flag 1
        set Offset1 20
        set Length1 1
        set Value1 70
        set ContinueFlag1 false
        set Repeat1 1
        set Step1 1
        set IncreaseMode1 up
    }

###############################################################################
#added by gengtao 2010.11.11
    if { $ProtoclEx == "Ipv4vrrp" } {
    	set PatternType nonRepeat
		set DataPattern userpattern
		set Pattern [FormatIpv4VrrpSegment $Ipv4VrrpInfo]
    }
#####################################GRE#######################################
#added by zhangfank,2010.7.9
	if {$GreInnerProtocolEx == "icmpv6"} {		;#修改icmpv6报文类型值
		set UDF1Flag 1
		if {$Protocl == "ipv4"} {
			if {$VlanTagFlag == 0} {
				set Offset1 78
			} elseif {$VlanTagFlag == 1} {		;#目前最多支持一层tag
				set Offset1 82
			}
		} elseif {$Protocl == "ipv6"} {
			if {$VlanTagFlag == 0} {
				set Offset1 98
			} elseif {$VlanTagFlag == 1} {		;#目前最多支持一层tag
				set Offset1 102
			}
		}	
		set Length1 1
		set Value1 [format %02x $GreInnerIcmpv6Type]
		set ContinueFlag1 false
		set Repeat1 1
	}

	########################set ixia#####################################
	set Version [ package require IxTclHal ]
	if {$StreamNum == 1} {
		ixInitialize $Host
	}
	set Chas [ixGetChassisID $Host]
	set portList [list [list $Chas $Card $Port]]
#	if {$StreamNum == 1} {
#		port setFactoryDefaults $Chas $Card $Port
#	}
	
	SetPort $Chas $Card $Port $RateMode $FlowControl $TransmitMode
	SetStream $Chas $Card $Port $StreamMode $LastStreamFlag $ReturnToId $StreamRateMode $StreamRate $NumFrames $SouMac $SouMask $SouNum $SouMode $DesMac $DesMask $DesNum $DesMode $FrameSizeType $FrameSize $FrameSizeStep $FrameSizeMin $FrameSizeMax $FrameErrors $PatternType $DataPattern $Pattern
	if { $EthernetTypeFlag == 1 } {
		#目前用脚本不能配置ethernetTypeNum，用udf四解决
		udf config -enable true
		if { $VlanTagFlag == 1 } {
			udf config -offset 16
		} else {
	        udf config -offset 12
	    }
        udf config -countertype c16 
        udf config -continuousCount false
        udf config -updown uuuu
        udf config -step 0
        udf config -initval [ FormatHex [ format "%#x" $EthernetTypeNum ] ]
        udf set 4
    }
	if { $UDF1Flag == 1 } {
		SetIxiaUDF 1 $Offset1 $Length1 $Value1 $ContinueFlag1 $Repeat1 $Step1 $IncreaseMode1
	}
	if { $UDF2Flag == 1 } {
		SetIxiaUDF 2 $Offset2 $Length2 $Value2 $ContinueFlag2 $Repeat2 $Step2 $IncreaseMode2
	}
	if { $UDF3Flag == 1 } {
		SetIxiaUDF 3 $Offset3 $Length3 $Value3 $ContinueFlag3 $Repeat3 $Step3 $IncreaseMode3
	}
	if { $UDF4Flag == 1 } {
		SetIxiaUDF 4 $Offset4 $Length4 $Value4 $ContinueFlag4 $Repeat4 $Step4 $IncreaseMode4
	}
	SetProtocol $Version $Chas $Card $Port $VlanTagFlag $VlanId $Tpid $IfTpid $UserPriority \
				$VlanMode $VlanNum $VlanStep $Tpid1 $VlanId1 $Tpid2 $VlanId2 $Protocl $EthernetType \
				$SouIp $SouMask $SouClassMode $SouIpMode $SouIpNum $DesIp $DesMask $DesClassMode \
				$DesIpMode $DesIpNum $LengthOverride $TTL $TotalLength $ValidChecksum $Fragment \
				$LastFragment $FragmentOffset $ProtoclEx $SPort $DPort $OpCode \
				$HardwareAddressLength $Hops $TransactionID $ClientIpAddr $DhcpRequestedIPAddr \
				$DhcpClientId $YourIpAddr $ClientHwAddr $DhcpMessageType $DhcpParamRequestList \
				$DhcpSvrIdentifier $DhcpIPAddrLeaseTime $DhcpRenewalTimeValue \
				$DhcpRebindingTimeValue $DhcpSubnetMask $SequenceNum $HeaderLength $Type $Code \
				$IgmpVersion $IgmpGroupAddress $IgmpSourceIpAddress $IgmpMode $IgmpRepeat \
				$IgmpGroupRecord $ValidChecksum $MaxResponseTime $QQIC $QRV $EnableS $ACK $FIN \
				$PSH $RST $URG $SYN $PriorityFlag $Dscp $Tos $Ipprecedence $ArpOperation $SenderMac \
				$SenderMacMode $SenderMacNum $TargetMac $TargetMacMode $TargetMacNum $SenderIp \
				$SenderIpMode $SenderIpNum $TargetIp $TargetIpMode $TargetIpNum $SouIpv6 \
				$SouAddrModev6 $SouStepSizev6 $SouNumv6 $SouNetworkv6 $DesIpv6 $DesAddrModev6 \
				$DesStepSizev6 $DesNumv6 $DesNetworkv6 $TrafficClass $FlowLabel $HopLimit \
				$NextHeader $Sequence $RipCommand $RipVersion $RipRoute $MplsTagFlag $MplsLabel \
				$MplsBottom $MplsExp $MplsTtl $GreInnerProtocol $GreInnerProtocolEx $GreInnerSouIp $GreInnerSouMask \
				$GreInnerDesIp $GreInnerDesMask $GreHeaderReserved0 $GreInnerSouIpv6 $GreInnerSouMaskv6 \
				$GreInnerDesIpv6 $GreInnerDesMaskv6 $greACK $greFIN $grePSH $greRST $greURG $greSYN \
				$greSPort $greDPort $greType $greCode
	
	#write to hardware
#	if {$Protocl == "ipv4" || $Protocl == "ipv6ipv4" } {
#		ip set $Chas $Card $Port
#	}
#	if {$Protocl == "ipv6" || $Protocl == "ipv6ipv4" } {
#		ipV6 set $Chas $Card $Port
#	}
	if {[stream set $Chas $Card $Port $StreamNum] != 0 } {
		puts "stream set error!!"
	}
	#####解决后配置的流数目小于先配置的流的数目导致发送流量错误的问题
	if { $LastStreamFlag == "true" } {
		for {set i [expr $StreamNum + 1]} {$i <= 255} {incr i} {
			if ![stream get $Chas $Card $Port $i] {
				stream setDefault
				stream config -enable false
				stream set $Chas $Card $Port $i
			}
		}		
	}
	if {[port set $Chas $Card $Port] != 0 } {
		puts "port set error!!!"
	}
	if { $LastStreamFlag == "true" } {
	    if { $Action == "set" } {
	        ixWritePortsToHardware portList
	    }
	    if { $Action == "change" } {
	        ixWriteConfigToHardware portList
    	}
    	IdleAfter 5000
    }
    return 100
}


################################
#
# SetPort:SetIxiaStream 内部调用函数
#
# args:
#     Chas Card Port RateMode
#
# return:
#
# addition:
#
# examples:
#
###############################
proc SetPort {Chas Card Port RateMode FlowControl TransmitMode } {
	# Setup port
	#port setFactoryDefaults $Chas $Card $Port
	#port setDefault
	switch -exact -- $RateMode {
	    auto { 
	    	port config -autonegotiate true
            port config -advertise100FullDuplex true
            port config -advertise100HalfDuplex true
            port config -advertise10FullDuplex true
            port config -advertise10HalfDuplex true
            port config -advertise1000FullDuplex true	
	    }
   		10half {
   			port config -autonegotiate false
			port config -duplex half
			port config -speed 10
   		}
   		10full {
   			port config -autonegotiate false
			port config -duplex full
			port config -speed 10
   		}
   		100half {
   			port config -autonegotiate false
			port config -duplex half
			port config -speed 100
   		}
   		100full {
   			port config -autonegotiate false
			port config -duplex full
			port config -speed 100
   		}
   		1gfull {
   		    port config -autonegotiate true
   			port config -advertise100FullDuplex false
            port config -advertise100HalfDuplex false
            port config -advertise10FullDuplex false
            port config -advertise10HalfDuplex false
            port config -advertise1000FullDuplex true
   		}
   		default {
   			port config -autonegotiate false
 
   		}
	}
	if {$FlowControl == "true"} {
	    port config -flowControl true
	    port config -advertiseAbilities portAdvertiseSendAndOrReceive
	}
	if { $TransmitMode == "packetstreams" } {
		port config -transmitMode portTxPacketStreams
	}
	if { $TransmitMode == "advancedstreams" } {
		port config -transmitMode portTxModeAdvancedScheduler
	}
	if { $TransmitMode == "echo" } {
		port config -transmitMode portTxModeEcho
	}
}

##########################################################
#
# SetStream:SetIxiaStream 内部调用函数
#
# args:
#     Chas Card Port StreamMode StreamRate NumFramesSouMac SouNum DesMac DesNum FrameSize
#
# return:
#
# addition:
#
# examples:
#
##########################################################
proc SetStream {Chas Card Port StreamMode LastStreamFlag ReturnToId StreamRateMode StreamRate NumFrames SouMac SouMask SouNum SouMode DesMac DesMask DesNum DesMode FrameSizeType FrameSize FrameSizeStep FrameSizeMin FrameSizeMax FrameErrors PatternType DataPattern Pattern } {
	#convert mac format	
    set SouMac [split $SouMac -]
    set DesMac [split $DesMac -]
    
	stream setDefault
	if { $StreamRateMode == "PercentRate" } {
	    stream config -rateMode usePercentRate
    	stream config -percentPacketRate $StreamRate
    }
    if { $StreamRateMode == "Fps" } {
        stream config -rateMode streamRateModeFps
    	stream config -fpsRate $StreamRate
    }
    if { $StreamRateMode == "Bps" } {
        stream config -rateMode streamRateModeBps
    	stream config -bpsRate $StreamRate
    }
	if {$StreamMode == 1} {
		stream config -numFrames $NumFrames
		stream config -dma stopStream
	}
	if {$StreamMode == 0} {
		stream config -dma contPacket
	}
	if {$StreamMode == 2 && $LastStreamFlag == "false" } {
	    stream config -dma advance
	    stream config -numFrames $NumFrames
	}
	if {$StreamMode == 2 && $LastStreamFlag == "true" } {
	    stream config -dma gotoFirst
	    stream config -returnToId $ReturnToId
	    stream config -numFrames $NumFrames
	}
	if {$StreamMode == 3 && $LastStreamFlag == "false" } {
	    stream config -dma advance
	    stream config -numFrames $NumFrames
	}
	if {$StreamMode == 3 && $LastStreamFlag == "true" } {
	    stream config -dma stopStream
	    stream config -numFrames $NumFrames
	}
	if {$StreamMode == 4 && $LastStreamFlag == "false" } {
	    stream config -dma advance
	    stream config -numFrames $NumFrames
	}
	if {$StreamMode == 4 && $LastStreamFlag == "true" } {
	    stream config -dma contPacket
	    stream config -numFrames $NumFrames
	}
	stream config -numSA $SouNum
	stream config -saRepeatCounter $SouMode
	stream config -sa $SouMac
#	stream config -saMaskValue $SouMask
#	stream config -saMaskSelect 00-00-00-00-00-00
	stream config -numDA $DesNum
	stream config -daRepeatCounter $DesMode
	stream config -da $DesMac
#	stream config -daMaskValue $DesMask
#	stream config -daMaskSelect 00-00-00-00-00-00
	switch -exact $FrameSizeType {
	fixed {
		stream config -frameSizeType sizeFixed
		stream config -framesize $FrameSize
		}
	random {
		stream config -frameSizeType sizeRandom
		stream config -frameSizeMIN $FrameSizeMin
		stream config -frameSizeMAX $FrameSizeMax
		}
	incr {
		stream config -frameSizeType sizeIncr
		stream config -frameSizeStep $FrameSizeStep
		stream config -frameSizeMIN $FrameSizeMin
		stream config -frameSizeMAX $FrameSizeMax
		}
	auto {
		stream config -frameSizeType sizeAuto
		}
	}
	stream config -fcs $FrameErrors
	stream config -patternType $PatternType
	stream config -dataPattern $DataPattern
	stream config -pattern $Pattern
}

############################################################
#
# SetProtocol:SetProtocol SetIxiaStream 内部调用函数
#
# args:
#     Chas Card Port VlanTagFlag VlanId UserPriority Protocl SouIp SouMask SouNum DesIp 
#     DesMask DesNum PriorityFlag Dscp Tos ArpOperation SenderMac SenderMacNum TargetMac 
#     TargetMacNum SenderIp SenderIpNum TargetIp TargetIpNum
#
# return:
#
# addition:
#
# examples:
#
############################################################
proc SetProtocol {Version Chas Card Port VlanTagFlag VlanId Tpid IfTpid UserPriority VlanMode \
					  VlanNum VlanStep Tpid1 VlanId1 Tpid2 VlanId2 Protocl EthernetType SouIp \
					  SouMask SouClassMode SouIpMode SouIpNum DesIp DesMask DesClassMode DesIpMode \
					  DesIpNum LengthOverride TTL TotalLength ValidChecksum Fragment LastFragment \
					  FragmentOffset ProtoclEx SPort DPort OpCode HardwareAddressLength Hops \
					  TransactionID ClientIpAddr DhcpRequestedIPAddr DhcpClientId YourIpAddr \
					  ClientHwAddr DhcpMessageType DhcpParamRequestList DhcpSvrIdentifier \
					  DhcpIPAddrLeaseTime DhcpRenewalTimeValue DhcpRebindingTimeValue \
					  DhcpSubnetMask SequenceNum HeaderLength Type Code IgmpVersion IgmpGroupAddress \
					  IgmpSourceIpAddress IgmpMode IgmpRepeat IgmpGroupRecord ValidChecksum \
					  MaxResponseTime QQIC QRV EnableS ACK FIN PSH RST URG SYN PriorityFlag Dscp \
					  Tos Ipprecedence ArpOperation SenderMac SenderMacMode SenderMacNum TargetMac \
					  TargetMacMode TargetMacNum SenderIp SenderIpMode SenderIpNum TargetIp \
					  TargetIpMode TargetIpNum SouIpv6 SouAddrModev6 SouStepSizev6 SouNumv6 \
					  SouNetworkv6 DesIpv6 DesAddrModev6 DesStepSizev6 DesNumv6 DesNetworkv6 \
					  TrafficClass FlowLabel HopLimit NextHeader Sequence RipCommand RipVersion \
					  RipRoute MplsTagFlag MplsLabel MplsBottom MplsExp MplsTtl GreInnerProtocol GreInnerProtocolEx \
					  GreInnerSouIp GreInnerSouMask GreInnerDesIp GreInnerDesMask GreHeaderReserved0 \
					  GreInnerSouIpv6 GreInnerSouMaskv6 GreInnerDesIpv6 GreInnerDesMaskv6 \
					  greACK greFIN grePSH greRST greURG greSYN greSPort greDPort greType greCode} {
	set SouIp [list $SouIp]
	set SouMask [list $SouMask]
	set DesIp [list $DesIp]
	set DesMask [list $DesMask]
    
    #arp para
    set SenderMac [split $SenderMac -]
    set TargetMac [split $TargetMac -]
	set SenderIp [list $SenderIp]
	set TargetIp [list $TargetIp]
	#set ipv6 ip
    #set SouIpv6 [split $SouIpv6 :]
	#set DesIpv6 [split $DesIpv6 :]
	protocol setDefault
	if {$Protocl == "ipv4"} {
		protocol config -name ip
	}
	if {($Protocl == "ipv4" && $ProtoclEx == "dhcpoffer") || ($Protocl == "ipv4" && $ProtoclEx == "dhcpack") || ($Protocl == "ipv4" && $ProtoclEx == "dhcprelease") || ($Protocl == "ipv4" && $ProtoclEx == "dhcpdiscover") || ($Protocl == "ipv4" && $ProtoclEx == "dhcprequest") || ($Protocl == "ipv4" && $ProtoclEx == "dhcperror")} {
		protocol config -name ip
		protocol config -appName Dhcp
	}
	if {$Protocl == "ipv6"} {
		protocol config -name ipV6
	}
	if {$Protocl == "arp"} {
		protocol config -name ip
		protocol config -appName Arp
	}
	if {$Protocl == "ipv6ipv4"} {
	    protocol config -name ipV4
	    set ProtoclEx ipV4ProtocolIpv6
	}
	if { $Protocl == "ipv4" && $ProtoclEx == "rip" } {
		protocol config -name ip
		protocol config -appName Rip
	}
	protocol config -ethernetType $EthernetType
	if {$VlanTagFlag == 0} {
		protocol config -enable802dot1qTag vlanNone
	}
	if {$VlanTagFlag == 1} {
		if {$Version == 3.80} {
			protocol config -enable802dot1qTag true
		} else {
			protocol config -enable802dot1qTag vlanSingle
		}
		#set vlan tag
		vlan setDefault
		if { $IfTpid == 1 } {
			vlan config -protocolTagId vlanProtocolTag$Tpid
		}
		vlan config -vlanID $VlanId
		vlan config -userPriority $UserPriority
		vlan config -mode $VlanMode
		if { $VlanMode == "vIncrement" || $VlanMode == "vDecrement"} {
    		vlan config -repeat $VlanNum
    		vlan config -step $VlanStep
    	}
		vlan set $Chas $Card $Port
	}
	if {$VlanTagFlag == 2} {
		protocol config -enable802dot1qTag vlanStacked
		stackedVlan setDefault
		vlan setDefault
		vlan config -protocolTagId vlanProtocolTag$Tpid2
		vlan config -vlanID $VlanId2
		stackedVlan setVlan 1
		vlan setDefault
		vlan config -protocolTagId vlanProtocolTag$Tpid1
		vlan config -vlanID $VlanId1
		stackedVlan setVlan 2
		stackedVlan set $Chas $Card $Port
	}
	if {$MplsTagFlag == 1} {
		#只支持1个label,并且MPLS Type为unicast
		protocol config -ethernetType ethernetII
		protocol config -enableMPLS true

		mpls setDefault
		mpls config -type mplsUnicast

		mplsLabel setDefault
		mplsLabel config -label $MplsLabel
		mplsLabel config -bottomOfStack $MplsBottom
		mplsLabel config -experimentalUse $MplsExp  
		mplsLabel config -timeToLive $MplsTtl 
		mplsLabel set 1

		mpls set $Chas $Card $Port
	}
	if {$Protocl == "arp"} {
		arp setDefault
		arp config -sourceProtocolAddr $SenderIp 
		switch -exact $SenderIpMode {
			fix {arp config -sourceProtocolAddrMode 0}
			increment {arp config -sourceProtocolAddrMode 1}
			decrement {arp config -sourceProtocolAddrMode 2}
			continueincrement {arp config -sourceProtocolAddrMode 3}
			continuedecrement {arp config -sourceProtocolAddrMode 4}
		}
		arp config -sourceProtocolAddrRepeatCount $SenderIpNum 
		
		arp config -destProtocolAddr $TargetIp 
		switch -exact $TargetIpMode {
			fix {arp config -destProtocolAddrMode 0}
			increment {arp config -destProtocolAddrMode 1}
			decrement {arp config -destProtocolAddrMode 2}
			continueincrement {arp config -destProtocolAddrMode 3}
			continuedecrement {arp config -destProtocolAddrMode 4}
		}
		arp config -destProtocolAddrRepeatCount $TargetIpNum 
		
		arp config -operation $ArpOperation 
		
		arp config -sourceHardwareAddr $SenderMac 
		switch -exact $SenderMacMode {
			Fixed {arp config -sourceHardwareAddrMode 0}
			Increment {arp config -sourceHardwareAddrMode 1}
			Decrement {arp config -sourceHardwareAddrMode 2}
		}
		arp config -sourceHardwareAddrRepeatCount $SenderMacNum 
		
		arp config -destHardwareAddr $TargetMac 
		switch -exact $TargetMacMode {
			Fixed {arp config -destHardwareAddrMode 0}
			Increment {arp config -destHardwareAddrMode 1}
			Decrement {arp config -destHardwareAddrMode 2}
		}
		arp config -destHardwareAddrRepeatCount $TargetMacNum 
		if {[arp set $Chas $Card $Port] != 0} {
			puts "arp set error!!!"
		}
		#stream set $Chas $Card $Port 1
	}
	
	# Set up IP
	#ip setDefault
	if {$Protocl == "ipv4" || $Protocl == "ipv6ipv4"} {
		ip setDefault
		ip config -sourceIpAddr $SouIp
		ip config -sourceIpMask $SouMask
		ip config -sourceClass $SouClassMode
		ip config -sourceIpAddrMode $SouIpMode
		ip config -sourceIpAddrRepeatCount $SouIpNum
		
		ip config -destIpAddr $DesIp
		ip config -destIpMask $DesMask
		ip config -destClass $DesClassMode	
		ip config -destIpAddrMode $DesIpMode
		ip config -destIpAddrRepeatCount $DesIpNum
	    
	    ip config -fragment $Fragment
	    ip config -lastFragment $LastFragment
	    ip config -fragmentOffset $FragmentOffset
	    ip config -totalLength $TotalLength
	    ip config -useValidChecksum $ValidChecksum
        ip config -lengthOverride $LengthOverride
        ip config -ttl $TTL
		if {$PriorityFlag == 0} {
			SetTos $Tos
		} elseif {$PriorityFlag == 1} {
			SetDscp $Dscp
		} elseif {$PriorityFlag == 2} {
			SetIpprecedence $Ipprecedence
		} elseif {$PriorityFlag == 3} {
			SetIpprecedenceTos $Ipprecedence $Tos
		} else {
			puts "wrong PriorityFlag!"
		}
		#if {$ProtoclEx != "none"} {
		#add by qiaoyua
		if {$ProtoclEx == "rip"} {
			ip config -ipProtocol udp
		} else {
			ip config -ipProtocol $ProtoclEx
		}
		#}

	    if {[ip set $Chas $Card $Port] != 0} {
	    	puts "ip set error!!!"
	    }
	    
		if {$ProtoclEx == "tcp"} {
			tcp setDefault
			tcp config -sourcePort $SPort
			tcp config -destPort $DPort
			tcp config -sequenceNumber $SequenceNum
			tcp config -offset $HeaderLength
			tcp config -acknowledgeValid $ACK
			tcp config -finished $FIN
			tcp config -pushFunctionValid $PSH
			tcp config -resetConnection $RST
			tcp config -urgentPointerValid $URG
			tcp config -synchronize $SYN
			tcp set $Chas $Card $Port
		}
		if {$ProtoclEx == "udp" || $ProtoclEx == "dhcpoffer" || $ProtoclEx == "dhcpack" || $ProtoclEx == "dhcprelease" || $ProtoclEx == "dhcpdiscover" || $ProtoclEx == "dhcprequest" || $ProtoclEx == "dhcperror" } {
			udp setDefault
			udp config -sourcePort $SPort
			udp config -destPort $DPort
			udp set $Chas $Card $Port
			#puts [udp set $Chas $Card $Port]
			if {$ProtoclEx == "dhcpoffer"} {
			    dhcp setDefault
			    dhcp config -opCode $OpCode
			    dhcp config -yourIpAddr $YourIpAddr
			    dhcp config -clientHwAddr $ClientHwAddr
			    dhcp config -optionData $DhcpMessageType
			    dhcp setOption dhcpMessageType
			    dhcp config -optionData $DhcpSvrIdentifier
			    dhcp setOption dhcpSvrIdentifier
			    dhcp config -optionData $DhcpIPAddrLeaseTime
			    dhcp setOption dhcpIPAddrLeaseTime
			    dhcp config -optionData $DhcpRenewalTimeValue
			    dhcp setOption dhcpRenewalTimeValue
			    dhcp config -optionData $DhcpRebindingTimeValue
			    dhcp setOption dhcpRebindingTimeValue
			    dhcp config -optionData $DhcpSubnetMask
			    dhcp setOption dhcpSubnetMask
			    dhcp setOption dhcpEnd
			    dhcp set $Chas $Card $Port
			}
			if {$ProtoclEx == "dhcpack"} {
			    dhcp setDefault
			    dhcp config -opCode $OpCode
			    dhcp config -yourIpAddr $YourIpAddr
			    dhcp config -clientHwAddr $ClientHwAddr
			    dhcp config -optionData $DhcpMessageType
			    dhcp setOption dhcpMessageType
			    dhcp config -optionData $DhcpSvrIdentifier
			    dhcp setOption dhcpSvrIdentifier
			    dhcp config -optionData $DhcpIPAddrLeaseTime
			    dhcp setOption dhcpIPAddrLeaseTime
			    dhcp config -optionData $DhcpRenewalTimeValue
			    dhcp setOption dhcpRenewalTimeValue
			    dhcp config -optionData $DhcpRebindingTimeValue
			    dhcp setOption dhcpRebindingTimeValue
			    dhcp config -optionData $DhcpSubnetMask
			    dhcp setOption dhcpSubnetMask
			    dhcp setOption dhcpEnd
			    dhcp set $Chas $Card $Port
			}
			if {$ProtoclEx == "dhcprelease"} {
			    dhcp setDefault
			    dhcp config -opCode $OpCode
			    dhcp config -clientHwAddr $ClientHwAddr
			    dhcp config -clientIpAddr $ClientIpAddr
			    dhcp config -optionData $DhcpMessageType
			    dhcp setOption dhcpMessageType
			    dhcp config -optionData $DhcpClientId
                dhcp setOption dhcpClientId
                dhcp config -optionData $DhcpSvrIdentifier
                dhcp setOption dhcpSvrIdentifier
			    dhcp setOption dhcpEnd
			    dhcp set $Chas $Card $Port
			}
			if {$ProtoclEx == "dhcpdiscover"} {
			    dhcp setDefault
			    dhcp config -opCode $OpCode
			    dhcp config -clientHwAddr $ClientHwAddr
			    dhcp config -optionData $DhcpMessageType
			    dhcp setOption dhcpMessageType
			    dhcp config -optionData $DhcpParamRequestList
                dhcp setOption dhcpParamRequestList
			    dhcp config -optionData $DhcpClientId
                dhcp setOption dhcpClientId
			    dhcp setOption dhcpEnd
			    dhcp set $Chas $Card $Port
			}
			if {$ProtoclEx == "dhcprequest"} {
			    dhcp setDefault
			    dhcp config -opCode $OpCode
			    dhcp config -clientHwAddr $ClientHwAddr
			    dhcp config -optionData $DhcpMessageType
			    dhcp setOption dhcpMessageType
			    dhcp config -optionData $DhcpParamRequestList
                dhcp setOption dhcpParamRequestList
			    dhcp config -optionData $DhcpClientId
                dhcp setOption dhcpClientId
                dhcp config -optionData $DhcpSvrIdentifier
                dhcp setOption dhcpSvrIdentifier
                dhcp config -optionData $DhcpRequestedIPAddr
                dhcp setOption dhcpRequestedIPAddr
			    dhcp setOption dhcpEnd
			    dhcp set $Chas $Card $Port
			}
			if {$ProtoclEx == "dhcperror"} {
			    dhcp setDefault
			    dhcp config -opCode $OpCode
			    dhcp config -hwLen $HardwareAddressLength
			    dhcp config -hops $Hops
			    dhcp config -transactionID $TransactionID
			    dhcp config -yourIpAddr $YourIpAddr
			    dhcp config -clientHwAddr $ClientHwAddr
			    dhcp config -optionData $DhcpMessageType
			    dhcp setOption dhcpMessageType
			    dhcp config -optionData $DhcpSvrIdentifier
                dhcp setOption dhcpSvrIdentifier
                dhcp config -optionData $DhcpIPAddrLeaseTime
                dhcp setOption dhcpIPAddrLeaseTime
                dhcp config -optionData $DhcpRenewalTimeValue
                dhcp setOption dhcpRenewalTimeValue
                dhcp config -optionData $DhcpRebindingTimeValue
                dhcp setOption dhcpRebindingTimeValue
                dhcp config -optionData $DhcpSubnetMask
                dhcp setOption dhcpSubnetMask
                dhcp setOption dhcpEnd
			    dhcp set $Chas $Card $Port
			}
		}
		if {$ProtoclEx == "icmp"} {
			icmp setDefault
			icmp config -type $Type
			icmp config -code $Code
			icmp config -sequence $Sequence
			icmp set $Chas $Card $Port
		}
		if {$ProtoclEx == "igmp"} {
		#igmp config -type dvmrpMessage dvmrp的路由信息是放在igmp数据包中传输的，、
		#IXIA手工不可以配置该项，脚本可以配置，但未补充
            if {$Type == 0} {
                set Type query
                set IgmpGroupAddress 0.0.0.0
            }
			igmp setDefault
			igmp config -version $IgmpVersion
			if {$IgmpVersion == 1} {
			    switch -exact -- $Type {
			        17 -
			        query {
			        	igmp config -type membershipQuery
			        	igmp config -maxResponseTime 0
			        }
			        18 -
			        report {igmp config -type membershipReport1}
			        default {puts "Wrong para of igmp-type $Type!";return -1}
			    }
			    igmp config -groupIpAddress $IgmpGroupAddress
			    igmp config -mode $IgmpMode
			    if { $IgmpMode == "igmpIncrement" || $IgmpMode == "igmpDecrement" } {
    			    igmp config -repeatCount $IgmpRepeat
    			}
    			igmp config -useValidChecksum $ValidChecksum
    	    }    
			if {$IgmpVersion == 2} {
			    switch -exact -- $Type {
			        17 -
			        query {igmp config -type membershipQuery}
			        22 -
			        report {igmp config -type membershipReport2}
			        23 -
			        leave {igmp config -type leaveGroup}
			        default {puts "Wrong para of igmp-type $Type!";return -1}
			    }
			    igmp config -groupIpAddress $IgmpGroupAddress
			    igmp config -mode $IgmpMode
			    if { $IgmpMode == "igmpIncrement" || $IgmpMode == "igmpDecrement" } {
    			    igmp config -repeatCount $IgmpRepeat
    			}
    			igmp config -maxResponseTime $MaxResponseTime
    			igmp config -useValidChecksum $ValidChecksum
			}			
			if {$IgmpVersion == 3} {
			    switch -exact -- $Type {
			        17 -
			        query {
			            igmp config -type membershipQuery
			            igmp config -groupIpAddress $IgmpGroupAddress
			            igmp config -mode $IgmpMode
			            if { $IgmpMode == "igmpIncrement" || $IgmpMode == "igmpDecrement" } {
    			            igmp config -repeatCount $IgmpRepeat
    			        }
    			        igmp config -sourceIpAddressList [split $IgmpSourceIpAddress " "]
    			        igmp config -qqic $QQIC
    			        igmp config -qrv $QRV
    			        igmp config -enableS $EnableS
    			        igmp config -maxResponseTime $MaxResponseTime
    			        igmp config -useValidChecksum $ValidChecksum 
			        }
			        34 -
			        report {
			            igmp config -type membershipReport3
			            #igmp config -groupIpAddress 0.0.0.0
                        #igmp config -maxResponseTime 100
                        #igmp config -mode igmpIdle
                        #igmp config -repeatCount 1
                        #igmp config -useValidChecksum true
                        #igmp config -qqic 127
                        #igmp config -qrv 0
                        #igmp config -enableS false
                        #igmp config -sourceIpAddressList {}
			            igmp clearGroupRecords
        			    igmpGroupRecord setDefault
        			    if {$IgmpGroupRecord != "NULL"} {        			        
        			        set igmpgrouprecordnum [llength $IgmpGroupRecord]
        			        for {set i 0} {$i < $igmpgrouprecordnum} {incr i} {
        			            igmpGroupRecord config -multicastAddress [lindex [lindex $IgmpGroupRecord $i] 0]
                                switch -exact -- [lindex [lindex $IgmpGroupRecord $i] 1] {
                			        1 -
                			        include {igmpGroupRecord config -type igmpModeIsInclude;}
                			        2 -
                			        exclude {igmpGroupRecord config -type igmpModeIsExclude}
                			        3 -
                			        toinclude -
                			        toInclude {igmpGroupRecord config -type igmpChangeToIncludeMode}
                			        4 -
                			        toexclude -
                			        toExclude {igmpGroupRecord config -type igmpChangeToExcludeMode}
                			        5 -
                			        allow {igmpGroupRecord config -type igmpAllowNewSources}
                			        6 -
                			        block {igmpGroupRecord config -type igmpBlockOldSources}
                			        default {puts "Wrong para of igmp-type [lindex [lindex $IgmpGroupRecord $i] 1]!";return -1}
                			    }
                			    igmpGroupRecord config -sourceIpAddressList [split [lindex [lindex $IgmpGroupRecord $i] 2] " "]
                			    set temp [igmp addGroupRecord]
                			    #puts "temp = $temp"
                			}
                	    } else {
                	        #为兼容以前的脚本，保留该分支
            			    igmpGroupRecord config -multicastAddress $IgmpGroupAddress
            			    igmpGroupRecord config -type 1
            			    igmpGroupRecord config -sourceIpAddressList [list [list $IgmpSourceIpAddress]]		    
            			    igmp addGroupRecord
            			}
			            
			        }
			        default {puts "Wrong para of igmp-type $type!";return -1}
			    }
			    
			}
			if {[igmp set $Chas $Card $Port] != 0} {
				puts "igmp set error!!!!"
			}
		}
		#add by qiaoyua
		if {$ProtoclEx == "rip"} {
			udp setDefault
			udp config -sourcePort 520
			udp config -destPort 520
			udp set $Chas $Card $Port
			# Set up Rip in general
			rip setDefault
			rip config -command $RipCommand
			rip config -version $RipVersion
			# Set up Rip Routes
			ripRoute setDefault
			for {set i 1} {$i <= [llength $RipRoute]} {incr i} {
				set ripentry [lindex $RipRoute [expr $i - 1]]
				set position [lsearch $ripentry "Family"]
				if {$position != -1} {
					ripRoute config -familyId [lindex $ripentry [expr $position + 1]]
				} else {
					ripRoute config -familyId 2
				}
				set position [lsearch $ripentry "Tag"]
				if {$position != -1} {
					ripRoute config -routeTag [lindex $ripentry [expr $position + 1]]
				} else {
					ripRoute config -routeTag 0
				}
				set position [lsearch $ripentry "Ip"]
				if {$position != -1} {
					ripRoute config -ipAddress [lindex $ripentry [expr $position + 1]]
				}
				set position [lsearch $ripentry "Mask"]
				if {$position != -1} {
					ripRoute config -subnetMask [lindex $ripentry [expr $position + 1]]
				}
				set position [lsearch $ripentry "Nexthop"]
				if {$position != -1} {
					ripRoute config -nextHop [lindex $ripentry [expr $position + 1]]
				}
				set position [lsearch $ripentry "Metric"]
				if {$position != -1} {
					ripRoute config -metric [lindex $ripentry [expr $position + 1]]
				}
				ripRoute set $i
			}
			rip set $Chas $Card $Port
		}

		#add by zhaohj
		#只提供了ospf接口，里面的字段未配置，默认值，hello包
		if {$ProtoclEx == "ospf"} {		
			ip config -ipProtocol ipV4ProtocolOspf			
			ip set $Chas $Card $Port
		}


		#add by zhangfank,2010.7.6,GREv4 Tunnel
		if {$ProtoclEx == "gre"} {
			if {$GreInnerProtocol == "ipv4"} {
				set GreInnerProtocol "08 00"	;#内层封装的报文为ipv4报文
				ip setDefault
				ip config -sourceIpAddr $GreInnerSouIp
				ip config -sourceIpMask $GreInnerSouMask
				ip config -destIpAddr $GreInnerDesIp
				ip config -destIpMask $GreInnerDesMask
				if {$GreInnerProtocolEx == "none"} {
					ip config -ipProtocol ipV4ProtocolReserved255
				}
				if {$GreInnerProtocolEx == "tcp"} {
					ip config -ipProtocol ipV4ProtocolTcp
					tcp setDefault
					tcp config -sourcePort $greSPort
					tcp config -destPort $greDPort
					tcp config -urgentPointerValid $greURG
					tcp config -acknowledgeValid $greACK
					tcp config -pushFunctionValid $grePSH
					tcp config -resetConnection $greRST
					tcp config -synchronize $greSYN
					tcp config -finished $greFIN
					tcp set $Chas $Card $Port
				}
				if {$GreInnerProtocolEx == "udp"} {
					ip config -ipProtocol ipV4ProtocolUdp
					udp setDefault        
					udp config -sourcePort $greSPort
					udp config -destPort $greDPort
					udp set $Chas $Card $Port
				}
				if {$GreInnerProtocolEx == "icmp"} {
					ip config -ipProtocol ipV4ProtocolIcmp
					icmp setDefault        
					icmp config -type $greType
					icmp config -code $greCode
					icmp set $Chas $Card $Port
				}	
				ip set $Chas $Card $Port
				gre config -reserved0 $GreHeaderReserved0
				gre config -protocolType $GreInnerProtocol
				gre set $Chas $Card $Port
			} elseif {$GreInnerProtocol == "ipv6"} {
				set GreInnerProtocol "86 dd"	;#内层封装的报文为ipv6报文
				ipV6 setDefault
				ipV6 config -sourceAddr $GreInnerSouIpv6
				ipV6 config -sourceMask $GreInnerSouMaskv6
				ipV6 config -destAddr $GreInnerDesIpv6
				ipV6 config -destMask $GreInnerDesMaskv6
				if {$GreInnerProtocolEx == "none"} {
  					ipV6 config -nextHeader ipV6NoNextHeader
  				}
  				if {$GreInnerProtocolEx == "icmpv6"} {
  					ipV6 config -nextHeader ipV4ProtocolIpv6Icmp
  				}
  				if {$GreInnerProtocolEx == "tcp"} {
					ipV6 config -nextHeader ipV4ProtocolTcp
					ipV6 clearAllExtensionHeaders 
					ipV6 addExtensionHeader ipV4ProtocolTcp
					tcp setDefault
					tcp config -sourcePort $greSPort
					tcp config -destPort $greDPort
					tcp config -urgentPointerValid $greURG
					tcp config -acknowledgeValid $greACK
					tcp config -pushFunctionValid $grePSH
					tcp config -resetConnection $greRST
					tcp config -synchronize $greSYN
					tcp config -finished $greFIN
					tcp set $Chas $Card $Port
				}
				if {$GreInnerProtocolEx == "udp"} {
					ipV6 config -nextHeader ipV4ProtocolUdp
					ipV6 clearAllExtensionHeaders 
					ipV6 addExtensionHeader ipV4ProtocolTcp
					udp setDefault        
					udp config -sourcePort $greSPort
					udp config -destPort $greDPort
					udp set $Chas $Card $Port
				}
				ipV6 set $Chas $Card $Port
				gre config -reserved0 $GreHeaderReserved0
				gre config -protocolType $GreInnerProtocol
				gre set $Chas $Card $Port
			}
			#Outer ipv4 header
			ip setDefault
			ip config -ipProtocol ipV4ProtocolGre
			ip config -sourceIpAddr $SouIp
			ip config -sourceIpMask $SouMask
			ip config -destIpAddr $DesIp
			ip config -destIpMask $DesMask
			ip set $Chas $Card $Port
		}	
			
	}



	
	# Set up IPv6
	#ipV6 setDefault
	if {$Protocl == "ipv6" || $Protocl == "ipv6ipv4"} {
	    #为了避免IXIA端口配置为ipv6ipv4报文后再配置ipv6报文导致实际配置的还是ipv6ipv4报文（可能是ixia的一个bug）
	    #增加如下的判断信息
	    if {$Protocl == "ipv6"} {
	        ip setDefault
	        ip set $Chas $Card $Port
	    }
		ipV6 setDefault
		ipV6 config -sourceAddr $SouIpv6
		ipV6 config -sourceStepSize $SouStepSizev6
		ipV6 config -sourceAddrRepeatCount $SouNumv6
		#default mask 64  ipIncrNetwork
		if {$SouAddrModev6 == "Fixed"} {
		    ipV6 config -sourceAddrMode ipV6Idle
		}
		if {$SouAddrModev6 == "IncrHost"} {
			if {[ regexp -nocase [string range $SouIpv6 0 1] ff] == 1} {
		        ipV6 config -sourceAddrMode 15
		    } else {
    			ipV6 config -sourceAddrMode 5
    		}
    		ipV6 config -sourceMask 96
		}
#		if {$SouAddrModev6 == "IncrNetwork"} {
#			puts "incrnetworik"
#			ipV6 config -sourceAddrMode ipV6IncrNetwork	
#		}
        if {$SouAddrModev6 == "IncrSiteNetwork"} {
			ipV6 config -sourceAddrMode 11
			ipV6 config -sourceMask 48
		}
		if {$SouAddrModev6 == "IncrNextLevelNetwork"} {
			ipV6 config -sourceAddrMode 9       ;#only cpu support
			ipV6 config -sourceMask 24
		}
		if {$SouAddrModev6 == "IncrTopLevelNetwork"} {
			ipV6 config -sourceAddrMode 7
			ipV6 config -sourceMask 4
		}
		if {$SouAddrModev6 == "DecrHost"} {
			if {[ regexp -nocase [string range $SouIpv6 0 1] ff] == 1} {
		        ipV6 config -sourceAddrMode 16
		    } else {
    			ipV6 config -sourceAddrMode 2
    		}
    		ipV6 config -sourceMask 96
		}
		if {$SouAddrModev6 == "DecrSiteNetwork"} {
			ipV6 config -sourceAddrMode 12
			ipV6 config -sourceMask 48
		}
		if {$SouAddrModev6 == "DecrNextLevelNetwork"} {
			ipV6 config -sourceAddrMode 10
			ipV6 config -sourceMask 24
		}
		if {$SouAddrModev6 == "DecrTopLevelNetwork"} {
			ipV6 config -sourceAddrMode 8
			ipV6 config -sourceMask 4
		}
		#ipV6 config -sourceMask $SouNetworkv6
		
		ipV6 config -destAddr $DesIpv6
		ipV6 config -destStepSize $DesStepSizev6
		ipV6 config -destAddrRepeatCount $DesNumv6
		if {$DesAddrModev6 == "Fixed"} {
		    ipV6 config -destAddrMode ipV6Idle
		}
		if {$DesAddrModev6 == "IncrHost"} {
		    if {[ regexp -nocase [string range $DesIpv6 0 1] ff] == 1} {
		        ipV6 config -destAddrMode 15
		    } else {
    			ipV6 config -destAddrMode 5
    			#puts aa
    		}
    		ipV6 config -destMask 96
		}
#		if {$DesAddrModev6 == "IncrNetwork"} {
#			ipV6 config -destAddrMode ipV6IncrNetwork	
#		}
        if {$DesAddrModev6 == "IncrSiteNetwork"} {
			ipV6 config -destAddrMode 11
			ipV6 config -destMask 48
		}
		if {$DesAddrModev6 == "IncrNextLevelNetwork"} {
			ipV6 config -destAddrMode 9
			ipV6 config -destMask 24
		}
		if {$DesAddrModev6 == "IncrTopLevelNetwork"} {
			ipV6 config -destAddrMode 7
			ipV6 config -destMask 4
		}
		if {$DesAddrModev6 == "DecrHost"} {
		    if {[ regexp -nocase [string range $DesIpv6 0 1] ff] == 1} {
		        ipV6 config -destAddrMode 16
		    } else {
    			ipV6 config -destAddrMode 2
    			#puts aa
    		}
    		ipV6 config -destMask 96
		}
		if {$DesAddrModev6 == "DecrSiteNetwork"} {
			ipV6 config -destAddrMode 12
			ipV6 config -destMask 48
		}
		if {$DesAddrModev6 == "DecrNextLevelNetwork"} {
			ipV6 config -destAddrMode 10
			ipV6 config -destMask 24
		}
		if {$DesAddrModev6 == "DecrTopLevelNetwork"} {
			ipV6 config -destAddrMode 8
			ipV6 config -destMask 4
		}
		#ipV6 config -destMask $DesNetworkv6
		
		#set traffic class and FlowLabel
	    ipV6 config -trafficClass $TrafficClass
        ipV6 config -flowLabel $FlowLabel
        ipV6 config -hopLimit $HopLimit
        #ipV6 config -nextHeader $NextHeader
#	    if { $ProtoclEx == "none" } {
#	  	    ipV6 config -nextHeader $NextHeader
#    	    puts "aa"
#	    } else {
#	  	    ipV6 config -nextHeader $ProtoclEx
#	  	    puts "bb"
#	    }
        #ipV6 clearAllExtensionHeaders
        if { $ProtoclEx == "none" } {
            #puts "ProtoclEx = $ProtoclEx"
            ipV6 config -nextHeader ipV6NoNextHeader
            ipV6 clearAllExtensionHeaders
        }
	    if { $ProtoclEx == "HopByHop" } {
	        #puts "cc1"
	        ipV6 clearAllExtensionHeaders
	        ipV6 config -nextHeader ipV6HopByHopOptions	        
	        ipV6HopByHop clearAllOptions
	        ipV6OptionPADN setDefault
	        ipV6OptionPADN config -length 4
	        ipV6OptionPADN config -value "00 00 00 00"
	        ipV6HopByHop addOption ipV6OptionPADN
#	  	    ipV6HopByHopOptions setDefault
#	  	    ipV6HopByHopOptions config -reserved {00 00 01 02}
#	  	    ipV6HopByHopOptions config -nodeList {FE80:0000:0000:0000:8888:8888:8888:8888}
	  	    ipV6 addExtensionHeader ipV6HopByHopOptions
	  	}
	    if { $ProtoclEx == "Routing" } {
	        #puts "cc2"
	        ipV6 clearAllExtensionHeaders
	        ipV6 config -nextHeader ipV6Routing	        
	  	    ipV6Routing setDefault
	  	    ipV6Routing config -reserved "00 00 00 00"
	  	    ipV6Routing config -nodeList ""
	  	    ipV6 addExtensionHeader ipV6Routing
	  	}
	  	if { $ProtoclEx == "Fragment" } {
	  	    #puts "cc3"
	  	    ipV6 clearAllExtensionHeaders
	  	    ipV6 config -nextHeader ipV6Fragment	  	    
	  	    ipV6Fragment setDefault
            ipV6Fragment config -enableFlag true
            ipV6Fragment config -fragmentOffset 100
            ipV6Fragment config -identification 286335522
            ipV6Fragment config -res 3
            ipV6Fragment config -reserved 30
	  	    ipV6 addExtensionHeader ipV6Fragment
	  	}

	  	#added by zhangfank,2009.5.5
        if { $ProtoclEx == "icmpv6-fragment1" } {
            ipV6 clearAllExtensionHeaders
	  	    ipV6 config -nextHeader ipV6Fragment	  	    
	  	    ipV6Fragment setDefault
	  	    #判断是否是分片的最后一片,借用了ipv4的LastFragment变量
	  	    if { $LastFragment == 0 } {
                ipV6Fragment config -enableFlag true
            } else {
                ipV6Fragment config -enableFlag false
            }    
            ipV6Fragment config -fragmentOffset $FragmentOffset
            ipV6Fragment config -identification 100
            ipV6Fragment config -res 0
            ipV6Fragment config -reserved 0
	  	    ipV6 addExtensionHeader ipV6Fragment

	  	    ipV6 addExtensionHeader ipV4ProtocolIpv6Icmp
	  	}

		#added by zhangfank,2009.5.6
        if { $ProtoclEx == "icmpv6-fragment2" } {
            ipV6 clearAllExtensionHeaders
	  	    ipV6 config -nextHeader ipV6Fragment	  	    
	  	    ipV6Fragment setDefault
	  	    #判断是否是分片的最后一片,借用了ipv4的LastFragment变量
	  	    if { $LastFragment == 0 } {
                ipV6Fragment config -enableFlag true
            } else {
                ipV6Fragment config -enableFlag false
            }    
            ipV6Fragment config -fragmentOffset $FragmentOffset
            ipV6Fragment config -identification 100
            ipV6Fragment config -res 0
            ipV6Fragment config -reserved 0
	  	    ipV6 addExtensionHeader ipV6Fragment

	  	    ipV6 addExtensionHeader ipV6NoNextHeader
	  	}    
	  	
	  	
	  	if { $ProtoclEx == "Authentication" } {
	  	    #puts "cc4"
	  	    ipV6 clearAllExtensionHeaders
	  	    ipV6 config -nextHeader ipV6Authentication	  	    
	  	    ipV6Authentication setDefault
	  	    ipV6Authentication config -payloadLength 2
            ipV6Authentication config -securityParamIndex 0
	  	    ipV6Authentication config -sequenceNumberField 0
	  	    ipV6Authentication config -authentication "00 00 00 00"
	  	    ipV6 addExtensionHeader ipV6Authentication
	  	}
	  	if { $ProtoclEx == "Destination" } {
	  	    #puts "cc5"
	  	    ipV6 config -nextHeader ipV6DestinationOptions
	  	    ipV6 clearAllExtensionHeaders
	  	    ipV6Destination setDefault
	  	    ipV6 addExtensionHeader ipV6DestinationOptions
	  	}
		if { $ProtoclEx == "tcp" } {
			#puts "TCP"
			ipV6 config -nextHeader ipV4ProtocolTcp
			ipV6 clearAllExtensionHeaders
			ipV6 addExtensionHeader ipV4ProtocolTcp
			tcp setDefault
			tcp config -sourcePort $SPort
			tcp config -destPort $DPort
			tcp config -acknowledgeValid $ACK
			tcp config -finished $FIN
			tcp config -pushFunctionValid $PSH
			tcp config -resetConnection $RST
			tcp config -urgentPointerValid $URG
			tcp config -synchronize $SYN
			tcp set $Chas $Card $Port
		}
		if { $ProtoclEx == "udp" } {
			#puts "UDP"
			ipV6 config -nextHeader ipV4ProtocolUdp
			ipV6 clearAllExtensionHeaders
  		    ipV6 addExtensionHeader ipV4ProtocolUdp
			udp setDefault
			udp config -sourcePort $SPort
			udp config -destPort $DPort
			udp set $Chas $Card $Port
		    #set bb [ udp set $Chas $Card $Port ]
			#puts $bb
		}
		if {$ProtoclEx == "icmpV6"} {
#    		puts "ICMPV6"
    		ipV6 config -nextHeader ipV4ProtocolIpv6Icmp
    		ipV6 clearAllExtensionHeaders
#			ipV6 addExtensionHeader $ProtoclEx
#			icmp setDefault
#			icmp config -type $Type
#			icmp config -code $Code
#			icmp set $Chas $Card $Port
			#set cc [ icmp set $Chas $Card $Port ]
			#puts $cc
		}
		if {$ProtoclEx == "mld" || $ProtoclEx == "icmpV6-request"} {
    		ipV6 clearAllExtensionHeaders
			ipV6 config -nextHeader ipV6HopByHopOptions

			ipV6HopByHop clearAllOptions   
			ipV6OptionRouterAlert setDefault        
			ipV6OptionRouterAlert config -length 2
			ipV6OptionRouterAlert config -routerAlert ipV6RouterAlertMLD
			ipV6HopByHop addOption ipV6OptionRouterAlert

			ipV6OptionPADN setDefault        
			ipV6OptionPADN config -length 0
			ipV6OptionPADN config -value ""
			ipV6HopByHop addOption ipV6OptionPADN

			ipV6 addExtensionHeader ipV6HopByHopOptions

			ipV6 addExtensionHeader ipV4ProtocolIpv6Icmp
		}

		#add by zhangfank,2010.7.7,Grev6 tunnel
		if {$ProtoclEx == "gre"} {
			if {$GreInnerProtocol == "ipv4"} {
				set GreInnerProtocol "08 00"	;#内层封装的报文为ipv4报文
				ip setDefault
				ip config -sourceIpAddr $GreInnerSouIp
				ip config -sourceIpMask $GreInnerSouMask
				ip config -destIpAddr $GreInnerDesIp
				ip config -destIpMask $GreInnerDesMask
				if {$GreInnerProtocolEx == "none"} {
					ip config -ipProtocol ipV4ProtocolReserved255
				}
				if {$GreInnerProtocolEx == "tcp"} {
					ip config -ipProtocol ipV4ProtocolTcp
					tcp setDefault
					tcp config -sourcePort $greSPort
					tcp config -destPort $greDPort
					tcp config -urgentPointerValid $greURG
					tcp config -acknowledgeValid $greACK
					tcp config -pushFunctionValid $grePSH
					tcp config -resetConnection $greRST
					tcp config -synchronize $greSYN
					tcp config -finished $greFIN
					tcp set $Chas $Card $Port
				}
				if {$GreInnerProtocolEx == "udp"} {
					ip config -ipProtocol ipV4ProtocolUdp
					udp setDefault        
					udp config -sourcePort $greSPort
					udp config -destPort $greDPort
					udp set $Chas $Card $Port
				}
				if {$GreInnerProtocolEx == "icmp"} {
					ip config -ipProtocol ipV4ProtocolIcmp
					icmp setDefault        
					icmp config -type $greType
					icmp config -code $greCode
					icmp set $Chas $Card $Port
				}
				ip set $Chas $Card $Port
				gre config -reserved0 $GreHeaderReserved0
				gre config -protocolType $GreInnerProtocol
				gre set $Chas $Card $Port
			} elseif {$GreInnerProtocol == "ipv6"} {
				set GreInnerProtocol "86 dd"	;#内层封装的报文为ipv6报文
				ipV6 setDefault
				ipV6 config -sourceAddr $GreInnerSouIpv6
				ipV6 config -sourceMask $GreInnerSouMaskv6
				ipV6 config -destAddr $GreInnerDesIpv6
				ipV6 config -destMask $GreInnerDesMaskv6
  				if {$GreInnerProtocolEx == "none"} {
  					ipV6 config -nextHeader ipV6NoNextHeader
  				}
  				if {$GreInnerProtocolEx == "icmpv6"} {
  					ipV6 config -nextHeader ipV4ProtocolIpv6Icmp
  				}
  				if {$GreInnerProtocolEx == "tcp"} {
					ipV6 config -nextHeader ipV4ProtocolTcp
					ipV6 clearAllExtensionHeaders 
					ipV6 addExtensionHeader ipV4ProtocolTcp
					tcp setDefault
					tcp config -sourcePort $greSPort
					tcp config -destPort $greDPort
					tcp config -urgentPointerValid $greURG
					tcp config -acknowledgeValid $greACK
					tcp config -pushFunctionValid $grePSH
					tcp config -resetConnection $greRST
					tcp config -synchronize $greSYN
					tcp config -finished $greFIN
					tcp set $Chas $Card $Port
				}
				if {$GreInnerProtocolEx == "udp"} {
					ipV6 config -nextHeader ipV4ProtocolUdp
					ipV6 clearAllExtensionHeaders 
					ipV6 addExtensionHeader ipV4ProtocolTcp
					udp setDefault        
					udp config -sourcePort $greSPort
					udp config -destPort $greDPort
					udp set $Chas $Card $Port
				}
				ipV6 set $Chas $Card $Port
				gre config -reserved0 $GreHeaderReserved0
				gre config -protocolType $GreInnerProtocol
				gre set $Chas $Card $Port
			}
			#Outer ipv6 header
			ipV6 setDefault
			ipV6 config -nextHeader ipV4ProtocolGre
			ipV6 config -sourceAddr $SouIpv6
			ipV6 config -sourceMask $SouNetworkv6
			ipV6 config -destAddr $DesIpv6
			ipV6 config -destMask $DesNetworkv6
			ipV6 clearAllExtensionHeaders 
			ipV6 addExtensionHeader ipV4ProtocolGre
			ipV6 set $Chas $Card $Port
		}	
			
        if {[ipV6 set $Chas $Card $Port] != 0} {
        	puts "ipv6 set error!!!"
        }
	}
	#ipV6 set $Chas $Card $Port
}

################################
#
# SetIxiaUDF:SetIxiaStream内部调用函数
#
# args:
# 
# return:
#
# addition:
#    
# examples:
#
###############################
proc SetIxiaUDF { udf offset length value continueflag repeat step increasemode } {
	udf setDefault
    udf config -enable true
    udf config -offset $offset
    switch $length {
        1 { udf config -countertype c8 }
        2 { udf config -countertype c16 }
        3 { udf config -countertype c24 }
        4 { udf config -countertype c32 }
    }
    udf config -continuousCount $continueflag
    #puts "increasemode == $increasemode"
    if { $increasemode == "up" } {
	    udf config -updown uuuu
	    #puts normarlcardup
	} else {
		udf config -updown duuu
		#puts normarlcarddown
	}
    udf config -repeat $repeat
    udf config -initval [FormatHex $value]
    udf config -step $step
    if [udf set $udf] {
    	puts cpucard
    	if { $increasemode == "up" } {
		    udf config -updown uddd
		    #puts cpucardup
		} else {
			udf config -updown dddd
			#puts cpucarddown
		}
		udf set $udf
	}
}

#added by lixiaa 2010-7-13
proc  FormatIpv6VrrpSegment { SrcIpv6 DstIpv6 VrrpInfo } {
    set segment1 ""
    set segment2 ""
    set version 3
    set type 1
    set vrid 10
    set pri 100
    set count 1
    set advint 100
    set checksum 0
    set ipv6addr fe80::10
    set Ipv6PseudoHeader ""
    array set Data $VrrpInfo
    if {[info exists Data(Version)]} {
        set version $Data(Version)
    }
    append segment1 [format "%0x" $version]
    if {[info exists Data(Type)]} {
        set type $Data(Type)
    }
    append segment1 [format "%0x" $type]
    if {[info exists Data(Vrid)]} {
        set vrid $Data(Vrid)
    }
    append segment1 [format "%02x" $vrid]
    if {[info exists Data(Pri)]} {
        set pri $Data(Pri)
    }
    append segment1 [format "%02x" $pri]
    if {[info exists Data(Count)]} {
        set count $Data(Count)        
    }
    append segment1 [format "%02x" $count]
    if {[info exists Data(AdvInt)]} {
        set advint $Data(AdvInt)
    }
    append segment1 "0"
    append segment1 [format "%03x" $advint]
    if {[info exists Data(Ipv6Addr)]} {
        for { set Addrnum 0 } { $Addrnum < [llength $Data(Ipv6Addr)]} {incr Addrnum} {
            append segment2 [join [FormatHexIpv6 [lindex $Data(Ipv6Addr) $Addrnum]] ""]
        }
    } else {
        append segment2 [ChangeIpv6ToStr $ipv6addr]
    }
    append Ipv6PseudoHeader  [join [FormatHexIpv6 $SrcIpv6] ""]
    append Ipv6PseudoHeader  [join [FormatHexIpv6 $DstIpv6] ""]
    set vrrplength  [expr ([string length $segment1] + [string length $segment2] + 4 )/2 ]
    append Ipv6PseudoHeader [format "%04x" $vrrplength]
    append Ipv6PseudoHeader "0070"
    set checksum [CalcCheckSum "${Ipv6PseudoHeader}${segment1}0000${segment2}"]
    set res "${segment1}${checksum}${segment2}"
    return $res
}

#added by gengtao 2010.11.11
proc  FormatIpv4VrrpSegment {Ipv4VrrpInfo } {
    set segment1 ""
    set segment2 ""
    set version 2
    set type 1
    set vrid 10
    set pri 100
    set count 1
    set advint 100
    set checksum 0
    array set Data $Ipv4VrrpInfo
    if {[info exists Data(Version)]} {
        set version $Data(Version)
    }
    append segment1 [format "%0x" $version]
    if {[info exists Data(Type)]} {
        set type $Data(Type)
    }
    append segment1 [format "%0x" $type]
    if {[info exists Data(Vrid)]} {
        set vrid $Data(Vrid)
    }
    append segment1 [format "%02x" $vrid]
    if {[info exists Data(Priority)]} {
        set pri $Data(Priority)
    }
    append segment1 [format "%02x" $pri]
    if {[info exists Data(Count)]} {
        set count $Data(Count)        
    }
    append segment1 [format "%02x" $count]
    if {[info exists Data(AdvInt)]} {
        set advint $Data(AdvInt)
    }
    append segment1 "0"
    append segment1 [format "%03x" $advint]
    if {[info exists Data(Ipv4Addr)]} {
   	 set ipv4add $Data(Ipv4Addr)
   	 set ipv4add [split $ipv4add .]
   	 set ip1 [lindex $ipv4add 0]
   	 append segment2 [format "%02x" $ip1]
   	 set ip2 [lindex $ipv4add 1]
   	 append segment2 [format "%02x" $ip2]
   	 set ip3 [lindex $ipv4add 2]
   	 append segment2 [format "%02x" $ip3]
   	 set ip4 [lindex $ipv4add 3]
   	 append segment2 [format "%02x" $ip4]
    }  
    set checksum [CalcCheckSum "${segment1}0000${segment2}"]
    set res "${segment1}${checksum}${segment2}"
    return $res
}

proc FormatIcmpv6Segment { MldVersion Type MldGroupAddress MldSourceIpAddress MldGroupRecord } {
	set segment ""
	if { $MldVersion == 1 } {
		append segment [FormatHexIpv6 $MldGroupAddress]
	}
	if { $MldVersion == 2 } {
		if { $Type == "query" } {
			append segment [FormatHexIpv6 $MldGroupAddress]
			append segment " 02 7D "   ;#resv = 0000, s = 0, qrv = 010(rebus), qqic = 01111101(query-interval),将来可以根据需要修改
			set SourceRecord [split $MldSourceIpAddress " "]
			append segment [FormatHex [format %04x [llength $SourceRecord]]]
			for {set i 0} {$i < [llength $SourceRecord]} {incr i} {
				append segment " [FormatHexIpv6 [lindex $SourceRecord $i]]"
			}
		}
		if { $Type == "report" } {
			for {set i 0} {$i < [llength $MldGroupRecord]} {incr i} {
				set GroupRecord [lindex $MldGroupRecord $i]
				set SourceRecord [split [lindex $GroupRecord 2] " "]
				switch [lindex $GroupRecord 1] {
					include {append segment "01"}
					exclude {append segment "02"}
					toinclude {append segment "03"}
					toexclude {append segment "04"}
					allow {append segment "05"}
					block {append segment "06"}
				}
				append segment " 00"
				append segment " [FormatHex [format %04x [llength $SourceRecord]]]"
				append segment " [FormatHexIpv6 [lindex $GroupRecord 0]]"
				for {set j 0} {$j < [llength $SourceRecord]} {incr j} {
					if { $j == [expr [llength $SourceRecord] - 1] } {
						append segment " [FormatHexIpv6 [lindex $SourceRecord $j]] "
					} else {
						append segment " [FormatHexIpv6 [lindex $SourceRecord $j]]"
					}
				}
			}
			set segment [string trimright $segment]
		}
	}
	return $segment
}

proc FormatLoopbackSegment { LoopbackDetectionInfo } {
	set VlanId [lindex $LoopbackDetectionInfo 0]
	set PortName [lindex $LoopbackDetectionInfo 1]
	#if {[llength $LoopbackDetectionInfo] == 3} {
	#	set Type [lindex $LoopbackDetectionInfo 2]
	#} else {
	#	set Type other
	#}
	#set segment "00 00 00 00 00 00 00 40 "
	set segment "00 00 00 00 00 00 "
	if {[llength $LoopbackDetectionInfo] >= 4} {
		append segment "[FormatHex [format %04x [lindex $LoopbackDetectionInfo 3]]] "
	} else {
		append segment "00 40 "
	}
	#if { $Type == "other" } {
	#	append segment "[format %02x [GetSlotnum $PortName]] "
	#} else {
	#	append segment "[format %02x [expr [GetSlotnum $PortName] + 2]] "
	#}
	if {[regexp -nocase "Ethernet\(\[0-9\]+\)/\(\[0-9\]+\)/\(\[0-9\]+\)" $PortName match chassis card port] == 1} {
		append segment "01 "
		append segment "[FormatHex [format %06x $port]] "
	} else {
		append segment "[format %02x [GetSlotnum $PortName]] "
		append segment "[FormatHex [format %06x [GetPortnum $PortName]]] "
	}
	append segment "[FormatHex [format %08x $VlanId]] "
	append segment "00 00 "
	append segment "00 00 00 00 00 00 "
	append segment "00 00 00 00 00 00 "
	append segment "00 00 00 00 00 00 "
	append segment "00 00 00 00 00 00 "
	append segment "00 00 00 00 00 00"
	return $segment
}
#Mrpp报文:
#1、mrpp hello报文：可以修改目的mac、control-vlan、mrpp-type
#2、linkdown报文：可以修改目的mac、control-vlan
#3、ring-up-flush-fdb报文：可以修改目的mac、control-vlan
#4、ring-down-flush-fdb：可以修改目的mac、control-vlan
#SetIxiaStream Host $host Card $Card1 Port $Port1 StreamRateMode Fps StreamRate 1 \
#              SouMac $cpumac DesMac 00-03-0f-00-00-06 EthernetType mrpp \
#              MrppPacketInfo {health 100 $cpumac 1 3 idle}
#SetIxiaStream Host $host Card $Card1 Port $Port1 StreamRateMode Fps StreamRate 1 \
#              SouMac $cpumac DesMac 00-03-0f-00-00-06 EthernetType mrpp \
#              VlanTagFlag 1 VlanId 3 UserPriority 5 \
#              MrppPacketInfo {health 100 $cpumac 1 3 idle}
#MrppPacketInfo : {MrppType CtrlVlanId SystemMacAddr HelloTimer FailTimer State}
#mrpptype : health/ring-up-flush-fdb/ring-down-flush-fdb/link-down
#state : idle/complete/failed/link-up/link-down/pre-forwarding
proc FormatMrppSegment { MrppPacketInfo } {
	#set VlanId [lindex $MrppPacketInfo 0]
	set MrppType [lindex $MrppPacketInfo 0]
	switch -exact $MrppType {
		health {set MrppType 1}
		ring-up-flush-fdb {set MrppType 2}
		ring-down-flush-fdb {set MrppType 3}
		link-down {set MrppType 4}
	}
	set CtrlVlanId [lindex $MrppPacketInfo 1]
	regsub -all {\-} [lindex $MrppPacketInfo 2] " " SystemMacAddr
	set HelloTimer [lindex $MrppPacketInfo 3]
	set FailTimer [lindex $MrppPacketInfo 4]
	set State [lindex $MrppPacketInfo 5]
	switch -exact $State {
		idle {set State 0}
		complete {set State 1}
		failed {set State 2}
		link-up {set State 3}
		link-down {set State 4}
		pre-forwarding {set State 5}
	}
	#set segment "81 00 "
	#append segment "[FormatHex [format %04x $VlanId]] "
	append segment "00 48 AA AA 03 00 E0 2B 00 BB 99 0B 00 40 01 "
	append segment "[format %02x $MrppType] "
	append segment "[FormatHex [format %04x $CtrlVlanId]] "
	append segment "00 00 00 00 "
	append segment "$SystemMacAddr "
	append segment "[FormatHex [format %04x $HelloTimer]] "
	append segment "[FormatHex [format %04x $FailTimer]] "
	append segment "[format %02x $State] "
	append segment "00 D2 9A 00 00 "
	append segment "00 00 00 00 00 00 "
	append segment "00 00 00 00 00 00 "
	append segment "00 00 00 00 00 00 "
	append segment "00 00 00 00 00 00 "
	append segment "00 00 00 00 00 00 "
	append segment "00 00 00 00 00 00"
	return $segment
}

#SetIxiaStream Host $host Card $Card1 Port $Port1 StreamRateMode Fps StreamRate 1 \
#              SouMac $cpumac DesMac 01-80-c2-00-00-00 EthernetType stp \
#              StpPacketInfo [list BpduType 00 Flag 00 RootBridgePriority 8000 RootBridgeMac $cpumac ExtRootPathCost 00000000 \
#                             DesignedBridgePriority 8000 DesignedBridgeMac $cpumac PortId 8004 MsgAge 0000 MaxAge 1400 HelloTime 0200 \
#                             ForwardDelay 0F00]
#SetIxiaStream Host $host Card $Card1 Port $Port1 StreamRateMode Fps StreamRate 1 \
#              SouMac $cpumac DesMac 01-80-c2-00-00-00 EthernetType stp \
#              StpPacketInfo [list BpduType 00 RootBridgePriority 8000 RootBridgeMac $cpumac ExtRootPathCost 00000000 \
#                             DesignedBridgePriority 8000 DesignedBridgeMac $cpumac PortId 8004]
proc FormatStpSegment { StpPacketInfo } {
	set segment "00 26 42 42 03 00 00 00 "   ;#length:00 26     dsap:42   ssap:42  control field:03
                                             ;#protocolid:00 00    protocolversion:00
	set position [lsearch $StpPacketInfo "BpduType"]   ;#bpdutype:00/80
	if { $position != -1 } {
		append segment "[lindex $StpPacketInfo [expr $position + 1]] "
	} else {
		append segment "00 "   
	}
	set position [lsearch $StpPacketInfo "Flag"]   ;#flag:00/**
	if { $position != -1 } {
		append segment "[lindex $StpPacketInfo [expr $position + 1]] "
	} else {
		append segment "00 "   
	}
	set position [lsearch $StpPacketInfo "RootBridgePriority"]
	if { $position != -1 } {
		set RootBridgePriority [lindex $StpPacketInfo [expr $position + 1]]
		append segment "[string range $RootBridgePriority 0 1] [string range $RootBridgePriority 2 3] "
	} else {
		append segment "80 00 "   
	}
	set position [lsearch $StpPacketInfo "RootBridgeMac"]
	if { $position != -1 } {
		set RootBridgeMac [lindex $StpPacketInfo [expr $position + 1]]
		append segment "[TransformMac $RootBridgeMac "-" " "] "
	} else {
		append segment "00 03 0F 00 FA 87 "   
	}
	set position [lsearch $StpPacketInfo "ExtRootPathCost"]
	if { $position != -1 } {
		set ExtRootPathCost [lindex $StpPacketInfo [expr $position + 1]]
		append segment "[string range $ExtRootPathCost 0 1] [string range $ExtRootPathCost 2 3] [string range $ExtRootPathCost 4 5] [string range $ExtRootPathCost 6 7] "
	} else {
		append segment "00 00 00 00 "   
	}
	set position [lsearch $StpPacketInfo "DesignedBridgePriority"]
	if { $position != -1 } {
		set DesignedBridgePriority [lindex $StpPacketInfo [expr $position + 1]]
		append segment "[string range $DesignedBridgePriority 0 1] [string range $DesignedBridgePriority 2 3] "
	} else {
		append segment "80 00 "   
	}
	set position [lsearch $StpPacketInfo "DesignedBridgeMac"]
	if { $position != -1 } {
		set DesignedBridgeMac [lindex $StpPacketInfo [expr $position + 1]]
		append segment "[TransformMac $DesignedBridgeMac "-" " "] "
	} else {
		append segment "00 03 0F 00 FA 87 "   
	}
	set position [lsearch $StpPacketInfo "PortId"]
	if { $position != -1 } {
		set PortId [lindex $StpPacketInfo [expr $position + 1]]
		append segment "[string range $PortId 0 1] [string range $PortId 2 3] "
	} else {
		append segment "80 04 "   
	}
	set position [lsearch $StpPacketInfo "MsgAge"]
	if { $position != -1 } {
		set MsgAge [lindex $StpPacketInfo [expr $position + 1]]
		append segment "[string range $MsgAge 0 1] [string range $MsgAge 2 3] "
	} else {
		append segment "00 00 "   
	}
	set position [lsearch $StpPacketInfo "MaxAge"]
	if { $position != -1 } {
		set MaxAge [lindex $StpPacketInfo [expr $position + 1]]
		append segment "[string range $MaxAge 0 1] [string range $MaxAge 2 3] "
	} else {
		append segment "14 00 "   
	}
	set position [lsearch $StpPacketInfo "HelloTime"]
	if { $position != -1 } {
		set HelloTime [lindex $StpPacketInfo [expr $position + 1]]
		append segment "[string range $HelloTime 0 1] [string range $HelloTime 2 3] "
	} else {
		append segment "02 00 "   
	}
	set position [lsearch $StpPacketInfo "ForwardDelay"]
	if { $position != -1 } {
		set ForwardDelay [lindex $StpPacketInfo [expr $position + 1]]
		append segment "[string range $ForwardDelay 0 1] [string range $ForwardDelay 2 3] "
	} else {
		append segment "0F 00 "   
	}
	append segment "00 00 00 00 00 00 00 00" 
	return $segment
}

#SetIxiaStream Host $host Card $Card1 Port $Port1 StreamRateMode Fps StreamRate 1 \
#              SouMac $cpumac DesMac 01-80-c2-00-00-00 EthernetType rstp \
#              RstpPacketInfo [list BpduType 02 Flag 7C RootBridgePriority 8000 RootBridgeMac $cpumac ExtRootPathCost 00000000 \
#                             DesignedBridgePriority 8000 DesignedBridgeMac $cpumac PortId 8004 MsgAge 0000 MaxAge 1400 HelloTime 0200 \
#                             ForwardDelay 0F00]
#SetIxiaStream Host $host Card $Card1 Port $Port1 StreamRateMode Fps StreamRate 1 \
#              SouMac $cpumac DesMac 01-80-c2-00-00-00 EthernetType rstp \
#              RstpPacketInfo [list BpduType 02 RootBridgePriority 8000 RootBridgeMac $cpumac ExtRootPathCost 00000000 \
#                             DesignedBridgePriority 8000 DesignedBridgeMac $cpumac PortId 8004]
proc FormatRstpSegment { StpPacketInfo } {
	set segment "00 27 42 42 03 00 00 02 "   ;#length:00 27     dsap:42   ssap:42  control field:03   
                                             ;#protocolid:00 00    protocolversion:02
                                             ;#由于目前产品未实现rstp，所以length写的是0027，实际应该是0026
	set position [lsearch $StpPacketInfo "BpduType"]   ;#bpdutype:00/80
	if { $position != -1 } {
		append segment "[lindex $StpPacketInfo [expr $position + 1]] "
	} else {
		append segment "02 "   
	}
	set position [lsearch $StpPacketInfo "Flag"]   ;#flag:00/**
	if { $position != -1 } {
		append segment "[lindex $StpPacketInfo [expr $position + 1]] "
	} else {
		append segment "7C "   
	}
	set position [lsearch $StpPacketInfo "RootBridgePriority"]
	if { $position != -1 } {
		set RootBridgePriority [lindex $StpPacketInfo [expr $position + 1]]
		append segment "[string range $RootBridgePriority 0 1] [string range $RootBridgePriority 2 3] "
	} else {
		append segment "80 00 "   
	}
	set position [lsearch $StpPacketInfo "RootBridgeMac"]
	if { $position != -1 } {
		set RootBridgeMac [lindex $StpPacketInfo [expr $position + 1]]
		append segment "[TransformMac $RootBridgeMac "-" " "] "
	} else {
		append segment "00 03 0F 00 FA 87 "   
	}
	set position [lsearch $StpPacketInfo "ExtRootPathCost"]
	if { $position != -1 } {
		set ExtRootPathCost [lindex $StpPacketInfo [expr $position + 1]]
		append segment "[string range $ExtRootPathCost 0 1] [string range $ExtRootPathCost 2 3] [string range $ExtRootPathCost 4 5] [string range $ExtRootPathCost 6 7] "
	} else {
		append segment "00 00 00 00 "   
	}
	set position [lsearch $StpPacketInfo "DesignedBridgePriority"]
	if { $position != -1 } {
		set DesignedBridgePriority [lindex $StpPacketInfo [expr $position + 1]]
		append segment "[string range $DesignedBridgePriority 0 1] [string range $DesignedBridgePriority 2 3] "
	} else {
		append segment "80 00 "   
	}
	set position [lsearch $StpPacketInfo "DesignedBridgeMac"]
	if { $position != -1 } {
		set DesignedBridgeMac [lindex $StpPacketInfo [expr $position + 1]]
		append segment "[TransformMac $DesignedBridgeMac "-" " "] "
	} else {
		append segment "00 03 0F 00 FA 87 "   
	}
	set position [lsearch $StpPacketInfo "PortId"]
	if { $position != -1 } {
		set PortId [lindex $StpPacketInfo [expr $position + 1]]
		append segment "[string range $PortId 0 1] [string range $PortId 2 3] "
	} else {
		append segment "80 04 "   
	}
	set position [lsearch $StpPacketInfo "MsgAge"]
	if { $position != -1 } {
		set MsgAge [lindex $StpPacketInfo [expr $position + 1]]
		append segment "[string range $MsgAge 0 1] [string range $MsgAge 2 3] "
	} else {
		append segment "00 00 "   
	}
	set position [lsearch $StpPacketInfo "MaxAge"]
	if { $position != -1 } {
		set MaxAge [lindex $StpPacketInfo [expr $position + 1]]
		append segment "[string range $MaxAge 0 1] [string range $MaxAge 2 3] "
	} else {
		append segment "14 00 "   
	}
	set position [lsearch $StpPacketInfo "HelloTime"]
	if { $position != -1 } {
		set HelloTime [lindex $StpPacketInfo [expr $position + 1]]
		append segment "[string range $HelloTime 0 1] [string range $HelloTime 2 3] "
	} else {
		append segment "02 00 "   
	}
	set position [lsearch $StpPacketInfo "ForwardDelay"]
	if { $position != -1 } {
		set ForwardDelay [lindex $StpPacketInfo [expr $position + 1]]
		append segment "[string range $ForwardDelay 0 1] [string range $ForwardDelay 2 3] "
	} else {
		append segment "0F 00 "   
	}
	append segment "00 00 00 00 00 00 00 00" 
	return $segment
}

#SetIxiaStream Host $host Card $Card1 Port $Port1 StreamRateMode Fps StreamRate 1 \
#              SouMac $cpumac DesMac 01-00-0C-CC-CC-CC EthernetType uldp \
#              ULDPPacketInfo {ULDPType hello ULDPID 1 Version 1 Type 1 Flag 0 AuthMode nopassword HelloInterval 10 DeviceMac $cpumac PortID 1}
#SetIxiaStream Host $host Card $Card1 Port $Port1 StreamRateMode Fps StreamRate 1 \
#              SouMac $cpumac DesMac 01-00-0C-CC-CC-CC EthernetType uldp \
#              ULDPPacketInfo {ULDPType rsy DeviceMac $cpumac PortID 1}
#SetIxiaStream Host $host Card $Card1 Port $Port1 StreamRateMode Fps StreamRate 1 \
#              SouMac $cpumac DesMac 01-00-0C-CC-CC-CC EthernetType uldp \
#              ULDPPacketInfo {ULDPType flush DeviceMac $cpumac PortID 1}
#SetIxiaStream Host $host Card $Card1 Port $Port1 StreamRateMode Fps StreamRate 1 \
#              SouMac $cpumac DesMac 01-00-0C-CC-CC-CC EthernetType uldp \
#              ULDPPacketInfo {ULDPType unidirection DeviceMac $cpumac PortID 1}
#SetIxiaStream Host $host Card $Card1 Port $Port1 StreamRateMode Fps StreamRate 1 \
#              SouMac $cpumac DesMac 01-00-0C-CC-CC-CC EthernetType uldp \
#              ULDPPacketInfo {ULDPType echo DeviceMac $cpumac PortID 1 NeighborInfo [list $cpumac 1]}

proc FormatULDPSegment { ULDPPacketInfo } {
	set position [lsearch $ULDPPacketInfo "ULDPType"]
	if { $position != -1 } {
		set ULDPType [lindex $ULDPPacketInfo [expr $position + 1]]
	} else {
		set ULDPType hello  
	}
	#Length
	set position [lsearch $ULDPPacketInfo "Length"]
	if { $position != -1 } {
		set length [lindex $ULDPPacketInfo [expr $position + 1]]
		set segment "[format %02x [expr $length / 256]] [format %02x [expr $length % 256]] "
	} else {
		switch -exact $ULDPType {
			hello -
			rsy   -
			flush -
			probe -
			unidirection {set segment "00 22 "}
			echo {set segment "00 2A "}
			default {set segment "00 22 "}
		}
	}
	
	#puts $segment
	set position [lsearch $ULDPPacketInfo "ULDPID"]
	if { $position != -1 } {
		set uldpid [lindex $ULDPPacketInfo [expr $position + 1]]
		append segment "[format %02x [expr $uldpid / 256]] [format %02x [expr $uldpid % 256]] "
	} else {
		append segment "00 01 "
	}
	set position [lsearch $ULDPPacketInfo "Version"]
	if { $position != -1 } {
		append segment "[format %02x [lindex $ULDPPacketInfo [expr $position + 1]]] "
	} else {
		append segment "01 "
	}
	set position [lsearch $ULDPPacketInfo "Type"]
	if { $position != -1 } {
		append segment "[format %02x [lindex $ULDPPacketInfo [expr $position + 1]]] "
	} else {
		switch -exact $ULDPType {
			hello -
			rsy   -
			flush {append segment "01 "}
			probe {append segment "02 "}
			unidirection {append segment "04 "}
			echo {append segment "03 "}
			default {append segment "01 "}
		}
	}
	set position [lsearch $ULDPPacketInfo "Flag"]
	if { $position != -1 } {
		append segment "[format %02x [lindex $ULDPPacketInfo [expr $position + 1]]] "
	} else {
		switch -exact $ULDPType {
			hello {append segment "00 "}
			rsy   {append segment "80 "}
			flush {append segment "40 "}
			probe -
			unidirection -
			echo -
			default {append segment "00 "}
		}
	}
	set position [lsearch $ULDPPacketInfo "AuthMode"]
	set authmode nopassword
	if { $position != -1 } {
		set authmode [lindex $ULDPPacketInfo [expr $position + 1]]
		switch -exact $authmode {
			nopassword {append segment "00 "}
			password {append segment "01 "}
			md5 {append segment "02 "}
			default {append segment "[format %02x $authmode] "}
		}
	} else {
		switch -exact $ULDPType {
			hello -
			rsy   -
			flush -
			probe -
			unidirection -
			echo {append segment "00 "}
			default {append segment "00 "}
		}
	}
	set position [lsearch $ULDPPacketInfo "Password"]
	if { $position != -1 } {
		set password [lindex $ULDPPacketInfo [expr $position + 1]]
		switch -exact $authmode {
			nopassword {append segment "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 "}
			password {
				set count [regsub -all " " $password {} ignore]
				if { $count == 31 } {
					append segment "$password "
				} else {
					append segment "[FormattoASCII $password 32] "}
				}
			md5 {append segment "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 "}
			default {append segment "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 "}
		}
	} else {
		switch -exact $ULDPType {
			hello -
			rsy   -
			flush -
			probe -
			unidirection -
			echo {append segment "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 "}
			default {append segment "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 "}
		}
	}
	set position [lsearch $ULDPPacketInfo "HelloInterval"]
	if { $position != -1 } {
		set hellointerval [lindex $ULDPPacketInfo [expr $position + 1]]
		append segment "[format %02x [expr $hellointerval / 256]] [format %02x [expr $hellointerval % 256]] "
	} else {
		append segment "00 0A "
	}
	append segment "00 00 "
	set position [lsearch $ULDPPacketInfo "DeviceMac"]
	if { $position != -1 } {
		regsub -all {\-} [lindex $ULDPPacketInfo [expr $position + 1]] " " devicemac
		append segment "$devicemac "
	} else {
		append segment "00 03 0F 00 00 01 "
	}
	set position [lsearch $ULDPPacketInfo "PortID"]
	if { $position != -1 } {
		set portid [lindex $ULDPPacketInfo [expr $position + 1]]
		append segment "[format %02x [expr $portid / 256]] [format %02x [expr $portid % 256]]"
	} else {
		append segment "00 01"
	}
	if { $ULDPType == "echo" } {
		append segment " "
		set position [lsearch $ULDPPacketInfo "NeighborInfo"]
		if { $position != -1 } {
			set neighborinfo [lindex $ULDPPacketInfo [expr $position + 1]]
			regsub -all {\-} [lindex $neighborinfo 0] " " mac
			set portid [lindex $neighborinfo 1]
			append segment "$mac "
			append segment "[format %02x [expr $portid / 256]] [format %02x [expr $portid % 256]]"
		} else {
			append segment "00 03 0F 00 00 01 00 01"
		}
	}
	#puts $segment
	return $segment
}

#SetIxiaStream Host $host Card $Card1 Port $Port1 StreamRateMode Fps StreamRate 1 \
#              SouMac $cpumac DesMac 01-80-c2-00-00-0E EthernetType lldp \
#              LLDPPacketInfo {LLDPType normal ChassisID {SubType 4 ChassisID 00-03-0f-00-00-01} \
#                                              PortID {SubType 3 PortID 00-03-0f-00-00-01} \
#                                              TTL {TTL 10} \
#                                              PortDescription {PortDescription abc} \
#                                              SystemName {SystemName abc} \
#                                              SystemDescription {SystemDescription abc} \
#                                              SystemCapabilities {SystemCapabilities 2 EnableCapabilities 1} \
#                                              ManagementAddress {ManagementAddress 00-03-0f-00-00-01 ManagementAddressSubType 1 \
#                                                                 InterfaceNumberingSubType 1 InterfaceNumber 1 OID abc}}
#SetIxiaStream Host $host Card $Card1 Port $Port1 StreamRateMode Fps StreamRate 1 \
#              SouMac $cpumac DesMac 01-80-c2-00-00-0E EthernetType lldp \
#              LLDPPacketInfo {LLDPType shutdown ChassisID {SubType 4 ChassisID 00-03-0f-00-00-01} \
#                                                PortID {SubType 3 ChassisID 00-03-0f-00-00-01} \
#                                                TTL {TTL 10}}
proc FormatLLDPSegment { LLDPPacketInfo } {
	set segment "88 CC "
	set position [lsearch $LLDPPacketInfo "LLDPType"]
	if { $position != -1 } {
		set LLDPType [lindex $LLDPPacketInfo [expr $position + 1]]
	} else {
		set LLDPType normal  
	}
	if { $LLDPType == "normal" } {
		#ChassisID TLV
		set position [lsearch $LLDPPacketInfo "ChassisID"]
		if { $position != -1 } {
			set ChassisID [lindex $LLDPPacketInfo [expr $position + 1]]
			set position [lsearch $ChassisID "Type"]
			if { $position != -1 } {
				set type [lindex $ChassisID [expr $position + 1]]
			} else {
				set type 1
			}
			set position [lsearch $ChassisID "SubType"]
			if { $position != -1 } {
				set subtype [lindex $ChassisID [expr $position + 1]]
			} else {
#				ID   	subtype ID 		 basis Reference
#				0 		Reserved	 -
#				1       Chassis component	 EntPhysicalAlias when entPhysClass has a value ofchassis(3)' (IETF RFC 2737)
#				2		Interface alias 		 IfAlias (IETF RFC 2863)
#				3       Port component 	 EntPhysicalAlias when entPhysicalClass has a value'port(10)' or 'backplane(4)' (IETF RFC 2737)
#				4 		MAC address 		 MAC address (IEEE Std 802-2001)(为了保证系统在网络中的唯一性，我们采用MAC地址来当chassis ID)
#				5 		Network address 	 networkAddress *
#				6		Interface name 	 	 ifName (IETF RFC 2863)
#				7 		Locally assigned		 local?
#				8-255 	Reserved 			 -
				set subtype 4
			}
			set position [lsearch $ChassisID "ChassisID"]
			if { $position != -1 } {
				if { $subtype == 4 } {
					regsub -all {\-} [lindex $ChassisID [expr $position + 1]] " " chassisid
				} else {
					set chassisid [lindex $ChassisID [expr $position + 1]]
				}
			} else {
				set chassisid "00 03 0f 01 01 01"
			}
			set position [lsearch $ChassisID "Length"]
			if { $position != -1 } {
				set length [lindex $ChassisID [expr $position + 1]]
			} else {
				set length [expr ([string length $chassisid] + 1) / 3 + 1]
			}
			append segment "[format %02x [expr ($type << 1) + ($length >> 8)]] [format %02x [expr ($length << 1) / 2]] [format %02x $subtype] $chassisid "
		} else {
			append segment "02 07 04 00 03 0f 01 01 01 "  
		}
		#modified by zhaohj 2011-3-29
		#PortID TLV
		set position [lsearch $LLDPPacketInfo "PortID"]
		if { $position != -1 } {
			set PortID [lindex $LLDPPacketInfo [expr $position + 1]]
			set position [lsearch $PortID "Type"]
			if { $position != -1 } {
				set type [lindex $PortID [expr $position + 1]]
			} else {
				set type 2
			}
			set position [lsearch $PortID "SubType"]
			if { $position != -1 } {
				set subtype [lindex $PortID [expr $position + 1]]
			} else {
#				ID 		subtype ID		 basis References
#				0		Reserved			 -
#				1 		Interface alias		 ifAlias (IETF RFC 2863)
#				2 		Port component 		 entPhysicalAlias when entPhysicalClass has a value	'port(10)' or 'backplane(4)' (IETF RFC 2737)
#				3 		MAC address 		 MAC address (IEEE Std 802-2001)
#				4 		Network address 	 networkAddress *
#				5 		Interface name		 ifName (IETF RFC 2863)
#				6 		Agent circuit ID 	 agent circuit ID (IETF RFC 3046)
#				7 		Locally assigned 	 local ?
#				8-255	Reserved 			-
				set subtype 3
			}
			set position [lsearch $PortID "PortID"]
			if { $position != -1 } {
				if { $subtype == 3 } {
					regsub -all {\-} [lindex $PortID [expr $position + 1]] " " portid
				} elseif { $subtype == 7 } {
					set fullportid [lindex $PortID [expr $position + 1]]
					set p1 [string last "/" $fullportid]
					set portindex [string range $fullportid [expr $p1 + 1] [expr $p1 + 1]]
					set p2 [string first "/" $fullportid]
					set slotnum [string range $fullportid [expr $p2 - 1] [expr $p2 - 1]]
					if {$slotnum == 0} {
						set slotnum 1
					}
					set portid [FormattoASCII [expr {($slotnum - 1) * 64 + $portindex}]]
				} else {
					set portid [lindex $PortID [expr $position + 1]]
				}
			} else {
				set portid "00 03 0f 01 01 01"
			}
			set position [lsearch $PortID "Length"]
			if { $position != -1 } {
				set length [lindex $PortID [expr $position + 1]]
			} else {
				set length [expr ([string length $portid] + 1) / 3 + 1]
			}
			append segment "[format %02x [expr ($type << 1) + ($length >> 8)]] [format %02x [expr ($length << 1) / 2]] [format %02x $subtype] $portid "
		} else {
			append segment "04 07 03 00 03 0f 01 01 01 "  
		}
		#modified by zhaohj end
		#TTL TLV
		set position [lsearch $LLDPPacketInfo "TTL"]
		if { $position != -1 } {
			set TTL [lindex $LLDPPacketInfo [expr $position + 1]]
			#set ttl [lindex $LLDPPacketInfo [expr $position + 1]]
			set position [lsearch $TTL "TTL"]
			if { $position != -1 } {
				set ttl [lindex $TTL [expr $position + 1]]
			} else {
				set ttl 3
			}
			set position [lsearch $TTL "Type"]
			if { $position != -1 } {
				set type [lindex $TTL [expr $position + 1]]
			} else {
				set type 3
			}
			set position [lsearch $TTL "Length"]
			if { $position != -1 } {
				set length [lindex $TTL [expr $position + 1]]
			} else {
				set length 2
			}
			append segment "[format %02x [expr ($type << 1) + ($length >> 8)]] [format %02x [expr ($length << 1) / 2]] [format %02x [expr $ttl >> 8]] [format %02x [expr ($ttl << 8) >> 8]] "
		} else {
			append segment "06 02 00 0a "  
		}
		#Port Description TLV
		set position [lsearch $LLDPPacketInfo "PortDescription"]
		if { $position != -1 } {
			set PortDescription [lindex $LLDPPacketInfo [expr $position + 1]]
			#set portdescription [lindex $LLDPPacketInfo [expr $position + 1]]
			set position [lsearch $PortDescription "PortDescription"]
			if { $position != -1 } {
				set portdescription [FormattoASCII [lindex $PortDescription [expr $position + 1]]]
			} else {
				set portdescription [FormattoASCII Ethernet1/1]
			}
			set position [lsearch $PortDescription "Type"]
			if { $position != -1 } {
				set type [lindex $PortDescription [expr $position + 1]]
			} else {
				set type 4
			}
			set position [lsearch $PortDescription "Length"]
			if { $position != -1 } {
				set length [lindex $PortDescription [expr $position + 1]]
			} else {
				set length [expr ([string length $portdescription] + 1) / 3]
			}
			append segment "[format %02x [expr ($type << 1) + ($length >> 8)]] [format %02x [expr ($length << 1) / 2]] $portdescription "
		}
		#System Name TLV
		set position [lsearch $LLDPPacketInfo "SystemName"]
		if { $position != -1 } {
			set SystemName [lindex $LLDPPacketInfo [expr $position + 1]]
			#set systemname [lindex $LLDPPacketInfo [expr $position + 1]]
			set position [lsearch $SystemName "SystemName"]
			if { $position != -1 } {
				set systemname [FormattoASCII [lindex $SystemName [expr $position + 1]]]
			} else {
				set systemname [FormattoASCII abc]
			}
			set position [lsearch $SystemName "Type"]
			if { $position != -1 } {
				set type [lindex $SystemName [expr $position + 1]]
			} else {
				set type 5
			}
			set position [lsearch $SystemName "Length"]
			if { $position != -1 } {
				set length [lindex $SystemName [expr $position + 1]]
			} else {
				set length [expr ([string length $systemname] + 1) / 3]
			}
			append segment "[format %02x [expr ($type << 1) + ($length >> 8)]] [format %02x [expr ($length << 1) / 2]] $systemname "
		}
		#System Description TLV
		set position [lsearch $LLDPPacketInfo "SystemDescription"]
		if { $position != -1 } {
			set SystemDescription [lindex $LLDPPacketInfo [expr $position + 1]]
			#set systemdescription [lindex $LLDPPacketInfo [expr $position + 1]]
			set position [lsearch $SystemDescription "SystemDescription"]
			if { $position != -1 } {
				set systemdescription [FormattoASCII [lindex $SystemDescription [expr $position + 1]]]
			} else {
				set systemdescription [FormattoASCII abc]
			}
			set position [lsearch $SystemDescription "Type"]
			if { $position != -1 } {
				set type [lindex $SystemDescription [expr $position + 1]]
			} else {
				set type 6
			}
			set position [lsearch $SystemDescription "Length"]
			if { $position != -1 } {
				set length [lindex $SystemDescription [expr $position + 1]]
			} else {
				set length [expr ([string length $systemdescription] + 1) / 3]
			}
			append segment "[format %02x [expr ($type << 1) + ($length >> 8)]] [format %02x [expr ($length << 1) / 2]] $systemdescription "
		}
		#System Capabilities TLV
		set position [lsearch $LLDPPacketInfo "SystemCapabilities"]
		if { $position != -1 } {
			set SystemCapabilities [lindex $LLDPPacketInfo [expr $position + 1]]
			set position [lsearch $SystemCapabilities "Type"]
			if { $position != -1 } {
				set type [lindex $SystemCapabilities [expr $position + 1]]
			} else {
				set type 7
			}
			set position [lsearch $SystemCapabilities "SystemCapabilities"]
			if { $position != -1 } {
				set systemcapabilities [lindex $SystemCapabilities [expr $position + 1]]
			} else {
				set systemcapabilities 2
			}
			set position [lsearch $SystemCapabilities "EnableCapabilities"]
			if { $position != -1 } {
				set enablecapabilities [lindex $SystemCapabilities [expr $position + 1]]
			} else {
				set enablecapabilities 1
			}
			set position [lsearch $SystemCapabilities "Length"]
			if { $position != -1 } {
				set length [lindex $SystemCapabilities [expr $position + 1]]
			} else {
				set length 4
			}
			append segment "[format %02x [expr ($type << 1) + ($length >> 8)]] [format %02x [expr ($length << 1) / 2]] "
			append segment "[format %02x [expr $systemcapabilities >> 8]] [format %02x [expr $systemcapabilities % 256]] "
			append segment "[format %02x [expr $enablecapabilities >> 8]] [format %02x [expr $enablecapabilities % 256]] "
		}
		#Management Address TLV
		set position [lsearch $LLDPPacketInfo "ManagementAddress"]
		if { $position != -1 } {
			set ManagementAddress [lindex $LLDPPacketInfo [expr $position + 1]]
			set position [lsearch $ManagementAddress "Type"]
			if { $position != -1 } {
				set type [lindex $ManagementAddress [expr $position + 1]]
			} else {
				set type 8
			}
			set position [lsearch $ManagementAddress "ManagementAddressSubType"]
			if { $position != -1 } {
				set managementaddresssubtype [lindex $ManagementAddress [expr $position + 1]]
			} else {
				set managementaddresssubtype 1
			}
			set position [lsearch $ManagementAddress "ManagementAddress"]
			if { $position != -1 } {
				set managementaddress [lindex $ManagementAddress [expr $position + 1]]
			} else {
				set managementaddress "00 03 0f 01 01 01"
			}
			set position [lsearch $ManagementAddress "ManagementAddressLength"]
			if { $position != -1 } {
				set managementaddresslength [lindex $ManagementAddress [expr $position + 1]]
			} else {
				set managementaddresslength [expr ([string length $managementaddress] + 1) / 3 + 1]
			}
			set position [lsearch $ManagementAddress "InterfaceNumberingSubType"]
			if { $position != -1 } {
				set interfacenumberingsubtype [lindex $ManagementAddress [expr $position + 1]]
			} else {
				set interfacenumberingsubtype 1
			}
			set position [lsearch $ManagementAddress "InterfaceNumber"]
			if { $position != -1 } {
				set interfacenumber [lindex $ManagementAddress [expr $position + 1]]
			} else {
				set interfacenumber "00 00 00 01"
			}
			set position [lsearch $ManagementAddress "OID"]
			if { $position != -1 } {
				set oid [lindex $ManagementAddress [expr $position + 1]]
			} else {
				set oid "00 00 00 01"
			}
			set position [lsearch $ManagementAddress "OIDLength"]
			if { $position != -1 } {
				set oidlength [lindex $ManagementAddress [expr $position + 1]]
			} else {
				set oidlength [expr ([string length $oid] + 1) / 3]
			}
			set position [lsearch $ManagementAddress "Length"]
			if { $position != -1 } {
				set length [lindex $ManagementAddress [expr $position + 1]]
			} else {
				set length [expr $managementaddresslength + 1 + 1 + 4 + $oidlength + 1]
			}
			append segment "[format %02x [expr ($type << 1) + ($length >> 8)]] [format %02x [expr ($length << 1) / 2]] "
			append segment "[format %02x $managementaddresslength] [format %02x $managementaddresssubtype] $managementaddress "
			append segment "[format %02x $interfacenumberingsubtype] $interfacenumber [format %02x $oidlength] $oid "
		}
		#End TLV
		set position [lsearch $LLDPPacketInfo "End"]
		if { $position != -1 } {
			append segment [lindex $LLDPPacketInfo [expr $position + 1]]
		} else {
			append segment "00 00"
		}
	}
	if { $LLDPType == "shutdown" } {
		#ChassisID TLV
		set position [lsearch $LLDPPacketInfo "ChassisID"]
		if { $position != -1 } {
			set ChassisID [lindex $LLDPPacketInfo [expr $position + 1]]
			set position [lsearch $ChassisID "Type"]
			if { $position != -1 } {
				set type [lindex $ChassisID [expr $position + 1]]
			} else {
				set type 1
			}
			set position [lsearch $ChassisID "SubType"]
			if { $position != -1 } {
				set subtype [lindex $ChassisID [expr $position + 1]]
			} else {
#				ID   	subtype ID 		 basis Reference
#				0 		Reserved	 -
#				1       Chassis component	 EntPhysicalAlias when entPhysClass has a value ofchassis(3)' (IETF RFC 2737)
#				2		Interface alias 		 IfAlias (IETF RFC 2863)
#				3       Port component 	 EntPhysicalAlias when entPhysicalClass has a value'port(10)' or 'backplane(4)' (IETF RFC 2737)
#				4 		MAC address 		 MAC address (IEEE Std 802-2001)(为了保证系统在网络中的唯一性，我们采用MAC地址来当chassis ID)
#				5 		Network address 	 networkAddress *
#				6		Interface name 	 	 ifName (IETF RFC 2863)
#				7 		Locally assigned		 local?
#				8-255 	Reserved 			 -
				set subtype 4
			}
			set position [lsearch $ChassisID "ChassisID"]
			if { $position != -1 } {
				if { $subtype == 4 } {
					regsub -all {\-} [lindex $ChassisID [expr $position + 1]] " " chassisid
				} else {
					set chassisid [lindex $ChassisID [expr $position + 1]]
				}
			} else {
				set chassisid "00 03 0f 01 01 01"
			}
			set position [lsearch $ChassisID "Length"]
			if { $position != -1 } {
				set length [lindex $ChassisID [expr $position + 1]]
			} else {
				set length [expr ([string length $chassisid] + 1) / 3 + 1]
			}
			append segment "[format %02x [expr ($type << 1) + ($length >> 8)]] [format %02x [expr ($length << 1) / 2]] [format %02x $subtype] $chassisid "
		} else {
			append segment "02 07 04 00 03 0f 01 01 01 "  
		}
		#PortID TLV
		set position [lsearch $LLDPPacketInfo "PortID"]
		if { $position != -1 } {
			set PortID [lindex $LLDPPacketInfo [expr $position + 1]]
			set position [lsearch $PortID "Type"]
			if { $position != -1 } {
				set type [lindex $PortID [expr $position + 1]]
			} else {
				set type 2
			}
			set position [lsearch $PortID "SubType"]
			if { $position != -1 } {
				set subtype [lindex $PortID [expr $position + 1]]
			} else {
#				ID 		subtype ID		 basis References
#				0		Reserved			 -
#				1 		Interface alias		 ifAlias (IETF RFC 2863)
#				2 		Port component 		 entPhysicalAlias when entPhysicalClass has a value	'port(10)' or 'backplane(4)' (IETF RFC 2737)
#				3 		MAC address 		 MAC address (IEEE Std 802-2001)
#				4 		Network address 	 networkAddress *
#				5 		Interface name		 ifName (IETF RFC 2863)
#				6 		Agent circuit ID 	 agent circuit ID (IETF RFC 3046)
#				7 		Locally assigned 	 local ?
#				8-255	Reserved 			-
				set subtype 3
			}
			set position [lsearch $PortID "PortID"]
			if { $position != -1 } {
				if { $subtype == 3 } {
					regsub -all {\-} [lindex $PortID [expr $position + 1]] " " portid
				} elseif { $subtype == 7 } {
					set fullportid [lindex $PortID [expr $position + 1]]
					set p1 [string last "/" $fullportid]
					set portindex [string range $fullportid [expr $p1 + 1] [expr $p1 + 1]]
					set p2 [string first "/" $fullportid]
					set slotnum [string range $fullportid [expr $p2 - 1] [expr $p2 - 1]]
					if {$slotnum == 0} {
						set slotnum 1
					}
					set portid [FormattoASCII [expr {($slotnum - 1) * 64 + $portindex}]]
				} else {
					set portid [lindex $PortID [expr $position + 1]]
				}
			} else {
				set portid "00 03 0f 01 01 01"
			}
			set position [lsearch $PortID "Length"]
			if { $position != -1 } {
				set length [lindex $PortID [expr $position + 1]]
			} else {
				set length [expr ([string length $portid] + 1) / 3 + 1]
			}
			append segment "[format %02x [expr ($type << 1) + ($length >> 8)]] [format %02x [expr ($length << 1) / 2]] [format %02x $subtype] $portid "
		} else {
			append segment "04 07 03 00 03 0f 01 01 01 "  
		}
		#TTL TLV
		set position [lsearch $LLDPPacketInfo "TTL"]
		if { $position != -1 } {
			#set ttl [lindex $LLDPPacketInfo [expr $position + 1]]
			set TTL [lindex $LLDPPacketInfo [expr $position + 1]]
			set position [lsearch $TTL "TTL"]
			if { $position != -1 } {
				set ttl [lindex $TTL [expr $position + 1]]
			} else {
				set ttl 0
			}
			set position [lsearch $TTL "Type"]
			if { $position != -1 } {
				set type [lindex $TTL [expr $position + 1]]
			} else {
				set type 3
			}
			set position [lsearch $TTL "Length"]
			if { $position != -1 } {
				set length [lindex $TTL [expr $position + 1]]
			} else {
				set length 2
			}
		} else {
			set type 3
			set length 2
			set ttl 0 
		}
		append segment "[format %02x [expr ($type << 1) + ($length >> 8)]] [format %02x [expr ($length << 1) / 2]] [format %02x [expr $ttl >> 8]] [format %02x [expr $ttl << 8]] "
		#End TLV
		set position [lsearch $LLDPPacketInfo "End"]
		if { $position != -1 } {
			append segment [lindex $LLDPPacketInfo [expr $position + 1]]
		} else {
			append segment "00 00"
		}
	}
	return $segment
}


#SetIxiaStream Host $host Card $Card1 Port $Port1 StreamRateMode Fps StreamRate 1 \
#              SouMac $cpumac DesMac 01-80-c2-00-00-00 EthernetType mstp \
#              MstpPacketInfo [list BpduType 02 Flag 7C RootBridgePriority 8000 RootBridgeMac $cpumac ExtRootPathCost 00000000 \
#                             DesignedBridgePriority 8000 DesignedBridgeMac $cpumac PortId 8004 MsgAge 0000 MaxAge 1400 HelloTime 0200 \
#                             ForwardDelay 0F00 \
#                             MstpBaseInfo [list MstpName haha MstpRevision 0000 CISTRootPathCost 80000003 CISTBridgePriority 0F00 \
#                                           CISTBridgeMac $cpumac RemainingHops 14 ]]
#SetIxiaStream Host $host Card $Card1 Port $Port1 StreamRateMode Fps StreamRate 1 \
#              SouMac $cpumac DesMac 01-80-c2-00-00-00 EthernetType mstp \
#              MstpPacketInfo [list BpduType 02 Flag 7C RootBridgePriority 8000 RootBridgeMac $cpumac ExtRootPathCost 00000000 \
#                             DesignedBridgePriority 8000 DesignedBridgeMac $cpumac PortId 8004 MsgAge 0000 MaxAge 1400 HelloTime 0200 \
#                             ForwardDelay 0F00 \
#                             MstpBaseInfo [list MstpName haha MstpRevision 0000 CISTRootPathCost 80000003 CISTBridgePriority 0F00 \
#                                           CISTBridgeMac $cpumac RemainingHops 14 ] \
#                             MstpOtherInfo [list [list InstanceId 1 Flag 00 RootBridgePriority 0000 RootBridgeMac $cpumac RootPathCost 0000 \
#                                                  DesignedBridgePriority 0000 DesignedBridgeMac $cpumac DesignedPortId 0000 RemainingHops 00] \
#                                                 [list InstanceId 2 Flag 00 RootBridgePriority 0000 RootBridgeMac $cpumac RootPathCost 0000 \
#                                                  DesignedBridgePriority 0000 DesignedBridgeMac $cpumac DesignedPortId 0000 RemainingHops 00]]]
proc FormatMstpSegment { StpPacketInfo } {
	set position [lsearch $StpPacketInfo "MstpOtherInfo"]
	if { $position != -1 } {
		set otherinfonum [llength [lindex $StpPacketInfo [expr $position + 1]]]
		set length [expr 106 + 26 * $otherinfonum]
	} else {
		set length 106
	}
	set segment "[format %02X [expr $length / 356]] [format %02X [expr $length % 256]] "
	append segment "42 42 03 00 00 03 "   ;#dsap:42   ssap:42  control field:03   
                                          ;#protocolid:00 00    protocolversion:03
	set position [lsearch $StpPacketInfo "BpduType"]   ;#bpdutype:00/80
	if { $position != -1 } {
		append segment "[lindex $StpPacketInfo [expr $position + 1]] "
	} else {
		append segment "02 "   
	}
	set position [lsearch $StpPacketInfo "Flag"]   ;#flag:00/**
	if { $position != -1 } {
		append segment "[lindex $StpPacketInfo [expr $position + 1]] "
	} else {
		append segment "7C "   
	}
	set position [lsearch $StpPacketInfo "RootBridgePriority"]
	if { $position != -1 } {
		set RootBridgePriority [lindex $StpPacketInfo [expr $position + 1]]
		append segment "[string range $RootBridgePriority 0 1] [string range $RootBridgePriority 2 3] "
	} else {
		append segment "80 00 "   
	}
	set position [lsearch $StpPacketInfo "RootBridgeMac"]
	if { $position != -1 } {
		set RootBridgeMac [lindex $StpPacketInfo [expr $position + 1]]
		append segment "[TransformMac $RootBridgeMac "-" " "] "
	} else {
		append segment "00 03 0F 00 FA 87 "   
	}
	set position [lsearch $StpPacketInfo "ExtRootPathCost"]
	if { $position != -1 } {
		set ExtRootPathCost [lindex $StpPacketInfo [expr $position + 1]]
		append segment "[string range $ExtRootPathCost 0 1] [string range $ExtRootPathCost 2 3] [string range $ExtRootPathCost 4 5] [string range $ExtRootPathCost 6 7] "
	} else {
		append segment "00 00 00 00 "   
	}
	set position [lsearch $StpPacketInfo "DesignedBridgePriority"]
	if { $position != -1 } {
		set DesignedBridgePriority [lindex $StpPacketInfo [expr $position + 1]]
		append segment "[string range $DesignedBridgePriority 0 1] [string range $DesignedBridgePriority 2 3] "
	} else {
		append segment "80 00 "   
	}
	set position [lsearch $StpPacketInfo "DesignedBridgeMac"]
	if { $position != -1 } {
		set DesignedBridgeMac [lindex $StpPacketInfo [expr $position + 1]]
		append segment "[TransformMac $DesignedBridgeMac "-" " "] "
	} else {
		append segment "00 03 0F 00 FA 87 "   
	}
	set position [lsearch $StpPacketInfo "PortId"]
	if { $position != -1 } {
		set PortId [lindex $StpPacketInfo [expr $position + 1]]
		append segment "[string range $PortId 0 1] [string range $PortId 2 3] "
	} else {
		append segment "80 04 "   
	}
	set position [lsearch $StpPacketInfo "MsgAge"]
	if { $position != -1 } {
		set MsgAge [lindex $StpPacketInfo [expr $position + 1]]
		append segment "[string range $MsgAge 0 1] [string range $MsgAge 2 3] "
	} else {
		append segment "00 00 "   
	}
	set position [lsearch $StpPacketInfo "MaxAge"]
	if { $position != -1 } {
		set MaxAge [lindex $StpPacketInfo [expr $position + 1]]
		append segment "[string range $MaxAge 0 1] [string range $MaxAge 2 3] "
	} else {
		append segment "14 00 "   
	}
	set position [lsearch $StpPacketInfo "HelloTime"]
	if { $position != -1 } {
		set HelloTime [lindex $StpPacketInfo [expr $position + 1]]
		append segment "[string range $HelloTime 0 1] [string range $HelloTime 2 3] "
	} else {
		append segment "02 00 "   
	}
	set position [lsearch $StpPacketInfo "ForwardDelay"]
	if { $position != -1 } {
		set ForwardDelay [lindex $StpPacketInfo [expr $position + 1]]
		append segment "[string range $ForwardDelay 0 1] [string range $ForwardDelay 2 3] "
	} else {
		append segment "0F 00 "   
	}
	append segment "00 " ;#version 1 length
	#mstp
	set MstpBaseInfo [lindex $StpPacketInfo [expr [lsearch $StpPacketInfo "MstpBaseInfo"] + 1]]
	append segment "00 "
	#MstpLength
	append segment "[format %02X [expr ($length - 42) / 256]] [format %02X [expr ($length - 42) % 256]]"
	set position [lsearch $MstpBaseInfo "MstpName"]
	if { $position != -1 } {
		set MstpName [lindex $MstpBaseInfo [expr $position + 1]]
		append segment "[FormattoASCII $MstpName 32] "  ;#32bytes
	} else {
		append segment "30 30 30 33 30 66 30 30 "
		append segment "66 61 38 37 00 00 00 00 "
		append segment "00 00 00 00 00 00 00 00 "
		append segment "00 00 00 00 00 00 00 00 "
	}
	set position [lsearch $MstpBaseInfo "MstpRevision"]
	if { $position != -1 } {
		set MstpRevision [lindex $MstpBaseInfo [expr $position + 1]]
		append segment "[string range $MstpRevision 0 1] [string range $MstpRevision 2 3] "
	} else {
		append segment "00 00 "
	}
	set position [lsearch $MstpBaseInfo "MstpDigest"]
	if { $position != -1 } {
		set MstpDigest [lindex $MstpBaseInfo [expr $position + 1]]
		append segment "$MstpDigest "   ;#  unknown   "xx xx xx"
	} else {
		append segment "B4 18 29 F9 03 0a 05 4F "
		append segment "B7 4E F7 A8 58 7F F5 8D "
	}
	set position [lsearch $MstpBaseInfo "CISTRootPathCost"]
	if { $position != -1 } {
		set CISTRootPathCost [lindex $MstpBaseInfo [expr $position + 1]]
		append segment "[string range $CISTRootPathCost 0 1] [string range $CISTRootPathCost 2 3] "
		append segment "[string range $CISTRootPathCost 4 5] [string range $CISTRootPathCost 6 7] "
	} else {
		append segment "80 00 00 03 "
	}
	set position [lsearch $MstpBaseInfo "CISTBridgePriority"]
	if { $position != -1 } {
		set CISTBridgePriority [lindex $MstpBaseInfo [expr $position + 1]]
		append segment "[string range $CISTBridgePriority 0 1] [string range $CISTBridgePriority 2 3] "
	} else {
		append segment "0F 00 "
	}
	set position [lsearch $MstpBaseInfo "CISTBridgeMac"]
	if { $position != -1 } {
		set CISTBridgeMac [lindex $MstpBaseInfo [expr $position + 1]]
		append segment "[TransformMac $CISTBridgeMac "-" " "] "
	} else {
		append segment "FA B7 00 00 00 00 "
	}
	set position [lsearch $MstpBaseInfo "RemainingHops"]
	if { $position != -1 } {
		set RemainingHops [lindex $MstpBaseInfo [expr $position + 1]]
		append segment "[string range $RemainingHops 0 1] "
	} else {
		append segment "14 "
	}
	append segment "00"
		#SetIxiaStream Host $host Card $Card1 Port $Port1 StreamRateMode Fps StreamRate 1 \
#              SouMac $cpumac DesMac 01-80-c2-00-00-00 EthernetType mstp \
#              MstpPacketInfo [list BpduType 02 Flag 7C RootBridgePriority 8000 RootBridgeMac $cpumac ExtRootPathCost 00000000 \
#                             DesignedBridgePriority 8000 DesignedBridgeMac $cpumac PortId 8004 MsgAge 0000 MaxAge 1400 HelloTime 0200 \
#                             ForwardDelay 0F00 \
#                             MstpBaseInfo [list MstpName haha MstpRevision 0000 CISTRootPathCost 80000003 CISTBridgePriority 0F00 \
#                                           CISTBridgeMac $cpumac RemainingHops 14 ] \
#                             MstpOtherInfo [list [list InstanceId 1 Flag 00 RootBridgePriority 0000 RootBridgeMac $cpumac RootPathCost 0000 \
#                                                  DesignedBridgePriority 0000 DesignedBridgeMac $cpumac DesignedPortId 0000 RemainingHops 00] \
#                                                 [list InstanceId 2 Flag 00 RootBridgePriority 0000 RootBridgeMac $cpumac RootPathCost 0000 \
#                                                  DesignedBridgePriority 0000 DesignedBridgeMac $cpumac DesignedPortId 0000 RemainingHops 00]]]
	set position [lsearch $StpPacketInfo "MstpOtherInfo"]
	if { $position != -1 } {
		append segment " "
		set MstpOtherInfo [lindex $StpPacketInfo [expr $position + 1]]
		set OtherInfoNum [llength $MstpOtherInfo]
		for {set j 0} {$j < $OtherInfoNum} {incr j} {
			set MstpOtherInfoMember [lindex $MstpOtherInfo $j]
			set position [lsearch $MstpOtherInfoMember "InstanceId"]
			if { $position != -1 } {
				append segment "[format %02X [lindex $MstpOtherInfoMember [expr $position + 1]]] "
			} else {
				append segment "01 "
			}
			set position [lsearch $MstpOtherInfoMember "Flag"]
			if { $position != -1 } {
				append segment "[lindex $MstpOtherInfoMember [expr $position + 1]] "
			} else {
				append segment "00 "
			}
			set position [lsearch $MstpOtherInfoMember "RootBridgePriority"]
			if { $position != -1 } {
				set RootBridgePriority [lindex $MstpOtherInfoMember [expr $position + 1]]
				append segment "[string range $RootBridgePriority 0 1] [string range $RootBridgePriority 2 3] "
			} else {
				append segment "00 00 "
			}
			set position [lsearch $MstpOtherInfoMember "RootBridgeMac"]
			if { $position != -1 } {
				set RootBridgeMac [lindex $MstpOtherInfoMember [expr $position + 1]]
				append segment "[TransformMac $RootBridgeMac "-" " "] "
			} else {
				append segment "FA B7 00 00 00 00 "
			}
			set position [lsearch $MstpOtherInfoMember "RootPathCost"]
			if { $position != -1 } {
				set RootPathCost [lindex $MstpOtherInfoMember [expr $position + 1]]
				append segment "[string range $RootPathCost 0 1] [string range $RootPathCost 2 3] "
			} else {
				append segment "00 00 "
			}
			set position [lsearch $MstpOtherInfoMember "DesignedBridgePriority"]
			if { $position != -1 } {
				set DesignedBridgePriority [lindex $MstpOtherInfoMember [expr $position + 1]]
				append segment "[string range $DesignedBridgePriority 0 1] [string range $DesignedBridgePriority 2 3] "
			} else {
				append segment "00 00 "
			}
			set position [lsearch $MstpOtherInfoMember "DesignedBridgeMac"]
			if { $position != -1 } {
				set DesignedBridgeMac [lindex $MstpOtherInfoMember [expr $position + 1]]
				append segment "[TransformMac $DesignedBridgeMac "-" " "] "
			} else {
				append segment "FA B7 00 00 00 00 "
			}
			set position [lsearch $MstpOtherInfoMember "DesignedPortId"]
			if { $position != -1 } {
				set DesignedPortId [lindex $MstpOtherInfoMember [expr $position + 1]]
				append segment "[string range $DesignedPortId 0 1] [string range $DesignedPortId 2 3] "
			} else {
				append segment "00 00 "
			}
			set position [lsearch $MstpOtherInfoMember "RemainingHops"]
			if { $position != -1 } {
				append segment "[lindex $MstpOtherInfoMember [expr $position + 1]] "
			} else {
				append segment "00 "
			}
			if { $j == [expr $OtherInfoNum - 1] } {
				append segment "00"
			} else {
				append segment "00 "
			}
		}
	}
	return $segment
}

#SetIxiaStream Host $host Card $Card1 Port $Port1 StreamRateMode Fps StreamRate 1 \
#              SouMac $cpumac DesMac 01-80-c2-00-00-00 EthernetType cluster \
#              ClusterPacketInfo [list ClusterType DP CommanderMac $cpumac]
proc FormatClusterSegment { ClusterPacketInfo segmentsize } {
	set position [lsearch $ClusterPacketInfo "ClusterType"]   
	if { $position != -1 } {
		set ClusterType [lindex $ClusterPacketInfo [expr $position + 1]]
		if { $ClusterType == "DP" } {
			set segment "00 12 AA AA 03 00 12 CF 00 01 "  ;#length:00 12,dsap:AA,ssap:AA,ctrl:03,org:00 12 CF,
			                                                          ;#ethernetType:00 01,version:02,OPCode:01(DP)/02(DR)/03(CP) 			set position [lsearch $ClusterPacketInfo "Version"]   
			set position [lsearch $ClusterPacketInfo "Version"]   
			if { $position != -1 } {
				set Version [lindex $ClusterPacketInfo [expr $position + 1]]
				append segment "$Version "
			} else {
				append segment "02 " 
			}
			set position [lsearch $ClusterPacketInfo "OpCode"]   
			if { $position != -1 } {
				set OpCode [lindex $ClusterPacketInfo [expr $position + 1]]
				append segment "$OpCode "
			} else {
				append segment "01 " 
			}
			set position [lsearch $ClusterPacketInfo "Length"]   
			if { $position != -1 } {
				set Length [lindex $ClusterPacketInfo [expr $position + 1]]
				append segment "[string range $Length 0 1] [string range $Length 2 3] "
			} else {
				append segment "00 0A " 
			}
			set position [lsearch $ClusterPacketInfo "CommanderMac"]   
			if { $position != -1 } {
				set CommanderMac [lindex $ClusterPacketInfo [expr $position + 1]]
				append segment "[TransformMac $CommanderMac "-" " "] "
			} else {
				append segment "00 03 0F 0E A7 B3 " 
			}
			set zerosize [expr $segmentsize - 10 - 10]
			append segment [string trimright [string repeat "00 " $zerosize] " "] 			                                                          
		}
		if { $ClusterType == "DR"} {
			set segment "00 86 AA AA 03 00 03 0F 00 01 "  ;#length:00 78,dsap:AA,ssap:AA,ctrl:03,org:00 12 CF,
			                                                          ;#ethernetType:00 01,version:02,OPCode:01(DP)/02(DR)/03(CP) 			set position [lsearch $ClusterPacketInfo "Version"]   
			set position [lsearch $ClusterPacketInfo "Version"]   
			if { $position != -1 } {
				set Version [lindex $ClusterPacketInfo [expr $position + 1]]
				append segment "$Version "
			} else {
				append segment "02 " 
			}
			set position [lsearch $ClusterPacketInfo "OpCode"]   
			if { $position != -1 } {
				set OpCode [lindex $ClusterPacketInfo [expr $position + 1]]
				append segment "$OpCode "
			} else {
				append segment "02 " 
			}
			set position [lsearch $ClusterPacketInfo "Length"]   
			if { $position != -1 } {
				set Length [lindex $ClusterPacketInfo [expr $position + 1]]
				append segment "[string range $Length 0 1] [string range $Length 2 3] "
			} else {
				append segment "00 7E " 
			}
			set position [lsearch $ClusterPacketInfo "CommanderMac"]   
			if { $position != -1 } {
				set CommanderMac [lindex $ClusterPacketInfo [expr $position + 1]]
				append segment "[TransformMac $CommanderMac "-" " "] "
			} else {
				append segment "00 03 0F 0E A7 B3 " 
			}
			set position [lsearch $ClusterPacketInfo "LocalMac"]   
			if { $position != -1 } {
				set CommanderMac [lindex $ClusterPacketInfo [expr $position + 1]]
				append segment "[TransformMac $CommanderMac "-" " "] "
			} else {
				append segment "00 03 0F 0E A7 B3 " 
			}
			set position [lsearch $ClusterPacketInfo "LocalPort"]   
			if { $position != -1 } {
				set LocalPort [lindex $ClusterPacketInfo [expr $position + 1]]
				regsub -all ernet $LocalPort "" LocalPort
				append segment "[FormattoASCII [string replace [string totitle $LocalPort 0 end] 3 7 ""] 12] "
			} else {
				append segment "45 74 68 31 2F 31 00 00 00 00 00 00 "    ;#Eth1/1
			}
			set position [lsearch $ClusterPacketInfo "RelayMac"]   
			if { $position != -1 } {
				set RelayMac [lindex $ClusterPacketInfo [expr $position + 1]]
				append segment "[TransformMac $RelayMac "-" " "] "
			} else {
				append segment "00 03 0F 0E A7 B3 " 
			}
			set position [lsearch $ClusterPacketInfo "RelayPort"]   
			if { $position != -1 } {
				set RelayPort [lindex $ClusterPacketInfo [expr $position + 1]]
				regsub -all ernet $RelayPort "" RelayPort
				append segment "[FormattoASCII [string replace [string totitle $RelayPort 0 end] 3 7 ""] 12] "
			} else {
				append segment "45 74 68 31 2F 31 00 00 00 00 00 00 "    ;#Eth1/1
			}
			set position [lsearch $ClusterPacketInfo "PortSpeed"]   
			if { $position != -1 } {
				set PortSpeed [lindex $ClusterPacketInfo [expr $position + 1]]
				set segportspeedtmp [format %02X $PortSpeed]
				append segportspeedtmp "0000000000000000000000"
				append segment "[FormatHex segportspeedtmp] "
			} else {
				append segment "31 47 00 00 00 00 00 00 00 00 00 00 00 00 00 "    ;#1-9
			}
			set position [lsearch $ClusterPacketInfo "ClusterRole"]   
			if { $position != -1 } {
				set ClusterRole [lindex $ClusterPacketInfo [expr $position + 1]]
				append segment "[FormatHex [format %02X $ClusterRole]] "
			} else {
				append segment "06 "    ;#>5
			}
			set position [lsearch $ClusterPacketInfo "Description"]   
			if { $position != -1 } {
				set Description [lindex $ClusterPacketInfo [expr $position + 1]]
				append segment "[FormattoASCII $Description 32] "
			} else {
				append segment "00 00 00 00 00 00 00 00 00 00 "
				append segment "00 00 00 00 00 00 00 00 00 00 "
				append segment "00 00 00 00 00 00 00 00 00 00 "
				append segment "00 00 "
			}
			set position [lsearch $ClusterPacketInfo "HostName"]   
			if { $position != -1 } {
				set Description [lindex $ClusterPacketInfo [expr $position + 1]]
				append segment "[FormattoASCII $HostName 32] "
			} else {
				append segment "00 00 00 00 00 00 00 00 00 00 "
				append segment "00 00 00 00 00 00 00 00 00 00 "
				append segment "00 00 00 00 00 00 00 00 00 00 "
				append segment "00 00 "
			}
		}
		if { $ClusterType == "CP" } {
			set segment "00 12 AA AA 03 00 12 CF 00 01 "  ;#length:00 12,dsap:AA,ssap:AA,ctrl:03,org:00 12 CF,
			                                                          ;#ethernetType:00 01,version:02,OPCode:01(DP)/02(DR)/03(CP) 			set position [lsearch $ClusterPacketInfo "Version"]   
			if { $position != -1 } {
				set Version [lindex $ClusterPacketInfo [expr $position + 1]]
				append segment "$Version "
			} else {
				append segment "02 " 
			}
			set position [lsearch $ClusterPacketInfo "OpCode"]   
			if { $position != -1 } {
				set OpCode [lindex $ClusterPacketInfo [expr $position + 1]]
				append segment "$OpCode "
			} else {
				append segment "03 " 
			}
			set position [lsearch $ClusterPacketInfo "SubOp"]   
			if { $position != -1 } {
				set SubOp [lindex $ClusterPacketInfo [expr $position + 1]]
				if { $SubOp == "0001" || $SubOp == "0002" } {
					set segment "00 30 AA AA 03 00 12 CF 00 01 "  ;#length:00 12,dsap:AA,ssap:AA,ctrl:03,org:00 12 CF,
			                                                          ;#ethernetType:00 01,version:02,OPCode:01(DP)/02(DR)/03(CP) 					set position [lsearch $ClusterPacketInfo "Version"]   
					if { $position != -1 } {
						set Version [lindex $ClusterPacketInfo [expr $position + 1]]
						append segment "$Version "
					} else {
						append segment "02 " 
					}
					set position [lsearch $ClusterPacketInfo "OpCode"]   
					if { $position != -1 } {
						set OpCode [lindex $ClusterPacketInfo [expr $position + 1]]
						append segment "$OpCode "
					} else {
						append segment "03 " 
					}
					set position [lsearch $ClusterPacketInfo "Length"]   
					if { $position != -1 } {
						set Length [lindex $ClusterPacketInfo [expr $position + 1]]
						append segment "[string range $Length 0 1] [string range $Length 2 3] "
					} else {
						append segment "00 28 " 
					}
					append segment "[string range $SubOp 0 1] [string range $SubOp 2 3] "  ;#OpCode
					set position [lsearch $ClusterPacketInfo "SubLength"]   
					if { $position != -1 } {
						set SubLength [lindex $ClusterPacketInfo [expr $position + 1]]
						append segment "[string range $SubLength 0 1] [string range $SubLength 2 3] "
					} else {
						append segment "00 20 " 
					}
					set position [lsearch $ClusterPacketInfo "MemberId"]   
					if { $position != -1 } {
						set MemberId [lindex $ClusterPacketInfo [expr $position + 1]]
						append segment "[string range $MemberId 0 1] [string range $MemberId 2 3] "
					} else {
						append segment "00 01 " 
					}
					set position [lsearch $ClusterPacketInfo "ErrCode"]   
					if { $position != -1 } {
						set ErrCode [lindex $ClusterPacketInfo [expr $position + 1]]
						append segment "[string range $ErrCode 0 1] [string range $ErrCode 2 3] "
					} else {
						append segment "00 00 " 
					}
					set position [lsearch $ClusterPacketInfo "ClusterKey"]   
					if { $position != -1 } {
						set ClusterKey [lindex $ClusterPacketInfo [expr $position + 1]]
						append segment "[FormattoASCII $Description 16] "
					} else {
						append segment "00 00 00 00 00 00 00 00 00 00 " 
						append segment "00 00 00 00 00 00 "
					}
					set position [lsearch $ClusterPacketInfo "SrcIp"]   
					if { $position != -1 } {
						set SrcIp [lindex $ClusterPacketInfo [expr $position + 1]]
						append segment "[FormatIptoHex $SrcIp] "
					} else {
						append segment "00 00 00 00 "
					}
					set position [lsearch $ClusterPacketInfo "DstIp"]   
					if { $position != -1 } {
						set DstIp [lindex $ClusterPacketInfo [expr $position + 1]]
						append segment "[FormatIptoHex $DstIp] "
					} else {
						append segment "00 00 00 00 "
					}
					set position [lsearch $ClusterPacketInfo "Interval"]   
					if { $position != -1 } {
						set Interval [lindex $ClusterPacketInfo [expr $position + 1]]
						append segment "[string range $Interval 0 1] [string range $Interval 2 3] "
					} else {
						append segment "00 01 "
					}
					set position [lsearch $ClusterPacketInfo "Losscount"]   
					if { $position != -1 } {
						set Losscount [lindex $ClusterPacketInfo [expr $position + 1]]
						append segment "[string range $Losscount 0 1] [string range $Losscount 2 3]"
					} else {
						append segment "00 01"
					}
  				} elseif { $OpCode == "0003" || $OpCode == "0004" } {
  					set segment "00 14 AA AA 03 00 12 CF 00 01 "  ;#length:00 12,dsap:AA,ssap:AA,ctrl:03,org:00 12 CF,
			                                                          ;#ethernetType:00 01,version:02,OPCode:01(DP)/02(DR)/03(CP) 					set position [lsearch $ClusterPacketInfo "Version"]   
					if { $position != -1 } {
						set Version [lindex $ClusterPacketInfo [expr $position + 1]]
						append segment "$Version "
					} else {
						append segment "02 " 
					}
					set position [lsearch $ClusterPacketInfo "OpCode"]   
					if { $position != -1 } {
						set OpCode [lindex $ClusterPacketInfo [expr $position + 1]]
						append segment "$OpCode "
					} else {
						append segment "03 " 
					}
					set position [lsearch $ClusterPacketInfo "Length"]   
					if { $position != -1 } {
						set Length [lindex $ClusterPacketInfo [expr $position + 1]]
						append segment "[string range $Length 0 1] [string range $Length 2 3] "
					} else {
						append segment "00 0C " 
					}
					append segment "[string range $SubOp 0 1] [string range $SubOp 2 3] "  ;#OpCode
					set position [lsearch $ClusterPacketInfo "SubLength"]   
					if { $position != -1 } {
						set SubLength [lindex $ClusterPacketInfo [expr $position + 1]]
						append segment "[string range $SubLength 0 1] [string range $SubLength 2 3] "
					} else {
						append segment "00 04 " 
					}
					set position [lsearch $ClusterPacketInfo "MemberId"]   
					if { $position != -1 } {
						set MemberId [lindex $ClusterPacketInfo [expr $position + 1]]
						append segment "[string range $MemberId 0 1] [string range $MemberId 2 3] "
					} else {
						append segment "00 01 " 
					}
					set position [lsearch $ClusterPacketInfo "ErrCode"]   
					if { $position != -1 } {
						set ErrCode [lindex $ClusterPacketInfo [expr $position + 1]]
						append segment "[string range $ErrCode 0 1] [string range $ErrCode 2 3]"
					} else {
						append segment "00 00" 
					}	
				} else {
					set position [lsearch $ClusterPacketInfo "Length"]   
					if { $position != -1 } {
						set Length [lindex $ClusterPacketInfo [expr $position + 1]]
						append segment "[string range $Length 0 1] [string range $Length 2 3] "
					} else {
						append segment "00 0C " 
					}
					append segment "[string range $SubOp 0 1] [string range $SubOp 2 3] "  ;#OpCode
					set zerosize [expr $segmentsize - 10 - 6]
					append segment [string trimright [string repeat "00 " $zerosize] " "] 	
				}
			} else {
				PrintRes Print "should have sub opcode!" 
				return 0
			}
		}
		if { $ClusterType == "CC" } {
			;#null
		}	
	} else {
		PrintRes Print "should have cluster type!"
		return 0
	}	
	return $segment
}


########################add by qiaoyua#############################
#对NA数据部分进行格式化，使其符合IXIA的需要
proc FormatIpv6NdpNaSegment { arrlist } {
	upvar 1 $arrlist arr
	#ipv6addr为NA报文Target Address字段
	if [info exist arr(Ipv6Addr)] {
    		set ipv6addr [FormatHexIpv6 $arr(Ipv6Addr)]
    	} else {
			return -1
    }
    append segment "$ipv6addr"
    if [info exists arr(NoOption)] {
		if {$arr(NoOption) == 1} {
			return $segment
		}
    }
    #以下为NA报文所附加的option:Target link-layer address
    #02为Target link-layer address的type字段
    #01为Target link-layer address的length字段
    append segment " 02 01 "
    #macaddr为Target link-layer address的linklayer address(即对应ipv6addr的mac地址)
    if [info exist arr(Mac)] {
    		regsub -all {\-} $arr(Mac) " " macaddr
    	} else {
			return -1
    }
    append segment "$macaddr"
    return $segment
}

########################add by qiaoyua#############################
#对NS数据部分进行格式化，使其符合IXIA的需要
proc FormatIpv6NdpNsSegment { arrlist } {
	upvar 1 $arrlist arr
	#TargetAddr为NS报文Target Address字段
	if [info exist arr(TargetAddr)] {
    		set ipv6addr [FormatHexIpv6 $arr(TargetAddr)]
    	} else {
			return -1
    }
    append segment "$ipv6addr"
    if [info exists arr(DAD)] {
		if {$arr(DAD) == 1} {
			return $segment
		}
    }
    #以下为NS报文所附加的option:Source link-layer address
    #01为Source link-layer address的type字段
    #01为Source link-layer address的length字段
    append segment " 01 01 "
    #macaddr为Source link-layer address的linklayer address
    if [info exist arr(Mac)] {
    		regsub -all {\-} $arr(Mac) " " macaddr
    	} else {
			return -1
    }
    append segment "$macaddr"
    return $segment
}

########################add by qiaoyua#############################
#对Redirect数据部分进行格式化，使其符合IXIA的需要
proc FormatIpv6NdpRedirectSegment { arrlist } {
	upvar 1 $arrlist arr
	#TargetAddr为Redirect报文Target Address字段
	if [info exist arr(TargetAddr)] {
    		set ipv6addr [FormatHexIpv6 $arr(TargetAddr)]
    	} else {
			return -1
    }
    append segment "$ipv6addr "
    #DesAddr为Redirect报文Destination Address字段
	if [info exist arr(DesAddr)] {
    		set ipv6addr [FormatHexIpv6 $arr(DesAddr)]
    	} else {
			return -1
    }
    append segment "$ipv6addr "
    append segment "02 01 "
    if [info exist arr(Mac)] {
    		regsub -all {\-} $arr(Mac) " " macaddr
    	} else {
			return -1
    }
    append segment "$macaddr "
    append segment "04 0E [string repeat "00 " 109]00"
    return $segment
}

#格式为 SetIxiaStream Host $host Card $Card1 Port $Port1 StreamRateMode Fps StreamRate 1 \
#                     SouMac $cpumac DesMac 33-33-00-00-00-01 Protocl ipv6 \
#                     SouIpv6 [GetLinkLocalAddress $cpumac] DesIpv6 FF02::1 ProtoclEx ipv6ra \
#                     Ipv6RAPacketInfo [list CheckSum "B5 6F" CurHopLimit 0 FlagM 0 FlagO 0 RouterLifeTime 12 ReachableTime 0 RetransTimer 0 \
#                     SourceLinkLayer [list Type 1 Length 1 LinkLayerAddress $cpumac] \
#                     MTU [list Type 5 Length 1 MTU 1500] \
#                     PrefixInformation [list Type 3 Length 4 PrefixLength 64 FlagLink 1 FlagAutonomous 1 FlagNotRouterAddress 0 \
#                                        FlagSitePrefix 1 ValidLifeTime 0 PreferredLifeTime 0 Prefix 2321::]]
proc FormatIpv6RASegment { Ipv6RAPacketInfo } {
	array set ra $Ipv6RAPacketInfo
	set segment ""
	if [info exists ra(ReachableTime)] {
		set reachabletime $ra(ReachableTime)
	} else {
		set reachabletime 0
	}
	append segment "[FormatHex [format %08x $reachabletime]] "
	if [info exists ra(RetransTimer)] {
		set retranstimer $ra(RetransTimer)
	} else {
		set retranstimer 0
	}
	append segment "[FormatHex [format %08x $retranstimer]] "
	if [info exists ra(SourceLinkLayer)] {
		array set sourcelinklayer $ra(SourceLinkLayer)
		if [info exists sourcelinklayer(Type)] {
			set type $sourcelinklayer(Type)
		} else {
			set type 1
		}
		if [info exists sourcelinklayer(Length)] {
			set length $sourcelinklayer(Length)
		} else {
			set length 1
		}
		if [info exists sourcelinklayer(LinkLayerAddress)] {
			regsub -all \\- $sourcelinklayer(LinkLayerAddress) " " linklayeraddress
		} else {
			set linklayeraddress "00 00 00 00 00 00"
		}
		append segment "[format %02x $type] [format %02x $length] $linklayeraddress "
	}
	#去掉下面的else语句。下面语句是去掉segment变量最后的空格，这样会导致后面附加的option字段内容
	#直接连接到segment，与前面内容没有空格分隔，不符合ixia格式要求
#	 else {
#		set segment [string trimright $segment " "]
#	}
	if [info exists ra(RedirectHeader)] {
		array set redirectheader $ra(RedirectHeader)
		if [info exists redirectheader(Type)] {
			set type redirectheader(Type)
		} else {
			set type 4
		}
		if [info exists redirectheader(Length)] {
			set length redirectheader(Length)
		} else {
			set length 1
		}
		append segment "[format %02x $type] [format %02x $length] 00 00 00 00 00 00 "
	}
#	 else {
#		set segment [string trimright $segment " "]
#	}
	if [info exists ra(MTU)] {
		array set mtu $ra(MTU)
		if [info exists mtu(Type)] {
			set type $mtu(Type)
		} else {
			set type 5
		}
		if [info exists mtu(Length)] {
			set length $mtu(Length)
		} else {
			set length 1
		}
		if [info exists mtu(MTU)] {
			set mtuvalue $mtu(MTU)
		} else {
			set mtuvalue 1500
		}
		append segment "[format %02x $type] [format %02x $length] 00 00 [FormatHex [format %04x $mtuvalue]] "
	}
#	 else {
#		set segment [string trimright $segment " "]
#	}
	if [info exists ra(PrefixInformation)] {
		array set prefixinformantion $ra(PrefixInformation)
		if [info exists prefixinformantion(Type)] {
			set type $prefixinformantion(Type)
		} else {
			set type 3
		}
		if [info exists prefixinformantion(Length)] {
			set length $prefixinformantion(Length)
		} else {
			set length 4
		}
		if [info exists prefixinformantion(PrefixLength)] {
			set prefixlength $prefixinformantion(PrefixLength)
		} else {
			set prefixlength 64
		}
		if [info exists prefixinformantion(FlagLink)] {
			set flaglink $prefixinformantion(FlagLink)
		} else {
			set flaglink 1
		}
		if [info exists prefixinformantion(FlagAutonomous)] {
			set flagautonomous $prefixinformantion(FlagAutonomous)
		} else {
			set flagautonomous 1
		}
		if [info exists prefixinformantion(FlagNotRouterAddress)] {
			set flagnotrouteraddress $prefixinformantion(FlagNotRouterAddress)
		} else {
			set flagnotrouteraddress 0
		}
		if [info exists prefixinformantion(FlagSitePrefix)] {
			set flagsitprefix $prefixinformantion(FlagSitePrefix)
		} else {
			set flagsitprefix 1
		}
		if [info exists prefixinformantion(ValidLifeTime)] {
			set validlifetime $prefixinformantion(ValidLifeTime)
		} else {
			set validlifetime 0
		}
		if [info exists prefixinformantion(PreferredLifeTime)] {
			set preferredlifetime $prefixinformantion(PreferredLifeTime)
		} else {
			set preferredlifetime 0
		}
		if [info exists prefixinformantion(Prefix)] {
			set prefix $prefixinformantion(Prefix)
		} else {
			set prefix 2321::
		}
		append segment "[format %02x $type] [format %02x $length] [format %02x $prefixlength] "
		append segment "[format %02x [expr $flaglink << 3 + $flagautonomous << 2 + $flagnotrouteraddress << 1 + $flagsitprefix]] "
		append segment "[FormatHex [format %08x $validlifetime]] [FormatHex [format %08x $preferredlifetime]] 00 00 00 00 "
		append segment "[FormatHexIpv6 $prefix]"
	}
#	 else {
#		set segment [string trimright $segment " "]
#	}
	#在最后对segment变量做清除后面空格的处理
	set segment [string trimright $segment " "]
	return $segment
		
}

########################add by zouleia#############################
#对RS数据部分进行格式化，使其符合IXIA的需要
proc FormatIpv6RSSegment { arrlist } {
	upvar 1 $arrlist arr
	append segment "01 01 "
    #macaddr为source link layer mac
    if [info exist arr(Mac)] {
    		regsub -all {\-} $arr(Mac) " " macaddr
    	} else {
			return -1
    }
    append segment "$macaddr"
    return $segment
}

################################
#
# FormatHex:SetIxiaUDF内部调用函数
#
# args:
#     hex
# 
# return:
#
# addition:
#    格式化16进制值，如将1111格式化为设置UDF需要的{11 11}
# examples:
#
###############################
proc FormatHex { hex } {    
    set newhex ""
    regsub "0x" $hex {} hex
    set length [ string length $hex ]
    if { [ expr $length % 2 ] != 0 } {
        set hex "0$hex"
        incr length
    }
    set i 0 
    while { $i < $length } {
        if { $i !=0 } {
            append newhex " "
        }
        append newhex [string range $hex $i [ expr $i + 1 ] ]
        set i [expr $i + 2 ]
    }
    return $newhex
}

	

################################
#
# SetDscp:SetIxiaStream 内部调用函数
#
# args: 
#     Dscp
#
# return:
#
# addition:
#
# examples:
#
###############################
proc SetDscp { Dscp } {
#    #转换为二进制
#    set binNum [Int2Binary $Dscp]
#    #将不到6bit的二进制格式到6bit，前面添0
#    set len [ expr 6 - [string length $binNum] ]
#    set ret $binNum
#    while { $len > 0 } {
#        set ret 0$ret
#        set len [ expr $len - 1 ]
#    }    
#	#puts "$ret"
#	set temp1 [expr 4 * [string index $ret 0]]
#	set temp2 [expr 2 * [string index $ret 1]]
#	set temp3 [expr 1 * [string index $ret 2]]
#	set temp [expr $temp1 + $temp2 + $temp3]
#	ip config -precedence $temp
#	ip config -delay [string index $ret 3]
#	ip config -throughput [string index $ret 4]
#	ip config -reliability [string index $ret 5]
	set ipprecedence [ expr { ( $Dscp & 56 ) / 8 } ]
	set delay [ expr { ( $Dscp & 4 ) / 4 } ]
	set throughput [ expr { ( $Dscp & 2 ) / 2 } ]
	set reliability [ expr { $Dscp & 1 } ]
	ip config -precedence $ipprecedence
	ip config -delay $delay
	ip config -throughput $throughput
	ip config -reliability $reliability
}

################################
#
# SetTos:SetIxiaStream 内部调用函数
#
# args: 
#     Dscp
#
# return:
#
# addition:
#
# examples:
#
###############################
proc SetTos { Tos } {
	set delay [ expr { ( $Tos & 8 ) / 8 } ]
	set throughput [ expr { ( $Tos & 4 ) / 4 } ]
	set reliability [ expr { ( $Tos & 2 ) / 2 } ]
	set cost [ expr { ( $Tos & 1 ) } ]
	ip config -delay $delay
	ip config -throughput $throughput
	ip config -reliability $reliability
	ip config -cost $cost
}

################################
#
# SetIpprecedence:SetIxiaStream 内部调用函数
#
# args: 
#     Dscp
#
# return:
#
# addition:
#
# examples:
#
###############################
proc SetIpprecedence { Ipprecedence } {
	ip config -precedence $Ipprecedence
}

################################
#
# SetIpprecedenceTos:SetIxiaStream 内部调用函数
#
# args: 
#     Dscp
#
# return:
#
# addition:
#
# examples:
#
###############################
proc SetIpprecedenceTos { Ipprecedence Tos } {	
	set delay [ expr { ( $Tos & 8 ) / 8 } ]
	set throughput [ expr { ( $Tos & 4 ) / 4 } ]
	set reliability [ expr { ( $Tos & 2 ) / 2 } ]
	set cost [ expr { $Tos & 1 } ]
	ip config -precedence $Ipprecedence
	ip config -delay $delay
	ip config -throughput $throughput
	ip config -reliability $reliability
	ip config -cost $cost
}




#SetIxiaAsPC Host 172.16.1.253 Card 4 Port 7 Ipv4Host {{Ipv4Address 20.1.1.2 Ipv4MaskWidth 24 GateWay 20.1.1.1 MacAddress 00-00-01-00-00-01}}
#SetIxiaAsPC Host 172.16.1.253 Card 4 Port 7 Ipv4Host {{Ipv4Address 20.1.1.2 Ipv4MaskWidth 24 GateWay 20.1.1.1 Ipv4IncrStep 1 Ipv4IncrMode ClassD Ipv4IncrNum 10}}
#SetIxiaAsPC Host 172.16.1.253 Card 4 Port 7 Ipv6Host {{Ipv6Address 2000::2 Ipv6MaskWidth 64 MacAddress 00-00-01-00-00-01}}
#SetIxiaAsPC Host 172.16.1.253 Card 4 Port 7 Ipv6Host {{Ipv6Address 2000::2 Ipv6MaskWidth 64 Ipv6IncrStep 1 Ipv6IncrMode 8 Ipv6IncrNum 10}}
#SetIxiaAsPC Host 172.16.1.253 Card 4 Port 7 Ipv4v6Host {{Ipv4Address 20.1.1.2 Ipv4MaskWidth 24 GateWay 20.1.1.1 Ipv6Address 2000::2 Ipv6MaskWidth 64 MacAddress 00-00-01-00-00-01}}
#SetIxiaAsPC Host 172.16.1.253 Card 4 Port 7 Ipv4v6Host {{Ipv4Address 20.1.1.2 Ipv4MaskWidth 24 GateWay 20.1.1.1 Ipv4IncrStep 1 Ipv4IncrMode ClassD \
#            Ipv6Address 2000::2 Ipv6MaskWidth 64 Ipv6IncrStep 1 Ipv6IncrMode 8 Ipv4v6IncrNum 10 MacAddress 00-00-01-00-00-01}}
#SetIxiaAsPC Host 172.16.1.253 Card 4 Port 7 Ipv4Host {{Ipv4Address 20.1.1.2 Ipv4MaskWidth 24 GateWay 20.1.1.1 Ipv4IncrStep 1 Ipv4IncrMode ClassD Ipv4IncrNum 10}} \
#            Ipv6Host {{Ipv6Address 2000::2 Ipv6MaskWidth 64 Ipv6IncrStep 1 Ipv6IncrMode 8 Ipv6IncrNum 10}} \
#            Ipv4v6Host {{Ipv4Address 20.1.1.2 Ipv4MaskWidth 24 GateWay 20.1.1.1 Ipv4IncrStep 1 Ipv4IncrMode ClassD \
#            Ipv6Address 2000::2 Ipv6MaskWidth 64 Ipv6IncrStep 1 Ipv6IncrMode 8 Ipv4v6IncrNum 10 MacAddress 00-00-01-00-00-01}}
#SetIxiaAsPC Host 172.16.1.253 Card 4 Port 7 Ipv4Host {{Ipv4Address 20.1.1.2 Ipv4MaskWidth 24 GateWay 20.1.1.1 MacAddress 00-00-01-00-00-01 VlanEnable true VlanId 10 VlanPriority 2}}
#SetIxiaAsPC Host 172.16.1.253 Card 4 Port 7 Ipv4Host {{Ipv4Address 20.1.1.2 Ipv4MaskWidth 24 GateWay 20.1.1.1 MacAddress 00-00-01-00-00-01} \
#                                                      {Ipv4Address 30.1.1.2 Ipv4MaskWidth 24 GateWay 30.1.1.1 MacAddress 00-00-01-00-00-01}}

#EnablePC 172.16.1.249 3 2
#EnablePC 172.16.1.249 3 2 {1 3 5}
proc EnablePC { Host Card Port {numlist all}} {
	set ChasId [ixGetChassisID $Host]
	interfaceTable select $ChasId $Card $Port
	set InterfaceDescription "[format %02d $Card]:[format %02d $Port] - 1"
	if { $numlist == "all" } {
		while {[interfaceTable getInterface $InterfaceDescription] == 0} {
			interfaceEntry config -enable enable
			interfaceTable setInterface $InterfaceDescription
			set InterfaceDescription [IncrInterfaceDescription $InterfaceDescription]
		}
		interfaceTable write
	} else {
		foreach num $numlist {
			set InterfaceDescription "[format %02d $Card]:[format %02d $Port] - $num"
			interfaceTable getInterface $InterfaceDescription
			interfaceEntry config -enable enable
			interfaceTable setInterface $InterfaceDescription
		}
		interfaceTable write
	}
}

#DisablePC 172.16.1.249 3 2
#DisablePC 172.16.1.249 3 2 {1 3 5}
proc DisablePC { Host Card Port {numlist all} } {
	set ChasId [ixGetChassisID $Host]
	interfaceTable select $ChasId $Card $Port
	set InterfaceDescription "[format %02d $Card]:[format %02d $Port] - 1"
	if { $numlist == "all" } {
		while {[interfaceTable getInterface $InterfaceDescription] == 0} {
			interfaceEntry config -enable disable
			interfaceTable setInterface $InterfaceDescription
			set InterfaceDescription [IncrInterfaceDescription $InterfaceDescription]
		}
		interfaceTable write
	} else {
		foreach num $numlist {
			set InterfaceDescription "[format %02d $Card]:[format %02d $Port] - $num"
			interfaceTable getInterface $InterfaceDescription
			interfaceEntry config -enable disable
			interfaceTable setInterface $InterfaceDescription
		}
		interfaceTable write
	}
}

proc SetIxiaAsPC { args } {
    set Host 172.16.1.251
    set Card 4
    set Port 1
    set Ip 10.1.1.2
    set MaskWidth 24
    set GateWay 10.1.1.1
    set IpIncrNum 1
    set IpIncrMode ClassD
    set IpIncrStep 1
    set Ipv6 2002::2
    set Ipv6MaskWidth 64
    set Ipv6IncrNum 0
    set Ipv6IncrMode 8
    set Ipv6IncrStep 1
    set Mac 00-00-00-00-00-01
    set Action set
    
	array set arrArgs $args 	
  	foreach {para value} [array get arrArgs] {
		#puts "para=$para"
		#puts "value =$value"  	
		switch -exact -- $para {
		    Host {
		    	set Host $value
		    }
		    Card {
		   		set Card $value
		   	}
		   	Port { 
		   		set Port $value
		   	}
		   	Ip {
		   		set Ip $value
		   	}
		   	MaskWidth {
		   		set MaskWidth $value
		   	}
		   	GateWay {
		   		set GateWay $value
		   	}
		   	IpIncrNum {
		   	    set IpIncrNum $value
		   	}
		   	IpIncrMode {
		   	    set IpIncrMode $value
		   	}
		   	IpIncrStep {
		   	    set IpIncrStep $value
		   	}
		   	Ipv6 {
		   	    set Ipv6 $value
		   	}
		   	Ipv6MaskWidth {
		   	    set Ipv6MaskWidth $value
		   	}
		   	Ipv6IncrNum {
		   	    set Ipv6IncrNum $value
		   	}	
		   	Ipv6IncrMode {
		   	    set Ipv6IncrMode $value
		   	}
		   	Ipv6IncrStep {
		   	    set Ipv6IncrStep $value
		   	}	   	
		   	Mac {
		   		set Mac $value
		   	}
		   	Ipv4Host {
		   	    set Ipv4Host $value
		   	}
		   	Ipv6Host {
		   	    set Ipv6Host $value
		   	}
		   	Ipv4v6Host {
		   	    set Ipv4v6Host $value
		   	}
		   	Action {
		   		set Action $value
		   	}
			default {
		   		puts "Wrong para name:$para "
		   		return -1	
		   	}
		}		
	}
	ixInitialize $Host
	set ChasId [ixGetChassisID $Host]
	set portlist [list [list $ChasId $Card $Port]]
	interfaceTable select $ChasId $Card $Port
	interfaceTable setDefault
	interfaceTable clearAllInterfaces 
    set InterfaceDescription "[format %02d $Card]:[format %02d $Port] - 1"
    if [info exists Ipv4Host] {
        set Ipv4HostListNum [llength $Ipv4Host]
        for {set Ipv4HostListIndex 1} {$Ipv4HostListIndex <= $Ipv4HostListNum} {incr Ipv4HostListIndex} {
            set Ipv4HostListIndexInfo [lindex $Ipv4Host [expr $Ipv4HostListIndex - 1]]
            set Ipv4IncrMode ClassD
            set Ipv4IncrStep 1
            set Ipv4IncrNum 1
            set MacAddress 00-00-00-00-00-01
            set MacStep 1
            set VlanEnable false
            set VlanId 0
            set VlanPriority 0
            array set arrIpv4HostListIndexInfo $Ipv4HostListIndexInfo 	
          	foreach {para value} [array get arrIpv4HostListIndexInfo] {
        		switch -exact -- $para {
        		    InterfaceDescription {
        		        set InterfaceDescription $value
        		    }
        		    Ipv4Address {
        		        set Ipv4Address $value
        		    }
        		    Ipv4MaskWidth {
                        set Ipv4MaskWidth $value
        		    }
        		    GateWay {
        		        set GateWay $value
        		    }
        		    Ipv4IncrStep {
        		        set Ipv4IncrStep $value
        		    }
        		    Ipv4IncrMode {
        		        set Ipv4IncrMode $value
        		    }
        		    Ipv4IncrNum {
        		        set Ipv4IncrNum $value
        		    }
        		    MacAddress {
        		        set MacAddress $value
        		    }
        		    MacStep {
        		        set MacStep $value
        		    }
        		    VlanEnable {
        		        set VlanEnable $value
        		    }
        		    VlanId {
        		        set VlanId $value
        		    }
        		    VlanPriority {
        		        set VlanPriority $value
        		    }
        			default {
        		   		puts "Wrong para name:$para "
        		   		return -1	
        		   	}
        		}		
        	}
        	for {set i 1} {$i <= $Ipv4IncrNum} {incr i} {
        	    interfaceEntry clearAllItems addressTypeIpV6
                interfaceEntry clearAllItems addressTypeIpV4
                interfaceEntry setDefault
                set MacAddresstemp [split $MacAddress -]
        	    interfaceIpV4 setDefault
                interfaceIpV4 config -ipAddress $Ipv4Address
                interfaceIpV4 config -maskWidth $Ipv4MaskWidth
                interfaceIpV4 config -gatewayIpAddress $GateWay
                interfaceEntry addItem addressTypeIpV4
                interfaceEntry config -enable true
        	    interfaceEntry config -description $InterfaceDescription
        	    interfaceEntry config -macAddress  $MacAddresstemp
        	    interfaceEntry config -enableVlan $VlanEnable
                interfaceEntry config -vlanId $VlanId
                interfaceEntry config -vlanPriority $VlanPriority
        	    interfaceTable addInterface interfaceTypeConnected
                set Ipv4Address [IncrIpStep $Ipv4Address $Ipv4IncrMode $Ipv4IncrStep]
                set InterfaceDescription [IncrInterfaceDescription $InterfaceDescription]
                set MacAddress [IncrMacStep $MacAddress $MacStep]
            }
        }
    }
    if [info exists Ipv6Host] {  
        set Ipv6HostListNum [llength $Ipv6Host]
        for {set Ipv6HostListIndex 1} {$Ipv6HostListIndex <= $Ipv6HostListNum} {incr Ipv6HostListIndex} {
            set Ipv6HostListIndexInfo [lindex $Ipv6Host [expr $Ipv6HostListIndex - 1]]
            set Ipv6IncrMode 8
            set Ipv6IncrStep 1
            set Ipv6IncrNum 1
            set MacAddress 00-00-00-00-00-01
            set MacStep 1
            set VlanEnable false
            set VlanId 0
            set VlanPriority 0
            array set arrIpv6HostListIndexInfo $Ipv6HostListIndexInfo 	
          	foreach {para value} [array get arrIpv6HostListIndexInfo] {
        		switch -exact -- $para {
        		    InterfaceDescription {
        		        set InterfaceDescription $value
        		    }
        		    Ipv6Address {
        		        set Ipv6Address $value
        		    }
        		    Ipv6MaskWidth {
                        set Ipv6MaskWidth $value
        		    }
        		    Ipv6IncrStep {
        		        set Ipv6IncrStep $value
        		    }
        		    Ipv6IncrMode {
        		        set Ipv6IncrMode $value
        		    }
        		    Ipv6IncrNum {
        		        set Ipv6IncrNum $value
        		    }
        		    MacAddress {
        		        set MacAddress $value
        		    }
        		    MacStep {
        		        set MacStep $value
        		    }
        		    VlanEnable {
        		        set VlanEnable $value
        		    }
        		    VlanId {
        		        set VlanId $value
        		    }
        		    VlanPriority {
        		        set VlanPriority $value
        		    }
        			default {
        		   		puts "Wrong para name:$para "
        		   		return -1	
        		   	}
        		}		
        	}
        	for {set i 1} {$i <= $Ipv6IncrNum} {incr i} {
        	    interfaceEntry clearAllItems addressTypeIpV6
                interfaceEntry clearAllItems addressTypeIpV4
                interfaceEntry setDefault
                set MacAddresstemp [split $MacAddress -]
        	    interfaceIpV6 setDefault
        	    interfaceIpV6 config -ipAddress $Ipv6Address
        	    interfaceIpV6 config -maskWidth $Ipv6MaskWidth
        	    interfaceEntry addItem addressTypeIpV6
                interfaceEntry config -enable true
        	    interfaceEntry config -description $InterfaceDescription
        	    interfaceEntry config -macAddress  $MacAddresstemp    	
        	    interfaceEntry config -enableVlan $VlanEnable
                interfaceEntry config -vlanId $VlanId
                interfaceEntry config -vlanPriority $VlanPriority
        	    interfaceTable addInterface interfaceTypeConnected
                set Ipv6Address [IncrIpv6Step $Ipv6Address $Ipv6IncrMode $Ipv6IncrStep]
                set InterfaceDescription [IncrInterfaceDescription $InterfaceDescription]
                set MacAddress [IncrMacStep $MacAddress $MacStep]
            }
        }
    }
    if [info exists Ipv4v6Host] {
        set Ipv4v6HostListNum [llength $Ipv4v6Host]
        for {set Ipv4v6HostListIndex 1} {$Ipv4v6HostListIndex <= $Ipv4v6HostListNum} {incr Ipv4v6HostListIndex} {
            set Ipv4v6HostListIndexInfo [lindex $Ipv4v6Host [expr $Ipv4v6HostListIndex - 1]]
            set Ipv4IncrMode ClassD
            set Ipv4IncrStep 1
            set Ipv6IncrMode 8
            set Ipv6IncrStep 1
            set Ipv4v6IncrNum 1
            set MacAddress 00-00-00-00-00-01
            set MacStep 1
            set VlanEnable false
            set VlanId 0
            set VlanPriority 0
            array set arrIpv4v6HostListIndexInfo $Ipv4v6HostListIndexInfo 	
          	foreach {para value} [array get arrIpv4v6HostListIndexInfo] {
        		switch -exact -- $para {
        		    InterfaceDescription {
        		        set InterfaceDescription $value
        		    }
        		    Ipv4Address {
        		        set Ipv4Address $value
        		    }
        		    Ipv4MaskWidth {
                        set Ipv4MaskWidth $value
        		    }
        		    GateWay {
        		        set GateWay $value
        		    }
        		    Ipv4IncrStep {
        		        set Ipv4IncrStep $value
        		    }
        		    Ipv4IncrMode {
        		        set Ipv4IncrMode $value
        		    }
        		    Ipv6Address {
        		        set Ipv6Address $value
        		    }
        		    Ipv6MaskWidth {
                        set Ipv6MaskWidth $value
        		    }
        		    Ipv6IncrStep {
        		        set Ipv6IncrStep $value
        		    }
        		    Ipv6IncrMode {
        		        set Ipv6IncrMode $value
        		    }
        		    Ipv4v6IncrNum {
        		        set Ipv4v6IncrNum $value
        		    }
        		    MacAddress {
        		        set MacAddress $value
        		    }
        		    MacStep {
        		        set MacStep $value
        		    }
        		    VlanEnable {
        		        set VlanEnable $value
        		    }
        		    VlanId {
        		        set VlanId $value
        		    }
        		    VlanPriority {
        		        set VlanPriority $value
        		    }
        			default {
        		   		puts "Wrong para name:$para "
        		   		return -1	
        		   	}
        		}		
        	}
        	for {set i 1} {$i <= $Ipv4v6IncrNum} {incr i} {
        	    interfaceEntry clearAllItems addressTypeIpV6
                interfaceEntry clearAllItems addressTypeIpV4
                interfaceEntry setDefault
                set MacAddresstemp [split $MacAddress -]
        	    interfaceIpV4 setDefault
                interfaceIpV4 config -ipAddress $Ipv4Address
                interfaceIpV4 config -maskWidth $Ipv4MaskWidth
                interfaceIpV4 config -gatewayIpAddress $GateWay
                interfaceEntry addItem addressTypeIpV4
                interfaceIpV6 setDefault
        	    interfaceIpV6 config -ipAddress $Ipv6Address
        	    interfaceIpV6 config -maskWidth $Ipv6MaskWidth
        	    interfaceEntry addItem addressTypeIpV6
                interfaceEntry config -enable true
        	    interfaceEntry config -description $InterfaceDescription
        	    interfaceEntry config -macAddress  $MacAddresstemp    	
        	    interfaceEntry config -enableVlan $VlanEnable
                interfaceEntry config -vlanId $VlanId
                interfaceEntry config -vlanPriority $VlanPriority
        	    interfaceTable addInterface interfaceTypeConnected
                set Ipv4Address [IncrIpStep $Ipv4Address $Ipv4IncrMode $Ipv4IncrStep]
                set Ipv6Address [IncrIpv6Step $Ipv6Address $Ipv6IncrMode $Ipv6IncrStep]
                set InterfaceDescription [IncrInterfaceDescription $InterfaceDescription]
                set MacAddress [IncrMacStep $MacAddress $MacStep]
            }
        }
    }
    if {![info exists Ipv4Host] && ![info exists Ipv6Host] && ![info exists Ipv4v6Host]} {
	#旧方式，逐步替代
	if { $IpIncrNum > $Ipv6IncrNum } {
    	set maxstep $IpIncrNum
    } else {
        set maxstep $Ipv6IncrNum
    }
    for {set i 1} {$i <= $maxstep} {incr i} {
        set MacAddress [split $Mac -]
        if { $i <= $Ipv6IncrNum } { 
            #puts "Ipv6"
    	    interfaceIpV6 setDefault
    	    interfaceIpV6 config -ipAddress $Ipv6
    	    interfaceIpV6 config -maskWidth $Ipv6MaskWidth
    	    interfaceEntry addItem addressTypeIpV6
    	    set Ipv6 [IncrIpv6Step $Ipv6 $Ipv6IncrMode $Ipv6IncrStep]
	    }
	    if { $i <= $IpIncrNum } {
	        #puts "Ipv4"
        	interfaceIpV4 setDefault
        	interfaceIpV4 config -ipAddress $Ip
        	interfaceIpV4 config -maskWidth $MaskWidth
        	interfaceIpV4 config -gatewayIpAddress $GateWay
        	interfaceEntry addItem addressTypeIpV4
        	set Ip [IncrIpStep $Ip $IpIncrMode $IpIncrStep]
        }    	
    	interfaceEntry config -enable true
    	interfaceEntry config -description $InterfaceDescription
    	interfaceEntry config -macAddress  $MacAddress    	
    	interfaceTable addInterface
    	if { $IpIncrNum > 0 } {
        	interfaceEntry clearAllItems addressTypeIpV4
        }
        if { $Ipv6IncrNum > 0 } {
        	interfaceEntry clearAllItems addressTypeIpV6
        }
    	set Mac [IncrMacStep $Mac 1]
    }	
	interfaceTable write
	}
	#Tell the hardware about it,write port configuration to hardware
	protocolServer get $ChasId $Card $Port
	protocolServer config -enableArpResponse true
	protocolServer config -enablePingResponse true
	set res [protocolServer set $ChasId $Card $Port]
	#puts $res
	if { $Action == "set" } {
		ixWritePortsToHardware portlist
	}
	if { $Action == "change" } {
	    ixWriteConfigToHardware portlist
    }
}

################################
#
# SetIxiaArpProtocol : 配置IXIA协议端口模拟ARP协议报文
#                      注意：如果测试例中仅需要让交换机通过流量触发能够学习到大量的arp，
#                      则可以采用这种方法。并且事先不需要使用SetIxiaAsPC函数模拟IPv4主机。
# args: 
#      Host 100.1.1.222
#      Card 8
#      Port 1
#
#      DefaultGateway 20.1.1.1   ：该协议端口的网关，也是路由的下一跳地址
#	   FromIp 20.1.1.3           ：模拟的arp报文的第一个arp地址
#	   FromMac 00-00-00-12-05-00 ：对应第一个arp地址的mac地址
#	   NumAddress 1024           ：模拟连续arp报文的数量
#	   NetMask 24                ：arp报文的掩码长度
#
# return:
#
# addition:
#
# examples:
#      1、模拟200个连续arp，ip地址：200.1.1.2开始，掩码长度：24，网关：200.1.1.1，mac地址：00-00-00-00-00-01开始
#	   SetIxiaArpProtocol Host 192.168.1.253 Card 8 Port 2 DefaultGateway 200.1.1.1 \
#                         FromIp 200.1.1.2 FromMac 00-00-00-00-00-01 NumAddress 200 \
#                         NetMask 24
#
###############################
proc SetIxiaArpProtocol { args } {   
    set Host 100.1.1.222
	set Card 8
	set Port 1	
	set DefaultGateway 20.1.1.1
	set FromIp 20.1.1.3
	set FromMac 00-00-00-12-05-00
	set NumAddress 1024
	set NetMask 24
	
	array set arrArgs $args 	
  	foreach {para value} [array get arrArgs] {
		#puts "para=$para"
		#puts "value =$value"  	
		switch -exact -- $para {
		    Host {
		    	set Host $value
		    }
		    Card {
		   		set Card $value
		   	}
		   	Port { 
		   		set Port $value
		   	}
		   	DefaultGateway {
		   	    set DefaultGateway $value
		   	}
		   	FromIp {
		   	    set FromIp $value
		   	}
		   	FromMac {
		   	    set FromMac $value
		   	    set FromMac [split $FromMac -]
		   	}
		   	NumAddress {
		   	    set NumAddress $value
		   	}
		   	NetMask {
		   	    set NetMask $value
		   	}
		}
    }
	
    #set protocol server and ip address on testerp3
    package require IxTclHal
	ixInitialize $Host
	set Chas [ixGetChassisID $Host]
	set portList [list [list $Chas $Card $Port]]
	
    protocolServer setDefault
    protocolServer config -enableArpResponse true
    protocolServer config -enablePingResponse  true
    protocolServer set $Chas $Card $Port
    protocolServer write $Chas $Card $Port
    
    ipAddressTable setDefault
    ipAddressTable config -defaultGateway $DefaultGateway
    
    ipAddressTableItem setDefault
    ipAddressTableItem config -fromIpAddress $FromIp
    ipAddressTableItem config -fromMacAddress $FromMac
    ipAddressTableItem config -numAddresses $NumAddress
    ipAddressTableItem config -enableUseNetwork true
    ipAddressTableItem config -netMask $NetMask
    ipAddressTableItem set
    ipAddressTable addItem
    ipAddressTable set $Chas $Card $Port
    
    # Tell the hardware about it,write port configuration to hardware
    ixWritePortsToHardware portList
    
    # Wait for ixia port Link up
    idle_after 5000
    ixCheckLinkState portlist
    
    
}

################################
#
# SetIxiaRipProtocol : 配置IXIA协议端口模拟rip路由器
#                      注意：使用StartIxiaRip和StopIxiaRip函数发送和停止rip路由信息。
#                      并且事先不需要使用SetIxiaAsPC函数模拟IPv4主机。
# args: 
#      Host 100.1.1.222
#      Card 8
#      Port 1
#
#      RouterMac {00 00 00 12 04 00}  ：模拟rip路由器的mac地址
#	   RouterIp   20.1.1.2            ：模拟rip路由器的ip地址
#	   GateWay 20.1.1.1               ：模拟rip路由器的下一跳地址，一般为交换机对应接口的地址
#      # Basic parameters for the RIP router，这些参数一般不使用
#	   mask 255.255.255.0
#	   sendType ripMulticast
#	   receiveType ripReceiveVersion2
#	   updateInterval 10
#	   updateIntervalOffset 5	
#	   #Field define:    RangeIp  Prefix NumRoutes Metric NextHop Tag  发送rip路由信息
#	   #set routeRanges {{3.3.3.0   24         1       1    0.0.0.0  1}}
#	   DestIp 3.3.3.0
#	   Prefix 24
#	   NumRoutes 1
#	   Metric 1
#	   NextHop 0.0.0.0
#	   RouteTag 1
#
# return:
#
# addition:
#
# examples:
#      	1、模拟200个rip路由，ip地址：100.1.1.2，网关：100.1.1.1，mac地址：00-00-00-00-00-01，模拟路由信息为：ip地址：200.1.1.2，掩码长度：24，路由数量：200，跳数：2，下一跳：200.1.1.1。
#	    SetIxiaRipProtocol Host 192.168.1.253 Card 8 Port 2 RouterMac 00-00-00-00-00-01 \
#                          RouterIp 100.1.1.2 GateWay 100.1.1.1 \
#                          DestIp 200.1.1.2 Prefix 24 NumRoutes 200 Metric 2 NextHop 200.1.1.1 
#
###############################
#SetIxiaRipProtocol Host 172.16.1.249 Card 3 Port 2 RouterMac 00-00-00-00-00-01 RouterIp 10.1.1.2 GateWay 10.1.1.1 \
#                          DestIp 200.1.1.2 Prefix 24 NumRoutes 200 Metric 2 NextHop 200.1.1.1 
#SetIxiaRipProtocol Host 172.16.1.253 Card 8 Port 2 RouterMac 00-00-00-00-00-01 RouterIp 100.1.1.2 GateWay 100.1.1.1 \
#                   RouteRange {{RouteRange {{DestIp 200.1.1.0 Prefix 24 NumRoutes 10 Metric 1 NextHop 200.1.1.1 RouteTag 0} \
#                                            {DestIp 200.2.1.0 Prefix 24 NumRoutes 10 Metric 1 NextHop 200.2.1.1 RouteTag 0}} \
#                                SendType ripMulticast ReceiveType ripReceiveVersion2 UpdateInterval 10 UpdateIntervalOffset 5} \
#                               {RouteRange {{DestIp 300.1.1.0 Prefix 24 NumRoutes 10 Metric 1 NextHop 300.1.1.1 RouteTag 0}} \
#                                SendType ripMulticast ReceiveType ripReceiveVersion2 UpdateInterval 10 UpdateIntervalOffset 5}}
#SetIxiaRipProtocol Host 172.16.1.249 Card 3 Port 2 RouterMac 00-01-0f-01-00-01 RouterIp 10.1.1.2 GateWay 10.1.1.1 \
#                   RouteRange {{RouteRange {{DestIp 200.1.1.0 Prefix 24 NumRoutes 10 Metric 1 NextHop 200.1.1.1 RouteTag 0} \
#                                            {DestIp 200.2.1.0 Prefix 24 NumRoutes 10 Metric 1 NextHop 200.2.1.1 RouteTag 0}}}}
proc SetIxiaRipProtocol { args } {
	set Host 100.1.1.222
	set Card 8
	set Port 1
	set  RouterMac {00 00 00 12 04 00}
	set  RouterIp   20.1.1.2
	set  GateWay 20.1.1.1
    # Basic parameters for the RIP router
	set mask 255.255.255.0
	set sendType ripMulticast
	set receiveType ripReceiveVersion2
	set updateInterval 10
	set updateIntervalOffset 5	
	#Field define:    RangeIp  Prefix NumRoutes Metric NextHop Tag
	#set routeRanges {{3.3.3.0   24         1       1    0.0.0.0  1}}
	#scan [lindex $routeRanges 0] "%s %s %s %s %s %s"  myIp prefix numRoutes metric nextHop routeTag
	set DestIp 3.3.3.0
	set Prefix 24
	set NumRoutes 1
	set Metric 1
	set NextHop 0.0.0.0
	set RouteTag 0
	set InterfaceDescription "[format %02d $Card]:[format %02d $Port] - 1"
	
	array set arrArgs $args 	
	foreach {para value} [array get arrArgs] {
		#puts "para=$para"
		#puts "value =$value"  	
		switch -exact -- $para {
		    Host {
		    	set Host $value
		    	set Chas [ixGetChassisID $Host]
		    }
		    Card {
		   		set Card $value
		   	}
		   	Port { 
		   		set Port $value
		   	}
		   	RouterMac {
		   	    set RouterMac $value
		   	    set RouterMac [split $RouterMac -]
		   	}
		   	RouterIp {
		   	    set RouterIp $value
		   	}
		   	GateWay {
		   	    set GateWay $value
		   	}
		   	DestIp {
		   	    set DestIp $value
		   	}
		   	Prefix {
		   	    set Prefix $value
		   	}
		   	NumRoutes {
		   	    set NumRoutes $value
		   	}
		   	Metric {
		   	    set Metric $value
		   	}
		   	NextHop {
		   	    set NextHop $value
		   	}
		   	RouteTag {
		   	    set RouteTag $value
		   	}
		   	RouteRange {
		   		set RouteRange $value
		   	}
		}
	}
	
	set Chas [ixGetChassisID $Host]
	set  portList   [list [list $Chas $Card $Port]]	
	# Select the port and clear all defined routers

	# Set up the interface table for an IPv4 and IPv6 interface
	# on the port
	interfaceTable select $Chas $Card $Port
	interfaceTable clearAllInterfaces
	
	interfaceIpV4 setDefault
	interfaceIpV4 config -ipAddress $RouterIp
	interfaceIpV4 config -gatewayIpAddress $GateWay
	interfaceIpV4 config -maskWidth 24
	interfaceEntry addItem addressTypeIpV4
	
	interfaceEntry setDefault
	interfaceEntry config -enable true	
	interfaceEntry config -description $InterfaceDescription
	interfaceEntry config -macAddress $RouterMac
	interfaceTable addInterface
	interfaceTable write

	ripServer select $Chas $Card $Port
	ripServer clearAllRouters

	set routerId 1
	set rangeId 1	
	
	if [info exists RouteRange] {
		set maxrouterid [llength $RouteRange]
		#puts "maxrouterid == $maxrouterid"
		for {set i 0} {$i < $maxrouterid} {incr i} {
			set routerange [lindex $RouteRange $i]
			#puts $routerange
			array set routeritem $routerange
			if [info exists routeritem(RouteRange)] {
				set maxrangeid [llength $routeritem(RouteRange)]
				#puts "maxrangeid == $maxrangeid"
				set rangeId 1
				for {set j 0} {$j < $maxrangeid} {incr j} {
					#puts [lindex $routeritem(RouteRange) $j]
					array set rangeitem [lindex $routeritem(RouteRange) $j]
					ripRouteRange setDefault
					ripRouteRange config -enableRouteRange true
					if [info exists rangeitem(RouterTag)] {
						ripRouteRange config -routeTag $rangeitem(RouterTag)
					} else {
						ripRouteRange config -routeTag 0
					}
					if [info exists rangeitem(DestIp)] {
						ripRouteRange config -networkIpAddress $rangeitem(DestIp)
						#puts $rangeitem(DestIp)
					} else {
						ripRouteRange config -networkIpAddress 0.0.0.0
					}
					if [info exists rangeitem(Prefix)] {
						ripRouteRange config -networkMaskWidth $rangeitem(Prefix)
					} else {
						ripRouteRange config -networkMaskWidth 24
					}
					if [info exists rangeitem(NumRoutes)] {
						ripRouteRange config -numberOfNetworks $rangeitem(NumRoutes)
					} else {
						ripRouteRange config -numberOfNetworks 1
					}
					if [info exists rangeitem(NextHop)] {
						ripRouteRange config -nextHop $rangeitem(NextHop)
					} else {
						ripRouteRange config -nextHop 0.0.0.0
					}
					if [info exists rangeitem(Metric)] {
						ripRouteRange config -metric $rangeitem(Metric)
					} else {
						ripRouteRange config -metric 1
					}
					ripInterfaceRouter addRouteRange [format "routeRange%02d" $rangeId]
					incr rangeId
				}
			}  ;#else undo
			ripInterfaceRouter setDefault
			ripInterfaceRouter config -enableRouter true
			ripInterfaceRouter config -protocolInterfaceDescription $InterfaceDescription
			if [info exists routeritem(SendType)] {
				ripInterfaceRouter config -sendType $routeritem(SendType)
			} else {
				ripInterfaceRouter config -sendType ripMulticast
			}
			if [info exists routeritem(ReceiveType)] {
				ripInterfaceRouter config -receiveType $routeritem(ReceiveType)
			} else {
				ripInterfaceRouter config -receiveType ripReceiveVersion2
			}
			if [info exists routeritem(UpdateInterval)] {
				ripInterfaceRouter config -updateInterval $routeritem(UpdateInterval)
			} else {
				ripInterfaceRouter config -updateInterval 10
			}
			if [info exists routeritem(UpdateIntervalOffset)] {
				ripInterfaceRouter config -updateIntervalOffset $routeritem(UpdateIntervalOffset)
			} else {
				ripInterfaceRouter config -updateIntervalOffset 5
			}
			#puts "routerId == $routerId"
			ripServer addRouter [format "router%02d" $routerId]
			incr routerId
		}
	} else {
		##Defaultly the var:OSPFRouteLen is defined in the main progame
#	if  { [info exists "OSPFRouteLen"] } {
#	    set  numRoutes  $OSPFRouteLen  }	
		ripRouteRange setDefault
		ripRouteRange config -enableRouteRange true
		ripRouteRange config -routeTag $RouteTag
		ripRouteRange config -networkIpAddress $DestIp
		ripRouteRange config -networkMaskWidth $Prefix
		ripRouteRange config -numberOfNetworks $NumRoutes
		ripRouteRange config -nextHop $NextHop
		ripRouteRange config -metric $Metric
			
		# Create a name for each individual route range
		ripInterfaceRouter addRouteRange [format "routeRange%02d" $rangeId]
				
		# Now set the basic parameters for the router
		ripInterfaceRouter setDefault
		ripInterfaceRouter config -enableRouter true
		ripInterfaceRouter config -protocolInterfaceDescription $InterfaceDescription
		ripInterfaceRouter config -sendType $sendType
		ripInterfaceRouter config -receiveType $receiveType
		ripInterfaceRouter config -updateInterval $updateInterval
		ripInterfaceRouter config -updateIntervalOffset $updateIntervalOffset
		# And add the router to the ripServer with a unique ID
		ripServer addRouter [format "router%02d" $routerId]
	}	
	protocolServer get $Chas $Card $Port
	protocolServer config -enableRipService true
	protocolServer config -enableArpResponse true
	protocolServer config -enablePingResponse true
	protocolServer set $Chas $Card $Port
		
	# Send to the hardware
	ixWritePortsToHardware portList
	if [CheckLinkState $portList] {
		return 1
	} else {
		return 0
	}
}

proc CheckLinkState { porlist {timer 1000}} {
	for {set i 1} {$i < $timer} {incr i} {
		if ![ ixCheckLinkState [list portlist] ] {
	    	return 1
		} else {
			IdleAfter 1000
		}
	}
	return 0
}

################################
#
# SetIxiaOspfProtocol : 配置IXIA协议端口模拟ospf路由器
#                       注意：使用StartIxiaOspf和StopIxiaOspf函数发送和停止rip路由信息。
#                       并且事先不需要使用SetIxiaAsPC函数模拟IPv4主机。
# args: 
#      Host 100.1.1.222
#      Card 8
#      Port 1
#
#	   RouterMac {00 00 00 12 04 00}  ：模拟ospf路由器的mac地址
#	   RouterIp 20.1.1.2              ：模拟ospf路由器的ip地址
#	   GateWay 20.1.1.1               ：模拟ospf路由器的下一跳地址，一般为交换机对应接口的地址
#	   MaskWidth 16	                  ：模拟ospf路由器的掩码长度
#	   以下是发送ospf路由信息
#      FirstSubnetIp   {100.1.1.0}    
#	   ospfInterfaceNetworkType ospfBroadcast
#	   areaId 0
#	   Metric 1
#	   numberOfRoute 4000
#	   Prefix 24
#      HelloInterval 10
#      DeadInterval 40
#      RouteOrigin 0
#
# return:
#
# addition:
#
# examples:
#      		1、模拟200个rip路由，ip地址：100.1.1.2，网关：100.1.1.1，mac地址：00-00-00-00-00-01，模拟路由信息为：ip地址：200.1.1.2，掩码长度：24，路由数量：200，跳数：1。
#	        SetIxiaOspfProtocol Host 192.168.1.253 Card 8 Port 2 RouterMac 00-00-00-00-00-01 \
#                               RouterIp 100.1.1.2 GateWay 100.1.1.1 \
#                               FirstSubnetIp 200.1.1.2 Metric 1 numberOfRoute 200 Prefix 24 
#
#SetIxiaOspfProtocol Host 172.16.1.253 Card 8 Port 2 RouterMac 00-00-00-00-00-01 RouterIp 100.1.1.2 GateWay 100.1.1.1 \
#                   Routers {{Interface {AreaId 0 HelloInterval 10 DeadInterval 40 NetworkType ospfBroadcast Metric 10 \
#                                        RouteRanges {{Metric 10 NumberofRoutes 100 Prefix 24 FirstRoute 30.1.1.0 RouteOrigin ospfRouteOriginArea} \
#                                                     {Metric 10 NumberofRoutes 200 Prefix 24 FirstRoute 40.1.1.0 RouteOrigin ospfRouteOriginArea}}} \
#                             RouterId 8.2.0.0} \
#                            {Interface {AreaId 0 NetworkType ospfBroadcast \
#                                        RouteRanges {{NumberofRoutes 100 Prefix 24 FirstRoute 50.1.1.0 RouteOrigin ospfRouteOriginArea} \
#                                                     {NumberofRoutes 200 Prefix 16 FirstRoute 60.1.0.0 RouteOrigin ospfRouteOriginArea}}}}}
###############################
proc SetIxiaOspfProtocol { args } {
	set Host 100.1.1.222
	set Card 8
	set Port 1
	# The router being simulated on the port
	set RouterMac {00 00 00 12 04 00}
	set RouterIp 20.1.1.2
	set GateWay 20.1.1.1
#	set InterfaceName {MyPortInterface 2:2}
	set MaskWidth 16	
	#set interfaceIp     {100.1.1.0}
	#set interfaceIpMask {255.255.255.0}
	set FirstSubnetIp   {100.1.1.0}
	set ospfInterfaceNetworkType ospfBroadcast
	set areaId 0
	set Metric 1
	set numberOfRoute 4000
	set Prefix 24
	#added by xuyongc 2006-11-20
    set HelloInterval 10
    set DeadInterval 40
    set RouteOrigin 0     ;#0 : ospfRouteOriginArea ;  1 : ospfRouteOriginExternal ; 2 : ospfRouteOriginExternalType2
    #end of added by xuyongc 2006-11-20
    

	array set arrArgs $args 	
	foreach {para value} [array get arrArgs] {
		#puts "para=$para"
		#puts "value =$value"  	
		switch -exact -- $para {
		    Host {
		    	set Host $value
		    	set Chas [ixGetChassisID $Host]
		    }
		    Card {
		   		set Card $value
		   	}
		   	Port { 
		   		set Port $value
		   	}
		   	RouterMac {
		   	    set RouterMac $value
		   	    set RouterMac [split $RouterMac -]
		   	}
		   	RouterIp {
		   	    set RouterIp $value
		   	}
		   	GateWay {
		   	    set GateWay $value
		   	}	
		   	MaskWidth {
		   		set MaskWidth $value
		   	}
#		   	interfaceIp {
#		   	    set interfaceIp $value
#		   	}
#		   	interfaceIpMask {
#		   	    set interfaceIpMask $value
#		   	}
		   	FirstSubnetIp {
		   	    set FirstSubnetIp $value
		   	}
		   	areaId {
		   	    set areaId $value
		   	}
		   	Metric {
		   		set Metric $value
		   	}
		   	numberOfRoute {
		   	    set numberOfRoute $value
		   	}
		   	Prefix {
		   		set Prefix $value
		   	}
		   	HelloInterval {
		   	    set HelloInterval $value
		   	}
		   	DeadInterval {
		   	    set DeadInterval $value
		   	}
		   	RouteOrigin {
		   	    set RouteOrigin $value
		   	}
		   	Routers {
		   		set Routers $value
		   	}
		   	Ipv4Host {
		   		set Ipv4Host $value
		   	}
		}
	}
	
	set Chas [ixGetChassisID $Host]
	set  portList   [list [list $Chas $Card $Port]]
	set InterfaceDescription "[format %02d $Card]:[format %02d $Port] - 1"
	
	###########################################################
	# Set up the interface table for an IPv4 and IPv6 interface
	# on the port
	interfaceTable select $Chas $Card $Port
	interfaceTable clearAllInterfaces

	if [info exists Ipv4Host] {
        set Ipv4HostListNum [llength $Ipv4Host]
        for {set Ipv4HostListIndex 1} {$Ipv4HostListIndex <= $Ipv4HostListNum} {incr Ipv4HostListIndex} {
            set Ipv4HostListIndexInfo [lindex $Ipv4Host [expr $Ipv4HostListIndex - 1]]
            set Ipv4IncrMode ClassD
            set Ipv4IncrStep 1
            set Ipv4IncrNum 1
            set MacAddress 00-00-00-00-00-01
            set MacStep 1
            set VlanEnable false
            set VlanId 0
            set VlanPriority 0
            array set arrIpv4HostListIndexInfo $Ipv4HostListIndexInfo 	
          	foreach {para value} [array get arrIpv4HostListIndexInfo] {
        		switch -exact -- $para {
        		    InterfaceDescription {
        		        set InterfaceDescription $value
        		    }
        		    Ipv4Address {
        		        set Ipv4Address $value
        		    }
        		    Ipv4MaskWidth {
                        set Ipv4MaskWidth $value
        		    }
        		    GateWay {
        		        set GateWay $value
        		    }
        		    Ipv4IncrStep {
        		        set Ipv4IncrStep $value
        		    }
        		    Ipv4IncrMode {
        		        set Ipv4IncrMode $value
        		    }
        		    Ipv4IncrNum {
        		        set Ipv4IncrNum $value
        		    }
        		    MacAddress {
        		        set MacAddress $value
        		    }
        		    MacStep {
        		        set MacStep $value
        		    }
        		    VlanEnable {
        		        set VlanEnable $value
        		    }
        		    VlanId {
        		        set VlanId $value
        		    }
        		    VlanPriority {
        		        set VlanPriority $value
        		    }
        			default {
        		   		puts "Wrong para name:$para "
        		   		return -1	
        		   	}
        		}		
        	}
        	for {set i 1} {$i <= $Ipv4IncrNum} {incr i} {
        	    interfaceEntry clearAllItems addressTypeIpV6
                interfaceEntry clearAllItems addressTypeIpV4
                interfaceEntry setDefault
                set MacAddresstemp [split $MacAddress -]
        	    interfaceIpV4 setDefault
                interfaceIpV4 config -ipAddress $Ipv4Address
                interfaceIpV4 config -maskWidth $Ipv4MaskWidth
                interfaceIpV4 config -gatewayIpAddress $GateWay
                interfaceEntry addItem addressTypeIpV4
                interfaceEntry config -enable true
        	    interfaceEntry config -description $InterfaceDescription
        	    interfaceEntry config -macAddress  $MacAddresstemp
        	    interfaceEntry config -enableVlan $VlanEnable
                interfaceEntry config -vlanId $VlanId
                interfaceEntry config -vlanPriority $VlanPriority
        	    interfaceTable addInterface interfaceTypeConnected
                set Ipv4Address [IncrIpStep $Ipv4Address $Ipv4IncrMode $Ipv4IncrStep]
                set InterfaceDescription [IncrInterfaceDescription $InterfaceDescription]
                set MacAddress [IncrMacStep $MacAddress $MacStep]
            }
        }
    } else {
		interfaceIpV4 setDefault
		interfaceIpV4 config -ipAddress $RouterIp
		interfaceIpV4 config -gatewayIpAddress $GateWay
		interfaceIpV4 config -maskWidth $MaskWidth
		interfaceEntry addItem addressTypeIpV4
		
		interfaceEntry setDefault
		interfaceEntry config -enable true
		##Name the interface
		interfaceEntry config -description $InterfaceDescription
		interfaceEntry config -macAddress $RouterMac
		interfaceTable addInterface
		interfaceTable write
	}

	# Select port to operate
	ospfServer select $Chas $Card $Port
	# Clear all routers
	ospfServer clearAllRouters
	set InterfaceDescription "[format %02d $Card]:[format %02d $Port] - 1"
#SetIxiaRipProtocol Host 172.16.1.253 Card 8 Port 2 RouterMac 00-00-00-00-00-01 RouterIp 100.1.1.2 GateWay 100.1.1.1 \
#                   Routers {{Interface {AreaId 0 HelloInterval 10 DeadInterval 40 NetworkType ospfBroadcast Metric 10 \
#                                        RouteRanges {{Metric 10 NumberofRoutes 100 Prefix 24 FirstRoute 30.1.1.0 RouteOrigin ospfRouteOriginArea} \
#                                                     {Metric 10 NumberofRoutes 200 Prefix 24 FirstRoute 40.1.1.0 RouteOrigin ospfRouteOriginArea}}} \
#                             RouterId 8.2.0.0} \
#                            {Interface {AreaId 0 NetworkType ospfBroadcast \
#                                        RouteRanges {{NumberofRoutes 100 Prefix 24 FirstRoute 50.1.1.0 RouteOrigin ospfRouteOriginArea} \
#                                                     {NumberofRoutes 200 Prefix 16 FirstRoute 60.1.0.0 RouteOrigin ospfRouteOriginArea}}}}}
	if [info exists Routers] {
		set routersnum [llength $Routers]
		#puts "maxrouterid == $maxrouterid"
		for {set i 0} {$i < $routersnum} {incr i} {
			array set routers [lindex $Routers $i]
			if [info exists routers(Interface)] {
				array set interface $routers(Interface)
				# Configure the interface connecting the DUT
				ospfInterface setDefault
				ospfInterface config -enable true
				ospfInterface config -connectToDut true
				ospfInterface config -protocolInterfaceDescription $InterfaceDescription
				set InterfaceDescription [IncrInterfaceDescription $InterfaceDescription]
				if [info exists interface(AreaId)] {
					ospfInterface config -areaId $interface(AreaId)
				} else {
					ospfInterface config -areaId 0
				}
				if [info exists interface(HelloInterval)] {
					ospfInterface config -helloInterval $interface(HelloInterval)
				} else {
					ospfInterface config -helloInterval 10
				}
				if [info exists interface(DeadInterval)] {
					ospfInterface config -deadInterval $interface(DeadInterval)
				} else {
					ospfInterface config -deadInterval 40
				}
				if [info exists interface(NetworkType)] {
					ospfInterface config -networkType $interface(NetworkType)
				} else {
					ospfInterface config -networkType ospfBroadcast
				}
				if [info exists interface(Metric)] {
					ospfInterface config -metric $interface(Metric)
				} else {
					ospfInterface config -metric 10
				}
				#puts "routerId == $routerId"
				if [ospfRouter addInterface interface1] {
				    logMsg "Error in adding ospfInterface interface1"
				}
				if [info exists interface(RouteRanges)] {
					for {set k 1} {$k <= [llength $interface(RouteRanges)]} {incr k} {
						#puts [llength $interface(RouteRanges)]
						array set routeranges [lindex $interface(RouteRanges) [expr $k - 1]]
						#puts [lindex $interface(RouteRanges) [expr $k - 1]]
						ospfRouteRange setDefault
						ospfRouteRange config -enable true
						if [info exists routeranges(Metric)] {
							ospfRouteRange config -metric $routeranges(Metric)
						} else {
							ospfRouteRange config -metric 0
						}
						if [info exists routeranges(NumberofRoutes)] {
							ospfRouteRange config -numberOfNetworks $routeranges(NumberofRoutes)
						} else {
							ospfRouteRange config -numberOfNetworks 1
						}
						if [info exists routeranges(Prefix)] {
							ospfRouteRange config -prefix $routeranges(Prefix)
						} else {
							ospfRouteRange config -prefix 24
						}
						if [info exists routeranges(FirstRoute)] {
							ospfRouteRange config -networkIpAddress $routeranges(FirstRoute)
						} else {
							ospfRouteRange config -networkIpAddress 0.0.0.0
						}
						if [info exists routeranges(RouteOrigin)] {
							ospfRouteRange config -routeOrigin $routeranges(RouteOrigin)
						} else {
							ospfRouteRange config -routeOrigin ospfRouteOriginArea
						}
						# Add the ospf routeRange to the router
						if [ospfRouter addRouteRange routeRange$k] {
						    logMsg "Error in adding routeRange$k"
						}
					}
				}
			}
			# Configure ospf router
			ospfRouter setDefault
			if [info exists routers(RouterId)] {
				ospfRouter config -routerId $routers(RouterId)
			} else {
				ospfRouter config -routerId $Card.$Port.0.$i
			}
			ospfRouter config -enable true
			# Add the router to the server
			if [ospfServer addRouter router$i] {
			    logMsg "Error in adding router$i"
			}
		}		
	} else {	
		# Configure the interface connecting the DUT
		ospfInterface setDefault
		ospfInterface config -enable true
		ospfInterface config -connectToDut true
		ospfInterface config -protocolInterfaceDescription $InterfaceDescription
		ospfInterface config -areaId $areaId
		ospfInterface config -helloInterval $HelloInterval
		ospfInterface config -deadInterval $DeadInterval
		ospfInterface config -networkType $ospfInterfaceNetworkType
		ospfInterface config -metric 10
		# Add the ospf interface to the router
		if [ospfRouter addInterface interface1] {
		    logMsg "Error in adding ospfInterface interface1"
		}
		
		
		
#	# Configure an interface not connected to the DUT and using a
#	# Network Range
#	ospfInterface setDefault
#	ospfInterface config -enable true
#	ospfInterface config -connectToDut false
#	##ospfInterface config -protocolInterfaceDescription $InterfaceName2
#	ospfInterface config -ipAddress $interfaceIp
#	ospfInterface config -ipMask    $interfaceIpMask
#	ospfInterface config -areaId $areaId
#	ospfInterface config -networkType ospfBroadcast
#	ospfInterface config -metric 10
#	ospfInterface config -enableAdvertiseNetworkRange true
		
		
		# Configure the routeRange
		ospfRouteRange setDefault
		ospfRouteRange config -enable true
		ospfRouteRange config -metric $Metric
		ospfRouteRange config -numberOfNetworks $numberOfRoute
		ospfRouteRange config -prefix $Prefix
		ospfRouteRange config -networkIpAddress $FirstSubnetIp
		ospfRouteRange config -routeOrigin $RouteOrigin
		# Add the ospf routeRange to the router
		if [ospfRouter addRouteRange routeRange1] {
		    logMsg "Error in adding routeRange"
		}
		# Add the ospf interface to the routers
#	if [ospfRouter addInterface interface2] {
#	logMsg “Error in adding ospfInterface interface2”
#	}
		
		# Configure ospf router
		ospfRouter setDefault
		ospfRouter config -routerId $Card.$Port.0.0
		ospfRouter config -enable true
		
		# Add the router to the server
		if [ospfServer addRouter router1] {
		    logMsg "Error in adding router"
		}
	}
	
	# Let the protocol server respond to ARP, OSPF
	protocolServer get $Chas $Card $Port
	protocolServer config -enableOspfService true
	protocolServer config -enableArpResponse true
	protocolServer config -enablePingResponse true
	protocolServer set $Chas $Card $Port
	# Send the data to the hardware
	ixWriteConfigToHardware portList
	if [CheckLinkState $portList] {
		return 1
	} else {
		return 0
	}

}

################################
#
# SetIxiaBgpProtocol : 配置IXIA协议端口模拟bgp/bgp4+路由器
#                      注意：使用StartIxiaBGP和StopIxiaBGP函数发送和停止bgp/bgp4+路由信息。
#                      并且事先需要使用SetIxiaAsPC函数模拟IPv4/IPv6主机。
# args: 
#      Host 100.1.1.222
#      Card 8
#      Port 1
#
#	   IpType addressTypeIpV4  : Ipv4/Ipv6(addressTypeIpV4/addressTypeIpV6)
#	   FromPrefix 24
#	   ThruPrefix 24
#	   NumOfRoute 1
#	   Step 1	
#
#	   NeighborMode bgp4NeighborExternal : External/Internal(bgp4NeighborExternal/bgp4NeighborInternal)
#	   LocalIp 10.1.1.2
#	   DUTIp 10.1.1.1
#	   LocalAsNumber 200
#	   ServerAsNumber 100
#
# return:
#
# addition:
#
# examples:
#      	1、模拟200个bgp路由，ip地址：100.1.1.2，网关：100.1.1.1，mac地址：00-00-00-00-00-01，模拟路由信息为：ip地址：200.1.1.2，掩码长度：24，路由数量：200，本端和对端as都为100。
#	    SetIxiaAsPC Host 192.168.1.253 Card 8 Port 2 Ip 100.1.1.2 MaskWidth 24 \
#                   GateWay 100.1.1.1 Mac 00-00-00-00-00-01
#	    SetIxiaBgpProtocol Host 192.168.1.253 Card 8 Port 2 RouterIp 200.1.1.2 \
#                          IpType Ipv4 NumOfRoute 200 \
#                          NeighborMode bgp4NeighborInternal \
#                          LocalIp 100.1.1.2 DUTIp 100.1.1.1 \
#                          LocalAsNumber 100 ServerAsNumber 100
#	   2、模拟200个bgp路由，ip地址：2000:1::2，mac地址：00-00-00-00-00-01，模拟路由信息为：ip地址：3000:2::2，掩码长度：64，路由数量：200，本端和对端as都为100。
#	   SetIxiaAsPC Host 192.168.1.253 Card 8 Port 2 Ipv6 2000:1::2 MaskWidth 64 \
#                  Mac 00-00-00-00-00-01
#	   SetIxiaBgpProtocol Host 192.168.1.253 Card 8 Port 2 RouterIp 3000:2::2 \
#                         IpType Ipv6 NumOfRoute 200 \
#                         NeighborMode bgp4NeighborInternal \
#                         LocalIp 2000:1::2 DUTIp 2000:1::1 \
#                         LocalAsNumber 100 ServerAsNumber 100
#
###############################
proc SetIxiaBgpProtocol { args } {
	set Host 100.1.1.222	
	set Card 8
	set Port 1
	set RouteIp   20.1.1.2
	#IpType : Ipv4/Ipv6(addressTypeIpV4/addressTypeIpV6)
	set IpType addressTypeIpV4
	set FromPrefix 24
	set ThruPrefix 24
	set NumOfRoute 1
	set Step 1	
	#NeighborMode : External/Internal(bgp4NeighborExternal/bgp4NeighborInternal)
	set NeighborMode bgp4NeighborExternal
	set LocalIp 10.1.1.2
	set DUTIp 10.1.1.1
	set LocalAsNumber 200
	set ServerAsNumber 100
	#LinkFlap : true/false #added by caisy 2010-5-15
	set LinkFlap false
	set LinkFlapDownTime 0
	set LinkFlapUpTime 0
#	set RouterIp 10.1.1.2
#	set GateWay 10.1.1.1
#	set MaskWidth 16
#	set RouterMac 00-00-01-00-00-01
	
	array set arrArgs $args 	
	foreach {para value} [array get arrArgs] {
		#puts "para=$para"
		#puts "value =$value"  	
		switch -exact -- $para {
		    Host {
		    	set Host $value
		    }
		    Card {
		   		set Card $value
		   	}
		   	Port { 
		   		set Port $value
		   	}
		   	RouteIp {
		   	    set RouteIp $value
		   	}
		   	IpType {
		   	    if {$value == "Ipv4"} {
		   	        set IpType addressTypeIpV4
				} elseif {$value == "Ipv6"} {
					set IpType addressTypeIpV6
		   	    } else {
		   	    	set IpType $value
		   	    }
		   	}
		   	FromPrefix {
		   	    set FromPrefix $value
		   	}
		   	ThruPrefix {
		   	    set ThruPrefix $value
		   	}
		   	NumOfRoute {
		   	    set NumOfRoute $value
		   	}
		   	Step {
		   	    set Step $value
		   	}
		   	LocalIp {
		   	    set LocalIp $value
		   	}
		   	DUTIp {
		   	    set DUTIp $value
		   	}
		   	LocalAsNumber {
		   	    set LocalAsNumber $value
		   	}
		   	ServerAsNumber {
		   	    set ServerAsNumber $value
		   	}
		   	MaskWidth {
		   	    set MaskWidth $value
		   	}
		   	RouteRange {
		   	    set RouteRange $value
		   	}
		   	NeighborMode {
		   	    set NeighborMode $value
		   	}		 
		   	LinkFlap {
		   		set LinkFlap $value
		   	}
		   	LinkFlapDownTime {
		   		set LinkFlapDownTime $value
		   	}
		   	LinkFlapUpTime {
		   		set LinkFlapUpTime $value
		   	}
		}
	}
	set Chas [ixGetChassisID $Host]
	set  portList   [list [list $Chas $Card $Port]]
	#set RouterMac [split $RouterMac -]
	
	# Select the port and clear all defined routers
	bgp4Server select $Chas $Card $Port
	bgp4Server clearAllNeighbors
    bgp4Server setDefault        
    bgp4Server config -internalLocalAsNum $ServerAsNumber
    bgp4Server set
	
#	bgp4AsPathItem setDefault
#    bgp4AsPathItem config -enableAsSegment true
#    bgp4AsPathItem config -asList {100 200 300 }
#    bgp4AsPathItem config -asSegmentType bgpSegmentAsSequence
#	bgp4RouteItem addASPathItem
    # Configure the route range
    if [info exists RouteRange] {
    	set bgprouterangenum [llength $RouteRange]
    	array set arr $RouteRange
    	for {set bgpi 0} {$bgpi < $bgprouterangenum} {incr bgpi} {
    			set IpType addressTypeIpV4
				set FromPrefix 24
				set ThruPrefix 24
				set NumOfRoute 1
				set Step 1
			foreach {para value} [lindex $RouteRange $bgpi] {  	
				switch -exact -- $para {
				   	RouteIp {
				   	    set RouteIp $value
				   	}
				   	IpType {
				   	    if {$value == "Ipv4"} {
				   	        set IpType addressTypeIpV4
						} elseif {$value == "Ipv6"} {
							set IpType addressTypeIpV6
				   	    } else {
				   	    	set IpType $value
				   	    }
				   	}
				   	FromPrefix {
				   	    set FromPrefix $value
				   	}
				   	ThruPrefix {
				   	    set ThruPrefix $value
				   	}
				   	NumOfRoute {
				   	    set NumOfRoute $value
				   	}
				   	Step {
				   	    set Step $value
				   	}
				}
			}
			bgp4RouteItem setDefault
			if {$NeighborMode == "bgp4NeighborInternal"} {
				bgp4RouteItem config -asPathSetMode bgpRouteAsPathNoInclude
			}
			bgp4RouteItem config -enableLocalPref true
			bgp4RouteItem config -localPref 0
			bgp4RouteItem config -enableRouteRange true
			bgp4RouteItem config -networkAddress $RouteIp
		    bgp4RouteItem config -ipType $IpType
		    bgp4RouteItem config -fromPrefix $FromPrefix
		    bgp4RouteItem config -thruPrefix $ThruPrefix
			bgp4RouteItem config -numRoutes $NumOfRoute
		    bgp4RouteItem config -iterationStep $Step
			# Add the route range to the Neighbor
		    bgp4Neighbor addRouteRange "routeRange[expr {$bgpi+1}]"
    	}
    } else {
	    bgp4RouteItem setDefault
	    if {$NeighborMode == "bgp4NeighborInternal"} {
			bgp4RouteItem config -asPathSetMode bgpRouteAsPathNoInclude
		}
		bgp4RouteItem config -enableLocalPref true
		bgp4RouteItem config -localPref 0
		bgp4RouteItem config -enableRouteRange true
	    bgp4RouteItem config -networkAddress $RouteIp
	    bgp4RouteItem config -ipType $IpType
	    bgp4RouteItem config -fromPrefix $FromPrefix
	    bgp4RouteItem config -thruPrefix $ThruPrefix
	    bgp4RouteItem config -numRoutes $NumOfRoute
	    bgp4RouteItem config -iterationStep $Step
		# Add the route range to the Neighbor
	    bgp4Neighbor addRouteRange routeRange1
	}
#    bgp4RouteItem config -enableRouteFlap true
#    bgp4RouteItem config -routeFlapTime 1999
#    bgp4RouteItem config -routeFlapDropTime 1
#    bgp4RouteItem config -enableNextHop true
#    bgp4RouteItem config -nextHopIpAddress {0.0.0.0}
#    bgp4RouteItem config -nextHopIpType addressTypeIpV4
#    bgp4RouteItem config -nextHopMode 1
#    bgp4RouteItem config -nextHopSetMode bgpRouteNextHopSetSameAsLocalIp
#    bgp4RouteItem config -enableOrigin true
#    bgp4RouteItem config -originProtocol bgpOriginIGP
#    bgp4RouteItem config -enableLocalPref true
#    bgp4RouteItem config -localPref 10
#    bgp4RouteItem config -enableASPath true
#    bgp4RouteItem config -iterationStep 2
#    bgp4RouteItem config -asPathSetMode
#    bgpRouteAsPathIncludeAsSeq
	
	bgp4Neighbor setDefault
	bgp4Neighbor config -enable true
    bgp4Neighbor config -type $NeighborMode    
    bgp4Neighbor config -localIpAddress $LocalIp
    bgp4Neighbor config -rangeCount 1
    bgp4Neighbor config -dutIpAddress $DUTIp
    bgp4Neighbor config -ipType $IpType
#    bgp4Neighbor config -holdTimer 90
#    bgp4Neighbor config -updateInterval 0
#   changed by caisy
    bgp4Neighbor config -enableLinkFlap $LinkFlap 
    bgp4Neighbor config -linkFlapDownTime $LinkFlapDownTime 
    bgp4Neighbor config -linkFlapUpTime $LinkFlapUpTime 
    bgp4Neighbor config -localAsNumber $LocalAsNumber
#    bgp4Neighbor config -asNumMode bgp4AsNumModeFixed
    bgp4Neighbor config -enableBgpId true
    bgp4Neighbor config -bgpId "$Card.$Port.0.1"
    # And add the neighbor to the server
    bgp4Server addNeighbor neighbor1
    	
	
#	# Set up the interface table for an IPv4 and IPv6 interface
#	# on the port
#	interfaceTable select $Chas $Card $Port
#	interfaceTable clearAllInterfaces
#	
#	interfaceIpV4 setDefault
#	interfaceIpV4 config -ipAddress $LocalIp
#	interfaceIpV4 config -gatewayIpAddress $DUTIp
#	interfaceIpV4 config -maskWidth $MaskWidth
#	interfaceEntry addItem addressTypeIpV4
#	
#	interfaceEntry setDefault
#	interfaceEntry config -enable true
#	
#	interfaceEntry config -macAddress $RouterMac
#	interfaceTable addInterface
#	interfaceTable write
	
	
	protocolServer get $Chas $Card $Port
	protocolServer config -enableBgp4Service true
	protocolServer config -enableArpResponse true
	protocolServer config -enablePingResponse true
	protocolServer set $Chas $Card $Port
	
	
	# Send to the hardware
	ixWriteConfigToHardware portList
	ixCheckLinkState portList
	# And start RIP on the port
	#ixStartRip portList
	IdleAfter 5000

}

################################
#
# SetIxiaRipngProtocol : 配置IXIA协议端口模拟Ripng路由器
#                        注意：使用StartIxiaRipng和StopIxiaRipng函数发送和停止RIPng路由信息。
#                        并且事先需要使用SetIxiaAsPC函数模拟IPv6主机。
# args: 
#      Host 172.16.1.251
#      Card 4
#      Port 1
#
#       InterfaceMetric 0
#       ResponseMode ripngSplitHorizon    : ripngSplitHorizon/ripngNoSplitHorizon/ripngPrisonReverse
#       NetworkIpAddress 0:0:0:0:0:0:0:0
#       MaskWidth 64
#       NumberOfRoutes 1
#       NextHop 0:0:0:0:0:0:0:0
#       Metric 1
#       RouteTag 0
#       Step 1
#       #LoobackFlag & MulticastFlag only can config by ixiatcl
#       LoopbackFlag true
#       MulticastFlag true    
#       #variable of ripngRouter
#       RouterId 1
#       ReceiveType ripngIgnore   : ripngIgnore/ripngStore 
#       UpdateInterval 30
#       UpdateIntervalOffset 5
#       InterfaceMetricFlag false    
#       #variable of ripngServer
#       NumPerTimer 0
#       TimePeriod 0
#
# return:
#
# addition:
#
# examples:
#      1、模拟200个ripng路由，ip地址：2000:1::2，mac地址：00-00-00-00-00-01，模拟路由信息为：ip地址：3000:1::2，掩码长度：64，路由数量：200。
#	   SetIxiaAsPC Host 192.168.1.253 Card 8 Port 2 Ipv6 2000:1::2 MaskWidth 64 \
#                   Mac 00-00-00-00-00-01
#	   SetIxiaRipngProtocol Host 192.168.1.253 Card 8 Port 2 \
#                            NetworkIpAddress 3000:1::2:: MaskWidth 64 NumberOfRoutes 200
#
###############################
proc SetIxiaRipngProtocol { args } {
    
    #variable of ixia
    set Host 172.16.1.251
    set Card 4
    set Port 1
    #variable of ripngInterface
    set InterfaceMetric 0
    #set InterfaceDescription "$Card:0$Port"
    #ResponseMode : ripngSplitHorizon/ripngNoSplitHorizon/ripngPrisonReverse
    set ResponseMode ripngSplitHorizon    
    #variable of ripngRouterRange
    set NetworkIpAddress 0:0:0:0:0:0:0:0
    set MaskWidth 64
    set NumberOfRoutes 1
    set NextHop 0:0:0:0:0:0:0:0
    set Metric 1
    set RouteTag 0
    set Step 1
    #LoobackFlag & MulticastFlag only can config by ixiatcl
    set LoopbackFlag true
    set MulticastFlag true    
    #variable of ripngRouter
    set RouterId 1
    #ReceiveTyep : ripngIgnore/ripngStore 
    set ReceiveType ripngIgnore
    set UpdateInterval 30
    set UpdateIntervalOffset 5
    set InterfaceMetricFlag false    
    #variable of ripngServer
    set NumPerTimer 0
    set TimePeriod 0
    
	array set arrArgs $args 	
  	foreach {para value} [array get arrArgs] {
		#puts "para=$para"
		#puts "value =$value"  	
		switch -exact -- $para {
		    Host {
		    	set Host $value
		    }
		    Card {
		   		set Card $value
		   	}
		   	Port { 
		   		set Port $value
		   	}
		   	InterfaceDescription {
		   	    set InterfaceDescription $value
		   	}
		   	InterfaceMetric {
		   	    set InterfaceMetric $value
		   	}		   	
		   	ResponseMode {
		   	    set ResponseMode $value
		   	}
		   	NetworkIpAddress {
		   	    set NetworkIpAddress $value
		   	}
		   	MaskWidth {
		   	    set MaskWidth $value
		   	}
		   	NumberOfRoutes {
		   	    set NumberOfRoutes $value
		   	}
		   	NextHop {
		   	    set NextHop $value
		   	}
		   	Metric {
		   	    set Metric $value
		   	}
		   	RouteTag {
		   	    set RouteTag $value
		   	}
		   	Step {
		   	    set Step $value
		   	}
		   	LoopbackFlag {
		   	    set LoopbackFlag $value
		   	}
		   	MulticastFlag {
		   	    set MulticastFlag $value
		   	}
		   	RouterId {
		   	    set RouterId $value
		   	}
		   	ReceiveType {
		   	    set ReceiveType $value
		   	}
		   	UpdateInteval {
		   	    set UpdateInteval $value
		   	}
		   	UpdateIntevalOffset {
		   	    set UpdateIntevalOffset $value
		   	}
		   	InterfaceMetricFlag {
		   	    set InterfaceMetricFlag $value
		   	}		   	
		   	NumPerTimer {
		   	    set NumPerTimer $value
		   	}
		   	TimePeriod {
		   	    set TimePeriod $value
		   	}

			default {
		   		puts "Wrong para name:$para "
		   		return -1	
		   	}
		}		
	}
	package require IxTclHal
	ixInitialize $Host
	set ChasId [ixGetChassisID $Host]
	set portlist [list [list $ChasId $Card $Port]]
	
	if { [info exists InterfaceDescription] } {
	    
	} else {
	    set InterfaceDescription "[format %02d $Card]:[format %02d $Port] - 1"
	    #puts $InterfaceDescription
	}
#	if { [info exists RouterId] } {
#	    
#	} else {
#	    set RouterId "$Card.$Port.0.0"
#	    #puts $RouterId
#	}
	#Set up Ripng server to send reports
	ripngServer select $ChasId $Card $Port
	ripngServer clearAllRouters
	
	ripngInterface setDefault
    ripngInterface config -enable true
    ripngInterface config -protocolInterfaceDescription $InterfaceDescription
    ripngInterface config -interfaceMetric $InterfaceMetric	
    ripngInterface config -responseMode $ResponseMode
    ripngRouter addInterface interface1
    
    ripngRouteRange setDefault
    ripngRouteRange config -enable true
    ripngRouteRange config -networkIpAddress $NetworkIpAddress
	ripngRouteRange config -maskWidth $MaskWidth
	ripngRouteRange config -numRoutes $NumberOfRoutes
	ripngRouteRange config -nextHop $NextHop
	ripngRouteRange config -metric $Metric
	ripngRouteRange config -routeTag $RouteTag
	ripngRouteRange config -step $Step
	ripngRouteRange config -enableIncludeLoopback $LoopbackFlag
	ripngRouteRange config -enableIncludeMulticast $MulticastFlag
	ripngRouter addRouteRange routeRange1
	
	ripngRouter setDefault
	ripngRouter config -enable true
	ripngRouter config -routerId $RouterId
	ripngRouter config -receiveType $ReceiveType
	ripngRouter config -updateInterval $UpdateInterval
	ripngRouter config -updateIntervalOffset $UpdateIntervalOffset
	ripngRouter config -enableInterfaceMetric $InterfaceMetricFlag
	ripngServer addRouter router1
	
	ripngServer setDefault
	ripngServer config -numRoutes $NumPerTimer
	ripngServer config -timePeriod $TimePeriod
    ripngServer set
	
	#Start the protocol server for Arp and IGMP
	#protocolServer setDefault
	protocolServer get $ChasId $Card $Port
	protocolServer config -enableArpResponse true
	protocolServer config -enablePingResponse true
	protocolServer config -enableRipngService true
	protocolServer set   $ChasId $Card $Port
	ixWritePortsToHardware portlist
	IdleAfter 5000
}

################################
#
# SetIxiaOspfv3Protocol : 配置IXIA协议端口模拟Ospfv3路由器
#                         注意：使用StartIxiaOSPFv3和StopIxiaOSPFv3函数发送和停止OSPFv3路由信息。
#                         并且事先需要使用SetIxiaAsPC函数模拟IPv6主机。
# args: 
#      Host 100.1.1.222
#      Card 8
#      Port 1
#
#      AreaId 0
#       V6Bit 1
#       DeadInterval 40
#       HelloInterval 10
#       InterfaceType ospfV3InterfaceBroadcast  : P2P/broadcast(ospfV3InterfacePointToPoint/ospfV3InterfaceBroadcast)
#       InterfaceId -1
#       InstanceId 0
#    
#       RouteOrigin ospfV3RouteOriginArea  : anotherArea/externalType1/externalType2(ospfV3RouteOriginArea/ospfV3RouteOriginExternalType1/ospfV3RouteOriginExternalType2)
#       Metric 0
#       NumOfRoute 1
#       MaskWidth 64
#       NetworkIpAddress 0:0:0:0:0:0:0:0
#       IterationStep 1
#
# return:
#
# addition:
#
# examples:
#      	1、模拟200个ospfv3路由，ip地址：2000:1::2，mac地址：00-00-00-00-00-01，模拟路由信息为：ip地址：3000:1::2，areaid：0，instanceid：1，掩码长度：64，路由数量：200。
#	    SetIxiaAsPC Host 192.168.1.253 Card 8 Port 2 Ipv6 2000:1::2 MaskWidth 64 \
#                    Mac 00-00-00-00-00-01
#	    SetIxiaOspfv3Protocol Host 192.168.1.253 Card 8 Port 2 AreaId 0 InstanceId 1 \
#                              RouteOrigin externalType1 NetworkIpAddress 3000:1::2 \
#                              IterationStep 1 NumOfRoute 1 MaskWidth 64
#
###############################
proc SetIxiaOspfv3Protocol { args } {
	set Host 100.1.1.222
	set Card 8
	set Port 1
    set AreaId 0
    #option : 
#    set DCBit 0x20
#    set RBit 0x10
#    set NBit 0x08
#    set MCBit 0x04
#    set EBit 0x02
#    set V6Bit 0x01
    set V6Bit 1
    set DeadInterval 40
    set HelloInterval 10
    #set InterfaceDescription "$Card:0$Port"
    #InterfaceType : P2P/broadcast(ospfV3InterfacePointToPoint/ospfV3InterfaceBroadcast)
    set InterfaceType ospfV3InterfaceBroadcast
    set InterfaceId -1
    set InstanceId 0
    
    #RouteOrigin : anotherArea/externalType1/externalType2(ospfV3RouteOriginArea/ospfV3RouteOriginExternalType1/ospfV3RouteOriginExternalType2)
    set RouteOrigin ospfV3RouteOriginArea
    set Metric 0
    set NumOfRoute 1
    set MaskWidth 64
    set NetworkIpAddress 0:0:0:0:0:0:0:0
    set IterationStep 1   	
	
	#set RouterId "$Card.$Port.0.0"

	array set arrArgs $args 	
	foreach {para value} [array get arrArgs] {
		#puts "para=$para"
		#puts "value =$value"  	
		switch -exact -- $para {
		    Host {
		    	set Host $value
		    }
		    Card {
		   		set Card $value
		   	}
		   	Port { 
		   		set Port $value
		   	}
		   	AreaId {
		   	    set AreaId $value
		   	}
		   	V6Bit {
		   	    set V6Bit $value
		   	}
		   	DeadInterval {
		   	    set DeadInterval $value
		   	}
		   	HelloInterval {
		   	    set HelloInterval $value
		   	}
		   	InterfaceDescription {
		   	    set InterfaceDescription $value
		   	}
		   	InterfaceType {
		   	    if {$value == "P2P"} {
		   	        set InterfaceType ospfV3InterfacePointToPoint
		   	    }
		   	    if {$value == "Broadcast"} {
		   	        set InterfaceType ospfV3InterfaceBroadcast
		   	    }
		   	}
		   	InterfaceId {
		   	    set InterfaceId $value
		   	}
		   	InstanceId {
		   	    set InstanceId $value
		   	}
		   	RouteOrigin {
		   	    if {$value == "anotherArea"} {
		   	        set RouteOrigin ospfV3RouteOriginArea
		   	    }
		   	    if {$value == "externalType1"} {
		   	        set RouteOrigin ospfV3RouteOriginExternalType1
		   	    }
		   	    if {$value == "externalType2"} {
		   	        set RouteOrigin ospfV3RouteOriginExternalType2
		   	    }
		   	}
		   	Metric {
		   	    set Metric $value
		   	}
		   	NumOfRoute {
		   	    set NumOfRoute $value
		   	}
		   	MaskWidth {
		   	    set MaskWidth $value
		   	}
		   	NetworkIpAddress {
		   	    set NetworkIpAddress $value
		   	}
            IterationStep {
                set IterationStep $value
            }
            RouterId {
                set RouterId $value
            }
		}
	}
	
	set Chas [ixGetChassisID $Host]
	set portList [list [list $Chas $Card $Port]]
	if { [info exists InterfaceDescription] } {
	    
	} else {
	    set InterfaceDescription "[format %02d $Card]:[format %02d $Port] - 1"
	    #puts $InterfaceDescription
	}
	if { [info exists RouterId] } {
	    
	} else {
	    set RouterId "$Card.$Port.0.0"
	    #puts $RouterId
	}
		
	# Time to set up the OSPFV3 Server
	ospfV3Server select $Chas $Card $Port
	ospfV3Server clearAllRouters
	
	# Start by defining an interface for a router
    ospfV3Interface setDefault
    ospfV3Interface config -enable true
    ospfV3Interface config -areaId $AreaId
#    ospfV3Interface config -options [expr $::ospfV3InterfaceOptionEBit | $::ospfV3InterfaceOptionMCBit | $::ospfV3InterfaceOptionRBit]
    if { $V6Bit == 1 } {
        ospfV3Interface config -options 0x13
    }
    if { $V6Bit == 0 } {
        ospfV3Interface config -options 0x12
    }
    ospfV3Interface config -helloInterval $HelloInterval
    ospfV3Interface config -deadInterval $DeadInterval
    ospfV3Interface config -protocolInterfaceDescription "$InterfaceDescription"
    ospfV3Interface config -type $InterfaceType
    ospfV3Interface config -interfaceId $InterfaceId
    ospfV3Interface config -instanceId $InstanceId
    # Add the interface to the router
    ospfV3Router addInterface interface1
    
    # Now define a route range for the router
    ospfV3RouteRange setDefault
    ospfV3RouteRange config -enable true
    ospfV3RouteRange config -routeOrigin $RouteOrigin
    ospfV3RouteRange config -metric $Metric
    ospfV3RouteRange config -numRoutes $NumOfRoute
    ospfV3RouteRange config -iterationStep $IterationStep
    ospfV3RouteRange config -maskWidth $MaskWidth
    ospfV3RouteRange config -networkIpAddress $NetworkIpAddress
    # Add the route range to the router
    ospfV3Router addRouteRange routeRange1
    	
	# Finalize the OSPF router details
    ospfV3Router setDefault
    ospfV3Router config -routerId $RouterId
    ospfV3Router config -enable true
    ####ospfV3Router config -autoGenerateRouterLsa 0
    ospfV3Router config -disableAutoGenerateRouterLsa       false
    ospfV3Router config -disableAutoGenerateLinkLsa         false
    ospfV3Router config -enableDiscardLearnedLsas           false
    ospfV3Router config -maxNumLsaPerSecond                 1000
    # And add the router to the server
    ospfV3Server addRouter router1
    # Make sure to enable the protocol with the Protocol Server
#    protocolServer setDefault
    protocolServer config -enableArpResponse true
	protocolServer config -enablePingResponse true
    protocolServer config -enableOspfV3Service true
    protocolServer set $Chas $Card $Port
    ixWritePortsToHardware portList
	ixCheckLinkState portList
	IdleAfter 10000
	# And start ospf on the port

}

################################
#
# SetIxiaMulticastClient : 配置IXIA协议端口模拟ipv4组播客户端
#                          注意：使用TransmitIgmpJoin和TransmitIgmpLeave函数发送和停止igmp repoprt报文。
#                          并且事先需要使用SetIxiaAsPC函数模拟IPv4主机。
# args: 
#      Host 172.16.1.251
#      Card 4
#      Port 1
#
#      ClientIp 10.1.1.2   ：组播客户端地址
#      Group 224.1.1.1     ：客户端点播的组地址
#      GroupNum 1          ：连续点播的组地址数目
#
# return:
#
# addition:
#      函数修改后，可支持cpu卡，暂时只最对支持5个组，源地址只支持1个，递增步数只支持1
# examples:
#      1、模拟100.1.1.2主机点播225.1.1.1-225.1.1.5组播的igmp report，ip地址：100.1.1.2，网关：100.1.1.1，mac地址：00-00-00-00-00-01。
#	   SetIxiaAsPC Host 192.168.1.253 Card 8 Port 2 Ip 100.1.1.2 MaskWidth 24 \
#                   GateWay 100.1.1.1 Mac 00-00-00-00-00-01
#	   SetIxiaRipProtocol Host 192.168.1.253 Card 8 Port 2 ClientIp 100.1.1.2 Group 225.1.1.1 \
#                          GroupNum 5
#
###############################
#proc SetIxiaMulticastClient { args } {
#    set Host 172.16.1.251
#    set Card 4
#    set Port 1
#    set ClientIp 10.1.1.2
#    set Group 224.1.1.1
#    set GroupNum 1
#	array set arrArgs $args 	
#  	foreach {para value} [array get arrArgs] {
#		#puts "para=$para"
#		#puts "value =$value"  	
#		switch -exact -- $para {
#		    Host {
#		    	set Host $value
#		    }
#		    Card {
#		   		set Card $value
#		   	}
#		   	Port { 
#		   		set Port $value
#		   	}
#		   	ClientIp {
#		   		set ClientIp $value
#		   	}
#		   	Group {
#		   		set Group $value
#		   	}
#		   	GroupNum {
#		   	    set GroupNum $value
#		   	}
#			default {
#		   		puts "Wrong para name:$para "
#		   		return -1	
#		   	}
#		}		
#	}
#	package require IxTclHal
#	ixInitialize $Host
#	set ChasId [ixGetChassisID $Host]
#	set portlist [list [list $ChasId $Card $Port]]
#	#Set up IGMP server to send reports
#	igmpServer setDefault
#	igmpServer config -reportMode 1
#	igmpServer config -reportFrequency 120
#	igmpServer config -repeatCount 10
#	igmpServer set $ChasId $Card $Port
#		
#	#Set up IGMP table for group addresses
#	igmpAddressTable clear
#	igmpAddressTableItem setDefault
#	igmpAddressTableItem config -fromGroupAddress   $Group
#	igmpAddressTableItem config -fromClientAddress  $ClientIp
#	igmpAddressTableItem config -numGroupAddresses  $GroupNum
#	igmpAddressTableItem config -numClientAddresses 1
#	igmpAddressTableItem set
#	igmpAddressTable addItem
#	igmpAddressTable set $ChasId $Card $Port
#	
#	
#	#Start the protocol server for Arp and IGMP
#	#protocolServer setDefault
#	protocolServer config -enableArpResponse true
#	protocolServer config -enableIgmpQueryResponse true
#	protocolServer set   $ChasId $Card $Port
#	ixWritePortsToHardware portlist
#	IdleAfter 5000
#}
proc SetIxiaMulticastClient { args } {
    set Host 172.16.1.251
    set Card 4
    set Port 1
    set ClientIp 10.1.1.2
    set ClientNum 1 ;#目前支持5个
    set Group 224.1.1.1
    set GroupNum 1
    set Version 2
	array set arrArgs $args 	
  	foreach {para value} [array get arrArgs] {
		#puts "para=$para"
		#puts "value =$value"  	
		switch -exact -- $para {
		    Host {
		    	set Host $value
		    }
		    Card {
		   		set Card $value
		   	}
		   	Port { 
		   		set Port $value
		   	}
		   	ClientIp {
		   		set ClientIp $value
		   	}
		   	ClientNum {
		   		set ClientNum $value
		   	}
		   	Group {
		   		set Group $value
		   	}
		   	GroupNum {
		   	    set GroupNum $value
		   	}
		   	Group2 {
		   		set Group2 $value
		   	}
		   	GroupNum2 {
		   	    set GroupNum2 $value
		   	}
		   	Group3 {
		   		set Group3 $value
		   	}
		   	GroupNum3 {
		   	    set GroupNum3 $value
		   	}
		   	Group4 {
		   		set Group4 $value
		   	}
		   	GroupNum4 {
		   	    set GroupNum4 $value
		   	}
		   	Group5 {
		   		set Group5 $value
		   	}
		   	GroupNum5 {
		   	    set GroupNum5 $value
		   	}
		   	Version {
		   		set Version $value
		   	}
			default {
		   		puts "Wrong para name:$para "
		   		return -1	
		   	}
		}		
	}
	package require IxTclHal
	ixInitialize $Host
	set ChasId [ixGetChassisID $Host]
	set portlist [list [list $ChasId $Card $Port]]
	#Set up IGMP server to send reports
	if {[igmpVxServer select $ChasId $Card $Port]} {
		igmpServer setDefault
		igmpServer config -reportMode 1
		igmpServer config -reportFrequency 120
		igmpServer config -repeatCount 10
		igmpServer config -version $Version
		igmpServer set $ChasId $Card $Port
		
		#Set up IGMP table for group addresses
		igmpAddressTable clear
		igmpAddressTableItem setDefault
		igmpAddressTableItem config -fromGroupAddress   $Group
		igmpAddressTableItem config -fromClientAddress  $ClientIp
		igmpAddressTableItem config -numGroupAddresses  $GroupNum
		igmpAddressTableItem config -numClientAddresses 1
		igmpAddressTableItem set
		igmpAddressTable addItem
		for {set i 2} {$i <= $ClientNum} {incr i} {
			igmpAddressTableItem config -fromGroupAddress   [set Group[set i]]
			igmpAddressTableItem config -fromClientAddress  $ClientIp
			igmpAddressTableItem config -numGroupAddresses  [set GroupNum[set i]]
			igmpAddressTableItem config -numClientAddresses 1
			igmpAddressTableItem set
			igmpAddressTable addItem
		}
		igmpAddressTable set $ChasId $Card $Port

		#Start the protocol server for Arp and IGMP
		#protocolServer setDefault
		protocolServer config -enableArpResponse true
		protocolServer config -enableIgmpQueryResponse true
		protocolServer set   $ChasId $Card $Port
		ixWritePortsToHardware portlist
	} else {
		protocolServer config -enableIgmpQueryResponse true
        protocolServer set $ChasId $Card $Port
		igmpVxServer clearAllHosts
		igmpGroupRange config -enable true
		igmpGroupRange config -groupIpFrom $Group
		igmpGroupRange config -groupCount $GroupNum
		igmpHost addGroupRange group1
		for {set i 2} {$i <= $ClientNum} {incr i} {
			igmpGroupRange config -groupIpFrom  [set Group[set i]]
			igmpGroupRange config -groupCount  [set GroupNum[set i]]
			igmpHost addGroupRange group$i
		}
		igmpHost config -enable true
		igmpHost config -protocolInterfaceDescription "[format %02d $Card]:[format %02d $Port] - 1"
		igmpVxServer addHost host1
		igmpVxServer set
		igmpVxServer write
	}
	IdleAfter 5000
}	

################################
#
# SetIxiaMldProtocol : 配置IXIA协议端口模拟ipv6组播客户端v2版本
#                      注意：使用StartIxiaMld和StopIxiaMld函数发送和停止mld repoprt报文。
#                      并且事先需要使用SetIxiaAsPC函数模拟IPv6主机。
# args: 
#      Host 172.16.1.251
#      Card 4
#      Port 1
#
#      ClientIp 10.1.1.2   ：组播客户端地址
#      Group 224.1.1.1     ：客户端点播的组地址
#      GroupNum 1          ：连续点播的组地址数目
#
# return:
#
# addition:
#
# examples:
#      	1、模拟2000::2主机include方式点播来自{2009::2，ff3f::1}组播的mld report，版本为v2。
#	    SetIxiaAsPC Host 192.168.1.253 Card 8 Port 2 Ipv6 2000::2 MaskWidth 64 \
#                    Mac 00-00-00-00-00-01
#	    SetIxiaMldProtocol Host 192.168.1.253 Card 8 Port 2 \
#                           Group ff3f::1 GroupNum 1 IncrementStep 1 \
#                           SourceMode Include SourceIpList {2009::2} Version mldVersion2
#
###############################
#SetIxiaMldProtocol Host 172.16.1.253 Card 4 Port 7 \
#   MldHost {{Version mldVersion1 GroupInfo {{GroupIpFrom ff3f::1 GroupCount 2 IncrementStep 1} \
#                                            {GroupIpFrom ff4f::1 GroupCount 3 IncrementStep 2}}} \
#            {Version mldVersion2 GroupInfo {{GroupIpFrom ff4f::1 GroupCount 2 IncrementStep 1 SourceMode Include SourceIpList {{2000::1 1} {2001::1 2}}} \
#                                            {GroupIpFrom ff5f::1 GroupCount 3 IncrementStep 2 SourceMode Exclude SourceIpList {{2002::1 1} {2003::1 2}}} \
#                                           }}}

proc SetIxiaMldProtocol { args } {
    set Host 172.16.1.251
    set Card 4
    set Port 1
    set NumPerTimer 0
    set TimePeriod 0
#    set ClientIp 2019::1
    set EnableGeneralQuery true
    set EnableGroupSpecific true
    set EnableImmediateResponse false
    set Group ff1f::1
    set GroupNum 1
    set IncrementStep 1
    set SourceMode multicastSourceModeExclude
    set SourceIpList {2009::1 2010::1}
    #version : mldVersion1  mldVersion2
    set Version mldVersion2
	array set arrArgs $args 	
  	foreach {para value} [array get arrArgs] {
		#puts "para=$para"
		#puts "value =$value"  	
		switch -exact -- $para {
		    Host {
		    	set Host $value
		    }
		    Card {
		   		set Card $value
		   	}
		   	Port { 
		   		set Port $value
		   	}
		   	NumPerTimer {
		   	    set NumPerTimer $value
		   	}
		   	TimePeriod {
		   	    set TimePeriod $value
		   	}
		   	Group {
		   		set Group $value
		   	}
		   	GroupNum {
		   	    set GroupNum $value
		   	}
		   	IncrementStep {
		   	    set IncrementStep $value
		   	}
		   	SourceMode {
		   	    if {$value == "Include"} {
		   	        set SourceMode multicastSourceModeInclude
		   	    }
		   	    if {$value == "Exclude"} {
		   	        set SourceMode multicastSourceModeExclude
		   	    }
		   	}
            SourceIpList {
                set SourceIpList $value
            }
            Version {
                set Version $value
            }
            MldHost {
                set MldHost $value
            }
			default {
		   		puts "Wrong para name:$para "
		   		return -1	
		   	}
		}		
	}
	ixInitialize $Host
	set ChasId [ixGetChassisID $Host]
	set portlist [list [list $ChasId $Card $Port]]
	#Set up MLD server to send reports
	mldServer select $ChasId $Card $Port
    mldServer clearAllHosts
    if [info exists MldHost] {
        set MldHostNum [llength $MldHost]
        for {set MldHostIndex 1} {$MldHostIndex <= $MldHostNum} {incr MldHostIndex} {
            set InterfaceDescription "[format %02d $Card]:[format %02d $Port] - $MldHostIndex"
            set MldHostIndexInfo [lindex $MldHost [expr $MldHostIndex - 1]]
            #puts $MldHostIndexInfo
            array set arrMldHostIndexInfo $MldHostIndexInfo 	
          	foreach {para value} [array get arrMldHostIndexInfo] {
                switch -exact -- $para {
                    InterfaceDescription {
        		        set InterfaceDescription $value
        		    }
        		    Version {
        		        set Version $value
        		    }
        		    GroupInfo {
        		        set GroupInfo $value
        		    }
 	                default {
        		   		puts "Wrong para name:$para "
        		   		return -1	
        		   	}
        		}
            }
            set GroupInfoNum [llength $GroupInfo]
            for {set GroupInfoIndex 1} {$GroupInfoIndex <= $GroupInfoNum} {incr GroupInfoIndex} {
                set GroupInfoIndexInfo [lindex $GroupInfo [expr $GroupInfoIndex - 1]]
                #puts $GroupInfoIndexInfo
                set GroupCount 1
                set IncrementStep 1
                array set arrGroupInfoIndexInfo $GroupInfoIndexInfo 	
              	foreach {para value} [array get arrGroupInfoIndexInfo] {
            		switch -exact -- $para {
            		    GroupIpFrom {
            		   		set GroupIpFrom $value
            		   	}
            		   	GroupCount {
            		   	    set GroupCount $value
            		   	}
            		   	IncrementStep {
            		   	    set IncrementStep $value
            		   	}
            		   	SourceMode {
            		   	    if {$value == "Include"} {
            		   	        set SourceMode multicastSourceModeInclude
            		   	    }
            		   	    if {$value == "Exclude"} {
            		   	        set SourceMode multicastSourceModeExclude
            		   	    }
            		   	}
                        SourceIpList {
                            set SourceIpList $value
                        }
                        default {
            		   		puts "Wrong para name:$para "
            		   		return -1	
            		   	}
            		}		
            	}
            	if { $Version == "mldVersion2" || $Version == "Version2" || $Version == "V2" } {
                	for {set i 1} {$i <= [llength $SourceIpList]} {incr i} {
                	    mldSourceRange setDefault 
                        mldSourceRange config -sourceIpFrom [lindex [lindex $SourceIpList [expr $i - 1]] 0]
                        mldSourceRange config -count [lindex [lindex $SourceIpList [expr $i - 1]] 1]
                        # Add the source range to the group range
                        if [mldGroupRange addSourceRange source$i] {
                            logMsg "Error in adding sourceRange source$i"
                        } else {
                            logMsg "adding sourceRange source$i successful!"
                        }
                    }
                }
    	        # Configure groupRange
    	        mldGroupRange setDefault 
                mldGroupRange config -enable true
                mldGroupRange config -groupIpFrom $GroupIpFrom
                mldGroupRange config -groupCount $GroupCount
                mldGroupRange config -incrementStep $IncrementStep
                if { $Version == "mldVersion2" || $Version == "Version2" || $Version == "V2" } {
                    mldGroupRange config -sourceMode $SourceMode
                }
                # Add the group range to the host
                if [mldHost addGroupRange group$GroupInfoIndex] {
                    logMsg "Error adding groupRange group$GroupInfoIndex"
                } else {
                    logMsg "adding groupRange group$GroupInfoIndex successful!"
                }
            }
            # Configure host - assume interface exists
            mldHost setDefault 
            mldHost config -enable true
            mldHost config -protocolInterfaceDescription $InterfaceDescription
            if { $Version == "mldVersion2" || $Version == "Version2" || $Version == "V2" } {
                set Version mldVersion2
            }
            if { $Version == "mldVersion1" || $Version == "Version1" || $Version == "V1" } {
                set Version mldVersion1
            }    
            mldHost config -version $Version
            # Add the host to the server
            mldServer setDefault
    	    mldServer config -numGroups $NumPerTimer
    	    mldServer config -timePeriod $TimePeriod
            if [mldServer addHost host$MldHostIndex] {
                logMsg "Error adding host host$MldHostIndex"
            } else {
                logMsg "adding host host$MldHostIndex successful!"
            }
        }
    } else {       
    	set sourcenum [llength $SourceIpList]
    	#configure source range
    	for {set i 1} {$i <= $sourcenum} {incr i} {
            mldSourceRange config -sourceIpFrom [lindex $SourceIpList [expr $i - 1]]
            mldSourceRange config -count 1
            # Add the source range to the group range
            if [mldGroupRange addSourceRange source$i] {
                logMsg "Error in adding sourceRange"
            }
        }
        # Configure groupRange
        mldGroupRange config -enable true
        mldGroupRange config -groupIpFrom $Group
        mldGroupRange config -groupCount $GroupNum
        mldGroupRange config -incrementStep $IncrementStep
        mldGroupRange config -sourceMode $SourceMode
        
        # Add the group range to the host
        if [mldHost addGroupRange group1] {
            logMsg "Error adding groupRange group1"
        }

        # Configure host - assume interface exists
        mldHost config -enable true
        mldHost config -protocolInterfaceDescription "[format %02d $Card]:[format %02d $Port] - 1"
        mldHost config -version $Version
        mldHost config -enableGeneralQuery $EnableGeneralQuery
        mldHost config -enableGroupSpecific $EnableGroupSpecific
        mldHost config -enableImmediateResponse $EnableImmediateResponse 
        # Add the host to the server
        mldServer setDefault
    	mldServer config -numGroups $NumPerTimer
    	mldServer config -timePeriod $TimePeriod
        if [mldServer addHost host1] {
            logMsg "Error adding host"
        }
        # Send to the hardware
        mldServer set
        if [mldServer write] {
            logMsg "Error writing"
        }
	}
	#Start the protocol server for Arp and IGMP
	#protocolServer setDefault
	protocolServer get   $ChasId $Card $Port
	#protocolServer config -enableArpResponse true
	#protocolServer config -enablePingResponse true
	protocolServer config -enableMldService true
	protocolServer set   $ChasId $Card $Port
	#ixWritePortsToHardware portlist
	ixWriteConfigToHardware portlist
	IdleAfter 5000
}
proc SetIxiaMldv1Protocol { args } {
    set Host 172.16.1.251
    set Card 4
    set Port 1
    set NumPerTimer 0
    set TimePeriod 0
#    set ClientIp 2019::1
    set EnableGeneralQuery true
    set EnableGroupSpecific true
    set EnableImmediateResponse false
    set GroupNum 1
    set Group1 ff1f::1
    set GroupNum1 1
    set IncrementStep1 1
    set Group2 ff1f::2
    set GroupNum2 1
    set IncrementStep2 1
    set Group3 ff1f::3
    set GroupNum3 1
    set IncrementStep3 1

    #version : mldVersion1  mldVersion2
    set Version mldVersion1
	array set arrArgs $args 	
  	foreach {para value} [array get arrArgs] {
		#puts "para=$para"
		#puts "value =$value"  	
		switch -exact -- $para {
		    Host {
		    	set Host $value
		    }
		    Card {
		   		set Card $value
		   	}
		   	Port { 
		   		set Port $value
		   	}
		   	NumPerTimer {
		   	    set NumPerTimer $value
		   	}
		   	TimePeriod {
		   	    set TimePeriod $value
		   	}
            GroupNum {
                set GroupNum $value
            }
		   	Group1 {
		   		set Group1 $value
		   	}
		   	GroupNum1 {
		   	    set GroupNum1 $value
		   	}
		   	IncrementStep1 {
		   	    set IncrementStep1 $value
		   	}
		   	Group2 {
		   		set Group2 $value
		   	}
		   	GroupNum2 {
		   	    set GroupNum2 $value
		   	}
		   	IncrementStep2 {
		   	    set IncrementStep2 $value
		   	}
		   	Group3 {
		   		set Group3 $value
		   	}
		   	GroupNum3 {
		   	    set GroupNum3 $value
		   	}
		   	IncrementStep3 {
		   	    set IncrementStep3 $value
		   	}
            Version {
                set Version $value
            }
			default {
		   		puts "Wrong para name:$para "
		   		return -1	
		   	}
		}		
	}
	package require IxTclHal
	ixInitialize $Host
	set ChasId [ixGetChassisID $Host]
	set portlist [list [list $ChasId $Card $Port]]
	#set sourcenum [llength $SourceIpList]
	
	#Set up IGMP server to send reports
	mldServer setDefault
	mldServer select $ChasId $Card $Port
	mldServer config -numGroups $NumPerTimer
	mldServer config -timePeriod $TimePeriod
	mldServer clearAllHosts
	
	mldGroupRange config -enable true
    # Configure groupRange
    for {set i 1} {$i <= $GroupNum} {incr i} {        
        #set g Group[set i]
        #set gn GroupNum[set i]
        #set is IncrementStep[set i]
        mldGroupRange config -groupIpFrom [set Group[set i]]
        mldGroupRange config -groupCount [set GroupNum[set i]]
        mldGroupRange config -incrementStep [set IncrementStep[set i]]
        
        # Add the group range to the host
        if [mldHost addGroupRange group[set i]] {
            logMsg "Error adding groupRange group[set i]"
        }
    }

    # Configure host - assume interface exists
    mldHost config -enable true
    mldHost config -protocolInterfaceDescription "[format %02d $Card]:[format %02d $Port] - 1"
    mldHost config -version $Version
    mldHost config -enableGeneralQuery $EnableGeneralQuery
    mldHost config -enableGroupSpecific $EnableGroupSpecific
    mldHost config -enableImmediateResponse $EnableImmediateResponse 
    # Add the host to the server
    if [mldServer addHost host1] {
        logMsg "Error adding host"
    }
    # Send to the hardware
    mldServer set
    if [mldServer write] {
        logMsg "Error writing"
    }
	
	#Start the protocol server for Arp and IGMP
	#protocolServer setDefault
	protocolServer config -enableArpResponse true
	protocolServer config -enablePingResponse true
	protocolServer config -enableMldService true
	protocolServer set   $ChasId $Card $Port
	#ixWritePortsToHardware portlist
	ixWriteConfigToHardware portlist
	IdleAfter 5000
}

proc SetIxiaMulticastStream { args } {
	set StreamRateMode PercentRate    ;#PercentRate/Fps/Bps
	set StreamRate 100               ;#100/148810/76190476
	set SouIpNum 1
	set DesMacNum 1
	set DesIpNum 1
	set SouMac 00-00-00-00-00-01
	array set arrArgs $args 	
  	foreach {para value} [array get arrArgs] {
		#puts "para=$para"
		#puts "value =$value"  	
		switch -exact -- $para {
		    Host {
		    	set Host $value
		    }
		    Card {
		   		set Card $value
		   	}
		   	Port { 
		   		set Port $value
		   	}
		   	StreamRateMode {
		   	    set StreamRateMode $value
		   	}
		   	StreamRate {
		   		set StreamRate $value
		   	}
		   	SouMac {
		   	    set SouMac $value
		   	}
		   	DesMac {
		   		set DesMac $value
		   	}
		   	DesMacNum {
		   	    set DesMacNum $value
		   	}
		   	SouIp {
		   		set SouIp $value
		   	}
		   	SouIpNum {
		   	    set SouIpNum $value
		   	}
		   	SouMask {
		   		set SouMask $value
		   	}
		   	DesIp {
		   		set DesIp $value
		   	}
		   	DesIpNum {
		   	    set DesIpNum $value
		   	}
		   	DesMask {
		   		set DesMask $value
		   	}
			default {
		   		puts "Wrong para name:$para "
		   		return -1	
		   	}
		}
	}
	SetIxiaStream Host $Host Card $Card Port $Port StreamRateMode $StreamRateMode StreamRate $StreamRate SouMac $SouMac DesMac $DesMac DesNum $DesMacNum Protocl ipv4 SouIp $SouIp SouIpNum $SouIpNum SouMask $SouMask DesIp $DesIp DesIpNum $DesIpNum DesMask $DesMask
}










##################################################################################
# 函数名  :GetQosCount
# 功能描述:
# 参数:
#	 host 100.1.1.222
#	 card 8
#	 port 1
#     mode 说明:取qos队列的模式
#		     ipEthernetII 0
#			ip8023Snap 1
#			vlan 2
#			custom 3
#			ipPpp 4
#			ipCiscoHdlc 5
# 函数结果:返回一个列表，里面是8个队列的值
# 创建日期:2005.7.21
# 创建人  :GAOWEI
# 举例:GetQosCount 172.16.1.251 8 1 vlan 
#      GetQosCount 172.16.1.251 8 1 ipEthernetII
################################################################################
proc GetQosCount {host card rxPort mode} {
	package require IxTclHal
	set host $host
	ixInitialize $host
	set chas [ixGetChassisID $host]
	set portList [list [list $chas $card $rxPort]]
	set lret {}
	# Set up port for QoS Statistics
	
	# QoS statistics mode
	stat config -mode statQos
	stat set $chas $card $rxPort
	# Set up locations of where to find the information
	qos setup $mode
	qos set $chas $card $rxPort
	protocol setDefault
	protocol config -name mac
	protocol config -ethernetType ethernetII
	port set $chas $card $rxPort
	# Write config to hardware
	ixWritePortsToHardware portList
	
	# Get the 8 QoS statistics and print them
	stat get allStats $chas $card $rxPort
	#stat getRate allStats $chas $card $rxPort
	for {set i 0} {$i <= 7} {incr i} {
	   ixPuts -nonewline "Count of Qos$i = "
	   ixPuts [stat cget -qualityOfService$i]
	   lappend lret [stat cget -qualityOfService$i]
	}
	return $lret
}

proc GetQosRate {host card rxPort mode} {
	package require IxTclHal
	ixInitialize $host
	set chas [ixGetChassisID $host]
	set portList [list [list $chas $card $rxPort]]
	set lret {}
	# Set up port for QoS Statistics
	
	# QoS statistics mode
	stat config -mode statQos
	stat set $chas $card $rxPort
	# Set up locations of where to find the information
	qos setup $mode
	qos set $chas $card $rxPort
	protocol setDefault
	protocol config -name mac
	protocol config -ethernetType ethernetII
	port set $chas $card $rxPort
	# Write config to hardware
	ixWriteConfigToHardware portList
	IdleAfter 5000
	# Get the 8 QoS statistics and print them
	#stat get allStats $chas $card $rxPort
	stat getRate allStats $chas $card $rxPort
	for {set i 0} {$i <= 7} {incr i} {
	   ixPuts -nonewline "Rate of Qos$i = "
	   ixPuts [stat cget -qualityOfService$i]
	   lappend lret [stat cget -qualityOfService$i]
	}
	return $lret
}
proc CheckArpCount {host card port} {
	package require IxTclHal
	set host $host
	ixInitialize $host
	set chas [ixGetChassisID $host]
	set portList [list [list $chas $card $port]]

	#
	stat get allStats $chas $card $port
	#stat getRate allStats $chas $card $rxPort
	set request [stat cget -txArpRequest]
	set reply [stat cget -rxArpReply]
	ixPuts -nonewline "Count of ArpRequest = $request.\nCount of ArpReply = $reply.\n"
#    if { $request == $reply }     由于REQUEST可能会在传输中丢失，所以只判断是否收到REPLY
    if { $reply > 0 } {
        return 1
    } else {
        return 0
    }
}


proc SetNormalRate {host card rxPort} {
	package require IxTclHal
	ixInitialize $host
	set chas [ixGetChassisID $host]
	set portList [list [list $chas $card $rxPort]]
	
	# Normal statistics mode
	stat config -mode statNormal
	stat set $chas $card $rxPort
	port set $chas $card $rxPort
	# Write config to hardware
	ixWriteConfigToHardware portList
	IdleAfter 5000
}
##################################################################################
# 函数名  :SetQosCount
# 功能描述:
# 参数:
#	 host 100.1.1.222
#	 card 8
#	 port 1
#     mode 说明:取qos队列的模式
#		     ipEthernetII 0
#			ip8023Snap 1
#			vlan 2
#			custom 3
#			ipPpp 4
#			ipCiscoHdlc 5
# 函数结果:返回一个列表，里面是8个队列的值
# 创建日期:2005.7.21
# 创建人  :GAOWEI
# 举例:SetQosCount 172.16.1.251 8 1 vlan 
#      SetQosCount 172.16.1.251 8 1 ipEthernetII
################################################################################
proc SetQosCount {host card port mode} {
	package require IxTclHal
	set host $host
	ixInitialize $host
	set chas [ixGetChassisID $host]
	set card $card
	set rxPort $port
	set portList [list [list $chas $card $rxPort]]
	set lret {}
	# Set up port for QoS Statistics
	
	# QoS statistics mode
	stat config -mode statQos
	stat set $chas $card $rxPort
	# Set up locations of where to find the information
	qos setup $mode
	qos set $chas $card $rxPort
	protocol setDefault
	protocol config -name mac
	protocol config -ethernetType ethernetII
	port set $chas $card $rxPort
	# Write config to hardware
	ixWritePortsToHardware portList
	
}

##################################################################################
# 函数名  :ClearPortStats
# 功能描述:配置某一个端口的某一条流
#	 host 100.1.1.222
#	 card 8
#	 port 1
# 函数结果:
# 创建日期:2005.7.21
# 创建人  :GAOWEI
# 举例:ClearPortStats 172.16.1.251 8 1
################################################################################
proc ClearPortStats {host card port} {
	package require IxTclHal
	set host $host
	ixInitialize $host
	set chas [ixGetChassisID $host]
	ixClearPortStats $chas $card $port
}

proc GetOversizeFrames { chas card port } {
	stat get statOversize $chas $card $port
	set count [ stat cget -oversize ]
	return $count
}
	
	
#######################################################
#
#
#Qos公用函数
#目前支持的prop值为12345678，11111111，87654321
# 这个函数属临时:）
#返回的值为1或0
#######################################################
proc TestProp {qos0 qos1 qos2 qos3 qos4 qos5 qos6 qos7 prop} {	
	for {set i 0} {$i < 8} {incr i} {
		set qos$i [format "%f" [set qos$i]]
		set temp [set qos$i]
		if {$temp == 0} {
			return -1
		}	
	}
	if {$prop == 12345678} {
		set prop1 [expr ceil([expr $qos1/$qos0])]
		set prop2 [expr ceil([expr $qos2/$qos0])]
		set prop3 [expr ceil([expr $qos3/$qos0])]
		set prop4 [expr ceil([expr $qos4/$qos0])]
		set prop5 [expr ceil([expr $qos5/$qos0])]
		set prop6 [expr ceil([expr $qos6/$qos0])]
		set prop7 [expr ceil([expr $qos7/$qos0])]
		
		puts "prop1 = $prop1"
		puts "prop2 = $prop2"
		puts "prop3 = $prop3"
		puts "prop4 = $prop4"
		puts "prop5 = $prop5"
		puts "prop6 = $prop6"
		puts "prop7 = $prop7"

		set proportion [ expr $prop1==2 && $prop2==3 && $prop3==4 && $prop4==5 && $prop5==6 && $prop6==7 && $prop7==8]
		if {$proportion == 1} {
			return 1	
		} else {
			return 0
		}
	} elseif {$prop == 87654321} {
		set prop1 [expr ceil([expr $qos0/$qos7])]
		set prop2 [expr ceil([expr $qos1/$qos7])]
		set prop3 [expr ceil([expr $qos2/$qos7])]
		set prop4 [expr ceil([expr $qos3/$qos7])]
		set prop5 [expr ceil([expr $qos4/$qos7])]
		set prop6 [expr ceil([expr $qos5/$qos7])]
		set prop7 [expr ceil([expr $qos6/$qos7])]
		puts "prop1 = $prop1"
		puts "prop2 = $prop2"
		puts "prop3 = $prop3"
		puts "prop4 = $prop4"
		puts "prop5 = $prop5"
		puts "prop6 = $prop6"
		puts "prop7 = $prop7"
		set proportion [ expr $prop1==8 && $prop2==7 && $prop3==6 && $prop4==5 && $prop5==4 && $prop6==3 && $prop7==2]
		if {$proportion == 1} {
			return 1	
		} else {
			return 0
		}
	} elseif {$prop == 11111111} {
		set prop1 [expr ceil([expr $qos1/$qos0])]
		set prop2 [expr ceil([expr $qos2/$qos0])]
		set prop3 [expr ceil([expr $qos3/$qos0])]
		set prop4 [expr ceil([expr $qos4/$qos0])]
		set prop5 [expr ceil([expr $qos5/$qos0])]
		set prop6 [expr ceil([expr $qos6/$qos0])]
		set prop7 [expr ceil([expr $qos7/$qos0])]
		
		puts "prop1 = $prop1"
		puts "prop2 = $prop2"
		puts "prop3 = $prop3"
		puts "prop4 = $prop4"
		puts "prop5 = $prop5"
		puts "prop6 = $prop6"
		puts "prop7 = $prop7"

		set proportion [ expr $prop1==1 && $prop2==1 && $prop3==1 && $prop4==1 && $prop5==1 && $prop6==1 && $prop7==1]
		if {$proportion == 1} {
			return 1	
		} else {
			return 0
		}
	} else {
		puts "wrong para!"
		return 0
	}
}



##################################################################################
# 函数名  :GetDscp 
# 功能描述:
# 参数:
#	 host 100.1.1.222
#	 card 8
#	 port 1
#     vlanflag 0 截取的数据包不带vlantag; 1 截取的数据报文带vlantag
# 函数结果:报文中的dscp值
# 创建日期:2005.7.21
# 创建人  :GAOWEI
# 举例:GetDscp 172.16.1.251 8 1 1 
################################################################################
proc GetDscp {host card port {vlanflag 0}} {
	package require IxTclHal
	# Connect to chassis and get chassis ID
	set host $host
	ixInitialize $host
	set chas [ixGetChassisID $host]
	# with port 1 looped to port 2
	set card $card
	set port $port
	set rxPortList [list [list $chas $card $port]]
	#set offset of dscp
	if {$vlanflag == 0} {
		set index1 45
		set index2 46
	} else {
		set index1 57
		set index2 58
	}
	ixClearStats rxPortList
	ixStartCapture rxPortList
	capture get $chas $card $port
	set numFrames [capture cget -nPackets]
	ixPuts "$numFrames frames captured"
	if {$numFrames == 0} {
		return -1
	}
	captureBuffer get $chas $card $port 2 2
	
	# Note that the frame number starts at 1
	captureBuffer getframe 1
	# Get the actual frame data
	set data [captureBuffer cget -frame]

	# We’ll only look at the dscp
	set data [string range $data $index1 $index2]

	set dscp [expr 0x0$data / 4]		
	ixPuts "dscp = $dscp"
	return $dscp
}

##################################################################################
# 
# GetIpprecedence:捕捉接收端包中的Ip precedence值 
# 
# args:
#	  host 100.1.1.222
#	  card 8
#	  port 1
#     vlanflag 0 截取的数据包不带vlantag; 1 截取的数据报文带vlantag
#
# return:报文中的ip precedence值
# 
# addition:
#
# examples:
#     GetIpprecedence 172.16.1.251 8 1 1 
################################################################################
proc GetIpprecedence { host card port {vlanflag 0} } {
	package require IxTclHal
	# Connect to chassis and get chassis ID
	set host $host
	ixInitialize $host
	set chas [ixGetChassisID $host]
	# with port 1 looped to port 2
	set card $card
	set port $port
	set rxPortList [list [list $chas $card $port]]
	#set offset of dscp
	if {$vlanflag == 0} {
		set index1 45
		set index2 46
	} else {
		set index1 57
		set index2 58
	}
	ixClearStats rxPortList
	ixStartCapture rxPortList
	capture get $chas $card $port
	set numFrames [capture cget -nPackets]
	ixPuts "$numFrames frames captured"
	if {$numFrames == 0} {
		return -1
	}
	captureBuffer get $chas $card $port 2 2
	
	# Note that the frame number starts at 1
	captureBuffer getframe 1
	# Get the actual frame data
	set data [captureBuffer cget -frame]
	# We’ll only look at the dscp
	set data [string range $data $index1 $index2]
	set ipprecedence [expr 0x0$data / 32]		
	ixPuts "ipprecedence = $ipprecedence"
	return $ipprecedence
}

##################################################################################
# 函数名  :GetTos
# 功能描述:
# 参数:
#	 host 100.1.1.222
#	 card 8
#	 port 1
#     vlanflag 0 截取的数据包不带vlantag; 1 截取的数据报文带vlantag
# 函数结果:报文中的tos值
# 创建日期:2005.7.21
# 创建人  :GAOWEI
# 举例:GetTos 172.16.1.251 8 1 1 
################################################################################
proc GetTos {host card port {vlanflag 0}} {
	package require IxTclHal
	# Connect to chassis and get chassis ID
	set host $host
	ixInitialize $host
	set chas [ixGetChassisID $host]
	# with port 1 looped to port 2
	set card $card
	set port $port
	set rxPortList [list [list $chas $card $port]]
	#set offset of dscp
	if {$vlanflag == 0} {
		set index1 45
		set index2 46
	} else {
		set index1 57
		set index2 58
	}
	ixClearStats rxPortList
	ixStartCapture rxPortList
	capture get $chas $card $port
	set numFrames [capture cget -nPackets]
	ixPuts "$numFrames frames captured"
	if {$numFrames == 0} {
		return -1
	}
	captureBuffer get $chas $card $port 2 2
	
	# Note that the frame number starts at 1
	captureBuffer getframe 1
	# Get the actual frame data
	set data [captureBuffer cget -frame]
	# We’ll only look at the dscp
	set data [string range $data $index1 $index2]
	set Tos [expr ( 0x0$data & 30 ) / 2]   ;#modified by liangdong		
	ixPuts "Tos = $Tos"
	return $Tos
}

##################################################################################
# 函数名 : GetUserPriority 
# 功能描述:
# 参数:
#	 host 100.1.1.222
#	 card 8
#	 port 1
# 函数结果:报文中的userPriority值
# 创建日期:2005.7.21
# 创建人  :GAOWEI
# 举例:GetUserPriority 172.16.1.251 8 1 1 
################################################################################
proc GetUserPriority {host card port} {
	package require IxTclHal
	# Connect to chassis and get chassis ID
	set host $host
	ixInitialize $host
	set chas [ixGetChassisID $host]
	# with port 1 looped to port 2
	set card $card
	set port $port
	set rxPortList [list [list $chas $card $port]]
	
	ixClearStats rxPortList
	ixStartCapture rxPortList
	capture get $chas $card $port
	set numFrames [capture cget -nPackets]
	if {$numFrames == 0} {
		return -1
	}
	ixPuts "$numFrames frames captured"
	captureBuffer get $chas $card $port 2 2
	
	# Note that the frame number starts at 1
	captureBuffer getframe 1
	# Get the actual frame data
	set data [captureBuffer cget -frame]
	# We’ll only look at the dscp
	set data [string range $data 42 42]
	set UserPriority [expr 0x0$data / 2]		
	ixPuts "UserPriority = $UserPriority"
	return $UserPriority
}


#############################################################
#用来设置ospfv3的协议
#参数说明: 
#set hostname      连接的ixia测试仪ip 
#set card          所需要设置的卡编号
#set port          端口编号
#PortIpv6Address   端口ipv6地址
#PortIpv6Mask      端口ipv6的掩码
#RouterIpv6Address 模拟路由的地址
#RouterIpv6Mask    模拟路有的掩码
#RouterNum         模拟路有的数量
#举例: 
#SetOspfv3Server 100.1.1.117 16 2 3002:0000:0000:0000:0000:0000:0000:2 64 33:3333:3333:3 12 123
#edit by gaowei 2006.8.7
###############################################################
proc SetOspfv3Server {HostName Card Port PortIpv6Address PortIpv6Mask RouterIpv6Address RouterIpv6Mask RouterNum} {
	set card $Card
	set port $Port
	set PortIpv6Address [split $PortIpv6Address :]
	set RouterIpv6Address [split $RouterIpv6Address :]
	package req IxTclHal
	ixInitialize $HostName
	set chassis [chassis cget -id]
	set portList [list [list $chassis $card $port]]
	# Reset port to factory defaults
	port setFactoryDefaults $chassis $card $port
	# Set up an interface entry for a single IPv6 address
	interfaceTable select $chassis $card $port
	interfaceTable clearAllInterfaces
	interfaceEntry clearAllItems addressTypeIpV6
	interfaceEntry clearAllItems addressTypeIpV4
	
	interfaceIpV6 config -ipAddress $PortIpv6Address
	interfaceIpV6 config -maskWidth $PortIpv6Mask
	interfaceEntry addItem addressTypeIpV6
	interfaceEntry setDefault
	
	interfaceEntry config -enable true
	interfaceEntry config -description {1 - 67:01 -EFC1:0:0:0:0:0:0:0/64}
	interfaceEntry config -macAddress {00 00 0A 54 65 35}
	interfaceTable addInterface
	ixWritePortsToHardware portList
	# Time to set up the OSPFv3 Server
	ospfV3Server select $chassis $card $port
	ospfV3Server clearAllRouters
	# Start by defining an interface for a router
	ospfV3Interface setDefault
	ospfV3Interface config -enable true
	ospfV3Interface config -areaId 0
	#ospfV3Interface config -options [expr $::ospfV3InterfaceOptionEBit | \
	 #                             $::ospfV3InterfaceOptionMCBit | $::ospfV3InterfaceOptionRBit]
	ospfV3Interface config -helloInterval 10
	ospfV3Interface config -deadInterval 40
	ospfV3Interface config -protocolInterfaceDescription {1 - 67:01 -EFC1:0:0:0:0:0:0:0/64}
	ospfV3Interface config -interfaceId 0
	# Add the interface to the router
	ospfV3Router addInterface interface1
	# Now define a route range for the router
	ospfV3RouteRange setDefault
	ospfV3RouteRange config -enable true
	ospfV3RouteRange config -routeOrigin ospfV3RouteOriginExternalType1
	ospfV3RouteRange config -metric 4
	ospfV3RouteRange config -numRoutes $RouterNum
	ospfV3RouteRange config -maskWidth $RouterIpv6Mask
	ospfV3RouteRange config -networkIpAddress $RouterIpv6Address
	# Add the route range to the router
	ospfV3Router addRouteRange routeRange1
	# Create one each of the different LSA types
	# Create a Router LSA - start with defining an interface
	ospfV3LsaRouterInterface setDefault
	ospfV3LsaRouterInterface config -interfaceId {10.0.0.0}
	ospfV3LsaRouterInterface config -neighborInterfaceId {2.0.0.0}
	ospfV3LsaRouterInterface config -neighborRouterId {8.0.0.0}
	ospfV3LsaRouterInterface config -type ospfV3LsaRouterInterfaceVirtual
	ospfV3LsaRouterInterface config -metric 9
	# Add the interface to the Router LSA
	ospfV3LsaRouter addInterface
	# And another
	ospfV3LsaRouterInterface setDefault
	ospfV3LsaRouterInterface config -interfaceId {22.0.0.0}
	ospfV3LsaRouterInterface config -neighborInterfaceId {3.0.0.0}
	ospfV3LsaRouterInterface config -neighborRouterId {9.0.0.0}
	ospfV3LsaRouterInterface config -type ospfV3LsaRouterInterfaceTransit
	ospfV3LsaRouterInterface config -metric 45
	ospfV3LsaRouter addInterface
	# Now define the remaining bits of the Router LSA
	ospfV3LsaRouter setDefault
	ospfV3LsaRouter config -enable false
	ospfV3LsaRouter config -linkStateId {10.0.0.0}
	ospfV3LsaRouter config -advertisingRouterId {0.0.0.90}
	ospfV3LsaRouter config -options [expr $::ospfV3LsaOptionNBit | $::ospfV3LsaOptionRBit | \
	                                      $::ospfV3LsaOptionDCBit]
	ospfV3LsaRouter config -enableVBit false
	ospfV3LsaRouter config -enableEBit true
	ospfV3LsaRouter config -enableBBit true
	ospfV3LsaRouter config -enableWBit false
	# Add the Router LSA to the user LSA group
	#ospfV3UserLsaGroup addUserLsa userLsa1 ospfV3LsaRouter
	# Now create a Network LSA
	ospfV3LsaNetwork setDefault
	ospfV3LsaNetwork config -enable false
	ospfV3LsaNetwork config -linkStateId {10.0.0.2}
	ospfV3LsaNetwork config -advertisingRouterId {2.0.0.92}
	ospfV3LsaNetwork config -options $::ospfV3LsaOptionDCBit
	ospfV3LsaNetwork config -neighborRouterIdList { 9.0.0.0 13.0.0.1 17.0.0.2 21.0.0.3 \
	                                       25.0.0.4 29.0.0.5 33.0.0.6 37.0.0.7 41.0.0.8 45.0.0.9}
	# Add the Network LSA to the user LSA group
	ospfV3UserLsaGroup addUserLsa userLsa2 ospfV3LsaNetwork
	# Create an Inter Area Prefix LSA
	#ospfV3LsaInterAreaPrefix setDefault
	ospfV3LsaInterAreaPrefix config -enable true
	ospfV3LsaInterAreaPrefix config -linkStateId {10.0.0.4}
	ospfV3LsaInterAreaPrefix config -advertisingRouterId {4.0.0.94}
	ospfV3LsaInterAreaPrefix config -numLsaToGenerate 1
	ospfV3LsaInterAreaPrefix config -incrementLinkStateIdBy {8.0.0.0}
	ospfV3LsaInterAreaPrefix config -prefixLength 45
	ospfV3LsaInterAreaPrefix config -prefixOptions [expr $::ospfV3PrefixOptionMCBit | \
	                                    $::ospfV3PrefixOptionPBit]
	ospfV3LsaInterAreaPrefix config -incrementPrefixBy 78
	ospfV3LsaInterAreaPrefix config -prefixAddress {100:0:0:0:0:0:0:0}
	# Add the Inter Area Prefix LSA to the User LSA group
	#ospfV3UserLsaGroup addUserLsa userLsa3
	#ospfV3LsaInterAreaPrefix
	# Create an Inter Area Router LSA
	ospfV3LsaInterAreaRouter setDefault
	ospfV3LsaInterAreaRouter config -enable true
	ospfV3LsaInterAreaRouter config -linkStateId {10.0.0.6}
	ospfV3LsaInterAreaRouter config -advertisingRouterId {6.0.0.96}
	ospfV3LsaInterAreaRouter config -numLsaToGenerate 1
	ospfV3LsaInterAreaRouter config -incrementLinkStateIdBy {8.0.0.0}
	ospfV3LsaInterAreaRouter config -destinationRouterId {7.6.0.0}
	ospfV3LsaInterAreaRouter config -incrementDestRouterIdBy {0.9.0.1}
	ospfV3LsaInterAreaRouter config -options [expr $::ospfV3LsaOptionV6Bit | \
	                          $::ospfV3LsaOptionNBit | $::ospfV3LsaOptionRBit]
	ospfV3LsaInterAreaRouter config -metric 78
	# Add the Inter Area Router LSA to the user group
	ospfV3UserLsaGroup addUserLsa userLsa4 ospfV3LsaInterAreaRouter
	# Create an AS External LSA
	ospfV3LsaAsExternal setDefault
	ospfV3LsaAsExternal config -enable true
	ospfV3LsaAsExternal config -linkStateId {10.0.0.8}
	ospfV3LsaAsExternal config -advertisingRouterId {8.0.0.98}
	ospfV3LsaAsExternal config -numLsaToGenerate 78
	ospfV3LsaAsExternal config -incrementLinkStateIdBy {8.0.0.0}
	ospfV3LsaAsExternal config -incrementPrefixBy 25
	ospfV3LsaAsExternal config -prefixLength 128
	ospfV3LsaAsExternal config -prefixOptions [expr $::ospfV3PrefixOptionLABit | \
	                                                $::ospfV3PrefixOptionPBit]
	ospfV3LsaAsExternal config -prefixAddress {545:0:0:0:0:0:0:0}
	ospfV3LsaAsExternal config -metric 10
	ospfV3LsaAsExternal config -enableEBit false
	ospfV3LsaAsExternal config -enableTBit false
	ospfV3LsaAsExternal config -enableFBit true
	ospfV3LsaAsExternal config -referencedLinkStateId {9.3.0.0}
	ospfV3LsaAsExternal config -externalRouteTag {7.8.0.0}
	ospfV3LsaAsExternal config -referencedType 1
	ospfV3LsaAsExternal config -forwardingAddress {245:0:0:0:0:0:0:0}
	# Add the AS External LSA to the user LSA group
	ospfV3UserLsaGroup addUserLsa userLsa5 ospfV3LsaAsExternal
	# Create a Link LSA, start by adding two address prefixes
	# First prefix
	ospfV3IpV6Prefix setDefault
	ospfV3IpV6Prefix config -incrementBy 8
	ospfV3IpV6Prefix config -length 19
	ospfV3IpV6Prefix config -options [expr $::ospfV3PrefixOptionMCBit | \
	                                  $::ospfV3PrefixOptionPBit]
	ospfV3IpV6Prefix config -address {2352:3:0:0:0:0:0:0}
	# Add the prefix to the Link LSA
	ospfV3LsaLink addPrefix
	# Second prefix
	ospfV3IpV6Prefix setDefault
	ospfV3IpV6Prefix config -incrementBy 9
	ospfV3IpV6Prefix config -length 7
	ospfV3IpV6Prefix config -options $::ospfV3PrefixOptionNUBit
	ospfV3IpV6Prefix config -address {35:0:0:0:0:0:0:0}
	# Add the prefix to the Link LSA
	ospfV3LsaLink addPrefix
	# Now the rest of the Link LSA contents
	ospfV3LsaLink setDefault
	ospfV3LsaLink config -enable true
	ospfV3LsaLink config -linkStateId {10.0.0.10}
	ospfV3LsaLink config -advertisingRouterId {10.0.0.100}
	ospfV3LsaLink config -numLsaToGenerate 65
	ospfV3LsaLink config -incrementLinkStateIdBy {0.8.0.0}
	ospfV3LsaLink config -options [expr $::ospfV3LsaOptionRBit | \
	                                    $::ospfV3LsaOptionDCBit]
	ospfV3LsaLink config -linkLocalAddress {0:77:0:0:0:0:0:0}
	ospfV3LsaLink config -priority 8
	# Add the Link LSA to the user LSA group
	ospfV3UserLsaGroup addUserLsa userLsa6 ospfV3LsaLink
	# Add an Intra Area Prefix LSA
	# Start with defining two address prefixes
	ospfV3IpV6Prefix setDefault
	ospfV3IpV6Prefix config -incrementBy 9
	ospfV3IpV6Prefix config -length 12
	ospfV3IpV6Prefix config -options [expr $::ospfV3PrefixOptionMCBit | \
	                                        $::ospfV3PrefixOptionPBit]
	ospfV3IpV6Prefix config -address {55:0:0:0:0:0:0:0}
	# Add the prefix to the LSA
	ospfV3LsaIntraAreaPrefix addPrefix
	ospfV3IpV6Prefix setDefault
	ospfV3IpV6Prefix config -incrementBy 78
	ospfV3IpV6Prefix config -length 25
	ospfV3IpV6Prefix config -options 0
	ospfV3IpV6Prefix config -address {5668:0:0:0:0:0:0:0}
	# Add the prefix to the LSA
	ospfV3LsaIntraAreaPrefix addPrefix
	# The rest of the options for the Intra Area Prefix LSA
	ospfV3LsaIntraAreaPrefix setDefault
	ospfV3LsaIntraAreaPrefix config -enable true
	ospfV3LsaIntraAreaPrefix config -linkStateId {10.0.0.12}
	ospfV3LsaIntraAreaPrefix config -advertisingRouterId {12.0.0.102}
	ospfV3LsaIntraAreaPrefix config -numLsaToGenerate 1
	ospfV3LsaIntraAreaPrefix config -incrementLinkStateIdBy {0.0.0.0}
	ospfV3LsaIntraAreaPrefix config -referencedType 1
	ospfV3LsaIntraAreaPrefix config -referencedLinkStateId {0.0.0.0}
	ospfV3LsaIntraAreaPrefix config -referencedRouterId {0.0.0.0}
	# Add the Intra Area Prefix LSA to the user LSA group
	ospfV3UserLsaGroup addUserLsa userLsa7 ospfV3LsaIntraAreaPrefix
	# Now finalize the details about the user LSA group
	ospfV3UserLsaGroup setDefault
	ospfV3UserLsaGroup config -enable false
	ospfV3UserLsaGroup config -areaId 10
	ospfV3UserLsaGroup config -description {}
	# And add the group to the router
	ospfV3Router addUserLsaGroup userLsaGroup1
	# Finalize the OSPF router details
	ospfV3Router setDefault
	ospfV3Router config -routerId {11.2.0.0}
	ospfV3Router config -enable true
	#ospfV3Router config -autoGenerateRouterLsa 0
	ospfV3Router config -enableDiscardLearnedLsas false
	# And add the router to the server
	ospfV3Server addRouter router1
	# Make sure to enable the protocol with the Protocol Server
	protocolServer setDefault
	protocolServer config -enableOspfV3Service true
	protocolServer set $chassis $card $port
	ixWritePortsToHardware portList
	#ixCheckLinkState portList
	# Now start the OSPFv3 simulation
	#ixStartOspfV3 portList
}

#proc StartOspfv3 {HostName card port} {
#	package req IxTclHal
#	ixInitialize $HostName
#	set chassis [chassis cget -id]
#	set portList [list [list $chassis $card $port]]
#	set portList [list [list $chassis $card $port]]
#	ixStartOspfV3 portList
#}
#proc StopOspfv3 {HostName card port} {
#	package req IxTclHal
#	ixInitialize $HostName
#	set chassis [chassis cget -id]
#	set portList [list [list $chassis $card $port]]
#	set portList [list [list $chassis $card $port]]
#	ixStopOspfV3 portList
#}

proc StartIxiaOspfv3 { portlist } {
    if [ixStartOspfV3 [list portlist] ] {
    		return -code error
	}
	IdleAfter 1000
}


proc StopIxiaOspfv3 { portlist } {
    if [ixStopOspfV3 [list portlist] ] {
    		return -code error
	}
	IdleAfter 1000
}

proc SetScheduledTransmitTime { portlist timer } {
	if [ixSetScheduledTransmitTime [list portlist] $timer] {
		ixPuts $::ixErrorInfo
	}
}

proc ClearScheduledTransmitTime { portlist } {
	if [ixClearScheduledTransmitTime [list portlist] ] {
		ixPuts $::ixErrorInfo
	}
}

######################################################################
#
# StartTransmit: 封装了Ixia的发包函数
#
# return: 无
# 
# examples:
#           StartTransmit $portList
######################################################################
#proc StartTransmit { portlist } {
#    if [ ixStartTransmit [list portlist] ] {
#    		return -code error
#	}
#	#IdleAfter 1000
#}

#proc StartTransmit { portlist {streamnum 0} } {
#    set portnum [llength $portlist]
#    #puts $portnum
#    for {set i 0} {$i < $portnum} {incr i} {
#    	set portvar [list [lindex $portlist $i]]
#    	#puts $portvar
#    	set chas [lindex [lindex $portvar 0] 0]
#        set card [lindex [lindex $portvar 0] 1]
#        set port [lindex [lindex $portvar 0] 2]
#
#        if [CheckLinkState $portvar] {
#        
#	        #puts "$chas:$card:$port"
#	        if { $streamnum == 0 } {
#	            if [ ixStartTransmit portvar ] {
#	        	    return -code error
#	    	    }
#	    	    #puts aaa
#	            stat getRate statBytesSent $chas $card $port
#	     	    set rate [stat cget -bytesSent]
#	     	    #puts "rate = $rate"
#	        	while { $rate == 0 } {
#	        	    Wait 100
#	        	    if [ ixStartTransmit portvar ] {
#	            		return -code error
#	        	    }
#	        	    stat getRate statBytesSent $chas $card $port
#	         	    set rate [stat cget -bytesSent]
#	         	    #puts "rate = $rate"
#	         	}
#	        } else {
#	            stat get statFramesSent $chas $card $port
#	            set beforesent [stat cget -framesSent]
#	            if [ ixStartTransmit portvar ] {
#	        	    return -code error
#	    	    }
#	    	    Wait 1000
#	    	    stat getRate statBytesSent $chas $card $port
#	     	    set rate [stat cget -bytesSent]
#	     	    while { $rate > 0 } {
#	        	    Wait 100
#	        	    stat getRate statBytesSent $chas $card $port
#	         	    set rate [stat cget -bytesSent]
#	         	}
#	         	stat get statFramesSent $chas $card $port
#	            set aftersent [stat cget -framesSent]
#	     	    while { [expr $aftersent - $beforesent] != $streamnum } {
#	     	        stat get statFramesSent $chas $card $port
#	                set beforesent [stat cget -framesSent]
#	                if [ ixStartTransmit portvar ] {
#	            	    return -code error
#	        	    }
#	        	    Wait 1000
#	        	    stat getRate statBytesSent $chas $card $port
#	         	    set rate [stat cget -bytesSent]
#	         	    while { $rate > 0 } {
#	            	    Wait 100
#	            	    stat getRate statBytesSent $chas $card $port
#	             	    set rate [stat cget -bytesSent]
#	             	}
#	             	stat get statFramesSent $chas $card $port
#	                set aftersent [stat cget -framesSent]
#	            }
#	        }
#
#        } else {
#        	continue
#        }
#    }
#    return 1      
#}
proc StartTransmit { portlist {streamnum 0} } {
    set portnum [llength $portlist]
    #puts $portnum
    set res 0
    for {set i 0} {$i < $portnum} {incr i} {
    	set portvar [list [lindex $portlist $i]]
    	#puts $portvar
    	set chas [lindex [lindex $portvar 0] 0]
        set card [lindex [lindex $portvar 0] 1]
        set port [lindex [lindex $portvar 0] 2]

        if [CheckLinkState $portvar] {
        	for {set j 0} {$j < 10} {incr j} {
	        	if [ ixStartTransmit portvar ] {
	        	    PrintRes Print "the card $card port $port can not send stream"
	    	    } else {
	    	    	set res [expr $res + 1]
	    	    	break
	    	    }
	    	}
        } else {
        	PrintRes Print "the card $card port $port not up"
        	continue
        }
    }
    return $res   ;#res值代表有几个端口的流发送成功   
}
#proc StartTransmit { portlist } {
#    set chas [lindex $portlist 0]
#    set card [lindex $portlist 1]
#    set port [lindex $portlist 2]
#    if [ ixStartTransmit [list portlist] ] {
#    	return -code error
#	}
#	stat getRate statBytesSent $chas $card $port
# 	set rate [stat cget -bytesSent]
#	while { $rate == 0 } {
#	    IdleAfter 1000
#	    if [ ixStartTransmit [list portlist] ] {
#    		return -code error
#	    }
#	    stat getRate statBytesSent $chas $card $port
# 	    set rate [stat cget -bytesSent]
# 	}
#	#IdleAfter 1000
#}

######################################################################
#
# StopTransmit: 封装了Ixia的停止发包函数
#
# return: 无
# 
# examples:
#           StopTransmit $portList
######################################################################
proc StopTransmit { portlist } {
    if [ ixStopTransmit [list portlist] ] {
    		return -code error
	}
	#IdleAfter 1000
}

######################################################################
#
# TransmitIgmpJoin: 封装了Ixia的igmp join函数
#
# return: 无
# 
# examples:
#           TransmitIgmpJoin $portList
######################################################################
proc TransmitIgmpJoin { portlist } {
    if [ ixTransmitIgmpJoin [list portlist] ] {
    		return -code error
	}
	#IdleAfter 1000
}

proc TransmitArpRequest { portlist } {
    if [ ixTransmitArpRequest [list portlist] ] {
    		return -code error
	}
	#IdleAfter 1000
}
proc ClearArpTable { portlist } {
	if [ ixClearArpTable [list portlist] ] {
    	return -code error
	}
}
#CheckArpIpMac $chasId $Card1 $Port1 13.1.1.105 $cpumacs3
proc CheckArpIpMac { chas card port ip mac } {
# Port1: Get the ARP table, get the first entry and print the entry
	arpServer get $chas $card $port
	if {[arpServer getFirstEntry]} \
	{
	ixPuts "Port 1: No ARP table entries"
	}
	arpAddressTableEntry get
	set ipi [arpAddressTableEntry cget -ipAddress]
	set maca [arpAddressTableEntry cget -macAddress]
	#ixPuts "Port 1: $ipi = $maca"
	regsub -all " " $maca "-" maca
	set maca [string toupper $maca]
	PrintRes Print "Get arp table of $chas $card $port is : $ipi,$maca."
	if { $ipi == $ip && $maca == $mac } {
		return 1
	} else {
		return 0
	}
}

######################################################################
#
# TransmitIgmpLeave: 封装了Ixia的停止发包函数
#
# return: 无
# 
# examples:
#           TransmitIgmpLeave $portList
######################################################################
proc TransmitIgmpLeave { portlist } {
    if [ ixTransmitIgmpLeave [list portlist] ] {
    		return -code error
	}
	#IdleAfter 1000
}

######################################################################
#
# StartCapture: 封装了Ixia的开始抓包函数
#
# return: 无
# 
# examples:
#           StartCapture $portList
######################################################################
proc StartCapture { portlist } {
	#ixClearStats [list portlist]
    if [ ixStartCapture [list portlist] ] {
        return -code error
	}
	Wait 500
}

######################################################################
#
# StopCapture: 封装了Ixia的停止抓包函数
#
# return: 无
# 
# examples:
#           StopCapture $portList
######################################################################
proc StopCapture { portlist } {
    if [ ixStopCapture [list portlist] ] {
		return -code error
	}
	#IdleAfter 1000
}

######################################################################
#
# CheckTransmitDone: 封装了Ixia的检查端口是否停止发包函数
#
# return: 1 端口已经停止发包
#         其它: 出现错误
# 
# examples:
#           CheckTransmitDone $portList
######################################################################
proc CheckTransmitDone { portlist } {
    if {[ ixCheckTransmitDone [list portlist] ] == 1} {
		return -code error
	} else {
	    return 1
	}
	#IdleAfter 1000
}

#################################################################
#
#  CheckStreamPairFull:测试端口速率
#
#   args:
#          chas1, port1, card1:端口1的chas, port, card
#          chas2, port2, card2:端口2的chas, port, card
#   return: 1:速率不符合要求
#           0:速率符合要求
###########################################################
proc CheckStreamPairFull {chas1 card1 port1 chas2 card2 port2} {
    stat getRate statBytesSent $chas1 $card1 $port1
 	set bsr [stat cget -bytesSent]
 	stat getRate statBytesReceived $chas2 $card2 $port2
 	set  brr [stat cget -bytesReceived]
 	if {$bsr != 0} {
 		append bsr ".0"
 		if {[expr $brr/$bsr] > 0.9 } {
 			PrintRes Print "$card2:$port2 bytes received rate [expr $brr/$bsr], OK"
 		} else {
 			PrintRes Print "$card2:$port2 bytes received rate [expr $brr/$bsr], FAILED"
 		}
 	} else {
 		 PrintRes Print "$card1:$port1 bytes send rate is zero, FAILED"
 		 return 1
	}
	return 0
} 

##################################################################
##
##  AddInterfaceToIxiaPort:设置IXIA端口地址
##
##   args:
##          chas, port, card:端口1的chas, port, card
##          ipAddr: IP地址
##          ipGateWay:网关
##          maskWidth:掩码
##          macAddr:MAC地址
##   return: 
##             无
##   Example : AddInterfaceToIxiaPort  1 5 1 20.1.1.2 20.1.1.1 24 00-00-00-00-00-01
############################################################
proc AddInterfaceToIxiaPort { chas card port ipAddr ipGateWay maskWidth macAddr } {
    
    regsub -all {\-} $macAddr " "  macAddr
    set  pl   [list [list $chas $card $port]]
    
    interfaceTable select $chas $card $port
    interfaceTable clearAllInterfaces
    
    interfaceIpV4 setDefault
    interfaceIpV4 config -ipAddress $ipAddr
    interfaceIpV4 config -gatewayIpAddress $ipGateWay
    interfaceIpV4 config -maskWidth $maskWidth
    interfaceEntry addItem addressTypeIpV4
    
    interfaceEntry setDefault
    interfaceEntry config -enable true
    
    interfaceEntry config -macAddress $macAddr
    interfaceTable addInterface
    interfaceTable write
    
    protocolServer get $chas $card $port
    protocolServer config -enableArpResponse true
    protocolServer set $chas $card $port
    
    ixWritePortsToHardware pl
    
    idle_after 8000
}

proc GetNumFrames { chas card port } {
    capture get $chas $card $port
	set numFrames [capture cget -nPackets]
	return $numFrames 
}

proc GetTTLofPacket { chas card port } {
	
    set counter 0   ;#内部使用的计数器
    
    # Get the number of frames captured
	capture get $chas $card $port
	set numFrames [capture cget -nPackets]
	#Limit the number of checked packets to 1000 
	if { $numFrames == 0 } {
        return {-1 -1}
	}
	if { $numFrames > 100} {
           set numFrames 100
	}

	set character ""
	captureBuffer get $chas $card $port 1 $numFrames
    for {set i 1} {$i <= $numFrames} {incr i} {
        # Note that the frame number starts at 1
        captureBuffer getframe $i
        set data [captureBuffer cget -frame]
		if { $data == "" } {
			continue
		}
		set type [string range $data 36 40]
	    if  { $type == "81 00" } {
	        set type [string range $data 48 52]
	        set ttl [string range $data 78 79]
	    } else {
	    	set ttl [string range $data 66 67]
	    }
	    if { $type != "08 00" } {
	    	#not ip packet
	    	continue
	    } else {
	    	if { $ttl == "" } {
	    		continue
	    	} else {
	    		lappend ttllist [format %d 0x0$ttl]
	    	}
	    }
	}
	set ttllist [lsort -integer -increasing $ttllist]
	return [list [lindex $ttllist 0] [lindex $ttllist end]]	    
}

#函数GetHopLimitofPacket对抓到的前100个包取出hop-limit字段进行判断，返回最大值和最小值
proc GetHopLimitofPacket { chas card port } {
	
    set counter 0   ;#内部使用的计数器
    
    # Get the number of frames captured
	capture get $chas $card $port
	set numFrames [capture cget -nPackets]
	#Limit the number of checked packets to 1000 
	if { $numFrames == 0 } {
        return {-1 -1}
	}
	if { $numFrames > 100} {
        set numFrames 100
	}

	set character ""
	#对hoplimitlist赋初始值，否则如果找不到该字段会导致脚本跳出，modified by chenjyd, 2010.6.11
	set hoplimitlist ""
	captureBuffer get $chas $card $port 1 $numFrames
    for {set i 1} {$i <= $numFrames} {incr i} {
        # Note that the frame number starts at 1
        captureBuffer getframe $i
        set data [captureBuffer cget -frame]
		if { $data == "" } {
			continue
		}
		set type [string range $data 36 40]
	    if  { $type == "81 00" } {
	        set type [string range $data 48 52]
	        set hoplimit [string range $data 75 76]
	    } else {
	    	set hoplimit [string range $data 63 64]
	    }
	    if { $type != "86 DD" } {
	    	#not ip packet
	    	continue
	    } else {
	    	if { $hoplimit == "" } {
	    		continue
	    	} else {
	    		lappend hoplimitlist [format %d 0x0$hoplimit]
	    	}
	    }
	}
	##增加对没有捕捉到hoplimit字段的处理，modified by chenjyd, 2010.6.11
	if {$hoplimitlist == ""} {
		PrintRes Print "The captured packets should have no hoplimit field."
		return {-1 -1}
	} else {
		set hoplimitlist [lsort -integer -increasing $hoplimitlist]
		#增加打印信息，modified by chenjyd, 2010.6.11
		PrintRes Print "The biggest hoplimit is [lindex $hoplimitlist end], the smallest hoplimit is [lindex $hoplimitlist 0]!"
		return [list [lindex $hoplimitlist 0] [lindex $hoplimitlist end]]
	}
}


######################################################################
#
# CheckCaptureStream: 检查抓到的流是否满足镜像的要求，
#                   目前从抓到的包数,vlan tag,source mac,destination mac
#                   source ip ,destination ip几方面判断抓到的流
#
# args:
#           chas:   抓包端口所在chas 
#           card:   抓包端口所在card
#           port:   抓包端口所在port
#           Srcmac: 源mac
#           Dstmac: 目的mac
#           Srcip: source ip
#           Dstip: destination ip
#           VlanTag:
#                   取值 -1 不带tag,0 不关心带不带tag,>0 要求大的tag
#           Cos :   user priority
#	    FragmentFlag: 取值 1 表示数据包分片，0 表示数据包不分片
#	    TotalLength：IP数据包的总长度（包括IP头和数据部分）
#
# return: 返回满足条件的个数
#
#*********************************************************************
# Change log:
#     - 2009.10.19 qiaoyua 增加VlanTag对于DoubleTag的支持
#*********************************************************************
# 
# examples:
#           CheckCaptureStream $chas $card3 $port3 SrcMac 00-00-00-00-00-02 \
#                             DstMac 00-00-00-00-00-01
######################################################################

#CheckCaptureStream $chas $card $port SrcMac $s1cpumac DstMac ff-ff-ff-ff-ff-ff EthernetType loopback LoopBackRecord {100 Ethernet1/1}
#CheckCaptureStream $chas $card $port SrcMac $s1cpumac DstMac ff-ff-ff-ff-ff-ff MrppRecord {EthernetType 0x8100 PRI 0 VlanId 100 \
#                    FrameLength 72 DSAPSSAP 0xAAAA Control 0x03 MrppLength 0x40 MrppVers 0x01 MrppType 1 CtrlVlanId 100 \
#                    SystemMacAddress $cpumac HelloTimer 100 FailTimer 100 State 1 HelloSeq 1}
#VlanTag参数取值为-1 表示不带tag,取值为0 表示不关心带不带tag,取值>0 要求带tag，值为报文所带vid
#注意:使用VlanTag {100 10}，也就是验证DoubleTag时，不能使用除SrcMac,DstMac以外的参数
proc CheckCaptureStream { chas card port args } {
    
    array set arrArgs $args 	
    set counter 0   ;#内部使用的计数器
    # Get the number of frames captured
	capture get $chas $card $port
	set numFrames [capture cget -nPackets]
	if [info exists arrArgs(Num)] {
		set checknum $arrArgs(Num)
	} else {
		set checknum 1000
	}
#add by lixia 2009-5-10  Limit the number of checked packets to 1000 
	if { $numFrames > $checknum} {
           set numFrames $checknum
	}
#End of edit by lixia
	#PrintRes Print "\n$numFrames frames captured"

	# Only look at the first 9 frames
	#if {$numFrames > 10} {
	#	set numFrames 10
	#} else {
	#    return 0        ;#表明出错
	#}
	set character ""
	captureBuffer get $chas $card $port 1 $numFrames
    for {set i 1} {$i <= $numFrames} {incr i} {
        # Note that the frame number starts at 1
        captureBuffer getframe $i
        # Get the actual frame data
        set data [captureBuffer cget -frame]
#        if {$i == 1 || $i == 2} {
#        	puts "$data"
#        }
		if { $data == "" } {
			continue
		}
        set ret 1
        
        #SrcMac
        if {[info exist arrArgs(SrcMac)]} {
            set ret [ expr $ret * [ CheckSrcMacInData $arrArgs(SrcMac) $data ] ]
            if {$i == 1} {
                append character "SrcMac($arrArgs(SrcMac)) "
            }
        }
        
        #DstMac
        if {[info exist arrArgs(DstMac)]} {
            set ret [ expr $ret * [ CheckDstMacInData $arrArgs(DstMac) $data ] ]
            if {$i == 1} {
                append character "DstMac($arrArgs(DstMac)) "
            }
        }
        
        #SrcIp
        if {[info exist arrArgs(SrcIp)]} {
            set ret [ expr $ret * [ CheckSrcIpInData $arrArgs(SrcIp) $data] ]
            if {$i == 1} {
                append character "SrcIp($arrArgs(SrcIp)) "
            }
        }
        
        #DstIp
        if {[info exist arrArgs(DstIp)]} {
            set ret [ expr $ret * [ CheckDstIpInData $arrArgs(DstIp) $data] ]
            if {$i == 1} {
                append character "DstIp($arrArgs(DstIp)) "
            }
        }
        #SrcIpv6
        if {[info exist arrArgs(SrcIpv6)]} {
            set ret [ expr $ret * [ CheckSrcIpv6InData $arrArgs(SrcIpv6) $data] ]
            if {$i == 1} {
                append character "SrcIpv6($arrArgs(SrcIpv6)) "
            }
        }
        
        #DstIpv6
        if {[info exist arrArgs(DstIpv6)]} {
            set ret [ expr $ret * [ CheckDstIpv6InData $arrArgs(DstIpv6) $data] ]
            if {$i == 1} {
                append character "DstIpv6($arrArgs(DstIpv6)) "
            }
        }    
        #VlanTag
        if {[info exist arrArgs(VlanTag)]} {
            set ret [ expr $ret * [ CheckVlanTagInData $arrArgs(VlanTag) $data ] ]
            if {$i == 1} {
                append character "VlanTag($arrArgs(VlanTag)) "
            }
        }
        #Length
         if {[info exist arrArgs(Length)]} {
            set ret [ expr $ret * [ CheckLengthOfData $arrArgs(Length) $data ] ]
            if {$i == 1} {
                append character "Length($arrArgs(Length)) "
            }
        }
        #cos
        if {[info exist arrArgs(Cos)]} {
             set ret [expr $ret * [ CheckCosInData $arrArgs(Cos) $data] ]
             if {$i == 1} {
                append character "Cos($arrArgs(Cos)) "
            }
        }
        #arp
        if {[info exist arrArgs(Arp)]} {
            set ret [expr $ret * [ CheckArpInData $arrArgs(Arp) $data] ]
            if {$i == 1} {
                append character "Arp "
            }
        }
        #arp-operation 
        if {[info exist arrArgs(ArpType)]} {
            set ret [expr $ret * [ CheckArpTypeInData $arrArgs(ArpType) $data] ]
            if {$i == 1} {
                append character "ArpType($arrArgs(ArpType)) "
            }
        }    
        #arp-operation 
        if {[info exist arrArgs(ArpSenderHardwareAddress)]} {
            set ret [expr $ret * [ CheckArpSenderHardwareAddressInData $arrArgs(ArpSenderHardwareAddress) $data] ]
            if {$i == 1} {
                append character "ArpSenderHardwareAddress($arrArgs(ArpSenderHardwareAddress)) "
            }
        }    
        #arp-operation 
        if {[info exist arrArgs(ArpSenderProtocolAddress)]} {
            set ret [expr $ret * [ CheckArpSenderProtocolAddressInData $arrArgs(ArpSenderProtocolAddress) $data] ]
            if {$i == 1} {
                append character "ArpSenderProtocolAddress($arrArgs(ArpSenderProtocolAddress)) "
            }
        }    
        #arp-operation 
        if {[info exist arrArgs(ArpTargetHardwareAddress)]} {
            set ret [expr $ret * [ CheckArpTargetHardwareAddressInData $arrArgs(ArpTargetHardwareAddress) $data] ]
            if {$i == 1} {
                append character "ArpTargetHardwareAddress($arrArgs(ArpTargetHardwareAddress)) "
            }
        }    
        #arp-operation 
        if {[info exist arrArgs(ArpTargetProtocolAddress)]} {
            set ret [expr $ret * [ CheckArpTargetProtocolAddressInData $arrArgs(ArpTargetProtocolAddress) $data] ]
            if {$i == 1} {
                append character "ArpTargetProtocolAddress($arrArgs(ArpTargetProtocolAddress)) "
            }
        }
        #igmp or snooping query
        if {[info exist arrArgs(IgmpQueryVersion)]} {
            set ret [expr $ret * [ CheckIgmpQueryVersionInData $arrArgs(IgmpQueryVersion) $data] ]
            if {$i == 1} {
                append character "IgmpQueryVersion($arrArgs(IgmpQueryVersion)) "
            }
        }
        #igmpv2 group address  in query 
        if {[info exist arrArgs(IgmpV2SpecialQuery)]} {
            set ret [expr $ret * [ CheckIgmpV2SpecialQueryInData $arrArgs(IgmpV2SpecialQuery) $data] ]
            if {$i == 1} {
                append character "IgmpV2SpecialQuery($arrArgs(IgmpV2SpecialQuery)) "
            }
        }
		#igmpv3 group address  in query        
        if {[info exist arrArgs(IgmpV3QueryGroup)]} {
            set ret [expr $ret * [ CheckIgmpV3QueryGroup $arrArgs(IgmpV3QueryGroup) $data] ]
            if {$i == 1} {
                append character "IgmpV3QueryGroup($arrArgs(IgmpV3QueryGroup)) "
            }
        }

		#igmpv3 source address  in query        
        if {[info exist arrArgs(IgmpV3QuerySource)]} {
            set ret [expr $ret * [ CheckIgmpV3QuerySoure $arrArgs(IgmpV3QuerySource) $data] ]
            if {$i == 1} {
                append character "IgmpV3QuerySource($arrArgs(IgmpV3QuerySource)) "
            }
        }
        
        #ethernet type
        if {[info exist arrArgs(EthernetType)]} {
            set ret [expr $ret * [ CheckEthernetTypeInData $arrArgs(EthernetType) $data] ]
            if {$i == 1} {
                append character "EthernetType($arrArgs(EthernetType)) "
            }
        }
        #loopback detection
        if {[info exist arrArgs(LoopBackRecord)]} {
            set ret [expr $ret * [ CheckLoopBackRecordInData $arrArgs(LoopBackRecord) $data] ]
            if {$i == 1} {
                append character "LoopBackRecord($arrArgs(LoopBackRecord)) "
            }
        }
        #mrpp data
        if {[info exist arrArgs(MrppRecord)]} {
            set ret [expr $ret * [ CheckMrppRecordInData $arrArgs(MrppRecord) $data] ]
            if {$i == 1} {
                append character "MrppRecord($arrArgs(MrppRecord)) "
            }
        }
        #protocolEx
        if {[info exist arrArgs(ProtocolEx)]} {
            set ret [expr $ret * [ CheckProtocolExInData $arrArgs(ProtocolEx) $data] ]
            if {$i == 1} {
                append character "ProtocolEx($arrArgs(ProtocolEx)) "
            }
        }
        #Ipprecedence
		if {[info exist arrArgs(Ipprecedence)]} {
            set ret [expr $ret * [ CheckIpprecedenceInData $arrArgs(Ipprecedence) $data] ]
            if {$i == 1} {
                append character "Ipprecedence($arrArgs(Ipprecedence)) "
            }
        }
        #Tos
        if {[info exist arrArgs(Tos)]} {
            set ret [expr $ret * [ CheckTosInData $arrArgs(Tos) $data] ]
            if {$i == 1} {
                append character "Tos($arrArgs(Tos)) "
            }
        }
        #TOSBits
        if {[info exist arrArgs(TOSBits)]} {
            set ret [expr $ret * [ CheckTOSBitsInData $arrArgs(TOSBits) $data] ]
            if {$i == 1} {
                append character "TOSBits($arrArgs(TOSBits)) "
            }
        }
        #Type
        if {[info exist arrArgs(Type)]} {
            set ret [expr $ret * [ CheckTypeInData $arrArgs(Type) $data] ]
            if {$i == 1} {
                append character "Type($arrArgs(Type)) "
            }
        }
        #Code
        if {[info exist arrArgs(Code)]} {
            set ret [expr $ret * [ CheckCodeInData $arrArgs(Code) $data] ]
            if {$i == 1} {
                append character "Code($arrArgs(Code)) "
            }
        }
        #SPort
        if {[info exist arrArgs(SPort)]} {
            set ret [expr $ret * [ CheckSPortInData $arrArgs(SPort) $data] ]
            if {$i == 1} {
                append character "SPort($arrArgs(SPort)) "
            }
        }
        #DPort
        if {[info exist arrArgs(DPort)]} {
            set ret [expr $ret * [ CheckDPortInData $arrArgs(DPort) $data] ]
            if {$i == 1} {
                append character "DPort($arrArgs(DPort)) "
            }
        }
        #FIN
        if {[info exist arrArgs(FIN)]} {
            set ret [expr $ret * [ CheckFINInData $arrArgs(FIN) $data] ]
            if {$i == 1} {
                append character "FIN($arrArgs(FIN)) "
            }
        }
        #SYN
        if {[info exist arrArgs(SYN)]} {
            set ret [expr $ret * [ CheckSYNInData $arrArgs(SYN) $data] ]
            if {$i == 1} {
                append character "SYN($arrArgs(SYN)) "
            }
        }
        #RST
        if {[info exist arrArgs(RST)]} {
            set ret [expr $ret * [ CheckRSTInData $arrArgs(RST) $data] ]
            if {$i == 1} {
                append character "RST($arrArgs(RST)) "
            }
        }
        #PSH
        if {[info exist arrArgs(PSH)]} {
            set ret [expr $ret * [ CheckPSHInData $arrArgs(PSH) $data] ]
            if {$i == 1} {
                append character "PSH($arrArgs(PSH)) "
            }
        }
        #ACK
        if {[info exist arrArgs(ACK)]} {
            set ret [expr $ret * [ CheckACKInData $arrArgs(ACK) $data] ]
            if {$i == 1} {
                append character "ACK($arrArgs(ACK)) "
            }
        }
        #URG
        if {[info exist arrArgs(URG)]} {
            set ret [expr $ret * [ CheckURGInData $arrArgs(URG) $data] ]
            if {$i == 1} {
                append character "URG($arrArgs(URG)) "
            }
        }
        #Offset
         if {[info exist arrArgs(Offset)]} {

            set ret [expr $ret * [ CheckOffsetVlaueInData $arrArgs(Offset) $data] ]
            if {$i == 1} {
               append character "Offset($arrArgs(Offset)) "
            }
        }
        #ipv6 flowlabel
        if {[info exist arrArgs(Flowlabel)]} {
            set ret [expr $ret * [ CheckFlowlabelInData $arrArgs(Flowlabel) $data] ]
            if {$i == 1} {
               append character "Flowlabel($arrArgs(Flowlabel)) "
            }
        }
        #DSCP  v4/v6
        if {[info exist arrArgs(DSCP)]} {
            set ret [expr $ret * [ CheckDSCPInData $arrArgs(DSCP) $data] ]
            if {$i == 1} {
               append character "DSCP($arrArgs(DSCP)) "
            }
        }
        #DhcpMessageType
        if {[info exist arrArgs(DhcpMessageType)]} {
            set ret [expr $ret * [ CheckDhcpMessageTypeInData $arrArgs(DhcpMessageType) $data] ]
            if {$i == 1} {
                append character "DhcpMessageType($arrArgs(DhcpMessageType)) "
            }
        }

        #EtherType
        if {[info exist arrArgs(EtherType)]} {
            set ret [ expr $ret * [ CheckEtherTypeInData $arrArgs(EtherType) $data ] ]
            if {$i == 1} {
                append character "EtherType($arrArgs(EtherType))"
            }
        } 

		#TotalLength
		if {[info exist arrArgs(TotalLength)]} {
			set ret [ expr $ret * [ CheckTotalLengthInData $arrArgs(TotalLength) $data ] ]
			if {$i == 1} {
				append character "TotalLength($arrArgs(TotalLength))"
			}
		}

		#PayloadLength
		if {[info exist arrArgs(PayloadLength)]} {
			set ret [ expr $ret * [ CheckPayloadLengthInData $arrArgs(PayloadLength) $data ] ]
			if {$i == 1} {
				append character "PayloadLength($arrArgs(PayloadLength))"
			}
		}
		
        #FragmentFlag
        if {[info exist arrArgs(FragmentFlag)]} {
                set ret [ expr $ret * [ CheckFragmentFlagInData $arrArgs(FragmentFlag) $data ] ]
                if {$i == 1} {
                        append character "FragmentFlag($arrArgs(FragmentFlag))"
                }
        }
 	   #FragmentHeader
 	   if {[info exist arrArgs(FragmentHeader)]} {
 	       set ret [ expr $ret * [ CheckFragmentHeaderInData $arrArgs(FragmentHeader) $data ] ]
  	       if {$i == 1} {
  	          append character "FragmentHeader($arrArgs(FragmentHeader))"
    	    }
   		} 
 	   #IcmpType
   	   if {[info exist arrArgs(IcmpType)]} {
 	       set ret [ expr $ret * [ CheckIcmpTypeInData $arrArgs(IcmpType) $data ] ]
  	      if {$i == 1} {
  	          append character "IcmpType($arrArgs(IcmpType))"
  	      }
 	   } 
 	   #add by qiaoyua
 	   #IcmpCode
   	   if {[info exist arrArgs(IcmpCode)]} {
 	       set ret [ expr $ret * [ CheckIcmpCodeInData $arrArgs(IcmpCode) $data ] ]
  	      if {$i == 1} {
  	          append character "IcmpCode($arrArgs(IcmpCode))"
  	      }
 	   }
 	   #IcmpSequence
   	   if {[info exist arrArgs(IcmpSequence)]} {
 	       set ret [ expr $ret * [ CheckIcmpSequenceInData $arrArgs(IcmpSequence) $data ] ]
  	      if {$i == 1} {
  	          append character "IcmpSequence($arrArgs(IcmpSequence))"
  	      }
 	   }
 	   #IcmpData
   	   if {[info exist arrArgs(IcmpData)]} {
 	       set ret [ expr $ret * [ CheckIcmpDataInData $arrArgs(IcmpData) $data ] ]
  	      if {$i == 1} {
  	          append character "IcmpData($arrArgs(IcmpData))"
  	      }
 	   }
       #Icmpv6Type
       if {[info exist arrArgs(Icmpv6Type)]} {
           set ret [ expr $ret * [ CheckIcmpv6TypeInData $arrArgs(Icmpv6Type) $data ] ]
           if {$i == 1} {
               append character "Icmpv6Type($arrArgs(Icmpv6Type))"
           }
       }
       #Icmpv6Code
       if {[info exist arrArgs(Icmpv6Code)]} {
           set ret [ expr $ret * [ CheckIcmpv6CodeInData $arrArgs(Icmpv6Code) $data ] ]
           if {$i == 1} {
               append character "Icmpv6Code($arrArgs(Icmpv6Code))"
           }
       }
       #Icmpv6Offset
       if {[info exist arrArgs(Icmpv6Offset)]} {
           set ret [ expr $ret * [ CheckIcmpv6OffsetInData $arrArgs(Icmpv6Offset) $data ] ]
           if {$i == 1} {
               append character "Icmpv6Offset($arrArgs(Icmpv6Offset))"
           }
       }
       #add by zhaohj
	   #Icmpv6Data
	   if {[info exist arrArgs(Icmpv6Data)]} {
	       set ret [ expr $ret * [ CheckIcmpv6DataInData $arrArgs(Icmpv6Data) $data ] ]
	       if {$i == 1} {
	  	       append character "Icmpv6Data($arrArgs(Icmpv6Data))"
	       }
	   }
	#add by gengtao linkaddress
	if {[info exist arrArgs(Icmpv6LinkAddress)]} {
           set ret [ expr $ret * [ CheckIcmpv6LinkAddressInData $arrArgs(Icmpv6LinkAddress) $data ] ]
           if {$i == 1} {
               append character "Icmpv6LinkAddress($arrArgs(Icmpv6LinkAddress))"
           }
       }	
       #MstpRecord
       if {[info exist arrArgs(MstpRecord)]} {
            set ret [expr $ret * [ CheckMstpRecordInData $arrArgs(MstpRecord) $data] ]
            if {$i == 1} {
                append character "MstpRecord($arrArgs(MstpRecord)) "
            }
        }
        #cluster
        if {[info exist arrArgs(Cluster)]} {
            set ret [expr $ret * [ CheckClusterInData $arrArgs(Cluster) $data] ]
            if {$i == 1} {
                append character "Cluster($arrArgs(Cluster)) "
            }
        }
        #MplsRecord 
        if {[info exist arrArgs(MplsRecord)]} {
        	set ret [expr $ret * [ CheckMplsRecordInData $arrArgs(MplsRecord) $data] ]
            if {$i == 1} {
                append character "MplsRecord($arrArgs(MplsRecord)) "
            }
        }
        #lldp
        if {[info exist arrArgs(LLDP)]} {
            set ret [expr $ret * [ CheckLLDPInData $arrArgs(LLDP) $data] ]
            if {$i == 1} {
                append character "LLDP($arrArgs(LLDP)) "
            }
        }
        #lldp
        if {[info exist arrArgs(ULDP)]} {
            set ret [expr $ret * [ CheckULDPInData $arrArgs(ULDP) $data] ]
            if {$i == 1} {
                append character "ULDP($arrArgs(ULDP)) "
            }
        }
        #IgmpType
        if {[info exist arrArgs(IgmpType)]} {
			set ret [expr $ret * [ CheckIgmpTypeInData $arrArgs(IgmpType) $data] ]
			if {$i == 1} {
				append character "IgmpType($arrArgs(IgmpType)) "
			}
		}	
        #Icmpv6 too big
        if {[info exist arrArgs(Icmpv6TooBig)]} {
			set ret [expr $ret * [ CheckIcmpv6TooBigInData $arrArgs(Icmpv6TooBig) $data] ]
			if {$i == 1} {
				append character "Icmpv6TooBig($arrArgs(Icmpv6TooBig)) "
			}
		}
		#add by qiaoyua
		#RipCommand
        if {[info exist arrArgs(RipCommand)]} {
			set ret [expr $ret * [ CheckRipCommandInData $arrArgs(RipCommand) $data] ]
			if {$i == 1} {
				append character "RipCommand($arrArgs(RipCommand)) "
			}
		}
		#add by qiaoyua
		#RipVersion
        if {[info exist arrArgs(RipVersion)]} {
			set ret [expr $ret * [ CheckRipVersionInData $arrArgs(RipVersion) $data] ]
			if {$i == 1} {
				append character "RipVersion($arrArgs(RipVersion)) "
			}
		}
		#add by qiaoyua
		#RipRoute
        if {[info exist arrArgs(RipRoute)]} {
			set ret [expr $ret * [ CheckRipRouteInData $arrArgs(RipRoute) $data] ]
			if {$i == 1} {
				append character "RipRoute($arrArgs(RipRoute)) "
			}
		}
		#add by qiaoyua
		#RipngCommand
        if {[info exist arrArgs(RipngCommand)]} {
			set ret [expr $ret * [ CheckRipngCommandInData $arrArgs(RipngCommand) $data] ]
			if {$i == 1} {
				append character "RipngCommand($arrArgs(RipngCommand)) "
			}
		}
		#add by qiaoyua
		#Ipv6ProtocolEx
        if {[info exist arrArgs(Ipv6ProtocolEx)]} {
			set ret [expr $ret * [ CheckIpv6ProtocolExInData $arrArgs(Ipv6ProtocolEx) $data] ]
			if {$i == 1} {
				append character "Ipv6ProtocolEx($arrArgs(Ipv6ProtocolEx)) "
			}
		}
		#add by qiaoyua
		#PrefixOption
        if {[info exist arrArgs(PrefixOption)]} {
			set ret [expr $ret * [ CheckPrefixOptionInData $arrArgs(PrefixOption) $data] ]
			if {$i == 1} {
				append character "PrefixOption($arrArgs(PrefixOption)) "
			}
		}
		#add by qiaoyua
		#MtuOption
        if {[info exist arrArgs(MtuOption)]} {
			set ret [expr $ret * [ CheckMtuOptionInData $arrArgs(MtuOption) $data] ]
			if {$i == 1} {
				append character "MtuOption($arrArgs(MtuOption)) "
			}
		}
		#add by qiaoyua
		#Icmpv6Ra
        if {[info exist arrArgs(Icmpv6Ra)]} {
			set ret [expr $ret * [ CheckIcmpv6RaInData $arrArgs(Icmpv6Ra) $data] ]
			if {$i == 1} {
				append character "Icmpv6Ra($arrArgs(Icmpv6Ra)) "
			}
		}
		#add by qiaoyua
		#Icmpv6Redirect
        if {[info exist arrArgs(Icmpv6Redirect)]} {
			set ret [expr $ret * [ CheckIcmpv6RedirectInData $arrArgs(Icmpv6Redirect) $data] ]
			if {$i == 1} {
				append character "Icmpv6Redirect($arrArgs(Icmpv6Redirect)) "
			}
		}

		#add by wangleiaq		
		#Icmpv6TargetAdd
        if {[info exist arrArgs(Icmpv6TargetAdd)]} {
			set ret [expr $ret * [ CheckIcmpv6TargetAddInData $arrArgs(Icmpv6TargetAdd) $data] ]
			if {$i == 1} {
				append character "Icmpv6TargetAdd($arrArgs(Icmpv6TargetAdd)) "
			}
		}
		
		#add by caisy
		#LacpDataUnit		
        if {[info exist arrArgs(LacpDU)]} {
            set ret [ expr $ret * [ CheckLacpDataUnitInData $arrArgs(LacpDU) $data ] ]
            if {$i == 1} {
                append character "LacpDU($arrArgs(LacpDU)) "
            }
        }
        #added by zhangfank,210.6.27
        #TTL
        if {[info exist arrArgs(TTL)]} {
            set ret [ expr $ret * [ CheckTTLInData $arrArgs(TTL) $data ] ]
            if {$i == 1} {
                append character "TTL($arrArgs(TTL)) "
            }
        }
        #added by gengtao, 2010.11.11
        #Vrrp
        if {[info exist arrArgs(Vrrp)]} {
            set ret [ expr $ret * [ CheckVrrpInData $arrArgs(Vrrp) $data ] ]
            if {$i == 1} {
                append character "Vrrp($arrArgs(Vrrp)) "
            }
        }
         #added by gengtao 2010.11.15
        #ipv6vrrp
        if {[info exist arrArgs(Ipv6Vrrp)]} {
		set ret [ expr $ret * [ CheckIpv6VrrpInData $arrArgs(Ipv6Vrrp) $data ] ]
		if {$i == 1} {
                append character "Ipv6Vrrp($arrArgs(Ipv6Vrrp)) "
            }
        }       
        #added by zhangfank,210.6.27
        #HopLimit
        if {[info exist arrArgs(HopLimit)]} {
            set ret [ expr $ret * [ CheckHopLimitInData $arrArgs(HopLimit) $data ] ]
            if {$i == 1} {
                append character "HopLimit($arrArgs(HopLimit)) "
            }
        }
        #TTL in gre packet
		if {[info exist arrArgs(GreTTL)]} {
			set ret [expr $ret * [ CheckTTLInGrePayload $arrArgs(GreTTL) $data ]]
			if {$i == 1} {
				append character "GreTTL($arrArgs(GreTTL)) "
			}
		}
		#Protocol type in gre header
		if {[info exist arrArgs(GreProtocol)]} {
			set ret [expr $ret * [ CheckProtocolTypeInGreHeader $arrArgs(GreProtocol) $data]]
			if {$i == 1} {
				append character "GreProtocol($arrArgs(GreProtocol)) "
			}
		}
		#hop limit in gre packet
		if {[info exist arrArgs(GreHopLimit)]} {
			set ret [expr $ret * [ CheckHopLimitInGrePayload $arrArgs(GreHopLimit) $data]]
			if {$i == 1} {
				append character "GreHopLimit($arrArgs(GreHopLimit)) "
			}
		}
	    #add by zhaohj 2010-11-03
	    #PppoeTlvType
	    if {[info exist arrArgs(PppoeTlvType)]} {
	        set ret [ expr $ret * [ CheckPppoeTlvTypeInData $arrArgs(PppoeTlvType) $data ] ]
	        if {$i == 1} {
	  	        append character "PppoeTlvType($arrArgs(PppoeTlvType))"
	        }
	    }
		
        if { $ret != 0 } {
            incr counter
        } else {
            #PrintRes Print "the $i frame is : $data"
        }
            
    } 
    PrintRes Print "Check capture packets on $chas:$card:$port with $character is $counter."   
    return $counter
}

#CheckCaptureStream $chas $card $port SrcMac xx-xx-xx-xx-xx-xx DstMac xx-xx-xx-xx-xx-xx Icmpv6TooBig { MTU 1400}
proc CheckIcmpv6TooBigInData { record data } {
	array set arrArgs $record
	set ethernettype [string range $data 36 40]
	set protocolex [string range $data 60 61]
	set type [string range $data 162 163]
	set code [string range $data 165 166]
	if { $ethernettype == "86 DD" && $protocolex == "3A" && $type == "02" && $code == "00" } {
		set res 1
		#MTU
		if {[info exists arrArgs(MTU)]} {
			set res [expr $res & ([format %d 0x0[string range $data 174 175][string range $data 177 178][string range $data 180 181][string range $data 183 184]]==$arrArgs(MTU)?1:0)]   
		} 
		return $res
	} else {
		return 0
	}
}

#added by gengtao,2010.11.29
proc CheckIcmpv6LinkAddressInData {record data} {
	set type [string range $data 162 163]
	if {$type == "88"} {
		set linkaddress [string range $data 240 256]
 	} else {
		return 0
 	} 
 	if {$linkaddress == $record} {
		return 1
 	} else {
		return 0
 	}
}

#added by zhangfank,2010.6.27
proc CheckTTLInData { record data } {
	set type [string range $data 36 40]
    if  { $type == "81 00" } {
        set type [string range $data 48 52]
        if {$type == "08 00"} {
        	set ttl [string range $data 78 79]
        } else {
        	return 0
        }	
    } elseif {$type == "08 00"} {
       	set ttl [string range $data 66 67]
    } else {
    	return 0
    }
    set ttl [format %i 0x0$ttl]
    if {$ttl == $record} {
    	return 1
    } else {
    	return 0
    }
}


#added by zhangfank,2010.6.27
proc CheckHopLimitInData { record data } {
	set type [string range $data 36 40]
    if  { $type == "81 00" } {
        set type [string range $data 48 52]
        if {$type == "86 DD"} {
        	set hoplimit [string range $data 75 76]
        } else {
        	return 0
        }	
    } elseif {$type == "86 DD"} {
    	set hoplimit [string range $data 63 64]
    } else {
    	return 0
    }	
    set hoplimit [format %i 0x0$hoplimit]
    if {$hoplimit == $record} {
    	return 1
    } else {
    	return 0
    }
}    

#TargetAddress判断,added by wangleiaq,2010.12.1
proc CheckIcmpv6TargetAddInData {TargetAdd data} {
    set data [string range $data 186 232]
    regsub -all " " $data "" data
    set n1 [string range $data 0 3]
    set n2 [string range $data 4 7]
    set n3 [string range $data 8 11]
    set n4 [string range $data 12 15]
	set n5 [string range $data 16 19]
    set n6 [string range $data 20 23]
    set n7 [string range $data 24 27]
    set n8 [string range $data 28 31]
	set spring $n1
	append spring ":" "$n2" ":" "$n3" ":" "$n4" ":" "$n5" ":" "$n6" ":" "$n7" ":" "$n8"
	set TargetAdd [ FormatIpv6 $TargetAdd ]
	set TargetAdd [string toupper $TargetAdd 0 end]
#	puts "TargetAdd == $TargetAdd"
    if { $TargetAdd == $spring } {
        return 1
    } else {
        return 0
    }
}

######################以下三个函数针对GRE隧道报文进行检查#################################
proc CheckProtocolTypeInGreHeader { protocol data } {
	set vlanflag [string range $data 36 40]
	#tag
	if {$vlanflag == "81 00"} {
		set protocol_en [string range $data 48 52]
		if {$protocol_en == "86 DD"} {
			set protocol_type [string range $data 180 184]
		} elseif {$protocol_en == "08 00"} {
			set protocol_type [string range $data 120 124]
		}
	} elseif {$vlanflag == "08 00"} {
		set protocol_type [string range $data 108 112]
	} elseif {$vlanflag == "86 DD"} {
		set protocol_type [string range $data 168 172]
	}	
	switch -exact $protocol {
		ipv4 {
			set protocol "08 00"
		}
		ipv6 {
			set protocol "86 DD"
		}
	}
	if {$protocol_type == $protocol} {
		return 1
	} else {
		return 0
	}
}


proc CheckTTLInGrePayload { ttl data } {
	set vlanflag [string range $data 36 40]
	if {$vlanflag == "81 00"} {
		set protocoltype [string range $data 48 52]
		if {$protocoltype == "08 00"} {
			set ttl_value [string range $data 150 151]
		} elseif {$protocoltype == "86 DD"}	{
			set ttl_value [string range $data 210 211]
		}	
	} elseif {$vlanflag == "08 00"} {
		set ttl_value [string range $data 138 139]
	} elseif {$vlanflag == "86 DD"} {
		set ttl_value [string range $data 198 199]
	}	
	if {[info exist ttl_value]} {
		set ttl_value [format %d 0x$ttl_value]
		if {$ttl_value == $ttl} {
			return 1
		} else {
			return 0
		}
	} else {
		return 0
	}
}


proc CheckHopLimitInGrePayload { hoplimit data } {
	set vlanflag [string range $data 36 40]
	if {$vlanflag == "81 00"} {
		set protocoltype [string range $data 48 52]
		if {$protocoltype == "08 00"} {
			set hoplimit_value [string range $data 147 148]
		} elseif {$protocoltype == "86 DD"}	{
			set hoplimit_value [string range $data 207 208]
		}	
	} elseif {$vlanflag == "08 00"} {
		set hoplimit_value [string range $data 135 136]
	} elseif {$vlanflag == "86 DD"} {
		set hoplimit_value [string range $data 195 196]
	}	
	if {[info exist hoplimit_value]} {
		set hoplimit_value [format %d 0x$hoplimit_value]
		if {$hoplimit_value == $hoplimit} {
			return 1
		} else {
			return 0
		}
	} else {
		return 0
	}
}
############################################################################################

#add by caisy 2010-2
proc CheckLacpDataUnitInData { record data } {	
	array set arrArgs $record
	set res 1
	##set macdata [string range $data 18 34]
 ##   regsub -all " " $macdata - macdata
 ##   set srcmac [string toupper $srcmac]
 if {[info exists arrArgs(ReturnData)]} {
			return $data			
		}
	#判断是否带vlantag，截取mac及vlantag字段后的其余字段
	set flag [string range $data 36 40]
	if { $flag == "81 00" } {
		set data [string range $data 48 end]
	} else {
		set data [string range $data 36 end]
			}
	set flag [string range $data 0 4]
	#type
	if { $flag == "88 09" } {	
		###return source mac
		##if {[info exists arrArgs(ReturnMac)]} {
		##	return $srcmac			
		##}
		#subtype: 01
		if {[info exists arrArgs(SubType)]} {
			set res [expr $res & ([string equal [string range $data 6 7] $arrArgs(SubType)]?1:0)]			
		}
		#Version Number: 01
		if {[info exists arrArgs(VersionNumber)]} {
			set res [expr $res & ([string equal [string range $data 9 10] $arrArgs(VersionNumber)]?1:0)]		
		}
		#TLV type: 01
		if {[info exists arrArgs(TLVType)]} {
			set res [expr $res & ([string equal [string range $data 12 13] $arrArgs(TLVType)]?1:0)]			
		}
		#Actor Information Length: 14
		if {[info exists arrArgs(ActorInforLength)]} {
			set res [expr $res & ([string equal [string range $data 15 16] $arrArgs(ActorInforLength)]?1:0)]			
		}
		#Reserved 1: 00 00 00
		if {[info exists arrArgs(Reserved1)]} {
			set dataTemp [string range $data 63 64][string range $data 66 67][string range $data 69 70]
			set res [expr $res & ([string equal $dataTemp $arrArgs(Reserved1)]?1:0)]			
		}
		#Reserved 2: 00 00 00
		if {[info exists arrArgs(Reserved2)]} {
			set dataTemp [string range $data 123 124][string range $data 126 127][string range $data 129 130]
			set res [expr $res & ([string equal $dataTemp $arrArgs(Reserved1)]?1:0)]			
		}
		#Reserved 3: 00 00 00 ...(x50)...00
		if {[info exists arrArgs(Reserved3)]} {
			set res [expr $res & ([string equal [string range $data 186 334] $arrArgs(Reserved1)]?1:0)]			
		}		
		return $res
	} else {
		return 0
	}
}

#列表中的s标志位请按实际情况编写，只有最后一个列表元素的S为1，其他都为0
#CheckCaptureStream $chas $card $port SrcMac $s1cpumac DstMac ff-ff-ff-ff-ff-ff MplsRecord {{Tag abc Cos 4 S 0 TTL 64} {Tag bcd Cos 4 S 1 TTL 64}}
proc CheckMplsRecordInData { record data } {
	set flag [string range $data 36 40]
    if  { $flag == "81 00" } {
        set flag [string range $data 48 52]
    }
    if { $flag == "88 47" } {
    	#mpls packet
    	set res 1
    	for {set i 0} {$i < [llength $record]} {incr i} {
			array set arrArgs [lindex $record $i]
			#Tag
			if {[info exists arrArgs(Tag)]} {
				set res [expr $res & ([format %d 0x0[string range $data 54 55][string range $data 57 58][string range $data 60 60]]== $arrArgs(Tag)?1:0)]  
			}
			#Cos
			if {[info exists arrArgs(Cos)]} {
				set res [expr $res & ([expr [format %d 0x0[string range $data 61 61]] / 2]== $arrArgs(Cos)?1:0)]  	
			}
			#S
			if {[info exists arrArgs(S)]} {
				set res [expr $res & ([expr [format %d 0x0[string range $data 61 61]] % 2]== $arrArgs(S)?1:0)]  	
			}
			#TTL
			if {[info exists arrArgs(TTL)]} {
				set res [expr $res & ([format %d 0x0[string range $data 63 64][string range $data 66 67]]== $arrArgs(TTL)?1:0)]  	
			}
    	}
    	return $res	
    } else {
    	#no mpls packet
    	return 0
    }
}



#CheckCaptureStream $chas $card $port SrcMac $s1cpumac DstMac ff-ff-ff-ff-ff-ff MstpRecord {ProtocolId 0000 ProtocolVersion 03 BpduType 02 \
#                   MsgAge 0000 MaxHop 00 MaxAge 0000 HelloTime 0000 ForwardDelay 0000}

proc CheckMstpRecordInData { record data } {
	array set arrArgs $record
	set flag [ string range $data 42 49]
	if { $flag == "42 42 03" } {
		set res 1
		#bpdu
		#ProtocolIdentifier
		if {[info exists arrArgs(ProtocolId)]} {
			set res [expr $res & ([string equal [string range $data 51 52][string range $data 54 55] $arrArgs(ProtocolId)]?1:0)]   ;#type = 0000
		}  
		#ProtocolVersion
		if {[info exists arrArgs(ProtocolVersion)]} {
		   set res [expr $res & ([string equal [string range $data 57 58] $arrArgs(ProtocolVersion)]?1:0)]   ;#type = 03
		}    
		#BpduType
		if {[info exists arrArgs(BpduType)]} {
		   set res [expr $res & ([string equal [string range $data 60 61] $arrArgs(BpduType)]?1:0)]   ;#type = 02
		}    
		#MsgAge
		if {[info exists arrArgs(MsgAge)]} {
		   set res [expr $res & ([string equal [string range $data 132 133][string range $data 135 136] $arrArgs(MsgAge)]?1:0)]   ;#type = 0000
		}  
		#MaxHop
		if {[info exists arrArgs(MaxHop)]} {
		   set res [expr $res & ([string equal [string range $data 354 355] $arrArgs(MaxHop)]?1:0)]   ;#type = 00
		}
		#MaxAge
		if {[info exists arrArgs(MaxAge)]} {
		   set res [expr $res & ([string equal [string range $data 138 139][string range $data 141 142] $arrArgs(MaxAge)]?1:0)]   ;#type = 0000
		}
		#HelloTime
		if {[info exists arrArgs(HelloTime)]} {
		   set res [expr $res & ([string equal [string range $data 144 145][string range $data 147 148] $arrArgs(HelloTime)]?1:0)]   ;#type = 0000
		}
		#MaxAge
		if {[info exists arrArgs(ForwardDelay)]} {
		   set res [expr $res & ([string equal [string range $data 150 151][string range $data 153 154] $arrArgs(ForwardDelay)]?1:0)]   ;#type = 0000
		}
		return $res
   	} else {
   		return 0
   	}
}
#add by zhangfank  2009-5-12
proc CheckEtherTypeInData { type data } {
        set flag [ string range $data 36 40 ]
        if { $flag == "81 00"} {
        #带vlan tag
            set n1 [ string range $data 48 49 ]
            set n2 [ string range $data 51 52 ]
            set type1 "$n1$n2"
        } else {
        #不带vlan tag
            set n1 [ string range $data 36 37 ]
            set n2 [ string range $data 39 40 ]
            set type1 "$n1$n2"
        }
        if { $type1 == $type } {
            return 1
        } else {
            return 0
        }
}        

#add by zhangfank 2009-5-12
#modify by qiaoyua 2009.10.21
#增加对DoubleTag的判断以及对Ipv4报头中协议字段的判断
proc CheckIcmpTypeInData { type data } {
	set tag [ string range $data 36 40 ]
	set doubletag [ string range $data 48 52 ]
	#判断报文是否带有Tag
	if { $tag == "81 00" } {
		#判断报文是否带有DoubleTag
		if { $doubletag == "81 00" } {
			#判断报文是否为Ipv4 Icmp报文
			set icmpflag [ string range $data 93 94 ]
	        if { $icmpflag == "01" } {
				set icmptype [ string range $data 126 127 ]
		        set icmptype "0x0$icmptype"
		        set icmptype [ format "%i" $icmptype ]
		        if { $icmptype == $type } {
		            return 1
		        }
        	}
        } else {
        	set icmpflag [ string range $data 81 82 ]
			if { $icmpflag == "01" } {
				set icmptype [ string range $data 114 115 ]
		        set icmptype "0x0$icmptype"
		        set icmptype [ format "%i" $icmptype ]
		        if { $icmptype == $type } {
		            return 1
		        }
        	}
        }
	} else {
		set icmpflag [ string range $data 69 70 ]
		if { $icmpflag == "01" } {
			set icmptype [ string range $data 102 103 ]
	        set icmptype "0x0$icmptype"
	        set icmptype [ format "%i" $icmptype ]
	        if { $icmptype == $type } {
	            return 1
	        }
        }
	}
	return 0
}

#add by qiaoyua 2009.10.29
#判断Icmp Code字段，支持带vlan tag以及double tag
proc CheckIcmpCodeInData { type data } {
	set tag [ string range $data 36 40 ]
	set doubletag [ string range $data 48 52 ]
	#判断报文是否带有Tag
	if { $tag == "81 00" } {
		#判断报文是否带有DoubleTag
		if { $doubletag == "81 00" } {
			#判断报文是否为Ipv4 Icmp报文
			set icmpflag [ string range $data 93 94 ]
	        if { $icmpflag == "01" } {
				set icmptype [ string range $data 129 130 ]
		        set icmptype "0x0$icmptype"
		        set icmptype [ format "%i" $icmptype ]
		        if { $icmptype == $type } {
		            return 1
		        }
        	}
        } else {
        	set icmpflag [ string range $data 81 82 ]
			if { $icmpflag == "01" } {
				set icmptype [ string range $data 117 118 ]
		        set icmptype "0x0$icmptype"
		        set icmptype [ format "%i" $icmptype ]
		        if { $icmptype == $type } {
		            return 1
		        }
        	}
        }
	} else {
		set icmpflag [ string range $data 69 70 ]
		if { $icmpflag == "01" } {
			set icmptype [ string range $data 105 106 ]
	        set icmptype "0x0$icmptype"
	        set icmptype [ format "%i" $icmptype ]
	        if { $icmptype == $type } {
	            return 1
	        }
        }
	}
	return 0
}

#add by qiaoyua 2009.10.29
#判断Icmp Sequence字段，支持带vlan tag以及double tag
proc CheckIcmpSequenceInData { type data } {
	set tag [ string range $data 36 40 ]
	set doubletag [ string range $data 48 52 ]
	#判断报文是否带有Tag
	if { $tag == "81 00" } {
		#判断报文是否带有DoubleTag
		if { $doubletag == "81 00" } {
			#判断报文是否为Ipv4 Icmp报文
			set icmpflag [ string range $data 93 94 ]
	        if { $icmpflag == "01" } {
				set icmptype1 [ string range $data 144 145 ]
				set icmptype2 [ string range $data 147 148 ]
				append icmptype $icmptype1 $icmptype2
		        set icmptype "0x0$icmptype"
		        set icmptype [ format "%i" $icmptype ]
		        if {[llength $type] == 2} {
		        	for {set i [lindex $type 0]} {$i <= [lindex $type 1]} {incr i} {
						if { $icmptype == $i } {
							return 1
						}
		        	}
		        } else {
			        if { $icmptype == $type } {
			            return 1
			        }
		        }
        	}
        } else {
        	set icmpflag [ string range $data 81 82 ]
			if { $icmpflag == "01" } {
				set icmptype1 [ string range $data 132 133 ]
				set icmptype2 [ string range $data 135 136 ]
				append icmptype $icmptype1 $icmptype2
		        set icmptype "0x0$icmptype"
		        set icmptype [ format "%i" $icmptype ]
		        if {[llength $type] == 2} {
		        	for {set i [lindex $type 0]} {$i <= [lindex $type 1]} {incr i} {
						if { $icmptype == $i } {
							return 1
						}
		        	}
		        } else {
			        if { $icmptype == $type } {
			            return 1
			        }
		        }
        	}
        }
	} else {
		set icmpflag [ string range $data 69 70 ]
		if { $icmpflag == "01" } {
			set icmptype1 [ string range $data 120 121 ]
			set icmptype2 [ string range $data 123 124 ]
			append icmptype $icmptype1 $icmptype2
	        set icmptype "0x0$icmptype"
	        set icmptype [ format "%i" $icmptype ]
	        if {[llength $type] == 2} {
		        for {set i [lindex $type 0]} {$i <= [lindex $type 1]} {incr i} {
					if { $icmptype == $i } {
						return 1
					}
		        }
			} else {
				if { $icmptype == $type } {
					return 1
			    }
		    }
        }
	}
	return 0
}

#add by qiaoyua 2009.11.2
#判断Icmp Data字段，支持带vlan tag
proc CheckIcmpDataInData { type data } {
	set tag [ string range $data 36 40 ]
	set length [ string length $data]
	#判断报文是否带有Tag
	if [string match $tag "81 00"] {
		set fragmentflag [ string range $data 73 76 ]
		if [string match $fragmentflag "0 00"] {
			set icmpdata [ string range $data 138 end-10 ]
			set num [regsub -all -nocase "$type " $icmpdata "" ignore]
	        set len [expr {($length-11-138)/3}]
	        if {$num == $len} {
		    	return 1
			}
        } else {
			set icmpdata [ string range $data 114 end-10 ]
			set num [regsub -all -nocase "$type " $icmpdata "" ignore]
	        set len [expr {($length-11-114)/3}]
	        if {$num == $len} {
		    	return 1
			}
        }
	} else {
		set fragmentflag [ string range $data 61 64 ]
		if [string match $fragmentflag "0 00"] {
			set icmpdata [ string range $data 126 end-10 ]
			set num [regsub -all -nocase "$type " $icmpdata "" ignore]
	        set len [expr {($length-11-126)/3}]
	        if {$num == $len} {
		    	return 1
			}
        } else {
			set icmpdata [ string range $data 102 end-10 ]
			set num [regsub -all -nocase "$type " $icmpdata "" ignore]
	        set len [expr {($length-11-102)/3}]
	        if {$num == $len} {
		    	return 1
			}
        }
	}
	return 0
}


#add by qiaoyua 2009.11.16
#判断Rip Command字段，支持带vlan tag
proc CheckRipCommandInData { type data } {
	set tag [ string range $data 36 40 ]
	#判断报文是否带有Tag
	if { $tag == "81 00" } {
		set ripcommand [ string range $data 138 139 ]
		set ripcommand "0x0$ripcommand"
	    set ripcommand [ format "%i" $ripcommand ]
		if { $ripcommand == $type } {
		    return 1
	    }
    } else {
		set ripcommand [ string range $data 126 127 ]
	    set ripcommand "0x0$ripcommand"
	    set ripcommand [ format "%i" $ripcommand ]
	    if { $ripcommand == $type } {
	        return 1
	    }
	}
	return 0
}

#add by qiaoyua 2009.11.16
#判断Rip Version字段，支持带vlan tag
proc CheckRipVersionInData { type data } {
	set tag [ string range $data 36 40 ]
	#判断报文是否带有Tag
	if { $tag == "81 00" } {
		set ripversion [ string range $data 141 142 ]
		set ripversion "0x0$ripversion"
	    set ripversion [ format "%i" $ripversion ]
		if { $ripversion == $type } {
		    return 1
	    }
    } else {
		set ripversion [ string range $data 129 130 ]
	    set ripversion "0x0$ripversion"
	    set ripversion [ format "%i" $ripversion ]
	    if { $ripversion == $type } {
	        return 1
	    }
	}
	return 0
}


#add by qiaoyua 2009.11.16
#判断Rip Route字段，支持带vlan tag
#RipRoute {{Num 1 Family 2 Ip 12.1.1.0 Mask 255.255.255.0 Nexthop 0.0.0.0 Metric 2} \
#          {Num 2 Family 2 Ip 23.1.1.0 Mask 255.255.255.0 Nexthop 0.0.0.0 Metric 1} \
#          {Num 3 Family 2 Ip 110.1.1.0 Mask 255.255.255.0 Nexthop 0.0.0.0 Metric 3} \
#          {Num 4 Family 2 Ip 120.1.1.0 Mask 255.255.255.0 Nexthop 0.0.0.0 Metric 2} \
#          {Num 5 Family 2 Ip 130.1.1.0 Mask 255.255.255.0 Nexthop 0.0.0.0 Metric 0}}
proc CheckRipRouteInData { type data } {
	set tag [ string range $data 36 40 ]
	set res 1
	#判断报文是否带有Tag
	if { $tag == "81 00" } {
	    for {set j 0} {$j < [llength $type]} {incr j} {
	    	set routerentry [lindex $type $j]
	    	set position [lsearch $routerentry "Num"]
	    	if {$position != -1} {
	    		set seq [lindex $routerentry [expr $position + 1]]
	    	} else {
				return 0
	    	}
	    	if {[string length $data] > [expr {208 + ($seq - 1) * 60}]} {
				set riproute [string range $data [expr {150 + ($seq - 1) * 60}] [expr {208 + ($seq - 1) * 60}]]
				#Family
				set position [lsearch $routerentry "Family"]
				if {$position != -1} {
					set ripfamily [string range $riproute 0 4]
					regsub -all " " $ripfamily "" ripfamily 
					set ripfamily "0x$ripfamily"
					set ripfamily [format "%i" $ripfamily]
					set res [expr $res * [expr {$ripfamily == [lindex $routerentry [expr $position + 1]]}]]
				}
				#Ip
				set position [lsearch $routerentry "Ip"]
				if {$position != -1} {
					set ripip1 [string range $riproute 12 13]
					set ripip2 [string range $riproute 15 16]
					set ripip3 [string range $riproute 18 19]
					set ripip4 [string range $riproute 21 22]
					set ripip1 "0x$ripip1"
					set ripip2 "0x$ripip2"
					set ripip3 "0x$ripip3"
					set ripip4 "0x$ripip4"
					set ripip1 [format "%i" $ripip1]
					set ripip2 [format "%i" $ripip2]
					set ripip3 [format "%i" $ripip3]
					set ripip4 [format "%i" $ripip4]
					set ripip $ripip1
					append ripip "." "$ripip2" "." "$ripip3" "." "$ripip4"
					set res [expr $res * [expr {$ripip == [lindex $routerentry [expr $position + 1]]}]]
				}
				#Mask
				set position [lsearch $routerentry "Mask"]
				if {$position != -1} {
					set ripmask1 [string range $riproute 24 25]
					set ripmask2 [string range $riproute 27 28]
					set ripmask3 [string range $riproute 30 31]
					set ripmask4 [string range $riproute 33 34]
					set ripmask1 "0x$ripmask1"
					set ripmask2 "0x$ripmask2"
					set ripmask3 "0x$ripmask3"
					set ripmask4 "0x$ripmask4"
					set ripmask1 [format "%i" $ripmask1]
					set ripmask2 [format "%i" $ripmask2]
					set ripmask3 [format "%i" $ripmask3]
					set ripmask4 [format "%i" $ripmask4]
					set ripmask $ripmask1
					append ripmask "." "$ripmask2" "." "$ripmask3" "." "$ripmask4"
					set res [expr $res * [expr {$ripmask == [lindex $routerentry [expr $position + 1]]}]]
				}
				#Nexthop
				set position [lsearch $routerentry "Nexthop"]
				if {$position != -1} {
					set ripnexthop1 [string range $riproute 36 37]
					set ripnexthop2 [string range $riproute 39 40]
					set ripnexthop3 [string range $riproute 42 43]
					set ripnexthop4 [string range $riproute 45 46]
					set ripnexthop1 "0x$ripnexthop1"
					set ripnexthop2 "0x$ripnexthop2"
					set ripnexthop3 "0x$ripnexthop3"
					set ripnexthop4 "0x$ripnexthop4"
					set ripnexthop1 [format "%i" $ripnexthop1]
					set ripnexthop2 [format "%i" $ripnexthop2]
					set ripnexthop3 [format "%i" $ripnexthop3]
					set ripnexthop4 [format "%i" $ripnexthop4]
					set ripnexthop $ripnexthop1
					append ripnexthop "." "$ripnexthop2" "." "$ripnexthop3" "." "$ripnexthop4"
					set res [expr $res * [expr {$ripnexthop == [lindex $routerentry [expr $position + 1]]}]]
				}
				#Metric
				set position [lsearch $routerentry "Metric"]
				if {$position != -1} {
					set ripmetric [string range $riproute 57 58]
					set ripmetric "0x$ripmetric"
					set ripmetric [format "%i" $ripmetric]
					set res [expr $res * [expr {$ripmetric == [lindex $routerentry [expr $position + 1]]}]]
				}
			} else {
				return 0
			}
		}
	} else {
	    for {set j 0} {$j < [llength $type]} {incr j} {
	    	set routerentry [lindex $type $j]
	    	set position [lsearch $routerentry "Num"]
	    	if {$position != -1} {
	    		set seq [lindex $routerentry [expr $position + 1]]
	    	} else {
				return 0
	    	}
	    	if {[string length $data] > [expr {196 + ($seq - 1) * 60}]} {
				set riproute [string range $data [expr {138 + ($seq - 1) * 60}] [expr {196 + ($seq - 1) * 60}]]
				#Family
				set position [lsearch $routerentry "Family"]
				if {$position != -1} {
					set ripfamily [string range $riproute 0 4]
					regsub -all " " $ripfamily "" ripfamily 
					set ripfamily "0x$ripfamily"
					set ripfamily [format "%i" $ripfamily]
					set res [expr $res * [expr {$ripfamily == [lindex $routerentry [expr $position + 1]]}]]
				}
				#Ip
				set position [lsearch $routerentry "Ip"]
				if {$position != -1} {
					set ripip1 [string range $riproute 12 13]
					set ripip2 [string range $riproute 15 16]
					set ripip3 [string range $riproute 18 19]
					set ripip4 [string range $riproute 21 22]
					set ripip1 "0x$ripip1"
					set ripip2 "0x$ripip2"
					set ripip3 "0x$ripip3"
					set ripip4 "0x$ripip4"
					set ripip1 [format "%i" $ripip1]
					set ripip2 [format "%i" $ripip2]
					set ripip3 [format "%i" $ripip3]
					set ripip4 [format "%i" $ripip4]
					set ripip $ripip1
					append ripip "." "$ripip2" "." "$ripip3" "." "$ripip4"
					set res [expr $res * [expr {$ripip == [lindex $routerentry [expr $position + 1]]}]]
				}
				#Mask
				set position [lsearch $routerentry "Mask"]
				if {$position != -1} {
					set ripmask1 [string range $riproute 24 25]
					set ripmask2 [string range $riproute 27 28]
					set ripmask3 [string range $riproute 30 31]
					set ripmask4 [string range $riproute 33 34]
					set ripmask1 "0x$ripmask1"
					set ripmask2 "0x$ripmask2"
					set ripmask3 "0x$ripmask3"
					set ripmask4 "0x$ripmask4"
					set ripmask1 [format "%i" $ripmask1]
					set ripmask2 [format "%i" $ripmask2]
					set ripmask3 [format "%i" $ripmask3]
					set ripmask4 [format "%i" $ripmask4]
					set ripmask $ripmask1
					append ripmask "." "$ripmask2" "." "$ripmask3" "." "$ripmask4"
					set res [expr $res * [expr {$ripmask == [lindex $routerentry [expr $position + 1]]}]]
				}
				#Nexthop
				set position [lsearch $routerentry "Nexthop"]
				if {$position != -1} {
					set ripnexthop1 [string range $riproute 36 37]
					set ripnexthop2 [string range $riproute 39 40]
					set ripnexthop3 [string range $riproute 42 43]
					set ripnexthop4 [string range $riproute 45 46]
					set ripnexthop1 "0x$ripnexthop1"
					set ripnexthop2 "0x$ripnexthop2"
					set ripnexthop3 "0x$ripnexthop3"
					set ripnexthop4 "0x$ripnexthop4"
					set ripnexthop1 [format "%i" $ripnexthop1]
					set ripnexthop2 [format "%i" $ripnexthop2]
					set ripnexthop3 [format "%i" $ripnexthop3]
					set ripnexthop4 [format "%i" $ripnexthop4]
					set ripnexthop $ripnexthop1
					append ripnexthop "." "$ripnexthop2" "." "$ripnexthop3" "." "$ripnexthop4"
					set res [expr $res * [expr {$ripnexthop == [lindex $routerentry [expr $position + 1]]}]]
				}
				#Metric
				set position [lsearch $routerentry "Metric"]
				if {$position != -1} {
					set ripmetric [string range $riproute 57 58]
					set ripmetric "0x$ripmetric"
					set ripmetric [format "%i" $ripmetric]
					set res [expr $res * [expr {$ripmetric == [lindex $routerentry [expr $position + 1]]}]]
				}
			} else {
				return 0
			}
		}
	}
	return $res
}

#add by qiaoyua 2009.12.29
#判断Ripng Command字段，没有考虑带Vlan tag字段情况
proc CheckRipngCommandInData { type data } {
	set ethtype1 [string range $data 36 37]
	set ethtype2 [string range $data 39 40]
	if {$ethtype1 == "86" && $ethtype2 == "DD"} {
		set ripngcommand [ string range $data 162 163 ]
		set ripngcommand "0x0$ripngcommand"
		set ripngcommand [ format "%i" $ripngcommand ]
		if { $ripngcommand == $type } {
		    return 1
		}
	}
	return 0
}

#add by qiaoyua 2009.12.29
#判断Ipv6ProtocolEx字段，只判断Ipv6报头中的下一报头字段，没有考虑带Vlan tag字段
proc CheckIpv6ProtocolExInData { record data } {
	switch -exact $record {
    	tcp {set record 6}
    	udp {set record 17}
    	ripng {set record 17}
    	icmpv6 {set record 58}
    	defaut {}
    }
	set ethtype1 [string range $data 36 37]
	set ethtype2 [string range $data 39 40]
	if {$ethtype1 == "86" && $ethtype2 == "DD"} {
		set ipv6protocolex [string range $data 60 61]
		set ipv6protocolex [format %i "0x$ipv6protocolex"]
		if {$ipv6protocolex == $record} {
			return 1
		}
	}
    return 0
}


#add by qiaoyua 2010.1.20
#判断Icmpv6 Prefix可选项
#Num是必带字段，标识该条Prefix Option是第几条 
#PrefixOption {{Num 1 Type 3 Length 4 PrefixLength 64 Link 1 Autonomous 1 NotRouter 0 \
#				SitePrefix 0 ValidTime 2592000 PreferredTime 604800 Prefix 2000::}}
proc CheckPrefixOptionInData { type data } {
	set res 1
    for {set j 0} {$j < [llength $type]} {incr j} {
    	set raentry [lindex $type $j]
    	set position [lsearch $raentry "Num"]
    	if {$position != -1} {
    		set raseq [lindex $raentry [expr $position + 1]]
    	} else {
			return 0
    	}
    	if {[string length $data] > [expr {328 + ($raseq - 1) * 96}]} {
			set raprefix [string range $data [expr {234 + ($raseq - 1) * 96}] [expr {328 + ($raseq - 1) * 96}]]
			#Type
			set position [lsearch $raentry "Type"]
			if {$position != -1} {
				set ratype [string range $raprefix 0 1]
				set ratype "0x$ratype"
				set ratype [format "%i" $ratype]
				set res [expr $res * [expr {$ratype == [lindex $raentry [expr $position + 1]]}]]
			}
			#Length
			set position [lsearch $raentry "Length"]
			if {$position != -1} {
				set ralength [string range $raprefix 3 4]
				set ralength "0x$ralength"
				set ralength [format "%i" $ralength]
				set res [expr $res * [expr {$ralength == [lindex $raentry [expr $position + 1]]}]]
			}
			#PrefixLength
			set position [lsearch $raentry "PrefixLength"]
			if {$position != -1} {
				set raprefixlength [string range $raprefix 6 7]
				set raprefixlength "0x$raprefixlength"
				set raprefixlength [format "%i" $raprefixlength]
				set res [expr $res * [expr {$raprefixlength == [lindex $raentry [expr $position + 1]]}]]
			}
			#Link
			set position [lsearch $raentry "Link"]
			if {$position != -1} {
				set ralink [string range $raprefix 9 9]
				set ralink "0x$ralink"
				set ralink [expr [expr {$ralink & 8}]==8?1:0]
				set res [expr $res * [expr {$ralink == [lindex $raentry [expr $position + 1]]}]]
			}
			#Autonomous
			set position [lsearch $raentry "Autonomous"]
			if {$position != -1} {
				set raautonomous [string range $raprefix 9 9]
				set raautonomous "0x$raautonomous"
				set raautonomous [expr [expr {$raautonomous & 4}]==4?1:0]
				set res [expr $res * [expr {$raautonomous == [lindex $raentry [expr $position + 1]]}]]
			}
			#NotRouter
			set position [lsearch $raentry "NotRouter"]
			if {$position != -1} {
				set ranotrouter [string range $raprefix 9 9]
				set ranotrouter "0x$ranotrouter"
				set ranotrouter [expr [expr {$ranotrouter & 2}]==2?1:0]
				set res [expr $res * [expr {$ranotrouter == [lindex $raentry [expr $position + 1]]}]]
			}
			#SitePrefix
			set position [lsearch $raentry "SitePrefix"]
			if {$position != -1} {
				set rasiteprefix [string range $raprefix 9 9]
				set rasiteprefix "0x$rasiteprefix"
				set rasiteprefix [expr {$rasiteprefix & 1}]
				set res [expr $res * [expr {$rasiteprefix == [lindex $raentry [expr $position + 1]]}]]
			}
			#ValidTime
			set position [lsearch $raentry "ValidTime"]
			if {$position != -1} {
				set ravalidtime [string range $raprefix 12 22]
				regsub -all " " $ravalidtime "" ravalidtime 
				set ravalidtime "0x$ravalidtime"
				set ravalidtime [format "%u" $ravalidtime]
				set res [expr $res * [expr {$ravalidtime == [lindex $raentry [expr $position + 1]]}]]
			}
			#PreferredTime
			set position [lsearch $raentry "PreferredTime"]
			if {$position != -1} {
				set rapreferredtime [string range $raprefix 24 34]
				regsub -all " " $rapreferredtime "" rapreferredtime 
				set rapreferredtime "0x$rapreferredtime"
				set rapreferredtime [format "%u" $rapreferredtime]
				set res [expr $res * [expr {$rapreferredtime == [lindex $raentry [expr $position + 1]]}]]
			}
			#Prefix
			set position [lsearch $raentry "Prefix"]
			if {$position != -1} {
				set raPrefixfield [string range $raprefix 48 end]
				regsub -all " " $raPrefixfield "" raPrefixfield 
				set n1 [string range $raPrefixfield 0 3]
			    set n2 [string range $raPrefixfield 4 7]
			    set n3 [string range $raPrefixfield 8 11]
			    set n4 [string range $raPrefixfield 12 15]
			    set n5 [string range $raPrefixfield 16 19]
			    set n6 [string range $raPrefixfield 20 23]
			    set n7 [string range $raPrefixfield 24 27]
			    set n8 [string range $raPrefixfield 28 31]
				set raPrefixfield $n1
   				append raPrefixfield ":" "$n2" ":" "$n3" ":" "$n4" ":" "$n5" ":" "$n6" ":" "$n7" ":" "$n8"
				set res [expr $res * [expr {$raPrefixfield == [FormatIpv6 [lindex $raentry [expr $position + 1]]]}]]
			}
		} else {
			return 0
		}
	}
	return $res
}

#add by qiaoyua 2010.1.22
#判断Icmpv6 MTU可选项
#MtuOption {PrefixNum 2 Type 5 Length 1 Mtu 1000}
#PrefixNum是发送RA报文的接口所配置的Ipv6地址的数量
proc CheckMtuOptionInData { type data } {
	set res 1
	set mtuposition [lsearch $type "PrefixNum"]
	if {$mtuposition != -1} {
		set mtuprefixnum [lindex $type [expr $mtuposition + 1]]
		if {[string length $data] > [expr {352 + ($mtuprefixnum - 1) * 96}]} {
			#Type
			set position [lsearch $type "Type"]
			if {$position != -1} {
				set ratype [string range $data [expr {330 + ($mtuprefixnum - 1) * 96}] [expr {331 + ($mtuprefixnum - 1) * 96}]]
				set ratype "0x$ratype"
				set ratype [format "%i" $ratype]
				set res [expr $res * [expr {$ratype == [lindex $type [expr $position + 1]]}]]
			}
			#Length
			set position [lsearch $type "Length"]
			if {$position != -1} {
				set ralength [string range $data [expr {333 + ($mtuprefixnum - 1) * 96}] [expr {334 + ($mtuprefixnum - 1) * 96}]]
				set ralength "0x$ralength"
				set ralength [format "%i" $ralength]
				set res [expr $res * [expr {$ralength == [lindex $type [expr $position + 1]]}]]
			}
			#Mtu
			set position [lsearch $type "Mtu"]
			if {$position != -1} {
				set ramtu [string range $data [expr {342 + ($mtuprefixnum - 1) * 96}] [expr {352 + ($mtuprefixnum - 1) * 96}]]
				regsub -all " " $ramtu "" ramtu 
				set ramtu "0x$ramtu"
				set ramtu [format "%i" $ramtu]
				set res [expr $res * [expr {$ramtu == [lindex $type [expr $position + 1]]}]]
			}
		} else {
			return 0
		}
	} else {
		return 0
	}
	return $res
}


#add by qiaoyua 2010.1.22
#判断Icmpv6 Ra报文相关字段
#Icmpv6Ra {HopLimit 0 ManageAdd 0 OtherState 0 RouterLifeTime 1800 ReachableTime 0 RetransTime 0}
proc CheckIcmpv6RaInData { type data } {
	set res 1
	if {[string length $data] > 210} {
		#HopLimit
		set position [lsearch $type "HopLimit"]
		if {$position != -1} {
			set rahoplimit [string range $data 174 175]
			set rahoplimit "0x$rahoplimit"
			set rahoplimit [format "%i" $rahoplimit]
			set res [expr $res * [expr {$rahoplimit == [lindex $type [expr $position + 1]]}]]
		}
		#ManageAdd
		set position [lsearch $type "ManageAdd"]
		if {$position != -1} {
			set ramanageadd [string range $data 177 177]
			set ramanageadd "0x$ramanageadd"
			set ramanageadd [expr [expr {$ramanageadd & 8}]==8?1:0]
			set res [expr $res * [expr {$ramanageadd == [lindex $type [expr $position + 1]]}]]
		}
		#OtherState
		set position [lsearch $type "OtherState"]
		if {$position != -1} {
			set raotheratate [string range $data 177 177]
			set raotheratate "0x$raotheratate"
			set raotheratate [expr [expr {$raotheratate & 4}]==4?1:0]
			set res [expr $res * [expr {$raotheratate == [lindex $type [expr $position + 1]]}]]
		}
		#RouterLifeTime
		set position [lsearch $type "RouterLifeTime"]
		if {$position != -1} {
			set rarouterlifetime [string range $data 180 184]
			regsub -all " " $rarouterlifetime "" rarouterlifetime 
			set rarouterlifetime "0x$rarouterlifetime"
			set rarouterlifetime [format "%u" $rarouterlifetime]
			set res [expr $res * [expr {$rarouterlifetime == [lindex $type [expr $position + 1]]}]]
		}
		#ReachableTime
		set position [lsearch $type "ReachableTime"]
		if {$position != -1} {
			set rareachabletime [string range $data 186 196]
			regsub -all " " $rareachabletime "" rareachabletime 
			set rareachabletime "0x$rareachabletime"
			set rareachabletime [format "%u" $rareachabletime]
			set res [expr $res * [expr {$rareachabletime == [lindex $type [expr $position + 1]]}]]
		}
		#RetransTime
		set position [lsearch $type "RetransTime"]
		if {$position != -1} {
			set raretranstime [string range $data 198 208]
			regsub -all " " $raretranstime "" raretranstime 
			set raretranstime "0x$raretranstime"
			set raretranstime [format "%u" $raretranstime]
			set res [expr $res * [expr {$raretranstime == [lindex $type [expr $position + 1]]}]]
		}
	} else {
		return 0
	}
	return $res
}

#add by qiaoyua 2010.1.22
#判断Icmpv6 Redirect报文相关字段
#Icmpv6Redirect {TargetAddr 2000::3 DesAddr 2002::2 DesOption {LinkAddr 00-00-00-00-00-02}}
proc CheckIcmpv6RedirectInData { type data } {
	set res 1
	if {[string length $data] > 306} {
		#TargetAddr
		set position [lsearch $type "TargetAddr"]
		if {$position != -1} {
			set redirecttarget [string range $data 186 232]
			regsub -all " " $redirecttarget "" redirecttarget 
			set n1 [string range $redirecttarget 0 3]
		    set n2 [string range $redirecttarget 4 7]
		    set n3 [string range $redirecttarget 8 11]
		    set n4 [string range $redirecttarget 12 15]
		    set n5 [string range $redirecttarget 16 19]
		    set n6 [string range $redirecttarget 20 23]
		    set n7 [string range $redirecttarget 24 27]
		    set n8 [string range $redirecttarget 28 31]
			set redirecttarget $n1
				append redirecttarget ":" "$n2" ":" "$n3" ":" "$n4" ":" "$n5" ":" "$n6" ":" "$n7" ":" "$n8"
			set res [expr $res * [expr {$redirecttarget == [FormatIpv6 [lindex $type [expr $position + 1]]]}]]
		}
		#DesAddr
		set position [lsearch $type "DesAddr"]
		if {$position != -1} {
			set redirectdes [string range $data 234 280]
			regsub -all " " $redirectdes "" redirectdes 
			set n1 [string range $redirectdes 0 3]
		    set n2 [string range $redirectdes 4 7]
		    set n3 [string range $redirectdes 8 11]
		    set n4 [string range $redirectdes 12 15]
		    set n5 [string range $redirectdes 16 19]
		    set n6 [string range $redirectdes 20 23]
		    set n7 [string range $redirectdes 24 27]
		    set n8 [string range $redirectdes 28 31]
			set redirectdes $n1
				append redirectdes ":" "$n2" ":" "$n3" ":" "$n4" ":" "$n5" ":" "$n6" ":" "$n7" ":" "$n8"
			set res [expr $res * [expr {$redirectdes == [FormatIpv6 [lindex $type [expr $position + 1]]]}]]
		}
		#DesOption
		set position [lsearch $type "DesOption"]
		if {$position != -1} {
			array set desoption [lindex $type [expr $position + 1]]
			if [info exists desoption(LinkAddr)] {
				set redirectlink [string range $data 288 304]
				regsub -all " " $redirectlink "-" redirectlink
				set res [expr $res * [expr {$redirectlink == $desoption(LinkAddr)}]]
			}
		}
	} else {
		return 0
	}
	return $res
}


#add by zhangfank
proc CheckIcmpv6TypeInData { type data } {
	#add by zhaohj 带有vlan tag的情况
	set vlantag [ string range $data 36 40 ]
	#判断报文是否带有vlan Tag
	if { $vlantag == "81 00" } {        
        set var [ string range $data 72 73 ]
        set var "0x0$var"
        set var [ format "%i" $var ]
        if { $var == 58 } {
            #只有一个icmpv6头，无其他扩展头的情况
            set data [ string range $data 174 175 ]
            set data "0x0$data"
            set data [ format "%i" $data ]
            if { $data == $type } {
                return 1
            } else {
                return 0
            }
        } else {
            #带一个除icmpv6以外ipv6扩展头的情况
            set data [ string range $data 198 199 ]
            set data "0x0$data"
            set data [ format "%i" $data ]
            if { $data == $type } {
                return 1
            } else {
                return 0
            }
        }
     } else {
        set var [ string range $data 60 61 ]
        set var "0x0$var"
        set var [ format "%i" $var ]
        if { $var == 58 } {
            #只有一个icmpv6头，无其他扩展头的情况
            set data [ string range $data 162 163 ]
            set data "0x0$data"
            set data [ format "%i" $data ]
            if { $data == $type } {
                return 1
            } else {
                return 0
            }
        } else {
            #带一个除icmpv6以外ipv6扩展头的情况
            set data [ string range $data 186 187 ]
            set data "0x0$data"
            set data [ format "%i" $data ]
            if { $data == $type } {
                return 1
            } else {
                return 0
            }
        }
     }
}        


#add by zhaohj
proc CheckIcmpv6CodeInData { code data } {
	set vlantag [ string range $data 36 40 ]
	#判断报文是否带有vlan Tag
	if { $vlantag == "81 00" } {        
        set var [ string range $data 72 73 ]
        set var "0x0$var"
        set var [ format "%i" $var ]
        if { $var == 58 } {
            #只有一个icmpv6头，无其他扩展头的情况
            set data [ string range $data 177 178 ]
            set data "0x0$data"
            set data [ format "%i" $data ]
            if { $data == $code } {
                return 1
            } else {
                return 0
            }
        } else {
            #带一个除icmpv6以外ipv6扩展头的情况
            set data [ string range $data 201 202 ]
            set data "0x0$data"
            set data [ format "%i" $data ]
            if { $data == $code } {
                return 1
            } else {
                return 0
            }
        }
     } else {
        set var [ string range $data 60 61 ]
        set var "0x0$var"
        set var [ format "%i" $var ]
        if { $var == 58 } {
            #只有一个icmpv6头，无其他扩展头的情况
            set data [ string range $data 165 166 ]
            set data "0x0$data"
            set data [ format "%i" $data ]
            if { $data == $code } {
                return 1
            } else {
                return 0
            }
        } else {
            #带一个除icmpv6以外ipv6扩展头的情况
            set data [ string range $data 189 190 ]
            set data "0x0$data"
            set data [ format "%i" $data ]
            if { $data == $code } {
                return 1
            } else {
                return 0
            }
        }
     }
}



#add by zhaohj
proc CheckIcmpv6OffsetInData { offset data } {
	set vlantag [ string range $data 36 40 ]
	#判断报文是否带有vlan Tag
	if { $vlantag == "81 00" } {        
        set var [ string range $data 72 73 ]
        set var "0x0$var"
        set var [ format "%i" $var ]
        if { $var == 44 } {
            #只有一个fragment header和一个icmpv6头，无其他扩展头的情况
            set data [ string range $data 180 184 ]
            if { $data == $offset } {
                return 1
            } else {
                return 0
            }
        } else {
            #带一个除icmpv6以外ipv6扩展头的情况
            set data [ string range $data 204 208 ]
            if { $data == $offset } {
                return 1
            } else {
                return 0
            }
        }
     } else {
        set var [ string range $data 60 61 ]
        set var "0x0$var"
        set var [ format "%i" $var ]
        if { $var == 44 } {
            #只有一个fragment header和一个icmpv6头，无其他扩展头的情况
            set data [ string range $data 168 172 ]
            if { $data == $offset } {
                return 1
            } else {
                return 0
            }
        } else {
            #带一个除icmpv6以外ipv6扩展头的情况
            set data [ string range $data 192 196 ]
            if { $data == $offset } {
                return 1
            } else {
                return 0
            }
        }
     }
}        


#add by zhaohj 2009.11.2
#判断Icmpv6 Data字段，支持带vlan tag,不支持除icmpv6以外ipv6扩展头的情况
proc CheckIcmpv6DataInData { type data } {
	set tag [ string range $data 36 40 ]
	set length [ string length $data]
	#判断报文是否带有vlan Tag
	if [string match $tag "81 00"] {
		set fragmentflag [ string range $data 181 184 ]
		if [string match $fragmentflag "0 01"] {
			set icmpdata [ string range $data 222 end-10 ]
			set num [regsub -all -nocase "$type " $icmpdata "" ignore]
	        set len [expr {($length-11-222)/3}]
	        if {$num == $len} {
		    	return 1
			}
        } else {
			set icmpdata [ string range $data 114 end-10 ]
			set num [regsub -all -nocase "$type " $icmpdata "" ignore]
	        set len [expr {($length-11-114)/3}]
	        if {$num == $len} {
		    	return 1
			}
        }
	} else {
		set fragmentflag [ string range $data 169 172 ]
		if [string match $fragmentflag "0 01"] {
			set icmpdata [ string range $data 210 end-10 ]
			set num [regsub -all -nocase "$type " $icmpdata "" ignore]
	        set len [expr {($length-11-210)/3}]
	        if {$num == $len} {
		    	return 1
			}
        } else {
			set icmpdata [ string range $data 186 end-10 ]
			set num [regsub -all -nocase "$type " $icmpdata "" ignore]
	        set len [expr {($length-11-186)/3}]
	        if {$num == $len} {
		    	return 1
			}
        }
	}
	return 0
}


##add by zhaohj 2010-11-03
##CheckCaptureStream $chasId $Card1 $Port1 PppoeTlvType "01 05"
proc CheckPppoeTlvTypeInData { type data } {
	set data [ string range $data 72 76 ]
        if { $data == $type } {
        	return 1
        } else {
            return 0
        }
}


#########################################################################################
# CheckTotalLengthInData: 检查抓到的包的IP报文长度是否满足镜像要求
#
# args:
#		len: request length of IP packet
#		data: actual frame data
#		
# return:
#		1: 长度符合要求
#		0：长度不符合要求
#########################################################################################
#added by zhangfank 2009-04-28
proc CheckTotalLengthInData { len data } {
		set data [string range $data 48 52]
		set n1 [string range $data 0 1]
		set n2 [string range $data 3 4]
		set n $n1$n2
		set n "0x0$n"
		set n [format "%i" $n]
		if {$n == $len} {
		    return 1
		} else {
		    return 0
		}
	}

#########################################################################################
# CheckPayloadLengthInData:检查抓到的IPv6包的载荷长度是否满足镜像要求
#
# args:
#		len: request payloadlength of IP packet
#		data: actual frame data
#		
# return:
#		1: 长度符合要求
#		0：长度不符合要求
#########################################################################################
#added by zhangfank 2009-04-29
proc CheckPayloadLengthInData { len data } {
		set data [string range $data 54 58]
		set n1 [string range $data 0 1]
		set n2 [string range $data 3 4]
		set n $n1$n2
		set n "0x0$n"
		set n [format "%i" $n]
		if {$n == $len} {
		    return 1
		} else {
		    return 0
		}
	}
	
#########################################################################################
# CheckFragmentFlagInData: 检查抓到的IPv4包是否是分片包
#
# args：
#		flag：
#			1：Fragment
#			0：Don't fragment
#		data：actual frame data
#
# return:
#		1:报文是分片报文
#		0:报文不是分片报文
#########################################################################################
#added by zhangfank 2009-04-28
proc CheckFragmentFlagInData { flag data } {
        set data [string index $data 60]
        set n "0x0$data"
        set n [ format "%i" $n ]
        if {$flag == 1} {
                if {$n!= 4} {
                        return 1
                } else {
                        return 0
                }
        } else {
                if {$n==4} {
                        return 1
                } else {
                        return 0
                }
        }
}

#########################################################################################
# CheckFragmentHeaderInData: 检查IPv6报文是否是分片报文
#
# args:
#        flag: 
#                1: more fragment
#                0: don't fragment
#        data: 
#                actual frame data
#
# return:
#        1: 符合分片要求
#        0: 不符合分片要求
#########################################################################################
#added by zhangfank 2009-04-29
proc CheckFragmentHeaderInData { flag data } {
        set data [ string range $data 60 61 ]
        set n "0x0$data"
        set n [ format "%i" $n ]
        if { $flag == 1 } {
            if {$n == 44} {
                return 1
            } else {
                return 0
            }
        } else {
            if {$n != 44} {
                return 1
            } else {
                return 0
            }
        }
}        



proc CheckFINInData { record data } {
	set flag [string range $data 36 40]
    if  { $flag == "81 00" } {
        #vlantag
        set TcpFlag [string range $data 153 154]
        set TcpFlag "0x0$TcpFlag"
        set TcpFlag [format %d $TcpFlag]
    } else {
        #no vlantag
        set TcpFlag [string range $data 141 142]
        set TcpFlag "0x0$TcpFlag"
        set TcpFlag [format %d $TcpFlag]   
    }
    if { [expr $TcpFlag & 1] == 1 && $record == "true" || [expr $TcpFlag & 1] != 1 && $record == "false" } {
    	return 1
    } else {
    	return 0
    }
}
proc CheckSYNInData { record data } {
	set flag [string range $data 36 40]
    if  { $flag == "81 00" } {
        #vlantag
        set TcpFlag [string range $data 153 154]
        set TcpFlag "0x0$TcpFlag"
        set TcpFlag [format %d $TcpFlag]
    } else {
        #no vlantag
        set TcpFlag [string range $data 141 142]
        set TcpFlag "0x0$TcpFlag"
        set TcpFlag [format %d $TcpFlag]	
    }
    if { [expr $TcpFlag & 2] == 2 && $record == "true" || [expr $TcpFlag & 2] != 2 && $record == "false" } {
    	return 1
    } else {
    	return 0
    }
}
proc CheckRSTInData { record data } {
	set flag [string range $data 36 40]
    if  { $flag == "81 00" } {
        #vlantag
        set TcpFlag [string range $data 153 154]
        set TcpFlag "0x0$TcpFlag"
        set TcpFlag [format %d $TcpFlag]
    } else {
        #no vlantag
        set TcpFlag [string range $data 141 142]
        set TcpFlag "0x0$TcpFlag"
        set TcpFlag [format %d $TcpFlag]	
    }
    if { [expr $TcpFlag & 4] == 4 && $record == "true" || [expr $TcpFlag & 4] != 4 && $record == "false" } {
    	return 1
    } else {
    	return 0
    }
}
proc CheckPSHInData { record data } {
	set flag [string range $data 36 40]
    if  { $flag == "81 00" } {
        #vlantag
        set TcpFlag [string range $data 153 154]
        set TcpFlag "0x0$TcpFlag"
        set TcpFlag [format %d $TcpFlag]
    } else {
        #no vlantag
        set TcpFlag [string range $data 141 142]
        set TcpFlag "0x0$TcpFlag"
        set TcpFlag [format %d $TcpFlag]	
    }
    if { [expr $TcpFlag & 8] == 8 && $record == "true" || [expr $TcpFlag & 8] != 8 && $record == "false" } {
    	return 1
    } else {
    	return 0
    }
}
proc CheckACKInData { record data } {
	set flag [string range $data 36 40]
    if  { $flag == "81 00" } {
        #vlantag
        set TcpFlag [string range $data 153 154]
        set TcpFlag "0x0$TcpFlag"
        set TcpFlag [format %d $TcpFlag]
    } else {
        #no vlantag
        set TcpFlag [string range $data 141 142]
        set TcpFlag "0x0$TcpFlag"
        set TcpFlag [format %d $TcpFlag]	
    }
    if { [expr $TcpFlag & 16] == 16 && $record == "true" || [expr $TcpFlag & 16] != 16 && $record == "false" } {
    	return 1
    } else {
    	return 0
    }
}
proc CheckURGInData { record data } {
	set flag [string range $data 36 40]
    if  { $flag == "81 00" } {
        #vlantag
        set TcpFlag [string range $data 153 154]
        set TcpFlag "0x0$TcpFlag"
        set TcpFlag [format %d $TcpFlag]
    } else {
        #no vlantag
        set TcpFlag [string range $data 141 142]
        set TcpFlag "0x0$TcpFlag"
        set TcpFlag [format %d $TcpFlag]	
    }
    if { [expr $TcpFlag & 32] == 32 && $record == "true" || [expr $TcpFlag & 32] != 32 && $record == "false" } {
    	return 1
    } else {
    	return 0
    }
}

#added by zhangfank,2009.9.7
proc CheckIgmpTypeInData { type data } {
	set flag [string range $data 36 40]
	if { $flag == "81 00" } {
		#vlantag
		set igmptype [string range $data 114 115]
		set igmptype "0x0$igmptype"
		set igmptype [format %d $igmptype]
	} else {
		#no vlantag
		set igmptype [string range $data 102 103]
		set igmptype "0x0$igmptype"
		set igmptype [format %d $igmptype]
	}
	if { $igmptype == $type } {
		return 1
	} else {
		return 0
	}
}	


#modified by zhangfank,check L4SPort in ipv4/v6 packet,2009.9.21
proc CheckSPortInData { record data } {
	set flag [string range $data 36 40]
    if  { $flag == "81 00" } {
        #vlantag
        set version [string index $data 54]
        if { $version == 4 } {
        	set sport [string range $data 114 118]
        }
        if { $version == 6 } {
        	set sport [string range $data 174 178]
        }
    } else {
        if { $flag == "08 00" } {
        #ipv4 packet and no tag
        	set sport [string range $data 102 106]
        }
        if { $flag == "86 DD" } {
        #ipv6 packet and no tag
        	set sport [string range $data 162 166]
        }	
    }
    if { ![info exists sport] } {
	return 0
    }
    regsub -all {\s} $sport "" sport
    if { [format %d 0x0$sport] == $record } {
        return 1
    } else {
        return 0
    }
}


#modified by zhangfank,check L4DPort in ipv4/v6 packet,2009.9.21
#modified by liuruij,check line5:set version [string index $data 54],2010.9.6
proc CheckDPortInData { record data } {
	set flag [string range $data 36 40]
    if  { $flag == "81 00" } {
        #vlantag
        set version [string index $data 54]
        if { $version == 4 } {
        	set dport [string range $data 120 124]
        }
        if { $version == 6 } {
        	set dport [string range $data 180 184]
        }	
    } else {
    	if { $flag == "08 00" } {
    	#ipv4 and no vlantag
        	set dport [string range $data 108 112]
        }
        if { $flag == "86 DD" } {
        #ipv6 and no vlantag
        	set dport [string range $data 168 172]
        }	     }
    #增加变量存在性判断，防止跳出
    if {![info exist dport]} {
    	return 0
    }	
    regsub -all {\s} $dport "" dport
    if { [format %d 0x0$dport] == $record } {
        return 1
    } else {
        return 0
    }
}
proc CheckDhcpMessageTypeInData { record data } {
	set flag [string range $data 36 40]
    if  { $flag == "81 00" } {
        #vlantag
        set DhcpMessageType [string range $data 865 866]
    } else {
        #no vlantag
        set DhcpMessageType [string range $data 853 854]
    }
#    puts $DhcpMessageType
#    regsub -all {\s} $DhcpMessageType "" DhcpMessageType
    if { $DhcpMessageType == $record } {
        #puts aa
        return 1
    } else {
        return 0
    }
}
proc CheckTosInData { record data } {
	set flag [string range $data 36 40]
    if  { $flag == "81 00" } {
        #vlantag
        set Tos [format %d 0x0[string range $data 57 58]]
    } else {
        #no vlantag
        set Tos [format %d 0x0[string range $data 45 46]]
        
    }
    if { [expr {($Tos & 30) / 2 }] == $record } {
        return 1
    } else {
        return 0
    }
}
proc CheckTOSBitsInData { record data } {
	set flag [string range $data 36 40]
    if  { $flag == "81 00" } {
        #vlantag
        set Tosbits [format %d 0x0[string range $data 57 58]]
    } else {
        #no vlantag
        set Tosbits [format %d 0x0[string range $data 45 46]]
    }
    if { $Tosbits == $record } {
        #puts aa
        return 1
    } else {
        return 0
    }
}

proc CheckIpprecedenceInData { record data } {
	set flag [string range $data 36 40]
    if  { $flag == "81 00" } {
        #vlantag
        set version [string  index $data 54]
        if { $version == 4} {
        set Tos [format %d 0x0[string range $data 57 58]]
        } elseif {  $version == 6 } {
            set precstring [string range $data 55 57]
            set precstring [string replace $precstring 1 1]
            set Tos  [format %d 0x0$precstring]
        }
    } else {
        #no vlantag
        set version [string  index $data 42]
         if { $version == 4} {
            set Tos [format %d 0x0[string range $data 45 46]]
        } elseif { $version == 6 } {
            set precstring [string range $data 43 45]
            set precstring [string replace $precstring 1 1]
            set Tos  [format %d 0x0$precstring]
        }
    }
    if {![info exist Tos]} {
    	return 0
    }	
    if { [expr $Tos >> 5] == $record } {
        #puts aa
        return 1
    } else {
        return 0
    }
}
proc CheckDSCPInData { record data } {
	set flag [string range $data 36 40]
    if  { $flag == "81 00" } {
        #vlantag
        set version [string  index $data 54]
        if { $version == 4} {
            #ipv4 protocol
            set dscp [format %d 0x0[string range $data 57 58]]
        } elseif { $version == 6 } {
            #ipv6 protocol
            set dscpstring [string range $data 55 57]
            set dscpstring [string replace $dscpstring 1 1]
            set dscp  [format %d 0x0$dscpstring]
        } else { #802.3snap packet
            set version1 [string  index $data 78]
            if { $version1 == 4} {
                set dscp [format %d 0x0[string range $data 81 82]]
            } elseif { $version1 == 6 } {
                set dscpstring [string range $data 79 81]
                set dscpstring [string replace $dscpstring 1 1]
                set dscp  [format %d 0x0$dscpstring]
            }
      	}
      	set dscnp [expr $dscp >> 2]
    } elseif { $flag == "08 00" } {
        #no vlantag && ipv4 protocol
      	set dscp [format %d 0x0[string range $data 45 46]]
      	set dscp [expr $dscp >> 2]
    } elseif { $flag == "86 DD"} {
        #no vlantag && ipv6 protocol
        set dscpstring [string range $data 43 45]
        set dscpstring [string replace $dscpstring 1 1]
        set dscp  [format %d 0x0$dscpstring]
        set dscp [expr $dscp >> 2]
    }

#    if { $dscp == $record } {
#        return 1
#    } else {
#        return 0
#    }
#modify by zhangfank,2010.3.15
	if {[info exist dscp]} {
		if {$dscp == $record} {
			return 1
		} else {
			return 0
		}
	} else {
		PrintRes Print "!Can't get dscp in packets!"
		return 0
	}	
}

    

####edit by gengtao 2011.2.21  
#proc CheckFlowlabelInData { record data } {
#    set flag [string range $data 48 52]
#    if  { $flag == "86 DD" } {
#        #Get Flowlabel
#        set Flowlabelstring [string range $data 58 64]
#    } else {
#        set Flowlabelstring [string range $data 70 76]
#    }
#        set Flowlabelstring [string replace $Flowlabelstring 1 1]
#        set Flowlabelstring [string replace $Flowlabelstring 3 3 ]  
#        set Flowlabel [format %d 0x0$Flowlabelstring]
#        if { $Flowlabel == $record } {
#            return 1
#        } else {
#            return 0
#        }
#
#}

proc CheckFlowlabelInData { record data } {
    set flag [string range $data 36 40]
    if  { $flag == "81 00" } {
        #Get Flowlabel
        set Flowlabelstring [string range $data 58 64]
    } else {
        set Flowlabelstring [string range $data 46 52]
    }
        set Flowlabelstring [string replace $Flowlabelstring 1 1]
        set Flowlabelstring [string replace $Flowlabelstring 3 3 ] 
        set Flowlabel [format %d 0x0$Flowlabelstring]
        if { $Flowlabel == $record } {
            return 1
        } else {
            return 0
        }
}

proc CheckTypeInData { record data } {
	set flag [string range $data 36 40]
    if  { $flag == "81 00" } {
        #vlantag
        set Type [format %d 0x0[string range $data 114 115]]
    } else {
        #no vlantag
        set Type [format %d 0x0[string range $data 102 103]]
    }
    if { $Type == $record } {
        #puts aa
        return 1
    } else {
        return 0
    }
}
proc CheckCodeInData { record data } {
	set flag [string range $data 36 40]
    if  { $flag == "81 00" } {
        #vlantag
        set Code [format %d 0x0[string range $data 117 118]]
    } else {
        #no vlantag
        set Code [format %d 0x0[string range $data 105 106]]
    }
    if { $Code == $record } {
        #puts aa
        return 1
    } else {
        return 0
    }
}
proc CheckProtocolExInData { record data } {
	set flag [string range $data 36 40]
    if  { $flag == "81 00" } {
        #vlantag
        set protocolEx [string range $data 81 82]
    } else {
        #no vlantag
        set protocolEx [string range $data 69 70]
    }
    switch -exact $record {
    	tcp {set record 6}
    	udp {set record 17}
    	rip {set record 17}
    	icmp {set record 1}
    	igmp {set record 2}
    	defaut {}
    }
    if { [format %d 0x0$protocolEx] == $record } {
        #puts aa
        return 1
    } else {
        return 0
    }
}

proc CheckEthernetTypeInData { record data } {
	set flag [string range $data 36 40]
	if { $flag == "81 00" } {
		set flag [string range $data 48 52]
	}
    if  { $record == "loopback" && $flag == "DC 09" } {
        return 1
    } else {
    	return 0
    }
}

#CheckCaputreStream $chas $card $port SrcMac $s1cpumac DstMac 01-00-0c-cc-cc-cc ULDP [list ULDPType hello HelloInterval 10 \
#                      DeviceMac $s1cpumac PortID [GetPortIndex $s1p1] Neighbor [list Mac $s1cpumac PortID [GetPortIndex $s1p1]]]
proc CheckULDPInData { record data } {
	array set arrArgs $record
	set res 1
	set flag [string range $data 36 40]
	if { $flag == "81 00" } {
		set uldprecord [string range $data 48 end-12]
	} else {
		set uldprecord [string range $data 36 end-12]
	}
	if {[info exists arrArgs(ULDPType)]} {
		switch -exact $arrArgs(ULDPType) {
			hello {
				set length 34
				set uldpid 1
				set version 1
				set type 1
				set flag 0
				set authmode 0
				set password 0		
			}
			rsy {
				set length 34
				set uldpid 1
				set version 1
				set type 1
				set flag 0x80
				set authmode 0
				set password 0		
			}
			flush {
				set length 34
				set uldpid 1
				set version 1
				set type 1
				set flag 0x40
				set authmode 0
				set password 0		
			}
			probe {
				set length 34
				set uldpid 1
				set version 1
				set type 2
				set flag 0
				set authmode 0
				set password 0		
			}
			echo {
				set length 42
				set uldpid 1
				set version 1
				set type 3
				set flag 0
				set authmode 0
				set password 0	
			}
			unidirection {
				set length 34
				set uldpid 1
				set version 1
				set type 4
				set flag 0
				set authmode 0
				set password 0	
			}
		}
		#Length
		set res [expr $res & (0x0[string range $uldprecord 0 1][string range $uldprecord 3 4]==$length?1:0)]
		#ULDPID
		set res [expr $res & (0x0[string range $uldprecord 6 7][string range $uldprecord 9 10]==$uldpid?1:0)]
		#Version
		set res [expr $res & (0x0[string range $uldprecord 12 13]==$version?1:0)]
		#Type
		set res [expr $res & (0x0[string range $uldprecord 15 16]==$type?1:0)]
		#Flag
		set res [expr $res & (0x0[string range $uldprecord 18 19]==$flag?1:0)]
		#AutoMode
		set res [expr $res & (0x0[string range $uldprecord 21 22]==$authmode?1:0)]
		#Password
		regsub -all " " [string range $uldprecord 24 70] "" pwd
		set res [expr $res & (0x0$pwd==$password?1:0)]
	} else {
		#Length
		if {[info exists arrArgs(Length)]} {
			set res [expr $res & (0x0[string range $uldprecord 0 1][string range $uldprecord 3 4]==$arrArgs(Length)?1:0)]   ;#length = 52/60
		}
		#ULDPID
		if {[info exists arrArgs(ULDPID)]} {
			set res [expr $res & (0x0[string range $uldprecord 6 7][string range $uldprecord 9 10]==$arrArgs(ULDPID)?1:0)]   ;#uldpid = 1
		}
		#Version
		if {[info exists arrArgs(Version)]} {
			set res [expr $res & (0x0[string range $uldprecord 12 13]==$arrArgs(Version)?1:0)]   ;#version = 1
		}
		#Type
		if {[info exists arrArgs(Type)]} {
			set res [expr $res & (0x0[string range $uldprecord 15 16]==$arrArgs(Type)?1:0)]   ;#version = 1
		}
		#Flag
		if {[info exists arrArgs(Flag)]} {
			set res [expr $res & (0x0[string range $uldprecord 18 19]==$arrArgs(Flag)?1:0)]   ;#flag = 0/0x80/0x40 
		}
		#AutoMode
		if {[info exists arrArgs(AutoMode)]} {
			set res [expr $res & (0x0[string range $uldprecord 21 22]==$arrArgs(AutoMode)?1:0)]   ;#automode = 0/1/2
		}
		#Password
		if {[info exists arrArgs(Password)]} {
			set res [expr $res & ([string equal [string range $uldprecord 24 70] $arrArgs(Password)]?1:0)]  
		}
	}
	#HelloInterval
	if {[info exists arrArgs(HelloInterval)]} {
		set res [expr $res & (0x0[string range $uldprecord 72 73][string range $uldprecord 75 76]==$arrArgs(HelloInterval)?1:0)]  
	}
	#reserved
	set res [expr $res & (0x0[string range $uldprecord 78 79][string range $uldprecord 81 82]==0?1:0)] 
	#DeviceMac
	if {[info exists arrArgs(DeviceMac)]} {
		regsub -all {\-} $arrArgs(DeviceMac) " " devicemac
		#puts [string range $uldprecord 84 100]
		#puts $devicemac
		set res [expr $res & ([string equal [string range $uldprecord 84 100] [string toupper $devicemac]]?1:0)]  
	}
	#PortID
	if {[info exists arrArgs(PortID)]} {
		set res [expr $res & (0x0[string range $uldprecord 102 103][string range $uldprecord 105 106]==$arrArgs(PortID)?1:0)]
	}
	#NeighborInfo
	if {[info exists arrArgs(NeighborInfo)]} {
		array set neighborinfo $arrArgs(NeighborInfo)
		if [info exists neighborinfo(Mac)] {
			regsub -all {\-} $neighborinfo(Mac) " " mac
			set res [expr $res & ([string equal [string range $uldprecord 108 124] [string toupper $mac]]?1:0)]  
		}
		if [info exists neighborinfo(PortID)] {
			set res [expr $res & (0x0[string range $uldprecord 126 127][string range $uldprecord 129 130]==$neighborinfo(PortID)?1:0)]
		}
	}
	return $res
}


#CheckCaputreStream $chas $card $port SrcMac $s1cpumac DstMac 01-80-c2-00-00-0e LLDP {LLDPType normal ChassisID {Subtype x ChassisID "xx xx xx"} \
#                      PortID {SubType x PortID "xx xx 32"} TTL 100 PortDescription "xx xx" SystemName "xx xx" SystemDescription "xx xx" \
#                      SystemCapabilities {SystemCapabilities "xx xx" Enablecapabilities 1} \
#                      ManagementAddress {Subtype x ManagementAddress "xx xx" InterfaceNumberingSubType x InterfaceNumber x OID "xx xx"}}
#CheckCaputreStream $chas $card $port SrcMac $s1cpumac DstMac 01-80-c2-00-00-0e LLDP {LLDPType shutdown ChassisID {Subtype x ChassisID "xx xx xx"} \
#                      PortID {SubType x PortID "xx xx"}}
#参数均可有可无
proc CheckLLDPInData { record data } {
	array set arrArgs $record
	set flag [string range $data 36 40]
	if { $flag == "81 00" } {
		set llpdrecord [string range $data 48 end-12]
	} else {
		set lldprecord [string range $data 36 end-12]
	}
	if { [string range $lldprecord 0 4] == "88 CC" } {
		if [info exists arrArgs(LLDPType)] {
			set lldptype $arrArgs(LLDPType)
			set res 1
			if [info exists arrArgs(SysDescripLength)] {
				upvar 2 $arrArgs(SysDescripLength) SysDescripLength
			}
			if { $lldptype == "normal" } {
				#chassis id tlv
				set start 6
				if { [expr [format %d 0x0[string range $lldprecord $start [expr $start + 1]]] >> 1] != 1 } {
					set res 0
				}
				set length [expr ([format %d 0x0[string range $lldprecord $start [expr $start + 1]]] << 8) % 512 + [format %d 0x0[string range $lldprecord [expr $start + 3] [expr $start + 4]]]]
				if [info exists arrArgs(ChassisID)] {
					array set chassisid $arrArgs(ChassisID)
					#chassis id subtype
					if [info exists chassisid(SubType)] {
						if { [format %d 0x0[string range $lldprecord [expr $start + 6] [expr $start + 7]]] != $chassisid(SubType) } {
							set res 0
						}
					}
					#chassis id
					if [info exists chassisid(ChassisID)] {
						if { [format %d 0x0[string range $lldprecord [expr $start + 6] [expr $start + 7]]] == 4 } {
							regsub -all {\-} $chassisid(ChassisID) " " cpumac
						} else {
							set cpumac $chassisid(ChassisID)
						}
						if { [string range $lldprecord [expr $start + 9] [expr $start + 9 + ($length - 1) * 3 - 2]] != [string toupper $cpumac] } {
							set res 0
						}
					}
				}
				#puts "start = $start, length = $length"
				#puts "chass id tlv = [string range $lldprecord $start [expr $start + 9 + ($length - 1) * 3 - 2]]"
				#port id tlv
				set start [expr $start + 9 + ($length - 1) * 3]
				if { [expr [format %d 0x0[string range $lldprecord $start [expr $start + 1]]] >> 1] != 2 } {
					set res 0
				}
				set length [expr ([format %d 0x0[string range $lldprecord $start [expr $start + 1]]] << 8) % 512 + [format %d 0x0[string range $lldprecord [expr $start + 3] [expr $start + 4]]]]
				if [info exists arrArgs(PortID)] {
					array set portid $arrArgs(PortID)
					#port id subtype
					if [info exists portid(SubType)] {
						if { [format %d 0x0[string range $lldprecord [expr $start + 6] [expr $start + 7]]] != $portid(SubType) } {
							set res 0
						}
					}
					#port id
					if [info exists portid(PortID)] {
						#puts [string range $lldprecord [expr $start + 9] [expr $start + 9 + ($length - 1) * 3 - 2]]
						#puts [string toupper $portid(PortID)]	
						
						#modified by zhaohj 2011-3-29
						set p1 [string last "/" $portid(PortID)]
						set portindex [string range $portid(PortID) [expr $p1 + 1] [expr $p1 + 1]]
						set p2 [string first "/" $portid(PortID)]
						set slotnum [string range $portid(PortID) [expr $p2 - 1] [expr $p2 - 1]]
						if {$slotnum == 0} {
							set slotnum 1
						}
						set portidindex [FormattoASCII [expr ($slotnum - 1) * 64 + $portindex]]
						
						if { [string range $lldprecord [expr $start + 9] [expr $start + 9 + ($length - 1) * 3 - 2]] != [string toupper $portidindex] } {
							set res 0
						}
						##modified by zhaohj 2011-3-29 end					
					}
				}
				#puts "port id tlv = [string range $lldprecord $start [expr $start + 9 + ($length - 1) * 3 - 2]]"
				#ttl tlv
				set start [expr $start + 9 + ($length - 1) * 3]
				if { [expr [format %d 0x0[string range $lldprecord $start [expr $start + 1]]] >> 1] != 3 } {
					set res 0
				}
				set length [expr ([format %d 0x0[string range $lldprecord $start [expr $start + 1]]] << 8) % 512 + [format %d 0x0[string range $lldprecord [expr $start + 3] [expr $start + 4]]]]
				if { $length != 2 } {
					set res 0
				}
				if [info exists arrArgs(TTL)] {
					#ttl
					if { [format %d 0x0[string range $lldprecord [expr $start + 6] [expr $start + 7]][string range $lldprecord [expr $start + 9] [expr $start + 10]]] != $arrArgs(TTL) } {
						set res 0
					}
				}
				#puts "ttl tlv = [string range $lldprecord $start [expr $start + 10]]"
				#optional tlv
				#first
				set start [expr $start + 6 + $length * 3]
				set type [expr [format %d 0x0[string range $lldprecord $start [expr $start + 1]]] >> 1]
				switch -exact $type {
					4 {
						#port description tlv
						set length [expr ([format %d 0x0[string range $lldprecord $start [expr $start + 1]]] << 8) % 512 + [format %d 0x0[string range $lldprecord [expr $start + 3] [expr $start + 4]]]]
						if [info exists arrArgs(PortDescription)] {
						puts [string range $lldprecord [expr $start + 6] [expr $start + 6 + $length * 3 - 2]]
						puts [string toupper $arrArgs(PortDescription)]
							if { [string range $lldprecord [expr $start + 6] [expr $start + 6 + $length * 3 - 2]] != [string toupper [FormattoASCII $arrArgs(PortDescription)]] } {
								set res 0
							}
						}
					}
					5 {
						#system name tlv
						set length [expr ([format %d 0x0[string range $lldprecord $start [expr $start + 1]]] << 8) % 512 + [format %d 0x0[string range $lldprecord [expr $start + 3] [expr $start + 4]]]]
						if [info exists arrArgs(SystemName)] {
							if { [string range $lldprecord [expr $start + 6] [expr $start + 6 + $length * 3 - 2]] != [string toupper [FormattoASCII $arrArgs(SystemName)]] } {
								set res 0
							}
						}
					}
					6 {
						#system description tlv
						set length [expr ([format %d 0x0[string range $lldprecord $start [expr $start + 1]]] << 8) % 512 + [format %d 0x0[string range $lldprecord [expr $start + 3] [expr $start + 4]]]]
						set SysDescripLength $length
						if [info exists arrArgs(SystemDescription)] {
							if { [string range $lldprecord [expr $start + 6] [expr $start + 6 + $length * 3 - 2]] != [string toupper [FormattoASCII $arrArgs(SystemDescription)]] } {
								set res 0
							}
						}
					}
					7 {
						#system capabilities tlv
						set length [expr ([format %d 0x0[string range $lldprecord $start [expr $start + 1]]] << 8) % 512 + [format %d 0x0[string range $lldprecord [expr $start + 3] [expr $start + 4]]]]
						if { $length != 4 } {
							set res 0
						}
						if [info exists arrArgs(SystemCapabilities)] {
							array set systemcapabilities $arrArgs(SystemCapabilities)
							#system capabilities
							if [info exists systemcapabilities(SystemCapabilities)] {
								if { [format %d 0x0[string range $lldprecord [expr $start + 6] [expr $start + 7]][string range $lldprecord [expr $start + 9] [expr $start + 10]]] != $systemcapabilities(SystemCapabilities) } {
									set res 0
								}
							}
							#enable capabilities
							if [info exists systemcapabilities(EnableCapabilities)] {
								if { [format %d 0x0[string range $lldprecord [expr $start + 12] [expr $start + 13]][string range $lldprecord [expr $start + 15] [expr $start + 16]]] != $systemcapabilities(EnableCapabilities) } {
									set res 0
								}
							}
						}
					}
					8 {
						#management address tlv
						set length [expr ([format %d 0x0[string range $lldprecord $start [expr $start + 1]]] << 8) % 512 + [format %d 0x0[string range $lldprecord [expr $start + 3] [expr $start + 4]]]]
						if [info exists arrArgs(ManagementAddress)] {
							array set managementaddress $arrArgs(ManagementAddress)
							set managementaddresslength [format %d 0x0[string range $lldprecord [expr $start + 6] [expr $start + 7]]]
							#manegement address subtype
							if [info exists managementaddress(ManagementAddressSubType)] {
								if { [format %d 0x0[string range $lldprecord [expr $start + 9] [expr $start + 10]]] != $managementaddress(ManagementAddressSubType) } {
									set res 0
								}
							}
							#management address
							if [info exists managementaddress(ManagementAddress)] {
								if { [format %d 0x0[string range $lldprecord [expr $start + 12] [expr $start + 12 + $managementaddresslength * 3 - 2]]] != [string toupper $managementaddress(ManagementAddress)] } {
									set res 0
								}
							}
							#interface numbering subtype
							if [info exists managementaddress(InterfaceNumberingSubType)] {
								if { [format %d 0x0[string range $lldprecord [expr $start + 12 + $managementaddresslength * 3] [expr $start + 12 + $managementaddresslength * 3 + 1]]] != $managementaddress(InterfaceNumberingSubType) } {
									set res 0
								}
							}
							#interface numbering
							if [info exists managementaddress(InterfaceNumbering)] {
								if { [format %d 0x0[string range $lldprecord [expr $start + 12 + $managementaddresslength * 3 + 3] [expr $start + 12 + $managementaddresslength * 3 + 13]]] != [string toupper $managementaddress(InterfaceNumberingSubType)] } {
									set res 0
								}
							}
							set oidlength [format %d 0x0[string range $lldprecord [expr $start + 12 + $managementaddresslength * 3 + 15] [expr $start + 12 + $managementaddresslength * 3 + 16]]]
							#oid
							if [info exists managementaddress(OID)] {
								if { [format %d 0x0[string range $lldprecord [expr $start + 12 + $managementaddresslength * 3 + 18] [expr $start + 12 + $managementaddresslength * 3 + 18 + $oidlength * 3 - 2]]] != [string toupper $managementaddress(OID)] } {
									set res 0
								}
							}
						}
					}
					0 {
						if { [expr [info exists arrArgs(PortDescription)] + [info exists arrArgs(SystemName)] + \
						     [info exists arrArgs(SystemDescription)] + [info exists arrArgs(SystemCapabilities)] + \
						     [info exists arrArgs(ManagementAddress)]] > 0 } {
							return 0
						} else {
							#end tlv
							if { [format %d 0x0[string range $lldprecord $start [expr $start + 1]][string range $lldprecord [expr $start + 3] [expr $start + 4]]] != 0 } {
								set res 0
							}
							return $res
						}
					}
					default {return 0}
				}
				#second
				set start [expr $start + 6 + $length * 3]
				set type [expr [format %d 0x0[string range $lldprecord $start [expr $start + 1]]] >> 1]
				switch -exact $type {
					4 {
						#port description tlv
						set length [expr ([format %d 0x0[string range $lldprecord $start [expr $start + 1]]] << 8) % 512 + [format %d 0x0[string range $lldprecord [expr $start + 3] [expr $start + 4]]]]
						if [info exists arrArgs(PortDescription)] {
						puts [string range $lldprecord [expr $start + 6] [expr $start + 6 + $length * 3 - 2]]
						puts [string toupper $arrArgs(PortDescription)]
							if { [string range $lldprecord [expr $start + 6] [expr $start + 6 + $length * 3 - 2]] != [string toupper [FormattoASCII $arrArgs(PortDescription)]] } {
								set res 0
							}
						}
					}
					5 {
						#system name tlv
						set length [expr ([format %d 0x0[string range $lldprecord $start [expr $start + 1]]] << 8) % 512 + [format %d 0x0[string range $lldprecord [expr $start + 3] [expr $start + 4]]]]
						if [info exists arrArgs(SystemName)] {
							if { [string range $lldprecord [expr $start + 6] [expr $start + 6 + $length * 3 - 2]] != [string toupper [FormattoASCII $arrArgs(SystemName)]] } {
								set res 0
							}
						}
					}
					6 {
						#system description tlv
						set length [expr ([format %d 0x0[string range $lldprecord $start [expr $start + 1]]] << 8) % 512 + [format %d 0x0[string range $lldprecord [expr $start + 3] [expr $start + 4]]]]
						set SysDescripLength $length
						if [info exists arrArgs(SystemDescription)] {
							if { [string range $lldprecord [expr $start + 6] [expr $start + 6 + $length * 3 - 2]] != [string toupper [FormattoASCII $arrArgs(SystemDescription)]] } {
								set res 0
							}
						}
					}
					7 {
						#system capabilities tlv
						set length [expr ([format %d 0x0[string range $lldprecord $start [expr $start + 1]]] << 8) % 512 + [format %d 0x0[string range $lldprecord [expr $start + 3] [expr $start + 4]]]]
						if { $length != 4 } {
							set res 0
						}
						if [info exists arrArgs(SystemCapabilities)] {
							array set systemcapabilities $arrArgs(SystemCapabilities)
							#system capabilities
							if [info exists systemcapabilities(SystemCapabilities)] {
								if { [format %d 0x0[string range $lldprecord [expr $start + 6] [expr $start + 7]][string range $lldprecord [expr $start + 9] [expr $start + 10]]] != $systemcapabilities(SystemCapabilities) } {
									set res 0
								}
							}
							#enable capabilities
							if [info exists systemcapabilities(EnableCapabilities)] {
								if { [format %d 0x0[string range $lldprecord [expr $start + 12] [expr $start + 13]][string range $lldprecord [expr $start + 15] [expr $start + 16]]] != $systemcapabilities(EnableCapabilities) } {
									set res 0
								}
							}
						}
					}
					8 {
						#management address tlv
						set length [expr ([format %d 0x0[string range $lldprecord $start [expr $start + 1]]] << 8) % 512 + [format %d 0x0[string range $lldprecord [expr $start + 3] [expr $start + 4]]]]
						if [info exists arrArgs(ManagementAddress)] {
							array set managementaddress $arrArgs(ManagementAddress)
							set managementaddresslength [format %d 0x0[string range $lldprecord [expr $start + 6] [expr $start + 7]]]
							#manegement address subtype
							if [info exists managementaddress(ManagementAddressSubType)] {
								if { [format %d 0x0[string range $lldprecord [expr $start + 9] [expr $start + 10]]] != $managementaddress(ManagementAddressSubType) } {
									set res 0
								}
							}
							#management address
							if [info exists managementaddress(ManagementAddress)] {
								if { [format %d 0x0[string range $lldprecord [expr $start + 12] [expr $start + 12 + $managementaddresslength * 3 - 2]]] != [string toupper $managementaddress(ManagementAddress)] } {
									set res 0
								}
							}
							#interface numbering subtype
							if [info exists managementaddress(InterfaceNumberingSubType)] {
								if { [format %d 0x0[string range $lldprecord [expr $start + 12 + $managementaddresslength * 3] [expr $start + 12 + $managementaddresslength * 3 + 1]]] != $managementaddress(InterfaceNumberingSubType) } {
									set res 0
								}
							}
							#interface numbering
							if [info exists managementaddress(InterfaceNumbering)] {
								if { [format %d 0x0[string range $lldprecord [expr $start + 12 + $managementaddresslength * 3 + 3] [expr $start + 12 + $managementaddresslength * 3 + 13]]] != [string toupper $managementaddress(InterfaceNumberingSubType)] } {
									set res 0
								}
							}
							set oidlength [format %d 0x0[string range $lldprecord [expr $start + 12 + $managementaddresslength * 3 + 15] [expr $start + 12 + $managementaddresslength * 3 + 16]]]
							#oid
							if [info exists managementaddress(OID)] {
								if { [format %d 0x0[string range $lldprecord [expr $start + 12 + $managementaddresslength * 3 + 18] [expr $start + 12 + $managementaddresslength * 3 + 18 + $oidlength * 3 - 2]]] != [string toupper $managementaddress(OID)] } {
									set res 0
								}
							}
						}
					}
					0 {
						if { [expr [info exists arrArgs(PortDescription)] + [info exists arrArgs(SystemName)] + \
						     [info exists arrArgs(SystemDescription)] + [info exists arrArgs(SystemCapabilities)] + \
						     [info exists arrArgs(ManagementAddress)]] > 1 } {
							return 0
						} else {
							#end tlv
							if { [format %d 0x0[string range $lldprecord $start [expr $start + 1]][string range $lldprecord [expr $start + 3] [expr $start + 4]]] != 0 } {
								set res 0
							}
							return $res
						}
					}
					default {return 0}
				}
				#third
				set start [expr $start + 6 + $length * 3]
				set type [expr [format %d 0x0[string range $lldprecord $start [expr $start + 1]]] >> 1]
				switch -exact $type {
					4 {
						#port description tlv
						set length [expr ([format %d 0x0[string range $lldprecord $start [expr $start + 1]]] << 8) % 512 + [format %d 0x0[string range $lldprecord [expr $start + 3] [expr $start + 4]]]]
						if [info exists arrArgs(PortDescription)] {
						puts [string range $lldprecord [expr $start + 6] [expr $start + 6 + $length * 3 - 2]]
						puts [string toupper $arrArgs(PortDescription)]
							if { [string range $lldprecord [expr $start + 6] [expr $start + 6 + $length * 3 - 2]] != [string toupper [FormattoASCII $arrArgs(PortDescription)]] } {
								set res 0
							}
						}
					}
					5 {
						#system name tlv
						set length [expr ([format %d 0x0[string range $lldprecord $start [expr $start + 1]]] << 8) % 512 + [format %d 0x0[string range $lldprecord [expr $start + 3] [expr $start + 4]]]]
						if [info exists arrArgs(SystemName)] {
							if { [string range $lldprecord [expr $start + 6] [expr $start + 6 + $length * 3 - 2]] != [string toupper [FormattoASCII $arrArgs(SystemName)]] } {
								set res 0
							}
						}
					}
					6 {
						#system description tlv
						set length [expr ([format %d 0x0[string range $lldprecord $start [expr $start + 1]]] << 8) % 512 + [format %d 0x0[string range $lldprecord [expr $start + 3] [expr $start + 4]]]]
						set SysDescripLength $length
						if [info exists arrArgs(SystemDescription)] {
							if { [string range $lldprecord [expr $start + 6] [expr $start + 6 + $length * 3 - 2]] != [string toupper [FormattoASCII $arrArgs(SystemDescription)]] } {
								set res 0
							}
						}
					}
					7 {
						#system capabilities tlv
						set length [expr ([format %d 0x0[string range $lldprecord $start [expr $start + 1]]] << 8) % 512 + [format %d 0x0[string range $lldprecord [expr $start + 3] [expr $start + 4]]]]
						if { $length != 4 } {
							set res 0
						}
						if [info exists arrArgs(SystemCapabilities)] {
							array set systemcapabilities $arrArgs(SystemCapabilities)
							#system capabilities
							if [info exists systemcapabilities(SystemCapabilities)] {
								if { [format %d 0x0[string range $lldprecord [expr $start + 6] [expr $start + 7]][string range $lldprecord [expr $start + 9] [expr $start + 10]]] != $systemcapabilities(SystemCapabilities) } {
									set res 0
								}
							}
							#enable capabilities
							if [info exists systemcapabilities(EnableCapabilities)] {
								if { [format %d 0x0[string range $lldprecord [expr $start + 12] [expr $start + 13]][string range $lldprecord [expr $start + 15] [expr $start + 16]]] != $systemcapabilities(EnableCapabilities) } {
									set res 0
								}
							}
						}
					}
					8 {
						#management address tlv
						set length [expr ([format %d 0x0[string range $lldprecord $start [expr $start + 1]]] << 8) % 512 + [format %d 0x0[string range $lldprecord [expr $start + 3] [expr $start + 4]]]]
						if [info exists arrArgs(ManagementAddress)] {
							array set managementaddress $arrArgs(ManagementAddress)
							set managementaddresslength [format %d 0x0[string range $lldprecord [expr $start + 6] [expr $start + 7]]]
							#manegement address subtype
							if [info exists managementaddress(ManagementAddressSubType)] {
								if { [format %d 0x0[string range $lldprecord [expr $start + 9] [expr $start + 10]]] != $managementaddress(ManagementAddressSubType) } {
									set res 0
								}
							}
							#management address
							if [info exists managementaddress(ManagementAddress)] {
								if { [format %d 0x0[string range $lldprecord [expr $start + 12] [expr $start + 12 + $managementaddresslength * 3 - 2]]] != [string toupper $managementaddress(ManagementAddress)] } {
									set res 0
								}
							}
							#interface numbering subtype
							if [info exists managementaddress(InterfaceNumberingSubType)] {
								if { [format %d 0x0[string range $lldprecord [expr $start + 12 + $managementaddresslength * 3] [expr $start + 12 + $managementaddresslength * 3 + 1]]] != $managementaddress(InterfaceNumberingSubType) } {
									set res 0
								}
							}
							#interface numbering
							if [info exists managementaddress(InterfaceNumbering)] {
								if { [format %d 0x0[string range $lldprecord [expr $start + 12 + $managementaddresslength * 3 + 3] [expr $start + 12 + $managementaddresslength * 3 + 13]]] != [string toupper $managementaddress(InterfaceNumberingSubType)] } {
									set res 0
								}
							}
							set oidlength [format %d 0x0[string range $lldprecord [expr $start + 12 + $managementaddresslength * 3 + 15] [expr $start + 12 + $managementaddresslength * 3 + 16]]]
							#oid
							if [info exists managementaddress(OID)] {
								if { [format %d 0x0[string range $lldprecord [expr $start + 12 + $managementaddresslength * 3 + 18] [expr $start + 12 + $managementaddresslength * 3 + 18 + $oidlength * 3 - 2]]] != [string toupper $managementaddress(OID)] } {
									set res 0
								}
							}
						}
					}
					0 {
						if { [expr [info exists arrArgs(PortDescription)] + [info exists arrArgs(SystemName)] + \
						     [info exists arrArgs(SystemDescription)] + [info exists arrArgs(SystemCapabilities)] + \
						     [info exists arrArgs(ManagementAddress)]] > 2 } {
							return 0
						} else {
							#end tlv
							if { [format %d 0x0[string range $lldprecord $start [expr $start + 1]][string range $lldprecord [expr $start + 3] [expr $start + 4]]] != 0 } {
								set res 0
							}
							return $res
						}
					}
					default {return 0}
				}
				#fourth
				set start [expr $start + 6 + $length * 3]
				set type [expr [format %d 0x0[string range $lldprecord $start [expr $start + 1]]] >> 1]
				switch -exact $type {
					4 {
						#port description tlv
						set length [expr ([format %d 0x0[string range $lldprecord $start [expr $start + 1]]] << 8) % 512 + [format %d 0x0[string range $lldprecord [expr $start + 3] [expr $start + 4]]]]
						if [info exists arrArgs(PortDescription)] {
						puts [string range $lldprecord [expr $start + 6] [expr $start + 6 + $length * 3 - 2]]
						puts [string toupper $arrArgs(PortDescription)]
							if { [string range $lldprecord [expr $start + 6] [expr $start + 6 + $length * 3 - 2]] != [string toupper [FormattoASCII $arrArgs(PortDescription)]] } {
								set res 0
							}
						}
					}
					5 {
						#system name tlv
						set length [expr ([format %d 0x0[string range $lldprecord $start [expr $start + 1]]] << 8) % 512 + [format %d 0x0[string range $lldprecord [expr $start + 3] [expr $start + 4]]]]
						if [info exists arrArgs(SystemName)] {
							if { [string range $lldprecord [expr $start + 6] [expr $start + 6 + $length * 3 - 2]] != [string toupper [FormattoASCII $arrArgs(SystemName)]] } {
								set res 0
							}
						}
					}
					6 {
						#system description tlv
						set length [expr ([format %d 0x0[string range $lldprecord $start [expr $start + 1]]] << 8) % 512 + [format %d 0x0[string range $lldprecord [expr $start + 3] [expr $start + 4]]]]
						set SysDescripLength $length
						if [info exists arrArgs(SystemDescription)] {
							if { [string range $lldprecord [expr $start + 6] [expr $start + 6 + $length * 3 - 2]] != [string toupper [FormattoASCII $arrArgs(SystemDescription)]] } {
								set res 0
							}
						}
					}
					7 {
						#system capabilities tlv
						set length [expr ([format %d 0x0[string range $lldprecord $start [expr $start + 1]]] << 8) % 512 + [format %d 0x0[string range $lldprecord [expr $start + 3] [expr $start + 4]]]]
						if { $length != 4 } {
							set res 0
						}
						if [info exists arrArgs(SystemCapabilities)] {
							array set systemcapabilities $arrArgs(SystemCapabilities)
							#system capabilities
							if [info exists systemcapabilities(SystemCapabilities)] {
								if { [format %d 0x0[string range $lldprecord [expr $start + 6] [expr $start + 7]][string range $lldprecord [expr $start + 9] [expr $start + 10]]] != $systemcapabilities(SystemCapabilities) } {
									set res 0
								}
							}
							#enable capabilities
							if [info exists systemcapabilities(EnableCapabilities)] {
								if { [format %d 0x0[string range $lldprecord [expr $start + 12] [expr $start + 13]][string range $lldprecord [expr $start + 15] [expr $start + 16]]] != $systemcapabilities(EnableCapabilities) } {
									set res 0
								}
							}
						}
					}
					8 {
						#management address tlv
						set length [expr ([format %d 0x0[string range $lldprecord $start [expr $start + 1]]] << 8) % 512 + [format %d 0x0[string range $lldprecord [expr $start + 3] [expr $start + 4]]]]
						if [info exists arrArgs(ManagementAddress)] {
							array set managementaddress $arrArgs(ManagementAddress)
							set managementaddresslength [format %d 0x0[string range $lldprecord [expr $start + 6] [expr $start + 7]]]
							#manegement address subtype
							if [info exists managementaddress(ManagementAddressSubType)] {
								if { [format %d 0x0[string range $lldprecord [expr $start + 9] [expr $start + 10]]] != $managementaddress(ManagementAddressSubType) } {
									set res 0
								}
							}
							#management address
							if [info exists managementaddress(ManagementAddress)] {
								if { [format %d 0x0[string range $lldprecord [expr $start + 12] [expr $start + 12 + $managementaddresslength * 3 - 2]]] != [string toupper $managementaddress(ManagementAddress)] } {
									set res 0
								}
							}
							#interface numbering subtype
							if [info exists managementaddress(InterfaceNumberingSubType)] {
								if { [format %d 0x0[string range $lldprecord [expr $start + 12 + $managementaddresslength * 3] [expr $start + 12 + $managementaddresslength * 3 + 1]]] != $managementaddress(InterfaceNumberingSubType) } {
									set res 0
								}
							}
							#interface numbering
							if [info exists managementaddress(InterfaceNumbering)] {
								if { [format %d 0x0[string range $lldprecord [expr $start + 12 + $managementaddresslength * 3 + 3] [expr $start + 12 + $managementaddresslength * 3 + 13]]] != [string toupper $managementaddress(InterfaceNumberingSubType)] } {
									set res 0
								}
							}
							set oidlength [format %d 0x0[string range $lldprecord [expr $start + 12 + $managementaddresslength * 3 + 15] [expr $start + 12 + $managementaddresslength * 3 + 16]]]
							#oid
							if [info exists managementaddress(OID)] {
								if { [format %d 0x0[string range $lldprecord [expr $start + 12 + $managementaddresslength * 3 + 18] [expr $start + 12 + $managementaddresslength * 3 + 18 + $oidlength * 3 - 2]]] != [string toupper $managementaddress(OID)] } {
									set res 0
								}
							}
						}
					}
					0 {
						if { [expr [info exists arrArgs(PortDescription)] + [info exists arrArgs(SystemName)] + \
						     [info exists arrArgs(SystemDescription)] + [info exists arrArgs(SystemCapabilities)] + \
						     [info exists arrArgs(ManagementAddress)]] > 3 } {
							return 0
						} else {
							#end tlv
							if { [format %d 0x0[string range $lldprecord $start [expr $start + 1]][string range $lldprecord [expr $start + 3] [expr $start + 4]]] != 0 } {
								set res 0
							}
							return $res
						}
					}
					default {return 0}
				}
				#fifth
				set start [expr $start + 6 + $length * 3]
				set type [expr [format %d 0x0[string range $lldprecord $start [expr $start + 1]]] >> 1]
				switch -exact $type {
					4 {
						#port description tlv
						set length [expr ([format %d 0x0[string range $lldprecord $start [expr $start + 1]]] << 8) % 512 + [format %d 0x0[string range $lldprecord [expr $start + 3] [expr $start + 4]]]]
						if [info exists arrArgs(PortDescription)] {
						puts [string range $lldprecord [expr $start + 6] [expr $start + 6 + $length * 3 - 2]]
						puts [string toupper $arrArgs(PortDescription)]
							if { [string range $lldprecord [expr $start + 6] [expr $start + 6 + $length * 3 - 2]] != [string toupper [FormattoASCII $arrArgs(PortDescription)]] } {
								set res 0
							}
						}
					}
					5 {
						#system name tlv
						set length [expr ([format %d 0x0[string range $lldprecord $start [expr $start + 1]]] << 8) % 512 + [format %d 0x0[string range $lldprecord [expr $start + 3] [expr $start + 4]]]]
						if [info exists arrArgs(SystemName)] {
							if { [string range $lldprecord [expr $start + 6] [expr $start + 6 + $length * 3 - 2]] != [string toupper [FormattoASCII $arrArgs(SystemName)]] } {
								set res 0
							}
						}
					}
					6 {
						#system description tlv
						set length [expr ([format %d 0x0[string range $lldprecord $start [expr $start + 1]]] << 8) % 512 + [format %d 0x0[string range $lldprecord [expr $start + 3] [expr $start + 4]]]]
						set SysDescripLength $length
						if [info exists arrArgs(SystemDescription)] {
							if { [string range $lldprecord [expr $start + 6] [expr $start + 6 + $length * 3 - 2]] != [string toupper [FormattoASCII $arrArgs(SystemDescription)]] } {
								set res 0
							}
						}
					}
					7 {
						#system capabilities tlv
						set length [expr ([format %d 0x0[string range $lldprecord $start [expr $start + 1]]] << 8) % 512 + [format %d 0x0[string range $lldprecord [expr $start + 3] [expr $start + 4]]]]
						if { $length != 4 } {
							set res 0
						}
						if [info exists arrArgs(SystemCapabilities)] {
							array set systemcapabilities $arrArgs(SystemCapabilities)
							#system capabilities
							if [info exists systemcapabilities(SystemCapabilities)] {
								if { [format %d 0x0[string range $lldprecord [expr $start + 6] [expr $start + 7]][string range $lldprecord [expr $start + 9] [expr $start + 10]]] != $systemcapabilities(SystemCapabilities) } {
									set res 0
								}
							}
							#enable capabilities
							if [info exists systemcapabilities(EnableCapabilities)] {
								if { [format %d 0x0[string range $lldprecord [expr $start + 12] [expr $start + 13]][string range $lldprecord [expr $start + 15] [expr $start + 16]]] != $systemcapabilities(EnableCapabilities) } {
									set res 0
								}
							}
						}
					}
					8 {
						#management address tlv
						set length [expr ([format %d 0x0[string range $lldprecord $start [expr $start + 1]]] << 8) % 512 + [format %d 0x0[string range $lldprecord [expr $start + 3] [expr $start + 4]]]]
						if [info exists arrArgs(ManagementAddress)] {
							array set managementaddress $arrArgs(ManagementAddress)
							set managementaddresslength [format %d 0x0[string range $lldprecord [expr $start + 6] [expr $start + 7]]]
							#manegement address subtype
							if [info exists managementaddress(ManagementAddressSubType)] {
								if { [format %d 0x0[string range $lldprecord [expr $start + 9] [expr $start + 10]]] != $managementaddress(ManagementAddressSubType) } {
									set res 0
								}
							}
							#management address
							if [info exists managementaddress(ManagementAddress)] {
								if { [format %d 0x0[string range $lldprecord [expr $start + 12] [expr $start + 12 + $managementaddresslength * 3 - 2]]] != [string toupper $managementaddress(ManagementAddress)] } {
									set res 0
								}
							}
							#interface numbering subtype
							if [info exists managementaddress(InterfaceNumberingSubType)] {
								if { [format %d 0x0[string range $lldprecord [expr $start + 12 + $managementaddresslength * 3] [expr $start + 12 + $managementaddresslength * 3 + 1]]] != $managementaddress(InterfaceNumberingSubType) } {
									set res 0
								}
							}
							#interface numbering
							if [info exists managementaddress(InterfaceNumbering)] {
								if { [format %d 0x0[string range $lldprecord [expr $start + 12 + $managementaddresslength * 3 + 3] [expr $start + 12 + $managementaddresslength * 3 + 13]]] != [string toupper $managementaddress(InterfaceNumberingSubType)] } {
									set res 0
								}
							}
							set oidlength [format %d 0x0[string range $lldprecord [expr $start + 12 + $managementaddresslength * 3 + 15] [expr $start + 12 + $managementaddresslength * 3 + 16]]]
							#oid
							if [info exists managementaddress(OID)] {
								if { [format %d 0x0[string range $lldprecord [expr $start + 12 + $managementaddresslength * 3 + 18] [expr $start + 12 + $managementaddresslength * 3 + 18 + $oidlength * 3 - 2]]] != [string toupper $managementaddress(OID)] } {
									set res 0
								}
							}
						}
					}
					0 {
						if { [expr [info exists arrArgs(PortDescription)] + [info exists arrArgs(SystemName)] + \
						     [info exists arrArgs(SystemDescription)] + [info exists arrArgs(SystemCapabilities)] + \
						     [info exists arrArgs(ManagementAddress)]] > 4 } {
							return 0
						} else {
							#end tlv
							if { [format %d 0x0[string range $lldprecord $start [expr $start + 1]][string range $lldprecord [expr $start + 3] [expr $start + 4]]] != 0 } {
								set res 0
							}
							return $res
						}
					}
					default {return 0}
				}
				#sixth
				set start [expr $start + 6 + $length * 3]
				set type [expr [format %d 0x0[string range $lldprecord $start [expr $start + 1]]] >> 1]
				if { $type != 0 } {
					set res 0
				}
				if { [format %d 0x0[string range $lldprecord $start [expr $start + 1]][string range $lldprecord [expr $start + 3] [expr $start + 4]]] != 0 } {
					set res 0
				}
				return $res
 			}
			if { $lldptype == "shutdown" } {
				#chassis id tlv
				set start 6
				if { [expr [format %d 0x0[string range $lldprecord $start [expr $start + 1]]] >> 1] != 1 } {
					set res 0
				}
				set length [expr ([format %d 0x0[string range $lldprecord $start [expr $start + 1]]] << 8) % 512 + [format %d 0x0[string range $lldprecord [expr $start + 3] [expr $start + 4]]]]
				if [info exists arrArgs(ChassisID)] {
					array set chassisid $arrArgs(ChassisID)
					#chassis id subtype
					if [info exists chassisid(SubType)] {
						if { [format %d 0x0[string range $lldprecord [expr $start + 6] [expr $start + 7]]] != $chassisid(SubType) } {
							set res 0
						}
					}
					#chassis id
					if [info exists chassisid(ChassisID)] {
						if { [format %d 0x0[string range $lldprecord [expr $start + 6] [expr $start + 7]]] == 4 } {
							regsub -all {\-} $chassisid(ChassisID) " " cpumac
						} else {
							set cpumac $chassisid(ChassisID)
						}
						if { [string range $lldprecord [expr $start + 9] [expr $start + 9 + ($length - 1) * 3 - 2]] != [string toupper $cpumac] } {
							set res 0
						}
					}
				}
				#puts "start = $start, length = $length"
				#puts "chass id tlv = [string range $lldprecord $start [expr $start + 9 + ($length - 1) * 3 - 2]]"
				#port id tlv
				set start [expr $start + 9 + ($length - 1) * 3]
				if { [expr [format %d 0x0[string range $lldprecord $start [expr $start + 1]]] >> 1] != 2 } {
					set res 0
				}
				set length [expr ([format %d 0x0[string range $lldprecord $start [expr $start + 1]]] << 8) % 512 + [format %d 0x0[string range $lldprecord [expr $start + 3] [expr $start + 4]]]]
				if [info exists arrArgs(PortID)] {
					array set portid $arrArgs(PortID)
					#port id subtype
					if [info exists portid(SubType)] {
						if { [format %d 0x0[string range $lldprecord [expr $start + 6] [expr $start + 7]]] != $portid(SubType) } {
							set res 0
						}
					}
					#port id
					if [info exists portid(PortID)] {
						#puts [string range $lldprecord [expr $start + 9] [expr $start + 9 + ($length - 1) * 3 - 2]]
						#puts [string toupper $portid(PortID)]

						#modified by zhaohj 2011-3-29
						set p1 [string last "/" $portid(PortID)]
						set portindex [string range $portid(PortID) [expr $p1 + 1] [expr $p1 + 1]]
						set p2 [string first "/" $portid(PortID)]
						set slotnum [string range $portid(PortID) [expr $p2 - 1] [expr $p2 - 1]]
						if {$slotnum == 0} {
							set slotnum 1
						}
						set portidindex [FormattoASCII [expr ($slotnum - 1) * 64 + $portindex]]

						
						if { [string range $lldprecord [expr $start + 9] [expr $start + 9 + ($length - 1) * 3 - 2]] != [string toupper $portidindex] } {
							set res 0
						}
						#modified by zhaohj end
					}
				}
				#ttl tlv
				set start [expr $start + 9 + ($length - 1) * 3]
				if { [expr [format %d 0x0[string range $lldprecord $start [expr $start + 1]]] >> 1] != 3 } {
					set res 0
				}
				set length [expr ([format %d 0x0[string range $lldprecord $start [expr $start + 1]]] << 8) % 512 + [format %d 0x0[string range $lldprecord [expr $start + 3] [expr $start + 4]]]]
				if { $length != 2 } {
					set res 0
				}
				if { [format %d 0x0[string range $lldprecord [expr $start + 6] [expr $start + 7]][string range $lldprecord [expr $start + 9] [expr $start + 10]]] != 0 } {
						set res 0
				}
				#end tlv
				set start [expr $start + 9 + ($length - 1) * 3]
				if { [format %d 0x0[string range $lldprecord $start [expr $start + 1]][string range $lldprecord [expr $start + 3] [expr $start + 4]]] != 0 } {
					set res 0
				}
			}
			return $res
		} else {
			return 1
		}
	} else {
		return 0
	}
}


proc CheckLoopBackRecordInData { record data } {
	set flag [string range $data 36 40]
    if  { $flag == "81 00" } {
        #vlantag
        #set length [string range 66 70]
        #set ethernet [string range $data 72 82]
        #set vlanid [string range $data 84 94]  
        set loopbackrecord [string range $data 48 190]
    } else {
    	#set length [string range 54 58]
        #set ethernet [string range $data 60 70]
        #set vlanid [string range $data 72 82]  
        set loopbackrecord [string range $data 36 178]
    }
    #if {[llength $record] == 3} {
    #	set lengthvalue [FormatHex [format %04x [lindex $record 2]]]
    #}
    #set ethernetvalue [lindex $record 1]
    #set vlanidvalue [FormatHex [format %08x [lindex $record 0]]]
    set recordvalue [FormatLoopbackSegment $record]
    if { $loopbackrecord == [string toupper [string replace $recordvalue 0 4 "DC 09"]]} {
    	return 1
    } else {
    	return 0
    }
}
#CheckCaptureStream $chas $card $port SrcMac $s1cpumac DstMac ff-ff-ff-ff-ff-ff MrppRecord {EthernetType 0x8100 PRI 0 VlanId 100 \
#                    FrameLength 72 DSAPSSAP 0xAAAA Control 0x03 MrppLength 0x0040 MrppVers 0x01 MrppType 1 CtrlVlanId 100 \
#                    SystemMacAddress $cpumac HelloTimer 100 FailTimer 100 State 1 HelloSeq 1}
#CheckCaptureStream $chas $card $port SrcMac $s1cpumac DstMac ff-ff-ff-ff-ff-ff MrppRecord {FrameLength 72 DSAPSSAP 0xAAAA \
#                    Control 0x03 MrppLength 0x0040 MrppVers 0x01 MrppType 1 CtrlVlanId 100 \
#                    SystemMacAddress $cpumac HelloTimer 100 FailTimer 100 State 1 HelloSeq 1}

proc CheckMrppRecordInData { record data } {
	array set arrArgs $record
	set dstmac [string range $data 0 16]
	set flag [string range $data 36 40]
	set res 1

		if { $flag == "81 00" } {
##enable the EthernetType check for Mrpp by zhaogang/2010/09/03						
		if [info exists arrArgs(EthernetType)] {
			regsub -all {\s} [string range $data 36 40] "" ethernettype
			if { $arrArgs(EthernetType) != "0x0$ethernettype" } {
				set res 0
			}
		}
#		if [info exists arrArgs(PRI)] {
#			set pri [format %d 0x0[string range $data 42 43]]
#			if { $arrArgs(PRI) != [expr $pri >> 5] } {
#				set res 0
#			}
#		}
#		if [info exists arrArgs(VlanId)] {
#			regsub -all {\s} [string range $data 42 46] "" pri_and_vlanid
#			if { $arrArgs(VlanId) != [expr $pri_and_vlanid & 8191] } {
#				set res 0
#			}
#		}
			if [info exists arrArgs(FrameLength)] {
				regsub -all {\s} [string range $data 48 52] "" framelength
				if { $arrArgs(FrameLength) != [format %d 0x0$framelength] } {
					set res 0
				}
			}
			if [info exists arrArgs(DSAPSSAP)] {
				regsub -all {\s} [string range $data 54 58] "" dsapssap
				if { $arrArgs(DSAPSSAP) != "0x$dsapssap" } {
					set res 0
				}
			}
			if [info exists arrArgs(Control)] {
				set control [string range $data 60 61]
				if { $arrArgs(Control) != "0x$control" } {
					set res 0
				}
			}
			if [info exists arrArgs(MrppLength)] {
				regsub -all {\s} [string range $data 84 88] "" mrpplength
				if { $arrArgs(MrppLength) != "0x$mrpplength" } {
					set res 0
				}
			}
			if [info exists arrArgs(MrppVers)] {
				set mrppvers [string range $data 90 91]
				if { $arrArgs(MrppVers) != "0x$mrppvers" } {
					set res 0
				}
			}
			if [info exists arrArgs(MrppType)] {
				set mrpptype [string range $data 93 94]
				if { $arrArgs(MrppType) != "0x$mrpptype" } {
					set res 0
				}
			}
			if [info exists arrArgs(CtrlVlanId)] {
				regsub -all {\s} [string range $data 96 100] "" ctrlvlanid
				if { $arrArgs(CtrlVlanId) != [format %d 0x0$ctrlvlanid] } {
					set res 0
				}
			}
			if [info exists arrArgs(SystemMacAddress)] {
				regsub -all {\s} [string range $data 114 130] - systemmacaddress
				if { $arrArgs(SystemMacAddress) != $systemmacaddress } {
					set res 0
				}
			}
			if [info exists arrArgs(HelloTimer)] {
				regsub -all {\s} [string range $data 132 136] "" hellotimer
				if { $arrArgs(HelloTimer) != [format %d 0x0$hellotimer] } {
					set res 0
				}
			}
			if [info exists arrArgs(FailTimer)] {
				regsub -all {\s} [string range $data 138 142] "" failtimer
				if { $arrArgs(FailTimer) != [format %d 0x0$failtimer] } {
					set res 0
				}
			}
			if [info exists arrArgs(State)] {
				set state [string range $data 144 145]
				if { $arrArgs(State) != [format %d 0x0$state] } {
					set res 0
				}
			}
			if [info exists arrArgs(HelloSeq)] {
				regsub -all {\s} [string range $data 150 154] "" helloseq
				if { $arrArgs(HelloSeq) != [format %d 0x0$helloseq] } {
					set res 0
				}
			}
			return $res
		} else {
			if [info exists arrArgs(FrameLength)] {
				regsub -all {\s} [string range $data 36 40] "" framelength
				if { $arrArgs(FrameLength) != [format %d 0x0$framelength] } {
					set res 0
				}
			}
			if [info exists arrArgs(DSAPSSAP)] {
				regsub -all {\s} [string range $data 42 46] "" dsapssap
				if { $arrArgs(DSAPSSAP) != "0x$dsapssap" } {
					set res 0
				}
			}
			if [info exists arrArgs(Control)] {
				set control [string range $data 48 49]
				if { $arrArgs(Control) != "0x$control" } {
					set res 0
				}
			}
			if [info exists arrArgs(MrppLength)] {
				regsub -all {\s} [string range $data 72 76] "" mrpplength
				if { $arrArgs(MrppLength) != "0x$mrpplength" } {
					set res 0
				}
			}
			if [info exists arrArgs(MrppVers)] {
				set mrppvers [string range $data 78 79]
				if { $arrArgs(MrppVers) != "0x$mrppvers" } {
					set res 0
				}
			}
			if [info exists arrArgs(MrppType)] {
				set mrpptype [string range $data 81 82]
				if { $arrArgs(MrppType) != "0x$mrpptype" } {
					set res 0
				}
			}
			if [info exists arrArgs(CtrlVlanId)] {
				regsub -all {\s} [string range $data 84 88] "" ctrlvlanid
				if { $arrArgs(CtrlVlanId) != [format %d 0x0$ctrlvlanid] } {
					set res 0
				}
			}
			if [info exists arrArgs(SystemMacAddress)] {
				regsub -all {\s} [string range $data 102 118] - systemmacaddress
				if { $arrArgs(SystemMacAddress) != $systemmacaddress } {
					set res 0
				}
			}
			if [info exists arrArgs(HelloTimer)] {
				regsub -all {\s} [string range $data 120 124] "" hellotimer
				if { $arrArgs(HelloTimer) != [format %d 0x0$hellotimer] } {
					set res 0
				}
			}
			if [info exists arrArgs(FailTimer)] {
				regsub -all {\s} [string range $data 126 130] "" failtimer
				if { $arrArgs(FailTimer) != [format %d 0x0$failtimer] } {
					set res 0
				}
			}
			if [info exists arrArgs(State)] {
				set state [string range $data 130 133]
				if { $arrArgs(State) != [format %d 0x0$state] } {
					set res 0
				}
			}
			if [info exists arrArgs(HelloSeq)] {
				regsub -all {\s} [string range $data 138 142] "" helloseq
				if { $arrArgs(HelloSeq) != [format %d 0x0$helloseq] } {
					set res 0
				}
			}
			return $res		
		}
	
}

#CheckCaptureStream $chas $card1 $port1 SrcMac 00-00-00-00-00-02 DstMac 00-00-00-00-00-01 Cluster {Type DP CommanderMac 00-00-00-00-00-02}
#
#CheckCaptureStream $chas $card1 $port1 SrcMac 00-00-00-00-00-02 DstMac 00-00-00-00-00-01 Cluster {Type DR CommanderMac 00-00-00-00-00-01 LocalMac 00-00-00-00-00-02 Role 1}
#
#CheckCaptureStream $chas $card1 $port1 SrcMac 00-00-00-00-00-02 DstMac 00-00-00-00-00-01 Cluster {Type CP SubOp 1 MemberId 1 ClusterKey test SrcIp 10.1.1.1 DstIp 10.1.1.2 Interval 30 Losscount 3}
#
#CheckCaptureStream $chas $card1 $port1 SrcMac 00-00-00-00-00-02 DstMac 00-00-00-00-00-01 Cluster {Type CP SubOp 3 MemberId 1}
#
###CC是TCP报文
#CheckCaptureStream $chas $card1 $port1 SrcMac 00-00-00-00-00-02 DstMac 00-00-00-00-00-01 Cluster {Type CC OpCode 1 CCType 1}

proc CheckClusterInData { record data } {
	array set arrArgs $record
	#set dstmac [string range $data 0 16]

	#判断是否带vlantag，截取mac及vlantag字段后的其余字段
	set flag [string range $data 36 40]
	if { $flag == "81 00" } {
		set data [string range $data 48 end]
	} else {
		set data [string range $data 36 end]
	}
	
	set res 1
	if { [string range $data 6 31] == "AA AA 03 00 03 0F 00 01 02" } {
		if ![info exists arrArgs(Type)] {
			set $arrArgs(Type) DP
		}
		if { $arrArgs(Type) == "DP" } {
			set type [string range $data 33 34]
			if { $type != "01" } {
				set res 0
			}
			if { [string range $data 36 40] != "00 0A" } {
				set res 0
			}
			if [info exists arrArgs(CommanderMac)] {
				regsub -all {\s} [string range $data 42 58] "-" commandermac
				if { [string toupper $arrArgs(CommanderMac)] != $commandermac } {
					set res 0
				}
			}
			regsub -all {\s} [string range $data 60 end-12] "" zerosegment
			if { $zerosegment != 0 } {
				set res 0
			}
			return $res
		}
		if { $arrArgs(Type) == "DR" } {
			set type [string range $data 33 34]
			if { $type != "02" } {
				set res 0
			}
			if [info exists arrArgs(Length)] {
				regsub -all {\s} [string range $data 0 4] "" length
				if { $arrArgs(Length) != [format %d 0x0$length] } {
					set res 0
				}
			}
			if { [string range $data 36 40] != "00 7E" } {
				set res 0
			}
			if [info exists arrArgs(CommanderMac)] {
				regsub -all {\s} [string range $data 42 58] "-" commandermac
				if { [string toupper $arrArgs(CommanderMac)] != $commandermac } {
					set res 0
				}
			}
			if [info exists arrArgs(LocalMac)] {
				regsub -all {\s} [string range $data 60 76] "-" localmac
				if { [string toupper $arrArgs(LocalMac)] != $localmac } {
					set res 0
				}
			}
			if [info exists arrArgs(LocalPort)] {
				set localport [FormattoASCII [string replace [string totitle $arrArgs(LocalPort) 0 end] 3 7 ""] 12]
				if { [string range $data 78 112] != $localport } {
					set res 0
				}
			}
			if [info exists arrArgs(RelayMac)] {
				regsub -all {\s} [string range $data 114 130] "-" relaymac
				if { [string toupper $arrArgs(RelayMac)] != $relaymac } {
					set res 0
				}
			}
			if [info exists arrArgs(RelayPort)] {
				set relayport [FormattoASCII [string replace [string totitle $arrArgs(RelayPort) 0 end] 3 7 ""] 12]
				if { [string range $data 132 166] != $relayport } {
					set res 0
				}
			}
			if [info exists arrArgs(PortSpeed)] {
				regsub -all " " [string range $data 168 178] "" newportspeed
				if { $arrArgs(PortSpeed) != [format %d 0x0$newportspeed]} {
					set res 0
				}
			}
			if [info exists arrArgs(ClusterRole)] {
				if { $arrArgs(ClusterRole) != [format %d 0x0[string range $data 213 214]] } {
					set res 0
				}
			}
			if [info exists arrArgs(Description)] {
				set description [FormattoASCII $arrArgs(Description) 32]
				if { [string range $data 174 268] != $description } {
					set res 0
				}
			}
			if [info exists arrArgs(Hostname)] {
				set hostname [FormattoASCII $arrArgs(Hostname) 32]
				if { [string range $data 270 364] != $hostname } {
					set res 0
				}
			}
			;#other segment not check
			return $res
		}
		#{Type CP SubOp 1 MemberId 1 ClusterKey test SrcIp 10.1.1.1 DstIp 10.1.1.2 Interval 30 Losscount 3}
		if { $arrArgs(Type) == "CP" } {
			set type [string range $data 33 34]
			if { $type != "03" } {
				set res 0
			}
			#CP报文有2中length，一种40byte，一种12byte
			if { [string range $data 36 40] != "00 28" && [string range $data 36 40] != "00 0C" } {
				set res 0
			}
			if [info exists arrArgs(SubOp)] {
				regsub -all {\s} [string range $data 42 46] "" subop
				if { $arrArgs(SubOp) != [format %d 0x0$subop] } {
					set res 0
				}
			}
			if [info exists arrArgs(Length)] {
				regsub -all {\s} [string range $data 48 52] "" length
				if { $arrArgs(Length) != $length } {
					set res 0
				}
			}
			if [info exists arrArgs(MemberId)] {
				regsub -all {\s} [string range $data 54 58] "" memberid
				if { $arrArgs(MemberId) != $memberid } {
					set res 0
				}
			}
			if [info exists arrArgs(ErrCode)] {
				regsub -all {\s} [string range $data 60 64] "" errcode
				if { $arrArgs(ErrCode) != $errcode } {
					set res 0
				}
			}
			if [info exists arrArgs(ClusterKey)] {
				set clusterkey [FormattoASCII $arrArgs(ClusterKey) 16]
				if { [string range $data 66 112] != $clusterkey } {
					set res 0
				}
			}
			if [info exists arrArgs(SrcIp)] {
				set ip [string range $data 114 124]
				if { [FormatIptoHex $arrArgs(SrcIp)] != $ip } {
					set res 0
				}
			}
			if [info exists arrArgs(DstIp)] {
				set ip [string range $data 126 136]
				if { [FormatIptoHex $arrArgs(DstIp)] != $ip } {
					set res 0
				}
			}
			if [info exists arrArgs(Interval)] {
				regsub -all {\s} [string range $data 138 142] "" interval
				if { $arrArgs(Interval) != [format %d 0x0$interval] } {
					set res 0
				}
			}
			if [info exists arrArgs(Losscount)] {
				regsub -all {\s} [string range $data 144 148] "" losscount
				if { $arrArgs(Losscount) != [format %d 0x0$losscount] } {
					set res 0
				}
			}
			return $res
		} else {
			return 0
		}
	} elseif { [string range $data 0 4] == "08 00" && [string range $data 33 34] == "06" } {
		if { $arrArgs(Type) == "CC" } {
			if [info exists arrArgs(OpCode)] {
				regsub -all {\s} [string range $data 126 130] "" opcode
				if { $arrArgs(OpCode) != [format %d 0x0$opcode] } {
					set res 0
				}
			}
			if [info exists arrArgs(CCType)] {
				regsub -all {\s} [string range $data 138 142] "" cctype
				if { $arrArgs(CCType) != [format %d 0x0$cctype] } {
					set res 0
				}
			}
			return $res
		} else {
			#PrintRes Print "!don't check cluster packet with type $Type!"
			return 0
		}
	} else {
		;#may not be a cluster packet
		return 0
	}
	
	
}

#added by gengtao 2010.11.11
proc CheckVrrpInData { record data } {
	array set arrArgs $record
	set type [string range $data 36 40]
	if  { $type == "81 00" } {
	    set type [string range $data 48 52]
	    if {$type == "08 00"} {
	    	set vrrp [string range $data 114 end]
	    } else {
	    	return 0
	    }	
	} elseif {$type == "08 00"} {
	   	set vrrp [string range $data 102 end]
	} else {
		return 0
	}
	set res 1
	if [info exists arrArgs(Priority)] {
		regsub -all " " [string range $vrrp 6 7] "" priority
		if { $arrArgs(Priority) != [format %d 0x0$priority]} {
			set res 0
		}
	}
	return $res
}


#added by gengtao 2010.11.15
proc CheckIpv6VrrpInData { record data } {
	array set arrArgs $record
	set ipv6vrrp [string range $data 162 end]
	set res 1
	if [info exists arrArgs(Version)] {
		regsub -all " " [string range $ipv6vrrp 0 0] "" version
		if { $arrArgs(Version) != [format %d 0x0$version]} {
			set res 0
		}
	}
	if [info exists arrArgs(Type)] {
		regsub -all " " [string range $ipv6vrrp 1 1] "" type
		if { $arrArgs(Type) != [format %d 0x0$type]} {
			set res 0
		}
	}
	if [info exists arrArgs(Vrid)] {
		regsub -all " " [string range $ipv6vrrp 3 4] "" vrid
		if { $arrArgs(Vrid) != [format %d 0x0$vrid]} {
			set res 0
		}
	}
	if [info exists arrArgs(Priority)] {
		regsub -all " " [string range $ipv6vrrp 6 7] "" priority
		if { $arrArgs(Priority) != [format %d 0x0$priority]} {
			set res 0
		}
	}
	if [info exists arrArgs(AdverInt)] {
		regsub -all " " [string range $ipv6vrrp 13 16] "" adverint
		if { $arrArgs(AdverInt) != [format %d 0x0$adverint]} {
			set res 0
		}
	}
	if [info exists arrArgs(Ipv6Address)] {
		set address1 [FormatHexIpv6 $arrArgs(Ipv6Address]
		regsub -all " " [string range $ipv6vrrp 24 end] " " address2
		if {$address1 != $address2} {
			set res 0
		}
	}
	return $res
}

proc CheckArpTypeInData { arptype data } {
    set flag [string range $data 36 40]
    if  { $flag == "81 00" } {
        #vlantag
        set arpoperation [string range $data 72 76]
    } elseif { $flag == "08 06" } {                       ;#修改判断逻辑
        #no vlantag
        set arpoperation [string range $data 60 64]
    } else {
    	return 0
    }
    if { $arptype == "request" && $arpoperation == "00 01" } {
        #puts bb
        return 1
    } elseif { $arptype == "reply" && $arpoperation == "00 02" } {;#修改判断逻辑
        #puts bb
        return 1
    } else {
        return 0
    }
}

proc CheckArpInData { arp data } {
    set flag [string range $data 36 40]
    if  { $flag == "81 00" } {
        #vlantag
        set arphardwaretype [string range $data 54 58]
        set arpprotocoltype [string range $data 60 64]
    } else {
        #no vlantag
        set arphardwaretype [string range $data 42 46]
        set arpprotocoltype [string range $data 48 52]
    }
    #set arphardwaretype [string range $data 42 46]
    #set arpprotocoltype [string range $data 48 52]
    if { $arphardwaretype == "00 01" && $arpprotocoltype == "08 00" } {
        #puts aa
        return 1
    } else {
        return 0
    }
}
proc CheckArpSenderHardwareAddressInData { sendermac data } {
    set flag [string range $data 36 40]
    if  { $flag == "81 00" } {
        #vlantag
        set data [string range $data 78 94]
    }
    if { $flag == "08 06" } {
        #no vlantag
        set data [string range $data 66 82]
    }
    regsub -all " " $data - data
    set sendermac [string toupper $sendermac]  ;#把小写字母转化为大写字母，避免判断错误
    if { $sendermac == $data } {
        return 1
    } else {
        return 0
    }
}
proc CheckArpTargetHardwareAddressInData { targetmac data } {
    set flag [string range $data 36 40]
    if  { $flag == "81 00" } {
        #vlantag
        set data [string range $data 108 124]
    }
    if { $flag == "08 06" } {
        #no vlantag
        set data [string range $data 96 112]
    }
    regsub -all " " $data - data
    set targetmac [string toupper $targetmac]  ;#把小写字母转化为大写字母，避免判断错误
    if { $targetmac == $data } {
        return 1
    } else {
        return 0
    }
}
proc CheckArpSenderProtocolAddressInData { senderip data } {
    set flag [string range $data 36 40]
    if  { $flag == "81 00" } {
        #vlantag
        set data [string range $data 96 106]
    }
    if { $flag == "08 06" } {
        #no vlantag
        set data [string range $data 84 94]
    }
    #puts $data
    set n1 [string range $data 0 1]
    set n2 [string range $data 3 4]
    set n3 [string range $data 6 7]
    set n4 [string range $data 9 10]
    set n1 "0x0$n1"
    set num1 [format "%i" $n1]
    set n2 "0x0$n2"
    set num2 [format "%i" $n2]
    set n3 "0x0$n3"
    set num3 [format "%i" $n3]
    set n4 "0x0$n4"
    set num4 [format "%i" $n4]
    set spring $num1
    append spring "." "$num2" "." "$num3" "." "$num4"
    if { $senderip == $spring } {
        #puts cc
        return 1
    } else {
        return 0
    }
}
proc CheckArpTargetProtocolAddressInData { targetip data } {
    set flag [string range $data 36 40]
    if  { $flag == "81 00" } {
        #vlantag
        set data [string range $data 126 136]
    }
    if { $flag == "08 06" } {
        #no vlantag
        set data [string range $data 114 124]
    }
    set n1 [string range $data 0 1]
    set n2 [string range $data 3 4]
    set n3 [string range $data 6 7]
    set n4 [string range $data 9 10]
    set n1 "0x0$n1"
    set num1 [format "%i" $n1]
    set n2 "0x0$n2"
    set num2 [format "%i" $n2]
    set n3 "0x0$n3"
    set num3 [format "%i" $n3]
    set n4 "0x0$n4"
    set num4 [format "%i" $n4]
    set spring $num1
    append spring "." "$num2" "." "$num3" "." "$num4"
    if { $targetip == $spring } {
        return 1
    } else {
        return 0
    }
}
proc CheckIgmpQueryVersionInData { version data } {
    set flag [string range $data 36 40]
    if  { $flag == "81 00" } {
        #vlantag
        set ipprotocol [string range $data 81 82]
        set iptotallength [string range $data 60 64]
        set igmptype [string range $data 126 127]
        set igmpmaxresptime [string range $data 129 130]
         set igmpgroup [string range $data 138 148]
    } else {
        #no vlantag
        set ipprotocol [string range $data 69 70]
        set iptotallength [string range $data 48 52]
        set igmptype [string range $data 114 115]
        set igmpmaxresptime [string range $data 117 118]
        set igmpgroup [string range $data 126 136]
    }
    if { $ipprotocol == "02" } {
        #igmp packet
		# puts $iptotallength
		# puts $igmptype
        if { ($iptotallength == "00 24" || $iptotallength == "00 28") && $igmptype == "11" } {
            #igmp query version 3
            if { $version == 3 } {
                return 1
            } else {
                return 0
            }
        }
        if { $iptotallength == "00 20"} {
            #igmp query version 1 or 2
            if { $igmpmaxresptime == "00" && $igmpgroup == "00 00 00 00"} {
                #igmp query version 1
                if { $version == 1 } {
                    return 1
                } else {
                    return 0
                }
            } elseif {$igmpmaxresptime == "64" && $igmpgroup == "00 00 00 00"} {
                #igmp query version 2
                if { $version == 2 } {
                    return 1
                } else {
                    return 0
                }
            }
        } else {
            return 0
        }
    } else {
        return 0
    }
    return 0
}


proc CheckIgmpV2SpecialQueryInData { ipaddress data } {
    set flag [string range $data 36 40]
    if  { $flag == "81 00" } {
        #vlantag
        set ipprotocol [string range $data 81 82]
        set iptotallength [string range $data 60 64]
        set igmptype [string range $data 126 127]
        set igmpmaxresptime [string range $data 129 130]
         set igmpgroup [string range $data 138 148]
    } else {
        #no vlantag
        set ipprotocol [string range $data 69 70]
        set iptotallength [string range $data 48 52]
        set igmptype [string range $data 114 115]
        set igmpmaxresptime [string range $data 117 118]
        set igmpgroup [string range $data 126 136]
    }
    if { $ipprotocol == "02" } {
       #igmp packet
#        if { $iptotallength == "00 24" && $igmptype == "11" } {
#            #igmp query version 3
#            if { $version == 3 } {
#                return 1
#            } else {
#                return 0
#            }
#        }
        if { $iptotallength == "00 20" && $igmptype == "11" } {
            #igmp query version 1 or 2
            if { $igmpmaxresptime != "00" && $igmpgroup == $ipaddress} {
            		return 1
                } else {
                	return 0
                }
             }
       }
    return 0
}

#######################################################
#
# CheckIgmpV3QueryGroup :检查抓到的igmpv3 query数据包中的group address是否符合预期值
#
#   args:
#                ipaddress: 组播地址的预期值
#                data: 实际捕获的报文
#
#   return: 
#                1 :满足要求
#                0:不满足要求
#
########################################################## 	

proc CheckIgmpV3QueryGroup { ipaddress data } {
    set flag [string range $data 36 40]
    if  { $flag == "81 00" } {
        #vlantag
        set ipprotocol [string range $data 81 82]
        set iptotallength [string range $data 60 64]
        set igmptype [string range $data 126 127]
        set igmpmaxresptime [string range $data 129 130]
        set igmpgroup [string range $data 138 148]
    } else {
        #no vlantag
        set ipprotocol [string range $data 69 70]
        set iptotallength [string range $data 48 52]
        set igmptype [string range $data 114 115]
        set igmpmaxresptime [string range $data 117 118]
        set igmpgroup [string range $data 126 136]
    }
    if { $ipprotocol == "02" } {
       #igmp packet
        if { ($iptotallength == "00 24" || $iptotallength == "00 28") && $igmptype == "11" } {
            #igmp query version 3
            set ipaddress [split $ipaddress .]
            for {set i 0} { $i < [llength $ipaddress]} { incr i} {
            	if {$i == 0} {
            		set tem [format %02x [lindex $ipaddress $i]]
            	} else {
            		append tem " "
            		append tem [format %02x [lindex $ipaddress $i]]
            	}
            }
            set ipaddress $tem
			#            puts $ipaddress
			#            puts $igmpgroup
			#            puts $igmpmaxresptime
			set flag [regexp -nocase $ipaddress $igmpgroup match]
			if { $igmpmaxresptime != "00" && $flag == 1} {
            		return 1
                } else {
                	return 0
                }
            }
            
    }
    return 0
}

#######################################################
#
# CheckIgmpV3QuerySoure :检查抓到的igmpv3 query数据包中的source address是否符合预期值
#
#   args:
#                ipaddress: 组播源地址的预期值
#                data: 实际捕获的报文
#
#   return: 
#                1 :满足要求
#                0:不满足要求
#
########################################################## 	

proc CheckIgmpV3QuerySoure { ipaddress data } {
    set flag [string range $data 36 40]
    if  { $flag == "81 00" } {
        #vlantag
        set ipprotocol [string range $data 81 82]
        set iptotallength [string range $data 60 64]
        set igmptype [string range $data 126 127]
        set igmpmaxresptime [string range $data 129 130]
        set igmpsource [string range $data 162 172]
    } else {
        #no vlantag
        set ipprotocol [string range $data 69 70]
        set iptotallength [string range $data 48 52]
        set igmptype [string range $data 114 115]
        set igmpmaxresptime [string range $data 117 118]
        set igmpsource [string range $data 150 160]
    }
    if { $ipprotocol == "02" } {
       #igmp packet
        if { ($iptotallength == "00 24" || $iptotallength == "00 28") && $igmptype == "11" } {
            #igmp query version 3
            set ipaddress [split $ipaddress .]
            for {set i 0} { $i < [llength $ipaddress]} { incr i} {
            	if {$i == 0} {
            		set tem [format %02x [lindex $ipaddress $i]]
            	} else {
            		append tem " "
            		append tem [format %02x [lindex $ipaddress $i]]
            	}
            }
            set ipaddress $tem
			#            puts $ipaddress
			#            puts $igmpsource
			#            puts $igmpmaxresptime
			set flag [regexp -nocase $ipaddress $igmpsource match]
			if { $igmpmaxresptime != "00" && $flag == 1} {
            		return 1
                } else {
                	return 0
                }
            }
            
    }
    return 0
}


#######################################################
#
# CheckOffsetValueInData :检查抓到的分片数据包的offset值是否正确
#
#   args:
#                offset: the ip offset vlaue in fragmented packet  
#                data: actual frame data
#
#   return: 
#                1 :满足要求
#                0:不满足要求
#
########################################################## 	  
proc CheckOffsetVlaueInData {offset data} {
set value1 [string index $data 73]
set value2 [string range $data 75 76]
append value $value1 $value2
set num [format "%i" 0x0$value]
if { $num == $offset } {
                return 1
            } else {
                return 0
            }
}
#######################################################
#
# CheckLengthOfData :检查抓到的数据包长度,单位字节
#
#   args:
#                length: the ip offset vlaue in fragmented packet  
#                data: actual frame data
#
#   return: 
#                1 :满足要求
#                0:不满足要求
#
########################################################## 	  
proc CheckLengthOfData {length data} {
if { $length == [llength $data] } {
                return 1
            } else {
                return 0
            }
}
     
#######################################################
#
# CheckSrcMacInData :检查抓到的流source mac是否满足镜像的要求
#
#   args:
#                scrmac: source mac
#                data: actual frame data
#
#   return: 
#                1 :满足要求
#                0:不满足要求
#
########################################################## 
proc CheckSrcMacInData { srcmac data } {
    
    #Get source mac from data
    set data [string range $data 18 34]
    regsub -all " " $data - data
    set srcmac [string toupper $srcmac]  ;#把小写字母转化为大写字母，避免判断错误
    if { $srcmac == $data } {
        return 1
    } else {
        return 0
    }
}

#######################################################
#
# CheckDstMacInData :检查抓到的流destination mac是否满足镜像的要求
#
#   args:
#                dstmac: destination mac
#                data: actual frame data
#
#   return: 
#                1 :满足要求
#                0:不满足要求
#
########################################################## 
proc CheckDstMacInData { dstmac data } {
    
    #Get destination mac from data
    set data [string range $data 0 16]
    regsub -all " " $data - data
    set dstmac [string toupper $dstmac]   ;#把小写字母转化为大写字母，避免判断错误
    if { $dstmac == $data } {
        return 1
    } else {
        return 0
    }
}

#######################################################
#
# CheckSrcIpInData :检查抓到的流source ip是否满足镜像的要求
#
#   args:
#                srcip: source ip
#                data: actual frame data
#
#   return: 
#                1 :满足要求
#                0:不满足要求
#
########################################################## 
proc CheckSrcIpInData { srcip data } {
    #Get source ip from data
    #set data [string range $data 90 100]
    #modified by xuyongc 2005-10-13  
    set vlanflag [string range $data 36 40]
    if  { $vlanflag == "81 00" } {
        set data [string range $data 90 100]
    } else {
        set data [string range $data 78 88]
    }
    set n1 [string range $data 0 1]
    set n2 [string range $data 3 4]
    set n3 [string range $data 6 7]
    set n4 [string range $data 9 10]
    set n1 "0x0$n1"
    set num1 [format "%i" $n1]
    set n2 "0x0$n2"
    set num2 [format "%i" $n2]
    set n3 "0x0$n3"
    set num3 [format "%i" $n3]
    set n4 "0x0$n4"
    set num4 [format "%i" $n4]
    set spring $num1
    append spring "." "$num2" "." "$num3" "." "$num4"
    if { $srcip == $spring } {
        return 1
    } else {
        return 0
    }
}

#######################################################
#
# CheckDstIpInData :检查抓到的流destination ip是否满足镜像的要求
#
#   args:
#                dstip: destination ip
#                data: actual frame data
#
#   return: 
#                1 :满足要求
#                0:不满足要求
#
########################################################## 
proc CheckDstIpInData { dstip data } {
    #Get destination ip from data
    #set data [string range $data 102 112]
    #modified by xuyongc 2005-10-13  
    set vlanflag [string range $data 36 40]
    if  { $vlanflag == "81 00" } {
        set data [string range $data 102 112]
    } else {
        set data [string range $data 90 100]
    }
    set n1 [string range $data 0 1]
    set n2 [string range $data 3 4]
    set n3 [string range $data 6 7]
    set n4 [string range $data 9 10]
    set n1 "0x0$n1"
    set num1 [format "%i" $n1]
    set n2 "0x0$n2"
    set num2 [format "%i" $n2]
    set n3 "0x0$n3"
    set num3 [format "%i" $n3]
    set n4 "0x0$n4"
    set num4 [format "%i" $n4]
    set spring $num1
    append spring "." "$num2" "." "$num3" "." "$num4"
    if { $dstip == $spring } {
        return 1
    } else {
        return 0
    }
}

#######################################################
#
# CheckDstMacInData :检查抓到的流cos是否满足镜像的要求
#
#   args:
#                cos: cos mac
#                data: actual frame data
#
#   return: 
#                1 :满足要求
#                0:不满足要求
#
########################################################## 
proc CheckCosInData { cos data }  {
    set data [string range $data 42 42]
	set data [expr 0x0$data / 2]		
	if { $cos == $data } {
	    return 1
    } else {
        return 0
    }
}   
  
#######################################################
#
# CheckVlanTagInData :检查抓到的流vlan tag是否满足镜像的要求
#
#   args:
#                vlantag: vlan tag
#                data: actual frame data
#
#   return: 
#                1 :满足要求
#                0:不满足要求
#
#*********************************************************************
# Change log:
#     - 2009.10.19 qiaoyua 增加VlanTag对于DoubleTag的支持
#*********************************************************************
#
##########################################################
#CheckCaptureStream $ChasId $Card3 $Port3 VlanTag {100 10}
#VlanTag取一个值，则仅判断报文第一层Tag;VlanTag取两个值，第一个值为外层Tag值，第二个值为内层Tag的值
#取值为-1，表示没有VlanTag;取值为0，表示不关心是否有VlanTag;取值为>0，表示要求有VlanTag，该值为Vid
proc CheckVlanTagInData { vlantag data } {
	#VlanTag只有一个值，
	if {[llength $vlantag] == 1} {
	    if { $vlantag == 0 } {
	        #VlanTag为0，不关心是否有Tag
	        return 1
	    } elseif { $vlantag > 0 } {
	        #VlanTag>0，对报文进行判断
	        if { [ string range $data 36 40 ] == "81 00" } {
	            set temp [ string range $data 43 46 ]
	            regsub -all " " $temp {} temp
	            set temp "0x0$temp"
	            set temp [format "%i" $temp]
	            if { $vlantag == $temp } {
	                return 1
	            }
	        }
	    } elseif { $vlantag == -1 } {
	    	#VlanTag为-1，报文不存在Tag
	        if { [ string range $data 36 40 ] != "81 00" } {
	            return 1
	        }
	    } else {}
	} elseif {([llength $vlantag] > 2) || ([llength $vlantag] < 0)} {
	} else {
		#VlanTag有两个取值
		set outtag [lindex $vlantag 0]
		set intag [lindex $vlantag 1]
	    if { $outtag == 0 } {
	    		#外层VlanTag为0时
	        	if {$intag == 0} {
	        		#outtag=0 inTag=0
					return 1
				#outtag=0 inTag=-1
	        	} elseif {$intag == -1} {
	        		if { [ string range $data 48 52 ] != "81 00" } {
						return 1
	        		}
	        	#outtag=0 inTag>0
	        	} elseif {$intag > 0} {
	        		if {[ string range $data 36 40 ] == "81 00"} {
						if { [ string range $data 48 52 ] == "81 00" } {
							set temp [string range $data 55 58 ]
				            regsub -all " " $temp {} temp
				            set temp "0x0$temp"
				            set temp [format "%i" $temp]
				            if { $intag == $temp } {
				                return 1
				            } 
						} 
					} 
				} else {}
			} elseif { $outtag > 0} {
				#外层VlanTag>0时
				if { [ string range $data 36 40 ] == "81 00" } {
		            set temp [ string range $data 43 46 ]
		            regsub -all " " $temp {} temp
		            set temp "0x0$temp"
		            format "%i" $temp
		            if { $outtag == $temp } {
		            	#当外层VlanTag匹配时，再对内层VlanTag值进行判断
		                if {$intag == 0} {
							return 1
		                } elseif {$intag == -1} {
		                	if { [ string range $data 48 52 ] != "81 00" } {
								return 1
			        		} 
		                } elseif {$intag > 0} {
		                	if { [ string range $data 48 52 ] == "81 00" } {
		                		set tmp [ string range $data 55 58 ]
		                		regsub -all " " $tmp {} tmp
		                		set tmp "0x0$tmp"
		                		set tmp [format "%i" $tmp]
		                		if {$intag == $tmp} {
		                			return 1
		                		}
		                	}
		                } else {}
		            }
		        }
		} else {}
	}
	return 0
}

######################################################################
#
# CheckAllCaptureStream: 检查抓到的流是否满足镜像的要求，
#                   目前从抓到的包数,vlan tag,source mac,destination mac
#                   source ip ,destination ip几方面判断抓到的流
#
# args:
#           chas:   抓包端口所在chas 
#           card:   抓包端口所在card
#           port:   抓包端口所在port
#           Srcmac: 源mac
#           Dstmac: 目的mac
#           VlanTag:
#                   取值 -1 不带tag,0 不关心带不带tag,>0 要求大的tag
#           
#
# return: 返回满足条件的个数
# 
# examples:
#           CheckTransmitDone $portList
######################################################################  
proc CheckAllCaptureStream { chas card port args } {
    
    array set arrArgs $args 	
    set counter 0   ;#内部使用的计数器
    # Get the number of frames captured
	capture get $chas $card $port
	set numFrames [capture cget -nPackets]
	#PrintRes Print "\n$numFrames frames captured"
	
	captureBuffer get $chas $card $port 1 $numFrames
    for {set i 1} {$i <= $numFrames} {incr i} {
        # Note that the frame number starts at 1
        captureBuffer getframe $i
        # Get the actual frame data
        set data [captureBuffer cget -frame]
        set ret 1
        #SrcMac
        if {[info exist arrArgs(SrcMac)]} {
            set ret [ expr $ret * [ CheckSrcMacInData $arrArgs(SrcMac) $data ] ]
        }
        
        #DstMac
        if {[info exist arrArgs(DstMac)]} {
            set ret [ expr $ret * [ CheckDstMacInData $arrArgs(DstMac) $data ] ]
        }
        
        #SrcIp
        if {[info exist arrArgs(SrcIp)]} {
            set ret [ expr $ret * [ CheckSrcIpInData $arrArgs(SrcIp) $data] ]
        }
        
        #DstIp
        if {[info exist arrArgs(DstIp)]} {
            set ret [ expr $ret * [ CheckDstIpInData $arrArgs(DstIp) $data] ]
        }
            
        #VlanTag
        if {[info exist arrArgs(VlanTag)]} {
            set ret [ expr $ret * [ CheckVlanTagInData $arrArgs(VlanTag) $data ] ]
        }
        
        #cos
        if {[info exist arrArgs(cos)]} {
             set ret [expr $ret * [ CheckCosInData $arrArgs(cos) $data] ]
        }
             
        if { $ret != 0 } {
            incr counter
        }
            
    }    
    return $counter
}

#####################################################################################
#
# StartMulticastSend: 在IXIA端口上启动组播发送
#
# 参数: 
#           chas card port:  IXIA端口的chas, card和port
#           ipaddr:   组播业务的起始源地址，必选参数
#           group:    组播业务的起始组地址，必选参数  
#           count:   组播业务的组地址数，可选参数，默认为1
#           srccout: 组播业务的源地址数，可选参数，默认为1
#           rate:    组播业务的百分比速率，可选参数，默认为1
# 返回值:
#	        空
# 
# 使用举例:
#           StartMulticastSend $chas $card1 $port1 1.1.1.100 225.0.0.1
#			StartMulticastSend 1 12 1 1.1.1.100 225.0.0.1 10 10 100
#           
########################################################################################
proc StartMulticastSend {chas card port ipaddr group {count 1} {srccount 1} {rate 1}} {

    set destmac [ MIp2Mac $group ]
    set srcip [list $ipaddr]
    set destip [list $group]
           
	set portlist [list [list $chas $card $port]]
	
	ixStopTransmit portlist
	port setFactoryDefaults $chas $card $port
	idle_after 5000
	port setDefault
	port set $chas $card $port
	
	#Stream 1 at ports
	stream setDefault

	#rateMode必须是第一个跟在setDefault的配置缺省是适用gap
	stream config -rateMode usePercentRate
	stream config -percentPacketRate $rate


	stream config -saRepeatCounter increment
	stream config -sa {00 01 02 03 04 07}
	stream config -numSA $srccount
	#YOU can change it    


	stream config -daRepeatCounter increment
	stream config -da $destmac
	stream config -daStep 1
	stream config -numDA $count

	stream config -dataPattern x5555
	stream config -patternType  repeat

	stream config -dma contPacket
	#contPacket
	stream config -framesize 1024


	# Set up IP: lowcost packets
	# Source address varies by incrementing the network part
	# Destination address varies by incrementing the host part
    
	set portIP $srcip
	set portMask {255.255.255.0}
	set destIP $group
	set destMask {255.255.255.0}

	ip setDefault
	#ip config -cost lowCost
	ip config -sourceIpAddr $portIP
	ip config -sourceIpMask $portMask
	ip config -sourceClass classC
	ip config -destIpAddr $destIP
	ip config -destIpMask $destMask
	ip config -destClass classC
	ip config -destIpAddrMode ipIncrHost
	ip config -destIpAddrRepeatCount $count
	ip set $chas $card $port

	protocol setDefault
	protocol config -name ipV4
	protocol config -ethernetType ethernetII
	protocol config -appName Udp

	# Set up UDP
	udp setDefault
	udp config -sourcePort 1036
	udp config -destPort 49152
	udp set $chas $card $port

	
	if {[stream set $chas $card $port 1] != 0} {
		PrintRes Print "----------\tCan't set Transmit stream on $chas $card $port 1"
	}
	ixWritePortsToHardware portlist
	idle_after 5000
	ixStartTransmit portlist
	
}


#####################################################################################
#
# StopMulticastSend: 在IXIA端口上停止组播发送
#
# 参数: 
#           chas card port:  IXIA端口的chas, card和port
# 返回值:
#	        空
# 
# 使用举例:
#           StopMulticastSend $chas $card1 $port1
#			StopMulticastSend 1 12 1
#           
########################################################################################
proc StopMulticastSend {chas card port} {
	set portlist [list [list $chas $card $port]]
	if {[ixStopTransmit portlist] != 0} {
		PrintRes Print "stop multicast send on $chas $card $port failed"
	}
}


#####################################################################################
#
# StartMulticastReceive: 在IXIA端口上通过IGMP协议模拟启动组播接收
#
# 参数: 
#           chas card port:  IXIA端口的chas, card和port
#           ipaddr:   IGMP报告的起始源地址，必选参数
#           group:    IGMP报告的起始组地址，必选参数  
#           count:   IGMP报告的组地址数，可选参数，默认为1
#           srccout: IGMP报告的源地址数，可选参数，默认为1
#           netmask:  IGMP报告的起始源地址子网掩码，必选参数 格式如:16 24
# 返回值:
#	        空
# 
# 使用举例:
#           StartMulticastReceive $chas $card1 $port1 1.1.1.100 16 225.0.0.1
#			StartMulticastReceive 1 12 1 1.1.1.100 16 225.0.0.1 10 10
#
########################################################################################
proc StartMulticastReceive {chas card port ipaddr netmask group {count 1} {srccount 1}} {
    
	set srcip [list $ipaddr]
    set destip [list $group]
           
	set portlist [list [list $chas $card $port]]
	
	ixStopTransmit portlist
	port setFactoryDefaults $chas $card $port
	idle_after 5000
	port setDefault
	port set $chas $card $port
	
	#############add by gw#############
	# Set up IP table with our IP-MAC and Gateway
	ipAddressTable setDefault
	#ipAddressTable config -defaultGateway 20.1.1.1
	ipAddressTableItem setDefault
	puts "srcip= $srcip"
	puts "ip adress= $ipaddr"
	ipAddressTableItem config -fromIpAddress $srcip
	#ipAddressTableItem config -fromMacAddress {00 11 11 00 00 11}
	ipAddressTableItem config -numAddresses 1
	ipAddressTableItem config -enableUseNetwork 1
	ipAddressTableItem config -netMask $netmask
	ipAddressTableItem set
	ipAddressTable addItem
	ipAddressTable set $chas $card $port
	#############end edit##############
	
	igmpServer setDefault
	igmpServer config -reportMode 1
	igmpServer config -reportFrequency 100
	igmpServer config -repeatCount 1000
	igmpServer set $chas $card $port
	
	# Set up IGMP table for group addresses
	igmpAddressTable clear
	igmpAddressTableItem setDefault
	igmpAddressTableItem config -fromGroupAddress $destip
	igmpAddressTableItem config -fromClientAddress $srcip
	igmpAddressTableItem config -numGroupAddresses $count
	igmpAddressTableItem config -numClientAddresses $srccount
	igmpAddressTableItem set
	igmpAddressTable addItem
	igmpAddressTable set $chas $card $port
	
	# Start the protocol server for IGMP
	protocolServer setDefault
	protocolServer config -enableIgmpQueryResponse true
	protocolServer set $chas $card $port
	protocolServer write $chas $card $port

	
	# Tell the hardware about it,write port configuration to hardware
	ixWritePortsToHardware portlist
	idle_after 5000
	###start the IgmpServer protocol server 
	if {[ixTransmitIgmpJoin portlist] != 0} {
   		PrintRes Print "Could not Transmit Igmp Join on $portlist"
   	}

}

#####################################################################################
#
# StopMulticastReceive: 在IXIA端口上停止IGMP协议模拟
#
# 参数: 
#           chas card port:  IXIA端口的chas, card和port
# 返回值:
#	        空
# 
# 使用举例:
#           StopMulticastReceive $chas $card1 $port1
#			StopMulticastReceive 1 12 1
#           
########################################################################################
proc StopMulticastReceive {chas card port} {
	set portlist [list [list $chas $card $port]]
	if {[ixTransmitIgmpLeave portlist] != 0} {
   		PrintRes Print "Could not Stop Igmp Leave on $portlist"
   	}
}


#####################################################################################
#
# CheckReceiveRate: 通过计算IXIA接收端口速率和发送端口速率检查流量接收
#
# 参数: 
#           rchas rcard rport:  接收端口的chas, card和port
#           schas scard sport:  发送端口的chas, card和port
#           flga:接收情况标识，目前支持none和full，分别表示线速接收和无法接收
# 返回值:
#	        空
# 
# 使用举例:
#		card2:port2线速接收card1:port1发送的流量
#           CheckReceiveRate $chas $card2 $port2 $chas $card1 $port1 full
#		12:2无法接收12:1发送的流量
#			CheckReceiveRate 1 12 2 1 12 1 none
#           
# 说明:该过程仅判断接收速率，并不对包进行检查
########################################################################################
proc CheckReceiveRate {rchas rcard rport schas scard sport flag} {
 
 #get send rate of schas scard sport
 stat getRate statBytesSent $schas $scard $sport
 set bsr [stat cget -bytesSent]
 PrintRes Print "The bytes sent from $scard : $sport is : $bsr"
 
 stat getRate statBytesReceived $rchas $rcard $rport
 set  brr [stat cget -bytesReceived]
 PrintRes Print "The bytes received from $rcard : $rport is : $brr"
 if {$bsr != 0} {
 	append bsr ".0"
 	set rrate [expr $brr/$bsr]
 } else {
 	set rrate 0
 }
 
 if {$flag == "none"} {
 	if {$rrate < 0.1} {
 		PrintRes Print "Receive rate \"$flag\" on $rchas $rcard $rport is $rrate, PASSED!"
 	} else {
 		PrintRes Print "!Receive rate \"$flag\" on $rchas $rcard $rport is $rrate, FAILED!"
 	}
 } else {
 	if {$rrate > 0.9} {
 		PrintRes Print "Receive rate \"$flag\" on $rchas $rcard $rport is $rrate, PASSED!"
 	} else {
 		PrintRes Print "!Receive rate \"$flag\" on $rchas $rcard $rport is $rrate, FAILED!"
 	}
 	
 }
}






#################################################################
#
# ShowReceiveRate显示端口速率
#
# args:
#     chas1, port1, card1:端口1的chas, port, card
#     chas2, port2, card2:端口2的chas, port, card
# 
# return: 
#
# addition:
#
# examples:
#     ShowReceiveRate 1 2 1 1 2 2
# 
###########################################################
proc ShowReceiveRate { chas1 card1 port1 chas2 card2 port2} {
    stat getRate statBytesSent $chas1 $card1 $port1
 	set bsr [stat cget -bytesSent]
 	stat getRate statBytesReceived $chas2 $card2 $port2
 	set  brr [stat cget -bytesReceived]
 	if {$bsr != 0} {
 		append bsr ".0"
 		PrintRes Print "$card2:$port2 bytes received rate [expr $brr/$bsr]"
 		return [expr $brr/$bsr]
 	} else {
 		 PrintRes Print "$card1:$port1 bytes send rate is zero"
 	}
}

###############################################################
#
# CheckStreamReceive :检查端口收到包的比例
#
# args: 
#     chas1, port1, card1:端口1的chas, port, card
#     chas2, port2, card2:端口2的chas, port, card
#     num:要求的比例
#
# return: 
#       0 :不符合要求
#       1 :符合要求
#
# addition:
#
# examples:
#     CheckStreamReceive 1 2 1 1 2 2 4
#
################################################################
proc CheckStreamReceive { chas1 card1 port1 chas2 card2 port2 num } {    
     idle_after 2000        
     stat getRate statBytesReceived $chas1 $card1 $port1
 	 set rate1 [stat cget -bytesReceived]
 	 stat getRate statBytesReceived $chas2 $card2 $port2
 	 set rate2 [stat cget -bytesReceived]
 	 PrintRes Print "The port ${card1}:${port1} received rate is : $rate1"
 	 PrintRes Print "The port ${card2}:${port2} received rate is : $rate2"
 	 append rate2 ".1"
     set num1 [expr $rate1 / $rate2 - $num ]
     set num2 [expr abs($num1)]
     #PrintRes Print $num2
     if { $num2 <= 0.26 } {
        return 1
     } else {
        return 0
     }
}

###############################################################
#
# CheckStreamSentReceive :检查端口收发包的比例
#
# args: 
#     chas1, port1, card1:端口1的chas, port, card
#     chas2, port2, card2:端口2的chas, port, card
#     num:要求的比例
#
# return: 
#       0 :不符合要求
#       1 :符合要求
#
# addition:
#
# examples:
#     CheckStreamSentReceive 1 2 1 1 2 2 4
#
################################################################
proc CheckStreamSentReceive { chas1 card1 port1 chas2 card2 port2 num {waittimer 10000} } {    
    Wait 2000        
    for {set i 0} {$i < 10} {incr i} {
        stat getRate statBytesSent $chas1 $card1 $port1
     	set rate1 [stat cget -bytesSent]
 	    if { $rate1 == 0 } {
 	        Wait 100
 	        continue
 	        if { $i == 9 } {
 		        PrintRes Print "!start transmit error!"
 		        return 0
 	        }
 	    } else {
 	        break
 	    }
 	}
 	for {set j 0} {$j < 10} {incr j} { 
# 	    IdleAfter $waittimer
        stat getRate statBytesSent $chas1 $card1 $port1
        set rate1 [stat cget -bytesSent]
     	stat getRate statBytesReceived $chas2 $card2 $port2
     	set rate2 [stat cget -bytesReceived]    	 	
     	if { $num == 0 } {
     		if { $rate1 == $rate2 } {
     			PrintRes Print "The port ${card1}:${port1} sent Frames rate is : $rate1"
                PrintRes Print "The port ${card2}:${port2} received Frames rate is : $rate2"
                return 0
            } else {
     	    	set num2 [expr abs( ( $rate1.0 / ( $rate1.0 - $rate2.0 ) - 1 ) / 1 ) ]
     	    }
     	} else {
    	    set num2 [expr abs( ( $rate1.0 / $rate2.1 - $num ) / $num )]
        }
        #PrintRes Print $num2
        if { $num2 <= 0.05 } {
            PrintRes Print "The port ${card1}:${port1} sent Bytes rate is : $rate1"
            PrintRes Print "The port ${card2}:${port2} received Bytes rate is : $rate2"
            return 1
        } else {
            if { $j == 9 } {
                PrintRes Print "The port ${card1}:${port1} sent Bytes rate is : $rate1"
                PrintRes Print "The port ${card2}:${port2} received Bytes rate is : $rate2"
                return 0
            } else {
                IdleAfter $waittimer
                continue
            }
        }
    }    
}
proc CheckFramesSentFilter { chas1 card1 port1 chas2 card2 port2 minnum {maxnum -1} } {    
    idle_after 2000        
    stat getRate statFramesSent $chas1 $card1 $port1
 	set rate1 [stat cget -framesSent]
 	stat getRate statcaptureFilter $chas2 $card2 $port2
 	set rate2 [stat cget -captureFilter]
 	PrintRes Print "The port ${card1}:${port1} sent frame rate is : $rate1"
 	PrintRes Print "The port ${card2}:${port2} filter frame rate is : $rate2"
 	append rate1 ".0"
 	if { $rate1 == 0 } {
 		PrintRes Print "!start transmit error!"
 		return 0
 	}
 	append rate2 ".1"
 	if { $maxnum == -1 } {
     	if { $minnum == 0 } {
     	    set num1 [expr $rate2 / $rate1 - $minnum]
     	    set num2 [expr abs($num1)]
     	} else {
    	    set num1 [expr $rate1 / $rate2 - $minnum ]
        	set num2 [expr abs($num1)]
        }
        if { $num2 <= 0.33 } {
            return 1
        } else {
            return 0
        } 
    } else {
        set result [expr $rate1 / $rate2]
        #PrintRes Print $num2
        if { $result >= $minnum && $result <= $maxnum } {
            return 1
        } else {
            return 0
        }
    }
}
proc CheckFramesSentReceive { chas1 card1 port1 chas2 card2 port2 num {waittimer 10000}} {    
    Wait 2000 
    for {set i 0} {$i < 10} {incr i} {
        stat getRate statFramesSent $chas1 $card1 $port1
 	set rate1 [stat cget -framesSent]
 	    if { $rate1 == 0 } {
 	        Wait 100
 	        continue
 	        if { $i == 9 } {
 		        PrintRes Print "!start transmit error!"
 		        return 0
 	        }
 	    } else {
 	        break
 	    }
 	}
 	for {set j 0} {$j < 10} {incr j} { 
# 	    IdleAfter $waittimer	    
     	stat getRate statFramesReceived $chas2 $card2 $port2
 	set rate2 [stat cget -framesReceived]    	 	
     	if { $num == 0 } {
     		if { $rate1 == $rate2 } {
     			PrintRes Print "The port ${card1}:${port1} sent Frames rate is : $rate1"
                PrintRes Print "The port ${card2}:${port2} received Frames rate is : $rate2"
                return 0
            } else {
	     	    set num2 [expr abs( ( $rate1.0 / ( $rate1.0 - $rate2.0 ) - 1 ) / 1 ) ]
	     	}
     	} else {
    	    set num2 [expr abs( ( $rate1.0 / $rate2.1 - $num ) / $num )]
        }
        #PrintRes Print $num2
        if { $num2 <= 0.05 } {
            PrintRes Print "The port ${card1}:${port1} sent Frames rate is : $rate1"
            PrintRes Print "The port ${card2}:${port2} received Frames rate is : $rate2"
            return 1
        } else {
            if { $j == 9 } {
                PrintRes Print "The port ${card1}:${port1} sent Frames rate is : $rate1"
                PrintRes Print "The port ${card2}:${port2} received Frames rate is : $rate2"
                return 0
            } else {
                IdleAfter $waittimer
                continue
            }
        }
    }          
}


proc GetStreamSentReceive { chas1 card1 port1 chas2 card2 port2 } {    
    idle_after 2000        
    stat getRate statBytesSent $chas1 $card1 $port1
 	set rate1 [stat cget -bytesSent]
 	stat getRate statBytesReceived $chas2 $card2 $port2
 	set rate2 [stat cget -bytesReceived]
 	PrintRes Print "The port ${card1}:${port1} sent rate is : $rate1"
 	PrintRes Print "The port ${card2}:${port2} received rate is : $rate2"
 	append rate1 ".0"
 	if { $rate1 == 0 } {
 		PrintRes Print "!start transmit error!"
 		return -1
 	}
 	append rate2 ".1"	
 	set num1 [expr $rate1 / $rate2 ]
    return $num1
}

##########################################################
#
# CheckStreamReceiveRate:检查端口出包速率
#
# args:   
#     chas1, port1, card1:端口1的chas, port, card
#     rate:要求的速率
#   
# return: 
#     0 :不符合要求
#     1 :符合要求
#
# addition:
#
# examples:
#     CheckStreamReceiveRate 1 2 1 50
#
################################################################
#该函数不太适合实际使用，请使用CheckFramesReceiveRate
proc CheckStreamReceiveRate { chas1 card1 port1 rate } {
    stat getRate statBytesReceived $chas1 $card1 $port1
 	set rate1 [stat cget -bitsReceived]
 	PrintRes Print "The reciever bitss rate of $chas1 $card1 $port1 is $rate1."
	if { $rate == 0 } {
		return [expr $rate1 == 0?1:0]
	} else {
	 	#set num [ expr abs ( $rate1 - $rate ) / "$rate.0" ]    ;# 将绝对值比较改为相对值比较
		return [expr abs ( $rate1 - $rate ) / "$rate.0" <= 0.005?1:0]
	}
}

proc CheckFramesReceiveRate { chas1 card1 port1 rate } {
    stat getRate statFramesReceived $chas1 $card1 $port1
 	set rate1 [stat cget -framesReceived] 
 	PrintRes Print "The reciever frames rate of $chas1 $card1 $port1 is $rate1."
	if { $rate == 0 } {
		return [expr $rate1 == 0?1:0]
	} else {
	 	#set num [ expr abs ( $rate1 - $rate ) / "$rate.0" ]    ;# 将绝对值比较改为相对值比较
		return [expr abs ( $rate1 - $rate ) / "$rate.0" <= 0.01?1:0]
	}
}
proc GetStreamReceiveRate { chas1 card1 port1 } {
    stat getRate statBytesReceived $chas1 $card1 $port1
 	set rate1 [stat cget -bitsReceived]
 	PrintRes Print "The reciever bitss rate of $chas1 $card1 $port1 is $rate1"
 	return $rate1

}
proc GetFramesReceiveRate { chas1 card1 port1 } {
    stat getRate statFramesReceived $chas1 $card1 $port1
 	set rate1 [stat cget -framesReceived] 
 	PrintRes Print  "The reciever frames rate of $chas1 $card1 $port1 is $rate1"
 	return $rate1

}
proc GetFramesSent { chas card port } {
	stat get statFramesSent $chas $card $port
 	set counter [stat cget -framesSent] 
 	PrintRes Print "The sent frames counter of $chas $card $port is $counter"
 	return $counter
}
proc GetFramesReceived { chas card port } {
	stat get statFramesReceived $chas $card $port
 	set counter [stat cget -framesReceived] 
 	PrintRes Print "The received frames counter of $chas $card $port is $counter"
 	return $counter
}
proc GetBytesReceived { chas card port } {
	stat get statBytesReceived $chas $card $port
 	set counter [stat cget -bytesReceived] 
 	PrintRes Print "The received bytes counter of $chas $card $port is $counter"
 	return $counter
}
proc EnableMldHost { ChasId Card Port } {
	mldServer select $ChasId $Card $Port
    mldServer getHost host1
    mldHost config -enable true
    mldServer setHost host1
    mldServer write
}

proc DisableMldHost { ChasId Card Port } {
	mldServer select $ChasId $Card $Port
    mldServer getHost host1
    mldHost config -enable false
    mldServer setHost host1
    mldServer write
}

#只能修改第一个HOST的GROUP
proc ModifyMldGroups { ChasId Card Port Group } {
    mldServer select $ChasId $Card $Port
    mldServer getHost host1
    mldHost getGroupRange group1
    mldGroupRange config -groupIpFrom $Group
    if [mldHost setGroupRange group1 ] {
        logMsg "Error in setting group range group1"
    }
    mldServer write
}
proc ModifyMldGroupsMode { ChasId Card Port SourceMode } {
    if {$SourceMode == "Include"} {
		set SourceMode multicastSourceModeInclude
	}
	if {$SourceMode == "Exclude"} {
		set SourceMode multicastSourceModeExclude
	}
    mldServer select $ChasId $Card $Port
    mldServer getHost host1
    mldHost getGroupRange group1
    mldGroupRange config -sourceMode $SourceMode
    if [mldHost setGroupRange group1 ] {
        logMsg "Error in setting group range group1"
    }
    mldServer write
}
proc ModifyMldSourcelist { ChasId Card Port Number {Source 0} {Count -1} } {
    mldServer select $ChasId $Card $Port
    mldServer getHost host1
    mldHost getGroupRange group1
    mldGroupRange getSourceRange source$Number
    if { $Source != 0 } {
        mldSourceRange config -sourceIpFrom $Source
    }
    if { $Count != -1 } {
        mldSourceRange config -count $Count
    }
    if [mldGroupRange setSourceRange source$Number] {
        logMsg "Error in setting source range"
    }
    mldServer write
}

proc AddMldSourcelist { ChasId Card Port Number {Source 0} {Count -1} } {
    mldServer select $ChasId $Card $Port
    mldServer getHost host1
    mldHost getGroupRange group1
    if { $Source != 0 } {
        mldSourceRange config -sourceIpFrom $Source
    }
    if { $Count != -1 } {
        mldSourceRange config -count $Count
    }
    if [mldGroupRange addSourceRange source$Number] {
        logMsg "Error in setting source range"
    }
    if [mldHost setGroupRange group1] {
        logMsg "Error setting groupRange group1"
    }
    mldServer write
}
proc DeleteMldSourcelist { ChasId Card Port Number } {
    mldServer select $ChasId $Card $Port
    mldServer getHost host1
    mldHost getGroupRange group1
    mldGroupRange delSourceRange source$Number
    if [mldHost setGroupRange group1] {
        logMsg "Error setting groupRange group1"
    }
    mldServer write
}    


proc StartIxiaRipng { portlist } {    
    if [ixStartRipng [list portlist] ] {
    		return -code error
	}
	IdleAfter 1000
}
proc StopIxiaRipng { portlist } {    
    if [ixStopRipng [list portlist] ] {
    		return -code error
	}
	IdleAfter 1000
}
proc StartIxiaOspf { portlist } {
    if [ixStartOspf [list portlist] ] {
    		return -code error
	}
	IdleAfter 1000
}

proc StopIxiaOspf { portlist } {
    if [ixStopOspf [list portlist] ] {
    		return -code error
	}
	IdleAfter 1000
}



proc StartIxiaRip { portlist } {
    if [ixStartRip [list portlist] ] {
    		return -code error
	}
	IdleAfter 1000
}


proc StopIxiaRip { portlist } {
    if [ixStopRip [list portlist] ] {
    		return -code error
	}
	IdleAfter 1000
}
proc StartIxiaBGP { portlist } {
    if [ixStartBGP4 [list portlist] ] {
    		return -code error
	}
	IdleAfter 1000
}


proc StopIxiaBGP { portlist } {
    if [ixStopBGP4 [list portlist] ] {
    		return -code error
	}
	IdleAfter 1000
}

proc StartIxiaMld { portlist } {
    if [ixStartMld [list portlist] ] {
    		return -code error
	}
	IdleAfter 1000
}


proc StopIxiaMld { portlist } {
    if [ixStopMld [list portlist] ] {
    		return -code error
	}
	#IdleAfter 1000
}

proc SetIxiaPorts {chas txCard txPort rxCard rxPort } {
	# Reset Ports for Factory Defaults Stream Mode / Capture
	port setFactoryDefaults $chas $txCard $txPort
	port setFactoryDefaults $chas $rxCard $rxPort
	port setDefault
	port config -autonegotiate true
    port config -advertise1000FullDuplex true
    port config -advertise100FullDuplex true
    port config -advertise10FullDuplex true
	port set $chas $txCard $txPort
	port set $chas $rxCard $rxPort
}


proc SetIxiaFactoryDefault { Host args } {
	ixInitialize $Host
	set ChasId [ixGetChassisID $Host]
	set portnum [ expr { [ llength $args ] / 2 } ]
	for {set i 0} {$i < $portnum} {incr i} {
		set Card [ lindex $args [ expr {$i * 2} ] ]
		set Port [ lindex $args [ expr {$i * 2 + 1} ] ]
		#所用ixia端口恢复出厂配置
		#puts "$ChasId $card $port"
		set portlist [list [list $ChasId $Card $Port]]	
		port setModeDefaults $ChasId $Card $Port
		ixWritePortsToHardware portlist
		ixClearStats portlist
	}
	IdleAfter 15000		
}
proc SetIxiaPortDuplex { args } {
	array set arrArgs $args 	
  	foreach {para value} [array get arrArgs] {
		#puts "para=$para"
		#puts "value =$value"  	
		switch -exact -- $para {
		    Host {
		    	set Host $value
		    }
		    Card {
		   		set Card $value
		   	}
		   	Port { 
		   		set Port $value
		   	}
		   	RateMode {
		   		set RateMode $value
		   	}
			default {
		   		puts "Wrong para name:$para "
		   		return -1	
		   	}
		}		
	}
	ixInitialize $Host
	set ChasId [ixGetChassisID $Host]
	port setDefault	
	switch -exact -- $RateMode {
	    auto { 
	    	port config -autonegotiate true
	    	port config -advertise1000FullDuplex true
			port config -advertise100FullDuplex true
			port config -advertise10FullDuplex true
	    }
   		10half {
   			port config -autonegotiate false
			port config -duplex half
			port config -speed 10
   		}
   		10full {
   			port config -autonegotiate false
			port config -duplex full
			port config -speed 10
   		}
   		100half {
   			port config -autonegotiate false
			port config -duplex half
			port config -speed 100
   		}
   		100full {
   			port config -autonegotiate false
			port config -duplex full
			port config -speed 100
   		}
   		1ghalf {
   			port config -autonegotiate auto
   		}
   		1gfull {
   			port config -autonegotiate auto
   		}
   		default {
   			port config -autonegotiate true
 
   		}
	}
	port set $ChasId $Card $Port
	set portlist [list [list $ChasId $Card $Port]] 
	ixWritePortsToHardware portlist
	IdleAfter 5000
}

#used in SetIxiaStream-icmpV6-xxxx
#FormatHexIpv6 2000::1
#20 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01
proc FormatHexIpv6 { ipv6 } {
	set result ""
	foreach item [split [FormatIpv6 $ipv6] :] {
		lappend result [FormatHex $item]
	}
	return [join $result " "]
}

#add in ipv6acl
#FormatIpv6 2000::1
#2000:0000:0000:0000:0000:0000:0000:0001
proc FormatIpv6 { ipv6 } {
	if { [string range $ipv6 0 1] == "::" } {
		set ipv6 [string replace $ipv6 0 1 "0::"]
	}
	if { [string range $ipv6 end-1 end] == "::" } {
		append ipv6 0
	}
	#puts $ipv6
    set ipv6length [ string length $ipv6 ]
    set count 0
    for {set i 0} {$i < $ipv6length} {incr i} {
        set tempchar [ string index $ipv6 $i ]
        if { $tempchar == ":" } {
            incr count
        }
    }
    #puts "count =$count"
    set flag [ string first "::" $ipv6]
    if { $flag == -1 } {
        set result [ Format4bit $ipv6 ]
    } else {
        set bitnum [ expr {7 - $count + 1} ]
        set ipv6temp [ string range $ipv6 0 [expr $flag - 1] ]
        for {set j 0} {$j < $bitnum} {incr j} {
            append ipv6temp ":" "0"
        }
     #   puts "ipv6temp =$ipv6temp"
        set tempipv6 [ string range $ipv6 [expr $flag + 1] end]
        append ipv6temp $tempipv6
      #  puts "ipv6temp =$ipv6temp"
        set result [ Format4bit $ipv6temp ]
        
    }
    return $result 
}

proc Format4bit { ipv6 } {
	#puts "ipv6=$ipv6"
    set templist [ split $ipv6 ":" ]
    set length [ llength $templist ]
    set result ""
    for {set i 0} {$i < $length} {incr i} {
        set tempipv6 [ lindex $templist $i ]
        #puts "i=$i"
				#puts "temp=$tempipv6"
        set tempipv6 [ format %04x 0x0$tempipv6 ]
				set n [expr $length -1]
        if { $i == $n } {
            append result $tempipv6
        } else {
            append result $tempipv6 ":"
        }
    }
    return $result
}
proc CheckDstIpv6InData { dstipv6 data } {

    set vlanflag [string range $data 36 40]
    if  { $vlanflag == "81 00" } {
        set data [string range $data 126 173]
    } else {
        set data [string range $data 114 161]
    }
    regsub -all " " $data "" data
    set n1 [string range $data 0 3]
    set n2 [string range $data 4 7]
    set n3 [string range $data 8 11]
    set n4 [string range $data 12 15]
    set n5 [string range $data 16 19]
    set n6 [string range $data 20 23]
    set n7 [string range $data 24 27]
    set n8 [string range $data 28 31]

    set spring $n1
    append spring ":" "$n2" ":" "$n3" ":" "$n4" ":" "$n5" ":" "$n6" ":" "$n7" ":" "$n8"
    #puts "desipv6 ==$dstipv6"
    #puts "spring == $spring"

    set dstipv6 [ FormatIpv6 $dstipv6 ]
    set dstipv6 [string toupper $dstipv6 0 end]
    #puts "dstipv6 == $dstipv6"
    if { $dstipv6 == $spring } {
        return 1
    } else {
        return 0
    }
}
proc CheckSrcIpv6InData { srcipv6 data } {

    set vlanflag [string range $data 36 40]
    if  { $vlanflag == "81 00" } {
        set data [string range $data 78 125]
    } else {
        set data [string range $data 66 113]
    }
    regsub -all " " $data "" data
    set n1 [string range $data 0 3]
    set n2 [string range $data 4 7]
    set n3 [string range $data 8 11]
    set n4 [string range $data 12 15]
    set n5 [string range $data 16 19]
    set n6 [string range $data 20 23]
    set n7 [string range $data 24 27]
    set n8 [string range $data 28 31]

    set spring $n1
    append spring ":" "$n2" ":" "$n3" ":" "$n4" ":" "$n5" ":" "$n6" ":" "$n7" ":" "$n8"
    #puts "srcipv6 ==$srcipv6"
    #puts "spring == $spring"
    #puts "data == $data"
    set srcipv6 [ FormatIpv6 $srcipv6 ]
    set srcipv6 [string toupper $srcipv6 0 end]
    #puts "srcipv6 == $srcipv6"
    if { $srcipv6 == $spring } {
    	#puts "ok"
        return 1
    } else {
        return 0
    }
}

proc SetIxiaFilter { args } {
    set Host 100.1.1.222
	set Card 8
	set Port 1
	set TriggerFlag true
	set TriggerDA anyAddr  ;#anyAddr/addr1/notAddr1/addr2/notAddr2
	set TriggerSA anyAddr
	set TriggerPattern anyPattern ;#anyPattern/pattern1/notPattern1/pattern2/notPattern2
	set TriggerError errAnyFrame
	set TriggerFrameSizeFlag false
	set TriggerFrameSizeFrom 64
	set TriggerFrameSizeTo 1518
	
	set FilterFlag true
	set FilterDA anyAddr
	set FilterSA anyAddr
	set FilterPattern anyPattern
	set FilterError errAnyFrame
	set FilterFrameSizeFlag false
	set FilterFrameSizeFrom 64
	set FilterFrameSizeTo 1518
	
	set UserDefinedStat1Flag false
	set UserDefinedStat1DA anyAddr
	set UserDefinedStat1SA anyAddr
	set UserDefinedStat1Pattern anyPattern
	set UserDefinedStat1Error errAnyFrame
	set UserDefinedStat1FrameSizeFlag false
	set UserDefinedStat1FrameSizeFrom 64
	set UserDefinedStat1FrameSizeTo 1518
	
	set UserDefinedStat2Flag false
	set UserDefinedStat2DA anyAddr
	set UserDefinedStat2SA anyAddr
	set UserDefinedStat2Pattern anyPattern
	set UserDefinedStat2Error errAnyFrame
	set UserDefinedStat2FrameSizeFlag false
	set UserDefinedStat2FrameSizeFrom 64
	set UserDefinedStat2FrameSizeTo 1518
	
	set PalletteFlag false
	set PalletteDA1 00-00-00-00-00-00
	set PalletteDAMask1 00-00-00-00-00-00
	set PalletteSA1 00-00-00-00-00-00
	set PalletteSAMask1 00-00-00-00-00-00
	set PalletteDA2 00-00-00-00-00-00
	set PalletteDAMask2 00-00-00-00-00-00
	set PalletteSA2 00-00-00-00-00-00
	set PalletteSAMask2 00-00-00-00-00-00
	set Pattern1Flag false
	set Pattern1Mode matchUser   ;#matchUser/matchIpSADAEthernetII/matchIpV6SAEthernetII/matchIpV6DAEthernetII
	set PatternOffset1 12
	set Pattern1 DE-ED-EF-FE-AC-CA
	set PatternMask1 00-00-00-00-00-00
	set Pattern2Flag false
	set Pattern2Mode matchUser
	set PatternOffset2 12
	set Pattern2 DE-ED-EF-FE-AC-CA
	set PatternMask2 00-00-00-00-00-00
	
	array set arrArgs $args 	
  	foreach {para value} [array get arrArgs] {
		#puts "para=$para"
		#puts "value =$value"  	
		switch -exact -- $para {
		    Host {
		    	set Host $value
		    }
		    Card {
		   		set Card $value
		   	}
		   	Port { 
		   		set Port $value
		   	}
		   	TriggerFlag {
		   	    set TriggerFlag $value
		   	}
		   	TriggerDA {
		   	    set TriggerDA $value
		   	}
		   	TriggerSA {
		   	    set TriggerSA $value
		   	}
		   	TriggerPattern {
		   	    set TriggerPattern $value
		   	}
		   	TriggerError {
		   	    set TriggerError $value
		   	}
		   	TriggerFrameSizeFlag {
		   	    set TriggerFrameSizeFlag $value
		   	}
		   	TriggerFrameSizeFrom {
		   	    set TriggerFrameSizeFrom $value
		   	}
		   	TriggerFrameSizeTo {
		   	    set TriggerFrameSizeTo $value
		   	}
		   	FilterFlag {
		   	    set FilterFlag $value
		   	}
		   	FilterDA {
		   	    set FilterDA $value
		   	}
		   	FilterSA {
		   	    set FilterSA $value
		   	}
		   	FilterPattern {
		   	    set FilterPattern $value
		   	}
		   	FilterError {
		   	    set FilterError $value
		   	}
		   	FilterFrameSizeFlag {
		   	    set FilterFrameSizeFlag $value
		   	}
		   	FilterFrameSizeFrom {
		   	    set FilterFrameSizeFrom $value
		   	}
		   	FilterFrameSizeTo {
		   	    set FilterFrameSizeTo $value
		   	}
		   	UserDefinedStat1Flag {
		   	    set UserDefinedStat1Flag $value
		   	}
		   	UserDefinedStat1DA {
		   	    set UserDefinedStat1DA $value
		   	}
		   	UserDefinedStat1SA {
		   	    set UserDefinedStat1SA $value
		   	}
		   	UserDefinedStat1Pattern {
		   	    set UserDefinedStat1Pattern $value
		   	}
		   	UserDefinedStat1Error {
		   	    set UserDefinedStat1FrameSizeFlag $value
		   	}
		   	UserDefinedStat1FrameSizeFlag {
		   	    set UserDefinedStat1FrameSizeFlag $value
		   	}
		   	UserDefinedStat1FrameSizeFrom {
		   	    set UserDefinedStat1FrameSizeFrom $value
		   	}
		   	UserDefinedStat1FrameSizeTo {
		   	    set UserDefinedStat1FrameSizeTo $value
		   	}
		   	UserDefinedStat2Flag {
		   	    set UserDefinedStat2Flag $value
		   	}
		   	UserDefinedStat2DA {
		   	    set UserDefinedStat2DA $value
		   	}
		   	UserDefinedStat2SA {
		   	    set UserDefinedStat2SA $value
		   	}
		   	UserDefinedStat2Pattern {
		   	    set UserDefinedStat2Pattern $value
		   	}
		   	UserDefinedStat2Error {
		   	    set UserDefinedStat2FrameSizeFlag $value
		   	}
		   	UserDefinedStat2FrameSizeFlag {
		   	    set UserDefinedStat2FrameSizeFlag $value
		   	}
		   	UserDefinedStat2FrameSizeFrom {
		   	    set UserDefinedStat2FrameSizeFrom $value
		   	}
		   	UserDefinedStat2FrameSizeTo {
		   	    set UserDefinedStat2FrameSizeTo $value
		   	}
		   	PalletteFlag {
		   	    set PalletteFlag $value
		   	}
		   	PalletteDA1 {
		   	    set PalletteDA1 $value
		   	}
		   	PalletteDAMask1 {
		   	    set PalletteDAMask1 $value
		   	}
		   	PalletteSA1 {
		   	    set PalletteSA1 $value
		   	}
		   	PalletteSAMask1 {
		   	    set PalletteSAMask1 $value
		   	}
		   	PalletteDA2 {
		   	    set PalletteDA2 $value
		   	}
		   	PalletteDAMask2 {
		   	    set PalletteDAMask2 $value
		   	}
		   	PalletteSA2 {
		   	    set PalletteSA2 $value
		   	}
		   	PalletteSAMask2 {
		   	    set PalletteSAMask2 $value
		   	}
		   	Pattern1Flag {
		   	    set Pattern1Flag $value
		   	}
		   	Pattern1 {
		   	    set Pattern1 $value
		   	}
		   	Pattern1Mode {
		   	    set Pattern1Mode $value
		   	}
		   	PatternOffset1 {
		   		set PatternOffset1 $value
		   	}
		   	PatternMask1 {
		   	    set PatternMask1 $value
		   	}
		   	Pattern2Flag {
		   	    set Pattern2Flag $value
		   	}
		   	Pattern2 {
		   	    set Pattern2 $value
		   	}
		   	Pattern2Mode {
		   	    set Pattern2Mode $value
		   	}
		   	PatternOffset2 {
		   		set PatternOffset2 $value
		   	}
		   	PatternMask2 {
		   	    set PatternMask2 $value
		   	}
		   	default {
		   		puts "Wrong para name:$para "
		   		return -1	
		   	}
		}  			
	}
	########################set filter#####################################
	#set Version [ package require IxTclHal ]
	ixInitialize $Host
	set Chas [ixGetChassisID $Host]
	set portList [list [list $Chas $Card $Port]]
	set PalletteDA1 [split $PalletteDA1 -]
	set PalletteDAMask1 [split $PalletteDAMask1 -]
	set PalletteSA1 [split $PalletteSA1 -]
	set PalletteSAMask1 [split $PalletteSAMask1 -]
	set PalletteDA2 [split $PalletteDA2 -]
	set PalletteDAMask2 [split $PalletteDAMask2 -]
	set PalletteSA2 [split $PalletteSA2 -]
	set PalletteSAMask2 [split $PalletteSAMask2 -]
	set Pattern1 [split $Pattern1 -]
	set PatternMask1 [split $PatternMask1 -]
	set Pattern2 [split $Pattern2 -]
	set PatternMask2 [split $PatternMask2 -]
	
	#port setFactoryDefaults $Chas $Card $Port
    #port setDefault
    filter setDefault
    if { $TriggerFlag == "true" } {
        filter config -captureTriggerDA $TriggerDA
        filter config -captureTriggerSA $TriggerSA
        filter config -captureTriggerPattern $TriggerPattern
        filter config -captureTriggerError $TriggerError
        if { $TriggerFrameSizeFlag == "true" } {
            filter config -captureTriggerFrameSizeEnable $TriggerFrameSizeFlag
            filter config -captureTriggerFrameSizeFrom $TriggerFrameSizeFrom
            filter config -captureTriggerFrameSizeTo $TriggerFrameSizeTo
        }
        filter config -captureTriggerEnable $TriggerFlag
    }
    if { $FilterFlag == "true" } {
        filter config -captureFilterDA $FilterDA
        filter config -captureFilterSA $FilterSA
        filter config -captureFilterPattern $FilterPattern
        filter config -captureFilterError $FilterError
        if { $FilterFrameSizeFlag == "true" } {
            filter config -captureFilterFrameSizeEnable $FilterFrameSizeFlag
            filter config -captureFilterFrameSizeFrom $FilterFrameSizeFrom
            filter config -captureFilterFrameSizeTo $FilterFrameSizeTo
        }  
        filter config -captureFilterEnable $FilterFlag
    }
    if { $UserDefinedStat1Flag == "true" } {
        filter config -userDefinedStat1Enable $UserDefinedStat1Flag
        filter config -userDefinedStat1DA $UserDefinedStat1DA
        filter config -userDefinedStat1SA $UserDefinedStat1SA
        filter config -userDefinedStat1Pattern $UserDefinedStat1Pattern
        filter config -userDefinedStat1Error $UserDefinedStat1Error
        if { $UserDefinedStat1FrameSizeFlag == "true" } {
            filter config -userDefinedStat1FrameSizeEnable $UserDefinedStat1FrameSizeFlag
            filter config -userDefinedStat1FrameSizeFrom $UserDefiendStat1FrameSizeFrom
            filter config -userDefinedStat1FrameSizeTo $UserDefiendStat1FrameSizeTo
        }
    }
    if { $UserDefinedStat2Flag == "true" } {
        filter config -userDefinedStat2Enable $UserDefinedStat2Flag
        filter config -userDefinedStat2DA $UserDefinedStat2DA
        filter config -userDefinedStat2SA $UserDefinedStat2SA
        filter config -userDefinedStat2Pattern $UserDefinedStat2Pattern
        filter config -userDefinedStat2Error $UserDefinedStat2Error
        if { $UserDefinedStat2FrameSizeFlag == "true" } {
            filter config -userDefinedStat2FrameSizeEnable $UserDefinedStat2FrameSizeFlag
            filter config -userDefinedStat2FrameSizeFrom $UserDefiendStat2FrameSizeFrom
            filter config -userDefinedStat2FrameSizeTo $UserDefiendStat2FrameSizeTo
        }
    }
    filter set $Chas $Card $Port
    filterPallette setDefault
    if { $PalletteFlag == "true" } {        
        filterPallette config -DA1 $PalletteDA1
        filterPallette config -DAMask1 $PalletteDAMask1
        filterPallette config -SA1 $PalletteSA1
        filterPallette config -SAMask1 $PalletteSAMask1
        filterPallette config -DA2 $PalletteDA2
        filterPallette config -DAMask2 $PalletteDAMask2
        filterPallette config -SA2 $PalletteSA2
        filterPallette config -SAMask2 $PalletteSAMask2
        if { $Pattern1Flag == "true" } {
            filterPallette config -matchType1 $Pattern1Mode
            filterPallette config -patternOffset1 $PatternOffset1
            filterPallette config -pattern1 $Pattern1
            filterPallette config -patternMask1 $PatternMask1
        }
        if { $Pattern2Flag == "true" } {
            filterPallette config -matchType2 $Pattern2Mode
            filterPallette config -patternOffset2 $PatternOffset2
            filterPallette config -pattern2 $Pattern2
            filterPallette config -patternMask2 $PatternMask2
        }
    }
    filterPallette set $Chas $Card $Port
    port set $Chas $Card $Port
	#write to hardware
	ixWriteConfigToHardware portList
    #ixWritePortsToHardware portList
	IdleAfter 5000
}
	
	
proc SetQosCapture { args } {
    set Host 100.1.1.222
	set Card 8
	set Port 1
	array set arrArgs $args 	
  	foreach {para value} [array get arrArgs] {
		#puts "para=$para"
		#puts "value =$value"  	
		switch -exact -- $para {
		    Host {
		    	set Host $value
		    }
		    Card {
		        set Card $value
		    }
		    Port {
		        set Port $value
		    }
		    default {
		   		puts "Wrong para name:$para "
		   		return -1	
		   	}
		}  			
	}
	########################set ixia#####################################
	ixInitialize $Host
	set Chas [ixGetChassisID $Host]
	set portList [list [list $Chas $Card $Port]]
	port setDefault
	stat setDefault
	stat config -mode statQos
	stat set $Chas $Card $Port
	qos setDefault
	qos setup vlan
	qos set $Chas $Card $Port
	protocol setDefault
	protocol config -ethernetType ethernetII
	port set $Chas $Card $Port
    ixWritePortsToHardware portList
	IdleAfter 5000
}

proc GetQosValue { Chas Card Port } {
    stat get allStats $Chas $Card $Port
    for {set i 0} {$i <= 7} {incr i} {
        set res$i [stat cget -qualityOfService$i]
    }
    set qoslist [list $res0 $res1 $res2 $res3 $res4 $res5 $res6 $res7]
    return $qoslist
} 

proc GetTrafficClass {host card port {vlanflag 0}} {
    package require IxTclHal
	# Connect to chassis and get chassis ID
	set host $host
	ixInitialize $host
	set chas [ixGetChassisID $host]
	# with port 1 looped to port 2
	set card $card
	set port $port
	set rxPortList [list [list $chas $card $port]]
	#set offset of dscp
	if {$vlanflag == 0} {
		set index1 43
		set index2 45
	} else {
		set index1 55
		set index2 57
	}
	ixClearStats rxPortList
	ixStartCapture rxPortList
	capture get $chas $card $port
	set numFrames [capture cget -nPackets]
	ixPuts "$numFrames frames captured"
	if {$numFrames == 0} {
		return -1
	}
	captureBuffer get $chas $card $port 2 2
	
	# Note that the frame number starts at 1
	captureBuffer getframe 1
	# Get the actual frame data
	set data [captureBuffer cget -frame]
	#puts $data
	# We’ll only look at the dscp
	set data [string range $data $index1 $index2]
	#puts $data
	regsub -all {\s} $data "" data
	set trafficclass [format %i 0x0$data ]		
	ixPuts "TrafficClass = $trafficclass"
	return $trafficclass
}
   
   
proc CheckIfHaveStream { chas card port args } {
    
    array set arrArgs $args 	
    #set counter 0   ;#内部使用的计数器
    # Get the number of frames captured
	capture get $chas $card $port
	set numFrames [capture cget -nPackets]
	#PrintRes Print "\n$numFrames frames captured"

	# Only look at the first 9 frames
	#if {$numFrames > 10} {
	#	set numFrames 10
	#} else {
	#    return 0        ;#表明出错
	#}
	
	captureBuffer get $chas $card $port 1 $numFrames
    for {set i 1} {$i <= $numFrames} {incr i} {
        # Note that the frame number starts at 1
        captureBuffer getframe $i
        # Get the actual frame data
        set data [captureBuffer cget -frame]
#        if {$i == 1 || $i == 2} {
#        	puts "$data"
#        }
		if { $data == "" } {
			continue
		}
        set ret 1
        
        #SrcMac
        if {[info exist arrArgs(SrcMac)]} {
            set ret [ expr $ret * [ CheckSrcMacInData $arrArgs(SrcMac) $data ] ]
        }
        
        #DstMac
        if {[info exist arrArgs(DstMac)]} {
            set ret [ expr $ret * [ CheckDstMacInData $arrArgs(DstMac) $data ] ]
        }
        
        #SrcIp
        if {[info exist arrArgs(SrcIp)]} {
            set ret [ expr $ret * [ CheckSrcIpInData $arrArgs(SrcIp) $data] ]
        }
        
        #DstIp
        if {[info exist arrArgs(DstIp)]} {
            set ret [ expr $ret * [ CheckDstIpInData $arrArgs(DstIp) $data] ]
        }
        #SrcIpv6
        if {[info exist arrArgs(SrcIpv6)]} {
            set ret [ expr $ret * [ CheckSrcIpv6InData $arrArgs(SrcIpv6) $data] ]
            #puts "ret=$ret"
        }
        
        #DstIpv6
        if {[info exist arrArgs(DstIpv6)]} {
            set ret [ expr $ret * [ CheckDstIpv6InData $arrArgs(DstIpv6) $data] ]
            #puts "dstipv6ret=$ret"
        }    
        #VlanTag
        if {[info exist arrArgs(VlanTag)]} {
            set ret [ expr $ret * [ CheckVlanTagInData $arrArgs(VlanTag) $data ] ]
        }
        
        #cos
        if {[info exist arrArgs(Cos)]} {
             set ret [expr $ret * [ CheckCosInData $arrArgs(Cos) $data] ]
        }
             
#        if { $ret != 0 } {
#            incr counter
#        } else {
#            #PrintRes Print "the $i frame is : $data"
#        }
        if { $ret != 0 } {
            return 1
        }
            
    }    
#    return $counter
}

proc EnableStream { chas card port num } {
    stream config -enable true
    stream set $chas $card $port $num
    stream write $chas $card $port $num
}

proc DisableStream { chas card port num } {
    stream config -enable false 
    stream set $chas $card $port $num
    stream write $chas $card $port $num
}

#SetIxiaAsDhcpClient Host 172.16.1.249 Card 4 Port 1 ClientId "" RenewTimer 0 ServerId 10.1.1.1 VendorId "" DhcpV4RequestRate 0 MacAddress "00 00 00 00 00 01"
#SetIxiaAsDhcpClient Host 172.16.1.249 Card 4 Port 1 DhcpV4RequestRate 0 \
#                     DhcpV4Record {{ClientId "" RenewTimer 0 ServerId 10.1.1.1 VendorId "" MacAddress "00 00 00 00 00 01"} \
#                                   {ClientId "" RenewTimer 0 ServerId 10.1.1.1 VendorId "" MacAddress "00 00 00 00 00 02"}}
#SetIxiaAsDhcpClient Host 172.16.1.249 Card 4 Port 1 DhcpV4RequestRate 0 \
#                    MoreDhcpV4Record 100 MacAddress 00-00-00-00-00-01 EnableDhcp true
proc SetIxiaAsDhcpClient { args } {
    set Host 172.16.1.251
    set Card 4
    set Port 1
    set ClientId ""
    set RenewTimer 0
    set ServerId 0.0.0.0
    set VendorId ""
    set DhcpV4RequestRate 0
    set EnableDhcp true
    set MacAddress {00 00 00 00 00 01}
    
	array set arrArgs $args 	
  	foreach {para value} [array get arrArgs] {
		#puts "para=$para"
		#puts "value =$value"  	
		switch -exact -- $para {
		    Host {
		    	set Host $value
		    }
		    Card {
		   		set Card $value
		   	}
		   	Port { 
		   		set Port $value
		   	}
		   	ClientId {
		   	    set ClientId $value
		   	}
		   	MacAddress {
		   	    set MacAddress $value
		   	}
		   	RenewTimer {
		   	    set RenewTimer $value
		   	}
		   	ServerId {
		   	    set ServerId $value
		   	}
		   	VendorId {
		   	    set VendorId $value
		   	}
		   	DhcpV4RequestRate {
		   	    set DhcpV4RequestRate $value
		   	}
		   	EnableDhcp {
		   	    set EnableDhcp $value
		   	}
		   	DhcpV4Record {
		   		set DhcpV4Record $value
		   	}
		   	MoreDhcpV4Record {
		   		set MoreDhcpV4Record $value
		   	}
			default {
		   		puts "Wrong para name:$para "
		   		return -1	
		   	}
		}		
	}
	ixInitialize $Host
	set ChasId [ixGetChassisID $Host]
	set portlist [list [list $ChasId $Card $Port]]
	set InterfaceDescription "[format %02d $Card]:[format %02d $Port] - 1"

	interfaceTable select $ChasId $Card $Port
	interfaceTable setDefault	 
    interfaceTable config -dhcpV4RequestRate $DhcpV4RequestRate
    interfaceTable set
    interfaceTable clearAllInterfaces
    interfaceEntry clearAllItems addressTypeIpV4
    if [info exists DhcpV4Record] {
    	for {set i 0} {$i < [llength $DhcpV4Record]} {incr i} {
    		interfaceEntry setDefault
			array set DhcpV4 [lindex $DhcpV4Record $i]
			dhcpV4Properties removeAllTlvs     
	    	dhcpV4Properties setDefault   
	    	if [info exists DhcpV4(ClientId)] {
	    		dhcpV4Properties config -clientId $DhcpV4(ClientId)
	    	} else {
	    		dhcpV4Properties config -clientId ""
	    	}
	    	if [info exists DhcpV4(ServerId)] {
	    		dhcpV4Properties config -serverId $DhcpV4(ServerId)
	    	} else {
	    		dhcpV4Properties config -serverId 0.0.0.0
	    	}
	    	if [info exists DhcpV4(VendorId)] {
	    		dhcpV4Properties config -vendorId $DhcpV4(VendorId)
	    	} else {
	    		dhcpV4Properties config -vendorId ""
	    	}
	    	if [info exists DhcpV4(RenewTimer)] {
	    		dhcpV4Properties config -renewTimer $DhcpV4(RenewTimer)
	    	} else {
	    		dhcpV4Properties config -renewTimer 0
	    	}
	    	interfaceEntry config -enable true
	    	if [info exists DhcpV4(MacAddress)] {
	    		regsub -all {\-} $DhcpV4(MacAddress) " "  MacAddress
	    		interfaceEntry config -macAddress $MacAddress
	    	} else {
	    		interfaceEntry config -macAddress "00 00 00 00 00 01"
	    	}
	    	if [info exists DhcpV4(EnableDhcp)] {
	    		interfaceEntry config -enableDhcp $DhcpV4(EnableDhcp)
	    	} else {
	    		interfaceEntry config -enableDhcp true
	    	}
	    	interfaceEntry config -description $InterfaceDescription
	    	set InterfaceDescription [IncrInterfaceDescription $InterfaceDescription]  
	    	interfaceTable addInterface interfaceTypeConnected
    	}
    }
    if [info exists MoreDhcpV4Record] {
    	set num $MoreDhcpV4Record
    	for {set i 0} {$i < $num} {incr i} {
    		interfaceEntry setDefault
			dhcpV4Properties removeAllTlvs     
	    	dhcpV4Properties setDefault   
			dhcpV4Properties config -clientId ""
	    	dhcpV4Properties config -serverId 0.0.0.0
	    	dhcpV4Properties config -vendorId ""
	    	dhcpV4Properties config -renewTimer 0
	    	regsub -all {\-} $MacAddress " "  MacAddresstemp
	    	interfaceEntry config -macAddress $MacAddresstemp
	    	interfaceEntry config -enableDhcp $EnableDhcp
	    	interfaceEntry config -description $InterfaceDescription
	    	interfaceEntry config -enable true
	    	set InterfaceDescription [IncrInterfaceDescription $InterfaceDescription]  
	    	set MacAddress [IncrMacStep $MacAddress]
	    	interfaceTable addInterface interfaceTypeConnected
    	}
    } else {
    	interfaceEntry setDefault
	    dhcpV4Properties removeAllTlvs     
	    dhcpV4Properties setDefault        
	    dhcpV4Properties config -clientId $ClientId
	    dhcpV4Properties config -serverId $ServerId
	    dhcpV4Properties config -vendorId $VendorId
	    dhcpV4Properties config -renewTimer $RenewTimer
	    interfaceEntry config -enable true
	    regsub -all {\-} $MacAddress " "  MacAddress
	    interfaceEntry config -macAddress $MacAddress
	    interfaceEntry config -enableDhcp $EnableDhcp
	    interfaceEntry config -description $InterfaceDescription
	    interfaceTable addInterface interfaceTypeConnected
	}
#changed by wangleiaq
#增加了对EnablePING for IPv4及enableArp的控制字段
	protocolServer get $ChasId $Card $Port
	protocolServer config -enableArpResponse true
#对应Ixia里面Protocal Management里面的EnablePING for IPv4,ture为打勾，FALSE为取消打勾	
	protocolServer config -enablePingResponse true
	set res [protocolServer set $ChasId $Card $Port]
#Tell the hardware about it,write port configuration to hardware
	ixWritePortsToHardware portlist
}

#GetDhcpInfo $host $card $port MoreIpAddress moreipAddress
#GetDhcpInfo $host $card $port IpAddress ipAddress
#GetDhcpInfo $host $card $port PrefixLength prefixLength
#GetDhcpInfo $host $card $port GatewayIpAddress gatewayIpAddress
#GetDhcpInfo $host $card $port LeaseDuration leaseDuration
#GetDhcpInfo $host $card $port IpAddress ipAddress PrefixLength prefixLength GatewayIpAddress gatewayIpAddress LeaseDuration leaseDuration
proc GetDhcpInfo { Host Card Port args } {
	if {[lsearch $args MoreIpAddress] != -1} {
		upvar 1 [lindex $args [expr [lsearch $args MoreIpAddress] + 1]] moreipAddress
	}
	if {[lsearch $args IpAddress] != -1} {
        upvar 1 [lindex $args [expr [lsearch $args IpAddress] + 1]] ipAddress
    }
    if {[lsearch $args PrefixLength] != -1} {
        upvar 1 [lindex $args [expr [lsearch $args PrefixLength] + 1]] prefixLength
    }
    if {[lsearch $args GatewayIpAddress] != -1} {
        upvar 1 [lindex $args [expr [lsearch $args GatewayIpAddress] + 1]] gatewayIpAddress
    }
    if {[lsearch $args LeaseDuration] != -1} {
        upvar 1 [lindex $args [expr [lsearch $args LeaseDuration] + 1]] leaseDuration
    }
    ixInitialize $Host
    set ChasId [ixGetChassisID $Host]
    set InterfaceDescription "[format %02d $Card]:[format %02d $Port] - 1"
    # Enable DHCP statistics
    stat config -enableDhcpStats true
    stat set $ChasId $Card $Port
    stat write $ChasId $Card $Port
    # Need to wait until the interface has been defined and
    for {set i 0} {$i < 5} {incr i 1} {
        after 200
        stat get allStats $ChasId $Card $Port
        if {1 == [stat cget -dhcpV4EnabledInterfaces]} {
            break
        }
    }
    # Need to wait until the DHCP server has assigned an address
    interfaceTable requestDiscoveredTable
    for {set i 0} {$i < 5} {incr i 1} {
        after 200
        stat get allStats $ChasId $Card $Port
        if {1 == [stat cget -dhcpV4AddressesLearned]} {
            break
        }
    }
    if [interfaceTable select $ChasId $Card $Port] {
        logMsg "Error selecting $ChasId $Card $Port"
        set retCode "FAIL"
    }
    if [interfaceTable getFirstInterface interfaceTypeConnected] {
        logMsg "Error getFirstInterface $ChasId $Card $Port"
        set retCode "FAIL"
    }
    # Ask for the discovered DHCP information
    if [interfaceTable requestDiscoveredTable] {
        logMsg "Error requestDiscoveredTable $ChasId $Card $Port"
        set retCode "FAIL"
    }
    # And fetch it
    #set InterfaceDescription "04:03 - 1"
    #puts $InterfaceDescription
    after 1000
    if {[lsearch $args MoreIpAddress] != -1} {
    	set counter 0
    	IdleAfter 120000
    	while { [interfaceTable getDhcpV4DiscoveredInfo $InterfaceDescription] == 0 } {
	        # Pull out the assigned IP address, mask, gateway and timer
	        lappend moreipAddress [dhcpV4DiscoveredInfo cget -ipAddress]
	        set InterfaceDescription [IncrInterfaceDescription $InterfaceDescription] 
	        incr counter
	    }
	    if { $counter == 0 } {
	    	PrintRes Print "The ipaddress doesn't exist!"
	        return $counter
	    } else {
	    	PrintRes Print "client get $counter dhcp ip : [join $moreipAddress {, }]."
	    	return $counter
	    }
    } else {
	    if ![interfaceTable getDhcpV4DiscoveredInfo $InterfaceDescription] {
	        # Pull out the assigned IP address, mask, gateway and timer
	        set ipAddress [dhcpV4DiscoveredInfo cget -ipAddress]
	        set prefixLength [dhcpV4DiscoveredInfo cget -prefixLength]
	        set gatewayIpAddress [dhcpV4DiscoveredInfo cget -gatewayIpAddress]
	        set leaseDuration [dhcpV4DiscoveredInfo cget -leaseDuration]
	        PrintRes Print "IpAddress is $ipAddress, PrefixLength is $prefixLength, GatewayIpAddress is $gatewayIpAddress, LeaseDuration is $leaseDuration."
	        return 1
	    } else {
	        PrintRes Print "The ipaddress doesn't exist!"
	        return 0
	    }
	}
}

#SetIxiaAsDhcpv6Client Host 172.16.1.249 Card 4 Port 1 IAId 1 RenewTimer 0 IAType 1 DhcpV6RequestRate 0 MacAddress "00 00 00 00 00 01"
#SetIxiaAsDhcpv6Client Host 172.16.1.249 Card 4 Port 1 DhcpV6RequestRate 0 \
#                     DhcpV6Record {{IAId "" RenewTimer 0 IAType 1 MacAddress "00 00 00 00 00 01"} \
#                                   {IAId "" RenewTimer 0 IAType 1 MacAddress "00 00 00 00 00 02"}}
#SetIxiaAsDhcpv6Client Host 172.16.1.249 Card 4 Port 1 DhcpV6RequestRate 0 \
#                    MoreDhcpV6Record 100 MacAddress 00-00-00-00-00-01 EnableDhcpv6 true
proc SetIxiaAsDhcpv6Client { args } {
    set Host 172.16.1.251
    set Card 4
    set Port 1
    set IAId 100
    set IAType 1
    set RenewTimer 0
    set DhcpV6RequestRate ""
    set EnableDhcpv6 true
    set MacAddress {00 00 00 00 00 01}
    
	array set arrArgs $args 	
  	foreach {para value} [array get arrArgs] {
		#puts "para=$para"
		#puts "value =$value"  	
		switch -exact -- $para {
		    Host {
		    	set Host $value
		    }
		    Card {
		   		set Card $value
		   	}
		   	Port { 
		   		set Port $value
		   	}
		   	IAId {
		   	    set IAId $value
		   	}
		   	MacAddress {
		   	    set MacAddress $value
		   	}
		   	RenewTimer {
		   	    set RenewTimer $value
		   	}
		   	IAType {
		   	    set IAType $value
		   	}
		   	DhcpV6RequestRate {
		   	    set DhcpV6RequestRate $value
		   	}
		   	EnableDhcpv6 {
		   	    set EnableDhcpv6 $value
		   	}
		   	DhcpV6Record {
		   		set DhcpV4Record $value
		   	}
		   	MoreDhcpV6Record {
		   		set MoreDhcpV6Record $value
		   	}
			default {
		   		puts "Wrong para name:$para "
		   		return -1	
		   	}
		}		
	}
	ixInitialize $Host
	set ChasId [ixGetChassisID $Host]
	set portlist [list [list $ChasId $Card $Port]]
	set InterfaceDescription "[format %02d $Card]:[format %02d $Port] - 1"

	interfaceTable select $ChasId $Card $Port
	interfaceTable setDefault	 
    interfaceTable config -dhcpV6RequestRate $DhcpV6RequestRate
    interfaceTable set
    interfaceTable clearAllInterfaces
    interfaceEntry clearAllItems addressTypeIpV6
    if [info exists DhcpV6Record] {
    	for {set i 0} {$i < [llength $DhcpV6Record]} {incr i} {
    		interfaceEntry setDefault
			array set DhcpV6 [lindex $DhcpV6Record $i]
			dhcpV6Properties removeAllTlvs     
	    	dhcpV6Properties setDefault   
	    	if [info exists DhcpV6(IAId)] {
	    		dhcpV6Properties config -iaId $DhcpV6(IAId)
	    	} else {
	    		dhcpV6Properties config -iaId ""
	    	}
	    	if [info exists DhcpV6(IAType)] {
	    		dhcpV6Properties config -iaType $DhcpV6(IAType)
	    	} else {
	    		dhcpV6Properties config -iaType 1
	    	}
	    	if [info exists DhcpV6(RenewTimer)] {
	    		dhcpV6Properties config -renewTimer $DhcpV6(RenewTimer)
	    	} else {
	    		dhcpV6Properties config -renewTimer 0
	    	}
	    	interfaceEntry config -enable true
	    	if [info exists DhcpV6(MacAddress)] {
	    		regsub -all {\-} $DhcpV6(MacAddress) " "  MacAddress
	    		interfaceEntry config -macAddress $MacAddress
	    	} else {
	    		interfaceEntry config -macAddress "00 00 00 00 00 01"
	    	}
	    	if [info exists DhcpV6(EnableDhcpv6)] {
	    		interfaceEntry config -enableDhcpV6 $DhcpV6(EnableDhcpv6)
	    	} else {
	    		interfaceEntry config -enableDhcpV6 true
	    	}
	    	interfaceEntry config -description $InterfaceDescription
	    	set InterfaceDescription [IncrInterfaceDescription $InterfaceDescription]  
	    	interfaceTable addInterface interfaceTypeConnected
    	}
    }
    if [info exists MoreDhcpV6Record] {
    	set num $MoreDhcpV6Record
    	for {set i 0} {$i < $num} {incr i} {
    		interfaceEntry setDefault
			dhcpV6Properties removeAllTlvs     
	    	dhcpV6Properties setDefault   
			dhcpV6Properties config -iaId ""
	    	dhcpV6Properties config -iaType 1
	    	dhcpV6Properties config -renewTimer 0
	    	regsub -all {\-} $MacAddress " "  MacAddresstemp
	    	interfaceEntry config -macAddress $MacAddresstemp
	    	interfaceEntry config -enableDhcpV6 $EnableDhcpv6
	    	interfaceEntry config -description $InterfaceDescription
	    	set InterfaceDescription [IncrInterfaceDescription $InterfaceDescription]  
	    	set MacAddress [IncrMacStep $MacAddress]
	    	interfaceTable addInterface interfaceTypeConnected
    	}
    } else {
    	interfaceEntry setDefault
	    dhcpV6Properties removeAllTlvs     
	    dhcpV6Properties setDefault        
	    dhcpV6Properties config -iaId $IAId
	    dhcpV6Properties config -iaType $IAType
	    dhcpV6Properties config -renewTimer $RenewTimer
	    interfaceEntry config -enable true
	    regsub -all {\-} $MacAddress " "  MacAddress
	    interfaceEntry config -macAddress $MacAddress
	    interfaceEntry config -enableDhcpV6 $EnableDhcpv6
	    interfaceEntry config -description $InterfaceDescription
	    interfaceTable addInterface interfaceTypeConnected
	}
	ixWritePortsToHardware portlist
}


#GetDhcpv6Info $host $card $port MoreIpv6Address moreipv6Address
#GetDhcpv6Info $host $card $port Ipv6Address ipv6Address ;只能判断存在某条ipv6Address
#GetDhcpv6Info $host $card $port IARenewTime iarenewtime
#GetDhcpv6Info $host $card $port IARebindTime iarebindtime
#GetDhcpv6Info $host $card $port Ipv6Address ipv6Address IARenewTime iarenewtime IARebindTime iarebindtime
proc GetDhcpv6Info { Host Card Port args } {
	if {[lsearch MoreIpv6Address $args] != -1} {
		upvar 1 [lindex $args [expr [lsearch $args MoreIpv6Address] + 1]] moreipv6Address
	}
	if {[lsearch Ipv6Address $args] != -1} {
        upvar 1 [lindex $args [expr [lsearch $args Ipv6Address] + 1]] ipv6Address
    }
    if {[lsearch IARenewTime $args] != -1} {
        upvar 1 [lindex $args [expr [lsearch $args IARenewTime] + 1]] iaRenewTime
    }
    if {[lsearch IARebindTime $args] != -1} {
        upvar 1 [lindex $args [expr [lsearch $args IARebindTime] + 1]] iaRebindTime
    }
    ixInitialize $Host
    set ChasId [ixGetChassisID $Host]
    set InterfaceDescription "[format %02d $Card]:[format %02d $Port] - 1"
    # Enable DHCP statistics
    stat config -enableDhcpV6Stats true
    stat set $ChasId $Card $Port
    stat write $ChasId $Card $Port
#    # Need to wait until the interface has been defined and
#    for {set i 0} {$i < 5} {incr i 1} {
#        after 200
#        stat get allStats $ChasId $Card $Port
#        if {1 == [stat cget -dhcpV6EnabledInterfaces]} {
#            break
#        }
#    }
#    # Need to wait until the DHCP server has assigned an address
#    interfaceTable requestDiscoveredTable
#    for {set i 0} {$i < 5} {incr i 1} {
#        after 200
#        stat get allStats $ChasId $Card $Port
#        if {1 == [stat cget -dhcpV4AddressesLearned]} {
#            break
#        }
#    }
    if [interfaceTable select $ChasId $Card $Port] {
        logMsg "Error selecting $ChasId $Card $Port"
        set retCode "FAIL"
    }
    if [interfaceTable getFirstInterface interfaceTypeConnected] {
        logMsg "Error getFirstInterface $ChasId $Card $Port"
        set retCode "FAIL"
    }
    # Ask for the discovered DHCP information
    if [interfaceTable requestDiscoveredTable] {
        logMsg "Error requestDiscoveredTable $ChasId $Card $Port"
        set retCode "FAIL"
    }
    # And fetch it
    #set InterfaceDescription "04:03 - 1"
    #puts $InterfaceDescription
    after 1000
    if {[lsearch MoreIpv6Address $args] != -1} {
    	set counter 0
    	while ![interfaceTable getDhcpV6DiscoveredInfo $InterfaceDescription] {
	        # Pull out the assigned IP address, mask, gateway and timer
	        lappend moreipAddress [dhcpV6DiscoveredInfo cget -discoveredAddressList]
	        set InterfaceDescription [IncrInterfaceDescription $InterfaceDescription] 
	        incr counter
	    }
	    if {[llength $moreipv6Address] == 0 } {
	    	PrintRes Print "The ipv6address doesn't exist!"
	        return $counter
	    } else {
	    	PrintRes Print "client get $counter dhcp ipv6 : $moreipAddress."
	    	return $counter
	    }
    } else {
	    if ![interfaceTable getDhcpV6DiscoveredInfo $InterfaceDescription] {
	        # Pull out the assigned IP address, mask, gateway and timer
	        set ipv6Address [dhcpV6DiscoveredInfo cget -discoveredAddressList]
	        set iaRenewTime [dhcpV6DiscoveredInfo cget -iaRebindTime]
	        set iaRebindTime [dhcpV6DiscoveredInfo cget -iaRenewTime]
	        PrintRes Print "Ipv6AddressList is $ipv6Address, IArenewTime is $iaRenewTime, IARebindTime is $iaRebindTime."
	        return 1
	    } else {
	        PrintRes Print "The ipv6address doesn't exist!"
	        return 0
	    }
	}
}

proc  CheckFilterUserDefinedStat1 { chas card port {num -1}}  {
	ixClearPortStats $chas $card $port
	IdleAfter 10000
	stat get allStats $chas $card $port
	set userDefinedStat1 [stat cget -userDefinedStat1 ]
	PrintRes Print "the userDefinedStat1 received bytes is $userDefinedStat1 in 10sec"
	if { $num == -1 } {
		return $userDefinedStat1
	} elseif { $num == 0 } {
		if { $userDefinedStat1 == 0 } {
			return 1
		} else {
			return 0
		}
	} else {
		append num ".1"
		set num1 [expr  { abs(($userDefinedStat1 - $num) / $userDefinedStat1) } ]
		if { $num1 <= 0.1 } {
		    return 1
		} else {
		    return 0
		}
	}
		
}
proc  CheckFilterUserDefinedStat2 { chas card port {num -1}}  {
	ixClearPortStats $chas $card $port
	IdleAfter 10000
	stat get allStats $chas $card $port
	set userDefinedStat2 [stat cget -userDefinedStat2 ]
	PrintRes Print "the userDefinedStat2 received bytes is $userDefinedStat2 in 10sec"
	if { $num == -1 } {
		return $userDefinedStat2
	} elseif { $num == 0 } {
		if { $userDefinedStat2 == 0 } {
			return 1
		} else {
			return 0
		}
	} else {
		append num ".1"
		set num1 [expr  { abs(($userDefinedStat2 - $num) / $userDefinedStat2) } ]
		if { $num1 <= 0.1 } {
		    return 1
		} else {
		    return 0
		}
	}
}
proc  CheckFilterUserDefinedStat1UserDefinedStat2 { chas card port num }  {
	ixClearPortStats $chas $card $port
	IdleAfter 20000
	stat get allStats $chas $card $port
	set userDefinedStat1 [stat cget -userDefinedStat1 ]
	set userDefinedStat2 [stat cget -userDefinedStat2 ]
	PrintRes Print "the userDefinedStat1 received bytes is $userDefinedStat1 in 10sec"
	PrintRes Print "the userDefinedStat2 received bytes is $userDefinedStat2 in 10sec"
	if { $userDefinedStat2 == 0  } {
		if { $num == 0 } {
			return 1
		} else {
			return 0
		}		
	} 
 	append userDefinedStat2 ".1"
	set num1 [expr  { $userDefinedStat1 / $userDefinedStat2 - $num } ]
  set num2 [expr abs($num1) ]
  if { $num2 <= 0.01 } {
        return 1
    } else {
        return 0
    }
}

#CheckTpidVid $chasId $Card2 $Port2
#CheckTpidVid $chasId $Card2 $Port2 0001 NULL
#CheckTpidVid $chasId $Card2 $Port2 0001 {{8100 10}}
#CheckTpidVid $chasId $Card2 $Port2 Ipv4 {{9100 20} {8100 10}}
#CheckTpidVid $chasId $Card2 $Port2 Ipv6 {{9100 20} {8100 10} {8100 10}}
proc CheckTpidVid { chas card port {ethernettype 0001} {tpidvid NULL} } {
    capture get $chas $card $port
	set numFrames [capture cget -nPackets]
	set checkmark 1
    #   未抓到包返回-1
	if {$numFrames == 0} {
		PrintRes Print "Receive no packet."
		return -1		
	}
	captureBuffer get $chas $card $port 5 5	
	# Note that the frame number starts at 1
	captureBuffer getframe 1
	# Get the actual frame data
	set data [captureBuffer cget -frame]
	if { $tpidvid == "NULL" } {
	    regsub -all " " [string range $data 36 40] {} getethernettype
	    if { [string equal $getethernettype [string toupper $ethernettype 0 end]] } {
	        PrintRes Print "Capture packet have no tpid-vid."
	        return 1
	    } else {
	        regsub -all " " [string range $data 36 46] {} gettpidvid
	        set gettpid [string range $gettpidvid 0 3]
	        set getvid [format %i 0x[string range $gettpidvid 5 7]]
	        PrintRes Print "Capture packet should have no tpid-vid, but have tpid/vid:0x$gettpid/$getvid."
	        return 0
	    }
	} else {
	    set tpidvidnum [llength $tpidvid]
	    for {set i 0} {$i < $tpidvidnum} {incr i} {
	        set tpid [lindex [lindex $tpidvid $i] 0]
	        set vid [lindex [lindex $tpidvid $i] 1]
	        regsub -all " " [string range $data [expr {36 + $i *12}] [expr {46 + $i * 12}]] {} gettpidvid
	        set gettpid [string range $gettpidvid 0 3]
	        set getvid [format %i 0x[string range $gettpidvid 5 7]]
	        if { [string equal $tpid $gettpid] & [string equal $vid $getvid] } {
	            PrintRes Print "Capture packet have [expr $i +1]-layer tpid-vid with tpid/vid:0x$tpid/$vid as should be."
	        } else {
	            PrintRes Print "Capture packet should have [expr $i +1]-layer tpid-vid with tpid/vid:0x$tpid/$vid."
	            PrintRes Print "But real have [expr $i +1]-layer tpid-vid with tpid/vid:0x$gettpid/$getvid."
	            set checkmark 0
	        }
	    }
	    regsub -all " " [string range $data [expr {36 + $tpidvidnum *12}] [expr {40 + $tpidvidnum * 12}]] {} getethernettype
        switch -exact $ethernettype {
            L2 {set ethernettype FFFF}
            Ipv4 {set ethernettype 0800}
            Ipv6 {set ethernettype 86DD}
            default {}
        }
        if { [string equal $getethernettype [string toupper $ethernettype 0 end]] } {
	        PrintRes Print "Capture packet have $tpidvidnum layers tpid-vid."
	    } else {	        
	        regsub -all " " [string range $data [expr {36 + $tpidvidnum *12}] [expr {46 + $tpidvidnum * 12}]] {} gettpidvid
	        set gettpid [string range $gettpidvid 0 3]
	        set getvid [format %i 0x[string range $gettpidvid 5 7]]
	        PrintRes Print "Capture packet have more than $tpidvidnum layers tpid-vid."
	        PrintRes Print "Capture packet [expr $tpidvidnum +1]-layer tpid-vid may be with tpid/vid:0x$gettpid/$getvid."
	        set checkmark 0
	    } 
	    return $checkmark
	}   	
}


##################################################################################
# 
# QinQGetTpid1:获取抓到的包中第一个tag的tpid。
#
# args: 
#     host : IXIA的IP地址
#     card : IXIA的接口
#     port : IXIA的接口
# return:
#     tpid1 : 第一个tag的tpid值
#     -1 :未抓到包
#
# addition:
#     - add by zouleia 2006.8.11
#
# examples:
#     QinQgetTpid1 $host $txcard $txport
#
####################################################################################
#       
proc QinQGetTpid1 {host card port} {
	package require IxTclHal
	# Connect to chassis and get chassis ID
	set host $host
	ixInitialize $host
	set chas [ixGetChassisID $host]
	# with port 1 looped to port 2
	set card $card
	set port $port
	set rxPortList [list [list $chas $card $port]]
	
	#ixClearStats rxPortList
	#ixStartCapture rxPortList
	capture get $chas $card $port
	set numFrames [capture cget -nPackets]
#	ixPuts "$numFrames frames captured"
#   未抓到包返回-1
	if {$numFrames == 0} {
		return -1
	}
	captureBuffer get $chas $card $port 3 3
	
	# Note that the frame number starts at 1
	captureBuffer getframe 1
	# Get the actual frame data
	set data [captureBuffer cget -frame]
	# Get tpid1
	set tpid1 [string range $data 36 40]
	regsub -all " " $tpid1 {} tpid1
	PrintRes Print "Get first tpid : $tpid1"
#	ixPuts "tpid1 = $tpid1"
#	ixPuts $data
	return $tpid1
}



##################################################################################
# 
# QinQGetTpid2:获取抓到的包中第二个tag的tpid。
#
# args: 
#     host : IXIA的IP地址
#     card : IXIA的接口
#     port : IXIA的接口
# return:
#     tpid2 : 第二个tag的tpid值
#     -1 :未抓到包
#
# addition:
#     - add by zouleia 2006.9.11
#
# examples:
#     QinQgetTpid2 $host $txcard $txport
#
####################################################################################
#       
proc QinQGetTpid2 {host card port} {
	package require IxTclHal
	# Connect to chassis and get chassis ID
	set host $host
	ixInitialize $host
	set chas [ixGetChassisID $host]
	# with port 1 looped to port 2
	set card $card
	set port $port
	set rxPortList [list [list $chas $card $port]]
	
	#ixClearStats rxPortList
	#ixStartCapture rxPortList
	capture get $chas $card $port
	set numFrames [capture cget -nPackets]
#	ixPuts "$numFrames frames captured"
#   未抓到包返回-1
	if {$numFrames == 0} {
		return -1
	}
	captureBuffer get $chas $card $port 3 3
	
	# Note that the frame number starts at 1
	captureBuffer getframe 1
	# Get the actual frame data
	set data [captureBuffer cget -frame]
	# Get tpid2
	set tpid2 [string range $data 48 52]	
	regsub -all " " $tpid2 {} tpid2
	PrintRes Print "Get second tpid : $tpid2"
	#ixPuts "tpid2 = $tpid2"
#	ixPuts $data
	return $tpid2
}

##################################################################################
# 
# QinQGetTpid3:获取抓到的包中第三个tag的tpid。
#
# args: 
#     host : IXIA的IP地址
#     card : IXIA的接口
#     port : IXIA的接口
# return:
#     tpid3 : 第三个tag的tpid值
#     -1 :未抓到包
#
# addition:
#     - add by zouleia 2008.9.22
#
# examples:
#     QinQgetTpid3 $host $txcard $txport
#
####################################################################################
#       
proc QinQGetTpid3 {host card port} {
	package require IxTclHal
	# Connect to chassis and get chassis ID
	set host $host
	ixInitialize $host
	set chas [ixGetChassisID $host]
	# with port 1 looped to port 2
	set card $card
	set port $port
	set rxPortList [list [list $chas $card $port]]
	
	#ixClearStats rxPortList
	#ixStartCapture rxPortList
	capture get $chas $card $port
	set numFrames [capture cget -nPackets]
#	ixPuts "$numFrames frames captured"
#   未抓到包返回-1
	if {$numFrames == 0} {
		return -1
	}
	captureBuffer get $chas $card $port 3 3
	
	# Note that the frame number starts at 1
	captureBuffer getframe 1
	# Get the actual frame data
	set data [captureBuffer cget -frame]
	# Get tpid3
	set tpid3 [string range $data 60 64]	
	regsub -all " " $tpid3 {} tpid3
	PrintRes Print "Get third tpid : $tpid3"
	#ixPuts "tpid3 = $tpid3"
	#ixPuts $data
	return $tpid3
}


##################################################################################
# 
# QinQGetTag1:获取抓到的包中的第一个vlantag。
#
# args: 
#     host : IXIA的IP地址
#     card : IXIA的接口
#     port : IXIA的接口
# return:
#     vlantag1 : 第一个vlantag值
#     -1 : 未抓到包
#     -2 :抓到的不是带tag包
#
# addition:
#     - add by zouleia 2006.8.11
#
# examples:
#     QinQGetTag1 $host $txcard $txport
#
####################################################################################
#       
proc QinQGetTag1 {host card port} {
	package require IxTclHal
	# Connect to chassis and get chassis ID
	set host $host
	ixInitialize $host
	set chas [ixGetChassisID $host]
	# with port 1 looped to port 2
	set card $card
	set port $port
	set rxPortList [list [list $chas $card $port]]
	
	#ixClearStats rxPortList
	#ixStartCapture rxPortList
	capture get $chas $card $port
	set numFrames [capture cget -nPackets]
#	ixPuts "$numFrames frames captured"
#   未抓到包返回-1
	if {$numFrames == 0} {
		return -1
	}
	captureBuffer get $chas $card $port 3 3
	
	# Note that the frame number starts at 1
	captureBuffer getframe 1
	# Get the actual frame data
	set data [captureBuffer cget -frame]
	# Get vlantag1
	#set temp [ string range $data 36 40 ]
	set temp [ string range $data 43 46 ]
    regsub -all " " $temp {} temp
    set temp "0x$temp"
    set vlantag1 [ format "%i" $temp ]
    #ixPuts [ string range $data 36 70 ]
#	if { $temp == "81 00" || $temp == "91 00" || $temp == "92 00" } {
#	    #ixPuts "vlantag1 = $vlantag1"\
#	    return $vlantag1
#    } else {
#        return $vlantag1
#    } 
    PrintRes Print "Get first vlan-tag : $vlantag1"
    return $vlantag1
	    
}



##################################################################################
# 
# QinQGetTag2:判断抓到的包是否double tag并获取第二个vlantag。
#
# args: 
#     host : IXIA的IP地址
#     card : IXIA的接口
#     port : IXIA的接口
# return:
#     vlantag2 : 第一个vlantag值
#     -1 :未抓到包
#     -2 :抓到的不是double tag包      
#
# addition:
#     - add by zouleia 2006.8.11
#
# examples:
#     QinQGetTag2 $host $txcard $txport
#
####################################################################################
#       
proc QinQGetTag2 {host card port} {
	package require IxTclHal
	# Connect to chassis and get chassis ID
	set host $host
	ixInitialize $host
	set chas [ixGetChassisID $host]
	# with port 1 looped to port 2
	set card $card
	set port $port
	set rxPortList [list [list $chas $card $port]]
	
	#ixClearStats rxPortList
	#ixStartCapture rxPortList
	capture get $chas $card $port
	set numFrames [capture cget -nPackets]
#	ixPuts "$numFrames frames captured"
#   未抓到包返回-1
	if {$numFrames == 0} {
		return -1
	}
	captureBuffer get $chas $card $port 3 3
	
	# Note that the frame number starts at 1
	captureBuffer getframe 1
	# Get the actual frame data
	set data [captureBuffer cget -frame]
	# Get vlantag2
	#set temp [ string range $data 48 52 ]
	set temp [string range $data 55 58 ]
    regsub -all " " $temp {} temp
    set temp "0x$temp"            
    set vlantag2 [format "%i" $temp]
    #ixPuts [ string range $data 36 64 ]
#	if { $temp1 == "81 00" || $temp1 == "91 00" || $temp1 == "92 00" } {
#	    ixPuts "vlantag2 = $vlantag2"
#	    return $vlantag2
#	} else {
##            ixPuts $data
#            return $vlantag2
#            }
    PrintRes Print "Get second vlan-tag : $vlantag2"
    return $vlantag2
}

##################################################################################
# 
# QinQGetTag3:判断抓到的包中是否three tags并获取第三个vlantag。
#
# args: 
#     host : IXIA的IP地址
#     card : IXIA的接口
#     port : IXIA的接口
# return:
#     vlantag3 : 第一个vlantag值
#     -1 :未抓到包
#     -2 :抓到的不是three tag包      
#
# addition:
#     - add by zouleia 2006.8.13
#
# examples:
#     QinQGetTag3 $host $txcard $txport
#
####################################################################################
#       
proc QinQGetTag3 {host card port} {
	package require IxTclHal
	# Connect to chassis and get chassis ID
	set host $host
	ixInitialize $host
	set chas [ixGetChassisID $host]
	# with port 1 looped to port 2
	set card $card
	set port $port
	set rxPortList [list [list $chas $card $port]]
	
	#ixClearStats rxPortList
	#ixStartCapture rxPortList
	capture get $chas $card $port
	set numFrames [capture cget -nPackets]
#	ixPuts "$numFrames frames captured"
#   未抓到包返回-1
	if {$numFrames == 0} {
		return -1
	}
	captureBuffer get $chas $card $port 3 3
	
	# Note that the frame number starts at 1
	captureBuffer getframe 1
	# Get the actual frame data
	set data [captureBuffer cget -frame]
	# Get vlantag3
	#set tpid3 [string range $data 60 64]
    set temp [string range $data 67 70 ]
    regsub -all " " $temp {} temp
    set temp "0x$temp"      
    set vlantag3 [format "%i" $temp]
    #ixPuts [ string range $data 36 64 ]
#	if { $tpid3 == "81 00" || $tpid3 == "91 00" || $tpid3 == "92 00" } {
#	    ixPuts "vlantag3 = $vlantag3"
#	    return $vlantag3
#	} else {
##            ixPuts $data
#            return $vlantag3
#            }
    PrintRes Print "Get third vlan-tag : $vlantag3"
    return $vlantag3
}


#这是需要计算校验和的ip头的16进制表示形式
#set Data "45000034921e400080060000c0a80141c0a80140"
#用要计算校验和的数据的16进制表示形式作为参数，返回校验和
proc CalcCheckSum { Data } {  
	set DataLen [string length $Data]
	set sum 0
	for {set i 0} {$i < [expr $DataLen - 3] } { incr i 4 } {
		set next "0x"
		append next [string range $Data $i [expr $i + 3] ]
		set sum [expr $sum + $next]
	}
	#对于长度不足的部分补0计算
	if { $i != $DataLen } {
		set next "0x"
		append next [string range $Data $i end ]
		append next [string repeat "0"  [expr 4-($DataLen - $i)]]
		#puts "$next"
		set sum [expr $sum + $next]
	}

	while { [expr $sum >> 16] > 0 } {
		set sum [expr ($sum & 0xffff) + ($sum >> 16)]
	}

	return [format %04X [expr (~$sum)& 0xffff]]
}

#sourceipv6 2000::1
#destinationipv6 3000::1
#icmpv6segment "83 00 00 00 00 00 00 00 FF 3F 00 00 00 00 00 00 00 00 00 00 00 00 00 01 00 00 00 00 00 00"
proc CalcIcmpv6CheckSum { sourceipv6 destinationipv6 payloadlength icmpv6segment } {
	regsub -all {\s} [FormatHexIpv6 $sourceipv6] "" sourceipv6
	regsub -all {\s} [FormatHexIpv6 $destinationipv6] "" destinationipv6
	set payloadlength [format %04X $payloadlength]
	set nextheader 003A
	set pseudoheader $sourceipv6$destinationipv6$payloadlength$nextheader
	regsub -all {\s} $icmpv6segment "" icmpv6segment
	set icmpv6segment [string replace $icmpv6segment 4 7 0000]
#	puts $pseudoheader$icmpv6segment
	return [CalcCheckSum $pseudoheader$icmpv6segment]
}

######################################################################
#
# CheckFrameReceivedNumber(已经修改):  获取某端口收/发包的统计数量
######################################################################
# 当需要查看的包的数量超过11201时，CheckCaptureStream不能返回大于上
# 值的任何数值，此时可以使用此函数获得统计数量
#
#
# args:
#     chas1, port1, card1:端口1的chas, port, card
#  
# addition:
#     成功：返回 收到包的数量
#     失败：返回 0 
# examples:
#     CheckFrameNumberReceived 1 1 2
######################################################################	 
proc CheckFrameReceivedNumber { chas1 card1 port1 } {
    set res [stat get statFramesReceived $chas1 $card1 $port1]
    if { $res > 0} {
        PrintRes Print "!could not get FramesReceivedNumber!"
        return -1
    } else {
        PrintRes Print "successful get FramesReceivedNumber: [stat cget -framesReceived] !"
        return [stat cget -framesReceived]
}
}


proc GetIxiaPortLineSpeed {chasid card port} {
	stat get statAllStats $chasid $card $port
	set res [stat cget -lineSpeed]
	return $res
}

##################################################################################
# 
# TakeOwnershipOfPorts : 配置ixia端口的ownership
#
#   hostname: ixia地址
#   username: 用户名
#       args: 端口号
#
# return:   1:配置成功
#           0:配置失败
#  
#
# examples: TakeOwnershipOfPorts 172.16.1.251 "zhangpengi" $Portlist1
####################################################################################
proc TakeOwnershipOfPorts {hostname username args} {
      #用户$username 登录    
	ixLogin $username
	set res 1
	if [ixConnectToChassis $hostname] {
		PrintRes Print "can not connect ixia:$hostname"
      		return 0    		
      	} else {
             for { set j 0} {$j < [llength $args ]} {incr j} {
      			set portvar [lindex $args $j]
      			for { set i 0} {$i < [llength $portvar ]} {incr i} {
      				set portlistx [list [lindex $portvar $i]]
      		 		if [ixTakeOwnership  $portlistx] {
      		 	      		PrintRes Print "take ownership $username for $portlistx failly" 
                         		set res 0
      		 		} else {
                         		PrintRes Print "take ownership $username for $portlistx successfully" 
      		 		}
      		 	}
      		}
      		
      	return $res
      		
      }
}

##################################################################################
# 
# ClearOwnershipOfPorts : 删除ixia端口的ownership
#
#   hostname: ixia地址
#   username: 用户名
#       args: 端口号
#
# return:   1:配置成功
#           0:配置失败
#  
#
# examples: ClearOwnershipOfPorts 172.16.1.251 "zhangpengi" $Portlist1
####################################################################################
proc ClearOwnershipOfPorts {hostname username args} {
      #用户$username 登录    
	ixLogin $username
	set res 1
	if [ixConnectToChassis $hostname] {
		PrintRes Print "can not connect ixia:$hostname"
      		return 0    		
      	} else {
             for { set j 0} {$j < [llength $args ]} {incr j} {
      			set portvar [lindex $args $j]
      			for { set i 0} {$i < [llength $portvar ]} {incr i} {
      				set portlistx [list [lindex $portvar $i]]
      		 		if [ixClearOwnership  $portlistx] {
      		 	      		PrintRes Print "clear ownership $username for $portlistx failly" 
                         		set res 0
      		 		} else {
                         		PrintRes Print "clear ownership $username for $portlistx successfully" 
      		 		}
      		 	}
      		}
      		
      	return $res
      		
      }
}


#**************************************************************#
#                                                              #
#                       结果检查函数                           #
#                                                              #
#**************************************************************#





