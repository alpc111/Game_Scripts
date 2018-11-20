# -*- coding: gbk -*-
import win32api,win32gui,win32con #导入win32api相关模块
import time
import win32ui,win32process
import os
import thread
from PIL import Image
import struct
import ctypes
import sys
import commctrl
from ctypes import *
from os.path import join, dirname, abspath, exists
#win32gui.GetClassName(hwnd)
#win32gui.GetWindowText(hwnd)

people_addr = 0x106c834
click_addr = 0x1129490
mouse_addr = 0x1127270
login_addr = 0x104f2fc


dll = ctypes.windll.LoadLibrary(join(dirname(__file__),'dc.dll'))
class dcVerCode:
    #user QQ超人打码账号
    #pwd QQ超人打码密码
    #softId 软件ID 缺省为0,作者务必提交softId,已保证分成
    def __init__(self,user,pwd,softId="0"):
        self.user = user
        self.pwd = pwd
        self.softId = softId

    #获取账号剩余点数
    #成功返回剩余点数
    #返回"-1"----网络错误
    #返回"-5"----账户密码错误

    def getUserInfo(self):
        p = dll.GetUserInfo(self.user,self.pwd)
        if p:
            return ctypes.string_at(p,-1)
        return ''

    #解析返回结果,成功返回(验证码,验证码ID),失败返回错误信息
    #点数不足:Error:No Money!
    #账户密码错误:Error:No Reg!
    #上传失败，参数错误或者网络错误:Error:Put Fail!
    #识别超时:Error:TimeOut!
    #上传无效验证码:Error:empty picture!
    #账户或IP被冻结:Error:Account or Software Bind!
    #软件被冻结:Error:Software Frozen!
    def parseResult(self,result):
        list = result.split('|')
        if len(list)==3:
            return (list[0],list[2])
        return (result,'')

    #recByte 根据图片二进制数据识别验证码,返回验证码,验证码ID
    #buffer 图片二进制数据

    def recByte(self,buffer):
        p = dll.RecByte_A(buffer,len(buffer),self.user,self.pwd,self.softId)
        if p:
            str = ctypes.string_at(p,-1)
            return self.parseResult(str)
        return ''

    #recYZM 根据验证码路径识别,返回验证码,验证码ID
    #path 图片路径
    def recYZM(self,path):
        p = dll.RecYZM_A(path,self.user,self.pwd,self.softId)
        if p:
            str = ctypes.string_at(p,-1)
            return self.parseResult(str)
        return ''

    #reportErr 提交识别错误验证码
    #imageId 验证码ID
    def reportErr(self,imageId):
        dll.ReportError(self.user,imageId)

    #reportErr 提交识别错误验证码
    #返回"-1",提交失败,返回"1",提交成功
    def reportErrA(self,imageId):
        return  dll.ReportError_A(self.user,imageId)

def check_captch( hwnd ):

    # 返回句柄窗口的设备环境、覆盖整个窗口，包括非客户区，标题栏，菜单，边框
    hwndDC = win32gui.GetWindowDC(hwnd)
    # 创建设备描述表
    mfcDC  = win32ui.CreateDCFromHandle(hwndDC)

    # 创建内存设备描述表
    saveDC = mfcDC.CreateCompatibleDC()
    # 创建位图对象
    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, 1, 1)
    saveDC.SelectObject(saveBitMap)

    # 截图至内存设备描述表
    img_dc = mfcDC
    mem_dc = saveDC
    mem_dc.BitBlt((0, 0), (1, 1), img_dc, (446, 265), win32con.SRCCOPY)

    # 将截图保存到文件中
    #bmp_dir = '1.bmp'
    #saveBitMap.SaveBitmapFile(mem_dc, bmp_dir)
    # 获取位图信息
    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(0)
    if abs(bmpstr[0]+40) + abs(bmpstr[1]+96) + abs(bmpstr[2]-64) < 15:
        
        get_Sreen(hwnd)
        time.sleep(5)
        return True
    else:
        return False


def get_Sreen(hwnd):


    # 返回句柄窗口的设备环境、覆盖整个窗口，包括非客户区，标题栏，菜单，边框
    hwndDC = win32gui.GetWindowDC(hwnd)
    # 创建设备描述表
    mfcDC  = win32ui.CreateDCFromHandle(hwndDC)

    # 创建内存设备描述表
    saveDC = mfcDC.CreateCompatibleDC()
    # 创建位图对象
    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, 130, 50)
    saveDC.SelectObject(saveBitMap)

    # 截图至内存设备描述表
    img_dc = mfcDC
    mem_dc = saveDC
    mem_dc.BitBlt((0, 0), (130, 50), img_dc, (272, 251), win32con.SRCCOPY)

    # 将截图保存到文件中
    #bmp_dir = 'D:\\1\\'+pic_dir+'\\'+str(idx)+'.bmp'
    #saveBitMap.SaveBitmapFile(mem_dc, bmp_dir)
    # 获取位图信息
    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)
    # 生成图像
    im = Image.frombuffer('RGB',(bmpinfo['bmWidth'], bmpinfo['bmHeight']),
            bmpstr, 'raw', 'BGRX', 0, 1)
    im.save("1.png")
    #ss = saveBitMap.GetBitmapBits(0)

    #saveBitMap.SaveBitmapFile(mem_dc, bmp_dir)
    # 改变下行决定是否截图整个窗口，可以自己测试下
    #result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 1)
    #result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 0)

    
    client = dcVerCode("Avenger911","1qaz2wsx","0"); #超人打码帐号,超人打码密码,软件ID
    img = open('1.png','rb')
    buff = img.read()
    #img.close()

    #查询帐号余额
    #print (client.getUserInfo())

    #按图片字节数据识别
    yzm,imageId = client.recByte(buff)
    LClickAtPos( hwnd, 366, 307 )
    SendChi( hwnd, yzm )
    LClickAtPos( hwnd, 468, 291 )
    #print(yzm,imageId)

    #按图片本地路径识别
    #yzm,imageId = client.recYZM("image.png")
    #print ( yzm,imageId )




    # 内存释放
    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)




def _MyCallback_lh(hwnd,tmp):
    name = win32gui.GetClassName(hwnd)
    if name == 'TWINCONTROL':
        tmp.append(hwnd)
        
