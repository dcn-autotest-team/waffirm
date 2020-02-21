#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# *********************************************************************
# BasicWebOperate.py - Proc of Basic Web Operate
#
# Author:guomf(guomf@digitalchina.com)
#
# Version 1.0.0
#
# Copyright (c) 2004-9999 Digital China Networks Co. Ltd
#
#
# *********************************************************************
# Change log:
#     - 2015.12.28  created by guomf
#     - 2018.3.12   modified by zhangjxp
#                   新增函数exportal_redirect_success,inportal_redirect_success,
#                   exportal_login_withcheck,inportal_login_withcheck,portal_logout_withcheck,
#                   open_url_withcheck,newis_extralportal_page,newextportal_login,newportal_logout,
#                   newextportal_logout,https_inportal_redirect_success, https_inportal_login_withcheck,
#                   https_portal_logout_withcheck
# *********************************************************************
import time

from dcntestlibrary.tplibrary.selenium import selenium
from dcntestlibrary.tplibrary.selenium import webdriver
from dcntestlibrary.tplibrary.selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from dcntestlibrary.tplibrary.selenium.common.exceptions import TimeoutException, UnableToSetCookieException, \
    WebDriverException, NoSuchElementException

from dutils.dcnprint import printRes


##################################################################################
# web_init :初始化web实例，后续关于页面的操作均在此实例上进行
#
# args:
#     host: 打开浏览器所在的设备
#     url(可选): 初始化打开浏览器时打开的页面，默认为本地页面
#     port(可选): selenium服务所监听的端口，默认为11918
#     browser(可选): 所使用的浏览器，默认为firefox
#
# return:
#     selenium实例
#
# addition:
#
# examples:
#    在S1上初始化浏览器实例
#    sel = web_init('s1','http://1.1.1.1')
###################################################################################
def web_init(host, url='http://localhost', port=11999, browser='*firefox'):
    return selenium(host, port, browser, url)


##################################################################################
# web_open :打开页面
#
# args:  
#     sel: 所初始化的web实例
#     url: 打开的网址，如果不指定，则打开web_init初始化时的url
#     注意：如果是portal跳转，页面加载完毕也算打开OK，即当前页面不一定是url的页面
#
# return: 
#
# addition:
#
# examples:
#    sel = web_init('s1')
#    res = web_open(sel)
###################################################################################
def web_open(sel, url='/'):
    try:
        web_close(sel)
        sel.start()
        sel.open(url)
        sel.wait_for_page_to_load("60000")
        sel.window_maximize()
        return {'status': True, 'Message': 'Load Success!'}
    except (TimeoutException, Exception):
        return {'status': False, 'Message': 'Page NOT loaded in 30 seconds!'}


##################################################################################
# web_close :关闭页面
#
# args:  
#     sel: 所初始化的web实例
#
# return: 
#
# addition:
#
# examples:
#    sel = web_init('s1')
#    web_open(sel,'http://192.168.1.1')
#    web_close(sel)
###################################################################################
def web_close(sel):
    try:
        sel.delete_all_visible_cookies()
    except (UnableToSetCookieException, Exception):
        return {'status': False, 'Message': 'Warning: may be some when delete cookies'}
    try:
        sel.close()
    except (WebDriverException, Exception):
        return {'status': False, 'Message': 'Warning: may be something wrong when close'}
    try:
        sel.stop()
    except (WebDriverException, Exception):
        return {'status': False, 'Message': 'Warning: may be some when selenium stop'}
    return {'status': True, 'Message': 'logout success'}


