#*********************************************************************
# 01_tool.tcl - Proc of Basic Management
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

proc CompareMacAddress { mac1 mac2 } {
	set mac1test [split $mac1 -]
	set mac2test [split $mac2 -]
	for {set i 0} {$i < 6} {incr i} {
		if { 0x0[lindex $mac1test $i] > 0x0[lindex $mac2test $i] } {
			PrintRes Print "$mac1 is more than $mac2!"
			return 1
		} elseif { 0x0[lindex $mac1test $i] == 0x0[lindex $mac2test $i] } {
			if { $i == 5 } {
				PrintRes Print "$mac1 is equal to $mac2!"
			} else {
				continue
			}	
		} else {
			PrintRes Print "$mac1 is less than $mac2!"
			return -1
		}
	}
}


#GetPortIndex Ethernet0/0/1
#GetPortIndex Ethernet1/1 chassis
#GetPortIndex Ethernet1/1 box
proc GetPortIndex { port {mode chassis} } {
	set res2 [regexp -nocase "Ethernet\(\[0-9\]+\)/\(\[0-9\]+\)/\(\[0-9\]+\)" $port match chas2 card2 port2]
    set res1 [regexp -nocase "Ethernet\(\[0-9\]+\)/\(\[0-9\]+\)" $port match card1 port1]
	if { $res2 == 1 } {
		return $port2
	}
	if { $res1 == 1 } {
		if { $mode == "chassis" } {
			return [expr $card1>4?(($card1 + 1) * 64 + $port1):(($card1 - 1) * 64 + $port1)]
		} else {
			return $port1
		}
	}
}

#add by liangdong 2008.10.28 
proc CheckCommandError { sut command {timer 1} {ncounter 0}} {
    set RecvBuf [ receiver $sut "$command" $timer ]
    set num [regsub -all \n $RecvBuf {} ignore ]
	if { $num == $ncounter } {
	    return 1
	} else {
	    PrintRes Print ">>>$sut can't config the command: \"$command\" for..."
	    PrintRes RecvBuf $RecvBuf
	    return 0
	}
}

#Switch(config-if-vlan1)#sho ver
#  Switch Device, Compiled on Jul 01 19:51:39 2009
#  SoftWare Version Switch_6.0.49.0
#  BootRom Version Switch_1.0.2
#  HardWare Version 0.0.0
#  Copyright (C) 2001-2009 by Vendor
#  All rights reserved.
#  Uptime is 0 weeks, 0 days, 2 hours, 8 minutes.
proc GetSysUpTime { sut } {
	EnterEnableMode $sut
	set RecvBuf [receiver $sut "show version" 2]
	set res [regexp -nocase {Uptime is (\d+) weeks, (\d+) days, (\d+) hours, (\d+) minutes} $RecvBuf match weeks days hours minutes]
	if { $res == 1 } {
		PrintRes Print "get system uptime : $match"
		return [expr $weeks * 7 * 24 * 60 + $days * 24 * 60 + $hours * 60 + $minutes]
	} else {
		PrintRes Print "!get system uptime error!"
		return 0
	}
}

#FormattoASCII abc 10
#61 62 63 00 00 00 00 00 00 00
#FormattoASCII abc 
#61 62 63
proc FormattoASCII { string {bytenum 0} } {
	set result ""
	set length [string length $string]
	if { $bytenum == 0 } {
		for {set i 0} {$i < $length} {incr i} {
			scan [string index $string $i] %c value
			if { $i == [expr $length - 1]} {
				append result [format %02x $value]
			} else {
				append result "[format %02x $value] "
			}
		}
	} else {
		if { $length > $bytenum } {
			PrintRes Print "your string is too long!"
			return 0
		}
		for {set i 0} {$i < $bytenum} {incr i} {
			if { $i < $length } {
				scan [string index $string $i] %c value
				if { $i == [expr $bytenum - 1] } {
					append result [format %02x $value]
				} else {
					append result "[format %02x $value] "
				}
			} else {
				if { $i == [expr $bytenum - 1] } {
					append result "00"
				} else {
					append result "00 "
				}
			}
		}
	}
	return [string toupper $result]
}

proc FormatIptoHex { ip } {
	set ip [split $ip .]
	for {set i 0} {$i < [llength $ip]} {incr i} {
		set ip [lreplace $ip $i $i [format %02X [lindex $ip $i]]]
	}
	return $ip
}

#######################################################
#
# MIp2Mac :根据组播ip地址获得对应的mac地址
#
# args:
#     ipaddr: 组播ip地址
#
# return: 
#     对应的组播mac地址，形如00 00 00 00 00 00
#
# addition:
#
# examples:
#     MIp2Mac 192.168.1.1
#
########################################################## 	
proc MIp2Mac { ipaddr } {
	set list [ split $ipaddr . ]
	set a [lindex $list 0 ]
	set b [lindex $list 1 ]
	set b [expr $b % 128]
	if { $b<16 } {
		set bb [format %X $b]
		append bbb 0 $bb
	} else {
		set bbb [format %X $b]
	}

		set c [lindex $list 2 ]
	if { $c<16 } {
		set cc [format %X $c]
		append ccc 0 $cc
	} else {
		set ccc [format %X $c]
	}

	set d [lindex $list 3 ]
	if { $d<16 } {
		set dd [format %X $d]
		append ddd 0 $dd
	} else {
		set ddd [format %X $d]
	}

	set multimac [ format "01-00-5E-%s-%s-%s" $bbb $ccc $ddd ]
	regsub -all {\-} $multimac " "  multimac
	return $multimac
}  

#######################################################
#
# RemoveR :去掉多余的回车键
#
# args:
#     strRecv: 捕获信息
#
# return: 
#     去掉多余回车键后的捕获信息
#
# addition:
#
# examples:
#     MIp2Mac $strRecv
#
########################################################## 	
proc RemoveR {strRecv} {
	regsub -all \r $strRecv {} Recv         ;#去掉多余的回车键
	return $Recv
}

######################################################################
#
# GetCpuMac:  获取交换机的CPU mac地址
#
# args:
#     sut:        待测设备
#     interface:  三层接口
#
# return:   
#       0   错误，无法得到cpu mac
#       cpu mac:  形如00 03 0f 00 10 78的交换机cpu mac
# 
# addition:
#
# examples:
#     GetCpuMac s1 vlan10
#           
######################################################################
#建议使用新的GetCpuMac
proc GetCpuMac { sut interface } {
    #edit by gaowei
    EnterEnableMode $sut
    set RecvBuf [receiver $sut "show interface $interface" 2]
    set exp [regexp -nocase {Hardware is (.*?),\s+address is (.*?)-(.*?)-(.*?)-(.*?)-(.*?)-(.*?)\n}  $RecvBuf match hardware mac1 mac2 mac3 mac4 mac5 mac6]
    
    if {[info exist mac1]} {
    	set cpu_mac $mac1
    } else {
    	PrintRes Print "!!!Can not get the mac of $sut!!!!!!!"
    	return 0
    }
    
    for {set i 2} {$i <= 6} {incr i 1} {
		if {[info exist mac$i]} {
    		append cpu_mac "-[set mac$i]"
    	} else {
    		PrintRes Print "!!!Can not get the mac of $sut!!!!!!!"
    		return 0
    	}
    }
    
    if { [info exist cpu_mac] } {
        for {set i 2} {$i<18} {incr i 3} {
            set cpu_mac [string toupper [string replace $cpu_mac $i $i " "]]
        }   
        PrintRes Print "Get mac of $sut is: $cpu_mac"
        return $cpu_mac
    } else {
        PrintRes Print "!!!can't get the mac, it is error!"
        return 0
    }
}
#########################################################################
#
#    TransformMac： mac转换
#
#  args: 
#     mac :    mac地址
#     symbol1 : 原分隔符
#     symbol2 : 新分隔符
#
#    return: 返回转换后的mac
#              0:转换失败
#    examples:
#     TransformMac 00-00-00-00-00-01 "-" ":"
#
##########################################################################
proc TransformMac {mac symbol1 symbol2} {
	set res [regsub -all -- "$symbol1" $mac "$symbol2" newmac]
	if {$res == 0} {
		PrintRes Print "can't transform $mac"
		return 0
	}
	return $newmac
}
#目前的GetCpuMac捕获到的应该是vlanmac，所以修改为以下函数
######################################################################
#
# GetVlanMac:  获取交换机的CPU mac地址
#
# args:
#     sut:        待测设备
#     interface:  三层接口
#
# return:   
#       0   错误，无法得到cpu mac
#       cpu mac:  形如00 03 0f 00 10 78的交换机cpu mac
# 
# addition:
#
# examples:
#     GetVlanMac s1 vlan10
#           
######################################################################
#建议使用新的GetVlanMac
proc GetVlanMac { sut {interface vlan1} } {
    #edit by gaowei
    EnterInterfaceMode $sut $interface
    EnterEnableMode $sut
    set RecvBuf [receiver $sut "show interface $interface" 2]
    #set exp [regexp -nocase {Hardware is EtherSVI, address is (.*?)-(.*?)-(.*?)-(.*?)-(.*?)-(.*?)\n}  $RecvBuf match mac1 mac2 mac3 mac4 mac5 mac6]
    set exp [regexp -nocase {Hardware is (.*?), address is (.*?)-(.*?)-(.*?)-(.*?)-(.*?)-(.*?)\n}  $RecvBuf match hardware mac1 mac2 mac3 mac4 mac5 mac6]
    if {[info exist mac1]} {
    	set cpu_mac $mac1
    } else {
    	PrintRes Print "!!!Can not get the mac of $sut!!!!!!!"
    	return 0
    }
    
    for {set i 2} {$i <= 6} {incr i 1} {
		if {[info exist mac$i]} {
    		append cpu_mac "-[set mac$i]"
    	} else {
    		PrintRes Print "!!!Can not get the mac of $sut!!!!!!!"
    		return 0
    	}
    }
#    DeleteInterfaceVlan $sut [string range $interface 4 end]   
    if { [info exist cpu_mac] } {
        for {set i 2} {$i<18} {incr i 3} {
            set cpu_mac [string toupper [string replace $cpu_mac $i $i " "]]
        }   
        PrintRes Print "Get mac of $sut is: $cpu_mac"
        return $cpu_mac
    } else {
        PrintRes Print "!!!can't get the mac, it is error!"
        return 0
    }
}

#DCRS-7604>%mEnter into super shell mode!!
#BCM.0> 
#BCM.0> shell
#-> sysBoardInfoShow
#Board Type is 1
#Vlan MAC: 00-03-0F-0E-7B-0D
#CPU  MAC: 00-03-0F-0E-7B-0E
#S/N: N074800123
#Manufacture Date:2008/04/18 
#H/W: R3.0               
#
#value = 26 = 0x1a
proc GetMacOfSwitch { sut } {
	EnterEnableMode $sut
	receiver $sut "%ma"
	receiver $sut "shell"
	set RecvBuf [receiver $sut "sysBoardInfoShow" 1]
	receiver $sut "exit"
	receiver $sut "exit\n"
	set res1 [regexp -nocase -line {Vlan MAC: ([^\n]+)} $RecvBuf match vlanmac]
	set res2 [regexp -nocase -line {CPU  MAC: ([^\n]+)} $RecvBuf match cpumac]
	if { $res1 == 1 && $res2 == 1 } {
		puts "Get vlan-mac of $sut is : $vlanmac!"
		puts "Get  cpu-mac of $sut is : $cpumac!"
		if { [string equal $cpumac $vlanmac] } {
		#暂时定义为只判断vlan-mac是否与cpu-mac相等，不判断vlan-mac+1是否等于cpu-mac
			puts "!cpu-mac should not be equal vlan-mac!"
			return 0
		} else {
			return [list $vlanmac $cpumac]
		}
	} else {
		puts "!Can't get vlan-mac or cpu-mac of $sut!"
		return -1
	}
}

proc CheckMacCrash { args } {
	#args : list of com
	set res 1
	set maclist ""
	for {set i 0} {$i < [llength $args]} {incr i} {
		set sut [lindex $args $i]
		set swmaclist [GetMacOfSwitch $sut]
		if { [llength $swmaclist] != 2 } {
			set res 0
		} else {
			lappend maclist [lindex $swmaclist 0] [lindex $swmaclist 1]
		}		
	}
	return [expr {$res & [CheckListEqual $maclist]}]
}

proc CheckListEqual { l } {
	for {set firstpoint 0} {$firstpoint < [llength $l] - 1} {incr firstpoint} {
		for {set secondpoint [expr {$firstpoint + 1}]} {$secondpoint < [llength $l]} {incr secondpoint} {
			if {[string equal [lindex $l $firstpoint] [lindex $l $secondpoint]]} {
				puts "![lindex $l $firstpoint] is equal to [lindex $l $secondpoint]!"
				return 0
			}
		}
	}
	return 1 
}
 

proc GetEUI64Address { cpumac } {
    append eui64address1 [string range $cpumac 0 7] "-ff-fe-" [string range $cpumac 9 16]
#    puts $eui64address1
    append eui64address2 [format "%02x" [expr 0x[string range $eui64address1 0 1] | 02]] [string range $eui64address1 2 22]
#    puts $eui64address2
    return $eui64address2
}

#GetLinkLocalAddress 00-01-0f-01-00-01
#GetLinkLocalAddress 23.1.1.3
proc GetLinkLocalAddress { cpumacorip } {
	if [regexp -nocase \\- $cpumacorip] {
		#mac
	    set eui64address [GetEUI64Address $cpumacorip]
	    append part1 [string range $eui64address 0 1] [string range $eui64address 3 4]
	    append part2 [string range $eui64address 6 7] [string range $eui64address 9 10]
	    append part3 [string range $eui64address 12 13] [string range $eui64address 15 16]
	    append part4 [string range $eui64address 18 19] [string range $eui64address 21 22]
	    append linklocaladdress "fe80::" [format "%x" 0x$part1] ":" [format "%x" 0x$part2] ":" [format "%x" 0x$part3] ":" [format "%x" 0x$part4]
#    puts $linklocaladdress
	    #PrintRes Print "Get link local address of $cpumac is: $linklocaladdress"
	    return $linklocaladdress
	} else {
		#ip
		set ip [split $cpumacorip .]
	    append linklocaladdress "fe80::" [format "%x" [lindex $ip 0]][format "%02x" [lindex $ip 1]] ":" [format "%x" [lindex $ip 2]][format "%02x" [lindex $ip 3]]
#    puts $linklocaladdress
	    #PrintRes Print "Get link local address of $cpumac is: $linklocaladdress"
	    return $linklocaladdress
	}
}



#########################################################################
#
# ShowErrInfo:打印错误提示信息，输出里面的内容以帮助查找错误原因
#               工具函数，方便阅读出错信息
#
# args:
#     recvbuf: 错误提示信息
# 
# return:
#
# addition:
# 
# examples: 
#     ShowErrInfo $recvbuf
#
######################################################################### 
proc ShowErrInfo { recvbuf } {
	PrintRes Print " ******************   The switch  Output:   ******************"
	PrintRes Print "|                                                             |"
	PrintRes Print " $recvbuf "
	PrintRes Print "|                                                             |"
	PrintRes Print " ******************   End the switch Output:   ***************"
	
}
proc IncrInterfaceDescription { interfacedescription } {
    set length [string length $interfacedescription]
    set res [regexp -nocase {[0-9]+:[0-9]+ - ([0-9]+)} $interfacedescription match num]
    if { $res == 1 } {
        set headstring [string range $interfacedescription 0 [expr $length - [string length $num] - 1]]
        return [append headstring [incr num]]       
    } else {
        return 0
    }
}
    
#########################################################################
#
# IncrMacStep:按设定步长增加mac地址值
#
# args:
#     mac :MAC地址
#     step:增加的步长
# 
# return:
#
# addition:
#     传入的mac形如00-00-00-00-00-00
#     返回值为增长后的mac值
#     为了避免产生的数值过大的问题，目前只对最后两位（即256）的数据进行处理。
#
# examples: 
#     IncrMacStep 00-00-00-00-00-01 
#
######################################################################### 
proc IncrMacStep { mac {step 1} } { 
    regsub -all {\-} $mac "" mac
    set firstpart [string range $mac 0 3]
    set lastpart [string range $mac 4 end] 
    set mac 0x$lastpart
    set mac [ format "%i" $mac ]
    incr mac $step
    set mac [ format "%#010x" $mac ]
    set mac "[string range $firstpart 0 1]-[string range $firstpart 2 3]-[string range $mac 2 3]-[string range $mac 4 5]-[string range $mac 6 7]-[string range $mac 8 9]"
    return $mac
}