def _MyCallback_log(hwnd,tmp):
    name = win32gui.GetClassName(hwnd)
    if name == 'Qt4QWindowIcon':
        tmp.append(hwnd)

def _MyCallback(hwnd,tmp):
    name = win32gui.GetClassName(hwnd)
    if name == 'QQSGWinClass':
        tmp.append(hwnd)
          



#根据句柄、基址、偏移读取指定长度内存
def readmemory(hwnd,addr,bps,length):

    tmp = create_string_buffer(4)
    bytesRead = c_ulong(0)

    hreadID, processID = win32process.GetWindowThreadProcessId(hwnd)
    PROCESS = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS,0,processID)
    ReadProcessMemory(PROCESS.handle, addr, tmp, 4, byref(bytesRead))
    
    num = len(bps)
    if num == 0:
        return tmp
    
    for idx in range(0,num-1):
        addr_nxt = 0
        for x in tmp[::-1]:
            addr_nxt = addr_nxt*256+ord(x)
            
        #print hex(addr_nxt)
        
        ReadProcessMemory(PROCESS.handle, addr_nxt+bps[idx], tmp, 4, byref(bytesRead))
        
    addr_final = 0
    for x in tmp[::-1]:
        addr_final = addr_final*256+ord(x)

    #print hex(addr_final)
        
    ret = create_string_buffer(length)
    ReadProcessMemory(PROCESS.handle, addr_final+bps[num-1], ret, length, byref(bytesRead))
    
    return ret

def writememory(hwnd,addr,val):
    bytesWrite = c_ulong(0)

    count = c_ulong(0)
    length = len(val)
    c_data = c_char_p(val[count.value:])

    hreadID, processID = win32process.GetWindowThreadProcessId(hwnd)
    PROCESS = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS,0,processID)
    WriteProcessMemory(PROCESS.handle, addr, c_data, length, byref(bytesWrite))
    #print bytesWrite.value

#self='QQSGwinclass' #窗口的类名
#hwnd = win32gui.FindWindow(self,None)#通过窗口类名获取窗口句柄
#print hwnd
def LClickAtPos( hwnd, pos_x, pos_y ):
    pos = win32api.MAKELONG(pos_x, pos_y)
    win32gui.SendMessage(hwnd, win32con.WM_LBUTTONDOWN,win32con.MK_LBUTTON,pos)
    win32gui.SendMessage(hwnd, win32con.WM_LBUTTONUP,win32con.MK_LBUTTON,pos)
    time.sleep(0.5)

def LClickAtPos_Short( hwnd, pos_x, pos_y ):
    pos = win32api.MAKELONG(pos_x, pos_y)
    win32gui.SendMessage(hwnd, win32con.WM_LBUTTONDOWN,win32con.MK_LBUTTON,pos)
    win32gui.SendMessage(hwnd, win32con.WM_LBUTTONUP,win32con.MK_LBUTTON,pos)
    time.sleep(0.1)


def DClickAtPos( hwnd, pos_x, pos_y ):
    pos = win32api.MAKELONG(pos_x,pos_y)
    win32gui.PostMessage(hwnd, win32con.WM_LBUTTONDBLCLK,win32con.MK_LBUTTON,pos)
    time.sleep(0.5)

def RClickAtPos( hwnd, pos_x, pos_y ):
    pos = win32api.MAKELONG(pos_x, pos_y)
    win32gui.SendMessage(hwnd, win32con.WM_RBUTTONDOWN,win32con.MK_LBUTTON,pos)
    win32gui.SendMessage(hwnd, win32con.WM_RBUTTONUP,win32con.MK_LBUTTON,pos)
    time.sleep(0.5)

def KeyClick( hwnd, key ):
    win32api.SendMessage(hwnd, win32con.WM_KEYDOWN, key, 0)#发送按键
    win32api.SendMessage(hwnd, win32con.WM_KEYUP, key, 0)
    time.sleep(0.5)
def SetMousePos( hwnd, pos_x, pos_y ):
    val = chr(pos_x%256)+chr(pos_x/256)
    writememory(hwnd,mouse_addr,val)
    val = chr(pos_y%256)+chr(pos_y/256)
    writememory(hwnd,mouse_addr+4,val)
    time.sleep( 0.2 )

def SendChi( hwnd, Chiese ):
    total = len(Chiese)
    i = 0
    while i < total:
        if ord(Chiese[i]) <= 0x7f:
            win32api.SendMessage(hwnd ,win32con.WM_CHAR ,ord(Chiese[i]),0)
            i = i + 1
        else:
            chi_char = ord(Chiese[i])*256 + ord(Chiese[i+1]) 
            win32api.SendMessage(hwnd ,win32con.WM_IME_CHAR ,chi_char,0)
            i = i + 2
        time.sleep( 0.01 )
    time.sleep( 0.2 )

def RollBack( hwnd ):
    neg = win32api.MAKELONG(1,1)
    time.sleep(0.1)
    for count in range(0,200):
        win32gui.SendMessage(hwnd,win32con.WM_MOUSEWHEEL,neg,0)   #滚轮向上滚动
        time.sleep(0.01)
    time.sleep(0.5)
def get_name(hwnd):
    
    bps = [0xc,0x338,0x8888]            #昵称偏移
    name = readmemory(hwnd,people_addr,bps,28)
    ss = bytes('')
    for x in name:
        tmp = ord(x)
        if tmp == 0:
            break
        ss = ss + chr(tmp)
    #ss.decode('gbk')
    return ss

def base_get_name(hwnd):
    bps = [0x6c, 0x0]            #昵称偏移
    name = readmemory(hwnd,people_addr,bps,28)
    ss = bytes('')
    for x in name:
        tmp = ord(x)
        if tmp == 0:
            break
        ss = ss + chr(tmp)
    return ss

