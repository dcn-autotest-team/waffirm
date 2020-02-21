#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# waffirm_4.11.1py - test case 4.11.1of waffirm_new
#
# Author:  ()
#
# Version 1.0.0
#
# Copyright (c) 2004-2013 Digital China Networks Co. Ltd
#
# Features:
# 4.11.1     wsGlobalConfig组节点测试
# 测试目的：检查wsGlobalConfig组私有mib节点。
# 测试环境：同测试拓扑
# 测试描述：通过get/write检查各个节点的值是否正确。执行snmpwalk能够读出相应的表节点。
#
#*******************************************************************************
# Change log:
#     - 
#*******************************************************************************

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase 4.11.1'
avoiderror(testname)
printTimer(testname,'Start','wsGlobalConfig group node test')

################################################################################
#Step 1
#操作
#PC1安装snmp管理软件，推荐使用SNMPc，EC view, LinkManager，并指定正确的私有mib路由。
#
#预期
# 网管软件安装成功。
################################################################################
printStep(testname,'Step 1',
          'Install snmp management software on PC1')
EnterEnableMode(switch1)
data1 = SetCmd(switch1,'show vendor')
tmpRe = re.search('VendorOid\s+\d+\s+(.+?)\n',data1)
if tmpRe is not None:
    oid = tmpRe.group(1).strip()
    print('Get oid from vendor file')
else:
    oid = '1.3.6.1.4.1.6339'
    print('Cannot get oid from vendor file, set to dcn default')
res1 = 0

#result
printCheckStep(testname, 'Step 1',res1)

################################################################################
#Step 2
#操作
#在AC1上ping PC1。
#
#预期
#能够ping通。
################################################################################
printStep(testname,'Step 2',
          'Ap img download start')

res1 = CheckPing(pc1,StaticIpv4_ac1,mode='linux',srcip=pc1_ipv4)

#result
printCheckStep(testname, 'Step 2',res1)



################################################################################
#Step 3
#操作
#AC1进行SNMP 配置：
#snmp-server enable
#snmp-server securityip disable
#snmp-server community rw xxxxxx
#PC1启动SNMP 管理软件后进行相应的配置（community 要匹配）
#配置成功。在PC1上面通过SNMP软件可以浏览AC1的私有mib库。
################################################################################
printStep(testname,'Step 3',
          'Config snmp server on ac1')
EnterConfigMode(switch1)
SetCmd(switch1,'snmp-server enable')
SetCmd(switch1,'snmp-server securityip disable')
SetCmd(switch1,'snmp-server community rw 0 public')

data1 = SetCmd(switch1,'show run')

res1 = CheckLine(data1,'snmp-server enable')
printCheckStep(testname, 'Step 3',res1)
               
################################################################################
#Step 4
#操作
#wsMode
#读取/设置无线全局的开启/关闭状态。OID = 1.3.6.1.4.1.6339.103.1.1.1。
#Value：1enable,2disable。
################################################################################
printStep(testname,'Step 4',
          'wsMode')

data1 = SetCmd(pc1,'snmpwalk -v 2c -c public ' + StaticIpv4_ac1 +  ' ' + oid + '.103.1.1.1')

res1 = CheckLine(data1,'INTEGER: 1')
printCheckStep(testname, 'Step 4',res1)

################################################################################
#Step 5
#操作
#wsCountryCode
#读取/设置国家码。Object ID =1.3.6.1.4.1.6339.103.1.1.2。
################################################################################
printStep(testname,'Step 5',
          'wsCountryCode')

data1 = SetCmd(pc1,'snmpwalk -v 2c -c public ' + StaticIpv4_ac1 +  ' ' + oid + '.103.1.1.2')

res1 = CheckLine(data1,'43 4E 00')
printCheckStep(testname, 'Step 5',res1)

################################################################################
#Step 6
#操作
#wsMode
#读取/设置AC的集群标识group-id。范围1-255，默认为1。Object ID = 1.3.6.1.4.1.6339.103.1.1.3。
################################################################################
printStep(testname,'Step 6',
          'wsPeerGroupId')