#########################################################################
#
# IncrIpStep:按设定步长增加ip地址值
#
# args:
#     ip :ip地址
#     mode ：增长哪一段
#     step:增加的步长
# 
# return:
#
# addition:
#     
#
# examples: 
#     IncrIpStep 10.1.1.1
#
######################################################################### 
proc IncrIpStep { ip {mode ClassD} {step 1} } {
    set firstdot [string first "." $ip]
    set seconddot [expr $firstdot + [string first "." [string range $ip [expr $firstdot + 1] end]] + 1]
    set thirddot [string last "." $ip]
    
    if { $mode == "ClassD" } {
        set temp [string range $ip [expr $seconddot + 1] end]
    }
    if { $mode == "ClassC" } {
        set temp [string range $ip [expr $firstdot + 1] [expr $thirddot - 1]]
    }
    
    set dotindex [string first "." $temp]
    set tempip ""
    append tempip [format "%02x" [string range $temp 0 [expr $dotindex - 1]]]
    append tempip [format "%02x" [string range $temp [expr $dotindex + 1] end]]
    set tempip 0x$tempip
    set tempip [format "%i" $tempip]
#    puts $tempip
    incr tempip $step
    set tempip [format "%04x" $tempip]
#    puts $tempip
    if { $mode == "ClassD" } {
        set resultip [string range $ip 0 $seconddot]
        append resultip [format "%i" 0x[string range $tempip 0 1]]
        append resultip "."
        append resultip [format "%i" 0x[string range $tempip 2 3]]
    }
    if { $mode == "ClassC" } {
        set resultip [string range $ip 0 $firstdot]
        append resultip [format "%i" 0x[string range $tempip 0 1]] 
        append resultip "."
        append resultip [format "%i" 0x[string range $tempip 2 3]]
        append resultip [string range $ip $thirddot end]
    }
    return $resultip
}

#########################################################################
#
# IncrIpv6Step:按设定步长增加ipv6地址值
#
# args:
#     ipv6 :ipv6地址
#     mode ：增长哪一段
#     step:增加的步长
# 
# return:
#
# addition:
#     
#
# examples: 
#     IncrIpv6Step 2000::1
#
######################################################################### 
#本函数有一定的局限性，不是无限增长的，最大宽度是0000 0000---ffff ffff，如果超出ffff ffff，就会提示报错。
proc IncrIpv6Step { ipv6 {mode 8} {step 1} } {
    set ipv6list [split $ipv6 :]
    set ipv6num [llength $ipv6list]
    set ipv6null [lsearch -exact $ipv6list {} ]
    if { $ipv6null == -1 } {
    	if { $ipv6num != 8 } {    		
    		puts "bad ipv6 format"
    		return -1
    	}
    } else {
    	if { $ipv6num >= 8 } {
    		puts "bad ipv6 format"
    		return -1
    	}
    	set ipv6list [lreplace $ipv6list $ipv6null $ipv6null]
    	set pos $ipv6null
    	set loopnum [expr { 8 - $ipv6num + 1 } ]
    	for {set i 1} {$i <= $loopnum } {incr i 1 } {
    		set ipv6list [linsert $ipv6list $pos 0 ] 		
    		incr pos 1
    	}
    }
    set ipv6num [llength $ipv6list]
    for {set i 0 } { $i < 8 } {incr i} {
    	set checkipv6 0x[lindex $ipv6list $i]
    	if {$checkipv6 < 0 || $checkipv6 > 0xffff } {
    		puts "ipv6 address is wrong"
    		return -1
    	}
    }
    if { $mode == 1 || $mode == 0 } {
	    set tempip [ format "%04x" 0x[lindex $ipv6list 0]  ]
	    set tempip 0x$tempip
	    set compareip $tempip
	    incr tempip $step
	    if { $tempip < $compareip } {
	    	puts "error: ipv6 data overflow,please decrease the step"
	    	return -1
	    }
	    set tempip [format "%04x" $tempip ]
	    set tempipv61 [format "%x" 0x[string range $tempip 0 3 ] ]    
	    #set ipv6list [lreplace $ipv6list $incrpos1 $incrpos1 $tempipv61 ];#get rid of this line ,add following line for the case of first segment incr,2009/10/26 hansong
	    set ipv6list [lreplace $ipv6list  0 0 $tempipv61 ];#      
	    set ipv6addr [join $ipv6list :]
	} else {
		set incrpos1 [expr $mode - 2 ]
	    set incrpos2 [expr $mode - 1 ]
	    set tempip [ format "%04x" 0x[lindex $ipv6list $incrpos1]  ]
	    append tempip [ format "%04x" 0x[lindex $ipv6list $incrpos2 ] ]
	    set tempip 0x$tempip
	    set compareip $tempip
	    incr tempip $step
	    if { $tempip < $compareip } {
	    	puts "error: ipv6 data overflow,please decrease the step"
	    	return -1
	    }
	    set tempip [format "%08x" $tempip ]
	    set tempipv61 [format "%x" 0x[string range $tempip 0 3 ] ]    
	    set ipv6list [lreplace $ipv6list $incrpos1 $incrpos1 $tempipv61 ]
	    set tempipv62 [format "%x" 0x[string range $tempip 4 7 ] ]     
			set ipv6list [lreplace $ipv6list $incrpos2 $incrpos2 $tempipv62 ]         
	    set ipv6addr [join $ipv6list :]
	}
        
    return $ipv6addr
    
}
#########################################################################
#
# GetInterfacerCpuMac:获得接口的CPU的MAC
#
# args:
#     sut : 被测设备
#     interface:接口
# 
# return:
#
# addition:
#
# examples: 
#     GetInterfaceCpuMac s1 e0/0/1
#
######################################################################### 
proc GetInterfaceCpuMac { sut interface } {
	EnterEnableMode $sut
    set RecvBuf [receiver $sut "show interface $interface" 2]
    set exp [regexp -nocase {Hardware is EtherSVI, address is (.*?)-(.*?)-(.*?)-(.*?)-(.*?)-(.*?)\n}  $RecvBuf match mac1 mac2 mac3 mac4 mac5 mac6]
      
    if {[info exist mac1]} {
      	set cpu_mac $mac1
    } else {
      	PrintRes Print "!!!Can not get the cpu mac of $sut!!!!!!!"
       	return 0
    }
        
    for {set i 2} {$i <= 6} {incr i 1} {
		if {[info exist mac$i]} {
    		append cpu_mac "-[set mac$i]"
    	} else {
    		PrintRes Print "!!!Can not get the cpu mac of $sut!!!!!!!"
    		return 0
    	}
    }
   	return $cpu_mac
}

######################################################################
#
# VerifyCmdOutput: 检查在指定的输出中是否有制定的字符串
#
# args:
#     sut:    待测设备
#     cmd:    输入到交换机上的命令
#     output: 需要匹配的字符串
#     timeout:等待的时长，单位为秒，缺省值为1秒
#     flag:   判断需要匹配的字符串是否在输出结果中的标志位；
#             取值:true，希望需要匹配的字符串在输出结果中出现；
#                   false，希望需要匹配的字符串在不在输出结果中出现；
#             缺省值:true
#
# return: 
#     1     结果正确，即需要的字符串在输出结果中，或者不需要的字符串不在输入结果中 
#     0     结果错误，即需要的字符串不在输出结果中，或者不需要的字符串在输入结果中 
# 
# addition:
#
# examples:
#     VerifyCmdOutput s11 "show run int vlan 11" "ip dvmrp cisco-compatible $ipaddr"
#     VerifyCmdOutput s11 "show run int vlan 11" "ip dvmrp cisco-compatible $ipaddr" 1 false
######################################################################
proc VerifyCmdOutput { sut cmd output { timeout 1 } {flag true} } {
    EnterEnableMode $sut
    set RecvBuf [receiver $sut $cmd $timeout]
	#EnterUserMode $sut
	if {[regexp -nocase $output $RecvBuf]} {
		if {$flag == "true"} {
			PrintRes Print "$cmd output test, OK!"
	    } else {
	    	PrintRes Print "!$cmd output test, ERROR!"
	    	return 0
	    }
	} else {
		if {$flag == "true"} {
			PrintRes Print "!$cmd output test, ERROR!"
			return 0
		} else {
			PrintRes Print "$cmd output test, OK!"
		}
	}
	return 1 
}

#########################################################################
#
# ShowRunInterface : 显示路由器show run interface 后的输出结果并作判断
#
# args: 
#	  interface: 路由器命令show run interface中的接口类型
#     expected_result: 期望输出的字符串
#     boolvar: true，则表示$expected_result应该在输出结果当中，
#              false,$expected_result就不应该在输出结果当中
#
# return:
#     1 : 存在
#     0 : 不存在
#
# addition:
#	  若$expected_result在路由器的输出字符串当中，并且$boolvar为true；或者
#	  $expected_result不在路由器的输出字符串当中，并且$boolvar为false则PASS；
#	  否则FAILED，
#
# examples:
#     ShowRunInterface s1 $s1p1 "ip access-group 2 in" true
#
#########################################################################
proc ShowRunInterface { sut interface expected_result boolvar { timeout 2 } } {
	EnterEnableMode $sut
	set RecvBuf [ receiver $sut "show running interface $interface" $timeout PromoteStop true]
	set res [ regexp -nocase $expected_result $RecvBuf ]
    if { $res > 0 } {
    	if { $boolvar == "true" } {
        	PrintRes Print "the configuration of $expected_result is OK!"
        	return 1 
        } else {
            PrintRes Print "!the configuration of $expected_result is ERROR!"
            return 0
        }
    } else {
        if { $boolvar == "false" } {
            PrintRes Print "the configuration of $expected_result is OK!"
            return 1
        } else {
            PrintRes Print "!the configuration of $expected_result is ERROR!"
            return 0
        }
    }
}
#########################################################################
#
# ShowRunCommand : 显示路由器show run 后的输出结果并作判断
#
# args: 
#     expected_result: 期望输出的字符串
#     boolvar: true，则表示$expected_result应该在输出结果当中，
#              false,$expected_result就不应该在输出结果当中
#
# return:
#     1 : 存在
#     0 : 不存在
#
# addition:
#	  若$expected_result在路由器的输出字符串当中，并且$boolvar为true；或者
#	  $expected_result不在路由器的输出字符串当中，并且$boolvar为false则PASS；
#	  否则FAILED，
#
# examples:
#     ShowRunCommand s1 "ip access-group 2 in" true
#
#########################################################################
proc ShowRunCommand { sut expected_result boolvar {timeout 5}} {
	EnterEnableMode $sut
	set RecvBuf [ receiver $sut "show running " $timeout ]
	set res [ regexp -nocase $expected_result $RecvBuf ]
    if { $res > 0 } {
    	if { $boolvar == "true" } {
        	PrintRes Print "the configuration of $expected_result is OK!"
        	return 1
        } else {
            PrintRes Print "!the configuration of $expected_result is ERROR!"
            return 0
        }
    } else {
        if { $boolvar == "false" } {
            PrintRes Print "the configuration of $expected_result is OK!"
            return 1
        } else {
            PrintRes Print "!the configuration of $expected_result is ERROR!"
            return 0
        }
    }
}

#########################################################################
#
# ShowCmdResult : 查看命令配置后是否有出错信息提示（对ACL表项的操作是否成功）
#
# args: 
#     sut: 被测设备
#	  cmd: 进行操作的相应命令字符串，用于提示
#	  expected_result: 期望输出的字符串
#     boolvar: 布尔变量，若为true，则表示$expected_result应该在输出结果当中，
#              若为false,则表示$expected_result就不应该在输出结果当中
#
# return:
#     1 : 存在
#     0 : 不存在
# addition:
#	  若$expected_result在路由器的输出字符串当中，并且$boolvar为true；或
#	  $expected_result不在路由器的输出字符串当中，并且$boolvar为false则PASS；
#	  否则FAILED
#
# examples:
#
#
#########################################################################
proc ShowCmdResult { sut cmd expected_result boolvar } {
	set RecvBuf [ receiver $sut $cmd 1 ]
	set res [ regexp -nocase $expected_result $RecvBuf ]
	if { $res > 0 } {
		if { $boolvar == "true" } {
			PrintRes Print "$cmd configuration OK!"
			return 1
		} else {
			PrintRes Print "!$cmd configuration ERROR!"
			return 0
		}
		
	} else {
		if { $boolvar == "false" } {
			PrintRes Print "$cmd configuration OK!"
			return 1
		} else {
			PrintRes Print "!$cmd configuration ERROR!"
			return 0
		}
	}
}



#####################################################################################
#
# CalcAddress: 计算并生成需要的mac或ip地址序列
#
# args:
#     type:指明生成地址序列的类型，0为ip地址，1为mac地址
#	  firstaddr:首地址，需要生成的地址序列的首地址
#	  number:序列长度，即需要生成的地址个数
#	  step:步长，即地址与下一地址之间的间隔
#     
# return: 
#     地址列表，配合foreach使用
#
# addition:
#     firstaddr的地址格式为:
#          ip（类型0）点分十进制格式，如:100.1.1.1
#          mac（类型1）连词符分隔形式，如:00-03-0f-00-00-01
#     -developed by sujun
#
# examples:
#     构造ip首地址为100.1.1.1，num为10，step为256的地址列表，匹配输出结果中是否存在地址列表中的地址
#          set iplist [CalcAddress 0 100.1.1.1 10 256]
#          foreach ipaddress $iplist {
#              .....
#          } 
#
######################################################################################
proc CalcAddress { type firstaddr number step } {
	if {$type==0} {  	
		regexp {([0-9]+).([0-9]+).([0-9]+).([0-9]+)} $firstaddr match A B C D
		set i $A
		set j $B
		set k $C
		set l $D
		for {set n 0} {$n<$number} {incr n} {
			set newip [join "$i $j $k $l" .]
			lappend iplist $newip
			set x [expr $step + $l]
			set l [expr $x%256]
			set y [expr $x/256 + $k]
			set k [expr $y%256]
			set z [expr $y/256 + $j]
			set j [expr $z%256]
			set i [expr $z/256 + $i]
		}
		return $iplist
	}	
	if {$type==1} {	
		regexp {(.*?)-(.*?)-(.*?)-(.*?)-(.*?)-(.*?)$} $firstaddr match A B C D E F
		set i $A
		set j $B
		set k $C
		set l $D
		set m $E
		set n $F		
		for {set s 0} {$s<$number} {incr s} {
			set newmac [join "$i $j $k $l $m $n" -]
			lappend maclist $newmac
			
			set iHex 0x$i
			set jHex 0x$j
			set kHex 0x$k
			set lHex 0x$l
			set mHex 0x$m
			set nHex 0x$n
			
			set stepHex [format "%#x" $step]
			set tempN [expr $nHex + $stepHex]
			set n [expr $tempN%256]
			set tempM [expr $tempN/256 + [format "%d" $mHex]]
			set m [expr $tempM%256]
			set tempL [expr $tempM/256 + [format "%d" $lHex]]
			set l [expr $tempL%256]
			set tempK [expr $tempL/256 + [format "%d" $kHex]]
			set k [expr $tempK%256]
			set tempJ [expr $tempK/256 + [format "%d" $jHex]]
			set j [expr $tempJ%256]
			set i [expr $tempJ/256 + [format "%d" $iHex]]
			
			set i [format "%02x" $i]
			set j [format "%02x" $j]
			set k [format "%02x" $k]
			set l [format "%02x" $l]
			set m [format "%02x" $m]
			set n [format "%02x" $n]			
		}		 				
		return $maclist
	}
}

#####################################################################################
#
# IdleAfter: 非阻塞等待
#
# args:
#     timeout:等待的毫秒数
#
# return: 
# 
# addition:
#
# examples:
#	  非阻塞等待30秒
#     idle_after 30000
#
######################################################################################
proc IdleAfter { timeout } {
#	puts stdout "please wait, in idle_after... timeout $timeout"
	set timeout_1 [expr {$timeout/1000.0}]
	PrintRes Print "please wait, in idle_after... timeout $timeout_1 seconds."
	set idleafter 0
	after $timeout {set idleafter 1}
	vwait idleafter
	
}

#####################################################################################
#
# Wait: 非阻塞等待
#
# args:
#     timeout:等待的毫秒数
#
# return: 
# 
# addition:
#
# examples:
#	  非阻塞等待30秒
#     Wait 30000
#
######################################################################################
proc Wait { timeout } {
    set idleafter 0
	after $timeout {set idleafter 1}
	vwait idleafter
}

#####################################################################################
#
# PrintRes Print: 将信息打印到stdout同时输出到result文件中.
#
# args:
#     str: 输出字符串
#     debugFlag :是否向终端上输出信息  默认为1 
#
# return:   
# 
# addition:
#
# examples:
#       PrintRes Print "this is just a test"
#       PrintRes Print nonewline "this is just a test"
#
###################################################################################
proc ResPuts {str {debugFlag 1}} {
	set errorflag 0
	if {[regexp -nocase FAILED $str]==1 || [regexp -nocase ERROR $str]==1} {
		puts stderr $str
		set errorflag 1		
		if {[info exist ::autotest::VAR(erridletimer)]} {
    		if {$::autotest::VAR(erridletimer) > 0} {
    		    IdleAfter $::autotest::VAR(erridletimer)
		    }
		}
	} else {
		puts stdout $str
	}
	
    #added by xuyongc 2005-2-4 
    #记录测试中的错误测试例已经测试例通过和失败的总数
#	if {[info exist ::autotest::VAR(failedresfile)]} {
#	    
#	    if {[regexp -nocase FAILED $str]} {
#	        puts $::autotest::VAR(failedresfile) $str
#		    incr ::autotest::VAR(counterfailed) 1
#	    }
#	    
#	    if {[regexp -nocase PASSED $str]} { 
#	        incr ::autotest::VAR(counterpass) 1
#	    }
#	}
    #end of added by xuyongc
    
    #if debugFlag==1 puts the message to moni term
    if {$debugFlag == 1} {
	    if {[info exist ::autotest::VAR(number)]} {
	    				PrintLogNewLineStart
	            LogPuts  $::autotest::VAR(number) $str 
	            PrintLogNewLineEnd
    	    }
    }
	
	if {[info exist ::autotest::VAR(resfile)]} {
		puts $::autotest::VAR(resfile) $str
	}
	#stop encountered error add by liuleic 2008.5.15
	if {$errorflag} {
		if { $::moni::M(Script.ErrorStop) } {
			::autotest::pause_test
		}
	}
}
#####################################################################################
#
# PauseTest: 遇错停止
#
# args:
#     str : 打印到标准输出的字符串
#
# return: 
# 
# addition:
#
# examples:
#	  
#     PauseTest
#
######################################################################################
proc PauseTest { {str "Pause current test for some reasion, may be an error occurred..."} } {
    ::autotest::pause_test
    PrintRes Print $str 
}

