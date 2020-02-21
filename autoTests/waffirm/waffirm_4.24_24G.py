#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# waffirm_4.24.py - test case 4.24 of waffirm
#
# Author:  fuzf@digitalchina.com
#
# Version 1.0.0
#
# Copyright (c) 2004-2012 Digital China Networks Co. Ltd
#
# Features:
# 4.24 RF-PING
# 测试目的：AP的RF-PING功能。
# 测试环境：同测试拓扑
# 测试描述：Client关联之后，通过RF-PING功能可以检测client与AP之间的无线链路质量
#          （STA1的MAC地址：STA1MAC）
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

testname = 'TestCase 4.24'
avoiderror(testname)
printTimer(testname,'Start',"RF-PING")
# 2.4G、5G差异化配置,test24gflag为True代表执行2.4G脚本，False代表执行5G脚本
if test24gflag ==  True:
    ath = 'ath0'
else:
    ath = 'ath16'   
################################################################################
#Step 1
#操作
# 无，step1的配置同初始化配置，可以直接pass，为了跟测试例对应上，脚本中必现有此步骤
#
#预期
# 直接pass
################################################################################
printStep(testname,'Step 1',\
          'same with initial configuration,pass')

res1=0
#operate

#result
printCheckStep(testname, 'Step 1',res1)

################################################################################
#Step 2
#操作
# STA1关联test1
#
#预期
#STA1关联test1成功
################################################################################
printStep(testname,'Step 2',\
          'STA1 connect test1')

res1=res2=res3=res4=1
#operate
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,bssid=ap1mac_lower,checkDhcpAddress=Dhcp_pool1)

if 0!=res1:
    printRes('Error:STA1 can not connect to test1')

# data1 = SetCmd(sta1,'ifconfig -v',Netcard_sta1)
# SearchResult1 = re.search('inet.+?(\d+\.\d+\.\d+\.\d+)\s+',data1,re.I)
# #printRes('SearchResult1.group(1):'+SearchResult1.group(1).strip())
# if None != SearchResult1:
    # if re.search(Dhcp_pool1,SearchResult1.group(1).strip(),re.I) !=None:
        # res2 = 0

#result
printCheckStep(testname, 'Step 2',res1)
# 如果客户端无法关联network或无法获取IP，则不执行后续步骤
keeponflag = res1
if GetWhetherkeepon(keeponflag):
    ################################################################################
    #Step 3
    #操作
    # STA1关联ping PC1
    #
    #预期
    #STA1可以ping通PC1
    ################################################################################
    printStep(testname,'Step 3',\
              'STA1 ping PC1 succeed')

    res1=1
    #operate
    res1=CheckPing(sta1,pc1_ipv4,mode='linux')

    #check
    if 0 != res1:
        printRes('Failed:STA1 ping PC1 failed!')

    #result
    printCheckStep(testname, 'Step 3',res1)


    ################################################################################
    #Step 4
    #操作
    #在AC1上执行wireless link-test STA1MAC
    #
    #预期
    #执行成功,从输出结果中获取STA1的RSSI
    ################################################################################

    printStep(testname,'Step 4',\
              'wireless link-test STA1MAC',\
              'get sta1 rssi from the output')

    res1=res2=1

    #operate   
    EnterEnableMode(switch1)
    data = Receiver(switch1,'wireless link-test '+sta1mac,10)
    SetCmd(switch1,'\x03')
    #check
    rssi_tmp = None
    if None != data:
        SearchResult1 = re.search('\s+\d+\s+\d+\s+\d+\s+\d+\s+(\d+)\s+\d+\s+.*?',data)
        if None != SearchResult1:
            rssi_tmp = int(SearchResult1.group(1))
        if None != rssi_tmp:
            printRes('STA1 RSSI get from RF-PING is:'+str(rssi_tmp))
            res1 = 0
        if None == rssi_tmp:
            printRes('Failed:Can not get STA1 RSSI from RF-PING!')
            res1 = 1

    #result
    printCheckStep(testname,'Step 4',res1)

    ################################################################################
    #Step 5 
    # 操作
    # 在AP1上执行wlanconfig athx list查看sta1的RSSI；
    #
    # 预期
    # 执行成功，成功获取sta1的RSSI
    ################################################################################
    printStep(testname,'Step 5',\
              'wlanconfig athx list',\
              'get sta1 rssi from the output success')

    res1=1

    #operate
    data = SetCmd(ap1,'wlanconfig '+ath+' list',timeout=20)
    result = re.search('.*?RSSI.*?',data)
    print 'result=',result
    if result != None:
        rssi_index = re.sub('\s+',' ',result.group()).split(' ').index('RSSI')
        print 'rssi_index=',rssi_index
        SearchResult1 = re.search(sta1mac_type1.lower()+'.*',data)
        print 'SearchResult1=',SearchResult1
        if None != SearchResult1:
            printRes('SearchResult1:'+SearchResult1.group())
            rssi_tmp_from_ap = int(re.sub('\s+',' ',SearchResult1.group()).split(' ')[rssi_index])
            print 'rssi_tmp_from_ap=',rssi_tmp_from_ap
    #check
            if rssi_tmp_from_ap != None:
                printRes("STA1 rssi get from AP is:"+str(rssi_tmp_from_ap))
                res1 = 0
            else:
                printRes("Failed:can not get STA1 rssi from AP!")
        

    #result
    printCheckStep(testname, 'Step 5',res1)

    ################################################################################
    #Step 6
    # 操作
    # 等待1min，然后对比分别从AC1和AP1上获取的STA1的RSSI
    #
    # 预期
    # 两种方式获取的STA1的RSSI误差不超过5
    ################################################################################
    printStep(testname,'Step 6',\
              'Check STA1 RSSI difference',\
              'the difference should not bigger than 5')

    res1=res2=1
    IdleAfter(60)
    data = SetCmd(ap1,'wlanconfig '+ath+' list')
    result = re.search('.*?RSSI.*?',data)
    if result != None:
        rssi_index = re.sub('\s+',' ',result.group()).split(' ').index('RSSI')
        SearchResult1 = re.search(sta1mac_type1.lower()+'.*',data)
        if None != SearchResult1:
            printRes('SearchResult1:'+SearchResult1.group())
            rssi_tmp_from_ap = int(re.sub('\s+',' ',SearchResult1.group()).split(' ')[rssi_index])
            if rssi_tmp_from_ap != None:
                printRes("STA1 rssi get from AP is:"+str(rssi_tmp_from_ap))
                res1 = 0
            else:
                printRes("Failed:can not get STA1 rssi from AP!")
    #operate
    if rssi_tmp != None and rssi_tmp_from_ap != None:
        if abs(rssi_tmp-rssi_tmp_from_ap) > 5:
            printRes('Failed:The RSSI difference bigger than 5,too bigger!')
        else:
            res2 = 0
    else:
        printRes('Error:can not get sta1 RSSI form AC1 or AP1!')


    #result
    printCheckStep(testname, 'Step 6',res1,res2)

################################################################################
#Step 7
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 7',\
          'Recover initial config')

#operate
WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)
#end
printTimer(testname, 'End')
