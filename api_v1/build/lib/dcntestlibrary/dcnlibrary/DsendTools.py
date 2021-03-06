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
#     - 2011.9.23 modified by qidb
#          -Add BuildRIP / BuildMSDP / BuildIGMP 
#     - 2011.10.25 modified by qidb
#          -Add CheckHEXInData/CheckBITInData/BuildPayload
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
#	  DesIp 2.2.2.2
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
    # 用于存储需要递增的报文域 :包括递增的类型(mac,ip,num),初始值，范围和步长；每条流的突发报文数目--countContinue；需要发送的报文数量(发完就停)--count,用于标识发送一定数量报文的发包速率是通过参数--rate指定:--mode 2
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
    
    BuildLLDP(args)
    
    # dcnstream += '/CUSTOM()'
    
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
    BuildPAYLOAD(args)
    # 添加报文结束
    
    # 针对发完一定数目报文就停的发包模式
    # --count 10 :标识该条流发完10条后停止
    # $dcnarrArgs(StreamMode2)为1则表示pc尽最大的能力发送数据，为0则通过用户指定(如果pc通过最大能力发包，则pc再抓取该包时会丢包
    # --mode 2用于表示发送指定数量报文的发送速率是通过--rate指定，而不是pc以最大能力发送(最后的真实发送速率在这个值附近)  
    # python实现实例
    # 1、正常发n个报文后停止(pps <= 10)
    # python Dsend.py --port 3   --rate 10 --proc "setStream" --streamMode pps  --streamSize 64 --stream {Ether(dst="01:00:00:00:02:11",type=0x8100)/Dot1Q(vlan=3,type=0xffff,prio=1) } --count 100
    #
    # 2、发n个报文后停止(超级快模式,没有--rate)
    # python Dsend.py --port 3  --proc "setStream" --streamMode pps  --streamSize 64 --stream {Ether(dst="01:00:00:00:02:11",type=0x8100)/Dot1Q(vlan=3,type=0xffff,prio=1) } --count 100
    #
    # 3、指定最大速率,发n个报文后停止(模式2,--mode 2)
    # python Dsend.py --port 3 --mode 2 --rate 200  --proc "setStream" --streamMode pps  --streamSize 64 --stream {Ether(dst="01:00:00:00:02:11",type=0x8100)/Dot1Q(vlan=3,type=0xffff,prio=1) } --count 100
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
    
    # 添加报文中域值变化的相关命令参数例如--incrMac1 00:00:01:00:00:01,100 ;是否为最后一条流的命令参数例如--lastStreamFlag 1   ;流的突发数目:--countContinue 2;需要发送的数量:--count 10
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
def BuildIncrField(name, type, initi, num, step='1', duan='64'):
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
###################################################################################	    
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
                        if int(args['StreamRate']) > 200 and int(args['StreamRate']) < 1000:
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
                
                ##################################################################################


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
#  BuildNoType :构建由python scapy发送的NoType报文头，如Dot3TagNoLen(....)
#				即二层包头的协议类型为空
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
#	             SouMac='00-00-00-00-00-03',DesMac='00-00-00-00-00-04')
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


