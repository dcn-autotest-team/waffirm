set filedir [file dirname [info script]]
lappend auto_path C:/Tcl/lib/tcl8.4
lappend auto_path C:/Tcl/lib
package require IxTclHal
package req IxTclExplorer
package req Scriptgen
source [file join $filedir 02_ixia.tcl]
source [file join $filedir 01_tool.tcl]
#source 02_ixia.tcl
#source 01_tool.tcl
##set filedir [file dirname [info script]]
##source [file join $filedir ixia_vars.tcl]

##source ixia_vars.tcl
##puts $tp1
##puts $portlist1
global longtime


proc InitIxia {host} {
  ixInitialize $host
}

proc print {msg} {
  #after 5000
  return [clock format [clock seconds]]\t$msg
}
proc compute {args} {
  return "expr\($args)=[expr $args]"
}

##proc SaveIxiaPortConfig1 {host chassisId card port filepath} {

##  ixConnectToChassis   $host
##  set portList [list  [list $chassisId $card $port] ]
##  foreach listItem $portList { puts $listItem }
##  ##set fileName "E:/python_ixia/12_1_6.tcl"
##  set fileName $filepath
##  ::scriptGen::generateScript $portList -outPutToFile $::true  -fileOverwrite $::false  -filePerPort $::false  -streamGenOption $::false   -fileName $fileName  -outputOption generateNonDefault
##}

proc SaveIxiaPortConfig {portList filepath {filePerPort false}} {
  ##ixConnectToChassis   $host
  set fileName $filepath
  ::scriptGen::generateScript $portList -outPutToFile $::true  -fileOverwrite $::false  \
  -filePerPort $filePerPort  -streamGenOption $::false   -fileName $fileName  -outputOption generateNonDefault
}

proc LoadIxiaPortConfig {filepath} {
  #puts $filepath
  source $filepath  
}

proc closechannel {} {
  global channel
  close $channel
  global longtime
  set longtime 1
}
proc callback {socketid addr port} {
  #puts $socketid
  fconfigure $socketid -blocking 0 -buffering line;#非阻塞模式 按行flush
  fileevent $socketid readable [list readcallback $socketid]
  #close $socketid
}
proc readcallback {socketid} {
  if {[eof $socketid] || [catch {gets $socketid line} err]} {
    close $socketid
  } else {
    #deal with line; suppose line is tcl scripts eval it and return the results
    #puts line=$line
    if {$line != ""} {
    if {[catch {eval $line} err]} {
      puts $socketid $err
    } else {
      puts $socketid $err
    }
    }
  }
}

 
####initIxia 172.16.1.253
####socket -server callback 9919
##initIxia [lindex $argv 0]
##puts $argv
catch {
  set socketid2 [socket localhost 9927]
  fconfigure $socketid2 -buffering line
  puts $socketid2 "closechannel"
}
IdleAfter 1000
set channel [socket -server callback [lindex $argv 0]]
puts "Server started!"
vwait longtime
puts "Server closed!"