data1 = SetCmd(pc1,'snmpwalk -v 2c -c public ' + StaticIpv4_ac1 +  ' ' + oid + '.103.1.1.3')

res1 = CheckLine(data1,'INTEGER: 1')
printCheckStep(testname, 'Step 6',res1)

################################################################################
#Step 7
#操作
#wsAPValidationMethod
#读取/设置AP的认证方式。Object ID =  1.3.6.1.4.1.6339.103.1.1.4。
#Value：1local,2radius。
################################################################################
printStep(testname,'Step 7',
          'wsAPValidationMethod')

data1 = SetCmd(pc1,'snmpwalk -v 2c -c public ' + StaticIpv4_ac1 +  ' ' + oid + '.103.1.1.4')

res1 = CheckLine(data1,'INTEGER: 1')
printCheckStep(testname, 'Step 7',res1)

################################################################################
#Step 8
#操作
#wsAPAuthenticationMode
#读取/设置AP与AC连接时是否需要进行身份验证。Object ID =  1.3.6.1.4.1.6339.103.1.1.5。
#Value：0-none，1-radius,2-pass-phrase。
################################################################################
printStep(testname,'Step 8',
          'wsAPAuthenticationMode')

data1 = SetCmd(pc1,'snmpwalk -v 2c -c public ' + StaticIpv4_ac1 +  ' ' + oid + '.103.1.1.5')

res1 = CheckLine(data1,'INTEGER: 0')
printCheckStep(testname, 'Step 8',res1)

################################################################################
#Step 9
#操作
#wsAPMacAddress
#读取AP的mac地址。Object ID =  1.3.6.1.4.1.6339.103.1.1.11.1.1。该值与AC1上面ap database一致。
################################################################################
printStep(testname,'Step 9',
          'wsAPMacAddress')

data1 = SetCmd(pc1,'snmpwalk -v 2c -c public ' + StaticIpv4_ac1 +  ' ' + oid + '.103.1.1.11.1.1')

res1 = CheckLine(data1,re.sub('-',' ',ap1mac),IC=True)
res2 = CheckLine(data1,re.sub('-',' ',ap2mac),IC=True)
printCheckStep(testname, 'Step 9',res1,res2)

################################################################################
#Step 10
#操作
#wsAPLocation
#读取/设置AP的位置描述信息。Object ID = 1.3.6.1.4.1.6339.103.1.1.11.1.2。
################################################################################
printStep(testname,'Step 10',
          'wsAPLocation')

data1 = SetCmd(pc1,'snmpwalk -v 2c -c public ' + StaticIpv4_ac1 +  ' ' + oid + '.103.1.1.11.1.2')

res1 = CheckLine(data1,'= ''')
printCheckStep(testname, 'Step 10',res1)

################################################################################
#Step 11
#操作
#wsAPMode
#读取/设置AP的工作模式。Object ID =  1.3.6.1.4.1.6339.103.1.1.11.1.3。
#Value：1wsManaged（缺省值），2standalone，3rogue。
################################################################################
printStep(testname,'Step 11',
          'wsAPMode')

data1 = SetCmd(pc1,'snmpwalk -v 2c -c public ' + StaticIpv4_ac1 +  ' ' + oid + '.103.1.1.11.1.3')

res1 = CheckLine(data1,'INTEGER: 1')
printCheckStep(testname, 'Step 11',res1)

################################################################################
#Step 12
#操作
#wsUseAPProfileId
#读取/设置AP Profile的ID。范围1~16。OID = 1.3.6.1.4.1.6339.103.1.1.11.1.5。
################################################################################
printStep(testname,'Step 12',
          'wsUseAPProfileId')

data1 = SetCmd(pc1,'snmpwalk -v 2c -c public ' + StaticIpv4_ac1 +  ' ' + oid + '.103.1.1.11.1.5')