#####################################################################################
#
# LogPuts: PrintRes Print内部调用函数
#
# args:
#
# return: 
#
# addition:  
# 
# examples:
#     LogPuts  $::autotest::VAR(number) $str
#  
###################################################################################
proc LogPuts { num str } {
    for { set i 1 } { $i <= $num } { incr i } {
#    	receiver s$i $str
	::moni::tty_in s$i "$str\n"
	::moni::log_out s$i "$str\n"
    }
}

#####################################################################################
#
# PrintLogNewLineStart: 在monitor及log文件中输出一个换行
#
# args:
#
# return: 
#
# addition:  
# 
# examples:
#     
#  
###################################################################################
proc PrintLogNewLineStart {} {
	for {set i 1} {$i <= $::autotest::VAR(number)} {incr i} {
		::moni::tty_in s$i "\n"
		::moni::log_out s$i "\n"
	}
}
#####################################################################################
#
# PrintLogNewLineEnd: 向交换机输出一个回车
#
# args:
#
# return: 
#
# addition:  
# 
# examples:
#    
#  
###################################################################################
proc PrintLogNewLineEnd {} {
#	for {set i 1} {$i <= $::autotest::VAR(number)} {incr i} {
#		receiver s$i ""
#	}
}

#####################################################################################
#
# SetPerformanceVlan: 性能测试时配置VLAN的工具函数
#
# args:
#     sut : 被测交换机
#     slot: 板卡号，如果端口是0/0/1之类，则此参数为0/0
#     num : 端口数目
#     
# return: 
#
# addition:  
#     add by liangdong 2006.9.19
# 
# examples:
#     SetPerformanceVlan s1 0/0 24
#  
###################################################################################
proc SetPerformanceVlan { sut slot num } {
    for {set i 1} {$i <= [expr $num / 2]} {incr i} {
    	AddVlan $sut $i Ethernet${slot}/[expr $i * 2 - 1] Ethernet${slot}/[expr $i * 2]
    }
}

#########################################################################
#
# MaskIp : 获取ip地址段
#
# args: 
#      ip: 		ip地址
#	     mask:	ip地址掩码
# return:
#        ip地址段
#
# addition:
#
# examples:
#     MaskIp 10.1.1.1 255.255.255.0
#
#########################################################################
proc MaskIp { ip mask } {
	set iplist [ split $ip . ]
	set masklist [ split $mask . ]
	set result ""
	append result [ expr [lindex $iplist 0] & [lindex $masklist 0] ]
	append result "."
	append result [ expr [lindex $iplist 1] & [lindex $masklist 1] ]
	append result "."
	append result [ expr [lindex $iplist 2] & [lindex $masklist 2] ]
	append result "."
	append result [ expr [lindex $iplist 3] & [lindex $masklist 3] ]
	return $result
}

#####################################################################################
#
# idle_after: 非阻塞等待
#
# 参数:
#           timeout，等待的毫秒数
# 返回值: 
#     无
#
# 使用举例:
#		非阻塞等待30秒
#           idle_after 30000
######################################################################################
proc idle_after {timeout} {
	puts stdout "please wait, in idle_after... timeout $timeout"
	set idleafter 0
	after $timeout {set idleafter 1}
	vwait idleafter
	#puts stdout "Exit from idle_after"
}

#####################################################################################
#
# CheckConnectionBetweenIxiaAndSwitch: 检查ixia端口与交换机端口的连接
#
# 参数:
#           host：ixia地址
#           testerport ：ixia端口
#           sut ：被测交换机
#           sutport：交换机端口
# 返回值: 
#     1:连接正确
#     0：连接错误
#
# 使用举例:
#           CheckConnectionBetweenIxiaAndSwitch 172.16.1.253 "2:1" s1 Ethernet1/1
######################################################################################
proc CheckConnectionBetweenIxiaAndSwitch { host testerport sut sutport } {
    upvar 1 $host ixiaip
    upvar 1 $testerport tport
    upvar 1 $sut switch
    upvar 1 $sutport switchport
    set tp [split $tport :]
    set card [lindex $tp 0]
    set port [lindex $tp 1]
    ixInitialize $ixiaip
    set chasId [ixGetChassisID $ixiaip]
    set portlist [list [list $chasId $card $port]]    	
	port setFactoryDefaults $chasId $card $port
	ixWritePortsToHardware portlist
    set RecvBuf [receiver $switch "\n" 10]
    set res [regexp -nocase $switchport $RecvBuf]
    if { $res == 1 } {
        PrintRes Print "Check $testerport\($tport) of $host\($ixiaip) should connect to $sutport\($switchport) of $sut\($switch), OK!"
        return 1
    } else {
        PrintRes Print "Check $testerport\($tport) of $host\($ixiaip) should connect to $sutport\($switchport) of $sut\($switch), ERROR!"
        return 0
    }
}
#####################################################################################
#
# CheckConnectionBetweenSwitchAndIxia: 检查ixia端口与交换机端口的连接
#
# 参数:
#           host：ixia地址
#           testerport ：ixia端口
#           sut ：被测交换机
#           sutport：交换机端口
# 返回值: 
#     1:连接正确
#     0：连接错误
#
# 使用举例:
#           CheckConnectionBetweenSwitchAndIxia 172.16.1.253 "2:1" s1 Ethernet1/1
######################################################################################
proc CheckConnectionBetweenSwitchAndIxia { host testerport sut sutport } {
    upvar 1 $host ixiaip
    upvar 1 $testerport tport
    upvar 1 $sut switch
    upvar 1 $sutport switchport
    set tp [split $tport :]
    set card [lindex $tp 0]
    set port [lindex $tp 1]
    ShutdownPort $switch $switchport
    Wait 5000
    ixInitialize $ixiaip
    set chasId [ixGetChassisID $ixiaip]
    for {set i 0} {$i < 10} {incr i} {
    	set linkstatedown [stat getLinkState $chasId $card $port]
    	if {$linkstatedown == 1} {
	    	Wait 5000
	    } else {
	    	break
	    }
    }
    NoShutdownPort $switch $switchport
    Wait 5000
    for {set i 0} {$i < 10} {incr i} {
    	set linkstateup [stat getLinkState $chasId $card $port]
    	if {$linkstatedown == 0} {
	    	Wait 5000
	    } else {
	    	break
	    }
    }
    if { $linkstatedown == 0 && $linkstateup == 1 } {
        PrintRes Print "Check $testerport\($tport) of $host\($ixiaip) should connect to $sutport\($switchport) of $sut\($switch), OK!"
        return 1
    } else {
        puts "linkstatedown = $linkstatedown; linkstateup = $linkstateup"
        PrintRes Print "Check $testerport\($tport) of $host\($ixiaip) should connect to $sutport\($switchport) of $sut\($switch), ERROR!"
        return 0
    }
}

#####################################################################################
#
# CheckConnectionBetweenSwtichAndSwitch: 检查ixia端口与交换机端口的连接
#
# 参数:
#           sut1 ：被测交换机1
#           sut1port：交换机1端口
#           sut2 ：被测交换机2
#           sut2port：交换机2端口
# 返回值: 
#     1:连接正确
#     0：连接错误
#
# 使用举例:
#           CheckConnectionBetweenSwtichAndSwitch s1 Ethernet1/1 s2 Ethernet1/1
######################################################################################
#新脚本请使用CheckConnectionBetweenSwitchAndSwitch，本函数有单词错误
proc CheckConnectionBetweenSwtichAndSwitch { sut1 sut1port sut2 sut2port } {
    upvar 1 $sut1 switch1
    upvar 1 $sut1port switch1port
    upvar 1 $sut2 switch2
    upvar 1 $sut2port switch2port
    EnterInterfaceMode $switch1 $switch1port
    receiver $switch1 "shutdown" 2
    receiver $switch1 "no shutdown"
    set RecvBuf [receiver $switch2 "\n" 10]
    set res [regexp -nocase $switch2port $RecvBuf]
    if { $res == 1 } {
        PrintRes Print "Check $sut1port\($switch1port) of $sut1\($switch1) should connect to $sut2port\($switch2port) of $sut2\($switch2), OK!"
        return 1
    } else {
        PrintRes Print "Check $sut1port\($switch1port) of $sut1\($switch1) should connect to $sut2port\($switch2port) of $sut2\($switch2), ERROR!"
        return 0
    }
}

proc CheckConnectionBetweenSwitchAndSwitch { sut1 sut1port sut2 sut2port } {
    upvar 1 $sut1 switch1
    upvar 1 $sut1port switch1port
    upvar 1 $sut2 switch2
    upvar 1 $sut2port switch2port
    EnterInterfaceMode $switch1 $switch1port
    receiver $switch1 "shutdown" 2
    receiver $switch1 "no shutdown"
    set RecvBuf [receiver $switch2 "\n" 10]
    set res [regexp -nocase $switch2port $RecvBuf]
    if { $res == 1 } {
        PrintRes Print "Check $sut1port\($switch1port) of $sut1\($switch1) should connect to $sut2port\($switch2port) of $sut2\($switch2), OK!"
        return 1
    } else {
        PrintRes Print "Check $sut1port\($switch1port) of $sut1\($switch1) should connect to $sut2port\($switch2port) of $sut2\($switch2), ERROR!"
        return 0
    }
}




