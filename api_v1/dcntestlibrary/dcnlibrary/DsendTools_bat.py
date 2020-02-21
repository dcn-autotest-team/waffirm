# -*- coding: UTF-8 -*-
# *********************************************************************
# DsendTools.py 
# 
# Author:  zhaohj@digitalchina.com
#
# Features: 
#           used by dcn auto generating packet tool
# 
# *********************************************************************
# Change log:
#     - 2011.8.1  modified by zhaohj
#
# *********************************************************************
import re

from dutils.dcnprint import printRes
from .dreceiver import *


##################################################################################
# 
# SetDsendStream:配置某一个端口的某一条流
#    
# args:
#     Port : 1
#     StreamMode 0 : 0:contine   1:stop after send  2:more than one stream on one port  默认为0
#     StreamNum 1 ：ixia端口模拟多条流时，各流的编号
#     LastStreamFlag true ：ixia端口模拟多条流时，该流是否为最后一条流
#     ReturnToId 1 ：ixia端口模拟多条流时，最后一条流的下一条流的编号
#     StreamRateMode : percent/fps/bps
#     StreamRate : 100/148810/76190476
#     NumFrames : 100
#
#     SouMac : 00-00-00-00-00-01
#     SouNum : 1
#     DesMac : 00-00-00-00-00-02
#     DesNum : 1
#
#     FrameSize : 128 报文长度
#
#     VlanTagFlag : 0   0:no vlan tag  1:exist one vlan tag  2:exist two vlan tag
#     VlanId : 3
#     Tpid : 8100
#     UserPriority : 5
#     Tpid1 : 9100
#     VlanId1 : 2
#     Tpid2 : 9200
#     VlanId2 : 3
#     
#     Protocl none : none/ipv4/arp/ipv6/ipv6ipv4  默认为none
#     EthernetType ieee8023/ieee8022 : notype/ethernetII/ieee8023snap/ieee8023，ieee8022  默认为ieee8023/ieee8022
#
#         SouIp 1.1.1.1
#         SouIpMode
#         SouIpNum 1
#     DesIp 2.2.2.2
#	  DesIpMode ipIncrHost
#	  DesIpNum 1
#	  Fragment 0   :是否分片
#	  LastFragment 0 :是否分片的最后一片
#	
#
#         ArpOperation  1 :  1 request 2 reply
#	  SenderMac  00-00-00-00-00-01
#	  SenderMacNum  1
#	  TargetMac  00-00-00-00-00-02
#	  TargetMacNum 1
#	  SenderIp  1.1.1.1
#	  SenderIpNum  1
#	  TargetIp  2.2.2.2
#	  TargetIpNum 1 
#
#         SouIpv6    2003:0001:0002:0003:0000:0000:0000:0003
#	  SouNumv6   1
#	  DesIpv6    2003:0001:0002:0003:0000:0000:0000:0004  
#	  DesNumv6   1
#	  PriorityFlag 1  ;#1:Dscp 0:Tos 2:Ipprecedence 3:Ipprecedence&Tos
#	  Dscp 41
#	  Tos 4
#	  Ipprecedence 7
#	  TrafficClass 3
#	  FlowLabel 0
#         NextHeader ipV6NoNextHeader
#
#
# return: 
#     编辑一个报文，Dsend()
# 
# 
# examples: 
################
# 1、持续发送一条流：
# 脚本中的调用格式：
#    SetDsendStream(Port='2',StreamMode='0',StreamRateMode='pps',StreamRate='10', FrameSize='64', \
#                   SouMac='00-00-00-00-00-01',SouNum='10',DesMac='00-00-00-00-00-04',DesNum='10')
# 实际发出的报文格式：
#    Dsend('''--port 2 --proc setStream --streamMode pps --rate 10 --streamSize 64 --stream Ether(dst=incrMac1[incrCount],src=incrMac2[incrCount],type=0x8100)/Dot1Q(vlan=2,type=0xffff) --incrMac1 00:00:00:00:00:04,10 --incrMac2 00:00:00:00:00:01,10''')
#################
# 2、发完一条流之后就停：（实际是利用pc发包，由于pc发包能力有限，速率控制有3种方式）
# 1）默认最大发包速率为200pps，大于200pps的速率会自动设置为200pps：
# 脚本中的调用格式：
#    SetDsendStream(Port='2',StreamMode='1',StreamRateMode='percent',StreamRate='10', FrameSize='64', \
#                   SouMac='00-00-00-00-00-01',SouNum='10',DesMac='00-00-00-00-00-04',DesNum='10')
# 实际发出的报文格式：
#    Dsend('''--port 2 --proc setStream --streamMode pps --rate 200 --streamSize 64 --stream Ether(dst=incrMac1[incrCount],src=incrMac2[incrCount],type=0x8100)/Dot1Q(vlan=2,type=0xffff) --incrMac1 00:00:00:00:00:04,10 --incrMac2 00:00:00:00:00:01,10 --count 1 --mode 2''')
# 2）如果200pps的速率太小，可以通过设置StreamMode2='1',这时会以pc的最大能力发包，大概1000pps：
# 脚本中的调用格式：
#    SetDsendStream(Port='2',StreamMode='1',StreamMode2='1',FrameSize='64',NumFrames='20000', \
#                   SouMac='00-00-00-00-00-01',SouNum='10',DesMac='00-00-00-00-00-04',DesNum='10')
# 实际发出的报文格式：
#    Dsend('''--port 2 --proc setStream --streamMode pps --streamSize 64 --stream Ether(dst=incrMac1[incrCount],src=incrMac2[incrCount],type=0x8100)/Dot1Q(vlan=2,type=0xffff) --incrMac1 00:00:00:00:00:04,10 --incrMac2 00:00:00:00:00:01,10 --count 20000''')
# 3）如果需要设置为200pps到1000pps之间的值，可以通过设置StreamMode3='1'
# 脚本中的调用格式：
#    SetDsendStream(Port='2',StreamMode='1',StreamMode3='1',StreamRateMode='pps',StreamRate='500',FrameSize='64',NumFrames='20000', \
#                   SouMac='00-00-00-00-00-01',SouNum='10',DesMac='00-00-00-00-00-04',DesNum='10')
# 实际发出的报文格式：
#    Dsend('''--port 2 --proc setStream --streamMode pps --rate 500 --streamSize 64 --stream Ether(dst=incrMac1[incrCount],src=incrMac2[incrCount],type=0x8100)/Dot1Q(vlan=2,type=0xffff) --incrMac1 00:00:00:00:00:04,10 --incrMac2 00:00:00:00:00:01,10 --count 20000 --mode 2''')
######################
# 3、持续循环发送几条流：
# 脚本中的调用格式：
#    SetDsendStream(Port='2',StreamMode='0',StreamRate='2000',StreamRateMode='pps',NumFrames='10',FrameSize='64',LastStreamFlag='false', \
#		   DesMac='00-00-00-02-00-02',SouMac='00-00-00-01-00-01',SouNum='10')
#    SetDsendStream(Port='2',StreamMode='2',StreamRate='2000',StreamRateMode='pps',NumFrames='1',FrameSize='64',LastStreamFlag='true', \
#		   DesMac='00-00-00-00-00-04',SouMac='00-00-00-00-00-03')
# 实际发出的报文格式：
#    Dsend('''--port 2 --proc setStream --streamMode pps --rate 2000 --streamSize 64 --stream Ether(dst="00:00:00:02:00:02",src=incrMac1[incrCount],type=0x8100)/Dot1Q(vlan=2,type=0xffff) --incrMac1 00:00:00:01:00:01,10 --lastStreamFlag 0''')
#    Dsend('''--port 2 --proc setStream --streamMode pps --rate 2000 --streamSize 64 --stream Ether(dst="00:00:00:00:00:04",src="00:00:00:00:00:03",type=0x8100)/Dot1Q(vlan=2,type=0xffff) --lastStreamFlag 1 --countContinue 1 ''')
###############################################################################################################
def SetDsendStream(**args):
    ########################################################################################################################################################################################################################################################################################################################################
    # 函数SetDsendStream设计原理:通过DCN自动发包软件发送报文时，最后需要执行如下命令:
    # Dsend('''--port 6  --proc setStream --streamMode percent --rate 100 --streamSize auto --stream Ether(src="00:00:00:00:00:01",dst="00:00:00:00:00:02",type=0x8100)/Dot1Q(vlan=6,type=0xffff)''')
    # 可以看出只要得到其中的参数--port，--streamMode，--rate，--streamSize，--stream的具体值，则可以很方便地发送报文，因此该函数的设计思路是按顺序获取这些参数值
    #
    # 如果是发送域值变化的数据报文，其最后的发包命令会有些不同，例如:
    # 配置源mac递增的报文：
    # Dsend('''--port 6  --proc setStream --streamMode percent --rate 100 --streamSize auto --stream Ether(src=incrMac1[incrCount],dst="00:00:00:00:00:02",type=0x8100)/Dot1Q(vlan=6,type=0xffff)/IP(src="110.1.1.28",dst="110.1.1.1",id=0)/UDP(sport=520)/RIP(cmd=2,version=2)/RIPEntry(addr="110.0.0.0",mask="255.255.255.0") --incrMac1 00:00:01:00:00:01,100''')
    # 但其设计思路不变，具体发包命令详见发包工具使用说明文档
    #
    # 如果是发送一定数量报文后停止存在两种发包模式:1不带参数--mode 2和--rate:标识自动发包工具以pc的最大发包能力进行发包，对于这样发送的报文，存在抓包丢包现象；2 带参数--mode 2和参数--rate:标识自动发包工具以--rate参数指定的发包速率进行发送，真实如果
    # 发送的速率小于等于10，则不需要带--mode 2
    #########################################################################################################################################################################################################################################################################################################################################
    # 需要用到的全局变量
    # 最后需要发送的流数据
    global dcnstream
    # 需要发送的数据流的参数列表
    global dcnarrArgs
    # 用于存储需要递增的报文域 :包括递增的类型(mac,ip,num),初始值，范围和步长；每条流的突发报文数目--countContinue；
    # 需要发送的报文数量(发完就停)--count,用于标识发送一定数量报文的发包速率是通过参数--rate指定:--mode 2
    global dcnincrlist
    # 用于记录是第几个需要变化的mac域类型
    global dcnincrmac
    # 用于记录是第几个需要变化的ip域类型
    global dcnincrip
    # 用于记录是第几个需要变化的num域类型
    global dcnincrnum
    # 用于记录是第几个需要变化的ipv6域类型
    global dcnincripv6
    # dot3用于标明是否是802.3报文(包括802.3 snap)，0表示不是，1表示是
    global dot3
    # 待发送数据的速率模式
    global streamMode
    # 待发送数据的大小
    global streamSize

    # 初始化各全局变量
    dcnincrmac = 0
    dcnincrip = 0
    dcnincrnum = 0
    dcnincripv6 = 0
    dot3 = 0
    # 初始化dcnincrlist为空列表
    dcnincrlist = []

    # 获取发包的速率模式--streamMode: percent,pps,bps
    streamMode = GetRateMode(args)

    # 获取发包的默认速率
    GetDefaultStreamRate(args)

    # 获取发包的大小 --streamSize:只有在速率小于10pps的时候才能设置streamsize为指定值或默认128，其余情况设置为auto
    # 这样设置的原因见自动发包工具设计原理:大于10pps是通过loopback口和带宽限制实现，为了精确速率就必须对报文大小做限制
    streamSize = GetStreamSize(args)

    # 构造需要发送的报文--stream(适合python scapy发送的报文结构，字符串格式,存储在dcnstream中)
    # 构造以太网报文头
    BuildEthernetII(args)

    # 构造Dot1q报文头:因为自动发包工具的设计原理，所发送的报文必须有dot1q头并且通过该报文头决定所发出的端口
    dcnstream = dcnstream + "/Dot1Q(vlan=" + args['Port'] + ",type=0xffff)"

    # 下面可以添加各种报文

    # 构造no type报文头
    BuildNoType(args)

    # 构造802.3和80.2.2报文头
    Build8023(args)

    # 构造802.3 snap 报文头
    Build8023Snap(args)

    # 构造802.1q tag
    BuildDot1Q(args)

    # 对于指定以太网协议类型，需要修改dot1q报文头中的type值
    SetEthernetIIType(args)

    # 构造后续三层协议报文
    if 'Protocl' in args:
        if args['Protocl'] == 'arp':
            print('build arp packet')
            BuildArp(args)
        if args['Protocl'] == 'ipv4':
            print('build ipv4 packet')
            BuildIPv4(args)
        if args['Protocl'] == 'ipv6':
            print('build ipv6 packet')
            BuildIPv6(args)
        if args['Protocl'] == 'ipv6ipv4':
            print('build ipv4 over ipv6 tunnel packet')
            BuildIPv4OverIPv6(args)

            # 添加报文结束

    # 针对发完一定数目报文就停的发包模式
    # --count 10 :标识该条流发完10条后停止
    # $dcnarrArgs(StreamMode2)为1则表示pc尽最大的能力发送数据，为0则通过用户指定(如果pc通过最大能力发包，则pc再抓取该包时会丢包
    # --mode 2用于表示发送指定数量报文的发送速率是通过--rate指定，而不是pc以最大能力发送(最后的真实发送速率在这个值附近)  
    # python实现实例
    # 1、正常发n个报文后停止(pps <= 10)
    # python Dsend.py --port 3   --rate 10 --proc "setStream" --streamMode pps  --streamSize 64 --stream
    # {Ether(dst="01:00:00:00:02:11",type=0x8100)/Dot1Q(vlan=3,type=0xffff,prio=1) } --count 100
    #
    # 2、发n个报文后停止(超级快模式,没有--rate)
    # python Dsend.py --port 3  --proc "setStream" --streamMode pps  --streamSize 64 --stream
    # {Ether(dst="01:00:00:00:02:11",type=0x8100)/Dot1Q(vlan=3,type=0xffff,prio=1) } --count 100
    #
    # 3、指定最大速率,发n个报文后停止(模式2,--mode 2)
    # python Dsend.py --port 3 --mode 2 --rate 200  --proc "setStream" --streamMode pps  --streamSize 64 --stream
    # {Ether(dst="01:00:00:00:02:11",type=0x8100)/Dot1Q(vlan=3,type=0xffff,prio=1) } --count 100
    SetStreamModeForStop(args)

    # 打印以方便调试
    print(args['Port'])
    print(streamMode)
    print(args['StreamRate'])
    print(streamSize)
    print(dcnstream)

    # 变量 dcnarrArgs(StreamMode2)为1表示自动发包工具以pc的最大速率发包(仅在尽力发送一定数量报文后就停时使用)
    if args['StreamMode2'] == '1':
        command = ("--port " + args[
            'Port'] + " --proc setStream " + "--streamMode " + streamMode + " --streamSize " + streamSize + " --stream " + dcnstream)
    else:
        command = ("--port " + args['Port'] + " --proc setStream " + "--streamMode " + streamMode + " --rate " + args[
            'StreamRate'] + " --streamSize " + streamSize + " --stream " + dcnstream)

    # 添加标识报文流是否为最后一条流的命令参数(存在多条流的情况才需要该参数),
    # 例如--lastStreamFlag 1
    AddLastStreamFlag(args)

    # 添加标识某条报文流的突发报文数量
    # 例如--countContinue 6 :标识该条流突发6条报文
    if 'NumFrames' in args and 'LastStreamFlag' in args and int(args['StreamMode']) == 2:
        print(args['NumFrames'])
        strinfo = '--countContinue ' + args['NumFrames']
        dcnincrlist.append(strinfo)

    # 添加报文中域值变化的相关命令参数例如--incrMac1 00:00:01:00:00:01,100 ;是否为最后一条流的命令参数例如--lastStreamFlag 1
    #    ;流的突发数目:--countContinue 2;需要发送的数量:--count 10
    if len(dcnincrlist) >= 1:
        length = len(dcnincrlist)
        for i in range(length):
            command = command + ' ' + dcnincrlist[i]

    # 打印出命令，主要用于调试
    print(command)

    # 执行发包操作
    res = Dsend(command)
    return res