##################################################################################
# portal_login :登录portal页面
#
# args:  
#     sel: 所初始化的web实例
#     username: 登录使用的用户名
#     password: 登录使用的密码
#
# return: 
#
# addition:
#
# examples:
#    sel = web_init('s1')
#    portal_login(sel,'user','passwd')
###################################################################################
def portal_login(sel, username, password):
    try:
        if sel.is_element_present('id=username'):
            sel.type("id=username", username)
        elif sel.is_element_present('name=p5'):
            sel.type("name=p5", username)
        else:
            return {'status': False, 'Message': 'Can NOT find id=username or name=p5 in page'}
        if sel.is_element_present('id=password'):
            sel.type("id=password", password)
        elif sel.is_element_present('name=p6'):
            sel.type("name=p6", password)
        else:
            return {'status': False, 'Message': 'Can NOT find id=password or name=p6 in page'}
        if sel.is_element_present('id=login'):
            sel.click("id=login")
        elif sel.is_element_present('name=Submit'):
            sel.click("name=Submit")
        else:
            return {'status': False, 'Message': 'Can NOT find id=login or name=Submit button in page'}
        time.sleep(20)
        if username == '':
            if sel.is_element_present('id=username') and sel.is_element_present(
                    'id=password') and sel.is_element_present('id=login'):  # 不输入用户名页面点击login无效
                return {'status': False, 'Message': 'No username inputed and page correct'}
            elif sel.is_element_present('name=p5') and sel.is_element_present('name=p6') and sel.is_element_present(
                    'name=Submit'):  # 不输入用户名页面点击login无效
                return {'status': False, 'Message': 'No username inputed and page correct'}
            else:
                return {'status': False, 'Message': 'Warring: No username inputed and page incorrect'}
        else:
            if not sel.is_element_present('name=p5') and not sel.is_element_present(
                    'name=p6') and sel.is_element_present('name=Submit'):
                return {'status': True, 'Message': 'Inner Portal login success'}
            elif sel.is_element_present('name=p5') and sel.is_element_present('name=p6') and sel.is_element_present(
                    'name=Submit'):  # 不输入用户名页面点击login无效
                return {'status': False, 'Message': 'page return "system busy" or "username or password incorrect"'}
            elif sel.is_text_present("You have successfully logged into our system"):
                return {'status': True, 'Message': 'Outer Portal login success'}
            elif sel.is_text_present("Account does not exist!"):
                return {'status': False, 'Message': 'Username incorrect'}
            elif sel.is_text_present("Please enter the correct password"):
                return {'status': False, 'Message': 'Password incorrect'}
            elif sel.is_text_present("Wireless network problems!"):
                return {'status': False, 'Message': 'Wireless network problems'}
            else:
                return {'status': False, 'Message': 'Something wrong when portal login'}
    except (NoSuchElementException, WebDriverException, Exception):
        return {'status': False, 'Message': 'Warning: throw exception when run portal_login'}


##################################################################################
# portal_logout :登出portal页面
#
# args:  
#     sel: 所初始化的web实例
#
# return: 
#
# addition:
#
# examples:
#    sel = web_init('s1')
#    portal_login(sel,'user','passwd')
#    portal_logout(sel)
###################################################################################
def portal_logout(sel):
    try:
        if sel.get_title() == '\u767b\u5f55\u6210\u529f':  # 登陆成功的ascii码
            if sel.is_element_present('name=logout'):
                sel.click("name=logout")
                return {'status': True, 'Message': 'Outer portal logout  success!'}
            else:
                return {'status': False, 'Message': 'Can NOT find name=logout in this page'}
        elif not sel.is_element_present('name=p5') and not sel.is_element_present('name=p6') and sel.is_element_present(
                'name=Submit'):
            sel.click("name=Submit")
            return {'status': True, 'Message': 'Inner portal logout  success!'}
        else:
            return {'status': False, 'Message': 'Page is not the login success page'}
    except(NoSuchElementException, WebDriverException, Exception):
        return {'status': False, 'Message': 'Warning: throw exception when run portal_logout'}


##################################################################################
# is_portal_page :检查当前页面事都是portal页面
#
# args:
#     sel: 所初始化的web实例
#
# return:
#
# addition:
#
# examples:
#    sel = web_init('s1')
#    web_open(sel,'http://1.1.1.1')
#    res = is_portal_page(sel)
###################################################################################
def is_portal_page(sel):
    try:
        if sel.get_title() == 'LoginTitle':
            if sel.is_element_present('id=username') and sel.is_element_present('id=password'):
                return {'status': True, 'Message': 'This page is Outer portal login page'}
            else:
                return {'status': False,
                        'Message': 'In this page CAN NOT find id=username and/or id=password input element'}
        elif sel.is_element_present('name=p5') and sel.is_element_present('name=p6') and sel.is_element_present(
                'name=Submit'):
            return {'status': True, 'Message': 'This page is Inner portal login page'}
        else:
            return {'status': False,
                    'Message': 'Page title is ' + sel.get_title() + ',please check why not is not "LoginTitle"'}
    except (NoSuchElementException, WebDriverException, Exception):
        return {'status': False, 'Message': 'Throw exception when execute is_portal_page'}


