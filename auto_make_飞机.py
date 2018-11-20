# -*- coding: gbk -*-
import win32api,win32gui,win32con #导入win32api相关模块
import time
import win32ui,win32process
import os 
from ctypes import *
#from PIL import Image

#win32gui.GetClassName(hwnd)
#win32gui.GetWindowText(hwnd)

people_addr = 0x106c834
click_addr = 0x1129490
mouse_addr = 0x1127270

global nameOfmake

def get_pos():
    while True:
        (x,y) = win32gui.GetCursorPos()
        print (x-560,y-209)
        time.sleep(1)


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
        #time.sleep( 0.1 )
    time.sleep( 0.2 )

def RollBack( hwnd ):
    neg = win32api.MAKELONG(1,1)
    time.sleep(0.1)
    for count in range(0,200):
        win32gui.SendMessage(hwnd,win32con.WM_MOUSEWHEEL,neg,0)   #滚轮向上滚动
        time.sleep(0.01)
    time.sleep(0.5)

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

            if thing_name_idx > 60000:
                
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

def get_name(hwnd):
    
    bps = [0xc,0x338,0x8888]            #昵称偏移
    name = readmemory(hwnd,people_addr,bps,28)
    ss = bytes('')
    for x in name:
        tmp = ord(x)
        if tmp == 0:
            break
        ss = ss + chr(tmp)
    return ss

def get_thing_num ( hwnd,thing ):      #获取背包中名为thing的物品的个数和该物品序号 不存在返回0,0
    idx = 0
    pre = 0
    for i in range(0,70):
        addr = 0
        bps = [ 0x38, i*4 + 0x14 ]
        ret = readmemory(hwnd,people_addr,bps,4)
        for x in ret[::-1]:
            addr = addr * 256 + ord(x)
        if addr == 0:
            continue
        bps = [ 0x4 ]

        ret_name = readmemory(hwnd,addr + 0x34,bps,20)
        
        cur_name = bytes('')
    
        for x in ret_name:
            tmp = ord(x)
            if tmp == 0:
                break
            cur_name = cur_name + chr(tmp)

        if cur_name == thing:
            bps = [  ]  #找出背包第x个物品的名字
            ret = readmemory(hwnd,addr + 0x28, bps, 4)
            num = 0
            for x in ret[::-1]:
                num = num*256+ord(x)
            return num, addr
    return 0, 0

def get_thingAtAddr_num( hwnd,addr ):
    
    bps = [  ]
    val = readmemory(hwnd,addr + 0x28,bps,4)
    ret = 0
    for x in val[::-1]:
        ret = ret * 256 + ord(x)
    #print ret,idx
    return ret

def rev_things( hwnd ):     #一键接收邮件中的物品
    KeyClick( hwnd, win32con.VK_F6 )
    LClickAtPos( hwnd, 404, 424 )
    LClickAtPos( hwnd, 508, 428 )
    
    time.sleep(10)

    KeyClick( hwnd, win32con.VK_F6 )
    KeyClick( hwnd, win32con.VK_RETURN )
    LClickAtPos( hwnd, 775, 206 )

def buy_something_AtGroup( hwnd, something, buy_num ):  #自动购买军团物品


    while True:
        num, addr = get_thing_num( hwnd, something )
        tar_num = buy_num
        buy_num = buy_num - num
        
        if buy_num <= 0:
            return
        
        KeyClick( hwnd, ord('O') )
        LClickAtPos( hwnd, 263, 117 )
        LClickAtPos( hwnd, 260, 533 )

        bps = [ 0x28, 0x488 ]
        flag, Pos_y = FindSomething( hwnd, something, 158, 272, 510, 119, bps )
        
        if flag:
            SetMousePos( hwnd, 158, Pos_y )

            DClickAtPos( hwnd, 158, Pos_y )
            time.sleep( 0.5 )
            for x in str(buy_num):
                win32api.PostMessage(hwnd ,win32con.WM_KEYDOWN , ord(x), 0)
                #win32api.PostMessage(hwnd, win32con.WM_KEYUP, ord(x), 0)
                time.sleep(0.15)
                
            LClickAtPos( hwnd, 204, Pos_y + 10 )
            LClickAtPos( hwnd, 474, 522 )
            KeyClick( hwnd, win32con.VK_F6 )
            KeyClick( hwnd, win32con.VK_F6 )
            num, addr = get_thing_num( hwnd, something )
            if num == tar_num:
                return
            else:
                continue
        else:
            stop( hwnd )
            KeyClick( hwnd, ord('O') )
            KeyClick( hwnd, ord('O') )
            #print '购买' + something + '失败'