##################################################################################
#
# GetRateMode :获取发送数据流的模式:percent,pps,bps
#
#
# return: 数据流的模式:percent,pps,bps
#
# addition:
#
# examples:
#     GetRateMode(args)
#
###################################################################################
def GetRateMode(args):
    if 'StreamRateMode' not in args:
        return 'percent'
    else:
        return args['StreamRateMode']


###################################################################################
#
# GetDefaultStreamRate :获取发送数据流的默认速率:100%线速，148810pps,76190476 bps
#
# args:  streamMode:数据流的发送模式:percent,pps.bps
#
# examples:
#     GetDefaultStreamRate(pps,args)
#
#################################################################################### 
def GetDefaultStreamRate(args):
    global streamMode
    if 'StreamRate' not in args:
        if streamMode == 'percent':
            args['StreamRate'] = '100'
        if streamMode == 'pps':
            args['StreamRate'] = '148810'
        if streamMode == 'bps':
            args['StreamRate'] = '76190476'


##################################################################################
#
# GetStreamSize :获取发送数据流的报文大小
#
# args:  
#    streamMode: percent/pps/bps
#    streamRate: 发包速率
#    args：全局参数
#
# return: 数据流的报文大小:auto或指定大小或默认大小128byte
#
# addition:
#
# examples:
#     GetStreamSize('pps','100',args)
#
###################################################################################
def GetStreamSize(args):
    global streamMode
    if streamMode == 'percent':
        if args['StreamRate'] == '100':
            if 'FrameSize' in args:
                return args['FrameSize']
            else:
                return 'auto'
        else:
            return 'auto'
    if streamMode == 'bps':
        if 'StreamRate' not in args:
            if 'FrameSize' in args:
                return args['FrameSize']
            else:
                return 'auto'
        else:
            return 'auto'
    if streamMode == 'pps':
        if 'StreamRate' in args:
            if args['StreamRate'] <= '10':
                if 'FrameSize' in args:
                    return args['FrameSize']
                else:
                    return 'auto'
            else:
                if 'FrameSize' in args:
                    if int(args['StreamRate']) * int(args['FrameSize']) % 64000 == 0:
                        return args['FrameSize']
                    else:
                        return 'auto'
                else:
                    return 'auto'
        else:
            if 'FrameSize' in args:
                return args['FrameSize']
            else:
                return 'auto'


##################################################################################
#
#  BuildEthernetII :构建由python scapy发送的EthernetII报文头，如Ether(....)
#
# args:  无
#
# return: 无
#
# addition:
#
# examples:
#     BuildEthernetII(args)
#
###################################################################################
def BuildEthernetII(args):
    global dcnstream
    dcnstream = "Ether("
    # 构造以太网的目的mac
    if 'DesMac' not in args:
        args['DesMac'] = '00-00-00-00-00-01'
    if 'DesNum' not in args:
        args['DesNum'] = '1'
    # 将mac的格式由00-00-00-00-00-01转化为00:00:00:00:00:01
    args['DesMac'] = re.sub('-', ':', args['DesMac'])
    # 构建目的mac域:覆盖两种处理情况连续变化和稳定不变
    BuildIncrField('dst', 'mac', args['DesMac'], args['DesNum'])

    # 构造以太网的源mac
    if 'SouMac' not in args:
        args['SouMac'] = '00-00-00-00-00-02'
    if 'SouNum' not in args:
        args['SouNum'] = '1'
    # 将mac的格式由00-00-00-00-00-01转化为00:00:00:00:00:01
    args['SouMac'] = re.sub('-', ':', args['SouMac'])
    # 构建目的mac域:覆盖两种处理情况连续变化和稳定不变
    BuildIncrField('src', 'mac', args['SouMac'], args['SouNum'])

    # 构造以太网的type，因为自动发包软件的特性需要加dot1q头，所以type始终为0x8100
    dcnstream = dcnstream + "type=0x8100)"


##################################################################################
#
# BuildIncrField  :构建由python scapy发送的报文中变化的域
#
# args:  name:域名，type:变化的类型，目前有三种:mac,ip和num;initi:变化的初始值；num:变化的范围数量
#          step为变化步长，duan为需要变化的字段具体位置
# return: 无
#
# addition:
#
# examples:
#     BuildIncrField('mac','dst','00:00:00:00:00:01','2',step='1',duan='128')
#
###################################################################################    
def BuildIncrField(name, type, initi, num, step='1', duan='128'):
    global dcnstream
    global dcnincrlist
    global dcnincrmac
    global dcnincrip
    global dcnincrnum
    global dcnincripv6

    if num == '1':
        if type == 'mac' or type == 'ip' or type == 'ipv6':
            dcnstream = dcnstream + name + '=' + '"' + initi + '"' + ','
        else:
            dcnstream = dcnstream + name + '=' + initi + ','
    else:
        if type == 'mac':
            dcnincrmac = dcnincrmac + 1
            dcnstream = dcnstream + name + '=incrMac' + str(dcnincrmac) + '[incrCount],'
            macliststr = "--incrMac" + str(dcnincrmac) + ' ' + initi + ',' + str(num)
            dcnincrlist.append(macliststr)
        if type == 'ip':
            dcnincrip = dcnincrip + 1
            dcnstream = dcnstream + name + '=incrIp' + str(dcnincrip) + '[incrCount],'
            ipliststr = "--incrIp" + str(dcnincrip) + ' ' + initi + ',' + str(num) + ',' + str(duan) + ',' + str(step)
            dcnincrlist.append(ipliststr)
        if type == 'num':
            dcnincrnum = dcnincrnum + 1
            dcnstream = dcnstream + name + '=incrNum' + str(dcnincrnum) + '[incrCount],'
            numliststr = "--incrNum" + str(dcnincrnum) + ' ' + initi + ',' + str(num)
            dcnincrlist.append(numliststr)
        if type == 'ipv6':
            dcnincripv6 = dcnincripv6 + 1
            dcnstream = dcnstream + name + '=incrIpv6' + str(dcnincripv6) + '[incrCount],'
            ipv6liststr = "--incrIpv6" + str(dcnincripv6) + ' ' + initi + ',' + str(num) + ',' + str(duan) + ',' + str(
                step)
            dcnincrlist.append(ipv6liststr)

            ##################################################################################


#
# SetStreamModeForStop :设置由python scapy发送报文的一种模式:发送一定数量的报文后停止
#
# args:  无
#
# return: 无
#
# addition:
#
# examples:
#     SetStreamModeForStop(args)
#
# ##################################################################################
def SetStreamModeForStop(args):
    global dcnarrArgs
    global dcnincrlist
    global streamMode
    global streamSize
    # StreamMode2用于标识该数据流是否通过pc尽力发送，1标识通过pc尽力发送
    if 'StreamMode2' not in args:
        args['StreamMode2'] = '0'
    # 当StreamMode3为1时，可以以大于200pps小于1000pps的速率发送报文
    if 'StreamMode3' not in args:
        args['StreamMode3'] = '0'

    if 'StreamMode' in args:
        if args['StreamMode'] == '1':
            if 'NumFrames' in args:
                numframestr = '--count ' + args['NumFrames']
                dcnincrlist.append(numframestr)
            else:
                dcnincrlist.append('--count 1')

            if args['StreamMode2'] == '1':
                streamMode = 'pps'
            else:
                if streamMode == 'pps' and int(args['StreamRate']) <= 10:
                    printstrinfo = 'sends ' + args['NumFrames'] + ' packets ' + args['StreamRate'] + ' pps.'
                    print(printstrinfo)
                else:
                    dcnincrlist.append('--mode 2')
                    if streamMode == 'percent':
                        args['StreamRate'] = '200'
                    if streamMode == 'pps':
                        if 200 < int(args['StreamRate']) < 1000:
                            if args['StreamMode3'] == '0':
                                args['StreamRate'] = '200'
                        if int(args['StreamRate']) >= 1000:
                            args['StreamRate'] = '200'
                    if streamMode == 'bps':
                        args['StreamRate'] = '200'

                    streamMode = "pps"

            if 'FrameSize' in args:
                streamSize = args['FrameSize']
            else:
                streamSize = '128'


# #################################################################################


#
# AddLastStreamFlag :对于待发送的多条流，需要添加参数--lastStreamFlag 0/1:
#                   1表示为最后一条流，0表示还有其它流
#
# args:  无
#
# return: 无
#
# addition:
#
# examples:
#     AddLastStreamFlagargs)
#
###################################################################################
def AddLastStreamFlag(args):
    global dcnincrlist
    if 'LastStreamFlag' in args:
        print(args['LastStreamFlag'])
        if args['LastStreamFlag'] == 'true':
            strinfo = '--lastStreamFlag 1'
            dcnincrlist.append(strinfo)
        if args['LastStreamFlag'] == 'false':
            strinfo = '--lastStreamFlag 0'
            dcnincrlist.append(strinfo)


##################################################################################
#
#  BuildNoType :构建由python scapy发送的NoType报文头，如Dot3TagNoLen(....), 即二层包头的协议类型为空
# args:  无
#
#
# examples:
#     BuildNoType(args)
# 脚本中的调用举例：SetDsendStream(Port='2',StreamRateMode='pps',StreamRate='10', FrameSize='64', \
#                                 EthernetType='notype',VlanId='12', \
#              	                  SouMac='00-00-00-00-00-03',DesMac='00-00-00-00-00-04')
###################################################################################
def BuildNoType(args):
    global dcnstream
    global dot3

    if 'EthernetType' in args and args['EthernetType'] == 'notype':
        dot3 = 1
        if 'VlanId' in args or 'UserPriority' in args:
            if 'Tpid' in args:
                strinfo = '0x' + args['Tpid']
                dcnstream = re.sub('0xffff', strinfo, dcnstream)
            else:
                dcnstream = re.sub('0xffff', '0x8100', dcnstream)
            dcnstream = dcnstream + '/Dot3TagNoLen('
            if 'VlanId' in args:
                args['VlanId'] = args['VlanId'].split(" ")
                vlanid1 = args['VlanId'][0]
                dcnstream = dcnstream + 'vlan=' + vlanid1 + ','
            else:
                args['VlanId'] = '1'
            if 'UserPriority' in args:
                dcnstream = dcnstream + 'prio=' + args['UserPriority'] + ','
            dcnstream = dcnstream + ')'
            if len(args['VlanId']) > 1:
                dcnstream = re.sub(',\)', ',len=0x8100)', dcnstream)
                dcnstream = dcnstream + '/Dot3TagNoLen('
                vlanid2 = args['VlanId'][1]
                dcnstream = dcnstream + 'vlan=' + vlanid2 + ',)'
        else:
            dcnstream = re.sub('Dot1Q', 'Dot3TagNoLen', dcnstream)
            dcnstream = re.sub('type=0xffff', '', dcnstream)