######################################################################################################################################
#
#  Build8023Snap :构建由python scapy发送的802.3snap报文头，如Ether()/Dot3Tag()/LLC(dsap=0xaa,ssap=0xaa,ctrl=0x03)/ SNAP()/"……"
#
# args:  无
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
#######################################################################################################################################		
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
###################################################################################				
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
#  BuildPAYLOAD :构建由python scapy发送的802.3报文头，如Dot3Tag(....)
#
# args:  无
#
# return: 无
#
# addition:
#
# examples:
#     BuildPAYLOAD(args)
# 脚本调用格式：
#     SetDsendStream(Port='2',StreamRateMode='pps',StreamRate='10', FrameSize='64', \
#                    VlanId='22',UserPriority='4',Offset1='18',Length1='3',Value1='aabb05', \
#	             SouMac='00-00-00-00-00-03',DesMac='00-00-00-00-00-04')
###################################################################################
def BuildPAYLOAD(args):
    global dcnstream
    if 'Payload' in args:
        dcnstream = dcnstream + '/"payloadflag' + args['Payload'].replace(' ', '') + 'payloadflag"'


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
#	    
###################################################################################	    
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
# BuildLLDP :构建由python scapy发送的LLDP(LLDP-MED)报文，如LLDP(....)
#
# args:  无
#
# return: 无
#
# addition:
#
# examples:
#     BuildLLDP(args)
# 脚本调用格式：
#    SetDsendStream()
###################################################################################	
def BuildLLDP(args):
    global dcnstream
    
    if 'LLDPType' in args:
        if args['LLDPType'] == 'normal':
            # if args['ChassisID'] is not None:
            dcnstream = dcnstream + '/ChassisID('
            if 'ChassisIdType' in args:
                dcnstream = dcnstream + 'type=' + args['ChassisIdType'] + ','
            if 'ChassisIdLength' in args:
                dcnstream = dcnstream + 'length=' + args['ChassisIdLength'] + ','
            if 'ChassisIdSubType' in args:
                dcnstream = dcnstream + 'subtype=' + args['ChassisIdSubType'] + ','
            if 'ChassisIdValue' in args:
                strIdvalue = ''
                templist = re.split('-', args['ChassisIdValue'])
                for ch in templist:
                    strIdvalue = strIdvalue + chr(int(ch, 16))
                dcnstream = dcnstream + 'chassisid=\"' + strIdvalue + '\",'
            dcnstream = dcnstream + ')'
            
            if 'PortID' in args:
                dcnstream = dcnstream + '/PortID('
                if 'PortIDType' in args:
                    dcnstream = dcnstream + 'type=' + args['PortIDType'] + ','
                if 'PortIDLength' in args:
                    dcnstream = dcnstream + 'length=' + args['PortIDLength'] + ','
                if 'PortIDSubType' in args:
                    dcnstream = dcnstream + 'subtype=' + args['PortIDSubType'] + ','
                if 'PortID' in args:
                    dcnstream = dcnstream + 'portid=\"' + chr(int(args['PortID'], 16)) + '\",'
                dcnstream = dcnstream + ')'
            if 'LLDPTTL' in args:
                dcnstream = dcnstream + '/TTL('
                if 'TTLType' in args:
                    dcnstream = dcnstream + 'type=' + args['TTLType'] + ','
                if 'TTLLength' in args:
                    dcnstream = dcnstream + 'length=' + args['TTLLength'] + ','
                if 'LLDPTTL' in args:
                    dcnstream = dcnstream + 'ttl=' + args['LLDPTTL'] + ','
                dcnstream = dcnstream + ')'
            if 'PortDescription' in args:
                dcnstream = dcnstream + '/PortDescription('
                if 'PortDescriptionType' in args:
                    dcnstream = dcnstream + 'type=' + args['PortDescriptionType'] + ','
                if 'PortDescriptionLength' in args:
                    dcnstream = dcnstream + 'length=' + args['PortDescriptionLength'] + ','
                if 'PortDescription' in args:
                    dcnstream = dcnstream + 'portdescription=' + args['PortDescription'] + ','
                dcnstream = dcnstream + ')'
            if 'SystemName' in args:
                dcnstream = dcnstream + '/SystemName('
                if 'SystemNameType' in args:
                    dcnstream = dcnstream + 'type=' + args['SystemNameType'] + ','
                if 'SystemNameLength' in args:
                    dcnstream = dcnstream + 'length=' + args['SystemNameLength'] + ','
                if 'SystemName' in args:
                    dcnstream = dcnstream + 'systemname=' + args['SystemName'] + ','
                dcnstream = dcnstream + ')'
            if 'SystemDescription' in args:
                dcnstream = dcnstream + '/SystemDescription('
                if 'SystemDescriptionType' in args:
                    dcnstream = dcnstream + 'type=' + args['SystemDescriptionType'] + ','
                if 'SystemDescriptionLength' in args:
                    dcnstream = dcnstream + 'length=' + args['SystemDescriptionLength'] + ','
                if 'SystemDescription' in args:
                    dcnstream = dcnstream + 'systemdescription=' + args['SystemDescription'] + ','
                dcnstream = dcnstream + ')'
            if 'SystemCapabilities' in args:
                dcnstream = dcnstream + '/SystemCapabilities('
                if 'SystemCapabilitiesType' in args:
                    dcnstream = dcnstream + 'type=' + args['SystemCapabilitiesType'] + ','
                if 'SystemCapabilitiesLength' in args:
                    dcnstream = dcnstream + 'length=' + args['SystemCapabilitiesLength'] + ','
                if 'SystemCapabilities' in args:
                    dcnstream = dcnstream + 'systemcapabilities=' + args['SystemCapabilities'] + ','
                if 'SystemEnableCapabilities' in args:
                    dcnstream = dcnstream + 'enablecapabilities=' + args['SystemEnableCapabilities'] + ','
                dcnstream = dcnstream + ')'
            if 'MEDCapabilities' in args:
                dcnstream = dcnstream + '/MEDCapabilities('
                if 'MEDCapabilitiesType' in args:
                    dcnstream = dcnstream + 'type=' + args['MEDCapabilitiesType'] + ','
                if 'MEDCapabilitiesLength' in args:
                    dcnstream = dcnstream + 'length=' + args['MEDCapabilitiesLength'] + ','
                if 'MEDCapabilitiesOUI' in args:
                    dcnstream = dcnstream + 'OUI=' + args['MEDCapabilitiesOUI'] + ','
                if 'MEDCapabilitiesSubType' in args:
                    dcnstream = dcnstream + 'subtype=' + args['MEDCapabilitiesSubType'] + ','
                if 'MEDCapabilitiesValue' in args:
                    dcnstream = dcnstream + 'capabilities=' + args['MEDCapabilitiesValue'] + ','
                if 'MEDCapabilitiesDeviceType' in args:
                    dcnstream = dcnstream + 'devicetype=' + args['MEDCapabilitiesDeviceType'] + ','
                dcnstream = dcnstream + ')'
            
            if 'MEDMacPhy' in args:
                dcnstream = dcnstream + '/MEDMacPhy('
                if 'MEDMacPhyType' in args:
                    dcnstream = dcnstream + 'type=' + args['MEDMacPhyType'] + ','
                if 'MEDMacPhyLength' in args:
                    dcnstream = dcnstream + 'length=' + args['MEDMacPhyLength'] + ','
                if 'MEDMacPhyOUI' in args:
                    dcnstream = dcnstream + 'OUI=' + args['MEDMacPhyOUI'] + ','
                if 'MEDMacPhySubType' in args:
                    dcnstream = dcnstream + 'subtype=' + args['MEDMacPhySubType'] + ','
                if 'MEDMacPhyAutoSupport' in args:
                    dcnstream = dcnstream + 'autosupport=' + args['MEDMacPhyAutoSupport'] + ','
                if 'MEDMacPhyPDMCapabilities' in args:
                    dcnstream = dcnstream + 'PMDcapabilities=' + args['MEDMacPhyPDMCapabilities'] + ','
                dcnstream = dcnstream + ')'
            
            if 'MEDNetworkPolicy' in args:
                dcnstream = dcnstream + '/MEDNetworkPolicy('
                if 'MEDNetworkPolicyType' in args:
                    dcnstream = dcnstream + 'type=' + args['MEDNetworkPolicyType'] + ','
                if 'MEDNetworkPolicyLength' in args:
                    dcnstream = dcnstream + 'length=' + args['MEDNetworkPolicyLength'] + ','
                if 'MEDNetworkPolicyOUI' in args:
                    dcnstream = dcnstream + 'OUI=' + args['MEDNetworkPolicyOUI'] + ','
                if 'MEDNetworkPolicySubType' in args:
                    dcnstream = dcnstream + 'subtype=' + args['MEDNetworkPolicySubType'] + ','
                if 'MEDNetworkPolicyApplicationType' in args:
                    dcnstream = dcnstream + 'applicationtype=' + args['MEDNetworkPolicyApplicationType'] + ','
                if 'MEDNetworkPolicyUTX' in args:
                    dcnstream = dcnstream + 'UTX=' + args['MEDNetworkPolicyUTX'] + ','
                if 'MEDNetworkPolicyVlanId' in args:
                    dcnstream = dcnstream + 'vlanid=' + args['MEDNetworkPolicyVlanId'] + ','
                if 'MEDNetworkPolicyL2Priority' in args:
                    dcnstream = dcnstream + 'l2priority=' + args['MEDNetworkPolicyL2Priority'] + ','
                if 'MEDNetworkPolicyDscp' in args:
                    dcnstream = dcnstream + 'dscp=' + args['MEDNetworkPolicyDscp'] + ','
                dcnstream = dcnstream + ')'
            
            if 'MEDEcsLocationId' in args:
                dcnstream = dcnstream + '/MEDEcsLocationId('
                if 'MEDEcsLocationIdType' in args:
                    dcnstream = dcnstream + 'type=' + args['MEDEcsLocationId'] + ','
                if 'MEDEcsLocationIdLength' in args:
                    dcnstream = dcnstream + 'length=' + args['MEDEcsLocationIdLength'] + ','
                if 'MEDEcsLocationIdOUI' in args:
                    dcnstream = dcnstream + 'OUI=' + args['MEDEcsLocationIdOUI'] + ','
                if 'MEDEcsLocationIdSubType' in args:
                    dcnstream = dcnstream + 'subtype=' + args['MEDEcsLocationIdSubType'] + ','
                if 'MEDEcsLocationIdLocationFormat' in args:
                    dcnstream = dcnstream + 'locationformat=' + args['MEDEcsLocationIdLocationFormat'] + ','
                if 'MEDEcsLocationIdValue' in args:
                    dcnstream = dcnstream + 'locationid=' + args['MEDEcsLocationIdValue'] + ','
                dcnstream = dcnstream + ')'
            
            if 'MEDExtendedPower' in args:
                dcnstream = dcnstream + '/MEDExtendedPower('
                if 'MEDExtendedPowerType' in args:
                    dcnstream = dcnstream + 'type=' + args['MEDExtendedPowerType'] + ','
                if 'MEDExtendedPowerLength' in args:
                    dcnstream = dcnstream + 'length=' + args['MEDExtendedPowerLength'] + ','
                if 'MEDExtendedPowerOUI' in args:
                    dcnstream = dcnstream + 'OUI=' + args['MEDExtendedPowerOUI'] + ','
                if 'MEDExtendedPowerSubType' in args:
                    dcnstream = dcnstream + 'subtype=' + args['MEDExtendedPowerSubType'] + ','
                if 'MEDExtendedPowerPowerType' in args:
                    dcnstream = dcnstream + 'powertype=' + args['MEDExtendedPowerPowerType'] + ','
                if 'MEDExtendedPowerPowerSource' in args:
                    dcnstream = dcnstream + 'powersource=' + args['MEDExtendedPowerPowerSource'] + ','
                if 'MEDExtendedPowerPowerPriority' in args:
                    dcnstream = dcnstream + 'powerpriority=' + args['MEDExtendedPowerPowerPriority'] + ','
                if 'MEDExtendedPowerPMDCapabilities' in args:
                    dcnstream = dcnstream + 'PMDcapabilities=' + args['MEDExtendedPowerPMDCapabilities'] + ','
                dcnstream = dcnstream + ')'
            
            if 'MEDInventorySoftwareRevision' in args:
                dcnstream = dcnstream + '/MEDInventorySoftwareRevision('
                if 'MEDInventorySoftwareRevisionType' in args:
                    dcnstream = dcnstream + 'type=' + args['MEDInventorySoftwareRevisionType'] + ','
                if 'MEDInventorySoftwareRevisionLength' in args:
                    dcnstream = dcnstream + 'length=' + args['MEDInventorySoftwareRevisionLength'] + ','
                if 'MEDInventorySoftwareRevisionOUI' in args:
                    dcnstream = dcnstream + 'OUI=' + args['MEDInventorySoftwareRevisionOUI'] + ','
                if 'MEDInventorySoftwareRevisionSubType' in args:
                    dcnstream = dcnstream + 'subtype=' + args['MEDInventorySoftwareRevisionSubType'] + ','
                if 'MEDInventorySoftwareRevisionSoftwareRevision' in args:
                    dcnstream = dcnstream + 'softwarerevision=' + args[
                        'MEDInventorySoftwareRevisionSoftwareRevision'] + ','
                dcnstream = dcnstream + ')'
            
            if 'MEDInventoryHardwareRevision' in args:
                dcnstream = dcnstream + '/MEDInventoryHardwareRevision('
                if 'MEDInventoryHardwareRevisionType' in args:
                    dcnstream = dcnstream + 'type=' + args['MEDInventoryHardwareRevisionType'] + ','
                if 'MEDInventoryHardwareRevisionLength' in args:
                    dcnstream = dcnstream + 'length=' + args['MEDInventoryHardwareRevisionLength'] + ','
                if 'MEDInventoryHardwareRevisionOUI' in args:
                    dcnstream = dcnstream + 'OUI=' + args['MEDInventoryHardwareRevisionOUI'] + ','
                if 'MEDInventoryHardwareRevisionSubType' in args:
                    dcnstream = dcnstream + 'subtype=' + args['MEDInventoryHardwareRevisionSubType'] + ','
                if 'MEDInventoryHardwareRevisionHardwareRevision' in args:
                    dcnstream = dcnstream + 'hardwarerevision=' + args[
                        'MEDInventoryHardwareRevisionSoftwareRevision'] + ','
                dcnstream = dcnstream + ')'
            
            if 'MEDInventoryFirmwareRevision' in args:
                dcnstream = dcnstream + '/MEDInventoryFirmwareRevision('
                if 'MEDInventoryFirmwareRevisionType' in args:
                    dcnstream = dcnstream + 'type=' + args['MEDInventoryFirmwareRevisionType'] + ','
                if 'MEDInventoryFirmwareRevisionLength' in args:
                    dcnstream = dcnstream + 'length=' + args['MEDInventoryFirmwareRevisionLength'] + ','
                if 'MEDInventoryFirmwareRevisionOUI' in args:
                    dcnstream = dcnstream + 'OUI=' + args['MEDInventoryFirmwareRevisionOUI'] + ','
                if 'MEDInventoryFirmwareRevisionSubType' in args:
                    dcnstream = dcnstream + 'subtype=' + args['MEDInventoryFirmwareRevisionSubType'] + ','
                if 'MEDInventoryFirmwareRevisionFirmwareRevision' in args:
                    dcnstream = dcnstream + 'firmwarerevision=' + args[
                        'MEDInventoryFirmwareRevisionFirmwareRevision'] + ','
                dcnstream = dcnstream + ')'
            
            if 'MEDInventorySerialNumberRevision' in args:
                dcnstream = dcnstream + '/MEDInventorySerialNumberRevision('
                if 'MEDInventorySerialNumberRevisionType' in args:
                    dcnstream = dcnstream + 'type=' + args['MEDInventorySerialNumberRevisionType'] + ','
                if 'MEDInventorySerialNumberRevisionLength' in args:
                    dcnstream = dcnstream + 'length=' + args['MEDInventorySerialNumberRevisionLength'] + ','
                if 'MEDInventorySerialNumberRevisionOUI' in args:
                    dcnstream = dcnstream + 'OUI=' + args['MEDInventorySerialNumberRevisionOUI'] + ','
                if 'MEDInventorySerialNumberRevisionSubType' in args:
                    dcnstream = dcnstream + 'subtype=' + args['MEDInventorySerialNumberRevisionSubType'] + ','
                if 'MEDInventorySerialNumberRevisionSerialNumberRevision' in args:
                    dcnstream = dcnstream + 'serialnumber=' + args[
                        'MEDInventorySerialNumberRevisionSerialNumberRevision'] + ','
                dcnstream = dcnstream + ')'
            
            if 'MEDInventoryManufacturer' in args:
                dcnstream = dcnstream + '/MEDInventoryManufacturer('
                if 'MEDInventoryManufacturerType' in args:
                    dcnstream = dcnstream + 'type=' + args['MEDInventoryManufacturerType'] + ','
                if 'MEDInventoryManufacturerLength' in args:
                    dcnstream = dcnstream + 'length=' + args['MEDInventoryManufacturerLength'] + ','
                if 'MEDInventoryManufacturerOUI' in args:
                    dcnstream = dcnstream + 'OUI=' + args['MEDInventoryManufacturerOUI'] + ','
                if 'MEDInventoryManufacturerSubType' in args:
                    dcnstream = dcnstream + 'subtype=' + args['MEDInventoryManufacturerSubType'] + ','
                if 'MEDInventoryManufacturerManufacturer' in args:
                    dcnstream = dcnstream + 'manufacturer=' + args['MEDInventoryManufacturerManufacturer'] + ','
                dcnstream = dcnstream + ')'
            
            if 'MEDInventoryModelName' in args:
                dcnstream = dcnstream + '/MEDInventoryModelName('
                if 'MEDInventoryModelNameType' in args:
                    dcnstream = dcnstream + 'type=' + args['MEDInventoryModelNameType'] + ','
                if 'MEDInventoryModelNameLength' in args:
                    dcnstream = dcnstream + 'length=' + args['MEDInventoryModelNameLength'] + ','
                if 'MEDInventoryModelNameOUI' in args:
                    dcnstream = dcnstream + 'OUI=' + args['MEDInventoryModelNameOUI'] + ','
                if 'MEDInventoryModelNameSubType' in args:
                    dcnstream = dcnstream + 'subtype=' + args['MEDInventoryModelNameSubType'] + ','
                if 'MEDInventoryModelNameModelName' in args:
                    dcnstream = dcnstream + 'modelname=' + args['MEDInventoryModelNameModelName'] + ','
                dcnstream = dcnstream + ')'
            
            if 'MEDAssetID' in args:
                dcnstream = dcnstream + '/MEDAssetID('
                if 'MEDAssetIDType' in args:
                    dcnstream = dcnstream + 'type=' + args['MEDAssetIDType'] + ','
                if 'MEDAssetIDLength' in args:
                    dcnstream = dcnstream + 'length=' + args['MEDAssetIDLength'] + ','
                if 'MEDAssetIDOUI' in args:
                    dcnstream = dcnstream + 'OUI=' + args['MEDAssetIDOUI'] + ','
                if 'MEDAssetIDSubType' in args:
                    dcnstream = dcnstream + 'subtype=' + args['MEDAssetIDSubType'] + ','
                if 'MEDAssetIDMEDAssetID' in args:
                    dcnstream = dcnstream + 'assetid=' + args['MEDAssetIDMEDAssetID'] + ','
                dcnstream = dcnstream + ')'
            if 'LLDPEnd' in args:
                dcnstream = dcnstream + '/EndTlv('
                if 'LLDPEndType' in args:
                    dcnstream = dcnstream + 'type=' + args['LLDPEndType'] + ','
                if 'LLDPEndLength' in args:
                    dcnstream = dcnstream + 'length=' + args['LLDPEndLength'] + ','
                dcnstream = dcnstream + ')'


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
###################################################################################	
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
###################################################################################  
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
        elif args['ProtoclEx'] == 'rip':
            dcnstream = dcnstream + ')'
            BuildRIP(args)
        elif args['ProtoclEx'] == 'msdp':
            dcnstream = dcnstream + ')'
            BuildMSDP(args)
        elif args['ProtoclEx'] == 'igmp':
            dcnstream = dcnstream + ')'
            BuildIGMP(args)
        elif args['ProtoclEx'] == 'ospf':
            dcnstream = dcnstream + ')'
            BuildOSPF(args)
        elif args['ProtoclEx'] == 'icmp':
            dcnstream = dcnstream + ')'
            BuildICMP(args)
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
        elif args['ProtoclEx'] == 'ipv6ndpna':
            dcnstream = dcnstream + ')'
            BuildIPv6NA(args)
        elif args['ProtoclEx'] == 'mld':
            dcnstream = dcnstream + ')'
            BuildIPv6MLD(args)
        elif args['ProtoclEx'] == 'icmpv6':
            dcnstream = dcnstream + ')'
            BuildICMPv6(args)
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


