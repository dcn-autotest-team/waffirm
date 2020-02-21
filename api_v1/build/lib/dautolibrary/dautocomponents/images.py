#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# *********************************************************************
# images.py - 存放图标
# 
# Author:caisy(caisy@digitalchina.com)
#
# Version 2.0.0
#
# Copyright (c) 2004-9999 Digital China Networks Co. Ltd 
#
# 
# *********************************************************************
# Change log:
#     - 2011.8.31  modified by caisy
#
# *********************************************************************

from wx.lib.embeddedimage import PyEmbeddedImage

__all__ = ['icon', 'autoTest', 'newConn', 'pause', 'ahead', 'stop', 'clear', 'ixos', 'quickConn', 'autoCreate', 'pin',
           'timelog', 'send', 'editScript', 'quickScript', 'debugpoint', 'debugpointon', 'printfront', 'printback',
           'printUI', 'quickShell', 'errorStop', 'errorPass']

newConn = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAVBJ"
    "REFUOI2lkzGKVUEQRc/tfpjINzYV3IfgNkwNnNQ9DBoIgusQXI4oDDKB6UTDF+a9uteg+w1/"
    "ws9vKLqCqlO3qruk1rnkLABffvzO3TEkgE1sykUcHJMqnJAqyubFs5VPH94IQNffb3I4PD+7"
    "8s3PX3z7+FbLcQ3Hu/uzAf/WjBZS4frd67MB7z/fTkAMwMNWBIhDGUywQ9nUlmExDxVevTxQ"
    "rgEYkwM1oYQ0EQVZtCakhlSoh+7Gso14bxOwkxoQCQQ9YIEdeqCpswhKodpQ7PJswYOIBMkT"
    "kASpYEEENNE9/o33FnZnMDScE5AXsdg4Q6VniD0VbOv6qEBAEiSRExCt0YFKaBqKt3Xbn3GQ"
    "Ooyk2coTRYCBLpFZeb+XXQqApnGSuJ/HjelzBrPI8vfPLVdfV1yFy1QVtql1xfbYAdcYZsae"
    "nNREl25juygb+A/CcuXjENevDwAAAABJRU5ErkJggg==")
getnewConnData = newConn.GetData
getnewConnImage = newConn.GetImage
getnewConnBitmap = newConn.GetBitmap

pause = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAIdJ"
    "REFUOI1jZGRiZqAEMFGke1AYwIIu0Lfq238GBgaGu+9eMUzNUGBE5xPlAlt9BobD+07j5OM1"
    "4B3DVwj9/RtWPlEuYGBgYGBAV49dPxYDvkOo999fYecT44Lv3/Hz8Rrw/vtXhnffGBgYvn3D"
    "yifKBe+/f2X4jodP0IDk4ml4+ciAcehnJgDeWkJBLSgqJAAAAABJRU5ErkJggg==")
getpauseData = pause.GetData
getpauseImage = pause.GetImage
getpauseBitmap = pause.GetBitmap

stop = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAM1J"
    "REFUOI3Vkz9OQkEQxn8P7byEN+AE3sfTSGVvKDkFR6FQC8nOVDNfqcUsT0F8kNDINpPZ7Pc3"
    "2WGY3XDJmV2E/hcEtz+Xp1V+AhhRF6rhivHN8+P98CcBwMMc4K7wAsva3YLFcj3toJQL/NbK"
    "gSvwBBOYcppgdyRwgbfAehRvG/iNPyixZ7YE9N2DK3h/DVwfpx2M6t22t0ACtD1mdt+BK7Ds"
    "syur2zeAPKMDV2BtgzdQC9y2WCauMeE0wctyjfciyk3l1hF1gOH6P9MX5gx9PpzI89wAAAAA"
    "SUVORK5CYII=")
getstopData = stop.GetData
getstopImage = stop.GetImage
getstopBitmap = stop.GetBitmap

ahead = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAALhJ"
    "REFUOI3N0yEOwkAQheF/C2eoxeCakGBwPQMKTfDgwCG5ASdAcwNUPQKO0MERkg0NbbJVIIqc"
    "bUtqGDNm35cndowJenSZoFPaB6z26btzg8WuHeIFolHIdNuMqEDuqh1PQuL1uRbRG5TVkicM"
    "BxHx0o+ogHXwcgV5BlcpuN1hPDuoiN7Agf2GraSQJVyOc6M97asNAKTAygOyBDlt1LAXwIF1"
    "zWEvkJdgpTkMNf+gTRjA/Ocx/TIfq3tF6iZAZcIAAAAASUVORK5CYII=")
getcontinueData = ahead.GetData
getcontinueImage = ahead.GetImage
getcontinueBitmap = ahead.GetBitmap

clear = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAQVJ"
    "REFUOI2lkzFLw0AUgL9LnXJzbnZu9/6T/gLd1E3cHJRu0o6u1uIWcLOjCI6FDIL7SbcLuL1A"
    "Bj2HNtHQxEbzuMfdce/7Do57SgU9ukTQiQb2dhVM5ksPYJ3FAOenI1UpUEGvMad3ic/zvMwk"
    "WfnD8b3/WdMaft/Mz8nKj6ffkto3mMyX/mg0KPcigjjBOWE4MLgsK8+2BLWwrNfGaK5mD7xZ"
    "Wy9oAyMZtk7QFo4XT7w83qiK4L8wbP6BCcGJgIDWoLWG9fgVLgU2FcJXAVIiHbEfgd5xcxGq"
    "6IWTy1sPMOz3y0ObWuJ40QhXBEUcHF94dAgCs+uzJg6Aj0+vtgR/jc7d+AW0/LQPFeHeaQAA"
    "AABJRU5ErkJggg==")