#####################################################################################
#
# receiver: 向串口发送命令并获取命令输出
#
# 参数:
#           sut: 被测设备
#			command: 向串口发送的命令
#			timeout: 超时时间（秒），即将超时时间内的被测设备输出作为返回值，可选参数，默认值为0，
#			flag: 是否添加换行输入的标识，目前支持两个值即newline和nonewline，可选参数，默认值为newline
# 返回值: 
#     被测设备的输出信息
#
# 使用举例:
#   向被测设备s1发送命令config terminal但并不获取命令输出  
#		receiver s1 "config terminal"
#	向被测设备s2发送命令show version，获取1秒内的命令输出
#		set RecvBuf [receiver s2 "show version" 1]
#	向被测设备s1输入en?但不输入换行，用于获取帮助信息
#		set helpinfo [receiver s1 "en?" 1 nonewline]
# 说明: 如果输入的超时时间过小（0除外），导致命令的输出结束，receiver过程会根据---More---
#       向被测设备输入空格，直至命令输出结束
######################################################################################
#proc receiver {sut command {timeout 0} {flag newline}} {
#
#    #wait the previous command output to be flushed
#    set y 0
#    after 200 {set y 1}
#    vwait y
#    set RecvBuf ""
#
#    #Raise the notebook page before send command to the sut
#    if {[info exist ::autotest::FLAG]} {
#    	if {$::autotest::FLAG == 1} {
#    		$::moni::M(Win.Notebook) raise $sut
#    	}
#    }
#    
#    if {$flag == "newline"} { ;#add by ligc, 2004-9-27 for command test
#    	::moni::rs232_put $sut "$command\r"
#    } elseif {$flag == "nonewline"} {
#    	::moni::rs232_put $sut "$command"
#    } else {
#    	puts "Error parameters passed to receiver $sut $command $timeout $flag"
#    	return
#    }
#  	
#    set timeout [expr $timeout*1000]
#    if {$timeout <= 0} {
#		set ::moni::M(RecvFlag.$sut) 0
#    } else {
#	    set ::moni::M(RecvFlag.$sut) 1
#    }
#    
#    set pos_more 0
#    if {$timeout > 0 || [regexp -nocase {^ex} $command]} {
#        #query interval 100ms
#        set times [expr $timeout/100]
#        #puts "times = $times"
#        for {set i 0} {$i < $times} {incr i 1} {
#            set x 0
#            after 100 {set x 1}
#            vwait x
#            
#            #"---More---" appears another time
#            set pos_temp [string last "--More" $::moni::M(RecvBuf.$sut)]
#            #puts "pos_temp = $pos_temp,pos_more = $pos_more"
#            #puts "THE NO. $i :$::moni::M(RecvBuf.$sut)"
#            if {$pos_temp > $pos_more} {
#            	::moni::rs232_put $sut " "
#            	set pos_more $pos_temp
#            }
#        }
#        
#        
#        if {[regexp -nocase {^ex} $command]==1} {
#	        after 500
#        } else {
#	        #add by ligc 2004-10-11 elimate the potential dangerous ---More---
#	        set z 0
#	        after 4000 {set z 1}
#	        vwait z
#	        #puts "wait for 4000ms"
#        }
#        
#        set pos_temp [string last "--More" $::moni::M(RecvBuf.$sut)]
#        #puts "pos_temp = $pos_temp"
#	    #puts "::moni::M= $::moni::M(RecvBuf.$sut)"
#        while {$pos_temp > $pos_more} {
#            #puts "pos_temp = $pos_temp,pos_more = $pos_more"
#
#        	::moni::rs232_put $sut " "
#            	#puts "-------2--------after 100"
#            	after 2000
#        	set pos_more $pos_temp
#        	set z 0
#        	after 2000 {set z 1}
#        	vwait z
#        	set pos_temp [string last "--More" $::moni::M(RecvBuf.$sut)]	
#
#        }
#        #end of add
#    }
#    
#    set RecvBuf $::moni::M(RecvBuf.$sut)
#	set ::moni::M(RecvBuf.$sut) ""
#
#	update
#
#    set ::moni::M(RecvFlag.$sut) 0
#    #puts "$RecvBuf"
#      
#      #puts "before $RecvBuf"
#      regsub -all [format %c 0x0] $RecvBuf "@" RecvBuf
#      if {[regexp ">" $RecvBuf] ==1} {
#      	set z 0
#        after 2000 {set z 1}
#        vwait z
#      }
#      
#       ###add by liangdong 2008.4.8
#      regsub -all " --More--           " $RecvBuf "" RecvBuf
#		  ###add by liangdong end
#		  
#		  ###trim the string before the command in RecvBuf add by liuleic
#		  set commandindex [string first $command $RecvBuf]
#		  if {$commandindex != -1} {
#		  	set l [string length $command]
#		  	#set commandindex [expr {$l + $commandindex}]
#		  	set commandindex [expr {$l + $commandindex + 1 }] ;#modify by liangdong for trim \n after command
#		  	set RecvBuf [string range $RecvBuf $commandindex end]
##		  	set RecvBuf [string range $RecvBuf $commandindex end]
#		  }
#		  ########################################################
#		  regsub -all {\r} $RecvBuf "" RecvBuf   ;#去掉\r后，可能会导致部分脚本匹配错误，遇到时修改
#		  
#	return $RecvBuf
#}
#proc receiver {sut command {timeout 0} {forceflag true} {flag newline} } {
#
#    #wait the previous command output to be flushed
#    set ::moni::M(RecvBufFlag.$sut) 0    
#    set y 0
#    after 200 {set y 1}
#    vwait y
#    set RecvBuf ""
#
#    #Raise the notebook page before send command to the sut
#    if {[info exist ::autotest::FLAG]} {
#    	if {$::autotest::FLAG == 1} {
#    		$::moni::M(Win.Notebook) raise $sut
#    	}
#    }
#    
#    if {$flag == "newline"} { ;#add by ligc, 2004-9-27 for command test
#    	::moni::rs232_put $sut "$command\r"
#    } elseif {$flag == "nonewline"} {
#    	::moni::rs232_put $sut "$command"
#    } else {
#    	puts "Error parameters passed to receiver $sut $command $timeout $flag"
#    	return
#    }
#  	
#    set timeout [expr $timeout*1000]
#    if {$timeout <= 0} {
#		set ::moni::M(RecvFlag.$sut) 0
#    } else {
#	    set ::moni::M(RecvFlag.$sut) 1
#    }
#    
#    set pos_more 0
##    if {$timeout > 0 || [regexp -nocase {^ex} $command]} {
##}
#    if {$timeout > 0 } {
#        #query interval 100ms
#        set times [expr $timeout/100]
#        #puts "times = $times"
#        for {set i 0} {$i < $times} {incr i 1} {
#            set x 0
#            after 100 {set x 1}
#            vwait x
#            
#            
#            
#            #"---More---" appears another time
#            set pos_temp [string last "--More" $::moni::M(RecvBuf.$sut)]
#            #puts "pos_temp = $pos_temp,pos_more = $pos_more"
#            #puts "THE NO. $i :$::moni::M(RecvBuf.$sut)"
#            if {$pos_temp > $pos_more} {
#            	::moni::rs232_put $sut " "
#            	set pos_more $pos_temp
#            }
#            
#            if {$forceflag == "false"} {
#            	if {$::moni::M(RecvBufFlag.$sut) == 1} {
#            		set ::moni::M(RecvBufFlag.$sut) 0            	
#            	} else {
#            		set y 0
#            		after 300 {set y 1}
#            		vwait y
#            		incr i 3
#            		if {$::moni::M(RecvBufFlag.$sut) == 0} {
#            			break
#            		}
#            	}
#          	}
#          	
#          	
#        }
#        
#        
##        if {[regexp -nocase {^ex} $command]==1} {
##	        after 500
##        } else {
##	        #add by ligc 2004-10-11 elimate the potential dangerous ---More---
##	        set z 0
##	        after 4000 {set z 1}
##	        vwait z
##	        #puts "wait for 4000ms"
##        }
#        set y 0
#        after 3000 {set y 1};#modify by hansong,wait 3s for the long print copy to buffer
#        vwait y
#        
#        set pos_temp [string last "--More" $::moni::M(RecvBuf.$sut)]
#        #puts "pos_temp = $pos_temp"
#	    #puts "::moni::M= $::moni::M(RecvBuf.$sut)"
#	      if { $pos_temp > $pos_more} {
#	      	::moni::rs232_put $sut " "
#	      	set pos_more $pos_temp
#	      	set moreloop 1
#	      	while { $moreloop == 1} {
#	      		if {$::moni::M(RecvBufFlag.$sut) == 1} {
#            	set ::moni::M(RecvBufFlag.$sut) 0
#            	set x 0
#            	after 500 {set x 1}
#            	vwait x            	
#            } else {
#            	set y 0
#            	after 1000 {set y 1}
#            	vwait y
#            	if {$::moni::M(RecvBufFlag.$sut) == 0} {
#            		set pos_temp [string last "--More" $::moni::M(RecvBuf.$sut)]
#            		if {$pos_temp > $pos_more} {
#            			::moni::rs232_put $sut " "
#            			set pos_more $pos_temp
#            		} else {
#            			break
#            		}
#            	}
#            } 
#	      	}
#	      	
#	      }
#	    
#	    
#	    
##        while {$pos_temp > $pos_more} {
##            #puts "pos_temp = $pos_temp,pos_more = $pos_more"
##
##        	::moni::rs232_put $sut " "
##            	#puts "-------2--------after 100"
##            	after 2000
##        	set pos_more $pos_temp
##        	set z 0
##        	after 2000 {set z 1}
##        	vwait z
##        	set pos_temp [string last "--More" $::moni::M(RecvBuf.$sut)]	
##
##        }
#        #end of add
#    }
#    
#    set RecvBuf $::moni::M(RecvBuf.$sut)
#	set ::moni::M(RecvBuf.$sut) ""
#
#	update
#
#    set ::moni::M(RecvFlag.$sut) 0
#    #puts "$RecvBuf"
#      
#      #puts "before $RecvBuf"
#      regsub -all [format %c 0x0] $RecvBuf "@" RecvBuf
##      if {[regexp ">" $RecvBuf] ==1} {
##      	set z 0
##        after 2000 {set z 1}
##        vwait z
##      }
#      
#       ###add by liangdong 2008.4.8
#      regsub -all " --More--           " $RecvBuf "" RecvBuf
#		  ###add by liangdong end
#
#		####fix by liangdong 
#		regsub -all {\r} $RecvBuf "" RecvBuf   ;#去掉\r后，可能会导致部分脚本匹配错误，遇到时修改
#		####fix by liangdong end 避免部分命令行最后有特殊字符\r
#
#		  
#		  ###trim the string before the command in RecvBuf add by liuleic
#		  set commandindex [string first $command $RecvBuf]
#		  if {$commandindex != -1} {
#		  	set l [string length $command]
#		  	set commandindex [expr {$l + $commandindex + 1}]
#		  	set RecvBuf [string range $RecvBuf $commandindex end]
#		  }
#		  ########################################################
#		  #regsub -all {\r} $RecvBuf "" RecvBuf   ;#去掉\r后，可能会导致部分脚本匹配错误，遇到时修改
#	return $RecvBuf
#}
#####################################################################################
#
# receiver: 向串口发送命令并获取命令输出
#
# 参数:
#     sut: 被测设备
#			command: 向串口发送的命令
#			timeout: 超时时间（秒），即将超时时间内的被测设备输出作为返回值，可选参数，默认值为0，
#			args:  可选参数 Flag TimeStop PromoteStop
#            Flag 是否添加回车输入的标识，目前支持两个值即newline和nonewline，可选参数，默认值为newline
#            PromoteStop 是否等待提示符，默认值为false，即不必等待提示符出现，此时函数在timeout后的2秒内检查是否出现提示符或--More--，若均未出现则返回。
#                        若为true，则函数必须等待到提示符出现时才返回
#            TimeStop    是否在timeout时间到达时强制函数返回，默认false，即timeout时间到时，若交换机继续有输出仍然等待交换机输出完毕。
# 返回值: 
#     被测设备的输出信息
#
# 说明:
#   提示符有：#，>,[Boot]: BCM.0>,->
#   PromoteStop参数为false是为了兼容debug信息
#   目前的修改，不影响以前的脚本，并可以在很大程度上避免丢字符的情况
# 举例：
#     receiver s1 "show running"  
#     receiver s1 "show running" 10
#     receiver s1 "set default"
#     receiver s1 "set default" 0 PromoteStop true ,#只在等待到提示符才退出。
######################################################################################
proc receiver {sut command {timeout 0} args} {

  set ::moni::M(RecvFlag.$sut) 0
  set RecvBuf ""
  set ::moni::M(RecvBuf.$sut) ""
	set ::moni::M(RecvBufFlag.$sut) 0
  set ::moni::M(RecvFlag.$sut) 1
  
  set TimeStop false
  set PromoteStop false
  set Flag newline
  set DropCharRepeat true
  set DropCharRepeatNum 2
  set DropCharRepeatError {% Invalid input detected at '^' marker.}
  set SpecialCharReturn {(^[-a-zA-Z0-9_]{0,30}(\(.*\))?[#>])|(^\[Boot]: $)|(^BCM\.[0-9]> $)|(^-> $)}
  set SpecialCharReturnTime false
  if {[llength $args]} {
  	array set arrArgs $args 	
  	foreach {para value} [array get arrArgs] {	
			switch -exact -- $para {
			    TimeStop {
			    	set TimeStop $value
			    }
			    PromoteStop {
			    	set PromoteStop $value
			    }
			    Flag {
			    	set Flag $value
			    }
			    SpecialCharReturn {
			    	set SpecialCharReturn $value
			    }
			    DropCharRepeat {
			    	set DropCharRepeat $value
			    }
			    DropCharRepeatNum {
			    	set DropCharRepeatNum $value
			    }
			    DropCharRepeatError {
			    	set DropCharRepeatError $value
			    }
			    SpecialCharReturnTime {
			    	set SpecialCharReturnTime $value
			    }
			  }
			}
  }
  #Raise the notebook page before send command to the sut
  if {[info exist ::autotest::FLAG]} {
    if {$::autotest::FLAG == 1} {
    	$::moni::M(Win.Notebook) raise $sut
    }
  }
    
    
    if {$Flag == "newline"} {
    	::moni::rs232_put $sut "$command\r"
    } elseif {$Flag == "nonewline"} {
    	::moni::rs232_put $sut "$command"
    } else {
    	set ::moni::M(RecvFlag.$sut) 0
    	puts "Error parameters"
    	return
    }
  	
#  	set command "show ipv6 neighbor"
    set timeout [expr $timeout*1000]
    set repeattime $timeout
    while {$timeout > 0 } {
    	set x 0
    	after 100 {set x 1}
    	vwait x
    	regsub -all {\r} $::moni::M(RecvBuf.$sut) "" ::moni::M(RecvBuf.$sut)
    	if {$DropCharRepeat == "true" && $DropCharRepeatNum > 0} {
    		if {[string first "$command" $::moni::M(RecvBuf.$sut)] == -1 && [string first $DropCharRepeatError $::moni::M(RecvBuf.$sut)] != -1 } {
    			puts $::moni::M(RecvBuf.$sut)
    			set ::moni::M(RecvBuf.$sut) ""
    			if {$Flag == "newline"} {
    			::moni::rs232_put $sut "$command\r"
    			} elseif {$Flag == "nonewline"} {
    				::moni::rs232_put $sut "$command"
    			}
    			set timeout $repeattime
    			incr DropCharRepeatNum -1
    		}
    	}
    	
    				
			regsub -all "          " $::moni::M(RecvBuf.$sut) "" ::moni::M(RecvBuf.$sut)
			if {[regexp -line {^ --More-- } $::moni::M(RecvBuf.$sut)] == 1} {
				::moni::rs232_put $sut " "
				regsub -all " --More-- " $::moni::M(RecvBuf.$sut) "" ::moni::M(RecvBuf.$sut)				
			}
			if {$SpecialCharReturnTime == "true"} {
				set matchline $SpecialCharReturn
				if {[regexp -line $matchline $::moni::M(RecvBuf.$sut)] == 1} {
					break
				}
			}
			
			set timeout [expr {$timeout - 100}]
    }
    set y 0
    if {$TimeStop == "false"} {
		regsub -all {\r} $::moni::M(RecvBuf.$sut) "" ::moni::M(RecvBuf.$sut)
		regsub -all " --More-- " $::moni::M(RecvBuf.$sut) "" ::moni::M(RecvBuf.$sut)
		regsub -all "          " $::moni::M(RecvBuf.$sut) "" ::moni::M(RecvBuf.$sut)
	    set matchline $SpecialCharReturn
			
		
	    
	    #查看最后一个字符是否是#	    
	    while {1} {
	      set x 0
	      
	      after 100 {set x 1}	      
	      vwait x

		  if {[regexp -line {^ --More-- } $::moni::M(RecvBuf.$sut)] == 1} {
				set y 0
				::moni::rs232_put $sut " "
				regsub -all " --More-- " $::moni::M(RecvBuf.$sut) "" ::moni::M(RecvBuf.$sut)
		  }
		  regsub -all {\r} $::moni::M(RecvBuf.$sut) "" ::moni::M(RecvBuf.$sut)	      	
		  regsub -all "          " $::moni::M(RecvBuf.$sut) "" ::moni::M(RecvBuf.$sut)	

	      set checkrecvbuf $::moni::M(RecvBuf.$sut)
	      
	      incr y 1
	      if {$DropCharRepeat == "true" && $DropCharRepeatNum > 0} {
	    		if {[string first "$command" $checkrecvbuf] == -1 && [string first $DropCharRepeatError $checkrecvbuf] != -1 } {
	    			puts $checkrecvbuf 
	    			set ::moni::M(RecvBuf.$sut) ""
	    			set checkrecvbuf ""
	    			if {$Flag == "newline"} {
	    			::moni::rs232_put $sut "$command\r"
	    			} elseif {$Flag == "nonewline"} {
	    				::moni::rs232_put $sut "$command"
	    			}
	    			incr DropCharRepeatNum -1
	    			set y 0
	    		}
    		}	
			
			if {$PromoteStop == "false"} {
			  if {$y > 50} {
			  	break
			  }
			} else {
				set y 0
			}

		     if {[regexp -line $matchline $checkrecvbuf] == 1} {
		     	break
		     }
	  }
	}
   
  #
  set ::moni::M(RecvFlag.$sut) 0
  set RecvBuf $::moni::M(RecvBuf.$sut)
	set ::moni::M(RecvBuf.$sut) ""
	update

  regsub -all [format %c 0x0] $RecvBuf "@" RecvBuf
  regsub -all " --More--           " $RecvBuf "" RecvBuf
	regsub -all {\r} $RecvBuf "" RecvBuf  

	set commandindex [string first $command $RecvBuf]
	if {$commandindex != -1} {
		set l [string length $command]
		set commandindex [expr {$l + $commandindex + 1}]
		set RecvBuf [string range $RecvBuf $commandindex end]
	}
	return $RecvBuf
}


# add by ligc 2004-10-19, suggested by weixhb
# alias name for reiceiver
proc rc {sut command {timeout 0} {flag newline}} {
	receiver $sut $command $timeout $flag
}

#add by ligc 2004-10-20, suggested by caoyg
#####################################################################################
#
# receiver2: 向串口发送命令并获取命令输出
#
# 参数:
#           sut: 被测设备
#			command: 向串口发送的命令
#			flag: 是否添加换行输入的标识，目前支持两个值即newline和nonewline，可选参数，默认值为newline
#			cmdoutput:命令输出结束的标志
# 返回值: 
#     被测设备的输出信息
#
# 使用举例:
#   向被测设备s1发送命令config terminal
#		receiver2 s1 "config terminal"
#	向被测设备s2发送命令show interface，同时获得屏幕输出
#		set RecvBuf [receiver2 s2 "show interface"]
#	向被测设备s1输入en?但不输入换行，用于获取帮助信息
#		set helpinfo [receiver2 s1 "en?" nonewline]
# 说明: receiver2过程会根据---More---向被测设备输入空格，直至命令输出结束
######################################################################################
proc receiver2 {sut command {flag newline} {cmdoutput "#|>"}} {

    #wait the previous command output to be flushed
    set y 0
    after 200 {set y 1}
    vwait y
    set RecvBuf ""

    #Raise the notebook page before send command to the sut
    if {[info exist ::autotest::FLAG]} {
    	if {$::autotest::FLAG == 1} {
    		$::moni::M(Win.Notebook) raise $sut
    	}
    }
    
    if {$flag == "newline"} { ;#add by ligc, 2004-9-27 for command test
    	::moni::rs232_put $sut "$command\n"
    } elseif {$flag == "nonewline"} {
    	::moni::rs232_put $sut "$command"
    } else {
    	puts "Error parameters passed to receiver $sut $command $timeout $flag"
    	return
    }
  	
    set ::moni::M(RecvFlag.$sut) 1
    
    set pos_more 0
    while {![regexp -nocase $cmdoutput $::moni::M(RecvBuf.$sut)]} {
        #query interval 100ms
        set x 0
        after 100 {set x 1}
        vwait x
            
        #"---More---" appears another time
        set pos_temp [string last "---More---" $::moni::M(RecvBuf.$sut)]
        #puts "pos_temp = $pos_temp,pos_more = $pos_more"
        if {$pos_temp > $pos_more} {
         	::moni::rs232_put $sut " "
          	set pos_more $pos_temp
        }
    }
    
    set RecvBuf $::moni::M(RecvBuf.$sut)
	set ::moni::M(RecvBuf.$sut) ""
	update
    set ::moni::M(RecvFlag.$sut) 0
	return $RecvBuf
}

# add by ligc 2004-10-20, suggested by caoyg
# alias name for reiceiver2
proc rc2 {sut command {flag newline} {cmdoutput "#|>"}} {
	receiver2 $sut $command $flag $cmdoutput
}

#####################################################################################
#
# PrintRes: 打印输出
#
# 参数:
#           
# 返回值: 
#     
#
# 使用举例:
#PrintRes TestCase 4.1.1 Step 1 Flag FAILED
#PrintRes TestCase 4.1.1 Step 1 Flag ERROR
#PrintRes TestCase 4.1.1 Step 1 Flag PASSED
#PrintRes TestCase 4.1.1 Step 1 Flag FAILED Expect aaaaaaaaaaaaaaaaaaaaaaaaaaaaa
#PrintRes TestCase 4.1.1 Step 1 Flag ERROR Expect aaaaaaaaaaaaaaaaaaaaaaaaaaaaa
#PrintRes TestCase 4.1.1 Step 1 Flag PASSED Expect aaaaaaaaaaaaaaaaaaaaaaaaaaaaa
#printRes Print "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
#
#           
######################################################################################
proc PrintRes { args } {
    array set arrArgs $args
    #以下判断默认不向LOG文件输出
    if {[info exists arrArgs(DebugFlag)] && $arrArgs(DebugFlag) == "true"} {
        set debugflag true
    } else {
        #debugflag == true 向LOG文件输出
        set debugflag false
    }
    if {[info exists arrArgs(TestCase)] && [info exists arrArgs(Step)] && [info exists arrArgs(Flag)]} {
        if {[regexp -nocase FAILED $arrArgs(Flag)] == 1 || [regexp -nocase ERROR $arrArgs(Flag)] == 1} {
            if {[info exists arrArgs(Expect)]} {
                set printStr "! Test case $arrArgs(TestCase), step $arrArgs(Step) is $arrArgs(Flag)!($arrArgs(Expect))"
                PrintToScreenLogfileResfile $printStr $debugflag stderr
                #记录测试中的错误测试例已经测试例通过和失败的总数
                if {[info exist ::autotest::VAR(failedresfile)]} {
#                    puts $::autotest::VAR(failedresfile) $str
                if { $::autotest::VAR(counterflag) == 0 } {
                 #edit by lixiaa 2009-11-19
                     if {$::autotest::VAR(RerunFlag) == 1 }  {
                      append ::autotest::VAR(Rerunfailedbuf) "\nTest case $arrArgs(TestCase), $::autotest::VAR(failedpurpose) \nstep $arrArgs(Step)  "
                	append ::autotest::VAR(Rerunfailedcase) "\n$arrArgs(TestCase)"
                     } else {
                	append ::autotest::VAR(failedbuf) "\nTest case $arrArgs(TestCase), $::autotest::VAR(failedpurpose) \nstep $arrArgs(Step)  "
                	append ::autotest::VAR(failedcase) "\n$arrArgs(TestCase)"
                	}
		            	set ::autotest::VAR(counterflag) 1
		          } else {
		          if {$::autotest::VAR(RerunFlag) == 1 }  {
		              append ::autotest::VAR(Rerunfailedbuf) "step $arrArgs(Step)  "
		          } else {
		          	append ::autotest::VAR(failedbuf) "step $arrArgs(Step)  "
		          	}
		          }
		        }
		        #puts "$::autotest::VAR(counterflag) $::autotest::VAR(counterpass) $::autotest::VAR(counterfailed)"
		        if {[info exist ::moni::M(Script.ErrorStop)] && $::moni::M(Script.ErrorStop) == 1} {
                    ::autotest::pause_test
                }
            } else {
                set printStr "! Test case $arrArgs(TestCase), step $arrArgs(Step) is $arrArgs(Flag)!"
                PrintToScreenLogfileResfile $printStr $debugflag stderr  
                #记录测试中的错误测试例已经测试例通过和失败的总数
                if {[info exist ::autotest::VAR(failedresfile)]} {
#                    puts $::autotest::VAR(failedresfile) $str
                if { $::autotest::VAR(counterflag) == 0 } {
                #edit by lixiaa  2009-11-19
                	if {$::autotest::VAR(RerunFlag) == 1 }  {
                	        append ::autotest::VAR(Rerunfailedbuf) "\nTest case $arrArgs(TestCase), $::autotest::VAR(failedpurpose) \nstep $arrArgs(Step)  "
                    		append ::autotest::VAR(Rerunfailedcase) "\n$arrArgs(TestCase)"
                	} else {
                		append ::autotest::VAR(failedbuf) "\nTest case $arrArgs(TestCase), $::autotest::VAR(failedpurpose) \nstep $arrArgs(Step)  "
                    		append ::autotest::VAR(failedcase) "\n$arrArgs(TestCase)"
                     }
		            	set ::autotest::VAR(counterflag) 1
		          } else {
		         	if {$::autotest::VAR(RerunFlag) == 1 }  {
		          		append ::autotest::VAR(Rerunfailedbuf) "step $arrArgs(Step)  "
		         	} else {
		          		append ::autotest::VAR(failedbuf) "step $arrArgs(Step)  "
		          	}
		          }
		        }
                if { [info exist ::moni::M(Script.ErrorStop)] && $::moni::M(Script.ErrorStop) == 1} {
                    ::autotest::pause_test
                }
            }
            return 0
        } else {
            if {[info exists arrArgs(Expect)]} {
                set printStr "> Test case $arrArgs(TestCase), step $arrArgs(Step) is $arrArgs(Flag)!($arrArgs(Expect))"
                PrintToScreenLogfileResfile $printStr $debugflag 
                #记录测试中的错误测试例已经测试例通过和失败的总数
#                if {[info exist ::autotest::VAR(failedresfile)]} {
##		            incr ::autotest::VAR(counterpass) 1
#		        }
		        return 1
            } else {
                set printStr "> Test case $arrArgs(TestCase), step $arrArgs(Step) is $arrArgs(Flag)!"
                PrintToScreenLogfileResfile $printStr $debugflag 
                #记录测试中的错误测试例已经测试例通过和失败的总数
#                if {[info exist ::autotest::VAR(failedresfile)]} {
#		            incr ::autotest::VAR(counterpass) 1
#		        }
		        return 2  
            } 
        }
    }
    if {[info exists arrArgs(Print)]} {
        if {[regexp -nocase "check physical link or port state of ixia" $arrArgs(Print)] == 1 } {
            set printStr "! $arrArgs(Print)"   ;#add by liangdong 20080527
        	PrintToScreenLogfileResfile $printStr $debugflag stderr
        	if {$::autotest::multicaseflag == 1} {
        		::autotest::pause_test
        	} else {
        		::autotest::stop_current_test
        	}
        	return 4        	
        }    	
        if {[regexp -nocase FAILED $arrArgs(Print)] == 1 || [regexp -nocase ERROR $arrArgs(Print)] == 1} {
            set printStr "! $arrArgs(Print)"
            PrintToScreenLogfileResfile $printStr $debugflag stderr
            #记录测试中的错误测试例已经测试例通过和失败的总数
#            if {[info exist ::autotest::VAR(failedresfile)]} {
#                puts $::autotest::VAR(failedresfile) $str
#		        incr ::autotest::VAR(counterfailed) 1
#		    }
            if {[info exist ::moni::M(Script.ErrorStop)] && $::moni::M(Script.ErrorStop) == 1} {
                ::autotest::pause_test
            }
            return 0         
        } else {
            set printStr "> $arrArgs(Print)"
            PrintToScreenLogfileResfile $printStr $debugflag
            #记录测试中的错误测试例已经测试例通过和失败的总数
#            if {[info exist ::autotest::VAR(failedresfile)]} {
#		        incr ::autotest::VAR(counterpass) 1
#		    }
		    return 3 
        }
    }
    if {[info exists arrArgs(RecvBuf)]} {
        set printStr "> $arrArgs(RecvBuf)"
        PrintToScreenLogfileResfile $printStr $debugflag
        return 5
    }
        
}
#####################################################################################
#
# PrintToScreenLogfileResfile: 打印运行信息到标准输出与日志
#
# 参数:
#           
# 返回值: 
#     
#
# 使用举例:
#           
######################################################################################
proc PrintToScreenLogfileResfile { printStr {debugflag true} {ioflag stdout} } {
    puts $ioflag $printStr
    if { $debugflag == "true" } {
        LogPuts  $::autotest::VAR(number) $printStr
    }
    if {[info exist ::autotest::VAR(resfile)]} {
		puts $::autotest::VAR(resfile) $printStr
	}
}

#####################################################################################
#
# PrintInfo: 打印运行信息
#
# 参数:
#           args ：TestCase Step OperateStep Purpose TestInitial TestTarget Timer
# 返回值: 
#     
#
# 使用举例:
#PrintInfo TestCase 4.1.1 Purpose "test print info" Timer start
#PrintInfo TestCase 4.1.1 Purpose "test print info bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbaaaaaaaaaaaaaaaaaa" Timer start
#PrintInfo TestCase 4.1.1 Step 1 OperateStep "{s1:Enable ipv6} {s2:Enable ipv6 bbbbbbb} {s3:Enable ipv6 aaaaaaa}" Expect "Ipv6 enable on s1/s2/s3"
#PrintInfo TestCase 4.1.1 Step 1 OperateStep "{s1:Enable ipv6 bbbbbbbbbbbbbbbbbbbbbbaaaaaaaaaaaaaaaaaaaaabbbbbbbbbbbsssssssssssssssssss} {s2:Enable ipv6 bbbbbbb} {s3:Enable ipv6 aaaaaaa}" Expect "Ipv6 enable on s1/s2/s3"
#PrintInfo TestCase 4.1.1 Step 1 Expect "Ipv6 enable on s1/s2/s3"
#PrintInfo TestCase 4.1.1 Step 1 Expect "Ipv6 enable on s1/s2/s3 bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbsssssssssssssssssssssssssssssssssss"
#PrintInfo TestCase 4.1.1 Timer end
#PrintInfo TestCase 4.1.1
#
#PrintInfo TestTarget DCSCM Timer start
#PrintInfo TestTarget DCSCM Timer end
#PrintInfo TestInitial Initial Timer start
#PrintInfo TestInitial Initial Timer end
#PrintInfo TestInitial Uninitial Timer start
#PrintInfo TestInitial Uninitial Timer end
#           
######################################################################################

proc PrintInfo { args } {
    array set arrArgs $args
    if {[info exists arrArgs(DebugFlag)] && $arrArgs(DebugFlag) == "false"} {
        set debugflag false
    } else {
        set debugflag true
    }
    set printTopButtom [string repeat # 80]
    if {[info exists arrArgs(TestTarget)] && [info exists arrArgs(Timer)] && $arrArgs(Timer) == "start"} {
    	  
    	  #设置测试例运行时间标志为0，初始化
    	  set ::autotest::TestCaseRunTimeFlag 0
    	  
        PrintLogNewLineStart
        PrintToScreenLogfileResfile $printTopButtom $debugflag
        set printStr [format "# %s #" [format "%-76s" "Test $arrArgs(TestTarget), Started at [clock format [clock seconds] -format "%H:%M on %D"]"]]
        PrintToScreenLogfileResfile $printStr $debugflag
        PrintToScreenLogfileResfile $printTopButtom $debugflag
        PrintLogNewLineEnd
        return 4
    }
    if {[info exists arrArgs(TestTarget)] && [info exists arrArgs(Timer)] && $arrArgs(Timer) == "end"} {
        PrintLogNewLineStart
        PrintToScreenLogfileResfile $printTopButtom $debugflag
        set printStr [format "# %s #" [format "%-76s" "Test $arrArgs(TestTarget), Finished at [clock format [clock seconds] -format "%H:%M on %D"]"]]
        PrintToScreenLogfileResfile $printStr $debugflag
        PrintToScreenLogfileResfile $printTopButtom $debugflag
        PrintLogNewLineEnd
        return 5
    }
    if {[info exists arrArgs(TestInitial)] && [info exists arrArgs(Timer)] && $arrArgs(Timer) == "start"} {
        PrintLogNewLineStart
        PrintToScreenLogfileResfile $printTopButtom $debugflag
        set printStr [format "# %s #" [format "%-76s" "$arrArgs(TestInitial) switch, Started at [clock format [clock seconds] -format "%H:%M on %D"]"]]
        PrintToScreenLogfileResfile $printStr $debugflag
        PrintToScreenLogfileResfile $printTopButtom $debugflag
        PrintLogNewLineEnd
        return 6
    }
    if {[info exists arrArgs(TestInitial)] && [info exists arrArgs(Timer)] && $arrArgs(Timer) == "end"} {
        PrintLogNewLineStart
        PrintToScreenLogfileResfile $printTopButtom $debugflag
        set printStr [format "# %s #" [format "%-76s" "$arrArgs(TestInitial) switch, Finished at [clock format [clock seconds] -format "%H:%M on %D"]"]]
        PrintToScreenLogfileResfile $printStr $debugflag
        PrintToScreenLogfileResfile $printTopButtom $debugflag
        PrintLogNewLineEnd
        return 7
    }    
    if {[info exists arrArgs(TestCase)] && [info exists arrArgs(Purpose)] && [info exists arrArgs(Timer)] && $arrArgs(Timer) == "start"} {
        set  ::autotest::VAR(failedpurpose) "Purpose: $arrArgs(Purpose)"
        PrintLogNewLineStart
        PrintToScreenLogfileResfile $printTopButtom $debugflag
        set strLengthOfTestCase [string length $arrArgs(TestCase)]
        set strLengthOfPurpose [string length $arrArgs(Purpose)]
        set strLength [expr $strLengthOfTestCase + $strLengthOfPurpose]
        set line [expr $strLength / 76 + 1]
        set spaceNum [expr 12 + $strLengthOfTestCase]
        set strSpace [string repeat " " $spaceNum]
        set printStr [format "# %s #" [format "%-76s" [ string range "Test case $arrArgs(TestCase), $arrArgs(Purpose)" [expr 76*0]  [expr 76*(0 + 1) - 1]]]]
        PrintToScreenLogfileResfile $printStr $debugflag
        for {set i 1} { $i < $line } { incr i} {
            set printStr [format "# $strSpace%s #" [format "%-*s" [expr 76 - $spaceNum] [ string range "Test case $arrArgs(TestCase), $arrArgs(Purpose)" [expr 76 * $i - $spaceNum * ($i - 1)]  [expr 76*($i + 1) - 1 - $spaceNum * $i]]]] 
            PrintToScreenLogfileResfile $printStr $debugflag
        }
        set printStr [format "# $strSpace%s #" [format "%-*s" [expr 76 - $spaceNum] "Started at [clock format [clock seconds] -format "%H:%M on %D"]"]]       
        PrintToScreenLogfileResfile $printStr $debugflag 
        PrintToScreenLogfileResfile $printTopButtom $debugflag
        PrintLogNewLineEnd
        
        #设置测试例开始执行的时间，并置标志位
        set ::autotest::TestCaseRunTime [ clock seconds]
    	  set ::autotest::TestCaseRunTimeFlag 1
    	  
        return 1      
    }    
    if {[info exists arrArgs(TestCase)] && [info exists arrArgs(Step)]} {
        PrintLogNewLineStart
        PrintToScreenLogfileResfile $printTopButtom $debugflag
        set printStr [format "# %s #" [format "%-76s" "Test case $arrArgs(TestCase), Step $arrArgs(Step)"]]
        PrintToScreenLogfileResfile $printStr $debugflag
        if { [info exists arrArgs(OperateStep)] } {
            set num [llength $arrArgs(OperateStep)]
            for { set i 0 } { $i < $num} {incr i} {
                set strLengthOfOperateStep [string length [lindex $arrArgs(OperateStep) $i]]
                set line [expr $strLengthOfOperateStep/71 + 1]
                for {set j 0} { $j < $line } { incr j } {
                    set printStr [format "#      %s #" [format "%-71s" [ string range [lindex $arrArgs(OperateStep) $i] [expr 71*$j]  [expr 71*($j + 1) - 1]]]]
                    PrintToScreenLogfileResfile $printStr $debugflag
                }        
            }
            if {[info exists arrArgs(Expect)]} {
                set strLengthOfExpect [expr [string length $arrArgs(Expect)] + 23 ]
                set line [expr $strLengthOfExpect/76 + 1]
                for {set i 0} { $i < $line } { incr i } {
                    set printStr [format "# %s #" [format "%-76s" [ string range "The result should be : $arrArgs(Expect)" [expr 76*$i]  [expr 76*($i + 1) - 1]]]]
                    PrintToScreenLogfileResfile $printStr $debugflag
                }
            }         
        } else {
            if {[info exists arrArgs(Expect)]} {
                set strLengthOfExpect [expr [string length $arrArgs(Expect)] + 23 ]
                set line [expr $strLengthOfExpect/76 + 1]
                for {set i 0} { $i < $line } { incr i } {
                    set printStr [format "# %s #" [format "%-76s" [ string range "The result should be : $arrArgs(Expect)" [expr 76*$i]  [expr 76*($i + 1) - 1]]]]
                    PrintToScreenLogfileResfile $printStr $debugflag
                }
            }
        }
        PrintToScreenLogfileResfile $printTopButtom $debugflag
        PrintLogNewLineEnd
        return 2      
    }    
    if {[info exists arrArgs(TestCase)] && [info exists arrArgs(Timer)] && $arrArgs(Timer) == "end"} {
        PrintLogNewLineStart
        PrintToScreenLogfileResfile $printTopButtom $debugflag
        set printStr [format "# %s #" [format "%-76s" "Test case $arrArgs(TestCase), Finished at [clock format [clock seconds] -format "%H:%M on %D"]"]]
        PrintToScreenLogfileResfile $printStr $debugflag
        
        #获得测试例结束时间，计算结束与开始之差，写入日志
        if {$::autotest::TestCaseRunTimeFlag == 1} {
        	set currentclock [ clock seconds]
					set duration [expr {$currentclock - $::autotest::TestCaseRunTime} ]
					if {$duration >= 0 } {
						set h [expr { $duration / 3600 } ]
						set m [expr { $duration % 3600 / 60 } ]
						set s [expr { $duration % 3600 % 60 } ]
						set printStr [format "# %s #" [format "%-76s" "TestCase Duration Time: $h:$m:$s Sec"]]
						PrintToScreenLogfileResfile $printStr $debugflag
						set ::autotest::TestCaseRunTimeFlag 0
					}
		
        }
        
        PrintToScreenLogfileResfile $printTopButtom $debugflag
        PrintLogNewLineEnd
        if {[info exist ::autotest::VAR(failedresfile)]} {
        #edit by lixiaa 2009-11-19
       	 if { $::autotest::VAR(counterflag) == 1 } {
                      if {$::autotest::VAR(RerunFlag) == 1 }  {      	                  
		            incr ::autotest::VAR(Reruncounterfailed) 1
                      } else {
                 	    incr ::autotest::VAR(counterfailed) 1
                      }
		          } else {
                      	if {$::autotest::VAR(RerunFlag) == 1 }  {  
                      		 incr ::autotest::VAR(Reruncounterpass) 1
		        	} else {
		         		 incr ::autotest::VAR(counterpass) 1

		       		}  
		        }
		        #puts "$::autotest::VAR(counterflag) $::autotest::VAR(counterpass) $::autotest::VAR(counterfailed)"
		        set ::autotest::VAR(counterflag) 0
		        set ::autotest::VAR(failedpurpose) ""
    }
        return 3                
    } else {
        puts stderr [format "# %s #" [format "%-76s" "ERROR ARGS"]]
        return 0
    }
    
}
#####################################################################################
#
# Random: 获得随机数
#
# 参数:
#           start：随机数开始值
#           end ：随机数结束值
# 返回值: 
#     随机数
#
# 使用举例:
#           Random 10 20
######################################################################################
#Random 2 4094 
#Random 2 4094  10
#Random 2 4094  1
#Random 2 4094  1 {10 20 100 1000}
#Random 2 4094 10 {10 20 100 1000}
proc Random { start end {num 1} {exceptlist ""}} {
    if { $num == 1 } {
    	if { $exceptlist == "" } {
	        return [expr int(($end - $start) * rand() + $start)]
        } else {
        	set res [expr int(($end - $start) * rand() + $start)]
        	while { [lsearch $res $exceptlist] >= 0 } {
        		set res [expr int(($end - $start) * rand() + $start)]
        		continue
        	}
        	return $res
        }     	
    } else {
        set randomlist ""
        if { $exceptlist == "" } {
	        for {set i 0} {$i < $num} {incr i} {
	            set randomtemp [expr int(($end - $start) * rand() + $start)]
	            while {[lsearch -exact $randomlist $randomtemp] >= 0} {
	                set randomtemp [expr int(($end - $start) * rand() + $start)]
	            }
	            lappend randomlist $randomtemp
	        }
	        return $randomlist
	    } else {
	    	for {set i 0} {$i < $num} {incr i} {
	            set randomtemp [expr int(($end - $start) * rand() + $start)]
	            while {[lsearch -exact $randomlist $randomtemp] >= 0 || [lsearch $randomtemp $exceptlist] >= 0 } {
	                set randomtemp [expr int(($end - $start) * rand() + $start)]
	            }
	            lappend randomlist $randomtemp
	        }
	        return $randomlist
	     }
    }
}
#GetInterfaceName 可以获得某设备的所有端口集合名称
#                   可以获得某设备上除指定端口外的所有端口集合名称
#                   可以获得某设备上除制定端口外的随机一个端口名称
#                   可以获得某设备的制定端口集合名称
#                   （以上端口仅限于同一板卡或盒式交换机）
#GetInterfaceName 12 Example Ethernet1/1
#GetInterfaceName 12 Except Ethernet1/1
#GetInterfaceName 12 Except {Ethernet1/1 Ethernet1/2}
#GetInterfaceName 12 Another {Ethernet1/1 Ethernet1/2}
#GetInterfaceName 0 Combination {Ethernet1/1 Ethernet1/2}
#on blade 
#GetInterfaceName 12 Example Ethernet0/0/1
#GetInterfaceName 12 Except Ethernet0/0/1
#GetInterfaceName 12 Except {Ethernet0/0/1 Ethernet0/0/2}
#GetInterfaceName 12 Another {Ethernet0/0/1 Ethernet0/0/2}
#GetInterfaceName 0 Combination {Ethernet0/0/1 Ethernet0/0/2}
proc GetInterfaceName { portnum args } {
    array set arrArgs $args
    foreach {para value} [array get arrArgs] {
		switch -exact -- $para {
		    Example {
		    	set Example $value
		    }
		    Except {
		    	set Except $value
		    }
		    Another {
		        set Another $value
		    }
		    Combination {
		        set Combination $value
		    }
		    default {
		        puts "may be some error para"
		        return 0
		    }
		}
    }
    if { $portnum != 0 } {
        if [info exists Example] {
            set res2 [regexp -nocase "Ethernet\(\[0-9\]+\)/\(\[0-9\]+\)/\(\[0-9\]+\)" $Example match chas card port]
            set res1 [regexp -nocase "Ethernet\(\[0-9\]+\)/\(\[0-9\]+\)" $Example match card1 port1]
            if { $res2 == 1 } {
            	return "Ethernet$chas/$card/1-$portnum"
            } elseif { $res1 == 1 } {
                return "Ethernet$card1/1-$portnum"
            } else {
                puts "the example portname may be unnormal portname!"
                return 0
            }
        }
        if [info exists Another] {
            set portname ""
            set firststring ""
            for {set i 1} {$i <= $portnum} {incr i} {
                lappend portname $i
            }
            set exceptportnum [llength $Another]
            for {set i 0} {$i < $exceptportnum} {incr i} {
                set res2 [regexp -nocase "Ethernet\(\[0-9\]+\)/\(\[0-9\]+\)/\(\[0-9\]+\)" [lindex $Another $i] match chas card port]
                set res1 [regexp -nocase "Ethernet\(\[0-9\]+\)/\(\[0-9\]+\)" [lindex $Another $i] match card1 port1]
                if { $res2 == 1 } {
                	set firststring Ethernet$chas/$card/
                    set index [lsearch -exact $portname $port]
                    set portname [lreplace $portname $index $index ] 
                } elseif { $res1 == 1 } {
                    set firststring Ethernet$card1/
                    set index [lsearch -exact $portname $port1]
                    set portname [lreplace $portname $index $index ]       
                } else {
                    puts "the another portname may be unnormal portname!"
                    return 0
                }
            }
            #puts $portname
            return [append firststring [lindex $portname [Random 0 [expr [llength $portname] - 1]]]]
        }
        if [info exists Except] {
            #set Except [lsort -dictionary $Except]
            set portname ""
            set firststring ""
            for {set i 1} {$i <= $portnum} {incr i} {
                lappend portname $i
            }
            set exceptportnum [llength $Except]
            for {set i 0} {$i < $exceptportnum} {incr i} {
                set res2 [regexp -nocase "Ethernet\(\[0-9\]+\)/\(\[0-9\]+\)/\(\[0-9\]+\)" [lindex $Except $i] match chas card port]
                set res1 [regexp -nocase "Ethernet\(\[0-9\]+\)/\(\[0-9\]+\)" [lindex $Except $i] match card1 port1]
                if { $res2 == 1 } {
                	set firststring Ethernet$chas/$card/
                    set index [lsearch -exact $portname $port]
                    set portname [lreplace $portname $index $index ]  
                } elseif { $res1 == 1 } {
                    set firststring Ethernet$card1/
                    set index [lsearch -exact $portname $port1]
                    set portname [lreplace $portname $index $index ]       
                } else {
                    puts "the except portname may be unnormal portname!"
                    return 0
                }
            }
            #puts $portname
            set length [llength $portname]
            set result ""
            for {set i 0} {$i < $length} {} {
                set basepointer [lindex $portname $i]
                #puts $basepointer
                set j [expr $i + 1]
                set firstpointer [lindex $portname $j]
                while {$firstpointer == [expr $basepointer + $j - $i]} {
                    incr j
                    set firstpointer [lindex $portname $j]
                }
                if { $j != [expr $i + 1] } {
                    lappend result "$basepointer-[lindex $portname [expr $j - 1]]"
                } else {
                    lappend result $basepointer
                }
                set i $j
            }       
            return [append firststring [join $result \;]]
        }
    } else {
        if [info exists Combination] {
            #only for less ports combination
            set comportnum [llength $Combination]
            set portname ""
            set firststring Ethernet
            for {set i 0} {$i < $comportnum} {incr i} {
                set res2 [regexp -nocase "Ethernet\(\[0-9\]+\)/\(\[0-9\]+\)/\(\[0-9\]+\)" [lindex $Combination $i] match chas card port]
                set res1 [regexp -nocase "Ethernet\(\[0-9\]+\)/\(\[0-9\]+\)" [lindex $Combination $i] match card1 port1]
                if { $res2 == 1 } {
                	set firststring Ethernet$chas/$card/
                    lappend portname $port  
                } elseif { $res1 == 1 } {
                	#fix by liangdong 对于机架式交换机板卡数目不定的情况，如果端口数小于等于10，则返回结果为简单排列方式，如Ethernet5/1;5/2;6/1;6/4;
                	#DCRS-7604(config-if-port-range)#interface Ethernet2/1;2/2;2/3;2/4;2/5;2/6;2/7;2/8;2/9;2/10;2/11;2/12;2/13
					#The length of the interface name is 63,it should be less than 60!
                	if { $comportnum <= 10 } {
                		if { $i == [expr $comportnum - 1] } {
                			append firststring "$card1/$port1"
                			return $firststring
                		} else {
                			append firststring "$card1/$port1;"
                		}
                	} else {
	                    set firststring Ethernet$card1/
    	                lappend portname $port1 
    	            }
                } else {
                    puts "the except portname may be unnormal portname!"
                    return 0
                }
            }
            set length [llength $portname]
            set result ""
            for {set i 0} {$i < $length} {} {
                set basepointer [lindex $portname $i]
                #puts $basepointer
                set j [expr $i + 1]
                set firstpointer [lindex $portname $j]
                while {$firstpointer == [expr $basepointer + $j - $i]} {
                    incr j
                    set firstpointer [lindex $portname $j]
                }
                if { $j != [expr $i + 1] } {
                    lappend result "$basepointer-[lindex $portname [expr $j - 1]]"
                } else {
                    lappend result $basepointer
                }
                set i $j
            }       
            return [append firststring [join $result \;]]
        }
    }
}            

#ResetSlot s1 3 1  重启设备s1上的slot 3 1次（本次等待180S）
#ResetSlot s1 3 5  重启设备s1上的slot 3 5次（只有最后依次等待180S,其他都随机选择时间重启）
proc ResetSlot { sut slotnum {times 1} {timer 180000}} {
    EnterEnableMode $sut
    for {set i 1} {$i <= $times} {incr i} {
        receiver $sut "reset slot $slotnum"
        if {$i == $times} {
            IdleAfter $timer
        } else {
            IdleAfter [Random 1 $timer]
        }
    }
}

#GetSlotnum Ethernet3/1  获得端口所在板卡的slot编号
proc GetSlotnum { portname } {
    set res [regexp -nocase {Ethernet(.*)/([0-9]+)} $portname match card port]
    if { $res == 1 } {
        return $card
    } else {
        PrintRes Print "portname $portname may be not currect!"
        return 0
    }
}

proc GetPortnum { portname } {
    set res [regexp -nocase "Ethernet\(\[0-9\]+\)/\(\[0-9\]+\)" $portname match card port]
    if { $res == 1 } {
        return $port
    } else {
        PrintRes Print "portname $portname may be not currect!"
        return 0
    }
}
proc GetSlotPortnum { portname } {
	set res [regexp -nocase "Ethernet\(.*\)" $portname match cardport]
    if { $res == 1 } {
        return $cardport
    } else {
        PrintRes Print "portname $portname may be not currect!"
        return 0
    }
}

#GetSouceModuleID_PortID MRS_7600_48GT Ethernet6/4
proc GetSouceModuleID_PortID { chassisordevtype sourceport } {
	regexp {([0-9]+)/([0-9]+)$} $sourceport match slotnum devport    ;#devport为Ethernet6/1的1，即面板上的端口编号
	if {![info exists devport] || ![info exists slotnum]} {
		return 0
	}
	set pnunit 0   ;#pnunit为芯片编号单芯片一般为0，双芯片不同板卡编号方式不同
	#g_nBcm56624PhyPortMap列表为2XFP24GB12GT/24GB12GT板卡逻辑端口号和物理端口号的对应关系
	set g_nBcm56624PhyPortMap {0 \
	    2  3  4  5  6    7 18 19  8  9 \
	   10 11 12 13 20   21 14 15 16 17 \
	   22 23 24 25 37   38 39 40 26 32 \
	   33 34 41 42 48   49 28 29}
	switch -exact $chassisordevtype {
		MRS_7600_4XFP -
	    MRS_6800_4XFP {
	   		#phyport为在交换机内部对应的物理端口号
			set phyport [expr 26 - $devport]  
			set modid [expr ($slotnum - 1) * 3 + $pnunit + 1]
		}
		MRS_7600_48GT -
	 	MRS_6800_48GT {
			if { $devport >= 25 && $devport <= 48 } {
				set devport [expr $devport - 24]
			} else {
				#48GT与44GT是相反的，unit 0的端口在后面
				set pnunit 1        
			}
			set phyport [expr 4 * (($devport - 1) / 4) + (3 - ($devport - 1) % 4)]
			set modid [expr ($slotnum - 1) * 3 + $pnunit + 2]
		}
		MRS_7604_M44GT -
		MRS_6804_M44GT -
		MRS_9800_24GT {
			if { $devport >= 25 && $devport <= 48 } {
				set devport [expr $devport - 24]
				set pnunit 1
			}
			set phyport [expr 4 * (($devport - 1) / 4) + (3 - ($devport - 1) % 4)]
			set modid [expr ($slotnum - 1) * 3 + $pnunit + 1]
		}
		MRS_7604_M1XFP12GX12GB -
		MRS_6804_M1XFP12GX12GB -
		MRS_7600_12GX12GB -
		MRS_6800_12GX12GB -
		MRS_7600_2XFP12GX12GB -
		MRS_6800_2XFP12GX12GB {
			if { $devport < 13 } {
				set phyport [expr 4 * (($devport - 1) / 4) + (3 - ($devport - 1) % 4)]
			} else {
				set phyport [expr $devport - 1]
			}
			set modid [expr ($slotnum - 1) * 3 + $pnunit + 1]
		}
		MRS_7600_2XFP24GB12GT -
		MRS_6800_2XFP24GB12GT -
		MRS_7600_24GB12GT -
		MRS_6800_24GB12GT {
			if { $devport <= 38 } {
				set phyport [lindex g_nBcm56624PhyPortMap $devport]
			}
			set modid [expr ($slotnum - 1) * 3 + $pnunit + 1]
		}
		DCRS_5950_28T -
		DCRS_5950_28T_L {
			if { $devport >= 25 } {
				set phyport [expr $devport - 1]
			} elseif { [expr $devport % 2] == 0 && $devport < 25 } {
				set phyport [expr $devport - 2]
			} else {
				set phyport $devport
			}
			set modid [expr ($slotnum - 1) * 3 + $pnunit + 1]
		}
		DCRS_5950_52T -
		DCRS_5950_52T_L {
			#may be bug
			if { $devport >= 25 && $devport <= 48 } {
				set devport [expr $devport - 24]
				set pnunit 1
			} elseif { $devport == 49 || $devport == 50 } {
				set phyport [expr $devport - 23]
				set pnunit 1
			} elseif { $devport == 51 || $devport == 52 } {
				set phyport [expr $devport - 25]
			}
			if { [expr $devport % 2] == 0 && $devport < 25 } {
				set phyport [expr $devport - 2]
			} else {
				set phyport $devport
			}
			set modid [expr ($slotnum - 1) * 3 + $pnunit + 1]
		}
		DCS_4500_26T -
		DCS_4500_26T_POE {
			if { $devport == 25 || $devport == 26 } {
				set phyport [expr $devport - 21]
			} else {
				set phyport [expr $devport + 5]
			}
			set modid [expr ($slotnum - 1) * 3 + $pnunit + 1]
		}
		DCS_4500_50T {
			if { $devport == 49 || $devport == 50 } {
				set phyport [expr $devport - 45]
			} else {
				set phyport [expr $devport + 5]
			}
			set modid [expr ($slotnum - 1) * 3 + $pnunit + 1]
		}
		default {
			#alarddin/apollo等老卡，如12GT/12GB/4GX24GX等
			set phyport [expr $devport - 1]
			set modid [expr ($slotnum - 1) * 3 + 1]
		}
	}
	return [list $modid $phyport]
}

#ChooseOutPortInPortchannel {SrcMac 00-00-00-00-00-01 Vlan 10 EthernetType ethernetII} src-mac 4 MRS_7600_48GT Ethernet6/4
#ChooseOutPortInPortchannel {DstMac 00-00-00-00-00-01 Vlan 10 EthernetType ethernetII} dst-mac 4 MRS_7600_48GT Ethernet6/4
#ChooseOutPortInPortchannel {SrcMac 00-00-00-00-00-01 DstMac 00-00-00-00-00-02 Vlan 10 EthernetType ethernetII} src-dst-mac 4 MRS_7600_48GT Ethernet6/4
#ChooseOutPortInPortchannel {SrcIp 10.1.1.1 SrcTcporUdpPort 0} src-ip 4 MRS_7600_48GT Ethernet6/4
#ChooseOutPortInPortchannel {DstIp 10.1.1.2 DstTcporUdpPort 0} dst-ip 4 MRS_7600_48GT Ethernet6/4
#ChooseOutPortInPortchannel {SrcIp 10.1.1.1 DstIp 10.1.1.2 SrcTcporUdpPort 0 DstTcporUdpPort 0} src-dst-ip 4 MRS_7600_48GT Ethernet6/4
#ChooseOutPortInPortchannel {SrcIpv6 2000::1 SrcTcporUdpPort 0} src-ip 4 MRS_7600_48GT Ethernet6/4
#ChooseOutPortInPortchannel {DstIpv6 2000::2 DstTcporUdpPort 0} dst-ip 4 MRS_7600_48GT Ethernet6/4
#ChooseOutPortInPortchannel {SrcIpv6 2000::1 DstIpv6 2000::2 SrcTcporUdpPort 0 DstTcporUdpPort 0} src-dst-ip 4 MRS_7600_48GT Ethernet6/4
proc ChooseOutPortInPortchannel { stream loadbalance portnum chassisordevtype sourceport } {
	if {[lsearch $stream SrcMac] != -1} {
		set srcmac [split [lindex $stream [expr [lsearch $stream SrcMac] + 1]] -]
	}
	if {[lsearch $stream DstMac] != -1} {
		set dstmac [split [lindex $stream [expr [lsearch $stream DstMac] + 1]] -]
	}
	if {[lsearch $stream Vlan] != -1} {
		set vlan [lindex $stream [expr [lsearch $stream Vlan] + 1]]
	}
	if {[lsearch $stream EthernetType] != -1} {
		switch -exact [lindex $stream [expr [lsearch $stream EthernetType] + 1]] {
			ethernetII {
				set ethernettype ffff
			}
			ipv4 {
				set ethernettype 0800
			}
			ipv6 {
				set ethernettype 86dd
			}
			default {
				set ethernettype [lindex $stream [expr [lsearch $stream EthernetType] + 1]]
			}
		}
	}
	if {[lsearch $stream SrcIp] != -1} {
		set srcip [split [lindex $stream [expr [lsearch $stream SrcIp] + 1]] .]
	}
	if {[lsearch $stream DstIp] != -1} {
		set dstip [split [lindex $stream [expr [lsearch $stream DstIp] + 1]] .]
	}
	if {[lsearch $stream SrcTcporUdpPort] != -1} {
		set srctcporudpport [lindex $stream [expr [lsearch $stream SrcTcporUdpPort] + 1]]
	}
	if {[lsearch $stream DstTcporUdpPort] != -1} {
		set dsttcporudpport [lindex $stream [expr [lsearch $stream DstTcporUdpPort] + 1]]
	}
	if {[lsearch $stream SrcIpv6] != -1} {
		set srcipv6 [split [FormatIpv6 [lindex $stream [expr [lsearch $stream SrcIpv6] + 1]]] :]
	}
	if {[lsearch $stream DstIpv6] != -1} {
		set dstipv6 [split [FormatIpv6 [lindex $stream [expr [lsearch $stream DstIpv6] + 1]]] :]
	}
	set modid [lindex [GetSouceModuleID_PortID $chassisordevtype $sourceport] 0]
	set portid [lindex [GetSouceModuleID_PortID $chassisordevtype $sourceport] 1]
	
	switch -exact $loadbalance {
		src-mac {
			set index [expr ([lindex $srcmac 0] & 7) ^ ([lindex $srcmac 1] & 7) ^ ([lindex $srcmac 2] & 7) ^ \
			                ([lindex $srcmac 3] & 7) ^ ([lindex $srcmac 4] & 7) ^ ([lindex $srcmac 5] & 7) ^ \
			                ($vlan >> 8 & 7) ^ ($vlan & 7) ^ (0x$ethernettype >> 8 & 7) ^ (0x$ethernettype & 7) ^ \
			                ($modid & 7) ^ ($portid & 7)]
		}
		dst-mac {
			set index [expr ([lindex $dstmac 0] & 7) ^ ([lindex $dstmac 1] & 7) ^ ([lindex $dstmac 2] & 7) ^ \
			                ([lindex $dstmac 3] & 7) ^ ([lindex $dstmac 4] & 7) ^ ([lindex $dstmac 5] & 7) ^ \
			                ($vlan >> 8 & 7) ^ ($vlan & 7) ^ (0x$ethernettype >> 8 & 7) ^ (0x$ethernettype & 7) ^ \
			                ($modid & 7) ^ ($portid & 7)]
		}
		src-dst-mac {
			set index [expr ([lindex $srcmac 0] & 7) ^ ([lindex $srcmac 1] & 7) ^ ([lindex $srcmac 2] & 7) ^ \
			                ([lindex $srcmac 3] & 7) ^ ([lindex $srcmac 4] & 7) ^ ([lindex $srcmac 5] & 7) ^ \
			                ([lindex $dstmac 0] & 7) ^ ([lindex $dstmac 1] & 7) ^ ([lindex $dstmac 2] & 7) ^ \
			                ([lindex $dstmac 3] & 7) ^ ([lindex $dstmac 4] & 7) ^ ([lindex $dstmac 5] & 7) ^ \
			                ($vlan >> 8 & 7) ^ ($vlan & 7) ^ (0x$ethernettype >> 8 & 7) ^ (0x$ethernettype & 7) ^ \
			                ($modid & 7) ^ ($portid & 7)]
		}
		src-ip {
			if [info exists srcip] {
				set index [expr ([lindex $srcip 0] & 7) ^ ([lindex $srcip 1] & 7) ^ ([lindex $srcip 2] & 7) ^ ([lindex $srcip 3] & 7) ^ \
				                ($srctcporudpport >> 8 & 7) ^ ($srctcporudpport & 7)]
			} else {
				set index [expr ([lindex $srcipv6 0] >> 8 & 7) ^ ([lindex $srcipv6 0] & 7) ^ \
				                ([lindex $srcipv6 1] >> 8 & 7) ^ ([lindex $srcipv6 1] & 7) ^ \
				                ([lindex $srcipv6 2] >> 8 & 7) ^ ([lindex $srcipv6 2] & 7) ^ \
				                ([lindex $srcipv6 3] >> 8 & 7) ^ ([lindex $srcipv6 3] & 7) ^ \
				                ([lindex $srcipv6 4] >> 8 & 7) ^ ([lindex $srcipv6 4] & 7) ^ \
				                ([lindex $srcipv6 5] >> 8 & 7) ^ ([lindex $srcipv6 5] & 7) ^ \
				                ([lindex $srcipv6 6] >> 8 & 7) ^ ([lindex $srcipv6 6] & 7) ^ \
				                ([lindex $srcipv6 7] >> 8 & 7) ^ ([lindex $srcipv6 7] & 7) ^ \
			                    ($srctcporudpport >> 8 & 7) ^ ($srctcporudpport & 7)]
			}
		}
		dst-ip {
			if [info exists dstip] {
				set index [expr ([lindex $dstip 0] & 7) ^ ([lindex $dstip 1] & 7) ^ ([lindex $dstip 2] & 7) ^ ([lindex $dstip 3] & 7) ^ \
				                ($dsttcporudpport >> 8 & 7) ^ ($dsttcporudpport & 7)]
			} else {
				set index [expr ([lindex $dstipv6 0] >> 8 & 7) ^ ([lindex $dstipv6 0] & 7) ^ \
				                ([lindex $dstipv6 1] >> 8 & 7) ^ ([lindex $dstipv6 1] & 7) ^ \
				                ([lindex $dstipv6 2] >> 8 & 7) ^ ([lindex $dstipv6 2] & 7) ^ \
				                ([lindex $dstipv6 3] >> 8 & 7) ^ ([lindex $dstipv6 3] & 7) ^ \
				                ([lindex $dstipv6 4] >> 8 & 7) ^ ([lindex $dstipv6 4] & 7) ^ \
				                ([lindex $dstipv6 5] >> 8 & 7) ^ ([lindex $dstipv6 5] & 7) ^ \
				                ([lindex $dstipv6 6] >> 8 & 7) ^ ([lindex $dstipv6 6] & 7) ^ \
				                ([lindex $dstipv6 7] >> 8 & 7) ^ ([lindex $dstipv6 7] & 7) ^ \
			                    ($dsttcporudpport >> 8 & 7) ^ ($dsttcporudpport & 7)]
			}
		}
		src-dst-ip {
			if { [info exists srcip] && [info exists dstip] } {
				set index [expr ([lindex $srcip 0] & 7) ^ ([lindex $srcip 1] & 7) ^ ([lindex $srcip 2] & 7) ^ ([lindex $srcip 3] & 7) ^ \
				                ([lindex $dstip 0] & 7) ^ ([lindex $dstip 1] & 7) ^ ([lindex $dstip 2] & 7) ^ ([lindex $dstip 3] & 7) ^ \
				                ($srctcporudpport >> 8 & 7) ^ ($srctcporudpport & 7) ^ ($dsttcporudpport >> 8 & 7) ^ ($dsttcporudpport & 7)]
			} else {
				set index [expr ([lindex $srcipv6 0] >> 8 & 7) ^ ([lindex $srcipv6 0] & 7) ^ \
				                ([lindex $srcipv6 1] >> 8 & 7) ^ ([lindex $srcipv6 1] & 7) ^ \
				                ([lindex $srcipv6 2] >> 8 & 7) ^ ([lindex $srcipv6 2] & 7) ^ \
				                ([lindex $srcipv6 3] >> 8 & 7) ^ ([lindex $srcipv6 3] & 7) ^ \
				                ([lindex $srcipv6 4] >> 8 & 7) ^ ([lindex $srcipv6 4] & 7) ^ \
				                ([lindex $srcipv6 5] >> 8 & 7) ^ ([lindex $srcipv6 5] & 7) ^ \
				                ([lindex $srcipv6 6] >> 8 & 7) ^ ([lindex $srcipv6 6] & 7) ^ \
				                ([lindex $srcipv6 7] >> 8 & 7) ^ ([lindex $srcipv6 7] & 7) ^ \
			                    ([lindex $dstipv6 0] >> 8 & 7) ^ ([lindex $dstipv6 0] & 7) ^ \
				                ([lindex $dstipv6 1] >> 8 & 7) ^ ([lindex $dstipv6 1] & 7) ^ \
				                ([lindex $dstipv6 2] >> 8 & 7) ^ ([lindex $dstipv6 2] & 7) ^ \
				                ([lindex $dstipv6 3] >> 8 & 7) ^ ([lindex $dstipv6 3] & 7) ^ \
				                ([lindex $dstipv6 4] >> 8 & 7) ^ ([lindex $dstipv6 4] & 7) ^ \
				                ([lindex $dstipv6 5] >> 8 & 7) ^ ([lindex $dstipv6 5] & 7) ^ \
				                ([lindex $dstipv6 6] >> 8 & 7) ^ ([lindex $dstipv6 6] & 7) ^ \
				                ([lindex $dstipv6 7] >> 8 & 7) ^ ([lindex $dstipv6 7] & 7) ^ \
				                ($srctcporudpport >> 8 & 7) ^ ($srctcporudpport & 7) ^ ($dsttcporudpport >> 8 & 7) ^ ($dsttcporudpport & 7)]
			}
		}
		default {
			return 0
		}
	}
	return [expr ( $index % $portnum ) + 1]
}

#Functional Code


#--------------------------------------------------------------------


######################################################################
#
# ShowVlanId:  查找指定vlan的相关信息
#
# args:
#     sut:    待测设备
#     vid:    指定vlan id
#     args:  设定需要关注的参数的键值对
#     name:   vlan名称
#     type:   vlan类型
#     media:  vlan媒介
#     port:   加入vlan的端口
#
# return: 
#     1,  查找成功
#     0,  查找失败
#
# addition:
# 
# examples:
#     ShowVlanId s1 10 name aaa type static media enet port ethernet1/10
#           
######################################################################
#今后使用ShowVlanId，一律用CheckPortAccessVlan代替
proc ShowVlanId { sut vid args } {
	array set vlan $args
	EnterEnableMode $sut 
	 
	set RecvBuf [receiver $sut "show vlan id $vid" 3]
	set regexpstr "(.*?)"
	
	#name
	if {[info exist vlan(name)]} {
		append regexpstr "(\[^\\n\])+$vlan(name)"
	}	
	#type
	if {[info exist vlan(type)]} {
		append regexpstr "(\[^\\n\])+$vlan(type)"
	}	
	#media
	if {[info exist vlan(media)]} {
		append regexpstr "(\[^\\n\])+$vlan(media)"
	}
	if {[info exist vlan(portmore)]} {
	    append regexpstr "(.*?)$vlan(port)(.*?)$vlan(portmore)"
	} else {
	    if {[info exist vlan(port)]} {
            append regexpstr "(.*?)$vlan(port)"
        }
	}	
		
	#PrintRes Print "regexpstr = $regexpstr, RecvBuf = $RecvBuf"
	if {[regexp -nocase $regexpstr $RecvBuf]} {
		return 1
	} else {
		PrintRes Print "regexpstr = $regexpstr"
		PrintRes Print "RecvBuf = $RecvBuf"
		return 0
	}
}


#GetInterfaceDuplexSpeed s1 ethernet1/1
#GetInterfaceDuplexSpeed s1 portchannel1
#GetInterfaceDuplexSpeed s1 "portchannel 1"
proc GetInterfaceDuplexSpeed { sut port } {
	EnterEnableMode $sut
	set RecvBuf [receiver $sut "show interface $port" 2]
	#Auto-duplex: Negotiation full-duplex, Auto-speed: Negotiation 100M bits
	#Force half-duplex, Force 100M
	set res1 [regexp -nocase -line "Auto-duplex: Negotiation (.*?), Auto-speed: Negotiation (.*?) bits" $RecvBuf duplexspeed1 duplex1 speed1]
	set res2 [regexp -nocase -line "Force (.*), Force (.*)" $RecvBuf duplexspeed2 duplex2 speed2]
	if { $res1 == 1 } {
		PrintRes Print "get interface $port duplex and speed is : $duplexspeed1."
		return [list $duplex1 $speed1]
	}
	if { $res2 == 1 } {
		PrintRes Print "get interface $port duplex and speed is : $duplexspeed2."
		return [list $duplex2 $speed2]
	}
}

#########################################################################
#
# TimeToSecond : 把小时：分钟：秒格式的数据转换为秒数
#
# args:
# 
#
# return:
#     
# 
# addition:
#
# examples: 
#     TimeToSecond "00:02:23"
#
######################################################################### 
proc TimeToSecond { time } {
	set res1 [clock scan "00:00:00"]
	set res2 [clock scan $time]
	set res [expr {$res2 - $res1}]
	return $res
}

proc GetMaskValue { mask } {
    set mask [split $mask .]
    set value 0
    for {set i 0} {$i < 4} {incr i} {
        set result [expr [lindex $mask $i] & 255]
        if { $result < 128 } {
            break
        }
        if { $result < 192 } {
            incr value 1
            continue
        }
        if { $result < 224 } {
            incr value 2
            continue
        }
        if { $result < 240 } {
            incr value 3
            continue
        }
        if { $result < 248 } {
            incr value 4
            continue
        }
        if { $result < 252 } {
            incr value 5
            continue
        }
        if { $result < 254 } {
            incr value 6
            continue
        }
        if { $result < 255 } {
            incr value 7
            continue
        } else {
            incr value 8
            continue
        }
    }
     return $value
}



##GetSouceModuleID_PortID MRS_7600_48GT Ethernet6/4
#proc GetSouceModuleID_PortID { chassisordevtype sourceport } {
#	regexp {([0-9]+)/([0-9]+)$} $sourceport match slotnum devport    ;#devport为Ethernet6/1的1，即面板上的端口编号
#	if {![info exists devport] || ![info exists slotnum]} {
#		return 0
#	}
#	set pnunit 0   ;#pnunit为芯片编号单芯片一般为0，双芯片不同板卡编号方式不同
#	#g_nBcm56624PhyPortMap列表为2XFP24GB12GT/24GB12GT板卡逻辑端口号和物理端口号的对应关系
#	set g_nBcm56624PhyPortMap {0 \
#	    2  3  4  5  6    7 18 19  8  9 \
#	   10 11 12 13 20   21 14 15 16 17 \
#	   22 23 24 25 37   38 39 40 26 32 \
#	   33 34 41 42 48   49 28 29}
#	switch -exact $chassisordevtype {
#		MRS_7600_4XFP -
#	    MRS_6800_4XFP {
#	   		#phyport为在交换机内部对应的物理端口号
#			set phyport [expr 26 - $devport]  
#			set modid [expr ($slotnum - 1) * 3 + $pnunit + 1]
#			#break
#		}
#		MRS_7600_48GT -
#	 	MRS_6800_48GT {
#			if { $devport >= 25 && $devport <= 48 } {
#				set devport [expr $devport - 24]
#			} else {
#				#48GT与44GT是相反的，unit 0的端口在后面
#				set pnunit 1        
#			}
#			set phyport [expr 4 * (($devport - 1) / 4) + (3 - ($devport - 1) % 4)]
#			set modid [expr ($slotnum - 1) * 3 + $pnunit + 2]
#			#break
#		}
#		MRS_7604_M44GT -
#		MRS_6804_M44GT -
#		MRS_9800_24GT {
#			if { $devport >= 25 && $devport <= 48 } {
#				set devport [expr $devport - 24]
#				set pnunit 1
#			}
#			set phyport [expr 4 * (($devport - 1) / 4) + (3 - ($devport - 1) % 4)]
#			set modid [expr ($slotnum - 1) * 3 + $pnunit + 1]
#			#break
#		}
#		MRS_7604_M1XFP12GX12GB -
#		MRS_6804_M1XFP12GX12GB -
#		MRS_7600_12GX12GB -
#		MRS_6800_12GX12GB -
#		MRS_7600_2XFP12GX12GB -
#		MRS_6800_2XFP12GX12GB {
#			if { $devport < 13 } {
#				set phyport [expr 4 * (($devport - 1) / 4) + (3 - ($devport - 1) % 4)]
#			} else {
#				set phyport [expr $devport - 1]
#			}
#			set modid [expr ($slotnum - 1) * 3 + $pnunit + 1]
#			#break
#		}
#		MRS_7600_2XFP24GB12GT -
#		MRS_6800_2XFP24GB12GT -
#		MRS_7600_24GB12GT -
#		MRS_6800_24GB12GT {
#			if { $devport <= 38 } {
#				set phyport [lindex g_nBcm56624PhyPortMap $devport]
#			}
#			set modid [expr ($slotnum - 1) * 3 + $pnunit + 1]
#			#break
#		}
#		DCRS_5950_28T -
#		DCRS_5950_28T_L {
#			if { $devport >= 25 } {
#				set phyport [expr $devport - 1]
#			} elseif { [expr $devport % 2] == 0 && $devport < 25 } {
#				set phyport [expr $devport - 2]
#			} else {
#				set phyport $devport
#			}
#			set modid [expr ($slotnum - 1) * 3 + $pnunit + 1]
#			#break
#		}
#		DCRS_5950_52T -
#		DCRS_5950_52T_L {
#			#puts 5950
#			#may be bug
#			if { $devport >= 25 && $devport <= 48 } {
#				set devport [expr $devport - 24]
#				set pnunit 1
#			} elseif { $devport == 49 || $devport == 50 } {
#				set phyport [expr $devport - 23]
#				set pnunit 1
#			} elseif { $devport == 51 || $devport == 52 } {
#				set phyport [expr $devport - 25]
#			}
#			#puts 222
#			if { [expr $devport % 2] == 0 && $devport < 25 } {
#				set phyport [expr $devport - 2]
#			} else {
#				set phyport $devport
#			}
#			set modid [expr ($slotnum - 1) * 3 + $pnunit + 1]
#			#puts 3333
#			#break
#		}
#		DCS_4500_26T -
#		DCS_4500_26T_POE {
#			if { $devport == 25 || $devport == 26 } {
#				set phyport [expr $devport - 21]
#			} else {
#				set phyport [expr $devport + 5]
#			}
#			set modid [expr ($slotnum - 1) * 3 + $pnunit + 1]
#			#break
#		}
#		DCS_4500_50T {
#			if { $devport == 49 || $devport == 50 } {
#				set phyport [expr $devport - 45]
#			} else {
#				set phyport [expr $devport + 5]
#			}
#			set modid [expr ($slotnum - 1) * 3 + $pnunit + 1]
#			#break
#		}
#		default {
#			#alarddin/apollo等老卡，如12GT/12GB/4GX24GX等
#			set phyport [expr $devport - 1]
#			set modid [expr ($slotnum - 1) * 3 + 1]
#		}
#	}
#	#puts 4444
#	return [list $modid $phyport]
#}
#**************************************************************#
#                                                              #
#                       结果检查函数                           #
#                                                              #
#**************************************************************#

#########################################################################################
# DisableWatchdog : 关闭看门狗
#
# args :     sut : 被测设备
#########################################################################################
proc DisableWatchdog { sut } {
    EnterConfigMode $sut
    receiver $sut "watchdog disable"
}      


proc FindFile { startDir namePat } {
    global str
    global title
    global path
    set pwd [pwd]
    if [catch {cd $startDir} err] {
        puts stderr $err
        return
    }
    foreach match [glob -nocomplain -- $namePat] {
        if { $match == "pkgIndex.tcl" } {
            continue
        } else {
            append str $title "[string range $startDir [expr [string length $path] + 1] end] $match\]\]\\n\n"
        }
    }
    foreach file [glob -nocomplain *] {
        if [file isdirectory $file] {
            FindFile [file join $startDir $file] $namePat
        }
    }
    cd $pwd
}     
proc MakePkgIndex { startDir namePat } {
    global str
    global title
    global path
    set str "package ifneeded DcnTestP 1.1 \""
    set title "\[list source \[file join \$dir "
    set path $startDir
    if [catch {open [file join $path pkgIndex.tcl] w} fileId] {
        puts stderr "Cannot open [file join $path pkgIndex.tcl]"
    } else {
        puts $fileId "# Tcl package index file, version 1.1"
        puts $fileId "# This file is generated by the \"pkg_mkIndex\" command"
        puts $fileId "# and sourced either when an application starts up or"
        puts $fileId "# by a \"package unknown\" script.  It invokes the"
        puts $fileId "# \"package ifneeded\" command to set up package-related"
        puts $fileId "# information so that packages will be loaded automatically"
        puts $fileId "# in response to \"package require\" commands.  When this"
        puts $fileId "# script is sourced, the variable \$dir must contain the"
        puts $fileId "# full path name of this file's directory."
        puts $fileId ""
        FindFile $startDir $namePat
        append str \"
        puts $fileId $str
        close $fileId
    }
}    


##############################################################################
#
# StopDebugAll: 关闭debug
#
# args:
#     sut:     被测设备
#
# return:
# 
# addition:
#     
#
# examples:
#      StopDebugAll $switch1
###############################################################################
proc StopDebugAll {sut} {
    receiver $sut "\x0f"
}


proc FormatArea { num } {
	return "[expr {$num / 16777216}].[expr {($num % 16777216) / 65536}].[expr {($num % 16777216 % 65536) / 256}].[expr {$num % 16777216 % 65536 % 256}]"
}

proc StartDebug { sut } {
	set ::autotest::VAR(debug.$sut) 1
}


#########################################################################
#CheckShowList用法举例：
#CheckShowList用法举例：
#CheckShowList s1 "show mac-address-table" StartLine 3 ExpectList {{1 00-00-0e-00-04-00 DYNAMIC Hardware Ethernet1/1} {1 00-00-0e-00-04-01 DYNAMIC Hardware Ethernet1/1} {1 00-00-0e-00-04-02 DYNAMIC Hardware Ethernet1/1}} NonExpectList {{1 00-00-0e-00-04-00 DYNAMIC Hardware Ethernet1/2} {1 00-01-0e-00-04-00 DYNAMIC Hardware Ethernet1/1}} ItemListCount {{1 DYNAMIC Ethernet1/1} {1 System CPU}}
#> the expct item "1 00-00-0e-00-04-00 DYNAMIC Hardware Ethernet1/1" is exist
#> the expct item "1 00-00-0e-00-04-01 DYNAMIC Hardware Ethernet1/1" is exist
#> the expct item "1 00-00-0e-00-04-02 DYNAMIC Hardware Ethernet1/1" is exist
#> the none expct item "1 00-00-0e-00-04-00 DYNAMIC Hardware Ethernet1/2" is not exist
#> the none expct item "1 00-01-0e-00-04-00 DYNAMIC Hardware Ethernet1/1" is not exist
#> the count of item "1 DYNAMIC Ethernet1/1" is 20
#> the count of item "1 System CPU" is 1
#返回列表 ItemListCount {20 1} NonExpectList 1 ExpectList 1 Result 1
#
#参数：CheckShowList sut cmd args
#sut：被测设备
#cmd：一般为show命令，表项特征类似show mac-address-table， show arp ，show ip route等在一个换行内，且各个类型值用空格分开，还用一点就是该函数还支持一行内前段连续补齐表项，类似这样的表项 “。。。 10.1.1.1 。。。 ethernet1/1”不支持补齐，。。。表示空，另外如有空行函数会自行删除
#args：目前支持StratLine：表项开始前需删除的行数，如StratLine 3
#DCRS-7608#show mac-address-table
#Read mac address table....
#Vlan Mac Address                 Type    Creator   Ports
#---- --------------------------- ------- -------------------------------------
#1    00-00-11-22-33-45           DYNAMIC Hardware Ethernet2/9
#1    00-03-0f-00-00-02           STATIC  System   CPU
#show的内容需删除3行是表项开始的行
#
#EndLine：表项结束后删除的行数，如EndLine 1
#DCRS-7608#show ip route 
#Codes: K - kernel, C - connected, S - static, R - RIP, B - BGP
#       O - OSPF, IA - OSPF inter area
#       N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
#       E1 - OSPF external type 1, E2 - OSPF external type 2
#       i - IS-IS, L1 - IS-IS level-1, L2 - IS-IS level-2, ia - IS-IS inter area
#       * - candidate default
#
#C       10.1.1.0/24 is directly connected, Vlan1  tag:0
#C       127.0.0.0/8 is directly connected, Loopback  tag:0
#Total routes are : 2 item(s)
#show的内容需删除最后1行，即最后的“Total routes are : 2 item(s)”不在扫描的表项内。
#
#ExpectLine：列表类型，一条表项各个类型值用空格分隔，如{{1 00-00-11-22-33-45 DYNAMIC Hardware Ethernet2/9} {1 00-03-0f-00-00-02 STATIC System CPU}}为两条表项，表项类型不用完整填写，可以根据实际情况填写若个类型，但一条表项类型值出现的顺序必须符合实际的顺序。
#
#NonExpectList：即不期望出现的表项，其他与ExpectLine一致
#
#ItemListCount：提供表项特征，表项中的类型值须按实际顺序排列，函数在类型值中间加了“空格.*?”，类型值要完整。如{{1 00-00-0e DYNAMIC Ethernet1/1}}是不可以的。
#
#TrimLeft：删除表项每行开始的字符数，一般下列情况使用：当所有表项的第一列类型值左端还有空格时，可以删除空格。
#
#ItemMatchVariable ：提供一组正则表达式来获取表项某个字段的值，用法：列表含有偶数个元素，第一个元素为正则表达式，第二个为获取字段的个数，如{{(...) (.*?) DYNAMIC Hardware Ethernet1/1} 2 {100 (.*?) (.*?) System CPU} 2}，
#注意：被匹配的表项格式为：将原始数据中多个空格合并为一个，同时对按上一条表项补齐，故正则表达式可以利用空格来协助匹配，如ItemMatchVariable {{(...) (.*?) .* (Ethernet.*?) } 3 }；
#返回列表中增加ItemMatchVariable项，按参数顺序给出匹配的内容；如ItemMatchVariable {{100 00-00-00-00-00-01} {00-03-0f-0f-4e-dc STATIC}}
#
#返回值说明：返回列表，目前包括内容：ItemListCount：列表，按顺序给出符合预期的表项个数；NonExpectList：1或0，表示不期望的表项未出现或出现；ExpectList：1或0，表示期望的表项出现或未出现；Result：1或0；是NonExpectList和ExpectList作与操作的结果，当只有ItemListCount时返回1
#
#当按要求show到的内容为空时，返回ItemListCount {} NonExpectList 0 ExpectList 0 Result 0
#
#在脚本中要用array set将列表转换为数组，然后做检查
#
#说明：CheckShowList函数参数的{}中不支持变量替换，即ExpectList {{1 00-00-0e-00-04-00 DYNAMIC Hardware $s1p1}}错误；需要修改为set matchlist [list [list 1 00-00-0e-00-04-00 DYNAMIC Hardware $s1p1]] 再使用ExpectList $matchlist
#ShowCommandToList为支持函数，返回符合的表项列表。
#########################################################################
proc ShowCommandToList { sut cmd args} {
		EnterEnableMode $sut
    set RecvBuf [receiver $sut "$cmd" 0 PromoteStop true]    
    set RecvBufList [split $RecvBuf "\n"]
    set listnum [expr [llength $RecvBufList] - 1]
    set reslist ""
    set args [join $args]
    set StartLine 0
    set EndLine $listnum
    set TrimLeft -1
    if {[llength $args]} {
  	array set arrArgs $args 	
  	foreach {para value} [array get arrArgs] {	
			switch -exact -- $para {
			    StartLine {
			    	set StartLine $value
			    }
			    EndLine {
			    	set EndLine [expr $listnum - $value]
			    }
			    TrimLeft {
			    	set TrimLeft [expr $value - 1]
			    }
			  }
			}
  	}
  	#若表项开始行大于等于结束行，则无表项，返回空
    if {$StartLine > $EndLine} {
    	return $reslist
    }
    set Currentline $StartLine
    set PreList ""
    set PreListLength 0
    for {set Currentline} {$Currentline < $EndLine} {incr Currentline} {
    	#将交换机输出信息转换为列表
    	set itemlist [lindex $RecvBufList $Currentline]
    	#删除掉表项左边指定的字符
    	if {$TrimLeft >= 0 } {
    		set itemlist [string replace $itemlist 0 $TrimLeft ""]
    	}
    	#将多个空格转换为一个空格
    	regsub -all {\s+} $itemlist " " itemlist
    	#删除掉行尾多余的空格
    	set itemlist [string trimright $itemlist]
    	if {[regexp -line {^$} $itemlist]} {
    		continue
    	}
    	set itemlist [split $itemlist]
    	set itemlistlength [llength $itemlist]
    	if {[lindex $itemlist 0] == ""} {
    		for {set j 0} {$j <= [expr $PreListLength - $itemlistlength]} {incr j} {
    			if {$j == 0} {
    				set itemlist [lreplace $itemlist 0 0 [lrange $PreList 0 0]]
    			} else {
    				set itemlist [linsert $itemlist $j [lrange $PreList $j $j]]
    			}
    		}	
    	} else {
    		set PreList $itemlist
    		set PreListLength [llength $itemlist]
    	}
    	append itemlist " "
			lappend reslist $itemlist
	}
	return $reslist
}

proc CheckShowList {sut cmd args} {
	set ExpectList ""
	set NonExpectList ""
	set ItemListCount ""
	set ItemMatchVariable ""
	if {[llength $args]} {
  	array set arrArgs $args 	
  	foreach {para value} [array get arrArgs] {	
			switch -exact -- $para {
			    ExpectList {
			    	set ExpectList $value
			    }
			    NonExpectList {
			    	set NonExpectList $value
			    }
			    ItemListCount {
			    	set ItemListCount $value
			    }
			    ItemMatchVariable {
			    	set ItemMatchVariable $value
			    }
			  }
			}
  	}
  	
  	set ExpectListLength [llength $ExpectList]
  	set NonExpectListLength [llength $NonExpectList]
  	set ItemListCountLength [llength $ItemListCount]
  	set ItemMatchVariableLength [llength $ItemMatchVariable]
  	if {[expr $ItemMatchVariableLength % 2 ] == 1} {
  		PrintRes Print "ItemMatchVariable should include even para"
  		return -1
  	} 
  	set ExpectMatchList ""
  	set NonExpectMatchList ""
  	set DestList ""
  	array set ResArray {
  		Result 0
  		ExpectList 0
  		NonExpectList 0
  		ItemListCount {}
  		ItemMatchVariable {}
  	}
  	set res 0
  	set expres 1
  	set nonexpres 1

  	
		set DestList [ShowCommandToList $sut $cmd $args]
  	set DestListLength [llength $DestList]
  	
  	if {$ItemListCountLength != 0 } {
  		set DestString [join $DestList "\n"]
  	}  	
  	for {set i 0} {$i < $ExpectListLength} {incr i} {
  		set matchitem [join [lindex $ExpectList $i] " .*?"]
  		append matchitem " "
  		set exprestmp 0
  		for {set j 0} {$j < $DestListLength} {incr j} {
  			if {[regexp -nocase $matchitem [lindex $DestList $j]]} {
  				set exprestmp 1
  				PrintRes Print "the expct item \"[lindex $ExpectList $i]\" is exist"
  				break
  			}
  		}
  		if {$exprestmp == 0} {
  			PrintRes Print "the expct item \"[lindex $ExpectList $i]\" is not exist"
  			set expres 0
  		}
  	}
  	set ResArray(ExpectList) $expres
  	
  	for {set i 0} {$i < $NonExpectListLength} {incr i} {
  		set matchitem [join [lindex $NonExpectList $i] " .*?"]
  		append matchitem " "
  		set nonexprestmp 1
  		for {set j 0} {$j < $DestListLength} {incr j} {
  			if {[regexp -nocase $matchitem [lindex $DestList $j]]} {
  				set nonexprestmp 0
  				set nonexpres 0
  				PrintRes Print "the none expct item \"[lindex $NonExpectList $i]\" is exist"						
  				break
  			}
  		}
  		if {$nonexprestmp == 1} {
  			PrintRes Print "the none expct item \"[lindex $NonExpectList $i]\" is not exist"
  		}
  	}
  	set ResArray(NonExpectList) $nonexpres
  	
  	for {set i 0} {$i < $ItemListCountLength} {incr i} {
  		set matchitem [join [lindex $ItemListCount $i] " .*?"]
  		append matchitem " "
  		set countrestmp [regsub -line -all $matchitem $DestString "" regsubtmp]
  		PrintRes Print "the count of item \"[lindex $ItemListCount $i]\" is $countrestmp"
  		lappend ResArray(ItemListCount) $countrestmp 
  	}
  	
  	for {set i 0} {$i < $ItemMatchVariableLength} {incr i} {
  		set matchrestmp 0
  		set matchitem [lindex $ItemMatchVariable $i]
  		set n $i
  		incr i
  		set matchitemnum [lindex $ItemMatchVariable $i]
  		set matchcommand [list regexp -nocase $matchitem "" match]
  		set variableitem ""
  		set variablecommand [list lappend variableitem]
  		for {set k 1} {$k <= $matchitemnum} {incr k} {
  			set variable[set k] ""
  			lappend matchcommand variable[set k]
  			set variablecommand [concat $variablecommand \$variable[set k]]
  		}
  		
  		for {set j 0} {$j < $DestListLength} {incr j} {
  			set matchcommand [lreplace $matchcommand 3 3 [lindex $DestList $j]]
  			if {[eval $matchcommand]} {
  				eval $variablecommand  
					lappend ResArray(ItemMatchVariable) $variableitem
					set matchrestmp 1
  				PrintRes Print "the match variable \"[lindex $ItemMatchVariable $n]\" is $variableitem"
  				break
  			}
  		}
  		if {$matchrestmp == 0} {
  			lappend ResArray(ItemMatchVariable) ""
  			PrintRes Print "can not match variable \"[lindex $ItemMatchVariable $n]\". "
  		}
  	}
  		  					
  	set res [expr {$expres && $nonexpres}]
  	
  	if {$res == 0} {
  		PrintRes Print "$cmd on $sut:"
  		PrintRes Print "$DestList"
  	} else {
  		set ResArray(Result) $res
  	}
		
		return [array get ResArray]
}


proc ForgetTestModuleNameSpace {namespacelist} {
	if {$namespacelist != ""} {
		foreach namesp $namespacelist {
			namespace forget [set namesp]::*
		}
	}
	return 0
}