def BuildIPv6NA(args):
    # pass
    global dcnstream
    if 'Ipv6NdpNaMaxPacketInfo' in args or 'Ipv6NdpNaPacketInfo' in args:
        if 'Ipv6NdpNaMaxPacketInfo' in args:
            NAInfo = args['Ipv6NdpNaMaxPacketInfo']
        else:
            NAInfo = args['Ipv6NdpNaPacketInfo']
        dcnstream = dcnstream + '/ICMPv6ND_NA('
        if 'FLagR' in NAInfo:
            dcnstream = dcnstream + 'R=' + NAInfo['FlagR'] + ','
        if 'FlagS' in NAInfo:
            dcnstream = dcnstream + 'S=' + NAInfo['FlagS'] + ','
        if 'FlagO' in NAInfo:
            dcnstream = dcnstream + 'O=' + NAInfo['FlagO'] + ','
        if 'Ipv6Addr' not in NAInfo:
            NAInfo['Ipv6Addr'] = '2001::1'
        if 'Num' not in NAInfo:
            NAInfo['Num'] = '1'
        if 'TgtStepv6' not in NAInfo:
            NAInfo['TgtStepv6'] = '1'
        if 'Ipv6Last16Bit' not in NAInfo:
            NAInfo['Ipv6Last16Bit'] = '128'
        BuildIncrField('tgt', 'ipv6', str(NAInfo['Ipv6Addr']), str(NAInfo['Num']), str(NAInfo['TgtStepv6']),
                       str(NAInfo['Ipv6Last16Bit']))
        dcnstream = dcnstream + ')/ICMPv6NDOptDstLLAddr('
        if 'Mac' not in NAInfo:
            NAInfo['Mac'] = '00-00-00-00-00-01'
        NAInfo['Mac'] = re.sub('-', ':', NAInfo['Mac'])
        if 'Num' not in NAInfo:
            NAInfo['Num'] = '1'
        BuildIncrField('lladdr', 'mac', str(NAInfo['Mac']), str(NAInfo['Num']))
        dcnstream = dcnstream + ')'
    else:
        dcnstream = dcnstream + '/ICMPv6ND_NA()/ICMPv6NDOptDstLLAddr()'