def buy_something_Atbusiness( hwnd, something, buy_num ):

    while True:
        num, addr = get_thing_num( hwnd, something )
        
        tar_num = buy_num
        buy_num = buy_num - num
        
        if buy_num <= 0:
            return

        KeyClick( hwnd, ord('G') )
        KeyClick( hwnd, win32con.VK_DOWN )
        KeyClick( hwnd, win32con.VK_RETURN )
        
        LClickAtPos( hwnd, 229, 257 )
        RollBack( hwnd )
        bps = [ 0x8, 0xa90 ]
        flag, Pos_y = FindSomething( hwnd, something, 227, 260, 518, 43, bps )
        
        if flag:
            SetMousePos( hwnd, 227, Pos_y )

            DClickAtPos( hwnd, 227, Pos_y )
            for x in str(buy_num):
                win32api.PostMessage(hwnd ,win32con.WM_KEYDOWN , ord(x), 0)
                #win32api.PostMessage(hwnd, win32con.WM_KEYUP, ord(x), 0)
                time.sleep(0.15)
                
            LClickAtPos( hwnd, 277, Pos_y + 20 )
            LClickAtPos( hwnd, 603, 545 )
            LClickAtPos( hwnd, 387, 363 )
            KeyClick( hwnd, win32con.VK_ESCAPE )
            num, addr = get_thing_num( hwnd, something )
            if num == tar_num:
                return
            else:
                continue
        else:
            KeyClick( hwnd, win32con.VK_ESCAPE )
        
def send_something( hwnd, something, send_num ):

    while True:
        KeyClick( hwnd, win32con.VK_F4 )
        LClickAtPos( hwnd, 285, 174 )
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
            LClickAtPos( hwnd, 300, Pos_y + 10 )
            LClickAtPos( hwnd, 606, 404 )
            LClickAtPos( hwnd, 445, 480 )
            return True
        else:
            KeyClick( hwnd, win32con.VK_F4 )
            KeyClick( hwnd, win32con.VK_F4 )
    
    
    
def stop( hwnd ):
    KeyClick( hwnd, win32con.VK_F6 )

    KeyClick( hwnd, win32con.VK_F6 )


def find_something( hwnd,thing_name ):
    KeyClick( hwnd, win32con.VK_F2 )
    LClickAtPos( hwnd, 535, 518 )
    SendChi( hwnd,thing_name )
    KeyClick( hwnd, win32con.VK_RETURN )
    

def throw_something( hwnd, something, thing_num ):
    KeyClick( hwnd, win32con.VK_F2 )
    for x in something:
        while True:
            LClickAtPos( hwnd, 532, 185 )
            RollBack( hwnd )
            bps = [ 0x38 ]
            flag, Pos_y = FindSomething( hwnd, x, 532, 185, 455, 45, bps )
            if flag == True:
                RClickAtPos( hwnd, 532, Pos_y )
                LClickAtPos( hwnd, 587, Pos_y+35 )
                SetMousePos( hwnd, 331, 361 )
                LClickAtPos( hwnd, 331, 361 )
                for _ in str(thing_num):
                    win32api.PostMessage(hwnd ,win32con.WM_KEYDOWN , ord(_), 0)
                    time.sleep(0.15)
                
                #LClickAtPos( hwnd, 397, 400 )
                LClickAtPos( hwnd, 383, 366 )
                LClickAtPos( hwnd, 614, 517 )
                break
    KeyClick( hwnd, win32con.VK_F2 )

def backTo_Group( hwnd ):
    KeyClick( hwnd, ord('O') )
    LClickAtPos( hwnd, 718, 524 )
    time.sleep(2)