def FindSomething( hwnd, Something, Pos_x, LPos_y, HPos_y, Delta, Bps ):

    while True:
        pre_id = -1
        insert_pos = len(Bps)
        Bps.append(1),Bps.append(0x34),Bps.append(0x4)
        error_time = 0
        while True:
            LClickAtPos_Short( hwnd, Pos_x , LPos_y )
            time.sleep(0.1)
            bps = [0x574,0x244]            #找出当前点击物品的序号
            idx_hex = readmemory(hwnd,click_addr,bps,4)
            thing_name_idx = ord(idx_hex[1])*256 + ord(idx_hex[0])

            
            if thing_name_idx > 100000:
                error_time = error_time + 1
                if error_time > 200:
                    #print 'click_error',thing_name_idx,cur_click_y
                    print '点击错误超过150次'
                    return False, 0
            
                if LPos_y < HPos_y:
                    LPos_y = LPos_y + Delta
                else:
                    win32gui.SendMessage(hwnd,win32con.WM_MOUSEWHEEL,1,0)   #滚轮向下滚动
                    LClickAtPos_Short( hwnd, Pos_x, LPos_y )    
                continue
            
            Bps[insert_pos] = thing_name_idx * 4 + 0x18
            
            ret_name = readmemory(hwnd,people_addr,Bps,20)
            cur_name = bytes('')
            for x in ret_name:
                tmp = ord(x)
                if tmp == 0:
                    break
                cur_name = cur_name + chr(tmp)
            if cur_name == Something:
                return True, LPos_y
            if pre_id == thing_name_idx:
                error_time = error_time + 1
                if error_time > 200:
                    #print 'click_error',thing_name_idx,cur_click_y
                    print '滚动多次未找到'+Something
                    return False, 0
            
                if LPos_y < HPos_y:
                    LPos_y = LPos_y + Delta
                else:
                    win32gui.SendMessage(hwnd,win32con.WM_MOUSEWHEEL,1,0)   #滚轮向下滚动
                    LClickAtPos_Short( hwnd, Pos_x, LPos_y )    
                continue
            pre_id = thing_name_idx
            if LPos_y < HPos_y:
                LPos_y = LPos_y + Delta
            else:
                win32gui.SendMessage(hwnd,win32con.WM_MOUSEWHEEL,1,0)   #滚轮向下滚动
                LClickAtPos_Short( hwnd, Pos_x, LPos_y )

def send_something( hwnd, something, send_num ):

    while True:
        KeyClick( hwnd, win32con.VK_F4 )
        LClickAtPos( hwnd, 345, 175 )
        SetMousePos( hwnd, 416, 215 )
        RClickAtPos( hwnd, 416, 215 )
        LClickAtPos( hwnd, 472, 271 )

        SendChi( hwnd, something )
        LClickAtPos( hwnd, 400, 249 )
        SendChi( hwnd, something )

        LClickAtPos( hwnd, 533, 163 )
        LClickAtPos( hwnd, 261, 260 )
        RollBack( hwnd )
        bps = [ 0x38 ]
        flag, Pos_y = FindSomething( hwnd, something, 261, 260, 389, 43, bps )
        if flag:
            SetMousePos( hwnd, 261, Pos_y )

            DClickAtPos( hwnd, 261, Pos_y )
            DClickAtPos( hwnd, 208, Pos_y + 7 )
            Flag = True
            for _ in str(send_num):
                if ord(_) == ord('1') and Flag:
                    win32api.PostMessage(hwnd ,win32con.WM_KEYDOWN , ord(_), 0)
                    time.sleep(0.3)
                Flag = False
                win32api.PostMessage(hwnd ,win32con.WM_KEYDOWN , ord(_), 0)
                time.sleep(0.3)
            LClickAtPos( hwnd, 300, Pos_y + 10 )
            LClickAtPos( hwnd, 606, 404 )
            LClickAtPos( hwnd, 445, 480 )
            return True
        else:
            KeyClick( hwnd, win32con.VK_F4 )
            KeyClick( hwnd, win32con.VK_F4 )
            
def Goto_id_x_y( hwnd, map_id, pos_x, pos_y ):
    KeyClick( hwnd, win32con.VK_F4 )
    LClickAtPos( hwnd, 455, 461 )
    text = '/<DnpcWalkEx=' + str(map_id) + '|' + str(pos_x) \
                             + '|' + str(pos_y) + '>        /<>'
    #print text
    for x in text:
        win32api.SendMessage(hwnd ,win32con.WM_CHAR ,ord(x),0)
    time.sleep(0.5)

    LClickAtPos( hwnd, 339, 311 )

    LClickAtPos( hwnd, 446, 365 )
    KeyClick( hwnd, win32con.VK_F4 )

def auto_Gto(hwnd, map_id, des_x, des_y):
    Goto_id_x_y( hwnd, map_id, des_x, des_y )
    while True:
        time.sleep(4)
        bps = [ 0xC, 0x338, 0x8910 ]
        ret = readmemory( hwnd, people_addr, bps, 4 )
        hp = ord(ret[1]) * 256 + ord(ret[0])
        if hp == 0 :
            LClickAtPos( hwnd, 417, 383 )
            
        bps = [ 0xC, 0x18c ]
        ret = readmemory( hwnd, people_addr, bps, 4 )
        cur_map = ord( ret[1] ) * 256 + ord( ret[0] )
        
        bps = [ 0xC, 0x338, 0x18 ]
        ret = readmemory( hwnd, people_addr, bps, 4 )
        cur_x = ( ord( ret[1] ) * 256 + ord( ret[0] ) )

        
        bps = [ 0xC, 0x338, 0x44 ]
        ret = readmemory( hwnd, people_addr, bps, 4 )
        cur_y = ( ord( ret[1] ) * 256 + ord( ret[0] ) )
        if cur_map == map_id and abs(cur_x-des_x) <= 50 and abs(cur_y-des_y) <= 100:
            break
        else:
            bps = [ 0xC, 0x338, 0x228 ]
            ret = readmemory( hwnd, people_addr, bps, 4 )
            cur_state = ( ord( ret[1] ) * 256 + ord( ret[0] ) )
            if cur_state == 2 or cur_state == 20:
                Goto_id_x_y( hwnd, map_id, des_x, des_y )
