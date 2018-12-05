# -*- coding: utf-8 -*-
from selenium import webdriver
import time
import requests
from PIL import Image
import os

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from selenium.webdriver import ActionChains

def vote(browser,qq,psw,idx):
    total = len(qq)
    count = 0
    for i in range(0,total):
        
        while True:
            browser.switch_to.default_content()

            try:
                wait = WebDriverWait(browser,2)
                wait.until(lambda browser: browser.find_element_by_xpath('//*[@id="loginIframe"]')) 
        
            except Exception,e:
                break
            
            browser.switch_to.frame('loginIframe')
            time.sleep(0.5)
            
            try:
                wait = WebDriverWait(browser,5)
                wait.until(lambda browser: browser.find_element_by_xpath('//*[@id="close"]')) 
        
            except Exception,e:
                print e
                os.system('pause')
            browser.find_element_by_xpath('//*[@id="close"]').click()
            time.sleep(1)

            try:
                browser.switch_to.default_content()
                time.sleep(1)
                browser.find_element_by_xpath('//*[@id="unlogin"]/a').click()
                time.sleep(3)
            except Exception,e:
                print e
                print '1'
                os.system('pause')

            
            time.sleep(1)
            flag = False
            try:
                wait = WebDriverWait(browser,2)
                wait.until(lambda browser: browser.find_element_by_xpath('//*[@id="loginIframe"]'))
                browser.switch_to.frame('loginIframe')
                time.sleep(1)
                wait.until(lambda browser: browser.find_element_by_xpath('//*[@id="switcher_plogin"]'))
                browser.find_element_by_xpath('//*[@id="switcher_plogin"]').click()
                
                wait.until(lambda browser: browser.find_element_by_xpath('//*[@id="u"]'))
                time.sleep(1)
                browser.find_element_by_xpath('//*[@id="u"]').clear()
                
                time.sleep(0.5)
                browser.find_element_by_xpath('//*[@id="u"]').send_keys(qq[i])
                time.sleep(1.5)
                browser.find_element_by_xpath('//*[@id="p"]').send_keys(psw[i])
                time.sleep(1.5)
                
                browser.find_element_by_xpath('//*[@id="login_button"]').click()
                
                wait = WebDriverWait(browser,2)
                wait.until(lambda browser: browser.find_element_by_xpath('//*[@id="newVcodeArea"]/div[1]/div/div[1]/a'))
                
                wait = WebDriverWait(browser,5)
                wait.until(lambda browser: browser.find_element_by_xpath('//*[@id="newVcodeIframe"]/iframe'))
                browser.switch_to.frame(browser.find_element_by_xpath('//*[@id="newVcodeIframe"]/iframe'))
                
                wait.until(lambda browser: browser.find_element_by_xpath('//*[@id="slideBkg"]'))
                flag = True
            except Exception,e:
                
                break
            while True:
                if flag == False:
                    break
                time.sleep(3)
                src = browser.find_element_by_xpath('//*[@id="slideBkg"]').get_attribute('src')
                distance = count_pos(src)
                distance = distance*240/680-12

                dragElement = browser.find_element_by_xpath('//*[@id="tcaptcha_drag_thumb"]')

                action_chains = ActionChains(browser)
                #action_chains.click_and_hold(dragElement).perform()
                action_chains.drag_and_drop_by_offset( dragElement, distance, 0 ).perform()
                time.sleep(5)
                try:
                    browser.find_element_by_xpath('//*[@id="e_reload"]')
                    time.sleep(3)
                except Exception,e:
                    break
                
        print u'登陆成功'    
        try:
            value = '62'
            Select(browser.find_element_by_xpath('//*[@id="area1ContentId_sg"]')).select_by_value(value)
            time.sleep(2)
            value = '5'
            Select(browser.find_element_by_xpath('//*[@id="areaContentId_sg"]')).select_by_value(value)
            time.sleep(5)
            if idx[i] == '1':
                Select(browser.find_element_by_xpath('//*[@id="roleContentId_sg"]')).select_by_index(0)
            else:
                Select(browser.find_element_by_xpath('//*[@id="roleContentId_sg"]')).select_by_index(1)
            time.sleep(5)
            browser.find_element_by_xpath('//*[@id="confirmButtonId_sg"]').click()
            time.sleep(3)
        except Exception,e:
            #print e
            pass
            
        
        browser.switch_to.default_content()
        time.sleep(1)
        browser.find_element_by_xpath('/html/body/div[1]/div[1]/div/div[2]/a[2]').click()
        try:
            wait = WebDriverWait(browser,5)
            wait.until(lambda browser: browser.find_element_by_xpath('//*[@id="SearchKey_508170"]'))

            value = 'sExtCharNine'
            Select(browser.find_element_by_xpath('//*[@id="SearchKey_508170"]')).select_by_value(value)
            time.sleep(1)
            name = '巜灬贝勒丶爷'#
            browser.find_element_by_xpath('//*[@id="SearchValue_508170"]').send_keys(name.decode('utf-8'))
            time.sleep(2)
            browser.find_element_by_xpath('/html/body/div[1]/div[3]/div/div[1]/a[3]').click()
            
            time.sleep(3)
        except Exception,e:
            print e
            print '4'
            os.system('pause')
        for i in range(0,3):
            browser.find_element_by_xpath('//*[@id="Work_List_Container_508170"]/a/div[1]').click()
            time.sleep(3)
            #os.system('pause')
            browser.find_element_by_xpath('//*[@id="vote"]').click()
            while True:
                try:
                    time.sleep(0.5)
                    alert = browser.switch_to_alert()
                    '''添加等待时间'''
                    time.sleep(1)
                    '''获取警告对话框的内容'''
                    print (alert.text)  #打印警告对话框内容
                    if alert.text.find(u'投票成功') != -1:
                        count = count + 1
                    alert.accept()   #alert对话框属于警告对话框，我们这里只能接受弹窗
                    '''添加等待时间'''
                    time.sleep(1)
                    browser.switch_to.default_content()
                    time.sleep(1)
                    break
                except Exception,e:
                    continue
            time.sleep(2)
            #browser.find_element_by_xpath('//*[@id="pop-detail"]/div/div[2]/a[2]').click()

        
        browser.find_element_by_xpath('//*[@id="lottery_start"]/div').click()
        while True:
            try:
                time.sleep(0.5)
                alert = browser.switch_to_alert()
                '''添加等待时间'''
                time.sleep(1)
                '''获取警告对话框的内容'''
                print (alert.text)  #打印警告对话框内容
                
                alert.accept()   #alert对话框属于警告对话框，我们这里只能接受弹窗
                '''添加等待时间'''
                time.sleep(1)
                browser.switch_to.default_content()
                time.sleep(1)
                break
            except Exception,e:
                continue
        
            
        browser.switch_to.default_content()
        time.sleep(1)
        browser.find_element_by_xpath('//*[@id="logined"]/a[1]').click()
        time.sleep(2)
        browser.find_element_by_xpath('//*[@id="unlogin"]/a').click()
        time.sleep(2)
        if count == 20:
            break
    print u'总计',count
    
            
                        