def binary_search( hwnd, make_idx, bps ):
    ret = readmemory(hwnd,people_addr,bps,4)
    cur_addr = 0
    for x in ret[::-1]:
        cur_addr = cur_addr * 256 + ord(x)
        
    bps = []
    ret = readmemory(hwnd,cur_addr+0xC,bps,4)
    cur_id = 0
    for x in ret[::-1]:
        cur_id = cur_id * 256 + ord(x)
    while cur_id != make_idx:
        if cur_id < make_idx:
            ret = readmemory(hwnd,cur_addr+0x8,bps,4)
        else:
            ret = readmemory(hwnd,cur_addr,bps,4)
        cur_addr = 0
        for x in ret[::-1]:
            cur_addr = cur_addr * 256 + ord(x)
        ret = readmemory(hwnd,cur_addr+0xC,bps,4)
        cur_id = 0
        for x in ret[::-1]:
            cur_id = cur_id * 256 + ord(x)
    return cur_addr

def find_material( hwnd, make_idx ):

    things_name = []
    things_num = []
    things_id = []
    bps = [ 0x24, 0x40, 0x8, 0x4 ]
    make_addr = binary_search( hwnd, make_idx, bps )
    
    for i in range(0,3):
        bps = [ 0x80 + i*0x4 ]

        _id = 0
        ret = readmemory(hwnd,make_addr + 0x10,bps,4)
        for x in ret[::-1]:
            _id = _id * 256 + ord(x)

        bps[0] = 0x8c + i * 0x4

        _num = 0
        ret = readmemory(hwnd,make_addr + 0x10,bps,4)
        for x in ret[::-1]:
            _num = _num * 256 + ord(x)
        if _id != 0:
            bps = [ 0x24, 0x14, 0x8, 0x4 ]
            cur_addr = binary_search( hwnd, _id, bps )
            
            bps = [ 0x4 ]
            
            ret_name = readmemory(hwnd, cur_addr + 0x10, bps,20)
            
            cur_name = bytes('')
    
            for x in ret_name:
                tmp = ord(x)
                if tmp == 0:
                    break
                cur_name = cur_name + chr(tmp)
            things_name.append( cur_name )
            things_num.append( _num )
            things_id.append( _id )
    return things_name, things_num, things_id



def make( hwnd ,thing, easy ):

    global nameOfmake
    
    KeyClick( hwnd, ord('K') )
    LClickAtPos( hwnd, 489, 139 )
    LClickAtPos( hwnd, 379, 247 )
    if easy == False:
        RollBack( hwnd )

    make_idx = -1

    click_pos = [244,283,318,352,386,420]
    cur_click_y = 0
    flag = True
    while True:
        LClickAtPos_Short( hwnd, 355, click_pos[cur_click_y] )
        
        bps = [0x574,0x244]            #找出当前点击物品的制造序号
        idx_hex = readmemory(hwnd,click_addr,bps,4)
        thing_name_idx = 0
        for x in idx_hex[::-1]:
            thing_name_idx = thing_name_idx*256+ord(x)
    
        if thing_name_idx > 10000:
            print 'click_error'
            flag = False
            break
        
        '''
        bps = [ thing_name_idx*32+48 , 0x4 ] #找出当前点击物品的名字
        ret_name = readmemory(hwnd,make_things_addr,bps,20)
        
        cur_name = bytes('')
    
        for x in ret_name:
            tmp = ord(x)
            if tmp == 0:
                break
            cur_name = cur_name + chr(tmp)
        '''
        if nameOfmake[thing_name_idx] == thing:
            make_idx = thing_name_idx
            break
        if cur_click_y < 5:
            cur_click_y = cur_click_y + 1
        else:
            win32gui.SendMessage(hwnd,win32con.WM_MOUSEWHEEL,1,0)   #滚轮向下滚动
    time.sleep(0.5)
    if flag == True:
        DClickAtPos( hwnd, 355, click_pos[cur_click_y] )

        LClickAtPos( hwnd, 422, 306 )
        LClickAtPos( hwnd, 488, 323 )

    else:
        KeyClick( hwnd, ord('K') )
        print thing + '制作失败'
        os.system('pause')
    return make_idx