def auto_repair( hwnd ):
    flag = False
    for i in range(0,12):
        equip_addr = 0
        bps = [ 0x38, 0x348 + i*0x4 ]
        ret = readmemory( hwnd, people_addr, bps, 4 )
        for _ in ret[::-1]:
            equip_addr = equip_addr * 256 + ord(_)
        if equip_addr == 0:
            continue
        bps = []
        ret = readmemory( hwnd, equip_addr + 0x2C, bps, 4 )
        _max = ord(ret[1]) * 256 + ord(ret[0])

        bps = []
        ret = readmemory( hwnd, equip_addr + 0x28, bps, 4 )
        _cur = ord(ret[1]) * 256 + ord(ret[0])
        if _max > 1000:
            if _cur < 1000:
                win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, ord('W'), 0)
                time.sleep(0.1)
                times = i/2
                pos_x = 202 if (i % 2)==0 else 362
                pos_y = times*42+145
                pos = win32api.MAKELONG(pos_x, pos_y)
                win32gui.SendMessage(hwnd, win32con.WM_LBUTTONDOWN,win32con.MK_LBUTTON,pos)
                win32gui.SendMessage(hwnd, win32con.WM_LBUTTONUP,win32con.MK_LBUTTON,pos)
                flag = True
        else:
            if _cur == 0:
                win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, ord('Q'), 0)
                time.sleep(0.1)
                times = i/2
                pos_x = 202 if (i % 2)==0 else 362
                pos_y = times*42+145
                pos = win32api.MAKELONG(pos_x, pos_y)
                win32gui.SendMessage(hwnd, win32con.WM_LBUTTONDOWN,win32con.MK_LBUTTON,pos)
                win32gui.SendMessage(hwnd, win32con.WM_LBUTTONUP,win32con.MK_LBUTTON,pos)
                flag = True
    if flag:
        KeyClick( hwnd, win32con.VK_F2)
        KeyClick( hwnd, win32con.VK_F2)


def check_Go(hwnd, map_id, des_x, des_y):
    Goto_id_x_y( hwnd, map_id, des_x, des_y )
    while True:
        time.sleep(4)
        bps = [ 0xC, 0x338, 0x8910 ]
        ret = readmemory( hwnd, people_addr, bps, 4 )
        hp = ord(ret[1]) * 256 + ord(ret[0])
        if hp == 0 :
            LClickAtPos( hwnd, 417, 383 )
            return -1
            
        bps = [ 0xC, 0x18c ]
        ret = readmemory( hwnd, people_addr, bps, 4 )
        cur_map = ord( ret[1] ) * 256 + ord( ret[0] )
        
        bps = [ 0xC, 0x338, 0x18 ]
        ret = readmemory( hwnd, people_addr, bps, 4 )
        cur_x = ( ord( ret[1] ) * 256 + ord( ret[0] ) )

        
        bps = [ 0xC, 0x338, 0x44 ]
        ret = readmemory( hwnd, people_addr, bps, 4 )
        cur_y = ( ord( ret[1] ) * 256 + ord( ret[0] ) )
        if cur_map == map_id and abs(cur_x-des_x) <= 50 and abs(cur_y-des_y) <= 100:
            return 0
        else:
            bps = [ 0xC, 0x338, 0x228 ]
            ret = readmemory( hwnd, people_addr, bps, 4 )
            cur_state = ( ord( ret[1] ) * 256 + ord( ret[0] ) )
            if cur_state == 2 or cur_state == 20:   # 0x20  攀爬
                Goto_id_x_y( hwnd, map_id, des_x, des_y )    

def back_877( hwnd ):
    while True:
        auto_Gto( hwnd,558,3000,1300 )
        win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_DOWN, 0)
        time.sleep(2)
        win32api.PostMessage(hwnd, win32con.WM_KEYUP, win32con.VK_DOWN, 0)
        win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_RIGHT, 0)
        time.sleep(1)
        win32api.PostMessage(hwnd, win32con.WM_KEYUP, win32con.VK_RIGHT, 0)
        win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_LEFT, 0)
        time.sleep(1)
        win32api.PostMessage(hwnd, win32con.WM_KEYUP, win32con.VK_LEFT, 0)
        win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_RIGHT, 0)
        time.sleep(1.5)
        win32api.PostMessage(hwnd, win32con.WM_KEYUP, win32con.VK_RIGHT, 0)
        
        status = check_Go( hwnd,558,3100,2200 )
        if status == -1:
            continue
        status = check_Go( hwnd,877,3970,1560 )
        if status == -1:
            continue
        
        LClickAtPos( hwnd, 330, 413 )
        break
        