def diff_tuple(pixel0,pixel1):
    [x0,y0,z0] = pixel0
    [x1,y1,z1] = pixel1
    if abs(x0-x1)+abs(y0-y1)+abs(z0-z1) > 30:
        return True
    return False


def count_pos(src1):
    
    src0 = src1
    src0 = src0.replace('hycdn_1','hycdn_0',1)
    src0 = src0.replace('&fb=1&','&fb=0&',1)
    src0 = src0.replace('img_index=1','img_index=0',1)
    
    path1 = 'c:/pic/1.jpg'
    path0 = 'c:/pic/0.jpg'
    r = requests.request('get',src1) #获取网页
    #print(r.status_code)
    with open(path1,'wb') as f:  #打开写入到path路径里-二进制文件，返回的句柄名为f
        f.write(r.content)  #往f里写入r对象的二进制文件
    f.close()
    time.sleep(1)
    r = requests.request('get',src0) #获取网页
    #print(r.status_code)
    with open(path0,'wb') as f:  #打开写入到path路径里-二进制文件，返回的句柄名为f
        f.write(r.content)  #往f里写入r对象的二进制文件
    f.close()

    

    im0, im1 = Image.open(path0), Image.open(path1)
    width, height = im0.size
    posl = -1
    posr = -1
    for x in xrange(width):
        count = 0
        for y in xrange(height):
            if diff_tuple(im0.getpixel((x, y)) , im1.getpixel((x, y))):
                count = count + 1
        if count > 50:
            if posl == -1:
                posl = x
            else:
                posr = x
    return (posl+posr) / 2




if __name__ == "__main__":
    qq = []
    psw = []
    idx = []
    f = open('fight.txt')
    line = f.readline()
    while line:
        if len(line) < 10:
            line = f.readline()
            continue
        line = line.strip('\n')
        ss = line.split('----')
        qq.append(ss[0])
        psw.append(ss[1])
        idx.append(ss[2])
        
        line = f.readline()
    f.close()

    
    browser = webdriver.Chrome()

    browser.get("http://sg.qq.com/cp/a20181022bbxq/index.html")
    
    
    time.sleep(8)
    vote(browser,qq,psw,idx)



def unuse():
    try:
        # 显示等待，其中5的解释：5秒内每隔0.5毫秒扫描1次页面变化，直到指定的元素
        wait = WebDriverWait(driver, 5)
        wait.until(lambda driver: driver.find_element_by_id("content_left"))
        # 打印源代码
        print(driver.page_source)
    except TimeoutException:
        print("查询元素超时")
    finally:
        time.sleep(3)
        driver.close()