##################################################################################
# is_alert_exist :网页是否染出提示信息
#
# args:
#     sel: 所初始化的web实例
#     text: 提示信息的内容
#
# return: 
#
# addition:
#
# examples:
#    sel = web_init('s1')
#    web_open(sel,'http://1.1.1.1')
#    res = is_alert_exist(sel,'Password error!')
###################################################################################
def is_alert_exist(sel, text):
    if sel.is_alert_present():
        if sel.get_alert() == text:
            return {'status': True, 'Message': 'Message alert correct'}
        else:
            return {'status': False, 'Message': 'Message alert but NOT ' + text}
    else:
        return {'status': False, 'Message': 'No message alert in this page'}


##################################################################################
# is_element_exist :页面是否存在元素
#
# args:
#     sel: 所初始化的web实例
#     str: 元素定位信息
#
# return: 
#
# addition:
#
# examples:
#    sel = web_init('s1')
#    web_open(sel,'http://1.1.1.1')
#    res = is_element_exist(sel,'id=passwd')
###################################################################################
def is_element_exist(sel, _str):
    if sel.is_element_present(_str):
        return {'status': True, 'Message': 'Find element ' + _str + ' on this page'}
    else:
        return {'status': False, 'Message': 'Can NOT find element ' + _str + ' on this page'}


##################################################################################
# checktitle :检查当前页面title
#
# args:
#     sel: 所初始化的web实例
#     title:页面title
#
# return:
#
# addition:
#
# examples:
#    sel = web_init('s1')
#    web_open(sel,'http://1.1.1.1')
#    res = checktitle(sel,'LoginTitle')
###################################################################################
def checktitle(sel, title):
    try:
        if sel.get_title() == title:
            return {'status': True, 'Message': 'Find title succesfully'}
        else:
            return {'status': False, 'Message': 'Can not find title ' + title + ' Please check'}
    except (NoSuchElementException, WebDriverException, Exception):
        return {'status': False, 'Message': 'fail to open url'}


################################################################################
# exportal_redirect_success :检查是否重定向到外置portal认证页面（适用于http连接）
#
# args:  
#      sel: 所初始化的web实例
#      url: 打开的网页
# return: 
#      res:重定向成功res=0
# examples:
#    sel = web_init('s1')
#    exportal_redirect_success(sel,'http://1.1.1.1')
###################################################################################		
def exportal_redirect_success(sel, url):
    res = 4
    if sel:
        resa = web_open(sel, url)
        if resa['status'] == True:
            resb = is_portal_page(sel)
            if resb['status'] == True and resb['Message'] == 'This page is Outer portal login page':
                res = 0
            else:
                res = 1
                print('sta redirect to external portal_login page failed!!!')
        else:
            res = 2
            print('web_open ' + url + ' failed!!!')
    else:
        res = 3
        print('web_init status false')
    return res


################################################################################
# inportal_redirect_success :检查是否重定向到内置portal认证页面（适用于http连接）
#
# args:
#      sel: 所初始化的web实例
#      url: 打开的网页
# return:
#      res:重定向成功res=0
# examples:
#    sel = web_init('s1')
#    inportal_redirect_success(sel,'http://1.1.1.1')
###################################################################################
def inportal_redirect_success(sel, url):
    res = 4
    if sel:
        resa = web_open(sel, url)
        if resa['status'] == True:
            resb = is_portal_page(sel)
            if resb['status'] == True and resb['Message'] == 'This page is Inner portal login page':
                res = 0
            else:
                res = 1
                print('sta redirect to internal portal_login page failed!!!')
        else:
            res = 2
            print('web_open ' + url + ' failed!!!')
    else:
        res = 3
        print('web_init status false')
    return res


################################################################################
# exportal_login_withcheck :检查外置portal是否登陆成功（适用于http连接）
#
# args:
#      sel: 所初始化的web实例
#      user:用户名
#      pwd: 密码
# return:
#      res:登陆成功res=0
# examples:
#    sel = web_init('s1')
#    exportal_redirect_success(sel,'http://1.1.1.1')
#    exportal_login_withcheck(sel,'aaa','111')
###################################################################################
def exportal_login_withcheck(sel, user, pwd):
    res = 1
    resa = portal_login(sel, user, pwd)
    if resa['status'] == True and resa['Message'] == 'Outer Portal login success':
        res = 0
    else:
        print(resa)
    return res