def auto_fight( hwnd, map_id, L_x, R_x, Y, hwndlist, nxt_x, nxt_y ):
    des_x = (L_x + R_x) / 2
    des_y = Y
    checkhwnd = hwndlist[0]
    bps = [ 0xa8, 0x3c ]
    ret = readmemory( checkhwnd, people_addr, bps, 4 )
    pre_act = ord(ret[1])*256 + ord(ret[0])
    
    auto_Gto( hwnd, map_id, des_x, des_y )
    repair = 0
    total_act = 0
    
    while True:
        bps = [ 0xC, 0x338, 0x8910 ]
        ret = readmemory( hwnd, people_addr, bps, 4 )
        hp = ord(ret[1]) * 256 + ord(ret[0])
        if hp == 0 :
            LClickAtPos( hwnd, 417, 383 )
            auto_Gto( hwnd, map_id, des_x, des_y )
        need_wait = False
        for cur_hwnd in hwndlist:
            bps = [ 0xC, 0x338, 0x8910 ]
            ret = readmemory( cur_hwnd, people_addr, bps, 4 )
            cur_hp = ord(ret[1]) * 256 + ord(ret[0])
            if cur_hp == 0:
                LClickAtPos( cur_hwnd, 417, 383 )
                need_wait = True
                #thread.start_new_thread ( back_877, (cur_hwnd,) )
        if need_wait:
            auto_Gto( hwnd, 558, 3000, 1800 )
            auto_Gto( hwnd, 558, 2600, 1300 )
            time.sleep(300)
            for cur_hwnd in hwndlist:
                LClickAtPos( cur_hwnd, 417, 383 )
                thread.start_new_thread ( back_877, (cur_hwnd,) )
            bps = [ 0xa8, 0x3c ]
            ret = readmemory( checkhwnd, people_addr, bps, 4 )
            cur_act = ord(ret[1])*256 + ord(ret[0])
            total_act = cur_act - pre_act + total_act
            
            wait_every_one( hwndlist )
            auto_Gto( hwnd, map_id, des_x, des_y )
            bps = [ 0xa8, 0x3c ]
            ret = readmemory( checkhwnd, people_addr, bps, 4 )
            pre_act = ord(ret[1])*256 + ord(ret[0])


            
        win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_LEFT, 0)
        time.sleep(0.01)
        win32api.PostMessage(hwnd, win32con.WM_KEYUP, win32con.VK_LEFT, 0)
        win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_RIGHT, 0)
        time.sleep(0.01)
        win32api.PostMessage(hwnd, win32con.WM_KEYUP, win32con.VK_RIGHT, 0)
        
        win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, ord('A'), 0)
        win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, ord('F'), 0)
        win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, ord('C'), 0)
        
        bps = [ 0xa8, 0x3c ]
        ret = readmemory( checkhwnd, people_addr, bps, 4 )
        cur_act = ord(ret[1])*256 + ord(ret[0])
        if (cur_act - pre_act + total_act == 40) or (cur_act - pre_act + total_act == 80):
            break
        repair = repair + 1
        if repair == 20:
            repair = 0
            auto_repair( hwnd )
        else:
            time.sleep(0.2)
            
        bps = [ 0xC, 0x338, 0x44 ]
        ret = readmemory( hwnd, people_addr, bps, 4 )
        cur_y = ord(ret[1]) * 256 + ord(ret[0])

        bps = [ 0xc, 0x338, 0x18 ]
        ret = readmemory( hwnd, people_addr, bps, 4 )
        cur_x = ord(ret[1])*256 + ord(ret[0])
        if abs(cur_y - des_y) > 300 or abs(cur_x-des_x) > 800:
            LClickAtPos( hwnd, 417, 383 )
            auto_Gto( hwnd, map_id, des_x, des_y )
            
        flag = False
        while cur_x < L_x:
            LClickAtPos( hwnd, 417, 383 )
            bps = [ 0xc, 0x338, 0x18 ]
            ret = readmemory( hwnd, people_addr, bps, 4 )
            cur_x = ord(ret[1])*256 + ord(ret[0])
            win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_RIGHT, 0)
            time.sleep(0.05)
            flag = True
        if flag:
            win32api.PostMessage(hwnd, win32con.WM_KEYUP, win32con.VK_RIGHT, 0)
        flag = False
        while cur_x > R_x:
            LClickAtPos( hwnd, 417, 383 )
            bps = [ 0xc, 0x338, 0x18 ]
            ret = readmemory( hwnd, people_addr, bps, 4 )
            cur_x = ord(ret[1])*256 + ord(ret[0])
            win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_LEFT, 0)
            flag = False
            time.sleep(0.05)
        if flag:
            win32api.PostMessage(hwnd, win32con.WM_KEYUP, win32con.VK_LEFT, 0)

    auto_Gto( hwnd, map_id, nxt_x, nxt_y )

    bps = [ 0xa8, 0x3c ]
    ret = readmemory( checkhwnd, people_addr, bps, 4 )
    pre = ord(ret[1])*256 + ord(ret[0])
    for i in range(0,400):
        win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, ord('A'), 0)
        win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, ord('C'), 0)
        bps = [ 0xa8, 0x3c ]
        ret = readmemory( checkhwnd, people_addr, bps, 4 )
        cur = ord(ret[1])*256 + ord(ret[0])
        if (cur - pre == 30) or (cur - pre == 60):
            break
        time.sleep(0.4)
    
            

def auto_close_speak( hwnd ):
    LClickAtPos( hwnd, 6, 507 )
    LClickAtPos( hwnd, 68, 392 )
    LClickAtPos( hwnd, 68, 434 )
    LClickAtPos( hwnd, 68, 453 )
    LClickAtPos( hwnd, 68, 472 )
    LClickAtPos( hwnd, 68, 493 )
    LClickAtPos( hwnd, 68, 512 )
    LClickAtPos( hwnd, 68, 532 )
    LClickAtPos( hwnd, 68, 550 )

def logout( hwnd ):
    LClickAtPos( hwnd, 417, 383 )
    KeyClick( hwnd, win32con.VK_ESCAPE )
    KeyClick( hwnd, win32con.VK_ESCAPE )
    KeyClick( hwnd, ord('O') )
    time.sleep(1.5)
    LClickAtPos( hwnd, 717, 524 )
    LClickAtPos( hwnd, 435, 415 )
    time.sleep(4)
    KeyClick( hwnd, win32con.VK_ESCAPE )
    KeyClick( hwnd, win32con.VK_ESCAPE )
    KeyClick( hwnd, ord('O') )
    time.sleep(1.5)
    LClickAtPos( hwnd, 717, 524 )
    LClickAtPos( hwnd, 435, 415 )
    time.sleep(5)
    hreadID, processID = win32process.GetWindowThreadProcessId(hwnd)
    os.popen('taskkill /PID '+ str(processID) + ' /F')
    '''
    KeyClick( hwnd, win32con.VK_F7 )
    time.sleep(2)
    LClickAtPos( hwnd, 418, 249 )
    time.sleep(2)
    LClickAtPos( hwnd, 343, 365 )
    '''
def exit_game( hwnd ):
    KeyClick( hwnd, win32con.VK_F7 )
    LClickAtPos( hwnd, 418, 406 )
    LClickAtPos( hwnd, 343, 365 )

