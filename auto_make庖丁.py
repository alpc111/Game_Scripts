# -*- coding: gbk -*-
import win32api,win32gui,win32con #����win32api���ģ��
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
          


#���ݾ������ַ��ƫ�ƶ�ȡָ�������ڴ�
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

#self='QQSGwinclass' #���ڵ�����
#hwnd = win32gui.FindWindow(self,None)#ͨ������������ȡ���ھ��
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
    win32api.SendMessage(hwnd, win32con.WM_KEYDOWN, key, 0)#���Ͱ���
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
        win32gui.SendMessage(hwnd,win32con.WM_MOUSEWHEEL,neg,0)   #�������Ϲ���
        time.sleep(0.01)
    time.sleep(0.5)

def FindSomething( hwnd, Something, Pos_x, LPos_y, HPos_y, Delta, Bps ):

    pre_id = -1
    insert_pos = len(Bps)
    Bps.append(1),Bps.append(0x34),Bps.append(0x4)
    error_time = 0
    while True:
        LClickAtPos_Short( hwnd, Pos_x , LPos_y )
        time.sleep(0.1)
        bps = [0x54C,0x244]            #�ҳ���ǰ�����Ʒ�����
        idx_hex = readmemory(hwnd,click_addr,bps,4)
        thing_name_idx = ord(idx_hex[1])*256 + ord(idx_hex[0])

        
        if thing_name_idx > 60000:
            error_time = error_time + 1
            if error_time > 200:
                #print 'click_error',thing_name_idx,cur_click_y
                print '������󳬹�150��'
                return False, 0
        
            if LPos_y < HPos_y:
                LPos_y = LPos_y + Delta
            else:
                win32gui.SendMessage(hwnd,win32con.WM_MOUSEWHEEL,1,0)   #�������¹���
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
                print '�������δ�ҵ�'+Something
                return False, 0
        
            if LPos_y < HPos_y:
                LPos_y = LPos_y + Delta
            else:
                win32gui.SendMessage(hwnd,win32con.WM_MOUSEWHEEL,1,0)   #�������¹���
                LClickAtPos_Short( hwnd, Pos_x, LPos_y )    
            continue
        pre_id = thing_name_idx
        if LPos_y < HPos_y:
            LPos_y = LPos_y + Delta
        else:
            win32gui.SendMessage(hwnd,win32con.WM_MOUSEWHEEL,1,0)   #�������¹���
            LClickAtPos_Short( hwnd, Pos_x, LPos_y )

def get_name(hwnd):
    
    bps = [0xc,0x338,0x8888]            #�ǳ�ƫ��
    name = readmemory(hwnd,people_addr,bps,28)
    ss = bytes('')
    for x in name:
        tmp = ord(x)
        if tmp == 0:
            break
        ss = ss + chr(tmp)
    #ss.decode('gbk')
    return ss

def get_thing_num ( hwnd,thing ):      #��ȡ��������Ϊthing����Ʒ�ĸ����͸���Ʒ��� �����ڷ���0,0
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
            bps = [  ]  #�ҳ�������x����Ʒ������
            ret = readmemory(hwnd,addr + 0x28, bps, 4)
            num = 0
            for x in ret[::-1]:
                num = num*256+ord(x)
            return num, addr
    return 0, 0
    '''
    L = 0
    R = 0
    bps = [ 0x38, 0x48c ]  #�ҳ�������Ʒ����
    ret = readmemory(hwnd,people_addr,bps,4)
    for x in ret[::-1]:
        L = L*256 + ord(x)
    bps = [ 0x38, 0x490 ]  #�ҳ�������Ʒ����
    ret = readmemory(hwnd,people_addr,bps,4)
    for x in ret[::-1]:
        R = R*256 + ord(x)
    print hex(L),hex(R)
    for addr in range(L,R,4):
        bps = [ 0x34, 0x4 ]
        
        ret_name = readmemory(hwnd,addr,bps,20)
        
        cur_name = bytes('')
    
        for x in ret_name:
            tmp = ord(x)
            if tmp == 0:
                break
            cur_name = cur_name + chr(tmp)

        if cur_name == thing:
            bps = [ 0x28 ]  #�ҳ�������x����Ʒ������
            ret = readmemory(hwnd,addr,bps,4)
            num = 0
            for x in ret[::-1]:
                num = num*256+ord(x)
            return num, idx
        idx = idx + 1
        time.sleep(0.01)
    return 0, 0
    '''

def get_thingAtAddr_num( hwnd,addr ):
    
    bps = [  ]
    val = readmemory(hwnd,addr + 0x28,bps,4)
    ret = 0
    for x in val[::-1]:
        ret = ret * 256 + ord(x)
    #print ret,idx
    return ret

def Goto_id_x_y( hwnd, map_id, pos_x, pos_y ):
    KeyClick( hwnd, win32con.VK_F4 )
    LClickAtPos( hwnd, 455, 461 )

    text = '/<DnpcWalkEx=' + str(map_id) + '|' + str(pos_x*100) \
                             + '|' + str(pos_y*100) + '|' + '>        /<>'
    #print text
    for x in text:
        win32api.SendMessage(hwnd ,win32con.WM_CHAR ,ord(x),0)

    time.sleep(0.5)
    LClickAtPos( hwnd, 337, 313 )
    LClickAtPos( hwnd, 438, 362 )
    KeyClick( hwnd, win32con.VK_F4 )