getclearData = clear.GetData
getclearImage = clear.GetImage
getclearBitmap = clear.GetBitmap

autoNew = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAVpJ"
    "REFUOI2tkkFLVVEUhb/7vL/CF4KjkMLEsQhiIWWTpirZP/CXOBCcNEinTqzgJRGpTZoWCo79"
    "Dd7nvefsc+7Z+zgILhI+qV5ruM7iY7H2KYreBOOoHPWwe1plFxO1RCon7KxNF3fleqMALiQW"
    "J2G5X3JVu79vMPQB70tElKr6B8BVLez/dFTXjuHQjwQU4444cgOAo0+D/PHD+3xfpmtwcvw1"
    "mxmqStu2iAjOObz3NE1DXdc0TdN57/b2C7i1QYyR5y9W7zzV79pYX+tajb1BufXtTVZT1Awz"
    "5e3KQQHwevAqhxSQEJEgfNn8XgA82Z7JMbSkNoFlekkTT/svefZglVZTR5ZWWOwvsTC1gA+h"
    "86NE5h4+Zv7RLGaZMqmilrCsJNUu6CUwjBV1vMaLdH5qE2qK5Uz+BUgMLg9RM9RuAYJwdPGZ"
    "ECIhxM43zfw4PyPn/zTivR/pT3QDggTUKlAVg08AAAAASUVORK5CYII=")
getautoNewData = autoNew.GetData
getautoNewImage = autoNew.GetImage
getautoNewBitmap = autoNew.GetBitmap

autoTest = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAYhJ"
    "REFUOI2lk7+KU1EQxn/n3Jm7nTYmjQj2WwqpbAQfIJVphPgCFrZun863EAwoaYU8gYUSsBO0"
    "3C4IWqjr7nxjkeR612RB2APDOXPOnPm++VdKbbjOKrM3X/LI4euPJBOQSAkSIoNUohQZgTLJ"
    "CELiRnvOz7PEEnhwfIuPp2d8/6WDKPdunvLh2+3tfoenrx8zf/KSd+8/UU5efc6MJDMhRWYi"
    "aYO6ZaPQ37sQUiAlqcAykrcvHlFKOSi1Vmqte3qtlbsPn2OZomka1uv1JaNDH/r6YDAgFNRN"
    "5jZrsVgwm83+uwK6CGoocHfcnclkwmg0Yjwe4+60bdu99cXMcHcUwlKJmWFmzOdzVqsVy+US"
    "d9+j3Q+raRqkwLRl0LYt0+mUUgru3hkCezkAMDMkYSl1tPoJ7CMe0jsGEdHF9K9xn0Ep5dK5"
    "1kpEYhmbMrr7prevQNzJzknTNFxImCTMjOFweND4KielFJSJlTxneP8ZikAhIgJpOzzatXAi"
    "BRnZtbgE6DfluuP8B0lo4LBenPPIAAAAAElFTkSuQmCC")
getautoTestData = autoTest.GetData
getautoTestImage = autoTest.GetImage
getautoTestBitmap = autoTest.GetBitmap

timer = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAApBJ"
    "REFUOI2lk0tIVHEUxn/3zowzzp33aJr5CtNKDTJMKiqEWlQS6aZFENGiWlvRooheRAQh0SZ6"
    "UFAYZUK0shQygzKMMFNMCzOf+Wqc0Xl4vXPvv0WgFdaivuXh8OM7H9+RJNnE/8i80PDlgxPC"
    "apvFZDGhxwWxSIxIGLYduCL9viv97KDp/jnh8UzhzSrH6krGavcihEE4OExgsJPhrka2H7wp"
    "LQhovHdWpC/z4cvawXjUSXtPiLHJKHFd4HXaKMhx4BWf+fDiDmWHbsxB5k5wKJN4MvbQMWhh"
    "Ihhida4PjysJgUQgpNPSNY7DmsrK4l3cPRMUe089lABkgIbbR4U7fQvjMRcjgRkqSrPxOQWB"
    "cBiHSyEzw0X51hxGpw0m5HxSli7h6vHdYg4gS1EUXzpvuwMU5vmJxgUWi4WGp0+YCoXQVJX6"
    "hkby85Jo7gySmleCScwyBxBCYFO8DE9E8fsTUXVBgt3OYH8/Dc+aOH/hIk6ngneRna+BGdzJ"
    "2ZiQ5gGaqmEYKrFZA1UHzYCx0DSKw0F72zvKyisoWluCGgdNMxDGDMIQ8yFGwjFCox9xK2n0"
    "jkTJTXeDbGNN8TpWrCrE7nYRVmFgJIJLkZkcamMmrs87mI7BQGcTJcsTaW4dxWIFxWZh46YN"
    "JHldWAGHDd60jrG5QKbv/Ss0YZ4H7D9ZLfV39+LTXpPhDHOrtpu+oSCSqiHFNPoHglyv6SIz"
    "cYzkWB0DPREqqx5Jv/Rg3+laqTrBEEWlYdL8JdQ9DxKc1tENgdMO6/MFSWo9LfUtaAn+hasM"
    "cO3YTpGSZScjrwDP4iwQcb4NfuJLewejwwaa2cHhSzXSHwEAl4+UC1nXMMs/ko4bErpsprLq"
    "8d+f6V/0HRaqEJ8OVfU3AAAAAElFTkSuQmCC")