res1 = CheckLine(data1,'INTEGER: 1')
res2 = CheckLine(data1,'INTEGER: 2')
printCheckStep(testname, 'Step 12',res1,res2)

################################################################################
#Step 13
#操作
#wsAPRadio1Channel
#读取/设置Radio 1的信道。缺省为0，即自动调整信道。
#OID=  1.3.6.1.4.1.6339.103.1.1.11.1.6。
################################################################################
printStep(testname,'Step 13',
          'wsAPRadio1Channel')

data1 = SetCmd(pc1,'snmpwalk -v 2c -c public ' + StaticIpv4_ac1 +  ' ' + oid + '.103.1.1.11.1.6')

res1 = CheckLine(data1,'INTEGER: 0')
printCheckStep(testname, 'Step 13',res1)


################################################################################
#Step 14
#操作
#wsAPRadio1TxPower
#读取/设置Radio 1的传输功率。Range = -1, 0..100，缺省为0，即自动调整功率。
#OID=  1.3.6.1.4.1.6339.103.1.1.11.1.8。
################################################################################
printStep(testname,'Step 14',
          'wsAPRadio1TxPower')

data1 = SetCmd(pc1,'snmpwalk -v 2c -c public ' + StaticIpv4_ac1 +  ' ' + oid + '.103.1.1.11.1.8')

res1 = CheckLine(data1,'INTEGER: 0')
printCheckStep(testname, 'Step 14',res1)


################################################################################
#Step 15
#操作
#wsIPAddress
#读取AC的无线IPv4地址。Object ID = 1.3.6.1.4.1.6339.103.1.1.12.1。
################################################################################
printStep(testname,'Step 15',
          'wsIPAddress')

data1 = SetCmd(pc1,'snmpwalk -v 2c -c public ' + StaticIpv4_ac1 +  ' ' + oid + '.103.1.1.12.1')

res1 = CheckLine(data1,StaticIpv4_ac1)
printCheckStep(testname, 'Step 15',res1)


################################################################################
#Step 16
#操作
#wsTotalPeerSwitches
#读取网络中可以探测到的peer-switch的总数，0~64。Object ID = 1.3.6.1.4.1.6339.103.1.1.12.4。
################################################################################
printStep(testname,'Step 16',
          'wsTotalPeerSwitches')

EnterEnableMode(switch1)
data = SetCmd(switch1,'show wireless peer-switch')
restmp = re.findall('\d+\.\d+\.\d+\.\d+\s+',data)
res = len(restmp)

data1 = SetCmd(pc1,'snmpwalk -v 2c -c public ' + StaticIpv4_ac1 +  ' ' + oid + '.103.1.1.12.4')

res1 = CheckLine(data1,'INTEGER: ' + str(res))
printCheckStep(testname, 'Step 16',res1)


################################################################################
#Step 17
#操作
#wsTotalAPs
#读取无线局域网交换机管理的AP、连接失败的AP和发现的AP总数。Object ID = 1.3.6.1.4.1.6339.103.1.1.12.5。
################################################################################
printStep(testname,'Step 17',
          'wsTotalAPs')

data1 = SetCmd(pc1,'snmpwalk -v 2c -c public ' + StaticIpv4_ac1 +  ' ' + oid + '.103.1.1.12.5')

res1 = CheckLine(data1,'Gauge32: 2')
printCheckStep(testname, 'Step 17',res1)


################################################################################
#Step 18
#操作
#wsTotalManagedAPs
#读取无线网络中无线交换机管理的AP的数量。Object ID = 1.3.6.1.4.1.6339.103.1.1.12.6。
################################################################################
printStep(testname,'Step 18',
          'wsTotalManagedAPs')

data1 = SetCmd(pc1,'snmpwalk -v 2c -c public ' + StaticIpv4_ac1 +  ' ' + oid + '.103.1.1.12.6')

res1 = CheckLine(data1,'INTEGER: 2')
printCheckStep(testname, 'Step 18',res1)