##################################################################################
#
#  Build8023 :构建由python scapy发送的802.3报文头，如Dot3Tag(....)
#
# args:  无
#
# return: 无
#
# addition:
#
# examples:
#     Build8023(args)
# 脚本调用格式：
#     SetDsendStream(Port='2',StreamRateMode='pps',StreamRate='10', FrameSize='64', \
#                    VlanId='22',UserPriority='4',Offset1='18',Length1='3',Value1='aabb05', \
#                    SouMac='00-00-00-00-00-03',DesMac='00-00-00-00-00-04')
###################################################################################
def Build8023(args):
    global dcnstream
    global dot3
    # 如果不存在参数 EthernetType，则默认发送802.3报文
    if 'EthernetType' not in args:
        args['EthernetType'] = 'ieee8023'
    # 构造802.3报文头
    if 'EthernetType' in args:
        if args['EthernetType'] == 'ieee8023' or args['EthernetType'] == 'ieee8022':
            dot3 = 1
            if 'VlanId' in args or 'UserPriority' in args:
                if 'Tpid' in args:
                    strinfo = '0x' + args['Tpid']
                    dcnstream = re.sub('0xffff', strinfo, dcnstream)
                else:
                    dcnstream = re.sub('0xffff', '0x8100', dcnstream)
                dcnstream = dcnstream + '/Dot3Tag('
                if 'VlanId' in args:
                    args['VlanId'] = args['VlanId'].split(" ")
                    vlanid1 = args['VlanId'][0]
                    dcnstream = dcnstream + 'vlan=' + vlanid1 + ','
                else:
                    args['VlanId'] = '1'
                if 'UserPriority' in args:
                    dcnstream = dcnstream + 'prio=' + args['UserPriority'] + ','
                dcnstream = dcnstream + ')'
                if len(args['VlanId']) > 1:
                    dcnstream = re.sub(',\)', ',len=0x8100)', dcnstream)
                    dcnstream = dcnstream + '/Dot3Tag('
                    vlanid2 = args['VlanId'][1]
                    dcnstream = dcnstream + 'vlan=' + vlanid2 + ',)'
            else:
                dcnstream = re.sub('Dot1Q', 'Dot3Tag', dcnstream)
                dcnstream = re.sub('type=0xffff', '', dcnstream)

            # 添加LLC头
            if 'Offset1' in args:
                if args['Offset1'] == '14' or args['Offset1'] == '18':
                    if 'Length1' not in args:
                        args['Length1'] = '2'
                    if args['Length1'] == '2':
                        if 'Value1' not in args:
                            args['Value1'] = 'aaaa'
                        value1 = '0x' + args['Value1']
                        dsap = hex((int(value1, 16) & 0xff00) >> 8)
                        ssap = hex(int(value1, 16) & 0x00ff)
                        dcnstream = dcnstream + '/LLC(dsap=' + dsap + ',ssap=' + ssap + ',ctrl=0x03)'
                    if args['Length1'] == '3':
                        if 'Value1' not in args:
                            args['Value1'] = 'aaaa03'
                        value1 = '0x' + args['Value1']
                        dsap = hex((int(value1, 16) & 0xff0000) >> 16)
                        ssap = hex((int(value1, 16) & 0x00ff00) >> 8)
                        ctrl = hex(int(value1, 16) & 0x0000ff)
                        dcnstream = dcnstream + '/LLC(dsap=' + dsap + ',ssap=' + ssap + ',ctrl=' + ctrl + ')'


###############################################################################################################
#  Build8023Snap :构建由python scapy发送的802.3snap报文头，如Ether()/Dot3Tag()/LLC(dsap=0xaa,ssap=0xaa,ctrl=0x03)/
#  SNAP()/"……"
#
# args: 无
#
# return: 无
#
# addition:
#
# examples:
#     Build8023Snap(args)
# 调用格式：
#     SetDsendStream(Port='2',StreamRateMode='pps',StreamRate='10', FrameSize='64', \
#                   EthernetType='ieee8023snap',Offset1='20',Value1='a',Repeat1='2', \
#		    VlanId='22',UserPriority='4', \
#		    SouMac='00-00-00-00-00-03',DesMac='00-00-00-00-00-04')			
# #################################################################################################################
def Build8023Snap(args):
    global dcnstream
    global dcnincrnum
    global dcnincrlist
    global dot3

    if 'EthernetType' in args and args['EthernetType'] == 'ieee8023snap':
        dot3 = 1
        if 'VlanId' in args or 'UserPriority' in args:
            dcnstream = re.sub('0xffff', '0x8100', dcnstream)
            dcnstream = dcnstream + '/Dot3Tag('
            if 'VlanId' in args:
                dcnstream = dcnstream + 'vlan=' + args['VlanId'] + ','
            if 'UserPriority' in args:
                dcnstream = dcnstream + 'prio=' + args['UserPriority'] + ','
            dcnstream = dcnstream + ')'
        else:
            dcnstream = re.sub('Dot1Q', 'Dot3Tag', dcnstream)
            dcnstream = re.sub('type=0xffff', '', dcnstream)
        # 添加LLC头
        dcnstream = dcnstream + '/LLC(dsap=0xaa,ssap=0xaa,ctrl=0x03)'
        # 添加SNAP头
        dcnstream = dcnstream + '/SNAP(code=0xffff)'

        if 'Offset1' in args and args['Offset1'] == '20':
            if 'Value1' not in args:
                args['Value1'] = '0'
            value1 = '0x' + args['Value1']
            value1 = int(value1, 16)
            if 'Repeat1' not in args:
                args['Repeat1'] = '1'
            if 'Step1' not in args:
                args['Step1'] = '1'
            if args['Repeat1'] == '1':
                dcnstream = re.sub('0xffff', value1, dcnstream)
            else:
                dcnincrnum = dcnincrnum + 1
                strinfo = 'incrNum' + str(dcnincrnum) + '[incrCount]'
                dcnstream = re.sub('0xffff', strinfo, dcnstream)
                strinfo1 = '--incrNum' + str(dcnincrnum) + ' ' + str(value1) + ',' + args['Repeat1']
                dcnincrlist.append(strinfo1)


##################################################################################
#
# BuildDot1Q :构建由python scapy发送的802.3报文头，如Dot1Q(....)
#
# args:  无
#
# return: 无
#
# addition:
#
# examples:
#     BuildDot1Q(args)
# 脚本调用格式：		
#     SetDsendStream(Port='2',StreamRateMode='pps',StreamRate='10', FrameSize='64', \
#                    VlanTagFlag='1',Tpid='9200',VlanId='33',UserPriority='5', \
#		     SouMac='00-00-00-00-00-03',DesMac='00-00-00-00-00-04')
# ##################################################################################
def BuildDot1Q(args):
    global dcnstream
    global dot3
    global dcnincrnum
    global dcnincrlist

    if 'VlanTagFlag' in args and dot3 == 0:
        # 判断是否带802.1q tag
        if args['VlanTagFlag'] == '1':
            # 如果是带802.1q tag则修改前面获取的Dot1Q()中的type字段为用户指定值
            if 'Tpid' in args:
                strinfo = '0x' + args['Tpid']
                dcnstream = re.sub('0xffff', strinfo, dcnstream)
            # 如果是带802.1q tag则修改前面获取的Dot1Q()中的type字段为0x8100
            else:
                dcnstream = re.sub('0xffff', '0x8100', dcnstream)
            dcnstream = dcnstream + '/Dot1Q('
            if 'VlanId' in args:
                dcnstream = dcnstream + 'vlan=' + args['VlanId'] + ','
            else:
                if 'Offset1' in args and args['Offset1'] == '14':
                    if 'Value1' not in args:
                        args['Value1'] = '1'
                    value1 = '0x' + args['Value1']
                    value1 = int(value1, 16)
                    if 'Repeat1' not in args:
                        args['Repeat1'] = '1'
                    if 'Step1' not in args:
                        args['Step1'] = '1'
                    if args['Repeat1'] == '1':
                        dcnstream = dcnstream + 'vlan=' + args['Value1']
                    else:
                        dcnincrnum = dcnincrnum + 1
                        dcnstream = dcnstream + 'vlan=incrNum' + str(dcnincrnum) + '[incrCount],'
                        strinfo = '--incrNum' + str(dcnincrnum) + ' ' + str(value1) + ',' + args['Repeat1']
                        dcnincrlist.append(strinfo)
            if 'UserPriority' in args:
                dcnstream = dcnstream + 'prio=' + args['UserPriority'] + ','
            dcnstream = dcnstream + 'type=0xffff)'
        # 添加对DoubleTag 的支持
        if args['VlanTagFlag'] == '2':
            if 'Tpid2' in args:
                strinfo = '0x' + args['Tpid2']
                dcnstream = re.sub('0xffff', strinfo, dcnstream)
            else:
                dcnstream = re.sub('0xffff', '0x8100', dcnstream)
            dcnstream = dcnstream + '/Dot1Q('
            if 'VlanId2' in args:
                dcnstream = dcnstream + 'vlan=' + args['VlanId2'] + ','
            if 'UserPriority2' in args:
                dcnstream = dcnstream + 'prio=' + args['UserPriority2'] + ','
            if 'Tpid1' in args:
                dcnstream = dcnstream + 'type=0x' + args['Tpid1'] + ')'
            else:
                dcnstream = dcnstream + 'type=0x8100)'

            dcnstream = dcnstream + '/Dot1Q('
            if 'VlanId1' in args:
                dcnstream = dcnstream + 'vlan=' + args['VlanId1'] + ','
            if 'UserPriority1' in args:
                dcnstream = dcnstream + 'prio=' + args['UserPriority1'] + ','
            dcnstream = dcnstream + 'type=0xffff)'


##################################################################################
#
# SetEthernetIIType :设置以太网报文的type值
#
# args:  无
#
# return: 无
#
# addition:
#
# examples:
#     SetEthernetIIType(args)
# ##################################################################################
def SetEthernetIIType(args):
    global dcnstream
    global dcnincrnum
    global dcnincrlist

    # 直接通过参数EthernetTypeNum指定    EthernetII 的Type值
    if 'EthernetTypeNum' in args:
        dcnstream = re.sub('0xffff', args['EthernetTypeNum'], dcnstream)
    # 通过参数EthernetTypeFlag和UDF1Flag指明通过偏移量指定 EthernetII 的Type值为Value1
    if 'EthernetTypeFlag' in args and 'UDF1Flag' in args:
        if args['EthernetTypeFlag'] == '1' and args['UDF1Flag'] == '1':
            if 'Value1' not in args:
                args['Value1'] = 'ffff'
            value1 = '0x' + args['Value1']
            value1 = int(value1, 16)
            if 'Repeat1' not in args:
                args['Repeat1'] = '1'
            if 'Step1' not in args:
                args['Step1'] = '1'
            if args['Repeat1'] == '1':
                dcnstream = re.sub('0xffff', hex(value1), dcnstream)
            else:
                dcnincrnum = dcnincrnum + 1
                strinfo = 'incrNum' + str(dcnincrnum) + '[incrCount]'
                dcnstream = re.sub('0xffff', strinfo, dcnstream)
                strinfo1 = '--incrNum' + str(dcnincrnum) + ' ' + value1 + ',' + args['Repeat1']
                dcnincrlist.append(strinfo1)
    # 直接通过参数UDF1Flag==1和Offset1==12指明通过偏移量修改    EthernetII 的Type值为Value1
    if 'Offset1' in args and 'UDF1Flag' in args:
        if args['Offset1'] == '12' and args['UDF1Flag'] == '1':
            if 'Value1' not in args:
                args['Value1'] = 'ffff'
            value1 = '0x' + args['Value1']
            value1 = int(value1, 16)
            if 'Repeat1' not in args:
                args['Repeat1'] = '1'
            if 'Step1' not in args:
                args['Step1'] = '1'
            if args['Repeat1'] == '1':
                # 区分Dot1Q和Dot3Q    :Dot1Q的type=0xffff,Dot3Q没有type,只有len且默认情况不赋值
                if 'type=0xffff' in dcnstream:
                    dcnstream = re.sub('0xffff', hex(value1), dcnstream)
                else:
                    strinfo = ',len=' + hex(value1) + ')'
                    dcnstream = re.sub(',\)', strinfo, dcnstream)
            else:
                dcnincrnum = dcnincrnum + 1
                if 'type=0xffff' in dcnstream:
                    strinfo1 = 'incrNum' + str(dcnincrnum) + '[incrCount]'
                    dcnstream = re.sub('0xffff', strinfo1, dcnstream)
                else:
                    strinfo1 = ',len=' + 'incrNum' + str(dcnincrnum) + '[incrCount]' + ')'
                    dcnstream = re.sub(',\)', strinfo1, dcnstream)
                strinfo2 = '--incrNum' + str(dcnincrnum) + ' ' + str(value1) + ',' + args['Repeat1']

        if args['Offset1'] == '14' and args['UDF1Flag'] == '1':
            if 'Length1' not in args:
                args['Length1'] = '2'
            if args['Length1'] == '2':
                if 'Value1' not in args:
                    args['Value1'] = 'aaaa'
                value1 = '0x' + args['Value1']
                dsap = hex((int(value1, 16) & 0xff00) >> 8)
                ssap = hex(int(value1, 16) & 0x00ff)
                dcnstream = dcnstream + '/LLC(dsap=' + dsap + ',ssap=' + ssap + ',ctrl=0x03)'
            if args['Length1'] == '3':
                if 'Value1' not in args:
                    args['Value1'] = 'aaaa03'
                value1 = '0x' + args['Value1']
                dsap = hex((int(value1, 16) & 0xff0000) >> 16)
                ssap = hex((int(value1, 16) & 0x00ff00) >> 8)
                ctrl = hex(int(value1, 16) & 0x0000ff)
                dcnstream = dcnstream + '/LLC(dsap=' + dsap + ',ssap=' + ssap + ',ctrl=' + ctrl + ')'