gettimerData = timer.GetData
gettimerImage = timer.GetImage
gettimerBitmap = timer.GetBitmap

quickConn = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAf9J"
    "REFUOI2lkztrlFEQhp/vks1l2V1ZFHchF8TENIKdrcbGxsagFm5roYUg/gUNWigR8xu0EkMK"
    "Gy2tBBERMcmGRKIYQ+6XzX6bPWdmLL5dQUwTcmDgcIpn3ve8M0EQRhzlxABPJqu2UTfMAFVM"
    "FVHB1FBTTAQ1w0QQVfIZx6PbFwKAYOzVvOVy2UN3np+e5fn9S0Fcd0Z9o3ZoQOIstWBijFUG"
    "Dw249XixBTAFoOkFA/zuJxpLE5h4TBT1iokizmH04AYecqr/NKKSAtKfgyAMCFSQnfd09pwk"
    "6jiBOY85jzQTks0ZrHSDjmwJAPUpIGyTQsD8Ks21t3R0D6B73wjCLCqexlaVqHyTrvIV4kyc"
    "AiRVHppay5Wwv/qGTG4QiNBkGfX7bP98R1QapbvvKlEckInSudG2hfbF16s0fk+S77uM+QSi"
    "MjiHaYzWfrA3/Qx1CRbm6Rq+jmqqIPbOAVBbGCdTGCJZn0G9kukZBI0plEZI1r8grsnO0meK"
    "5x8QdR7DO9+OMSV1FUfwjTUIQ4KoyebCFPnyRXxji2Z9jbBwjv7Rp8S5PsIowtoK2lKyvZW/"
    "GauvsT37gvrKVxq7KxTP3qNw5to/c6Ct9OJf3xe5M+5QEVQUEaHSO8Hw8SIf5kKmlu+SfIww"
    "eZ3uhSqtnrTyj/6ruZdDdtD7gXXUdf4Dfv8YZ4B4PeYAAAAASUVORK5CYII=")

getquickConnData = quickConn.GetData
getquickConnImage = quickConn.GetImage
getquickConnBitmap = quickConn.GetBitmap

editScript = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAApJJ"
    "REFUOI1Vk8tvTVEUxn9rn3Mut1pXSKQtSkOjIU2JiIjngHjGX2AmJAYMGZh4jIiYGFQ8QkjE"
    "QIIg4hVBlYFUkRsiLvXuW+ve6n2cvZfBuY9ag72Tlb2+/X1rfUvEeABsPfpMjfB/CKAC6gid"
    "Y3hQ6Ti+5r9XIsZj45HHemnPEowRFIiOKLSY6M8UuPxymJ6vOc7ubS6D+ADGE2K+R7IPjAhE"
    "n2LVEYbKWMGytqmG9XXtTE9fZN+1wzo68JjFOx+KH9EQVJWY5yEoCjgDOLACBiHXc52m9Avi"
    "LdtJNC5m+PN8Oo4Z9cczNoAIKBFDFcEIJMbuYfUNU5tWMJR6R0zy1EyupXpaQyShpNX3QBBU"
    "BGcVjFA91k7DhE4SjRvI/bpCrEr40vWekb/C8t3nxZSKFfDFYEQwgGeEieknNOh9EnM3k/15"
    "Bgl+E1TXEHdDnBrYVGYdaS7SNyIYEbLdN5k6eo/EvG1kf7RhggL5P3Poffqa+OpD/LB1FQAX"
    "RixcEWz0022q0h1MX7iFfM9ZvJiS+zOb3vZOBle2IdOasY5xAE7Roo6ezivEh59TcPX8ensS"
    "R5bRoRn0vnhPevUppLqOiYFgQ60AWAdWo9n3vz3HgpW7mPCtnQ83ntF1d4jkgy4yy44SVtWj"
    "QOAZwnxYMZILFafKwVd5WlL95JO3aGxdxUj/IKmuFI/WXmWgexaOqOhybUAh5yoAYWixFuom"
    "ByQ/9nHidBtLmxsZq28ls+4ii2pmRpNSeNMXok4pZMcxCHPRsuQtTDnwnU+ipIpmchmQTIhT"
    "UCMYJ/i+ENpxDApZy6SYx/6WfLmZxSaTiPtlo8UDQQQCT7Chq2wjQOuOOypS2oSSPaOxlnPF"
    "yzlH8sJWAfgHfe05PpgOvmEAAAAASUVORK5CYII=")

geteditScriptData = editScript.GetData
geteditScriptImage = editScript.GetImage
geteditScriptBitmap = editScript.GetBitmap