def log_in( hwnd, qq, pwd, idx, line ):
    bps = []
    ret = readmemory(hwnd,login_addr,bps,4)
    while ord(ret[0]) < 2:
        time.sleep(2)
        #print ord(ret[0])
        ret = readmemory(hwnd,login_addr,bps,4)
    if ord(ret[0]) == 3:
        LClickAtPos( hwnd, 468, 326 )
        LClickAtPos( hwnd, 566, 376 )
        LClickAtPos( hwnd, 384, 364 )
        LClickAtPos( hwnd, 696, 521 )
        
    posx = 455
    if line % 2 == 1:
        posx = 345
    posy = (line-1)/2*30 + 270
    DClickAtPos( hwnd, posx, posy )
    time.sleep(1)
    ret = readmemory(hwnd,login_addr,bps,4)

    while ord(ret[0]) != 3:
        time.sleep(3)
        DClickAtPos( hwnd, posx, posy )
        ret = readmemory(hwnd,login_addr,bps,4)
    while True:
        LClickAtPos( hwnd, 468, 326 )
        LClickAtPos( hwnd, 566, 376 )
        LClickAtPos( hwnd, 384, 364 )
        
        DClickAtPos( hwnd, 400, 282 )
        SendChi( hwnd,qq )
        LClickAtPos( hwnd, 400, 329 )
        SendChi( hwnd,pwd )
        LClickAtPos( hwnd, 390, 460 )
        time.sleep(5)
        ret = readmemory(hwnd,login_addr,bps,4)
        if ord(ret[0]) == 3:
            count = 0
            while check_captch( hwnd ) and count < 5:
                count = count + 1
                if count == 5:
                    os.system('pause')
                time.sleep(2)
                ret = readmemory(hwnd,login_addr,bps,4)
                if ord(ret[0]) != 3:
                    break
                
            ret = readmemory(hwnd,login_addr,bps,4)
            if ord(ret[0]) != 3:
                break
        else:
            break
    if idx == '1':
        DClickAtPos( hwnd, 680, 64 )
    elif idx == '2':
        DClickAtPos( hwnd, 680, 177 )
    else:
        DClickAtPos( hwnd, 680, 277 )
    time.sleep(1)
            
    
def change_id( hwnd, hwndlist, qq, pwd, idx, bp ):
    SetMousePos( hwnd, 42, 42 )
    RClickAtPos( hwnd, 42, 42 )
    LClickAtPos( hwnd, 70, 60 )
    for x in hwndlist:
        logout(x)
    time.sleep(3)
    for i in range(0,4):
        win32api.ShellExecute(0, 'open', r'C:\Program Files (x86)\落花黑屏2.177\QQSG.exe', '-.	','',1)
        time.sleep(15)
    time.sleep(10)
    curhwnd = []
    win32gui.EnumWindows(_MyCallback,curhwnd)
    while len(curhwnd) < 5:
        win32api.ShellExecute(0, 'open', r'C:\Program Files (x86)\落花黑屏2.177\QQSG.exe', '-.	','',1)
        time.sleep(15)
        curhwnd = []
        win32gui.EnumWindows(_MyCallback,curhwnd)
    hwndlist = []
    for x in curhwnd:
        if x != hwnd:
            hwndlist.append(x)
    #os.system('pause')
    time.sleep(10)
    bps = [ 0x28, 0x294 ]
    ret = readmemory(hwnd,people_addr,bps,4)
    cur_line = ord(ret[0])
    for i in range(0,4):
        log_in( hwndlist[i],qq[i+bp],pwd[i+bp],idx[i+bp],cur_line )
        time.sleep(5)
        bps = []
        ret = readmemory(hwndlist[i],login_addr,bps,4)
        while ord(ret[0]) != 6:
            log_in( hwndlist[i],qq[i+bp],pwd[i+bp],idx[i+bp],cur_line )
    return hwndlist

def close_start_pic( hwndlist ):
    for hwnd in hwndlist:
        KeyClick( hwnd, win32con.VK_F7 )
        KeyClick( hwnd, win32con.VK_F7 )
        LClickAtPos( hwnd, 663, 214 )
        LClickAtPos( hwnd, 343, 365 )
        
def make_team( hwnd, hwndlist ):
    LClickAtPos( hwnd, 417, 383 )
    time.sleep(5)
    for x in hwndlist:
        while True:
            ret = get_name(x)
            LClickAtPos( hwnd, 10, 520 )
        
            DClickAtPos( hwnd, 30, 575 )
            SendChi( hwnd, ret )
            LClickAtPos( hwnd, 165, 575 )
            text = '1'
            SendChi( hwnd, text )
            KeyClick( hwnd, win32con.VK_RETURN )
            time.sleep(2)
        
            SetMousePos( hwnd, 120, 450 )
            RClickAtPos( hwnd, 120, 450 )
            LClickAtPos( hwnd, 150, 390 )
            
            SetMousePos( hwnd, 120, 450 )
            RClickAtPos( hwnd, 120, 450 )
            LClickAtPos( hwnd, 150, 390 )
    
            time.sleep(2)
            LClickAtPos_Short( x, 517, 505 )
            LClickAtPos_Short( x, 340, 360 )
            LClickAtPos_Short( x, 475, 505 )
            LClickAtPos_Short( x, 340, 360 )
            LClickAtPos_Short( x, 428, 505 )
            LClickAtPos_Short( x, 340, 360 )
            LClickAtPos_Short( x, 386, 505 )
            LClickAtPos_Short( x, 340, 360 )
            LClickAtPos( x, 523, 101 )
            KeyClick( x, win32con.VK_ESCAPE )
            KeyClick( x, win32con.VK_ESCAPE )
            bps = [ 0x5C,0x08,-0x40 ]
            name = readmemory( hwnd, people_addr, bps, 28 )
            ss = bytes('')
            for _ in name:
                tmp = ord(_)
                if tmp == 0:
                    break
                ss = ss + chr(tmp)
            #print ss
            #print ret
            if ss == ret:
                break
            else:
                time.sleep(1)
        time.sleep(1)
    
def Read_Country( hwnd ):
    bps = [ 0xC, 0x338, 0x892c ]
    ret = readmemory( hwnd, people_addr, bps, 4 )
    return ord(ret[0])
