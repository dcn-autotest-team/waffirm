#-*- coding: UTF-8 -*-#
testName = 'performance'
priority = 10
runtimes = 1
central24G = False  #是否执行集中转发2.4G
central5G = False #是否执行集中转发5G
local24G = True  #是否执行本地转发2.4G
local5G = False #是否执行本地转发5G

# 下列参数用于判断脚本执行顺序，优先级小的先执行，如对执行顺序无特别要求则不需修改
central24G_pri = 3 #集中转发2.4G优先级
central5G_pri = 4 #集中转发5G优先级
local24G_pri = 2 #本地转发2.4G优先级
local5G_pri = 1 #本地转发5G优先级

testlist = []
testlist.append(['performance_3.4.1.py',1])