autoCreate = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAblJ"
    "REFUOI2lkrFrE2EYxn/fnZJLjksPNMbYuVDBJYNBQghaG0FqKR1sQRyzxH9BxNnN0c1JcFNC"
    "oEPp0AgWFOMd5IKiJKPQtKU5Qoxtcq9TotE0jfjCs3w8z/d+z49PKU3nf0ab1tjenpdx52cm"
    "ht5cEYIeBD00cw74hL91QaI3d9XAo06r0Kmsiwqdg7M2QatC//At0Zw/+YL29rwQHKFZl1Ez"
    "V3m38x7LsrCiFpfMzxz7O9DvYt/WFUrTT1Tn46qUX6xIt9uVIAjkw+t78r32QFobyMBzIkR/"
    "67ysPTrGmHuIiOB5Hn6rhdIjEJwC0d+05f7Ta8zOXqRcLtNoNDAPnrG4kOLH1ycj3rEMlu8s"
    "SSKRwHVdIpEIpmny8nFAv1WBozYzS50hxL9eMAg7jkM4HKZarfLl+S69b2Cv6OrwVV/g19IR"
    "ButrdyWVSuE4DoZh4Hkezb19ZS/ratDbXtXV75lhhVu5RclkMpRKJQzDoFarsbd/MGIeNxrA"
    "wo3rkk6nKRaLhEKhqcMAFAoFqdfrkkwmJZfLSSwWk0l/409pAM1mk3w+j+u6028eQtB0stms"
    "xOPxf9o80E+A7a2av0R7kAAAAABJRU5ErkJggg==")

getautoCreateData = autoCreate.GetData
getautoCreateImage = autoCreate.GetImage
getautoCreateBitmap = autoCreate.GetBitmap

pin = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAYBJ"
    "REFUOI29kyFvG0EQhb+1E7KHAm6lomwjox4ujlR4qsoOFCQ1CDtshcapme0f0cYs/FhqW0V1"
    "pICqd8RSdKSgNnLSXWnRFjhRc7KTWqqUJw2aN2/fG80KUavzP6htSuz3uv7jcduvNESt/s8a"
    "DAbeOeedc/7q65U/en/k73sbOZBSYowBQEeaOIl59+atB9h61PJp1yutODj8IKy1jLIR4W5I"
    "QACAYSm4VuDs8yefJAkGQ3/W9UmS0EpbKK2QUmKtZV7O1wv0e8sBgOw8I01T8jxHv9KMx2Mw"
    "UJqS79c/xFoBa+3SnoE4jsnLnKIoyLIMDFx8G4qH/LVLzCf5cmkBYGAymtBsNrmLX0FdiKrG"
    "cDhq7+29PFksFmyzjTEGtaOY5lMup5f8+jlrP+RXIvRPu94C+/uv6bV7hDpEIkFCURSEQbji"
    "oCJggVYrJdIROoow5Zy5KYGQMICLL9X8wN9L7HQ63jnnGy8afpPrvK+KA6UUN7e/V195AuLZ"
    "fuNj+AP9t5bpL+X+CAAAAABJRU5ErkJggg==")

getpinData = pin.GetData
getpinImage = pin.GetImage
getpinBitmap = pin.GetBitmap

send = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAilJ"
    "REFUOI2V0b9rE2Ecx/H3c3f5Va1WxWppF604OAmOLv4Fbiqi0CWKU3VQJ9EOItgWNwepSpeC"
    "qNXFDkJFQymliENRQxVsJE0M0SRNLrl77rm75HEolBbSln73z+v7eZ6vEIbJTmdoIq0d6TOS"
    "PCnEdsD4dFGHzQA/aBKEIc3QJxEzyP6t86vQwNpum2mE7O0wUEEL5QukMqg5inhEUK7aWwOP"
    "3ma0JTQrtkfJ9pDKx/FCOhMmP7MVPoyeFVsCtitRvmR3TBCzoFBWuFIhtEWl1ABo3+DZ0zEd"
    "BAHXLp0QAOfvf9KH90XpjBsUSh6mEaNRWwWM9cHn0wX9ZPKz7unpob+/n5Hhhxrg5Z0zYiGd"
    "53euyp4OC8fzcMr1jcDY+5y2jBaJrkN8/dPCtm2klGt46vE5sfgtR365TOZ7AbfmbASkCumI"
    "gilaRA4cZyYT5e69IXHj+qC+eiWpAb68SorMQpZitshi6pbY8AfK95GeJl922RUXJPb3cuH2"
    "uD7aW6W7u5tKpaJfT74R6Y83xfpnrzVwPR/H82m4HpmCTTwCfUeOMfvDZWlpCaVU20utNfAD"
    "heuB7Sqk51Os+MQtk0TfKabm55h9NyXaAaYQBgPDM/pgVxTb8YiaAssEyxA0W02ymX+kJgbb"
    "hgGsiw9SOh6FZhjiSMVyvkZ9xUE2PLyGQtrOZtlVoNpwMXSEdKlOLldhbvzyptvajRCGyenk"
    "Cx1KxfzEwI7CAP8BEVoRr2+2he0AAAAASUVORK5CYII=")

getsendData = send.GetData
getsendImage = send.GetImage
getsendBitmap = send.GetBitmap