################################################################################
#Step 19
#操作
#wsTotalConnectionFailedAPs
#读取通过交换机的验证并被交换机管理但当前与交换机失去连接的AP的数量。
#Object ID = 1.3.6.1.4.1.6339.103.1.1.12.9
################################################################################
printStep(testname,'Step 19',
          'wsTotalConnectionFailedAPs')

data1 = SetCmd(pc1,'snmpwalk -v 2c -c public ' + StaticIpv4_ac1 +  ' ' + oid + '.103.1.1.12.9')

res1 = CheckLine(data1,'Gauge32: 0')
printCheckStep(testname, 'Step 19',res1)


################################################################################
#Step 20
#操作
#wsMaximumManagedAPsInPeerGroup
#读取AC Controller可以管理的 AP数的最大值。Object ID = 1.3.6.1.4.1.6339.103.1.1.12.12。
################################################################################
printStep(testname,'Step 20',
          'wsMaximumManagedAPsInPeerGroup')

data1 = SetCmd(pc1,'snmpwalk -v 2c -c public ' + StaticIpv4_ac1 +  ' ' + oid + '.103.1.1.12.12')
data2 = SetCmd(switch1,'show wireless status')
num1 = re.search('Maximum Managed APs in Peer Group.............. (\d+)',data2)
if num1 is not None:
    res1 = CheckLine(data1,'Gauge32: ' + num1.group(1))
else:
    res1 = 1
printCheckStep(testname, 'Step 20',res1)


################################################################################
#Step 21
#操作
#wsTotalClients
#读取网络中客户端的总数量。Object ID = 1.3.6.1.4.1.6339.103.1.1.12.13。
################################################################################
printStep(testname,'Step 21',
          'wsTotalClients')
data0 = SetCmd(switch1,'show wireless client status')


data1 = SetCmd(pc1,'snmpwalk -v 2c -c public ' + StaticIpv4_ac1 +  ' ' + oid + '.103.1.1.12.13')

re1 = re.search('To Local Switch....... (\d+)',data0)
if re1 is not None:
    res1 = CheckLine(data1,'Gauge32: ' + re1.group(1))
else:
    res1 = CheckLine(data1,'Gauge32: 0')
printCheckStep(testname, 'Step 21',res1)


################################################################################
#Step 22
#操作
#wsTotalAuthenticatedClients
#读取网络中通过认证的客户端的总数量。Object ID = 1.3.6.1.4.1.6339.103.1.1.12.14。
################################################################################
printStep(testname,'Step 22',
          'wsTotalAuthenticatedClients')

data0 = SetCmd(switch1,'show wireless client status')

data1 = SetCmd(pc1,'snmpwalk -v 2c -c public ' + StaticIpv4_ac1 +  ' ' + oid + '.103.1.1.12.14')

re1 = re.search('To Local Switch....... (\d+)',data0)
if re1 is not None:
    res1 = CheckLine(data1,'Gauge32: ' + re1.group(1))
else:
    res1 = CheckLine(data1,'Gauge32: 0')
printCheckStep(testname, 'Step 22',res1)


################################################################################
#Step 23
#操作
#wsMaximumAssociatedClients
#读取无线系统可支持客户端数量的最大值。Object ID = 1.3.6.1.4.1.6339.103.1.1.12.15。
################################################################################
printStep(testname,'Step 23',
          'wsMaximumAssociatedClients')

data1 = SetCmd(pc1,'snmpwalk -v 2c -c public ' + StaticIpv4_ac1 +  ' ' + oid + '.103.1.1.12.15')
data2 = SetCmd(switch1,'show wireless status')
num1 = re.search('Maximum Associated Clients..................... (\d+)',data2)
if num1 is not None:
    res1 = CheckLine(data1,'Gauge32: ' + num1.group(1))
else:
    res1 = 1
    
printCheckStep(testname, 'Step 23',res1)