################################################################################
# inportal_login_withcheck :检查内置portal是否登陆成功（适用于http连接）
#
# args:
#      sel: 所初始化的web实例
#      user:用户名
#      pwd: 密码
# return:
#      res:登陆成功res=0
# examples:
#    sel = web_init('s1')
#    inportal_redirect_success(sel,'http://1.1.1.1')
#    inportal_login_withcheck(sel,'aaa','111')
###################################################################################
def inportal_login_withcheck(sel, user, pwd):
    res = 1
    resa = portal_login(sel, user, pwd)
    if resa['status'] == True and resa['Message'] == 'Inner Portal login success':
        res = 0
    else:
        print(resa)
    return res


################################################################################
# portal_logout_withcheck :检查内置/外置portal是否推出登陆（适用于http连接）
#
# args:
#      sel: 所初始化的web实例
# return:
#      res:登陆成功res=0
# examples:
#    sel = web_init('s1')
#    exportal_redirect_success(sel,'http://1.1.1.1')
#    exportal_login_withcheck(sel,'aaa','111')
#    portal_logout_withcheck(sel)
###################################################################################
def portal_logout_withcheck(sel):
    res = 1
    resa = portal_logout(sel)
    if resa != None:
        if resa['status'] == True:
            res = 0
        else:
            print(resa)
    return res


################################################################################
# open_url_withcheck :检查客户端是否正确打开网页（适用于http连接）
#
# args:
#      sel: 所初始化的web实例
#      url: 网址
# return:
#      res:登陆成功res=0
# examples:
#    sel = web_init('s1')
###################################################################################
def open_url_withcheck(sel, url, **args):
    res = 1
    resa = web_open(sel, url)
    if resa['status'] == True:
        if 'title' in args:
            title = args['title']
            resb = checktitle(sel, title)
            if resb['status'] == True:
                res = 0
            else:
                print(resb)
    else:
        print(resa)
    return res


################################下面函数适用于https连接###################################

##################################################################################
# newweb_init :初始化web实例，后续关于页面的操作均在此实例上进行(仅用于https连接时使用，避免弹出连接不安全页面）
#
# args:
#     host: 打开浏览器所在的设备
#     port(可选): selenium服务所监听的端口，默认为11918
#
# return:
#     webdriver实例
#
# addition:
#
# examples:
#    在S1上初始化浏览器实例
#    web = newweb_init('s1')
###################################################################################
def newweb_init(host, port='11999'):
    try:
        profile = webdriver.FirefoxProfile()
        profile.accept_untrusted_certs = True
        url = 'http://' + host + ':' + port + '/wd/hub'
        driver = webdriver.Remote(command_executor=url, desired_capabilities=DesiredCapabilities.FIREFOX,
                                  browser_profile=profile)
        return driver
    except (TimeoutException, Exception) as e:
        printRes(str({'status': False, 'Message': str(e)}))
        return None


##################################################################################
# newweb_open :打开页面(仅用于用例6.3.2https连接时使用，避免弹出连接不安全页面）
#
# args:  
#     driver: 所初始化的web实例
#     url: 打开的网址，如果不指定，则打开web_init初始化时的url
#     注意：如果是portal跳转，页面加载完毕也算打开OK，即当前页面不一定是url的页面
#
# return: 
#
# addition:
#
# examples:
#    sel = newweb_init('s1')
#    res = newweb_open(sel)
###################################################################################
def newweb_open(driver, url="/"):
    try:
        driver.get(url)
        return {'status': True, 'Message': 'Load Success!'}
    except (TimeoutException, Exception):
        return {'status': False, 'Message': 'Page NOT loaded in 30 seconds!'}