timelog = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAwtJ"
    "REFUOI1tk11oW3UYxn//c3KSk+arJjJDSNbGFkvmoA5BilovRnfjNstGweLmzfBiKOKNt14I"
    "4oXQeeFE2azrbqRq1a3ViWx+liXMSec2JGlrTT/WJYvzpCdfJ+csyfEi1nXoc/XC+z4Pz8v7"
    "vEJIMgDlmabNP/DtlwX/g82ZrX0hJBltqmkrsUM44y9gZMfJ5HQ+7fjsHvJI7Vl2xMI4XCHM"
    "zBsER9oiQkgyG6nnbLVrlFJ2ipW1eS5EpvG6mriVFgDGHQnLqLI7P0J3Yhi5WaKWHiN8SBYS"
    "gFC7KC5Osbg0TzI2SdxnETQMzD80qosa3lKVsM/J3ANj5LJJ5NAAtjsBgAPg5qVj/CX1crHn"
    "DDEJFM3k0d4gnf0hbASa3uTnzJ/g7uaavQdrdgylsn5X4AP5Y+TObnoUgVxpcGB3nKKuc7tS"
    "IRYJ4/VDJOrnwlcfkaj8guzdT9XwA9+2BXKNCBEbWmWLnTvD1Bo2iqJw/psvGDl4ALeqMvfD"
    "2wx4NnB3HSYQ38VGto/kW5LtADCNKg1LoJstQiE3ZtPG09HBjdVVzn/3I8baGQ4OdeH1P4G2"
    "lMYpLHz+MN7Q9rYDy6hSrbkwZIHZbJ+toJfxeL2UVs4xuidKID6EmZvE2SFY+TVDyYCBoxPt"
    "K1hGlVK5hnC0yOZrNIUEkspgv5vRoSCBnqep3zyJUIooXh+Nap4P87sAkDZXKOk6Wt0kdeUW"
    "igvqy1/zUOcKgd5nqK+/h6TcwSp1c+P7Kxwv7GOh7LubRIDHX3rH9nTGeDgaoM+R4ano7/QN"
    "7sO6dRohW9T1KLmf5ni98DxrWonkuy+LewQAjr45YTcL13llyEFDbCMUvMh925zU9Rirs9c5"
    "WRnFarUYf+3Iv7/g2Jr3F/c+QvrcBDueHGd+8lUWZpO4tvej5df53BzmyN4HkSTB+BaOtFnM"
    "TJ+1VVVlYamA9duXxPsH8Xj6WL6c5sRygsvZ2xSLGveHQsxMn7X/40DTNFKpFFfT6xx7/ziP"
    "JeLYquDwqTUBJwAY/gROT5yytxjgb20aPSxD9YfOAAAAAElFTkSuQmCC")

gettimelogData = timelog.GetData
gettimelogImage = timelog.GetImage
gettimelogBitmap = timelog.GetBitmap

quickScript = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAvpJ"
    "REFUOI1t089v03Ucx/Hn5/v99rvv2q79buvGLJWUjBVwmhBRNJNgDTHzx8JlhKiJF24aLiZc"
    "MJ408Q8wHjh4EDTRxGAQ48GQANuCm1UcsKJ1FDZ+dbXbvvv2x9p+v/32+/GGmdv7/M7j9HoK"
    "oahsdfO/npZeLYdr1yGyj32vvi+2+hP/B3I/H5dmfBBFDdL0DFrrTVr1MsXCIul3v9yEPAYW"
    "b/wiNe8M7VmV7tFR2o6FaFlUVwqoIk6zusrKnd8pViscOTUjNgB3Z7+QmnhAb//zrE5cITwc"
    "wrHmsK8XCA1202U+gRbdixLooXD7D/6+9YCxUxfEY2D2xEGZ+vAk7fU85YWL2FP/gC7YfngE"
    "6fkI2ULBp+UIAv0vULw5QXG9m/R7nwtl/uqnMnb8bQrnfkS4ZbyGpGG5xA89g4aLIlsono/v"
    "uuDWWb9/i2jyRazsJACa3/yTSOIYq9YZlrMLVHMWqWP7eTSTpVluI3QNIxZE03VCQY2OQJl2"
    "1w602NN8NOpKbSX7kMSuFonXX2H+7AXaPgSMGMlDL4HnIiRUSiV8x8MuVWiVXQJLGfpCXdRL"
    "i2j1yQz1lwto0idg6vQOxbj2zUWeHU+jIpBCJdq3Dek5RKIGwnPA6MW2YSQZRokfTVO5u0bu"
    "/CUId5IYHObJ53Yy/cM01nIVoUgkAikUUAHfQzF6cGprFG0fzfMUOoYGCK8MU1++TW1tmf7E"
    "AEa0l5tTOYRQ2XsgiRkGxfcQRgihhVi9t8iJy5bQ0EbIX/+NeF8KM9KkmF8i9VQcs0Nw8LXd"
    "lK0mf2UWwPPpCCoM7H+DuW8v891P1/4b0vlPjkqn0mDsrTeZm5xhd7KBobggQaoKUkhUzaSm"
    "DHF/OsOls99z8o4qNkz54/E98vCBPWzbOYweiRL0H9HpN1D0TkRkOzQbNHJXuHF1ivRXntjU"
    "AsDpD8Zkj50lYg7SsyuFJTsJyQqR+hLOwwnyBXjnXG1DUJtqBPhsfIfULRtTh1JQJ5P3+XrO"
    "2jLnfwHX5kNGpasOiQAAAABJRU5ErkJggg==")

debugpointon = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAALVJ"
    "REFUOI3dkksKwkAQRN/MGLyASxcBd55AyXm8hQtBryaIKAieQd1JPo4mwZn2AJmAkkXAXnZX"
    "F9XVpZQ2dCndafs/CAZtA2+cvAVqgVJghFEhnAp9wRsnfrnCJ3OkKnnuDtzWG6ZaN0iCCmoB"
    "ncxw+y3unhLFE4qWa4PdlweXZrgsR8oK/7DkhPMSVGABfzozHMeItWRpwYUIcA1s0AOAoxex"
    "GAoUVyIWuvzexF+q/yD1T/AB0pdCSa0HdO8AAAAASUVORK5CYII=")