def auto_make_Atbusiness( hwnd, things_name, things_num ):
    total = len( things_name )
    for _ in range(0,total):
        stop( hwnd )
        _id = 0
        num, addr = get_thing_num( hwnd, things_name[_] )
        if num < things_num[_]:
            print '准备制造' + things_name[_] + ',当前数量为 ' + str(num)
            _id = make( hwnd, things_name[_], False )
            m_things_name, m_things_num, m_id = find_material( hwnd, _id )
            
            pre_num = 0
            while num < things_num[_]:
                time.sleep(4)
                if addr == 0:
                    num, addr = get_thing_num( hwnd, things_name[_] )
                else:
                    num = get_thingAtAddr_num( hwnd, addr )
                        
                if num == pre_num:
                    stop( hwnd )
                    rev_things( hwnd )

                    need_num = things_num[_] - num
                    
                    m_total = len(m_things_name)
                    for i in range(0,m_total):
                        m_num, m_addr = get_thing_num(hwnd,m_things_name[i])
                        if m_num < m_things_num[i]:
                            if m_id[i] > 1800 and m_id[i] <= 1975:
                                tmp_name = [ m_things_name[i] ]
                                tmp_num  = [ min(need_num * m_things_num[i],900) ]
                                auto_make_Atbusiness( hwnd, tmp_name, tmp_num )
                                continue
                            #  庖丁材料      镶工工匠材料    制符师材料
                            if m_id[i] <= 710 or ( m_id[i] <= 805 and m_id[i] > 800 ) or (m_id[i] >= 829 and m_id[i] <= 835):
                                buy_something_AtGroup( hwnd, m_things_name[i], min(need_num * m_things_num[i],990) )
                            else:
                                buy_something_Atbusiness( hwnd, m_things_name[i], min(need_num * m_things_num[i],990) )
                    make( hwnd, things_name[_], True )
                    time.sleep(4)
                pre_num = num
            stop(hwnd)
        print things_name[_], num

def auto_buyAndsend( name_b,name_s,things,things_num,times ):
    sender = 0
    buyer = 0
    for x in windows:
        ret = get_name(x)
        if ret == name_b:
            buyer = x
        if ret == name_s:
            sender = x
            
    for _ in range(0, times):
        print '当前第'+str(_+1)+'次'
        for x in things:
            buy_something_AtGroup( buyer, x, things_num )
            tmp = [ x ]
            throw_something( buyer, tmp, things_num )
            time.sleep(2)
            send_something( sender, x, things_num )
            print x + ' ',
        print ''


def auto_make_WithB( hwnd, things_name, things_num, buyer ):
    total = len( things_name )
    for _ in range(0,total):
        stop( hwnd )
        _id = 0
        num, addr = get_thing_num( hwnd, things_name[_] )
        if num < things_num[_]:
            _id = make( hwnd, things_name[_], False )
            m_things_name, m_things_num, m_id = find_material( hwnd, _id )

            
            pre_num = 0
            
            while num < things_num[_]:
                time.sleep(4)
                if addr == 0:
                    num, addr = get_thing_num( hwnd, things_name[_] )
                else:
                    num = get_thingAtAddr_num( hwnd, addr )
                        
                if num == pre_num:
                    stop( hwnd )
                    rev_things( hwnd )
                    
                    total = len(m_things_name)
                    
                    for i in range(0,total):
                        m_num, m_addr = get_thing_num(hwnd,m_things_name[i])
                        if m_num < m_things_num[i]:
                            buy_something_AtGroup( buyer, m_things_name[i], 990 )
                            tmp = [ m_things_name[i] ]
                            throw_something( buyer, tmp, 990 )
                            m_num, m_addr = get_thing_num( hwnd, m_things_name[i] )
                            while m_num < 990:
                                KeyClick( hwnd, ord('C') )
                                m_num, m_addr = get_thing_num( hwnd, m_things_name[i] )
                            '''
                            if m_id[i] > 1800 and m_id[i] <= 1975:
                                tmp_name = [ m_things_name[i] ]
                                tmp_num  = [ 950 ]
                                auto_make_Atbusiness( hwnd, tmp_name, tmp_num )
                                continue
                            #  庖丁材料      镶工工匠材料    制符师材料
                            if m_id[i] <= 710 or ( m_id[i] <= 805 and m_id[i] > 800 ) or (m_id[i] >= 829 and m_id[i] <= 835):
                                buy_something_AtGroup( hwnd, m_things_name[i], 999/m_things_num[i]*m_things_num[i] )
                            else:
                                buy_something_Atbusiness( hwnd, m_things_name[i], 999/m_things_num[i]*m_things_num[i] )
                            '''
                    make( hwnd, things_name[_], True )
                    time.sleep(4)
                pre_num = num
            stop(hwnd)
        print things_name[_].decode('gbk'), num