##################################################################################
# newis_innerportal_page:检查当前页面是内部portal页面（仅用于用例6.3.2https连接时使用，避免弹出连接不安全页面）
#
# args:
#     driver: 所初始化的web实例
#
# return:
#
# addition:
#
# examples:
#    sel = newweb_init('s1')
#    newweb_open(sel,'http://1.1.1.1')
#    res = newis_innerportal_page(sel)
###################################################################################
def newis_innerportal_page(driver):
    try:
        driver.find_element_by_name("p5")
        driver.find_element_by_name("p6")
        driver.find_element_by_name("Submit")
        return {'status': True, 'Message': 'This page is Inner portal login page'}
    except (NoSuchElementException, WebDriverException, Exception):
        return {'status': False, 'Message': 'Throw exception when execute is_portal_page'}


def is_outer_portal_page(driver):
    """
    检查当前页面是否为外部portal页面
    :param driver: 初始化的web实例
    :return: {'status': True, 'Message': 'This page is Extral portal login page'} or not
    """
    try:
        driver.find_element_by_id('username')
        driver.find_element_by_id('password')
        return {'status': True, 'Message': 'This page is Outer portal login page'}
    except (NoSuchElementException, WebDriverException, Exception):
        return {'status': False,
                'Message': 'In this page CAN NOT find id=username and/or id=password input element'}


##################################################################################
# newis_extralportal_page:检查当前页面是外部portal页面(适用于https连接）
#
# args:
#     driver: 所初始化的web实例
#
# return:
#
# addition:
#
# examples:
#    sel = newweb_init('s1')
#    newweb_open(sel,'http://1.1.1.1')
#    res = newis_extralportal_page(sel)
###################################################################################
def newis_extralportal_page(driver):
    try:
        elem1 = driver.find_element_by_id("username")
        elem2 = driver.find_element_by_id("password")
        return {'status': True, 'Message': 'This page is Extral portal login page'}
    except Exception:
        return {'status': False, 'Message': 'Throw exception when execute is_portal_page'}


##################################################################################
# newportal_login :登录portal页面（仅用于用例6.3.2https连接时使用，避免弹出连接不安全页面）
#
# args:  
#     driver: 所初始化的web实例
#     username: 登录使用的用户名
#     password: 登录使用的密码
#
# return: 
#
# addition:
#
# examples:
#    sel = newweb_init('s1')
#    newportal_login(sel,'user','passwd')
###################################################################################
def newportal_login(driver, username, password):
    try:
        elem1 = driver.find_element_by_name("p5")
        elem2 = driver.find_element_by_name("p6")
        elem1.clear()
        elem1.send_keys(username)
        elem2.clear()
        elem2.send_keys(password)
        elem3 = driver.find_element_by_name("Submit")
        elem3.click()
        time.sleep(15)
        driver.find_element_by_id("Submit")
        return {'status': True, 'Message': 'Inner Portal login successfully'}
    except (NoSuchElementException, WebDriverException, Exception):
        return {'status': False, 'Message': 'Warning: throw exception when run portal_login'}


def outer_portal_login(driver, username, password):
    try:
        user_element = driver.find_element_by_id('username')
        pwd_element = driver.find_element_by_id('password')
        user_element.clear()
        user_element.send_keys(username)
        pwd_element.clear()
        pwd_element.send_keys(password)
        submit_element = driver.find_element_by_id('login')
        submit_element.click()
        time.sleep(15)
        driver.find_element_by_name('logout')
        return {'status': True, 'Message': 'Outer Portal login successfully'}
    except (NoSuchElementException, WebDriverException, Exception):
        return {'status': False, 'Message': 'Warning: throw exception when run portal_login'}


def outer_portal_logout(driver):
    try:
        elem = driver.find_element_by_name("logout")
        elem.click()
        time.sleep(5)
        alert = driver.switch_to_alert()
        alert.accept()
        driver.close()
        return {'status': True, 'Message': 'Outer portal logout  successfully!'}
    except (NoSuchElementException, WebDriverException, Exception):
        return {'status': False, 'Message': 'Warning: throw exception when run portal_logout'}


##################################################################################
# newextportal_login :登录外置portal页面(适用于https连接）
#
# args:
#     driver: 所初始化的web实例
#     username: 登录使用的用户名
#     password: 登录使用的密码
#
# return:
#
# addition:
#
# examples:
#    sel = newweb_init('s1')
#    newextportal_login(sel,'user','passwd')
###################################################################################
def newextportal_login(driver, username, password):
    try:
        elem1 = driver.find_element_by_id("username")
        elem2 = driver.find_element_by_id("password")
        elem1.clear()
        elem1.send_keys(username)
        elem2.clear()
        elem2.send_keys(password)
        elem3 = driver.find_element_by_id("login")
        elem3.click()
        time.sleep(15)
        driver.find_element_by_name("logout")
        return {'status': True, 'Message': 'Extral Portal login successfully'}
    except Exception:
        return {'status': False, 'Message': 'Warning: throw exception when run portal_login'}