debugpoint = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAMJJ"
    "REFUOI3d0j0KwkAQBeCXaKFor6itiGKfMqewEkvvY2PlRXIAGwsbTSGCkAMYlPxtsruT8QBu"
    "QEgR8LXDfAyPsSy7hTqxa23/B9CuGriew0wMaEYpSxxXZ+tnwPUcXk82mPUXKKjAPbxBHRSf"
    "tpcvxAiwZkx7c1zfPhIZY9wZgQUZLzV2wLJEqhJkMoUuFQqdgzIzYLyABCF4PTDsDpDrHHEU"
    "QT2lEbCqPtHZL5kEgQRBhRL+LjCWWAn8muYfqXngA4LZU7uUj7qNAAAAAElFTkSuQmCC")

ixos = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAAAA3NCSVQICAjb4U/gAAAAXElE"
    "QVQokc2SUQqAMAxDm+G9u508fhQlKq1TEOzPwsiDtzJYt6npFk3MAtu0Z/VfAkscdOotBjLg"
    "sCU6i+pLpRSgMzz3cAOom+ZKCQPXV1VAtE8LbJmx9jR///lWtX0sB1gS3IgAAAAASUVORK5C"
    "YII=")

printfront = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAARVJ"
    "REFUOI3FkztOA0EQRN+OLXJSUosIOBW3gdNwDV/AGMkREjcg8G5XFcF6vWDsiICWShqN1K/6"
    "M9N1bcFfov0pG1gCPL+8Z7pQQgQKWEYOUrCgSjw93na/AAA311ckwYE42CAbG3yA7D7qfAVK"
    "sMdkO98EkkeAwzDoAkDMCSeuU7IVqnIBUKZ03tUKMtimr7B93cQ2trm7f+iWAFWe3U5cj2eD"
    "BrFa3ZKEzWYzV1A1Qs65Tu3YoQSSaK1hewb0g5CWZ12tAyRBnocoaQYMZd7eP6lD/+NQfdy/"
    "EmITIBkHOVVA1xa/tNvtIil93x+13++Pqqqs1+t0bTE/pO8hiSS0dvml/2jhNGyz3W6Z1nVJ"
    "AN2//8Yv4wFtllmhytIAAAAASUVORK5CYII=")

printback = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAP5J"
    "REFUOI3FkzFOxDAURMdmBfWKLtDSwy434h7Qcw/EdaKUSIDErrgBzebPfArHkbNxRLEFX4pk"
    "F/P+jEcJIZ7hlIknqQGsAGC/+3JJyB9JkJydN9v7UAVIQtM0i1vcHW3bLjsgiQyqiWOMMLO/"
    "AcfCckji6fXTSYcImBHPDzdhBjgW5rskXK3PITlIx/u3zR2U4poDMyWAHH3PKSBnXZrURhKL"
    "DjOfArquq1ZYVmsmUCnOoQTc3m3Gfh9fPvz68mLMmi2rPAtgGaEcM0yyij5ulQApgWx49xng"
    "0BPkqrpVHCDuMC046E142/3ABJACieENUv90h0vIHYV//xt/AdsXJdn97R7aAAAAAElFTkSu"
    "QmCC")

test = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAAAA3NCSVQICAjb4U/gAAACoElE"
    "QVQokU2SPUvrYBiG37e1rdYIVlqshEoJDpXqYFykIIJDOihujoKDi9ItP8DfoLg4ipujIGq7"
    "WMVqNpcaqEqsaMFoU4hJ3s80Z8g5cp75urjvGx4YBAH4d7quN5vNVqvVbrcJIel0WpIkWZYX"
    "FhZ+GRgK3W63Xq9fX19PTU2NjIwMDQ0RQkzTfHt7u7+/X1tb29jYmJyc/Ct8f3+fnp4ihBYX"
    "F7PZrOu6r6+vrus2m81kMuk4jqZpqVRqd3c3n89HAAC1Ws227aWlpWKxSAjZ39+v1WqmaYqi"
    "+Pj42O12Z2Zmnp6eDg4OAACRh4eHs7OzfD4/NjamadrR0REAQFVVTdMkSWKMfX19maZZKBQO"
    "Dw+r1WpUluV4PJ5Op2VZ3tvb29zc5JyfnJxks9mVlZWLiwvO+c/Pz+DgoG3bEMLoxMRELpdD"
    "CGUyGUppq9WKxWLFYnFra+vl5eX29pZzzhhzXRdj/PHxEU0kEvPz85ZlMcZWV1cJIbFYbHl5"
    "GUJ4fn5uGAZjLAzxfV/X9QHHcRBCCKFGo8E5n5ubkyTp+flZ07R6vc45932fMUYp9TwPAAAV"
    "RSkUCsPDw71eD0IYBEG/3/d9P2wSoq7rep7XbrdzuVxkdnZW1/V4PI4QwhgTQgghlFJKaSgQ"
    "QlzXpZT2er1SqRRRFOXu7q7T6UAIPc/DGFNKfx2MseM4GOP39/dIJFIul6PHx8eWZV1dXY2O"
    "jjLGPM8LVxJCEEK2bXueZ5qmZVk7Ozvb29sDAIBKpfL5+XlzcyOKoiAICCFKKee83+9jjDud"
    "DsZ4fX29UqkAAEAQBEEQGIahqqogCKlUanx8XBTFTCaTTCYTiYQgCKqqGoYRkvD/965Wq5eX"
    "l41GQ9d1AMD09HSpVCqXy4qi/DJ/APn/xxEndIeaAAAAAElFTkSuQmCC")