def BuildIPv6MLD(args):
    # pass
    global dcnstream
    if 'HopLimit' not in args:
        v6stream = str(re.search("IPv6\((.*)\)", dcnstream).group(1))
        v6stream = v6stream + "hlim=1,"
        dcnstream = str(re.sub(re.search("IPv6\((.*)\)", dcnstream).group(1), v6stream, dcnstream))
        dcnstream = dcnstream + "/IPv6ExtHdrHopByHop(nh=58,options=RouterAlert())"
    if 'MldVersion' not in args:
        args['MldVersion'] = '1'
    if 'Type' not in args:
        args['Type'] = 'report'
    if args['MldVersion'] == '1':
        if args['Type'] == 'report':
            dcnstream = dcnstream + "/ICMPv6MLReport("
        elif args['Type'] == 'query':
            dcnstream = dcnstream + "/ICMPv6MLQuery("
        elif args['Type'] == 'done':
            dcnstream = dcnstream + "/ICMPv6MLDone("
        if 'MldGroupAddress' not in args:
            args['MldGroupAddress'] = 'ff3f::1'
        if 'MldGroupNum' not in args:
            args['MldGroupNum'] = '1'
        if 'MldGroupStep' not in args:
            args['MldGroupStep'] = '1'
        if 'MldGroupAddrMode' not in args:
            args['MldGroupAddrMode'] = '128'
        BuildIncrField('mladdr', 'ipv6', args['MldGroupAddress'], args['MldGroupNum'], args['MldGroupStep'],
                       args['MldGroupAddrMode'])
        dcnstream = dcnstream + ")"
    elif args['MldVersion'] == '2':
        if args['Type'] == 'report':
            dcnstream = dcnstream + "/ICMPv6MLv2Report("
        if 'MldGroupRecord' in args:
            if len(args['MldGroupRecord']) >= 1:
                len_groupRecord = len(args['MldGroupRecord'])
                dcnstream = dcnstream + "numofrec=" + str(len_groupRecord) + ",)"
                for i in range(len_groupRecord):
                    typelist = args['MldGroupRecord'][i]
                    group = typelist[0]
                    sourc = typelist[2]
                    lensourc = len(sourc)
                    record_type = typelist[1]
                    if 'include' == record_type:
                        dcnstream = dcnstream + '/ICMPv6MLv2Record(rectype=0x01,'
                    elif 'exclude' == record_type:
                        dcnstream = dcnstream + '/ICMPv6MLv2Record(rectype=0x02,'
                    elif 'toinclude' == record_type:
                        dcnstream = dcnstream + '/ICMPv6MLv2Record(rectype=0x03,'
                    elif 'toexclude' == record_type:
                        dcnstream = dcnstream + '/ICMPv6MLv2Record(rectype=0x04,'
                    elif 'allow' == record_type:
                        dcnstream = dcnstream + '/ICMPv6MLv2Record(rectype=0x05,'
                    elif 'block' == record_type:
                        dcnstream = dcnstream + '/ICMPv6MLv2Record(rectype=0x06,'
                    dcnstream = dcnstream + "numofsource=" + str(lensourc) + ","
                    dcnstream = dcnstream + "group=\"" + str(group) + "\")"
                    for j in range(lensourc):
                        arraysourc = sourc[j]
                        dcnstream = dcnstream + "/Srcv6List(sourcev6=\"" + str(arraysourc) + "\")"
        else:
            dcnstream = dcnstream + ")"


def BuildICMPv6(args):
    global dcnstream
    if 'Offset1' in args:
        if args['Offset1'] == 54 or args['Offset1'] == 58:
            if 'Length1' in args:
                if args['Length1'] == 2:
                    if 'Value1' not in args:
                        value1 = '0x0000'
                    else:
                        value1 = '0x' + args['Value1']
                    type = (int(value1, 16) & 0xff00) >> 8
                    code = int(value1, 16) & 0x00ff
                    dcnstream = dcnstream + '/ICMPv6Unknown(type=' + str(type) + ',code=' + str(code) + ')'
                    dcnstream = dcnstream + ')'
                elif args['Length1'] == 1:
                    if 'Value1' not in args:
                        value1 = '0x00'
                    else:
                        value1 = '0x' + args['Value1']
                    if 'Value2' not in args:
                        value2 = '0x00'
                    else:
                        value2 = '0x' + args['Value2']
                    dcnstream = dcnstream + '/ICMPv6Unknown(type=' + str(int(value1, 16)) + ',code=' + str(
                        int(value2, 16)) + ')'
                    dcnstream = dcnstream + ')'
    if 'Type' in args or 'Code' in args:
        dcnstream = dcnstream + '/ICMPv6Unknown('
        if 'Type' in args:
            dcnstream = dcnstream + 'type=' + str(int(args['Type'], 16)) + ','
        if 'Code' in args:
            dcnstream = dcnstream + 'code=' + str(int(args['Code'], 16)) + ','
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


##################################################################################
#
# BuildRIP :构建由于python scapy发送的 RIP报文，如RIP(....)
#
# args:  无
#
# return: 无
#
# addition:
#
# examples:
#     BuildRIP(args)
# 脚本调用格式：
#    SetDsendStream(Port='4',StreamMode='0',StreamRateMode='pps',StreamRate='10', \
#		   SouMac='00-00-00-0F-00-05',DesMac='00-00-00-0F-00-06', \
#		   Protocl='ipv4',SouIp = '120.1.1.1', DesIp = '122.1.1.1',ProtoclEx='rip',RipCommand='2',RipVersion='2', \
#		   RipRoute=[{'Ip':'10.1.1.1','Mask':'255.255.255.255','Nexthop':'10.1.1.1','Metric':'5','Num':'5'}, \
#			     {'Ip':'20.1.1.1','Mask':'255.255.255.0','Nexthop':'100.1.1.1','Metric':'6','Num':'20'}])
###################################################################################
def BuildRIP(args):
    global dcnstream
    dcnstream = dcnstream + "/UDP(sport=520)"
    dcnstream = dcnstream + "/RIP("
    # 构建rip command和version
    if "RipCommand" in args:
        dcnstream = dcnstream + "cmd=" + str(args["RipCommand"]) + ","
    if "RipVersion" in args:
        dcnstream = dcnstream + "version=" + str(args["RipVersion"]) + ","
    dcnstream = dcnstream + ")"
    if "RipRoute" in args:
        intRouteLength = len(args["RipRoute"])
        for i in range(intRouteLength):
            RIPEntryArgs = args["RipRoute"][i]
            dcnstream = dcnstream + "/RIPEntry("
            if "Ip" in RIPEntryArgs:
                if "Num" not in RIPEntryArgs:
                    strRIPEntryNum = "1"
                else:
                    strRIPEntryNum = RIPEntryArgs["Num"]
                if "RIPEntryMode" not in RIPEntryArgs:
                    strRIPEntryMode = "classC"
                else:
                    strRIPEntryMode = RIPEntryArgs["RIPEntryMode"]
                if "RIPEntryStep" not in RIPEntryArgs:
                    strRIPEntryStep = "1"
                else:
                    strRIPEntryStep = RIPEntryArgs["RIPEntryStep"]
                BuildIncrField("addr", "ip", RIPEntryArgs["Ip"], strRIPEntryNum, strRIPEntryStep, strRIPEntryMode)
            if "Mask" in RIPEntryArgs:
                dcnstream = dcnstream + "mask=\"" + RIPEntryArgs["Mask"] + "\","
            if "Nexthop" in RIPEntryArgs:
                dcnstream = dcnstream + "nextHop=\"" + RIPEntryArgs["Nexthop"] + "\","
            if "Metric" in RIPEntryArgs:
                dcnstream = dcnstream + "metric=" + str(RIPEntryArgs["Metric"])
            dcnstream = dcnstream + ")"


##################################################################################
#
# BuildMSDP :构建由于python scapy发送的 MSDP报文，如MSDP(....)
#
# args:  无
#
# return: 无
#
# addition:
#
# examples:
#     BuildMSDP(args)
# 脚本调用格式：
#    SetDsendStream(Port='4',StreamMode='0',StreamRateMode='pps',StreamRate='10', \
#		   SouMac='00-00-00-0F-00-05',DesMac='00-00-00-0F-00-06', \
#		   Protocl='ipv4',SouIp = '120.1.1.1', DesIp = '122.1.1.1',ProtoclEx='msdp',MsdpType='0x05')

###################################################################################
def BuildMSDP(args):
    global dcnstream
    dcnstream = dcnstream + "/TCP(dport=639,sport=3531,flags=0x18)"
    dcnstream = dcnstream + "/MSDP("
    # 构建rip command和version
    if "MsdpType" in args:
        dcnstream = dcnstream + "type=" + str(args["MsdpType"]) + ","
    dcnstream = dcnstream + ")"


##################################################################################
#
# BuildOSPF :构建由于python scapy发送的 OSPF报文，如OSPF(....)
#
# args:  无
#
# return: 无
#
# addition:
#
# examples:
#     BuildOSPF(args)
# 脚本调用格式：
#    SetDsendStream(Port='4',StreamMode='0',StreamRateMode='pps',StreamRate='10', \
#		   SouMac='00-00-00-0F-00-05',DesMac='00-00-00-0F-00-06', \
#		   Protocl='ipv4',SouIp = '120.1.1.1', DesIp = '122.1.1.1',ProtoclEx='ospf')