##################################################################################
#
# BuildArp :构建由python scapy发送的arp报文，如ARP(....)
#
# args:  无
#
# return: 无
#
# addition:
#
# examples:
#     BuildArp(args)
# 脚本调用格式：
#    SetDsendStream(Port='2',StreamRateMode='pps',StreamRate='10', FrameSize='64', \
#		   SouMac='00-00-00-00-00-03',DesMac='00-00-00-00-00-04', \
#		   Protocl='arp',ArpOperation='2',\
#		   SenderMac='00-00-00-00-00-05',SenderMacNum='2',TargetMac='00-00-00-00-00-06',TargetMacNum='2', \
#		   SenderIp='5.5.5.5',SenderIpNum='2',TargetIp='6.6.6.6',TargetIpNum='2')		
# ##################################################################################
def BuildArp(args):
    global dcnstream

    # 修改前面获取的Dot1Q()中的type字段为0x0806,如果前面是Dot3Tag,则需要增加len=0x0806
    if 'type=0xffff' in dcnstream:
        dcnstream = re.sub('0xffff', '0x0806', dcnstream)
    else:
        dcnstream = re.sub(',\)', ',len=0x0806)', dcnstream)
    dcnstream = dcnstream + '/ARP('

    # 构建arp operation字段
    if 'ArpOperation' in args:
        dcnstream = dcnstream + 'op=' + args['ArpOperation'] + ','

    # 构建arp SenderMac字段
    if 'SenderMac' not in args:
        args['SenderMac'] = '00-00-00-00-00-01'
    if 'SenderMacNum' not in args:
        args['SenderMacNum'] = '1'
    # 将mac的格式由00-00-00-00-00-01转化为00:00:00:00:00:01
    args['SenderMac'] = re.sub('-', ':', args['SenderMac'])
    BuildIncrField('hwsrc', 'mac', args['SenderMac'], args['SenderMacNum'])

    # 构建arp TargetMac字段
    if 'TargetMac' not in args:
        args['TargetMac'] = '00-00-00-00-00-02'
    if 'TargetMacNum' not in args:
        args['TargetMacNum'] = '1'
    # 将mac的格式由00-00-00-00-00-02转化为00:00:00:00:00:02
    args['TargetMac'] = re.sub('-', ':', args['TargetMac'])
    BuildIncrField('hwdst', 'mac', args['TargetMac'], args['TargetMacNum'])

    # 构建arp SenderIp字段
    if 'SenderIp' not in args:
        args['SenderIp'] = '1.1.1.1'
    if 'SenderIpNum' not in args:
        args['SenderIpNum'] = '1'
    if 'SenderIpMode' not in args:
        args['SenderIpMode'] = 'classD'
    if 'SenderIpStep' not in args:
        args['SenderIpStep'] = '1'
    BuildIncrField('psrc', 'ip', args['SenderIp'], args['SenderIpNum'], args['SenderIpStep'], args['SenderIpMode'])

    # 构建arp TargetIp字段
    if 'TargetIp' not in args:
        args['TargetIp'] = '2.2.2.2'
    if 'TargetIpNum' not in args:
        args['TargetIpNum'] = '1'
    if 'TargetIpMode' not in args:
        args['TargetIpMode'] = 'classD'
    if 'TargetIpStep' not in args:
        args['TargetIpStep'] = '1'
    BuildIncrField('pdst', 'ip', args['TargetIp'], args['TargetIpNum'], args['TargetIpStep'], args['TargetIpMode'])

    dcnstream = dcnstream + ')'

    ##################################################################################


#
# BuildIPv4 :构建由python scapy发送的ipv4报文，如IP(....)
#
# args:  无
#
# return: 无
#
# addition:
#
# examples:
#     BuildIPv4(args)
# 脚本调用格式：
#     SetDsendStream(Port='2',StreamRateMode='pps',StreamRate='10', FrameSize='64', \
#		     SouMac='00-00-00-00-00-03',DesMac='00-00-00-00-00-04', \
#		     Protocl='ipv4',Tos='12',Fragment='2',TTL='240', \
#		     SouIp='10.1.1.1',SouIpNum='10',DesIp='20.1.1.1',DesIpNum='10')     
# ##################################################################################
def BuildIPv4(args):
    global dcnstream

    # 修改前面获取的Dot1Q()中的type字段为0x0800,如果前面是Dot3Tag,则需要增加len=0x0800
    if 'type=0xffff' in dcnstream:
        dcnstream = re.sub('0xffff', '0x0800', dcnstream)
    else:
        dcnstream = re.sub(',\)', ',len=0x0800)', dcnstream)
    dcnstream = dcnstream + '/IP('

    # 构建tos字段,tosh3存储tos的高三位的值即Ipprecedence的值
    if 'Ipprecedence' in args:
        tosh3 = int(args['Ipprecedence']) * 32
        if 'Tos' in args:
            tos = tosh3 + (int(args['Tos']) * 2)
        elif 'Dscp' in args:
            tos = int(args['Dscp']) * 4
        else:
            tos = tosh3
    elif 'Tos' in args:
        if 'Dscp' in args:
            tos = int(args['Dscp']) * 4
        else:
            tos = int(args['Tos'])
    elif 'Dscp' in args:
        tos = int(args['Dscp']) * 4
    else:
        tos = 0
    if tos > 0:
        dcnstream = dcnstream + 'tos=' + str(tos) + ','

    # 构建ip报头的长度值:TotalLength
    if 'LengthOverride' in args and 'TotalLength' in args:
        if 'true' in args['LengthOverride']:
            dcnstream = dcnstream + 'len=' + str(args['TotalLength']) + ','

    # 构建ip报头的fragment标志位
    if 'Fragment' in args or 'LastFragment' in args:
        if 'Fragment' not in args:
            args['Fragment'] = '0'
        if 'LastFragment' not in args:
            args['LastFragment'] = '0'
        fragment = int(args['Fragment']) * 2 + int(args['LastFragment'])
        dcnstream = dcnstream + 'flags=' + str(fragment) + ','

    # 构建ip报头的偏移量FragmentOffset
    if 'FragmentOffset' in args:
        dcnstream = dcnstream + 'frag=' + str(args['FragmentOffset']) + ','

    # 构建ip报头的ttl
    if 'TTL' in args:
        dcnstream = dcnstream + 'ttl=' + str(args['TTL']) + ','

    # 构建ip报头的自定义checksum
    if 'ValidChecksum' in args:
        if args['ValidChecksum'] == 'false':
            dcnstream = dcnstream + 'chksum=0,'

    # 构建ip报头源地址
    if 'SouIp' not in args:
        args['SouIp'] = '1.1.1.1'
    if 'SouIpNum' not in args:
        args['SouIpNum'] = '1'
    if 'SouClassMode' not in args:
        args['SouClassMode'] = 'classD'
    if 'SouIpStep' not in args:
        args['SouIpStep'] = '1'
    BuildIncrField('src', 'ip', args['SouIp'], args['SouIpNum'], args['SouIpStep'], args['SouClassMode'])

    # 构建ip报头目的地址
    if 'DesIp' not in args:
        args['DesIp'] = '2.2.2.2'
    if 'DesIpNum' not in args:
        args['DesIpNum'] = '1'
    if 'DesClassMode' not in args:
        args['DesClassMode'] = 'classD'
    if 'DesIpStep' not in args:
        args['DesIpStep'] = '1'
    BuildIncrField('dst', 'ip', args['DesIp'], args['DesIpNum'], args['DesIpStep'], args['DesClassMode'])

    # 构建ProtoclEx字段
    if 'ProtoclEx' in args:
        # 此处可以添加多种子协议报文，比如udp,tcp,icmp,dhcp,igmp等等
        if args['ProtoclEx'] == 'udp':
            dcnstream = dcnstream + ')'
            BuildUDP(args)
        elif args['ProtoclEx'] == 'tcp':
            dcnstream = dcnstream + ')'
            BuildTCP(args)

        #
        # 添加报文结束
        else:
            dcnstream = dcnstream + 'proto=' + args['ProtoclEx'] + ',)'
    else:
        dcnstream = dcnstream + ')'


        ##################################################################################


#
# BuildIPv6 :构建由于python scapy发送的ipv6报文，如IPv6(....)
#
# args:  无
#
# return: 无
#
# addition:
#
# examples:
#     BuildIPv6(args)
# 脚本调用格式：
#     SetDsendStream(Port='2',StreamRateMode='pps',StreamRate='10', FrameSize='64', \
#		     SouMac='00-00-00-00-00-03',DesMac='00-00-00-00-00-04', \
#		     Protocl='ipv6',TrafficClass='12',FlowLabel='10',HopLimit='20',NextHeader='58', \
#		     SouIpv6='2001::1',SouNumv6='10',DesIpv6='2002::1',DesNumv6='10')
# 注：以下参数中的值都是以十进制赋值，TrafficClass='12',FlowLabel='10',HopLimit='20',NextHeader='58',
###################################################################################
def BuildIPv6(args):
    global dcnstream
    global dcnincrlist
    global dcnincrnum

    # 修改前面获取的Dot1Q()中的type字段为0x0800,如果前面是Dot3Tag,则需要增加len=0x86dd
    if 'type=0xffff' in dcnstream:
        dcnstream = re.sub('0xffff', '0x86dd', dcnstream)
    else:
        dcnstream = re.sub(',\)', ',len=0x86dd)', dcnstream)
    dcnstream = dcnstream + '/IPv6('

    # 构建TrafficClass字段
    if 'TrafficClass' in args:
        dcnstream = dcnstream + 'tc=' + args['TrafficClass'] + ','

    # 构建FlowLabel字段
    if 'FlowLabel' in args:
        dcnstream = dcnstream + 'fl=' + args['FlowLabel'] + ','
    else:
        if 'Offset1' in args and args['Offset1'] == '20':
            if 'Value1' not in args:
                args['Value1'] = '0'
            value1 = '0x' + args['Value1']
            value1 = int(value1, 16)
            if 'Repeat1' not in args:
                args['Repeat1'] = '1'
            if 'Step1' not in args:
                args['Step1'] = '1'
            if args['Repeat1'] == '1':
                dcnstream = dcnstream + 'fl=' + str(value1) + ','
            else:
                dcnincrnum = dcnincrnum + 1
                dcnstream = dcnstream + 'fl=incrNum' + str(dcnincrnum) + '[incrCount],'
                strinfo = '--incrNum' + str(dcnincrnum) + ' ' + str(value1) + ',' + args['Repeat1']
                dcnincrlist.append(strinfo)

    # 构建HopLimit 字段
    if 'HopLimit' in args:
        dcnstream = dcnstream + 'hlim=' + args['HopLimit'] + ','

    # 构建NextHeader 字段
    if 'NextHeader' in args:
        dcnstream = dcnstream + 'nh=' + args['NextHeader'] + ','

    # 构建ipv6 源ipv6地址字段
    if 'SouIpv6' not in args:
        args['SouIpv6'] = '2003:0001:0002:0003:0000:0000:0000:0003'
    if 'SouNumv6' not in args:
        args['SouNumv6'] = '1'
    if 'SouStepv6' not in args:
        args['SouStepv6'] = '1'
    if 'SouAddrModev6' not in args:
        args['SouAddrModev6'] = '128'
    else:
        if args['SouAddrModev6'] == 'IncrHost':
            args['SouAddrModev6'] = '128'
    BuildIncrField('src', 'ipv6', args['SouIpv6'], args['SouNumv6'], args['SouStepv6'], args['SouAddrModev6'])

    # 构建ipv6 目的ipv6地址字段
    if 'DesIpv6' not in args:
        args['DesIpv6'] = '2003:0001:0002:0003:0000:0000:0000:0001'
    if 'DesNumv6' not in args:
        args['DesNumv6'] = '1'
    if 'DesStepv6' not in args:
        args['DesStepv6'] = '1'
    if 'DesAddrModev6' not in args:
        args['DesAddrModev6'] = '128'
    else:
        if args['DesAddrModev6'] == 'IncrHost':
            args['DesAddrModev6'] = '128'
    BuildIncrField('dst', 'ipv6', args['DesIpv6'], args['DesNumv6'], args['DesStepv6'], args['DesAddrModev6'])

    # 构建ProtoclEx字段
    if 'ProtoclEx' in args:
        # 此处可以添加多种子协议报文，比如udp,tcp,icmpv6,mld等等
        if args['ProtoclEx'] == 'udp':
            dcnstream = dcnstream + ')'
            BuildUDP(args)
        elif args['ProtoclEx'] == 'tcp':
            dcnstream = dcnstream + ')'
            BuildTCP(args)

        #
        # 添加报文结束
        else:
            dcnstream = dcnstream + 'nh=' + args['ProtoclEx'] + ')'
    else:
        if 'Offset1' in args and args['Offset1'] == '20':
            if 'Value1' in args:
                nh = '0x' + args['Value1']
                nh = int(nh, 16)
                dcnstream = dcnstream + 'nh=' + str(nh) + ','
            else:
                dcnstream = dcnstream + 'nh=0,'
        dcnstream = dcnstream + ')'



        ##################################################################################