##################################################################################
# newportal_logout :登出portal页面,推出后自动关闭页面（仅用于用例6.3.2https连接时使用，避免弹出连接不安全页面）
#
# args:  
#     driver: 所初始化的web实例
#
# return: 
#
# addition:
#
# examples:
#    sel = newweb_init('s1')
#    newportal_login(sel,'user','passwd')
#    newportal_logout(sel)
###################################################################################
def newportal_logout(driver):
    try:
        elem = driver.find_element_by_id("Submit")
        elem.click()
        time.sleep(5)
        alert = driver.switch_to_alert()
        alert.accept()
        driver.close()
        return {'status': True, 'Message': 'Inner portal logout  successfully!'}
    except (NoSuchElementException, WebDriverException, Exception):
        return {'status': False, 'Message': 'Warning: throw exception when run portal_logout'}


################################################################################
# newextportal_logout :退出外置portal页面,推出后自动关闭页面(适用于https连接）
#
# args:  
#     driver: 所初始化的web实例
#
# return: 
#
# addition:
#
# examples:
#    sel = newweb_init('s1')
#    newextportal_login(sel,'user','passwd')
#    newextportal_logout(sel)
###################################################################################
def newextportal_logout(driver):
    try:
        elem = driver.find_element_by_name("logout")
        elem.click()
        time.sleep(5)
        alert = driver.switch_to_alert()
        alert.accept()
        driver.close()
        return {'status': True, 'Message': 'Outer portal logout  success!'}
    except Exception:
        return {'status': False, 'Message': 'Warning: throw exception when run portal_logout'}


################################################################################
# https_inportal_redirect_success :检查是否重定向到内置portal认证页面（适用于https连接）
#
# args:
#      sel: 所初始化的web实例
#      url: 打开的网页
# return:
#      res:重定向成功res=0
# examples:
#    sel = newweb_init('s1')
#    https_inportal_redirect_success(sel,'http://1.1.1.1')
###################################################################################
def https_inportal_redirect_success(sel, url):
    _res = 1
    if sel:
        _resa = newweb_open(sel, url)
        if _resa['status'] == True:
            _resb = newis_innerportal_page(sel)
            if _resb['status'] == True:
                _res = 0
            else:
                _res = 2
                print('is_internal_portal_page status false')
        else:
            _res = 3
            print('web_open', url, 'failed')
    else:
        _res = 4
        print('web_init status false')
    return _res


################################################################################
# https_inportal_login_withcheck :检查内置portal是否登陆成功（适用于https连接）
#
# args:
#      sel: 所初始化的web实例
#      user:用户名
#      pwd: 密码
# return:
#      res:登陆成功res=0
# examples:
#    sel = newweb_init('s1')
#    https_inportal_redirect_success(sel,'http://1.1.1.1')
#    https_inportal_login_withcheck(sel,'aaa','111')
###################################################################################
def https_inportal_login_withcheck(sel, user, pwd):
    _res = 1
    if sel:
        _resa = newportal_login(sel, user, pwd)
        if _resa['status'] == True:
            _res = 0
        else:
            print(_resa)
    return _res


################################################################################
# https_portal_logout_withcheck :检查内置/外置portal是否推出登陆（适用于https连接）
#
# args:
#      sel: 所初始化的web实例
#      user:用户名
#      pwd: 密码
# return:
#      res:登陆成功res=0
# examples:
#    sel = newweb_init('s1')
#    https_inportal_redirect_success(sel,'http://1.1.1.1')
#    https_inportal_login_withcheck(sel,'aaa','111')
#    https_portal_logout_withcheck(sel)
###################################################################################
def https_portal_logout_withcheck(sel):
    _res = 1
    if sel:
        _resa = newportal_logout(sel)
        if _resa['status'] == True:
            _res = 0
        else:
            _res = 1
            print(_resa)
    return _res