###################################################################################
def BuildOSPF(args):
    global dcnstream
    dcnstream = dcnstream + "/OSPF("
    dcnstream = dcnstream + ")"


##################################################################################
#
# BuildIGMP :构建由于python scapy发送的 IGMP报文，如IGMP(....)
#
# args:  无
#
# return: 无
#
# addition:
#
# examples:
#     BuildIGMP(args)
# 脚本调用格式：
# SetDsendStream(Port='4',StreamMode='0',StreamRateMode='pps',StreamRate='10', \
#		   SouMac='00-00-00-0F-00-05',DesMac='FF-FF-FF-FF-FF-FF', \
#		   Protocl='ipv4',SouIp = '120.1.1.1', DesIp = '224.0.0.27',ProtoclEx='igmp', \
#		   Type='report',IgmpVersion='3',IgmpGroupRecord=[['239.1.1.1','include',['14.0.0.1' \
#		   ,'14.0.0.2']],['225.1.1.9','exclude',['18.0.0.1','19.0.0.1']]])
# SetDsendStream(Port='4',StreamMode='0',StreamRateMode='pps',StreamRate='10', \
#		   SouMac='00-00-00-0F-00-05',DesMac='FF-FF-FF-FF-FF-FF', \
#		   Protocl='ipv4',SouIp = '120.1.1.1', DesIp = '224.0.0.27',ProtoclEx='igmp', \
#		   Type='report',IgmpVersion='2',IgmpGroupAddress = '225.10.10.1', IgmpRepeat='10')
###################################################################################
def BuildIGMP(args):
    global dcnstream
    dcnstream = dcnstream + "/IGMP("
    if "Version" in args or "Type" in args:
        if "Type" in args:
            if "IgmpVersion" in args:
                if args["IgmpVersion"] == '1':
                    if args["Type"] == 'report' or args["Type"] == '2':
                        dcnstream = dcnstream + 'version=0x12,maxres=0x00,'
                    elif args["Type"] == 'query' or args["Type"] == '1':
                        dcnstream = dcnstream + 'version=0x11,maxres=0x00,'
                    else:
                        pass
                if args["IgmpVersion"] == '2':
                    if args["Type"] == 'report' or args["Type"] == '22':
                        dcnstream = dcnstream + 'version=0x16,'
                    elif args["Type"] == 'query' or args["Type"] == '17':
                        dcnstream = dcnstream + 'version=0x11,'
                    elif args["Type"] == 'leave' or args["Type"] == '23':
                        dcnstream = dcnstream + 'version=0x17,'
                    else:
                        pass
                if args["IgmpVersion"] == '3':
                    if args["Type"] == 'report' or args["Type"] == '22' or args["Type"] == '34':
                        dcnstream = re.sub('IGMP', 'IGMPv3Report', dcnstream)
                        dcnstream = dcnstream + 'version=0x22,'
                    elif args["Type"] == 'query' or args["Type"] == '17':
                        dcnstream = re.sub('IGMP', 'IGMPv3Query', dcnstream)
                        dcnstream = dcnstream + 'version=0x11,'
                    else:
                        pass
            else:
                dcnstream = dcnstream + 'version=' + args["Type"] + ','
        else:
            dcnstream = dcnstream + 'version=' + args["Version"] + ','
    else:
        if 'Offset1' in args:
            if args["Offset1"] == '38' or args["Offset1"] == '34':
                if "Value1" not in args:
                    tempValue = 0
                else:
                    tempValue = args["Value1"]
                value1 = '0x'
                value1 = value1 + tempValue
                value1 = int(value1, 16)
                if "Repeat1" not in args:
                    strRepeat = 1
                else:
                    strRepeat = args["Repeat1"]
                if "Step1" not in args:
                    strStep1 = 1
                else:
                    strStep1 = args["Step1"]
                BuildIncrField('version', 'num', value1, strRepeat)
    if 'Group' in args or 'IgmpGroupAddress' in args:
        if 'IgmpGroupAddress' in args:
            group = args['IgmpGroupAddress']
        else:
            group = args['Group']
        if 'IgmpRepeat' not in args:
            tmpIgmpRepeat = 1
        else:
            tmpIgmpRepeat = args["IgmpRepeat"]
        if 'IgmpStep' not in args:
            tmpIgmpStep = 1
        else:
            tmpIgmpStep = args["IgmpStep"]
        if 'DesClassMode' not in args:
            tmpIgmpClassMode = 'classD'
        else:
            tmpIgmpClassMode = args["DesClassMode"]
        BuildIncrField('group', 'ip', group, tmpIgmpRepeat, tmpIgmpStep, tmpIgmpClassMode)
    if 'IgmpVersion' in args and 'Type' in args:
        if args["IgmpVersion"] == '3' and args["Type"] == 'query':
            if 'IgmpSourceIpAddress' in args:
                dcnstream = dcnstream + 'sournum=1,/SrcList(source=\"' + args["IgmpSourceIpAddress"] + '\"'
    if 'IgmpGroupRecord' in args:
        if len(args["IgmpGroupRecord"]) >= 1:
            tmpLen = len(args["IgmpGroupRecord"])
            dcnstream = dcnstream + 'numrec=' + str(tmpLen) + ',)'
            for i in range(tmpLen):
                tmpList = args["IgmpGroupRecord"][i]
                strGroup = tmpList[0]
                listSourc = tmpList[2]
                intLenSourc = len(listSourc)
                if str.lower(tmpList[1]) == 'include':
                    dcnstream = dcnstream + '/IGMPv3Record(rectype=0x01,'
                elif str.lower(tmpList[1]) == 'exclude':
                    dcnstream = dcnstream + '/IGMPv3Record(rectype=0x02,'
                elif str.lower(tmpList[1]) == 'toinclude':
                    dcnstream = dcnstream + '/IGMPv3Record(rectype=0x03,'
                elif str.lower(tmpList[1]) == 'toexclude':
                    dcnstream = dcnstream + '/IGMPv3Record(rectype=0x04,'
                elif str.lower(tmpList[1]) == 'allow':
                    dcnstream = dcnstream + '/IGMPv3Record(rectype=0x05,'
                elif str.lower(tmpList[1]) == 'block':
                    dcnstream = dcnstream + '/IGMPv3Record(rectype=0x06,'
                dcnstream = dcnstream + 'numsour=' + str(intLenSourc) + ','
                dcnstream = dcnstream + 'group=\"' + strGroup + '\")'
                if intLenSourc == 0:
                    dcnstream = dcnstream + '/SrcList(source=\"\"'
                    if i != tmpLen - 1:
                        dcnstream = dcnstream + ')'
                else:
                    for j in range(intLenSourc):
                        tmpSourc = listSourc[j]
                        if (i == tmpLen - 1) and (j == intLenSourc - 1):
                            dcnstream = dcnstream + '/SrcList(source=\"' + tmpSourc + '\"'
                        else:
                            dcnstream = dcnstream + '/SrcList(source=\"' + tmpSourc + '\")'
    
    dcnstream = dcnstream + ")"


##################################################################################
#
# BuildICMP :构建由于python scapy发送的 ICMP报文，如ICMP(....)
#
# args:  无
#
# return: 无
#
# addition:
#
# examples:
#     BuildICMP(args)
# 脚本调用格式：
# SetDsendStream(Port='11',StreamMode='0',StreamRateMode='pps',StreamRate='1', \
# SouMac='00-00-00-0F-00-05',DesMac='01-00-5e-01-01-01', \
# Protocl='ipv4',SouIp = '20.1.1.2', DesIp = '11.1.1.3',ProtoclEx='icmp', \
# IcmpType = '9',IcmpCode = '9',IcmpSequence = '9',IcmpChecksum = '999')
###################################################################################
def BuildICMP(args):
    global dcnstream
    dcnstream = dcnstream + '/ICMP('
    if 'IcmpType' in args:
        dcnstream = dcnstream + 'type=' + args['IcmpType'] + ','
    if 'IcmpCode' in args:
        dcnstream = dcnstream + 'code=' + args['IcmpCode'] + ','
    if 'IcmpSequence' in args:
        dcnstream = dcnstream + 'seq=' + args['IcmpSequence'] + ','
    if 'IcmpChecksum' in args:
        dcnstream = dcnstream + 'chksum=' + args['IcmpChecksum'] + ','
    dcnstream = dcnstream + ")"


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
    num = str(num)
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
        if re.search('ERROR', rate1) is not None or re.search('ERROR', rate2) is not None:
            # if rate1 == 'ERROR: timed out' or rate2 == 'ERROR: timed out':
            time.sleep(waittimer)
            continue
            # rate1 = '0'
            # rate2 = '0'
        
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
    if int(rate) == 0:
        if int(rate1) == 0:
            return 0
        else:
            return 1
    else:
        rate2 = abs(float(rate1) - float(rate)) / float(rate)
        if float(rate2) <= float(pianyi):
            return 0
        else:
            return 1