#
# BuildIPv4OverIPv6 :构建由python scapy发送的ipv4 over ipv6 隧道报文，如IP(....)/IPv6()
#
# args:  无
#
# return: 无
#
# addition:
#
# examples:
#     BuildIPv4OverIPv6(args)
# 脚本调用格式：
#     SetDsendStream(Port='2',StreamRateMode='pps',StreamRate='10', FrameSize='128', \
#		   SouMac='00-00-00-00-00-03',DesMac='00-00-00-00-00-04', \
#		   Protocl='ipv6ipv4',Tos='12',Fragment='2', \
#		   SouIp='10.1.1.1',SouIpNum='10',DesIp='20.1.1.1',DesIpNum='10', \
#		   TrafficClass='12',FlowLabel='10', \
#		   SouIpv6='2001::1',SouNumv6='10',DesIpv6='2002::1',DesNumv6='10')
###################################################################################	   
def BuildIPv4OverIPv6(args):
    global dcnstream
    global dcnincrlist
    global dcnincrnum

    # 先构建外层ipv4报文头
    # 修改前面获取的Dot1Q()中的type字段为0x0800,如果前面是Dot3Tag,则需要增加len=0x0800
    if 'type=0xffff' in dcnstream:
        dcnstream = re.sub('0xffff', '0x0800', dcnstream)
    else:
        dcnstream = re.sub(',\)', ',len=0x0800)', dcnstream)
    dcnstream = dcnstream + '/IP('

    # 构建tos字段,tosh3存储tos的高三位的值即Ipprecedence的值
    if 'Ipprecedence' in args:
        tosh3 = int(args['Ipprecedence']) * 32
    else:
        tosh3 = 0
    if 'Tos' in args:
        tos = tosh3 + (int(args['Tos']) * 2)
    else:
        tos = tosh3
    if tos > 0:
        dcnstream = dcnstream + 'tos=' + str(tos) + ','

    # 构建ip报头的长度值:TotalLength
    if 'LengthOverride' in args and 'TotalLength' in args:
        if 'true' in args['LengthOverride']:
            dcnstream = dcnstream + 'len=' + str(args['TotalLength']) + ','

    # 构建ip报头的fragment标志位
    if 'Fragment' in args or 'LastFragment' in args:
        if 'Fragment' not in args:
            args['Fragment'] = '0'
        if 'LastFragment' not in args:
            args['LastFragment'] = '0'
        fragment = int(args['Fragment']) * 2 + int(args['LastFragment'])
        dcnstream = dcnstream + 'flags=' + str(fragment) + ','

    # 构建ip报头的偏移量FragmentOffset
    if 'FragmentOffset' in args:
        dcnstream = dcnstream + 'frag=' + str(args['FragmentOffset']) + ','

    # 构建ip报头的隧道报文协议类型
    dcnstream = dcnstream + 'proto=41,'

    # 构建ip报头的自定义checksum
    if 'ValidChecksum' in args:
        if args['ValidChecksum'] == 'false':
            dcnstream = dcnstream + 'chksum=0,'

    # 构建ip报头源地址
    if 'SouIp' not in args:
        args['SouIp'] = '1.1.1.1'
    if 'SouIpNum' not in args:
        args['SouIpNum'] = '1'
    if 'SouClassMode' not in args:
        args['SouClassMode'] = 'classD'
    if 'SouIpStep' not in args:
        args['SouIpStep'] = '1'
    BuildIncrField('src', 'ip', args['SouIp'], args['SouIpNum'], args['SouIpStep'], args['SouClassMode'])

    # 构建ip报头目的地址
    if 'DesIp' not in args:
        args['DesIp'] = '2.2.2.2'
    if 'DesIpNum' not in args:
        args['DesIpNum'] = '1'
    if 'DesClassMode' not in args:
        args['DesClassMode'] = 'classD'
    if 'DesIpStep' not in args:
        args['DesIpStep'] = '1'
    BuildIncrField('dst', 'ip', args['DesIp'], args['DesIpNum'], args['DesIpStep'], args['DesClassMode'])

    dcnstream = dcnstream + ')'

    # 构建内层ipv6报文头
    dcnstream = dcnstream + '/IPv6('

    # 构建TrafficClass字段
    if 'TrafficClass' in args:
        dcnstream = dcnstream + 'tc=' + args['TrafficClass'] + ','

    # 构建FlowLabel字段
    if 'FlowLabel' in args:
        dcnstream = dcnstream + 'fl=' + args['FlowLabel'] + ','
    else:
        if 'Offset1' in args and args['Offset1'] == '20':
            if 'Value1' not in args:
                args['Value1'] = '0'
            value1 = '0x' + args['Value1']
            value1 = int(value1, 16)
            if 'Repeat1' not in args:
                args['Repeat1'] = '1'
            if 'Step1' not in args:
                args['Step1'] = '1'
            if args['Repeat1'] == '1':
                dcnstream = dcnstream + 'fl=' + str(value1) + ','
            else:
                dcnincrnum = dcnincrnum + 1
                dcnstream = dcnstream + 'fl=incrNum' + str(dcnincrnum) + '[incrCount],'
                strinfo = '--incrNum' + str(dcnincrnum) + ' ' + str(value1) + ',' + args['Repeat1']
                dcnincrlist.append(strinfo)

    # 构建HopLimit 字段
    if 'HopLimit' in args:
        dcnstream = dcnstream + 'hlim=' + args['HopLimit'] + ','

    # 构建ipv6 源ipv6地址字段
    if 'SouIpv6' not in args:
        args['SouIpv6'] = '2003:0001:0002:0003:0000:0000:0000:0003'
    if 'SouNumv6' not in args:
        args['SouNumv6'] = '1'
    if 'SouStepv6' not in args:
        args['SouStepv6'] = '1'
    if 'SouAddrModev6' not in args:
        args['SouAddrModev6'] = '128'
    else:
        if args['SouAddrModev6'] == 'IncrHost':
            args['SouAddrModev6'] = '128'
    BuildIncrField('src', 'ipv6', args['SouIpv6'], args['SouNumv6'], args['SouStepv6'], args['SouAddrModev6'])

    # 构建ipv6 目的ipv6地址字段
    if 'DesIpv6' not in args:
        args['DesIpv6'] = '2003:0001:0002:0003:0000:0000:0000:0001'
    if 'DesNumv6' not in args:
        args['DesNumv6'] = '1'
    if 'DesStepv6' not in args:
        args['DesStepv6'] = '1'
    if 'DesAddrModev6' not in args:
        args['DesAddrModev6'] = '128'
    else:
        if args['DesAddrModev6'] == 'IncrHost':
            args['DesAddrModev6'] = '128'
    BuildIncrField('dst', 'ipv6', args['DesIpv6'], args['DesNumv6'], args['DesStepv6'], args['DesAddrModev6'])

    # 构建ProtoclEx字段
    if 'ProtoclEx' in args:
        # 此处可以添加多种子协议报文，比如udp,tcp,icmpv6,mld等等
        if args['ProtoclEx'] == 'udp':
            dcnstream = dcnstream + ')'
            BuildUDP(args)
        elif args['ProtoclEx'] == 'tcp':
            dcnstream = dcnstream + ')'
            BuildTCP(args)

        #
        # 添加报文结束
        else:
            dcnstream = dcnstream + 'nh=' + args['ProtoclEx'] + ')'
    else:
        if 'Offset1' in args and args['Offset1'] == '20':
            if 'Value1' in args:
                nh = '0x' + args['Value1']
                nh = int(nh, 16)
                dcnstream = dcnstream + 'nh=' + str(nh) + ','
            else:
                dcnstream = dcnstream + 'nh=0,'
        dcnstream = dcnstream + ')'


##################################################################################
#
# BuildUDP :构建由于python scapy发送的 udp报文头，如UDP(....)
#
# args:  无
#
# return: 无
#
# addition:
#
# examples:
#     BuildUDP(args)
# 脚本调用格式：
#     #ipv4 UDP报文，source port和destination port分别为12和22
#     SetDsendStream(Port='2',StreamMode='1',StreamRateMode='pps',StreamRate='10',NumFrames='50', \
#		   SouMac='00-00-00-0F-00-05',DesMac='00-00-00-0F-00-06', \
#		   Protocl='ipv4',ProtoclEx='udp', \	   
#		   SPort='12',DPort='22')
#     #ipv6 UDP报文，source port为从18开始递增10个，destination port为从15开始递增10个
#     SetDsendStream(Port='2',StreamMode='1',StreamRateMode='pps',StreamRate='10',NumFrames='50', \
#		   SouMac='00-00-00-0F-00-05',DesMac='00-00-00-0F-00-06', \
#		   Protocl='ipv6',ProtoclEx='udp', \
#		   Offset1='58',Value1='12',Repeat1='10', \
#		   Offset2='60',Value2='F',Repeat2='10')
###################################################################################
def BuildUDP(args):
    global dcnstream
    dportflag = '0'
    sportflag = '0'
    dcnstream = dcnstream + "/UDP("

    # 构造Dport字段
    if 'DPort' not in args:
        args['DPort'] = '0'

    if 'Offset2' in args or 'Offset1' in args:
        if 'Offset1' in args:
            # 如果dcnarrArgs(Offset1)为40则ipv4 udp Dport的值渐变
            if args['Offset1'] == '40':
                if 'Value1' not in args:
                    args['Value1'] == '0'
                value1 = '0x' + args['Value1']
                value1 = int(value1, 16)
                if 'Repeat1' not in args:
                    args['Repeat1'] == '1'
                BuildIncrField('dport', 'num', str(value1), args['Repeat1'])
                dportflag = '1'
            # 如果dcnarrArgs(Offset1)为60则ipv6 udp Dport的值渐变
            if args['Offset1'] == '60':
                if 'Value1' not in args:
                    args['Value1'] == '0'
                value1 = '0x' + args['Value1']
                value1 = int(value1, 16)
                if 'Repeat1' not in args:
                    args['Repeat1'] == '1'
                BuildIncrField('dport', 'num', str(value1), args['Repeat1'])
                dportflag = '1'
        if 'Offset2' in args:
            # 如果dcnarrArgs(Offset2)为40则ipv4 udp Dport的值渐变
            if args['Offset2'] == '40':
                if 'Value2' not in args:
                    args['Value2'] == '0'
                value2 = '0x' + args['Value2']
                value2 = int(value2, 16)
                if 'Repeat2' not in args:
                    args['Repeat2'] == '1'
                BuildIncrField('dport', 'num', str(value2), args['Repeat2'])
                dportflag = '1'
            # 如果dcnarrArgs(Offset2)为60则ipv6 udp Dport的值渐变
            if args['Offset2'] == '60':
                if 'Value2' not in args:
                    args['Value2'] == '0'
                value2 = '0x' + args['Value2']
                value2 = int(value2, 16)
                if 'Repeat2' not in args:
                    args['Repeat2'] == '1'
                BuildIncrField('dport', 'num', str(value2), args['Repeat2'])
                dportflag = '1'
    if dportflag == '0':
        if '-' in args['DPort']:
            Dinitvalue = (args['DPort'].split('-'))[0]
            Dfinalvalue = (args['DPort'].split('-'))[1]
            Dchangenum = int(Dfinalvalue) - int(Dinitvalue) + 1
            if Dchangenum <= 0:
                printRes('the Dport para is set to wrong value please check')
            BuildIncrField('dport', 'num', str(Dinitvalue), str(Dchangenum))
        else:
            dcnstream = dcnstream + 'dport=' + args['DPort'] + ','

    # 构造Sport字段
    if 'SPort' not in args:
        args['SPort'] = '0'
    if 'Offset2' in args or 'Offset1' in args:
        if 'Offset1' in args:
            # 如果dcnarrArgs(Offset1)为38则ipv4 udp Sport的值渐变
            if args['Offset1'] == '38':
                if 'Value1' not in args:
                    args['Value1'] == '0'
                value1 = '0x' + args['Value1']
                value1 = int(value1, 16)
                if 'Repeat1' not in args:
                    args['Repeat1'] == '1'
                BuildIncrField('sport', 'num', str(value1), args['Repeat1'])
                sportflag = '1'
            # 如果dcnarrArgs(Offset1)为58则ipv6 udp Dport的值渐变
            if args['Offset1'] == '58':
                if 'Value1' not in args:
                    args['Value1'] == '0'
                value1 = '0x' + args['Value1']
                value1 = int(value1, 16)
                if 'Repeat1' not in args:
                    args['Repeat1'] == '1'
                BuildIncrField('sport', 'num', str(value1), args['Repeat1'])
                sportflag = '1'
        if 'Offset2' in args:
            # 如果dcnarrArgs(Offset2)为38则ipv4 udp Dport的值渐变
            if args['Offset2'] == '38':
                if 'Value2' not in args:
                    args['Value2'] == '0'
                value2 = '0x' + args['Value2']
                value2 = int(value2, 16)
                if 'Repeat2' not in args:
                    args['Repeat2'] == '1'
                BuildIncrField('dport', 'num', str(value2), args['Repeat2'])
                sportflag = '1'
            # 如果dcnarrArgs(Offset2)为58则ipv6 udp Dport的值渐变
            if args['Offset2'] == '58':
                if 'Value2' not in args:
                    args['Value2'] == '0'
                value2 = '0x' + args['Value2']
                value2 = int(value2, 16)
                if 'Repeat2' not in args:
                    args['Repeat2'] == '1'
                BuildIncrField('dport', 'num', str(value2), args['Repeat2'])
                sportflag = '1'
    if sportflag == '0':
        if '-' in args['SPort']:
            Sinitvalue = (args['SPort'].split('-'))[0]
            Sfinalvalue = (args['SPort'].split('-'))[1]
            Schangenum = int(Sfinalvalue) - int(Sinitvalue) + 1
            if Dchangenum <= 0:
                printRes('the SPort para is set to wrong value please check')
            BuildIncrField('sport', 'num', str(Dinitvalue), str(Dchangenum))
        else:
            dcnstream = dcnstream + 'sport=' + args['SPort'] + ','

    dcnstream = dcnstream + ')'