def auto_go( hwnd ):
    Country = Read_Country( hwnd )
    if Country == 1:
        auto_Gto( hwnd, 113, 1980, 750 )
    elif Country == 2:
        auto_Gto( hwnd, 23, 1295, 1620 )
    else:
        auto_Gto( hwnd, 39, 2466, 1510 )
    time.sleep(1)
    while True:
        if Country == 1:
            KeyClick( hwnd, ord('G') )
            KeyClick( hwnd, win32con.VK_DOWN )
            KeyClick( hwnd, win32con.VK_RETURN )
            DClickAtPos( hwnd, 308, 391 )
        elif Country == 2:
            KeyClick( hwnd, ord('G') )
            KeyClick( hwnd, win32con.VK_DOWN )
            KeyClick( hwnd, win32con.VK_RETURN )
            DClickAtPos( hwnd, 308, 355 )
        else:
            KeyClick( hwnd, ord('G') )
            KeyClick( hwnd, win32con.VK_DOWN )
            KeyClick( hwnd, win32con.VK_RETURN )
            DClickAtPos( hwnd, 308, 355 )
        LClickAtPos( hwnd, 340, 359 )
        time.sleep(5)
        bps = [ 0xC, 0x18C ]
        ret = readmemory( hwnd, people_addr, bps, 4 )
        if ord(ret[0])+256*ord(ret[1]) == 849 :
            break
        else:
            LClickAtPos( hwnd, 195, 235 )
            LClickAtPos( hwnd, 495, 95 )
        
            
    time.sleep(5)
    while True:
        KeyClick( hwnd, ord('G') )
        KeyClick( hwnd, win32con.VK_DOWN )
        KeyClick( hwnd, win32con.VK_RETURN )
        DClickAtPos( hwnd, 308, 430 )
        LClickAtPos( hwnd, 340, 359 )
        time.sleep(5)
        bps = [ 0xC, 0x18C ]
        ret = readmemory( hwnd, people_addr, bps, 4 )
        if ord(ret[0])+256*ord(ret[1]) == 864 :
            break
        else:
            LClickAtPos( hwnd, 195, 235 )
            LClickAtPos( hwnd, 495, 95 )
        
    time.sleep(5)
    
    back_877( hwnd )
    
        
def wait_every_one( hwndlist ):
    while True:
        flag = True
        for x in hwndlist:
            bps = [ 0xC, 0x338, 0x228 ]
            ret = readmemory( x, people_addr, bps, 4 )
            cur_state = ( ord( ret[1] ) * 256 + ord( ret[0] ) )
            bps = [ 0xC, 0x18C ]
            ret = readmemory( x, people_addr, bps, 4 )
            if ord(ret[0])+256*ord(ret[1]) != 877 or cur_state != 2:
                flag = False
        if flag:
            break
        time.sleep(5)

def Do_RC( hwnd ):

    cur_hwnd = win32gui.FindWindowEx(hwnd,0,'_EL_HyperLinker','刷新列表')
    win32gui.PostMessage(cur_hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, 0)
    time.sleep(0.2)
    win32gui.PostMessage(cur_hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, 0)
    time.sleep(2)
    
    cur_hwnd = win32gui.FindWindowEx(hwnd,0,'_EL_HyperLinker','全部启动')
    win32gui.PostMessage(cur_hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, 0)
    time.sleep(0.2)
    win32gui.PostMessage(cur_hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, 0)
    time.sleep(0.2)

def Stop_RC( hwnd ):

    cur_hwnd = win32gui.FindWindowEx(hwnd,0,'Button','桃园/抚琴')
    win32gui.PostMessage(cur_hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, 0)
    time.sleep(0.2)
    win32gui.PostMessage(cur_hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, 0)
    time.sleep(0.2)
    
    cur_hwnd = win32gui.FindWindowEx(hwnd,0,'_EL_HyperLinker','刷新列表')
    win32gui.PostMessage(cur_hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, 0)
    time.sleep(0.2)
    win32gui.PostMessage(cur_hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, 0)
    time.sleep(0.2)
    
    cur_hwnd = win32gui.FindWindowEx(hwnd,0,'_EL_HyperLinker','全部停止')
    win32gui.PostMessage(cur_hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, 0)
    time.sleep(0.2)
    win32gui.PostMessage(cur_hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, 0)
    time.sleep(0.2)


        
def auto_get( hwnd, hwndlist, qq, pwd, idx ):
    
    auto_Gto( hwnd, 877, 3400, 1500 )
    make_team(hwnd, hwndlist)
    for x in hwndlist:
        thread.start_new_thread ( auto_go, (x,) )
    auto_Gto( hwnd, 558, 3000, 1800 )
    auto_Gto( hwnd, 558, 2600, 1300 )
    wait_every_one( hwndlist )
    
    #auto_fight( hwnd, 877, 800, 1600, 300, hwndlist, 3500, 1200 )
    auto_fight( hwnd, 877, 1700, 2100, 1200, hwndlist,100, 1400 )
    auto_Gto( hwnd, 877, 2500, 1400 )
    auto_Gto( hwnd, 877, 3400, 1500 )
    
    for i in range(0,4,4):
        hwndlist = change_id( hwnd, hwndlist, qq, pwd, idx, i )
        time.sleep(30)
        close_start_pic( hwndlist )
        make_team(hwnd, hwndlist)
        for x in hwndlist:
            thread.start_new_thread ( auto_go, (x,) )
        auto_Gto( hwnd, 558, 3000, 1800 )
        auto_Gto( hwnd, 558, 2600, 1300 )
        wait_every_one( hwndlist )
        
        auto_fight( hwnd, 877, 1700, 2100, 1200, hwndlist,100, 1400 )
        auto_Gto( hwnd, 877, 2500, 1400 )
        auto_Gto( hwnd, 877, 3400, 1500 )
        auto_repair(hwnd)
    
    for i in range(4,36,4):
        hwndlist = change_id( hwnd, hwndlist, qq, pwd, idx, i )
        time.sleep(30)
        close_start_pic( hwndlist )
        make_team(hwnd, hwndlist)
        for x in hwndlist:
            thread.start_new_thread ( auto_go, (x,) )
        auto_Gto( hwnd, 558, 3000, 1800 )
        auto_Gto( hwnd, 558, 2600, 1300 )
        wait_every_one( hwndlist )
        
        auto_fight( hwnd, 877, 800, 1600, 300, hwndlist, 3500, 1200 )
        auto_Gto( hwnd, 877, 2500, 1400 )
        auto_Gto( hwnd, 877, 3400, 1500 )
        auto_repair(hwnd)
        

    for x in hwndlist:
        KeyClick( x, ord('O') )
        LClickAtPos( x, 717, 524 )
    for x in hwndlist:
        exit_game(x)
        
    #send_something( hwnd, '回城符', 1 )
    exit_game( hwnd )
    
    time.sleep(100)
    
    get_prepare()
    #KeyClick( hwnd, ord('O') )
    #LClickAtPos( hwnd, 717, 524 )
    
    time.sleep(10)
    
    check_lh_state()
    