def exit_game( hwnd ):
    
    KeyClick( hwnd, ord('O') )
    LClickAtPos( hwnd, 717, 524 )
    time.sleep(1)
    KeyClick( hwnd, win32con.VK_F7 )
    LClickAtPos( hwnd, 418, 406 )
    LClickAtPos( hwnd, 343, 365 )

if __name__ == "__main__":

    global nameOfmake
    
    windows = []
    win32gui.EnumWindows(_MyCallback,windows)


    
    kernel32 = windll.LoadLibrary("kernel32.dll")
    ReadProcessMemory = kernel32.ReadProcessMemory
    WriteProcessMemory = kernel32.WriteProcessMemory



    nameOfmake = []
    name_file = open('制造物品名称.txt')
    line = name_file.readline()
    nameOfmake.append('空')
    while line:
        ss = line.split(' ')
        nameOfmake.append(ss[1].strip('\n'))
        line = name_file.readline()
    name_file.close()
    

    buy_things = [[] for i in range(10)]
    buy_things[3] = [ '灰炭石', '凡晶石', '黑岩石', '铁原石']
    buy_things[2] = [ '精品猪肉','酿酒的粮食' ]
    buy_things[1] = [  '群青','藤黄','孔雀绿','朱砂' ]
    name_b = '妖丶3839'
    name_s = 'zerry重新'

    
    #auto_buyAndsend(name_b, name_s, buy_things[2], 998, 5)

    
    name = 'sdfsdffffffv'
    name1 = '丷讨饭佬乀'
    name2 = '丩日光倾城'
    things = [ '枭首窟传送卷', '八阵图传送卷', '虎牢关传送卷', '东吴水防传送卷', '赤壁传送卷' ]
    things_num = [947,448,452,434,390]
    tmp = [ '队友单人召唤符', '缩地符', '好友单人召唤符', \
            '临江传送卷', '江夏传送卷', '襄阳传送卷','江陵传送卷', \
            '巴郡传送卷', '魏郡传送卷', '吴郡传送卷' ,\
            '成都传送卷', '洛阳传送卷', '建业传送卷',\
            '三江城传送卷','永昌郡传送卷']
    tmp_num = [ 0,0,0,\
                592,448,415,842,\
                536,528,406,\
                523,810,774,\
                600,600]
    name_buyer = '射你三箭你就ko'
    buyer = 0
    for x in windows:
        ret = get_name(x)
        if ret == name_buyer:
            buyer = x
            break
    temp = [ '队友单人召唤符', '缩地符', '好友单人召唤符', '三江城传送卷','永昌郡传送卷']
    temp_num = [0,0,0,0,0]
    hwnd = 0
    for x in windows:
        ret = get_name(x)
        if ret == name2:
            hwnd = x
            #auto_make_Atbusiness( x,things,things_num )
            #auto_make_WithB( x,,buyer )
            #auto_make_WithB( x,tmp,tmp_num,buyer )
            #for y in tmp:
                #send_something( x,y,900 )
    #auto_make_Atbusiness( hwnd,temp,temp_num )
    auto_make_WithB( hwnd,things,things_num,buyer )
    auto_make_WithB( hwnd,tmp,tmp_num,buyer )
    #auto_make_WithB( hwnd,temp,temp_num,buyer )
    #auto_make_Atbusiness( hwnd,things,things_num )
    #auto_make_WithB( hwnd,things,things_num,buyer )
    #auto_make_WithB( hwnd,tmp,tmp_num,buyer )
    #auto_make_Atbusiness( hwnd,tmp,tmp_num )
    #exit_game( hwnd )
    #exit_game( buyer )