################################################################################
#Step 24
#操作
#wsNetworkMutualAuthenticationStatus
#读取双向认证的状态。Object ID = 1.3.6.1.4.1.6339.103.1.1.12.39。
#Values = (1: not-started), 
#(2: exchange-start), 
#(3: in-progress), 
#(4: provisioning-in-progress), 
#(5: exchange-in-progress), 
#(6: provisioning-complete), 
#(7: exchange-complete), 
#(8: complete-without-errors), 
#(9: complete-with-errors)
################################################################################
printStep(testname,'Step 24',
          'wsNetworkMutualAuthenticationStatus')

data1 = SetCmd(pc1,'snmpwalk -v 2c -c public ' + StaticIpv4_ac1 +  ' ' + oid + '.103.1.1.12.39')

res1 = CheckLine(data1,'INTEGER: 1')
printCheckStep(testname, 'Step 24',res1)


################################################################################
#Step 25
#操作
#wsClusterPriority
#读取/设置成为AC Controller的优先级。Object ID = 1.3.6.1.4.1.6339.103.1.1. 16。范围：0~255，缺省为0。
################################################################################
printStep(testname,'Step 25',
          'wsClusterPriority')

data1 = SetCmd(pc1,'snmpwalk -v 2c -c public ' + StaticIpv4_ac1 +  ' ' + oid + '.103.1.1.16')

res1 = CheckLine(data1,'Gauge32: 1')
printCheckStep(testname, 'Step 25',res1)


################################################################################
#Step 26
#操作
#wsAPClientQosMode
#读取/设置AP为客户端提供的QoS模式。Object ID = 1.3.6.1.4.1.6339.103.1.1. 17。
#Value：1enable,2disable。缺省为2。
################################################################################
printStep(testname,'Step 26',
          'wsAPClientQosMode')

data1 = SetCmd(pc1,'snmpwalk -v 2c -c public ' + StaticIpv4_ac1 +  ' ' + oid + '.103.1.1.17')

res1 = CheckLine(data1,'INTEGER: 2')
printCheckStep(testname, 'Step 26',res1)


################################################################################
#Step 27
#操作
#wsAPAutoUpgradeMode
#读读取/设置AP自动更新的模式。Object ID = 1.3.6.1.4.1.6339.103.1.1. 18。
#Value：1enable,2disable。缺省为2。
################################################################################
printStep(testname,'Step 27',
          'wsAPAutoUpgradeMode')

data1 = SetCmd(pc1,'snmpwalk -v 2c -c public ' + StaticIpv4_ac1 +  ' ' + oid + '.103.1.1.18')

res1 = CheckLine(data1,'INTEGER: 2')
printCheckStep(testname, 'Step 27',res1)


################################################################################
#Step 28
#操作
#wsAutoIPAssignMode
#读取/设置自动配置IP地址的模式。Object ID = 1.3.6.1.4.1.6339.103.1.1. 29。
#Value：1enable,2disable。
################################################################################
printStep(testname,'Step 28',
          'wsAutoIPAssignMode')

data1 = SetCmd(pc1,'snmpwalk -v 2c -c public ' + StaticIpv4_ac1 +  ' ' + oid + '.103.1.1.29')

res1 = CheckLine(data1,'INTEGER: 2')
printCheckStep(testname, 'Step 28',res1)


################################################################################
#Step 29
#操作
#wsSwitchStaticIPAddress
#读取/设置静态配置IPv4地址。Object ID = 1.3.6.1.4.1.6339.103.1.1.30。
################################################################################
printStep(testname,'Step 29',
          'wsSwitchStaticIPAddress')

data1 = SetCmd(pc1,'snmpwalk -v 2c -c public ' + StaticIpv4_ac1 +  ' ' + oid + '.103.1.1.30')

res1 = CheckLine(data1,StaticIpv4_ac1)
printCheckStep(testname, 'Step 29',res1)


################################################################################
#Step 30
#操作
#Return to initial
################################################################################
printStep(testname,'Step 30',
          'Return to initial')

EnterConfigMode(switch1)
SetCmd(switch1,'no snmp-server enable')

printCheckStep(testname, 'Step 30',res1)





#end
printTimer(testname, 'End')