##################################################################################
#
# BuildTCP :构建由于python scapy发送的 tcp报文头，如TCP(....)
#
# args:  无
#
# return: 无
#
# addition:
#
# examples:
#     BuildTCP(args)
# 脚本调用格式：
#    #ipv4 UDP报文，source port和destination port分别为12和22
#    SetDsendStream(Port='2',StreamMode='1',StreamRateMode='pps',StreamRate='10',NumFrames='50', \
#		   SouMac='00-00-00-0F-00-05',DesMac='00-00-00-0F-00-06', \
#		   Protocl='ipv4',ProtoclEx='tcp', \
#		   SPort='12',DPort='22', \
#		   SequenceNum='22',PSH='true',ACK='false',URG='true',RST='true',SYN='false',FIN='true')
#
#    #ipv6 UDP报文，source port为从18开始递增10个，destination port为从15开始递增10个
#    SetDsendStream(Port='2',StreamMode='1',StreamRateMode='pps',StreamRate='10',NumFrames='50', \
#		   SouMac='00-00-00-0F-00-05',DesMac='00-00-00-0F-00-06', \
#		   Protocl='ipv6',ProtoclEx='tcp', \
#		   Offset1='58',Value1='12',Repeat1='10', \
#		   Offset2='60',Value2='f',Repeat2='10', \
#		   SequenceNum='22',PSH='true',ACK='false',URG='true',RST='true',SYN='false',FIN='true')		   
###################################################################################
def BuildTCP(args):
    global dcnstream
    dportflag = '0'
    sportflag = '0'
    dcnstream = dcnstream + "/TCP("

    # 构造Dport字段
    if 'DPort' not in args:
        args['DPort'] = '0'

    if 'Offset2' in args or 'Offset1' in args:
        if 'Offset1' in args:
            # 如果dcnarrArgs(Offset1)为36则ipv4 udp Dport的值渐变
            if args['Offset1'] == '36':
                if 'Value1' not in args:
                    args['Value1'] == '0'
                value1 = '0x' + args['Value1']
                value1 = int(value1, 16)
                if 'Repeat1' not in args:
                    args['Repeat1'] == '1'
                BuildIncrField('dport', 'num', str(value1), args['Repeat1'])
                dportflag = '1'
            # 如果dcnarrArgs(Offset1)为60则ipv6 udp Dport的值渐变
            if args['Offset1'] == '60':
                if 'Value1' not in args:
                    args['Value1'] == '0'
                value1 = '0x' + args['Value1']
                value1 = int(value1, 16)
                if 'Repeat1' not in args:
                    args['Repeat1'] == '1'
                BuildIncrField('dport', 'num', str(value1), args['Repeat1'])
                dportflag = '1'
        if 'Offset2' in args:
            # 如果dcnarrArgs(Offset2)为36则ipv4 udp Dport的值渐变
            if args['Offset2'] == '36':
                if 'Value2' not in args:
                    args['Value2'] == '0'
                value2 = '0x' + args['Value2']
                value2 = int(value2, 16)
                if 'Repeat2' not in args:
                    args['Repeat2'] == '1'
                BuildIncrField('dport', 'num', str(value2), args['Repeat2'])
                dportflag = '1'
            # 如果dcnarrArgs(Offset2)为60则ipv6 udp Dport的值渐变
            if args['Offset2'] == '60':
                if 'Value2' not in args:
                    args['Value2'] == '0'
                value2 = '0x' + args['Value2']
                value2 = int(value2, 16)
                if 'Repeat2' not in args:
                    args['Repeat2'] == '1'
                BuildIncrField('dport', 'num', str(value2), args['Repeat2'])
                dportflag = '1'
    if dportflag == '0':
        if '-' in args['DPort']:
            Dinitvalue = (args['DPort'].split('-'))[0]
            Dfinalvalue = (args['DPort'].split('-'))[1]
            Dchangenum = int(Dfinalvalue) - int(Dinitvalue) + 1
            if Dchangenum <= 0:
                printRes('the Dport para is set to wrong value please check')
            BuildIncrField('dport', 'num', str(Dinitvalue), str(Dchangenum))
        else:
            dcnstream = dcnstream + 'dport=' + args['DPort'] + ','

    # 构造Sport字段
    if 'SPort' not in args:
        args['SPort'] = '0'
    if 'Offset2' in args or 'Offset1' in args:
        if 'Offset1' in args:
            # 如果dcnarrArgs(Offset1)为34则ipv4 udp Sport的值渐变
            if args['Offset1'] == '34':
                if 'Value1' not in args:
                    args['Value1'] == '0'
                value1 = '0x' + args['Value1']
                value1 = int(value1, 16)
                if 'Repeat1' not in args:
                    args['Repeat1'] == '1'
                BuildIncrField('sport', 'num', str(value1), args['Repeat1'])
                sportflag = '1'
            # 如果dcnarrArgs(Offset1)为58则ipv6 udp Dport的值渐变
            if args['Offset1'] == '58':
                if 'Value1' not in args:
                    args['Value1'] == '0'
                value1 = '0x' + args['Value1']
                value1 = int(value1, 16)
                if 'Repeat1' not in args:
                    args['Repeat1'] == '1'
                BuildIncrField('sport', 'num', str(value1), args['Repeat1'])
                sportflag = '1'
        if 'Offset2' in args:
            # 如果dcnarrArgs(Offset2)为34则ipv4 udp Dport的值渐变
            if args['Offset2'] == '34':
                if 'Value2' not in args:
                    args['Value2'] == '0'
                value2 = '0x' + args['Value2']
                value2 = int(value2, 16)
                if 'Repeat2' not in args:
                    args['Repeat2'] == '1'
                BuildIncrField('dport', 'num', str(value2), args['Repeat2'])
                sportflag = '1'
            # 如果dcnarrArgs(Offset2)为58则ipv6 udp Dport的值渐变
            if args['Offset2'] == '58':
                if 'Value2' not in args:
                    args['Value2'] == '0'
                value2 = '0x' + args['Value2']
                value2 = int(value2, 16)
                if 'Repeat2' not in args:
                    args['Repeat2'] == '1'
                BuildIncrField('dport', 'num', str(value2), args['Repeat2'])
                sportflag = '1'
    if sportflag == '0':
        if '-' in args['SPort']:
            Sinitvalue = (args['SPort'].split('-'))[0]
            Sfinalvalue = (args['SPort'].split('-'))[1]
            Schangenum = int(Sfinalvalue) - int(Sinitvalue) + 1
            if Dchangenum <= 0:
                printRes('the SPort para is set to wrong value please check')
            BuildIncrField('sport', 'num', str(Dinitvalue), str(Dchangenum))
        else:
            dcnstream = dcnstream + 'sport=' + args['SPort'] + ','

    # 构造SequenceNum字段
    if 'SequenceNum' in args:
        dcnstream = dcnstream + 'seq=' + args['SequenceNum'] + ','

        # 构造FlagsField字段
    # 计算FIN
    if 'FIN' in args:
        if 'true' in args['FIN']:
            fin = '1'
        else:
            if args['FIN'] == 'false':
                fin = '0'
            else:
                printRes('the para FIN value is wrong.')
    else:
        fin = '0'

    # 计算SYN
    if 'SYN' in args:
        if 'true' in args['SYN']:
            syn = '2'
        else:
            if args['SYN'] == 'false':
                syn = '0'
            else:
                printRes('the para SYN value is wrong.')
    else:
        syn = '0'

    # 计算RST
    if 'RST' in args:
        if 'true' in args['RST']:
            rst = '4'
        else:
            if args['RST'] == 'false':
                rst = '0'
            else:
                printRes('the para RST value is wrong.')
    else:
        rst = '0'

    # 计算PSH
    if 'PSH' in args:
        if 'true' in args['PSH']:
            psh = '8'
        else:
            if args['PSH'] == 'false':
                psh = '0'
            else:
                printRes('the para PSH value is wrong.')
    else:
        psh = '0'

    # 计算ACK
    if 'ACK' in args:
        if 'true' in args['ACK']:
            ack = '16'
        else:
            if args['ACK'] == 'false':
                ack = '0'
            else:
                printRes('the para ACK value is wrong.')
    else:
        ack = '0'

    # 计算URG
    if 'URG' in args:
        if 'true' in args['URG']:
            urg = '32'
        else:
            if args['URG'] == 'false':
                urg = '0'
            else:
                printRes('the para URG value is wrong.')
    else:
        urg = '0'

    tcpflags = int(ack) + int(fin) + int(psh) + int(rst) + int(syn) + int(urg)
    tcpflags = hex(tcpflags)
    if tcpflags != '0x2':
        dcnstream = dcnstream + 'flags=' + tcpflags + ','
    dcnstream = dcnstream + ')'


############### Dsend tools  ############################


##################################################################################
#
# ConnectDsend :连接发包工具服务器
#
# args:  
#    host: 发包工具服务器ip地址
#    port: 连接服务器的端口号，默认为11918
#
# return: 连接成功返回0
#
# addition:
#
# examples:
#     ConnectDsend('172.16.1.43')
#
###################################################################################
def ConnectDsend(host, port=11918):
    res = Dconn(host, port)
    return res


##################################################################################
#
# DisconnectDsend :断开连接发包工具服务器
#
# args:  
#
# return: 断开成功返回0
#
# addition:
#
# examples:
#     DisconnectDsend()
#
###################################################################################
def DisconnectDsend():
    res = Ddisconn()
    return res


##################################################################################
#
# StartTransmit :开始发包
#
# args:  
#    port: 发包的端口
#
# return: 发包成功返回0
#
# addition:
#
# examples:
#     StartTransmit('6','7')
#
###################################################################################
def StartTransmit(*args):
    res = 0
    for port in args:
        resx = Dsend(" --port " + str(port) + " --proc startTransmit")
        res = int(res) + int(resx)
    return res


##################################################################################
#
# StartTransmit :停止发包
#
# args:  
#    port: 停止发包的端口
#
# return: 停止成功返回0
#
# addition:
#
# examples:
#     StopTransmit('6','7')
#
###################################################################################
def StopTransmit(*args):
    res = 0
    for port in args:
        resx = Dsend(" --port " + str(port) + " --proc stopTransmit")
        res = int(res) + int(resx)
    return res


##############################################################################################################################
#
# SetDsendDefault :发包工具的端口恢复默认值：停止发包、清空端口统计、重设端口。
#
# args: 
#      port1:端口1
#      port2:端口2
#      可变个数的端口
#
# return: 
#       
#
# addition:
#
# examples:
#     SetDsendDefault('2','3')
#
###############################################################################################################################
def SetDsendDefault(*args):
    for port in args:
        Dsend("--port " + str(port) + " --proc stopTransmit")
        Dsend("--proc clearStatistic" + " --port " + str(port))
        Dsend("--proc resetPortState" + " --port " + str(port))
    time.sleep(15)


##################################################################################
# 函数名  :ClearDsendPortStats
# 功能描述:清除某一个或几个端口的统计值
# return: 
#
# 函数结果:
# 举例:ClearDsendPortStats('2','3')
################################################################################
def ClearDsendPortStats(*args):
    for port in args:
        Dsend("--port " + str(port) + " --proc stopTransmit")
        Dsend("--proc clearStatistic" + " --port " + str(port))


##################################################################################
#
# CheckDsendStreamSentReceive :检查端口收发包的比例
#
# args: 
#     port1:端口1
#     port2:端口2
#     num:要求的比例(port1发送的速率/port2收到的速率)
#
# return: 
#       1 :不符合要求
#       0 :符合要求
#
# addition:
#
# examples:
#     CheckDsendStreamSentReceive('2','3','1')
#
###################################################################################
def CheckDsendStreamSentReceive(port1, port2, num, waittimer=10):
    time.sleep(2)

    for i in range(10):
        rate1 = Dshow("--port " + str(port1) + " --type packetSendRate")
        if rate1 == '0':
            time.sleep(0.1)
            if i == 9:
                print('!start transmit error!')
                return 1
            else:
                continue
        else:
            break

    for j in range(10):
        rate2 = Dshow("--port " + str(port2) + " --type packetReceiveRate")
        rate1 = Dshow("--port " + str(port1) + " --type packetSendRate")
        # if判断是否有连接错误，防止abs处跳出
        if rate1 == 'ERROR: timed out' or rate2 == 'ERROR: timed out':
            rate1 = '0'
            rate2 = '0'

        rate1 = re.sub(',', '', rate1)
        rate2 = re.sub(',', '', rate2)
        print(rate1)
        print(rate2)

        if num == '0':
            if rate1 == rate2:
                if j == 9:
                    strinfo1 = 'The port ' + port1 + ' sent Frames rate is : ' + rate1
                    strinfo2 = 'The port ' + port2 + ' sent Frames rate is : ' + rate2
                    print(strinfo1)
                    print(strinfo2)
                    return 1
                else:
                    time.sleep(waittimer)
                    continue
            else:
                num2 = abs((float(rate1) / (float(rate1) - float(rate2)) - 1) / 1)
        else:
            num2 = abs((float(rate1) / (float(rate2) + 0.1) - float(num)) / float(num))

        if num2 <= 0.05:
            strinfo1 = 'The port ' + port1 + ' sent Frames rate is : ' + rate1
            strinfo2 = 'The port ' + port2 + ' received Frames rate is : ' + rate2
            print(strinfo1)
            print(strinfo2)
            return 0
        else:
            if j == 9:
                strinfo1 = 'The port ' + port1 + ' sent Frames rate is : ' + rate1
                strinfo2 = 'The port ' + port2 + ' received Frames rate is : ' + rate2
                print(strinfo1)
                print(strinfo2)
                return 1
            else:
                time.sleep(waittimer)
                continue