def rev_things( hwnd ):     #һ�������ʼ��е���Ʒ
    KeyClick( hwnd, win32con.VK_F6 )
    LClickAtPos( hwnd, 404, 424 )
    LClickAtPos( hwnd, 508, 428 )
    
    time.sleep(10)

    KeyClick( hwnd, win32con.VK_F6 )
    KeyClick( hwnd, win32con.VK_RETURN )
    LClickAtPos( hwnd, 775, 206 )

def buy_something_AtGroup( hwnd, something, buy_num ):  #�Զ����������Ʒ


    while True:
        num, addr = get_thing_num( hwnd, something )
        buy_num = buy_num - num
        if buy_num <= 0:
            return
        
        KeyClick( hwnd, ord('O') )
        LClickAtPos( hwnd, 263, 117 )
        LClickAtPos( hwnd, 260, 533 )

        bps = [ 0x28, 0x484 ]
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
            return True
        else:
            KeyClick( hwnd, ord('O') )
            KeyClick( hwnd, ord('O') )
            #print '����' + something + 'ʧ��'

def buy_something_Atbusiness( hwnd, something, buy_num ):

    while True:
        num, addr = get_thing_num( hwnd, something )
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
            return True
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
        
        bps = [0x54C,0x244]            #�ҳ���ǰ�����Ʒ���������
        idx_hex = readmemory(hwnd,click_addr,bps,4)
        thing_name_idx = 0
        for x in idx_hex[::-1]:
            thing_name_idx = thing_name_idx*256+ord(x)
    
        if thing_name_idx > 10000:
            print 'click_error'
            flag = False
            break
        
        '''
        bps = [ thing_name_idx*32+48 , 0x4 ] #�ҳ���ǰ�����Ʒ������
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
            win32gui.SendMessage(hwnd,win32con.WM_MOUSEWHEEL,1,0)   #�������¹���
    time.sleep(0.5)
    if flag == True:
        DClickAtPos( hwnd, 355, click_pos[cur_click_y] )

        LClickAtPos( hwnd, 422, 306 )
        LClickAtPos( hwnd, 488, 323 )

    else:
        KeyClick( hwnd, ord('K') )
        print thing + '����ʧ��'
        os.system('pause')
    return make_idx

def auto_make_Atbusiness( hwnd, things_name, things_num ):
    total = len( things_name )
    for _ in range(0,total):
        stop( hwnd )
        _id = 0
        num, addr = get_thing_num( hwnd, things_name[_] )
        if num < things_num[_]:
            print '׼������' + things_name[_] + ',��ǰ����Ϊ ' + str(num)
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
                            if (m_id[i] > 1800 and m_id[i] <= 1975) or (m_id[i] > 1200 and m_id[i] <= 1240):
                                tmp_name = [ m_things_name[i] ]
                                tmp_num  = [ min(need_num * m_things_num[i],900) ]
                                auto_make_Atbusiness( hwnd, tmp_name, tmp_num )
                                continue
                            #  �Ҷ�����      �⹤��������    �Ʒ�ʦ����
                            if m_id[i] <= 710 or ( m_id[i] <= 805 and m_id[i] > 800 ) or (m_id[i] >= 829 and m_id[i] <= 835):
                                buy_something_AtGroup( hwnd, m_things_name[i], min(need_num * m_things_num[i],999) )
                            else:
                                buy_something_Atbusiness( hwnd, m_things_name[i], min(need_num * m_things_num[i],999) )
                    make( hwnd, things_name[_], False )
                    time.sleep(4)
                pre_num = num
            stop(hwnd)
        print things_name[_], num

if __name__ == "__main__":
    global nameOfmake
    
    windows = []
    win32gui.EnumWindows(_MyCallback,windows)


    
    kernel32 = windll.LoadLibrary("kernel32.dll")
    ReadProcessMemory = kernel32.ReadProcessMemory
    WriteProcessMemory = kernel32.WriteProcessMemory



    nameOfmake = []
    name_file = open('������Ʒ����.txt')
    line = name_file.readline()
    nameOfmake.append('��')
    while line:
        ss = line.split(' ')
        nameOfmake.append(ss[1].strip('\n'))
        line = name_file.readline()
    name_file.close()


    name1 = '�ҿɰ�����'
    name2 = '��ؼ78658'
    name3 = '������shit'
    

    hwnd = 0
    tmp = [ '�ſ���', '��Ȼ������' ]
    tmp_num = [ 990, 0 ]
    things_name = [ '����ͷ', '�����',\
                    '����С��', '±���', '���ּ���',\
                    '�����ٴ�', '��Ц������']
    things_num = [ 0, 990,\
                   990, 990, 990,\
                   990, 990]
    for x in windows:
        ret = get_name(x)
        if ret == name3:
            hwnd = x
    if hwnd != 0:
        #auto_make_Atbusiness( hwnd,tmp,tmp_num )
        auto_make_Atbusiness( hwnd,things_name,things_num )
                