printUI = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAAAA3NCSVQICAjb4U/gAAACf0lE"
    "QVQokUWSP0vzUBTG701ibUoVIo22STVkcXASREGcFAS/gTr5AfwIfhAHF6cujlJcrHMXwUFs"
    "G0SRFkRLctPmNsn9kxyHvPo+yxnOc87h4fwwAKBfMcaCIJhMJuPxOIqiLMsWFhZc13Uc58+j"
    "FAUAvr6+BoMBADQaDdd1R6NRGIYA0Ol0bm9vkyT5PwAAo9GIc76+vl6r1TDGqqpubW0JIe7v"
    "7wFgfn6+3W6naYoQwsVuznm9XpdS5nkuhMAYA0CSJL7vc84rlUoQBLPZ7PDwUGGMfX5+Yoxb"
    "rdbNzc1wONR1HQDiOI7jWFEURVHG43G5XI6i6O3tTfN9f2lp6fLy0vO8jY2NWq3mOE72qzRN"
    "0zQVQnx/f1uW9fj4qBBC8jz3PK9SqVBKX15ewjDknBdWABgOh51OJ4oiVVU/Pj40Smme50EQ"
    "xHE8mUwAYDabKYqSJImUst/vX19fT6dT3/dPTk4YY4oQwjTN1dVV3/cNwzg7OyuVSnEcc857"
    "vd7V1VUQBAih5+fnIAiEEJqqqqVS6eLi4u7ubn9/3zTN4iZCKAzDIjdCSNO0crmcZZm2uLhI"
    "CFlZWTk+Ps6yjDEmpZRSpmnabDar1SqlFABc19V13TRNxbKsp6cnhFCSJEIIKaUQQgjBOccY"
    "W5al67plWQcHB6+vr7u7u5phGM1m0/O8tbU13/dVVS1+V+jo6EgIYds253wwGGxubmIAYIy1"
    "2+1qtep5HiHEcRzbtoUQaZrOzc0ZhkEI6Xa75+fn9XodF7ROp9NWq0UpLdq6ru/t7amqSint"
    "9/uEkNPT00aj8Y+lP3S73e7Dw8P7+7uU0rZtAFheXt7e3t7Z2dE0rfD8AE27vCA8hXTdAAAA"
    "AElFTkSuQmCC")

quickShell = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAAAA3NCSVQICAjb4U/gAAACW0lE"
    "QVQokU2SMU/jQBCFZ9brjW0whBSxIIoSJAQISJfCDUh0lPxHfgMFBYgSpQGhNMSKQuHYKMGK"
    "jdGuYnt3rzDc3deN9J5mnuah1hoAAEBrnf6yWq2UUpRSx3F6vZ7nefAL1ob1ep0kyfv7u+u6"
    "nufZtr1ardI0tSxrPB67ruv7vuu6P4ayLIMgoJTu7u5qrYUQSinHcRAxjmMhhBCCcz4cDre3"
    "t4nWOo5jy7KazWZVVVJK0zQZY1LK9Xq9ublp2/bp6Ski3t/fAwDJsiwIglar1Wg0lFJaa0KI"
    "YRhSyqIoLMvyPG8ymdi2HYZhEAQ4m82yLOt2u4j4EwtRa621llIiYlEUnHPO+ff3dxRFJAzD"
    "TqfDOS/LEhH/qgkhpmlyzqMochyn3+8nSTKfz0me54Zh/C/9i5SSMVan55x3u93FYkEAYDqd"
    "Oo5jGIYQoizLOoMQIkkSRNzb21ssFs/Pz/1+n3NOGWOEECll/Q0AME0TAIqiqMd6T7PZDMOw"
    "3W5TxtjGxsZ8PldK7e/vK6U+Pj4AwPO8ra2tOI7jOD47O+t0Ojc3N71ejxwcHIxGI0opIiql"
    "lFJ5nn99fQEAIaS+UErJOR+Px0dHR6i1vr29tSzL9/2XlxcAOD4+RsTpdJrn+WAwYIy9vr6+"
    "vb3t7OxcX18TADg/P6+q6vHx0XVd27allFVVaa0bjUZRFHmeR1GUZZnv+4Zh/JQvy7K7u7vZ"
    "bHZxcZGmKaV0OBx+fn4+PDw8PT1dXV1dXl622+1/ba2ZTCaj0Wi5XC6XyzzPW63WycnJ4eHh"
    "YDCglNaaP9hSe57KFIm/AAAAAElFTkSuQmCC")