##############################################################################################
#
# GetDsendPacketsReceiveRate :查看端口收报速率是否符合预期速率，提供误差参数
#
# args:
#     port:收包端口
#
# return:
#     0,符合预期
#     1，不符合预期
# examples:
#    GetDsendPacketsReceiveRate('3')
#############################################################################################
def GetDsendPacketsReceiveRate(port):
    rate1 = Dshow("--port " + str(port) + " --type packetReceiveRate")
    return int(rate1)


##############################################################################################
#
# GetDsendBytesReceiveRate :查看端口收报速率是否符合预期速率，提供误差参数
#
# args:
#     port:收包端口
# 
# return:
#     0,符合预期
#     1，不符合预期
# examples:
#    GetDsendBytesReceiveRate('3')
#############################################################################################
def GetDsendBytesReceiveRate(port):
    rate1 = Dshow("--port " + str(port) + " --type byteReceiveRate")
    return int(rate1)


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


######################################################################
#
# SetPortIpFilter:  获取某端口发包的字节速率
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
#     SetPortFilter('3')
######################################################################
def SetPortIpFilter(port, acl):
    strAcl = re.sub(' ', '_', acl)
    count = Dsend("--port " + str(port) + " --proc setPortIpFilter" + ' --acl "' + strAcl + '"')
    return count


######################################################################
#
# SetPortMacFilter:  获取某端口发包的字节速率
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
#     SetPortMacFilter('3')
######################################################################
def SetPortMacFilter(port, acl):
    strAcl = re.sub(' ', '_', acl)
    count = Dsend("--port " + str(port) + " --proc setPortMacFilter" + ' --acl "' + strAcl + '"')
    return count


######################################################################
#
# EnableIpFilter:  获取某端口发包的字节速率
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
#     SetPortMacFilter('3')
######################################################################
def EnableIpFilter(port):
    count = Dsend("--port " + str(port) + " --proc enableIpFilter")
    return count


######################################################################
#
# EnableMacFilter:  获取某端口发包的字节速率
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
#     EnableMacFilter('3')
######################################################################
def EnableMacFilter(port):
    count = Dsend("--port " + str(port) + " --proc enableMacFilter")
    return count


######################################################################
#
# GetFilterCounter:  获取某端口发包的字节速率
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
#     GetFilterCounter('3')
######################################################################
def GetFilterCounter(port):
    count = Dsend("--port " + str(port) + " --proc getFilterCounter")
    retValue = {'ip': [], 'mac': []}
    compilestr = re.compile('Rule ID \d+ packet\(s\) number is (\d+)\.', re.DOTALL)
    res1 = re.search('(IP Ingress.+)MAC', count, flags=re.DOTALL)
    if res1 is not None:
        reslist1 = re.split('\n', res1.group(0))
        for tempstr in reslist1:
            tempret = compilestr.search(tempstr)
            if tempret is not None:
                retValue['ip'].append(tempret.group(1))
    res2 = re.search('(MAC Ingress.+)', count, flags=re.DOTALL)
    if res2 is not None:
        reslist2 = re.split('\n', res2.group(0))
        for tempstr in reslist2:
            tempret = compilestr.search(tempstr)
            if tempret is not None:
                retValue['mac'].append(tempret.group(1))
    print(retValue)
    return retValue


######################################################################
#
# ResetCounter:  获取某端口发包的字节速率
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
#     ResetCounter('3')
######################################################################
def ResetCounter(port):
    count = Dsend("--port " + str(port) + " --proc resetCounter")
    return count


######################################################################
#
# DisableIpFilter:  获取某端口发包的字节速率
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
#     DisableIpFilter('3')
######################################################################
def DisableIpFilter(port):
    count = Dsend("--port " + str(port) + " --proc disableIpFilter")
    return count


######################################################################
#
# DisableMacFilter:  获取某端口发包的字节速率
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
#     DisableMacFilter('3')
######################################################################
def DisableMacFilter(port):
    count = Dsend("--port " + str(port) + " --proc disableMacFilter")
    return count


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
def StartDsendCapture(*arg, **args):
    res = 0
    if 'capFilter' in args:
        strFilter = '\'' + args['capFilter'] + '\''
        strFilter = re.sub(' and ', '\' and \'', strFilter)
        strFilter = re.sub(' or ', '\' or \'', strFilter)
        strFilter = re.sub(' ', '_', strFilter)
        for port in arg:
            resx = Dcapture("--port " + str(port) + " --proc startCapture --capFilter " + strFilter)
            res = int(res) + int(resx)
    else:
        for port in arg:
            resx = Dcapture("--port " + str(port) + " --proc startCapture ")
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
#           SrcMac: 源mac
#           DstMac: 目的mac
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
                
                # ACK
        if 'ACK' in args:
            ret = ret * CheckACKInData(args['ACK'], data)
            if i == 1:
                character = character + ' ACK ' + str(args['ACK'])
        
        # SYN
        if 'SYN' in args:
            ret = ret * CheckSYNInData(args['SYN'], data)
            if i == 1:
                character = character + ' SYN ' + str(args['SYN'])
        
        # FIN
        if 'FIN' in args:
            ret = ret * CheckFINInData(args['FIN'], data)
            if i == 1:
                character = character + ' FIN ' + str(args['FIN'])
        
        # RST
        if 'RST' in args:
            ret = ret * CheckRSTInData(args['RST'], data)
            if i == 1:
                character = character + ' RST ' + str(args['RST'])
        
        # PSH
        if 'PSH' in args:
            ret = ret * CheckPSHInData(args['PSH'], data)
            if i == 1:
                character = character + ' PSH ' + str(args['PSH'])
        
        # URG
        if 'URG' in args:
            ret = ret * CheckURGInData(args['URG'], data)
            if i == 1:
                character = character + ' URG ' + str(args['URG'])
        
        # protocolEx
        if 'ProtocolEx' in args:
            ret = ret * CheckProtocolExInData(args['ProtocolEx'], data)
            if i == 1:
                character = character + ' ProtocolEx ' + str(args['ProtocolEx'])
        
        # Dot1xType
        if 'Dot1xType' in args:
            ret = ret * CheckDot1xTypeInData(args['Dot1xType'], data)
            if i == 1:
                character = character + ' Dot1xType ' + str(args['Dot1xType'])
        
        # Dot1xCode
        if 'Dot1xCode' in args:
            ret = ret * CheckDot1xCodeInData(args['Dot1xCode'], data)
            if i == 1:
                character = character + ' Dot1xCode ' + str(args['Dot1xCode'])
        
        # Dot1xProType
        if 'Dot1xProType' in args:
            ret = ret * CheckDot1xProTypeInData(args['Dot1xProType'], data)
            if i == 1:
                character = character + ' Dot1xProType ' + str(args['Dot1xProType'])
        
        # EthernetType
        if 'EthernetType' in args:
            ret = ret * CheckEthernetTypeInData(args['EthernetType'], data)
            if i == 1:
                character = character + ' EthernetType ' + str(args['EthernetType'])
        ######  添加报文结束 #####
        # DSCP
        if 'DSCP' in args:
            ret = ret * CheckDSCPInData(args['DSCP'], data)
            if i == 1:
                character = character + ' DSCP ' + str(args['DSCP'])
        # Ipprecedence
        if 'Ipprecedence' in args:
            ret = ret * CheckIpprecedenceInData(args['Ipprecedence'], data)
            if i == 1:
                character = character + ' Ipprecedence ' + str(args['Ipprecedence'])
        
        # CUSTOM BYTE
        if 'HEX' in args:
            if 'StartByte' in args and 'EndByte' in args:
                ret = ret * CheckHEXInData(args['HEX'], data, args['StartByte'], args['EndByte'])
            else:
                ret = ret * CheckHEXInData(args['HEX'], data)
            if i == 0:
                character = character + ' HEX ' + str(args['HEX'])
        
        # CUSTOM BIT
        if 'BIT' in args:
            if 'ByteOffset' in args and 'BitOffset' in args:
                ret = ret * CheckBITInData(args['BIT'], data, args['ByteOffset'], args['BitOffset'])
                if i == 0:
                    character = character + ' BIT ' + str(args['BIT']) + ' Byte offset ' + args[
                        'ByteOffset'] + ' Bit offset ' + args['BitOffset']
        
        # Flowlabel
        if 'Flowlabel' in args:
            ret = ret * CheckFlowlabelInData(args['Flowlabel'], data)
            if i == 1:
                character = character + ' Flowlabel ' + str(args['Flowlabel'])
        
        if ret != 0:
            counter = counter + 1
        else:
            pass
    
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
                        if data[48:53] == '81 00' or data[48:53] == '91 00' or data[48:53] == '92 00':
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
        
        #######################################################