def use_auto_log():

    control_win = []
    win32gui.EnumWindows(_MyCallback_log,control_win)
    hwnd = control_win[0]
    for i in range(0,3):
        cur_hwnd = win32gui.FindWindowEx(hwnd,0,'_EL_HyperLinker','刷新状态')
        win32gui.PostMessage(cur_hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, 0)
        time.sleep(0.2)
        win32gui.PostMessage(cur_hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, 0)
        time.sleep(0.2)
        time.sleep(3)
    
    cur_hwnd = win32gui.FindWindowEx(hwnd,0,'_EL_HyperLinker','选中启动')
    win32gui.PostMessage(cur_hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, 0)
    time.sleep(0.2)
    win32gui.PostMessage(cur_hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, 0)
    time.sleep(0.2)

def get_prepare():


    use_auto_log()
    while True:
        time.sleep(70)
        windows = []
        win32gui.EnumWindows(_MyCallback,windows)
        num = 0
        for x in windows:
            if get_name(x) != '':
                num = num + 1
        if num < 6:
            use_auto_log()
        else:
            break


def readListViewItems(hwnd, column_index=0):
    
    GetWindowThreadProcessId = ctypes.windll.user32.GetWindowThreadProcessId
    VirtualAllocEx = ctypes.windll.kernel32.VirtualAllocEx
    VirtualFreeEx = ctypes.windll.kernel32.VirtualFreeEx
    OpenProcess = ctypes.windll.kernel32.OpenProcess
    WriteProcessMemory = ctypes.windll.kernel32.WriteProcessMemory
    ReadProcessMemory = ctypes.windll.kernel32.ReadProcessMemory
    memcpy = ctypes.cdll.msvcrt.memcpy
    # Allocate virtual memory inside target process
    pid = ctypes.create_string_buffer(4)
    p_pid = ctypes.addressof(pid)
    GetWindowThreadProcessId(hwnd, p_pid) # process owning the given hwnd
    hProcHnd = OpenProcess(win32con.PROCESS_ALL_ACCESS, False, struct.unpack("i",pid)[0])
    pLVI = VirtualAllocEx(hProcHnd, 0, 128, win32con.MEM_RESERVE|win32con.MEM_COMMIT, win32con.PAGE_READWRITE)
    pBuffer = VirtualAllocEx(hProcHnd, 0, 128, win32con.MEM_RESERVE|win32con.MEM_COMMIT, win32con.PAGE_READWRITE)
  
    # Prepare an LVITEM record and write it to target process memory
    lvitem_str = struct.pack('iiiiiiiii', *[0,0,column_index,0,0,pBuffer,128,0,0])
    lvitem_buffer = ctypes.create_string_buffer(lvitem_str)
    copied = ctypes.create_string_buffer(4)
    p_copied = ctypes.addressof(copied)
    WriteProcessMemory(hProcHnd, pLVI, ctypes.addressof(lvitem_buffer), ctypes.sizeof(lvitem_buffer), p_copied)
  
    # iterate items in the SysListView32 control
    num_items = win32gui.SendMessage(hwnd, commctrl.LVM_GETITEMCOUNT)
    item_texts = []
    for item_index in range(num_items):
        win32gui.SendMessage(hwnd, commctrl.LVM_GETITEMTEXT, item_index, pLVI)
        target_buff = ctypes.create_string_buffer(128)
        ReadProcessMemory(hProcHnd, pBuffer, ctypes.addressof(target_buff), 128, p_copied)
        item_texts.append(target_buff.value)
  
    VirtualFreeEx(hProcHnd, pBuffer, 0, win32con.MEM_RELEASE)
    VirtualFreeEx(hProcHnd, pLVI, 0, win32con.MEM_RELEASE)
    win32api.CloseHandle(hProcHnd)
    return item_texts

def check_lh_state():
    
    control_win = []
    win32gui.EnumWindows(_MyCallback_lh,control_win)
    hwnd = control_win[0]
    
    Do_RC( hwnd )
    time.sleep(30)
    
    des_hwnd = win32gui.FindWindowEx(hwnd,0,'SysListView32',None)
    
    while True:
        Flag = True
        state = readListViewItems(des_hwnd,4)
        for x in state:
            if x[0]+x[1] == '原':
                Flag = False
                break
        if Flag:
            break
        Stop_RC( hwnd )
        time.sleep(5)
        Do_RC( hwnd )
        time.sleep(30)

if __name__ == "__main__":
    windows = []
    win32gui.EnumWindows(_MyCallback,windows)

    
    kernel32 = windll.LoadLibrary("kernel32.dll")
    ReadProcessMemory = kernel32.ReadProcessMemory
    WriteProcessMemory = kernel32.WriteProcessMemory
    
    name = '0000星星000'
    namelist = [ '蛋丶1830', '蛋丶2859', '蛋丶6227', '蛋丶9085' ]
    #namelist = [ '丩日光倾城', '丷失她失心', '乁残阳抹壁画', '讠暖风处' ]
    
    '''
    while True:
       now = datetime.datetime.now()
       if now.hour == 9 and now.minute == 0:
           break
       time.sleep(25)
    '''
    qq = []
    pwd = []
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
        pwd.append(ss[1])
        idx.append(ss[2])
        
        line = f.readline()
    f.close()

    nameecp = '妖丶2703'
    fighter= 0
    hwndlist = []
    ecphwnd=0
    for x in windows:
        ret = get_name(x)
        if ret == name:
            fighter = x
        if ret == nameecp:
            ecphwnd = x
        for y in namelist:
            if ret == y:
                hwndlist.append(x)

    hwndlist = []
    
    
    for x in windows:
        if x!=fighter and x != ecphwnd:
            hwndlist.append(x)
    
    '''
    while True:
        localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        if localtime == '2018-03-27 00:11:00':
            break
        time.sleep(0.5)
    '''
    if fighter == 0 or len(hwndlist) != 4:
        exit(0)
    print 'start'
    auto_close_speak( fighter )
    auto_get( fighter, hwndlist, qq, pwd, idx )
    #auto_fight( fighter, 877, 1700, 2100, 1200, fighter, 100, 1400 )
    #auto_fight( fighter, 877, 800, 1600, 300, hwndlist[0], 3500, 1200 )