######################################################################
#
# CheckDsendFrameReceivedNumber:  获取某端口收包的统计数量
#
#
#
# args:
#     port:需要检查的端口
#  
# addition:
#     成功：返回 收到包的数量
#     失败：返回 0 
# examples:
#     CheckDsendFrameReceivedNumber('3')
######################################################################
def CheckDsendFrameReceivedNumber(port):
    count = Dshow("--port " + str(port) + " --type packetReceiveNum")
    strinfo = 'successful get FramesReceivedNumber:' + str(count)
    print(strinfo)
    return int(count)


######################################################################
# CheckDsendFrameSentNumber:  获取某端口发包的统计数量
#					 
#
# args:
#     port:需要检查的端口对应的port
#  
# addition:
#     成功：返回 收到包的数量
#     失败：返回 0 
# examples:
#     CheckDsendFrameSentNumber('2')
######################################################################
def CheckDsendFrameSentNumber(port):
    count = Dshow("--port " + str(port) + " --type packetSendNum")
    strinfo = 'The sent frames counter of port ' + port + ' is: ' + str(count)
    print(strinfo)
    return int(count)


##############################################################################################
#
# CheckDsendPacketsReceiveRate :查看端口收报速率是否符合预期速率，提供误差参数
#
# args:
#     port:收包端口
#     rate:预期的收报速率（pps）
#     pianyi:可以接受的误差
# 
# return:
#     0,符合预期
#     1，不符合预期
# examples:
#    CheckDsendPacketsReceiveRate('3','1000')
#############################################################################################
def CheckDsendPacketsReceiveRate(port, rate, pianyi='0.05'):
    rate1 = Dshow("--port " + str(port) + " --type packetReceiveRate")
    strinfo = 'The reciever frames rate of ' + str(port) + ' is ' + rate1
    if rate == '0':
        if rate1 == '0':
            return 0
        else:
            return 1
    else:
        rate2 = abs(float(rate1) - float(rate)) / float(rate)
        if float(rate2) <= float(pianyi):
            return 0
        else:
            return 1


######################################################################
#
# CheckDsendBytesReceivedRate:  获取某端口收包的字节速率
#
#
#
# args:
#     port:需要检查的端口
#  
# addition:
#     成功：返回 收字节速率
#     失败：返回 0 
# examples:
#     CheckDsendBytesReceivedRate('3')
######################################################################
def CheckDsendBytesReceivedRate(port):
    count = Dshow("--port " + str(port) + " --type byteReceiveRate")
    strinfo = 'successful get byteReceiveRate: ' + str(count)
    print(strinfo)
    return int(count)


######################################################################
#
# CheckDsendBytesSendRate:  获取某端口发包的字节速率
#
#
#
# args:
#     port:需要检查的端口
#  
# addition:
#     成功：返回 发送字节速率
#     失败：返回 0 
# examples:
#     CheckDsendBytesSendRate('3')
######################################################################
def CheckDsendBytesSendRate(port):
    count = Dshow("--port " + str(port) + " --type byteSendRate")
    strinfo = 'successful get byteSendRate: ' + str(count)
    print(strinfo)
    return int(count)


######################################################################
#
# CheckDsendSendOver: 查询端口发包是否发送完毕，发送完毕返回0，否则返回1
#
# return: 
#       发送完毕返回0
#       未发送完毕返回1
# examples:
#           CheckDsendSendOver('2')
######################################################################
def CheckDsendSendOver(*args):
    res = 0
    for port in args:
        resx = Dsend("--port " + str(port) + " --proc getSendState")
        res = int(res) + int(resx)
    return res


##---------------------------------抓包相关函数------------------------------------##

######################################################################
#
# StartDsendCapture: 开始抓包函数，针对自动发包工具
#
# return: 开始抓包操作成功返回0
# 
# examples:
#           StartDsendCapture('2','3')
######################################################################
def StartDsendCapture(*args):
    res = 0
    for port in args:
        resx = Dcapture("--port " + str(port) + " --proc startCapture")
        res = int(res) + int(resx)
    return res


######################################################################
#
# StopDsendCapture: 停止抓包函数,针对自动发包工具（该函数会打印抓到的包的个数）
#
# return: 停止抓包操作成功返回0
# 
# examples:
#           StopDsendCapture('2','3')
######################################################################
def StopDsendCapture(*args):
    res = 0
    for port in args:
        resx = Dcapture("--port " + str(port) + " --proc stopCapture")
        pktnum = Dcapture("--port " + str(port) + " --proc getCaptureBuffer --fid count")
        print(pktnum)
        res = int(res) + int(resx)
    return res


######################################################################
#
# CheckDsendCaptureStream: 检查抓到的流是否满足要求
#
# args:
#           
#           port:   抓包端口
#           Srcmac: 源mac
#           Dstmac: 目的mac
#           Srcip: source ip
#           Dstip: destination ip
#           VlanTag:
#                   取值 -1 不带tag,0 不关心带不带tag>0 要求带的tag
#           Cos :   user priority
#	       FragmentFlag: 取值 1 表示数据包分片，0 表示数据包不分片
#	       TotalLength：IP数据包的总长度（包括IP头和数据部分）
#
# return: 
#      成功：返回满足条件的报文个数
#      失败：返回0
# 
# examples:
#           CheckDsendCaptureStream('2',SrcMac='00-00-00-00-00-03')
#
#########################################################################################################
def CheckDsendCaptureStream(port, **args):
    counter = 0
    # Get the number of frames captured
    numFrames = Dcapture("--port " + port + " --proc getCaptureBuffer --fid count")

    if not numFrames:
        print('capture no packet,please check')
        return 0

    if 'Num' in args:
        checknum = int(args['Num'])
    else:
        checknum = 1000

    # Limit the number of checked packets to 1000
    if int(numFrames) > int(checknum):
        numFrames = str(checknum)

    checknum = int(numFrames)
    character = ''
    # pak是自定义的一个字符串，是为了与python后台交互。在numFrames后面跟一个pak字符串，后台就会识别为输出全部的抓包数据（最大1000个）
    numFrames = str(numFrames) + 'pak'
    capturebuffer = Dcapture("--port " + port + " --proc getCaptureBuffer --fid " + numFrames)

    for i in range(checknum):
        # Note that the frame number starts at 1
        # Get the actual frame data 
        data = capturebuffer[i]
        if data == '':
            continue
        ret = 1

        ################# 添加各个需要检查的报文或字段 ###############

        # SrcMac
        if 'SrcMac' in args:
            ret = ret * CheckSrcMacInData(args['SrcMac'], data)
            if i == 1:
                character = character + ' SrcMac ' + str(args['SrcMac'])

        # DstMac
        if 'DstMac' in args:
            ret = ret * CheckDstMacInData(args['DstMac'], data)
            if i == 1:
                character = character + ' DstMac ' + str(args['DstMac'])

        # SrcIp
        if 'SrcIp' in args:
            ret = ret * CheckSrcIpInData(args['SrcIp'], data)
            if i == 1:
                character = character + ' SrcIp ' + str(args['SrcIp'])

        # DstIp
        if 'DstIp' in args:
            ret = ret * CheckDstIpInData(args['DstIp'], data)
            if i == 1:
                character = character + ' DstIp ' + str(args['DstIp'])

        # SrcIpv6
        if 'SrcIpv6' in args:
            ret = ret * CheckSrcIpv6InData(args['SrcIpv6'], data)
            if i == 1:
                character = character + ' SrcIpv6 ' + str(args['SrcIpv6'])

        # DstIpv6
        if 'DstIpv6' in args:
            ret = ret * CheckDstIpv6InData(args['DstIpv6'], data)
            if i == 1:
                character = character + ' DstIpv6 ' + str(args['DstIpv6'])

        # Tpid
        if 'Tpid' in args:
            ret = ret * CheckTpidInData(args['Tpid'], data)
            if i == 1:
                character = character + ' Tpid ' + str(args['Tpid'])

        # VlanTag
        if 'VlanTag' in args:
            ret = ret * CheckVlanTagInData(args['VlanTag'], data)
            if i == 1:
                character = character + ' VlanTag ' + str(args['VlanTag'])

        # Length
        if 'Length' in args:
            ret = ret * CheckLengthOfData(args['Length'], data)
            if i == 1:
                character = character + ' Length ' + str(args['Length'])

        # Cos
        if 'Cos' in args:
            ret = ret * CheckCosInData(args['Cos'], data)
            if i == 1:
                character = character + ' Cos ' + str(args['Cos'])

        # Arp
        if 'Arp' in args:
            ret = ret * CheckArpInData(args['Arp'], data)
            if i == 1:
                character = character + ' Arp '

        # ArpType
        if 'ArpType' in args:
            ret = ret * CheckArpTypeInData(args['ArpType'], data)
            if i == 1:
                character = character + ' ArpType ' + str(args['ArpType'])

        # ArpSenderHardwareAddress
        if 'ArpSenderHardwareAddress' in args:
            ret = ret * CheckArpSenderHardwareAddressInData(args['ArpSenderHardwareAddress'], data)
            if i == 1:
                character = character + ' ArpSenderHardwareAddress ' + str(args['ArpSenderHardwareAddress'])

        # ArpSenderProtocolAddress
        if 'ArpSenderProtocolAddress' in args:
            ret = ret * CheckArpSenderProtocolAddressInData(args['ArpSenderProtocolAddress'], data)
            if i == 1:
                character = character + ' ArpSenderProtocolAddress ' + str(args['ArpSenderProtocolAddress'])

        # ArpTargetHardwareAddress
        if 'ArpTargetHardwareAddress' in args:
            ret = ret * CheckArpTargetHardwareAddressInData(args['ArpTargetHardwareAddress'], data)
            if i == 1:
                character = character + ' ArpTargetHardwareAddress ' + str(args['ArpTargetHardwareAddress'])

        # ArpTargetProtocolAddress
        if 'ArpTargetProtocolAddress' in args:
            ret = ret * CheckArpTargetProtocolAddressInData(args['ArpTargetProtocolAddress'], data)
            if i == 1:
                character = character + ' ArpTargetProtocolAddress ' + str(args['ArpTargetProtocolAddress'])




                ######  添加报文结束 #####

        if ret != 0:
            counter = counter + 1
            # else:
            # print ''

    strinfo = 'Check capture packets on ' + str(port) + ' with ' + character + ' is ' + str(counter)
    print(strinfo)
    return counter


#######################################################
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
def CheckSrcMacInData(srcmac, data):
    # Get source mac from data
    data = data[18:35]
    data = re.sub(' ', '-', data)
    srcmac = srcmac.upper()
    if srcmac == data:
        return 1
    else:
        return 0


#######################################################
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
# examples:
#           CheckDsendCaptureStream('2',DstMac='00-00-00-00-00-03')
########################################################## 
def CheckDstMacInData(dstmac, data):
    # Get destination mac from data
    data = data[0:17]
    data = re.sub(' ', '-', data)
    dstmac = dstmac.upper()
    if dstmac == data:
        return 1
    else:
        return 0


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
# examples:
#           CheckDsendCaptureStream('2',SrcIp='1.1.1.1')
########################################################## 
def CheckSrcIpInData(srcip, data):
    vlanflag = data[36:41]
    if vlanflag == '81 00':
        data = data[90:101]
    else:
        data = data[78:89]
    n1 = data[0:2]
    n2 = data[3:5]
    n3 = data[6:8]
    n4 = data[9:11]
    num1 = '0x' + str(n1)
    num1 = int(num1, 16)
    num2 = '0x' + str(n2)
    num2 = int(num2, 16)
    num3 = '0x' + str(n3)
    num3 = int(num3, 16)
    num4 = '0x' + str(n4)
    num4 = int(num4, 16)
    ipstr = str(num1) + '.' + str(num2) + '.' + str(num3) + '.' + str(num4)
    if srcip == ipstr:
        return 1
    else:
        return 0


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
# examples:
#           CheckDsendCaptureStream('2',DstIp='2.2.2.2')
##########################################################  
def CheckDstIpInData(dstip, data):
    vlanflag = data[36:41]
    if vlanflag == '81 00':
        data = data[102:113]
    else:
        data = data[90:101]
    n1 = data[0:2]
    n2 = data[3:5]
    n3 = data[6:8]
    n4 = data[9:11]
    num1 = '0x' + str(n1)
    num1 = int(num1, 16)
    num2 = '0x' + str(n2)
    num2 = int(num2, 16)
    num3 = '0x' + str(n3)
    num3 = int(num3, 16)
    num4 = '0x' + str(n4)
    num4 = int(num4, 16)
    ipstr = str(num1) + '.' + str(num2) + '.' + str(num3) + '.' + str(num4)
    if dstip == ipstr:
        return 1
    else:
        return 0



        #######################################################


#
# CheckSrcIpv6InData :检查抓到的流source ipv6是否满足镜像的要求
#
#   args:
#                srcipv6: source ipv6
#                data: actual frame data
#
#   return: 
#                1 :满足要求
#                0:不满足要求
# examples:
#           CheckDsendCaptureStream('2',SrcIpv6='2001::1')
##########################################################  
def CheckSrcIpv6InData(srcipv6, data):
    vlanflag = data[36:41]
    if vlanflag == '81 00':
        data = data[78:126]
    else:
        data = data[66:114]
    data = re.sub(' ', '', data)
    n1 = data[0:4]
    n2 = data[4:8]
    n3 = data[8:12]
    n4 = data[12:16]
    n5 = data[16:20]
    n6 = data[20:24]
    n7 = data[24:28]
    n8 = data[28:32]
    ipv6str = str(n1) + ':' + str(n2) + ':' + str(n3) + ':' + str(n4) + ':' + str(n5) + ':' + str(n6) + ':' + str(
        n7) + ':' + str(n8)
    srcipv6 = FormatIpv6(srcipv6)
    srcipv6 = srcipv6.upper()
    if srcipv6 == ipv6str:
        return 1
    else:
        return 0