# CheckACKInData :检查抓到的流ACK是否满足要求
#
#   args:
#                record: true or false
#                data: actual frame data
#
#   return: 
#                1 :满足要求
#                0:不满足要求
#
# examples:
#           CheckDsendCaptureStream('2',ACK='true')
########################################################## 
def CheckACKInData(record, data):
    # Get tcp ACK from data
    flag = data[36:41]
    if flag == '81 00':
        TcpFlag = data[153:155]
        TcpFlag = '0x0' + TcpFlag
        TcpFlag = int(TcpFlag, 16)
    else:
        TcpFlag = data[141:143]
        TcpFlag = '0x0' + TcpFlag
        TcpFlag = int(TcpFlag, 16)
    if ((TcpFlag & 16 == 16) and (record == 'true')) or ((TcpFlag & 16 != 16) and (record == 'false')):
        return 1
    else:
        return 0


#######################################################
# CheckSYNInData :检查抓到的流SYN是否满足要求
#
#   args:
#                record: true or false
#                data: actual frame data
#
#   return: 
#                1 :满足要求
#                0:不满足要求
#
# examples:
#           CheckDsendCaptureStream('2',SYN='true')
########################################################## 
def CheckSYNInData(record, data):
    # Get tcp SYN from data
    flag = data[36:41]
    if flag == '81 00':
        TcpFlag = data[153:155]
        TcpFlag = '0x0' + TcpFlag
        TcpFlag = int(TcpFlag, 16)
    else:
        TcpFlag = data[141:143]
        TcpFlag = '0x0' + TcpFlag
        TcpFlag = int(TcpFlag, 16)
    if ((TcpFlag & 2 == 2) and (record == 'true')) or ((TcpFlag & 2 != 2) and (record == 'false')):
        return 1
    else:
        return 0


#######################################################
# CheckFINInData :检查抓到的流FIN是否满足要求
#
#   args:
#                record: true or false
#                data: actual frame data
#
#   return: 
#                1 :满足要求
#                0:不满足要求
#
# examples:
#           CheckDsendCaptureStream('2',FIN='true')
########################################################## 
def CheckFINInData(record, data):
    # Get tcp FIN from data
    flag = data[36:41]
    if flag == '81 00':
        TcpFlag = data[153:155]
        TcpFlag = '0x0' + TcpFlag
        TcpFlag = int(TcpFlag, 16)
    else:
        TcpFlag = data[141:143]
        TcpFlag = '0x0' + TcpFlag
        TcpFlag = int(TcpFlag, 16)
    if ((TcpFlag & 1 == 1) and (record == 'true')) or ((TcpFlag & 1 != 1) and (record == 'false')):
        return 1
    else:
        return 0


#######################################################
# CheckRSTInData :检查抓到的流RST是否满足要求
#
#   args:
#                record: true or false
#                data: actual frame data
#
#   return: 
#                1 :满足要求
#                0:不满足要求
#
# examples:
#           CheckDsendCaptureStream('2',RST='true')
########################################################## 
def CheckRSTInData(record, data):
    # Get tcp RST from data
    flag = data[36:41]
    if flag == '81 00':
        TcpFlag = data[153:155]
        TcpFlag = '0x0' + TcpFlag
        TcpFlag = int(TcpFlag, 16)
    else:
        TcpFlag = data[141:143]
        TcpFlag = '0x0' + TcpFlag
        TcpFlag = int(TcpFlag, 16)
    if ((TcpFlag & 4 == 4) and (record == 'true')) or ((TcpFlag & 4 != 4) and (record == 'false')):
        return 1
    else:
        return 0


#######################################################
# CheckPSHInData :检查抓到的流PSH是否满足要求
#
#   args:
#                record: true or false
#                data: actual frame data
#
#   return: 
#                1 :满足要求
#                0:不满足要求
#
# examples:
#           CheckDsendCaptureStream('2',PSH='true')
########################################################## 
def CheckPSHInData(record, data):
    # Get tcp PSH from data
    flag = data[36:41]
    if flag == '81 00':
        TcpFlag = data[153:155]
        TcpFlag = '0x0' + TcpFlag
        TcpFlag = int(TcpFlag, 16)
    else:
        TcpFlag = data[141:143]
        TcpFlag = '0x0' + TcpFlag
        TcpFlag = int(TcpFlag, 16)
    if ((TcpFlag & 8 == 8) and (record == 'true')) or ((TcpFlag & 8 != 8) and (record == 'false')):
        return 1
    else:
        return 0


#######################################################
# CheckURGInData :检查抓到的流URG是否满足要求
#
#   args:
#                record: true or false
#                data: actual frame data
#
#   return: 
#                1 :满足要求
#                0:不满足要求
#
# examples:
#           CheckDsendCaptureStream('2',URG='true')
########################################################## 
def CheckURGInData(record, data):
    # Get tcp URG from data
    flag = data[36:41]
    if flag == '81 00':
        TcpFlag = data[153:155]
        TcpFlag = '0x0' + TcpFlag
        TcpFlag = int(TcpFlag, 16)
    else:
        TcpFlag = data[141:143]
        TcpFlag = '0x0' + TcpFlag
        TcpFlag = int(TcpFlag, 16)
    if ((TcpFlag & 32 == 32) and (record == 'true')) or ((TcpFlag & 32 != 32) and (record == 'false')):
        return 1
    else:
        return 0


#######################################################
# CheckProtocolExInData :检查抓到的流ProtocolEx是否满足要求
#
#   args:
#                record: tcp, udp, rip, icmp or igmp
#                data: actual frame data
#
#   return: 
#                1 :满足要求
#                0:不满足要求
#
# examples:
#           CheckDsendCaptureStream('2',ProtocolEx='tcp')
########################################################## 
def CheckProtocolExInData(record, data):
    # Get tcp URG from data
    flag = data[36:41]
    if flag == '81 00':
        if data[48:53] == '08 00':
            protocolEx = data[81:83]
        else:
            protocolEx = data[72:74]
    else:
        if flag == '08 00':
            protocolEx = data[69:71]
        else:
            protocolEx = data[60:62]
    if record == 'tcp':
        record = 6
    elif record == 'udp':
        record = 17
    elif record == 'rip':
        record = 17
    elif record == 'icmp':
        record = 1
    elif record == 'igmp':
        record = 2
    else:
        record = -1
    strTemp = '0x0' + protocolEx
    if int(strTemp, 16) == record:
        return 1
    else:
        return 0


#######################################################
# CheckEthernetTypeInData  :检查抓到的流Ethernet Type是否满足要求
#
#   args:
#                record: tcp, udp, rip, icmp or igmp
#                data: actual frame data
#
#   return: 
#                1 :满足要求
#                0 :不满足要求
#
# examples:
#           CheckDsendCaptureStream('2',EthernetType='dot1x')
#           CheckDsendCaptureStream('4',EthernetType='08 06')
########################################################## 
def CheckEthernetTypeInData(record, data):
    # Get dot1x type from data
    flag = data[36:41]
    if flag == '81 00':
        flag = data[48:53]
    if record == '802.1x' or record == 'dot1x':
        record = '88 8E'
    elif record == 'ipv4' or record == 'IPv4':
        record = '08 00'
    elif record == 'arp' or record == 'ARP':
        record = '08 06'
    elif record == 'ipv6' or record == 'IPv6':
        record = '86 DD'
    elif record == 'ipx' or record == 'IPX':
        record = '81 37'
    if flag == record:
        return 1
    else:
        return 0


#######################################################
# CheckDSCPInData  :检查抓到的流DSCP是否满足要求
#
#   args:
#                dscp: dscp value
#                data: actual frame data
#
#   return: 
#                1 :满足要求
#                0 :不满足要求
#
# examples:
#           CheckDsendCaptureStream('4',DSCP='20')
########################################################## 
def CheckDSCPInData(dscp, data):
    # Get DSCP from data
    flag = data[36:41]
    dscpData = -1
    if flag == '81 00':
        version = data[54]
        if version == '4':
            dscpData = data[57:59]
            dscpData = '0x0' + dscpData.replace(' ', '')
            dscpData = int(dscpData, 16)
            dscpData = dscpData >> 2
        elif version == '6':
            dscpString = data[55:58]
            dscpString = dscpString[1:]
            dscpData = '0x0' + dscpString.replace(' ', '')
            dscpData = int(dscpData, 16)
            dscpData = dscpData >> 2
        else:
            version1 = data[78]
            if version1 == '4':
                dscpData = '0x0' + data[81:83].replace(' ', '')
                dscpData = int(dscpData, 16)
            elif version1 == '6':
                dscpString = data[79:82]
                dscpString = dscpString[1:]
                dscpData = '0x0' + dscpString.replace(' ', '')
                dscpData = int(dscpData, 16)
                dscpData = dscpData >> 2
    elif flag == '08 00':
        dscpData = data[45:47]
        dscpData = '0x0' + dscpData.replace(' ', '')
        dscpData = int(dscpData, 16)
        dscpData = dscpData >> 2
    elif flag == '86 DD':
        dscpString = data[43:46]
        dscpString = dscpString[1:]
        dscpData = '0x0' + dscpString.replace(' ', '')
        dscpData = int(dscpData, 16)
        dscpData = dscpData >> 2
    if int(dscp) == dscpData:
        return 1
    else:
        return 0