errorPass = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAgpJ"
    "REFUOI2lkz1oU2EUhp/vu99tbpKmaZv+0CpipSDdSjWLP2BBlC4RFRwEp046ODlo0UHQgoPg"
    "4iBiEacScHDpoEjFUqQpVhQURFtraWOStkljriZpcu/notULpQH7judwHl7ec44Q0mA7Uls1"
    "T1yOaRUpUQoaVNYC9M/OoQtpAIbiSbEl4ORIn97bHmKg7yJ2JUdidZzpiTyjg894cfs4w6CH"
    "4kkhhDQ4dvOGNnc9BuEgANAM7DxFb08/pqzDrq7huC7qdZo9VpKXY6Ocu/P+rwNlvuPS0VtU"
    "3Qqg8akApjBJFRdoMJtJFudZdxooP71L9+mzLK8WvBlYVpZ0cZE3uQkAOv27aaqL0GJ1UHZL"
    "aDSlwjfaglDMfqFUrm4AJIBlaqQQSCTqdyxSKAxRR9n5iasd6tfDtERCKCvs3cLBKw907ACs"
    "rWcxhEIIiRQSKQxCZhitXXyGxceFWfa3tZD6NOUF2H6Br9HP5+UJHF2l09/FjkAXARVi0Z4j"
    "sTRJRYY5ZEWhOEV6xfYCgo0f+FHpZl/zEQB8hkUiM87b5DTtdpRob4z5JYfhC4M8un6YzEp+"
    "4wYAlC+/wMPJSWS4CBqwTZyvrTy/OiNghhHuAXD/fI+WymA1+93rYPxaXFBDw2c6dWtr46Y9"
    "WWv4jzram7YHqA/6SWVy/w8AyOYKngChxjf+qydjrzat/wL5hbkAbU5i1AAAAABJRU5ErkJg"
    "gg==")

errorStop = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAgpJ"
    "REFUOI2lk81LVFEYxn/n3DszdxprrjozYjNOoBYUKYlgRFCblrUIyT6wP6BdtIrATURtWggV"
    "BG2CiCIESUqFNhlU9AHBQIlJWAZ+TOMMjtN83Dv3nhYT2g2pyAcOHJ4Xfpz3ed8jhNTYiPQ/"
    "Fe/t3a0SVhklXRY0P586gqiVRQAuPJgTAAiprXsWkyFl9R9V7rs3yh0ZUtUDXWpyX6eySzn1"
    "5FKPunKiRQmpIYTUKOzQFa4LrgIHcBSBgUG0g4dgiwnzc2BbTKSnaDXmeDZ6n9OD78VqC9KR"
    "GAPXQdPBrkKiBUwTvsxAcxw+pKBUZDJ1m/beU3xbWvFmIK2fQY6NgFLQ2QXxJLRth+8FcF2W"
    "p6aJhqCUnaFcqa4CJIAMhGpXqYEvAEKA3w/BIOTz4DjMb2sj0rgZ3Qh7gpZvO6JKO3sevn6G"
    "oAFGoAby+8BsqIGa41i6j1gswsL0K+8Yk3YBsSkEzyegXIE93dDaDpEYzounFMceE7Ar5ML1"
    "xPbDYqbgfUGdq1C2BUd64dhJVHcP1o2rLPUfJjU8RPjusMg0NHJudBy36pDOLK/tAKA/MpPs"
    "unaRpmIBF8gKg1Q4xvHZkmB2HIDEzTvi1pmdSuoaS9m8t4W+1x+Fx6ECLHucy31bVTRq/r6o"
    "a1P4FzU31W8MUBcKspDO/T8AIJtb8QQIf/mNv+rh6Mt1/R9tpbjPTgXayQAAAABJRU5ErkJg"
    "gg==")

icon = PyEmbeddedImage(
    "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")
geticonData = icon.GetData
geticonImage = icon.GetImage
geticonBitmap = icon.GetBitmap

Smiles = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAolJ"
    "REFUOI1tk91Lk2EYxn/vx7OmwyBhVsytmY1cCBFBQWSRlYVGJ51EjajptliH4X/QQeJ5J+ZJ"
    "f0AnIVSWJ0EQQfQhzNG3JkRQILrl3tft6sDNRvnAdfI8z8V939d13Vi2w79IpS4pHt8p17Vk"
    "jK1EIqpcLqPN/to0nWwmrc5IUL29n3jw4Ajl8mVKpYvcv7+frq5HdEZqymauqZljWbYDwOlT"
    "xxSL/eTOnfMY4wElYAWoAhXgI75fIJ/3mJ8/wvST5xaw3kE2k1YsBhMTtzEmCYTqxEaxVaCM"
    "MRYTE1uIxZ6RzVxdf7Rsh2i0XZ5XkPRF0mONjo4KkJSSlBKgcDgsqVVSizwPRTuRZTu42Uxa"
    "XV1rGNMCOECN8fHxpimX6OnpYW5uDmgF1TAEuXG9yuf5lOyZmYcMDUWAReAj8LqJXAEWWVhY"
    "aLqrQaWVoZNtzMxMYRljq1S6iTFtwCrDw9+ZnPQ2hIOFuqB1crUKSx34qw6hXfMNG7264stM"
    "TvrAEvAOKDaRBVpjd2cQ/BbwgwDY8XiEYvEb8AMokky+BF7UK+svGR+qNp+/L0O5jeKcRXxX"
    "GLe//wxTU/fo7Q0AolCAUEiUGoWpAWtQtTi4rw19iUB5K1OPf9F//GTDRkue11K3ad0qBYMK"
    "BAJyXUehoKv93e3S4l6p0Cfv1QlFdwS0EeXBwTT5/Op6mw389qn4Pr5jcTjZweunUVgOw1qA"
    "/K0ig2fOsREky3YYGOjTyAjyPCTVUbWllW3St6T04ZC8N0c1cmGHBo4f0H/LNP3kueU4w3R3"
    "w9gYzM6CX3HwKzaz71cYu/uV7rMvcLb2Mf3srbURi81WNJdLK5HYLuMi46LEng7lMlc2Xec/"
    "xiMt8QU2mDwAAAAASUVORK5CYII=")