#######################################################
#
# CheckDstIpv6InData :检查抓到的流destination ipv6是否满足镜像的要求
#
#   args:
#                dstipv6: destination ipv6
#                data: actual frame data
#
#   return: 
#                1 :满足要求
#                0:不满足要求
# examples:
#           CheckDsendCaptureStream('2',DstIpv6='2001::2')
##########################################################
def CheckDstIpv6InData(dstipv6, data):
    vlanflag = data[36:41]
    if vlanflag == '81 00':
        data = data[126:173]
    else:
        data = data[114:161]
    data = re.sub(' ', '', data)
    n1 = data[0:4]
    n2 = data[4:8]
    n3 = data[8:12]
    n4 = data[12:16]
    n5 = data[16:20]
    n6 = data[20:24]
    n7 = data[24:28]
    n8 = data[28:32]
    ipv6str = str(n1) + ':' + str(n2) + ':' + str(n3) + ':' + str(n4) + ':' + str(n5) + ':' + str(n6) + ':' + str(
        n7) + ':' + str(n8)
    dstipv6 = FormatIpv6(dstipv6)
    dstipv6 = dstipv6.upper()
    if dstipv6 == ipv6str:
        return 1
    else:
        return 0


# 调用格式：FormatIpv6('2000::1') ==>2000:0000:0000:0000:0000:0000:0000:0001
def FormatIpv6(ipv6):
    if ipv6[0:2] == '::':
        ipv6 = re.sub(ipv6[0:2], '0::', ipv6)
    if ipv6[(len(ipv6) - 2):len(ipv6)] == '::':
        ipv6 = str(ipv6) + '0'
    ipv6length = len(ipv6)
    count = 0
    for i in range(ipv6length):
        tempchar = ipv6[i]
        if tempchar == ':':
            count = count + 1

    flag = ipv6.find('::')
    if flag == -1:
        result = Format4bit(ipv6)
    else:
        bitnum = (7 - count) + 1
        ipv6temp = ipv6[0:flag]
        for j in range(bitnum):
            ipv6temp = ipv6temp + ':0'
        tempipv6 = ipv6[(flag + 1):len(ipv6)]
        ipv6temp = ipv6temp + tempipv6
        result = Format4bit(ipv6temp)
    return result


# 将ipv6地址的每一个字段变为4字符宽度
def Format4bit(ipv6):
    templist = ipv6.split(':')
    length = len(templist)
    result = ''
    for i in range(length):
        tempipv6 = templist[i]
        tempipv6 = '0x' + str(tempipv6)
        tempipv6 = int(tempipv6, 16)
        tempipv6 = '%04X' % tempipv6
        n = length - 1
        if i == n:
            result = result + tempipv6
        else:
            result = result + tempipv6 + ':'
    return result


#######################################################
#
# CheckTpidInData :检查抓到的流vlan tpid是否满足镜像的要求
#
#   args:
#                vlantag: vlan tpid
#                data: actual frame data
#
#   return: 
#                1 :满足要求
#                0:不满足要求
#   eg:
# CheckDsendCaptureStream('2',Tpid=['81','91'])
# CheckDsendCaptureStream('2',Tpid=['81'])
# Tpid取一个值，则仅判断报文第一层Tpid;Tpid取两个值，第一个值为外层Tpid值，第二个值为内层Tpid的值
# 当Tpid值为8100或9100时，判断时只取81或91，即对前两位判断
#
##########################################################
def CheckTpidInData(Tpid, data):
    if len(Tpid) == 1:
        data = data[36:38]
        if Tpid[0] == data:
            return 1
        else:
            return 0
    if len(Tpid) == 2:
        outtpid = Tpid[0]
        intpid = Tpid[1]
        outdata = data[36:38]
        indata = data[48:50]
        if outtpid == outdata and intpid == indata:
            return 1
        else:
            return 0


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
# CheckDsendCaptureStream('2',VlanTag=['100','10'])
# CheckDsendCaptureStream('2',VlanTag=['100'])
# VlanTag取一个值，则仅判断报文第一层Tag;VlanTag取两个值，第一个值为外层Tag值，第二个值为内层Tag的值
# 取值为-1，表示没有VlanTag;取值为0，表示不关心是否有VlanTag;取值为>0，表示要求有VlanTag，该值为Vid
#
##########################################################
def CheckVlanTagInData(vlantag, data):
    if len(vlantag) == 1:
        if int(vlantag[0]) == 0:
            # VlanTag为0，不关心是否有Tag
            return 1
        if int(vlantag[0]) > 0:
            # VlanTag>0，对报文进行判断
            if data[36:41] == '81 00':
                temp = data[43:47]
                temp = re.sub(' ', '', temp)
                temp = '0x' + temp
                temp = int(temp, 16)
                if int(vlantag[0]) == temp:
                    return 1
        if vlantag[0] == '-1':
            # VlanTag为-1，报文不存在Tag
            if data[36:41] != '81 00':
                return 1
    elif len(vlantag) > 2:
        # 判断三层tag
        outtag = vlantag[0]
        intag = vlantag[1]
        intag1 = vlantag[2]
        # 最外层
        temp = data[43:47]
        temp = re.sub(' ', '', temp)
        temp = '0x' + temp
        temp = int(temp, 16)
        # 第二层
        tmp = data[55:59]
        tmp = re.sub(' ', '', tmp)
        tmp = '0x' + tmp
        tmp = int(tmp, 16)
        # 第三层
        tmp1 = data[67:71]
        tmp1 = re.sub(' ', '', tmp1)
        tmp1 = '0x' + tmp1
        tmp1 = int(tmp1, 16)
        if outtag == temp and intag == tmp and intag1 == tmp1:
            return 1
    else:
        # VlanTag有两个取值
        outtag = vlantag[0]
        intag = vlantag[1]
        # 外层VlanTag为0时
        if int(outtag) == 0:
            if int(intag) == 0:
                return 1
            if intag == '-1':
                if data[48:53] != '81 00':
                    return 1
            if int(intag) > 0:
                if data[36:41] == '81 00':
                    if data[48:53] == '81 00':
                        temp = data[55:59]
                        temp = re.sub(' ', '', temp)
                        temp = '0x' + temp
                        temp = int(temp, 16)
                        if int(intag) == temp:
                            return 1
        # 外层VlanTag为0时
        if int(outtag) > 0:
            if data[36:41] == '81 00':
                temp = data[43:47]
                temp = re.sub(' ', '', temp)
                temp = '0x' + temp
                temp = int(temp, 16)
                if int(outtag) == temp:
                    if int(intag) == 0:
                        return 1
                    if intag == '-1':
                        if data[48:53] != '81 00':
                            return 1
                    if int(intag) > 0:
                        if data[48:53] == '81 00' or data[48:53] == '91 00':
                            tmp = data[55:59]
                            tmp = re.sub(' ', '', tmp)
                            tmp = '0x' + tmp
                            tmp = int(tmp, 16)
                            if int(intag) == tmp:
                                return 1
    return 0


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
#   CheckDsendCaptureStream('2',Length='180')
########################################################## 
def CheckLengthOfData(length, data):
    if int(length) == len(data):
        return 1
    else:
        return 0


#######################################################
#
# CheckDstMacInData :检查抓到的流cos是否满足镜像的要求
#
#   args:
#                cos: cos 
#                data: actual frame data
#
#   return: 
#                1 :满足要求
#                0:不满足要求
#
# CheckDsendCaptureStream('2',Cos=['3'])
# CheckDsendCaptureStream('2',Cos=['3','4','5'])
# Cos的值使用十进制
# Cos取一个值，则仅判断报文第一层Cos;Cos取两个值，第一个值为外层Cos值，第二个值为内层Cos的值
# Cos取三个值，判断三层Cos值，第一个值为外层Cos值，第二个值为次外层Cos的值，第三个值为内层Cos的值
########################################################## 
def CheckCosInData(cos, data):
    # cos 取一个值
    if len(cos) == 1:
        data = data[42]
        data = '0x' + data
        data = int(data, 16)
        data = data / 2
        if int(cos[0]) == data:
            return 1
        else:
            return 0
    # cos 取两个值
    if len(cos) == 2:
        outcos = cos[0]
        incos = cos[1]
        outdata = data[42]
        outdata = '0x' + outdata
        outdata = int(outdata, 16)
        outdata = outdata / 2
        indata = data[54]
        indata = '0x' + indata
        indata = int(indata, 16)
        indata = indata / 2
        if int(outcos) == outdata and int(incos) == indata:
            return 1
        else:
            return 0
    # cos 取三个值
    if len(cos) == 3:
        outcos = cos[0]
        incos = cos[1]
        incos1 = cos[2]
        outdata = data[42]
        outdata = '0x' + outdata
        outdata = int(outdata, 16)
        outdata = outdata / 2
        indata = data[54]
        indata = '0x' + indata
        indata = int(indata, 16)
        indata = indata / 2
        indata1 = data[66]
        indata1 = '0x' + indata1
        indata1 = int(indata1, 16)
        indata1 = indata1 / 2
        if int(outcos) == outdata and int(incos) == indata and int(incos1) == indata1:
            return 1
        else:
            return 0

            ##################################


# 判断是否是arp包
# CheckDsendCaptureStream('2',Arp='1')
##################################
def CheckArpInData(arp, data):
    flag = data[36:41]
    if flag == '81 00':
        arphardwaretype = data[54:59]
        arpprotocoltype = data[60:65]
    else:
        arphardwaretype = data[42:47]
        arpprotocoltype = data[48:53]
    if arphardwaretype == '00 01' and arpprotocoltype == '08 00':
        return 1
    else:
        return 0


###########################################
# 判断arp包的类型
# CheckDsendCaptureStream('2',ArpType='request')
# CheckDsendCaptureStream('2',ArpType='reply')
###########################################
def CheckArpTypeInData(arptype, data):
    flag = data[36:41]
    if flag == '81 00':
        arpoperation = data[72:77]
    elif flag == '08 06':
        arpoperation = data[60:65]
    else:
        return 0
    if arptype == 'request' and arpoperation == '00 01':
        return 1
    elif arptype == 'reply' and arpoperation == '00 02':
        return 1
    else:
        return 0


###########################################
# 判断arp包的协议源mac
# CheckDsendCaptureStream('2',ArpSenderHardwareAddress='00-00-00-00-00-01')
###########################################    
def CheckArpSenderHardwareAddressInData(sendermac, data):
    flag = data[36:41]
    if flag == '81 00':
        data = data[78:95]
    if flag == '08 06':
        data = data[66:83]
    data = re.sub(' ', '-', data)
    sendermac = sendermac.upper()
    if sendermac == data:
        return 1
    else:
        return 0


###########################################
# 判断arp包的协议源ip
# CheckDsendCaptureStream('2',ArpSenderProtocolAddress='1.1.1.1')
###########################################    
def CheckArpSenderProtocolAddressInData(senderip, data):
    flag = data[36:41]
    if flag == '81 00':
        data = data[96:107]
    if flag == '08 06':
        data = data[84:95]
    n1 = data[0:2]
    n2 = data[3:5]
    n3 = data[6:8]
    n4 = data[9:11]
    n1 = '0x' + n1
    num1 = int(n1, 16)
    n2 = '0x' + n2
    num2 = int(n2, 16)
    n3 = '0x' + n3
    num3 = int(n3, 16)
    n4 = '0x' + n4
    num4 = int(n4, 16)
    spring = str(num1) + '.' + str(num2) + '.' + str(num3) + '.' + str(num4)
    if senderip == spring:
        return 1
    else:
        return 0


###########################################
# 判断arp包的协议源mac
# CheckDsendCaptureStream('2',ArpTargetHardwareAddress='00-00-00-00-00-01')
###########################################    
def CheckArpTargetHardwareAddressInData(targetmac, data):
    flag = data[36:41]
    if flag == '81 00':
        data = data[108:125]
    if flag == '08 06':
        data = data[96:113]
    data = re.sub(' ', '-', data)
    targetmac = targetmac.upper()
    if targetmac == data:
        return 1
    else:
        return 0


###########################################
# 判断arp包的协议源ip
# CheckDsendCaptureStream('2',ArpTargetProtocolAddress='1.1.1.1')
###########################################    
def CheckArpTargetProtocolAddressInData(targetip, data):
    flag = data[36:41]
    if flag == '81 00':
        data = data[126:137]
    if flag == '08 06':
        data = data[114:125]
    n1 = data[0:2]
    n2 = data[3:5]
    n3 = data[6:8]
    n4 = data[9:11]
    n1 = '0x' + n1
    num1 = int(n1, 16)
    n2 = '0x' + n2
    num2 = int(n2, 16)
    n3 = '0x' + n3
    num3 = int(n3, 16)
    n4 = '0x' + n4
    num4 = int(n4, 16)
    spring = str(num1) + '.' + str(num2) + '.' + str(num3) + '.' + str(num4)
    if targetip == spring:
        return 1
    else:
        return 0


def SetIxiaStream(**args):
    cmdstr = 'SetIxiaStream '
    for i in list(args.keys()):
        cmdstr += str(i) + ' ' + str(args[i]) + ' '
    print(cmdstr)
    res = IxiaProc(cmdstr)
    return res