#######################################################
# CheckIpprecedenceInData  :检查抓到的流DSCP是否满足要求
#
#   args:
#                dscp: dscp value
#                data: actual frame data
#
#   return: 
#                1 :满足要求
#                0 :不满足要求
#
# examples:
#           CheckDsendCaptureStream('4',DSCP='20')
########################################################## 
def CheckIpprecedenceInData(dscp, data):
    # Get DSCP from data
    flag = data[36:41]
    dscpData = -1
    if flag == '81 00':
        version = data[54]
        if version == '4':
            dscpData = data[57:59]
            dscpData = '0x0' + dscpData.replace(' ', '')
            dscpData = int(dscpData, 16)
            dscpData = dscpData >> 5
        elif version == '6':
            dscpString = data[55:58]
            dscpString = dscpString[1:]
            dscpData = '0x0' + dscpString.replace(' ', '')
            dscpData = int(dscpData, 16)
            dscpData = dscpData >> 5
        else:
            version1 = data[78]
            if version1 == '4':
                dscpData = '0x0' + data[81:83].replace(' ', '')
                dscpData = int(dscpData, 16)
            elif version1 == '6':
                dscpString = data[79:82]
                dscpString = dscpString[1:]
                dscpData = '0x0' + dscpString.replace(' ', '')
                dscpData = int(dscpData, 16)
                dscpData = dscpData >> 5
    elif flag == '08 00':
        dscpData = data[45:47]
        dscpData = '0x0' + dscpData.replace(' ', '')
        dscpData = int(dscpData, 16)
        dscpData = dscpData >> 5
    elif flag == '86 DD':
        dscpString = data[43:46]
        dscpString = dscpString[1:]
        dscpData = '0x0' + dscpString.replace(' ', '')
        dscpData = int(dscpData, 16)
        dscpData = dscpData >> 5
    if int(dscp) == dscpData:
        return 1
    else:
        return 0


#######################################################
# CheckHEXInData  :检查抓到的流DSCP是否满足要求
#
#   args:
#                strHexCheck: Hex string to be checked
#                data: actual frame data
#
#   return: 
#                1 :满足要求
#                0 :不满足要求
#
# examples:
#           CheckDsendCaptureStream('4', HEX='86dd',StartByte='20',EndByte='21')
#           CheckDsendCaptureStream('4', HEX='86dd12345678')
#           CheckDsendCaptureStream('4', HEX='86dd.*?0000')
########################################################## 
def CheckHEXInData(strHexCheck, data, strStartByte='ff', strEndByte='ff'):
    # Get HEX from data
    
    strHexGot = data.replace(' ', '')
    strHexCheck = strHexCheck.replace(' ', '')
    strHexCheck = strHexCheck.upper()
    if strStartByte == 'ff' and strEndByte == 'ff':
        tmpHex = re.search(strHexCheck, strHexGot)
    else:
        strHexGot = strHexGot[int(strStartByte) * 2:int(strEndByte) * 2 + 2]
        tmpHex = re.search(strHexCheck, strHexGot)
    if tmpHex is not None:
        return 1
    else:
        return 0


#######################################################
# CheckBITInData  :检查抓到的流DSCP是否满足要求
#
#   args:
#                strBITCheck: Bit to be checked '0' or '1'
#                data: actual frame data
#                strByteOffset:Byte offset which bit in ,start with '0'
#                strBitOffset:Bit offset in byte '1' to '8'(left to right)
#
#   return: 
#                1 :满足要求
#                0 :不满足要求
#
# examples:
#           CheckDsendCaptureStream('4',DstMac='FF-FF-FF-FF-FF-FF', BIT='0',ByteOffset='20',BitOffset='4')
########################################################## 
def CheckBITInData(strBITCheck, data, strByteOffset='0', strBitOffset='0'):
    # Get BIT from data
    
    strHexGot = data.replace(' ', '')
    strBITCheck = strBITCheck.replace(' ', '')
    tmpByte = strHexGot[int(strByteOffset) * 2:int(strByteOffset) * 2 + 2]
    tmpByte = int(tmpByte, 16)
    if strBitOffset == '8':
        if ((tmpByte & 1 == 1) and (strBITCheck == '1')) or ((tmpByte & 1 != 1) and (strBITCheck == '0')):
            return 1
        else:
            return 0
    elif strBitOffset == '7':
        if ((tmpByte & 2 == 2) and (strBITCheck == '1')) or ((tmpByte & 2 != 2) and (strBITCheck == '0')):
            return 1
        else:
            return 0
    elif strBitOffset == '6':
        if ((tmpByte & 4 == 4) and (strBITCheck == '1')) or ((tmpByte & 4 != 4) and (strBITCheck == '0')):
            return 1
        else:
            return 0
    elif strBitOffset == '5':
        if ((tmpByte & 8 == 8) and (strBITCheck == '1')) or ((tmpByte & 8 != 8) and (strBITCheck == '0')):
            return 1
        else:
            return 0
    elif strBitOffset == '4':
        if ((tmpByte & 16 == 16) and (strBITCheck == '1')) or ((tmpByte & 16 != 16) and (strBITCheck == '0')):
            return 1
        else:
            return 0
    elif strBitOffset == '3':
        if ((tmpByte & 32 == 32) and (strBITCheck == '1')) or ((tmpByte & 32 != 32) and (strBITCheck == '0')):
            return 1
        else:
            return 0
    elif strBitOffset == '2':
        if ((tmpByte & 64 == 64) and (strBITCheck == '1')) or ((tmpByte & 64 != 64) and (strBITCheck == '0')):
            return 1
        else:
            return 0
    elif strBitOffset == '1':
        if ((tmpByte & 128 == 128) and (strBITCheck == '1')) or ((tmpByte & 128 != 128) and (strBITCheck == '0')):
            return 1
        else:
            return 0
    else:
        return 0


#######################################################
# CheckFlowlabelInData :检查抓到的流Flowlabel是否满足要求
#
#   args:
#                record: tcp, udp, rip, icmp or igmp
#                data: actual frame data
#
#   return: 
#                1 :满足要求
#                0:不满足要求
#
# examples:
#           CheckDsendCaptureStream('2',Flowlabel='1')
########################################################## 
def CheckFlowlabelInData(record, data):
    # Get tcp Flowlabel from data
    flag = data[36:41]
    if flag == '81 00':
        flowLabel = data[58:65]
    else:
        flowLabel = data[46:53]
    flowLabel = flowLabel.replace(' ', '')
    flowLabel = int(flowLabel, 16)
    
    if int(record) == flowLabel:
        return 1
    else:
        return 0


#######################################################
# GetEUI64Address :
#
#   args:
#                cpumac: 要转换的mac地址
#
#   return: 
#                转换后的地址
#
# examples:
#           GetEUI64Address("00-00-00-00-01-01")
########################################################## 
def GetEUI64Address(cpumac):
    eui64address1 = cpumac[0:8] + "-ff-fe-" + cpumac[9:17]
    str1 = "0x" + str(eui64address1[0:2])
    str2 = str(eui64address1[2:23])
    str1 = str("%02x" % (int(str1, 16) | 0o2))
    eui64address2 = str1 + str2
    return eui64address2


#######################################################
# GetLinkLocalAddress : 计算本地链路地址
#
#   args:
#                cpumac: 要转换的mac地址
#
#   return: 
#                转换后的地址
#
# examples:
#           GetLinkLocalAddress("00-00-00-00-01-01")
########################################################## 
def GetLinkLocalAddress(cpumacorip):
    res = cpumacorip.find('-')
    if res >= 0:
        eui64address = GetEUI64Address(cpumacorip)
        part1 = eui64address[0:2] + eui64address[3:5]
        part2 = eui64address[6:8] + eui64address[9:11]
        part3 = eui64address[12:14] + eui64address[15:17]
        part4 = eui64address[18:20] + eui64address[21:23]
        str1 = str("%x" % (int("0x" + str(part1), 16)))
        str2 = str("%x" % (int("0x" + str(part2), 16)))
        str3 = str("%x" % (int("0x" + str(part3), 16)))
        str4 = str("%x" % (int("0x" + str(part4), 16)))
        linklocaladdress = "fe80::" + str1 + ":" + str2 + ":" + str3 + ":" + str4
        return linklocaladdress
    else:
        iplist = cpumacorip.split('.')
        str1 = str("%x" % (int(iplist[0])))
        str2 = str("%02x" % (int(iplist[1])))
        str3 = str("%x" % (int(iplist[2])))
        str4 = str("%02x" % (int(iplist[3])))
        linklocaladdress = "fe80::" + str1 + str2 + ":" + str3 + str4
        return linklocaladdress
