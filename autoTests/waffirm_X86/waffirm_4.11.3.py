#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# waffirm_4.11.3.py - test case 4.11.3 of waffirm_new
#
# Author:  ()
#
# Version 1.0.0
#
# Copyright (c) 2004-2013 Digital China Networks Co. Ltd
#
# Features:
# 4.11.3     wsNetworkTable组节点测试
# 测试目的：检查wsNetworkTable组私有mib节点。
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

testname = 'TestCase 4.11.3'
printTimer(testname,'Start','wsNetworkTable group node test')

################################################################################
#Step 1
#操作
#PC1安装snmp管理软件，推荐使用SNMPc，EC view, LinkManager，并指定正确的私有mib路由。
#
#预期
# 网管软件安装成功。
################################################################################
printStep(testname,'Step 1',\
                   'Install snmp management software on PC1')
EnterEnableMode(switch1)
data1 = SetCmd(switch1,'show vendor')
tmpRe = re.search('VendorOid\s+\d+\s+(.+?)\n',data1)
if tmpRe is not None:
    oid = tmpRe.group(1).strip()
    print 'Get oid from vendor file'
else:
    oid = '1.3.6.1.4.1.6339'
    print 'Cannot get oid from vendor file, set to dcn default'
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
printStep(testname,'Step 2',\
          'Ap img download start')

res1 = CheckPing(pc1,StaticIpv4_ac1,mode='linux',srcip=pc1_ipv4)

#result
printCheckStep(testname, 'Step 2',0)

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
printStep(testname,'Step 3',\
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
#wsNetworkId
#读取网络ID。Object ID =  1.3.6.1.4.1.6339.103.1.3.8.1.1。范围：1~64。
################################################################################
printStep(testname,'Step 4',\
          'wsNetworkId')

data1 = SetCmd(pc1,'snmpwalk -v 2c -c public ' + StaticIpv4_ac1 +  ' ' + oid + '.103.1.3.8.1.1')

res1 = CheckLine(data1,'INTEGER: 1')
res2 = CheckLine(data1,'INTEGER: 16')
res3 = CheckLine(data1,'INTEGER: 17')
printCheckStep(testname, 'Step 4',res1,res2,not res3)

################################################################################
#Step 5
#操作
#wsNetworkSSID
#读取/设置网络的SSID。Object ID =  1.3.6.1.4.1.6339.103.1.3.8.1.3。
################################################################################
printStep(testname,'Step 5',\
          'wsNetworkSSID')

data1 = SetCmd(pc1,'snmpwalk -v 2c -c public ' + StaticIpv4_ac1 +  ' ' + oid + '.103.1.3.8.1.3')

res1 = CheckLine(data1,Network_name1)
res2 = CheckLine(data1,Network_name2)
printCheckStep(testname, 'Step 5',res1,res2)

################################################################################
#Step 6
#操作
#wsNetworkDefaultVLANId
#读取/设置网络的默认vlan id。Object ID =  1.3.6.1.4.1.6339.103.1.3.8.1.4。范围：1~4094。
################################################################################
printStep(testname,'Step 6',\
          'wsNetworkDefaultVLANId')

data1 = SetCmd(pc1,'snmpwalk -v 2c -c public ' + StaticIpv4_ac1 +  ' ' + oid + '.103.1.3.8.1.4')

res1 = CheckLine(data1,Vlan4092)
res2 = CheckLine(data1,Vlan4092)

printCheckStep(testname, 'Step 6',res1,res2)

################################################################################
#Step 7
#操作
#Return to initial
################################################################################
printStep(testname,'Step 7',\
          'Return to initial')

EnterConfigMode(switch1)
SetCmd(switch1,'no snmp-server enable')

printCheckStep(testname, 'Step 7',0)
#end
printTimer(testname, 'End')