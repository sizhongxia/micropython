from machine import Pin
from dyplayer import DYPlayer
import time


io0 = Pin(32, Pin.OUT)
io1 = Pin(33, Pin.OUT)
io2 = Pin(25, Pin.OUT)
io3 = Pin(26, Pin.OUT)
io4 = Pin(27, Pin.OUT)
io5 = Pin(14, Pin.OUT)
io6 = Pin(12, Pin.OUT)
io7 = Pin(13, Pin.OUT)


io0.value(0)
io1.value(0)
io2.value(0)
io3.value(0)
io4.value(0)
io5.value(0)
io6.value(0)
io7.value(0)

touchPin = Pin(19, Pin.IN)
curTouchVal = 0

curVolum = 0x14


#print('Init RFID...')
#uart1 = UART(2, baudrate=9600, tx=17, rx=16)
#uart1.init(9600, bits=8, parity=None, stop=1)
#print('Init RFID Success')
#io1.value(1)

def _ByteToHex( bins ):
    return ''.join( [ "%02X" % x for x in bins ] ).strip()


def _ToPlay( code = 'welcome' ):
    print(code)
    if code == '0357E009' :
        print('00001 ：这里是学习区，你可以在这里看书、写字和画画')
        _ToPlayAudio('/00001.mp3')
        
    elif code == '3357E009' :
        print('00002 ：这里面是泡沫海绵大积木玩具')
        _ToPlayAudio('/00002.mp3')
        
    elif code == '9357E009' :
        print('00003 ：这里面是厨房餐具玩具')
        _ToPlayAudio('/00003.mp3')
        
    elif code == 'C357E009' :
        print('00004 ：这里面是交通工具大汽车玩具')
        _ToPlayAudio('/00004.mp3')
        
    elif code == 'C35EE009' :
        print('00005 ：这里面是交通工具小汽车玩具')
        _ToPlayAudio('/00005.mp3')
        
    elif code == '4358E009' :
        print('00006 ：这里是学习卡片存放区')
        _ToPlayAudio('/00006.mp3')
        
    elif code == 'F357E009' :
        print('00009 ：我是克缇小台灯，我可以照明，还可以显示日期、时间和温度')
        _ToPlayAudio('/00009.mp3')
        
    elif code == '7358E009' :
        print('00010 ：我是小书架，你可以把你喜欢的图书放在我身上')
        _ToPlayAudio('/00010.mp3')
        
    elif code == '6357E009' :
        print('00011 ：我是大箱子，这里有好多玩具哦~')
        _ToPlayAudio('/00011.mp3')
        
    elif code == 'welcome' :
        print('00013 ：你好呀，我是神奇的魔法棒，快来探索和发现更多有趣的地方吧~')
        _ToPlayAudio('/00013.mp3')


def _ToPlayAudio(path):
    print('PlayAudio: ' + path)
    player.play(single_name=path)


io0.value(1)
print('Start Running...')
# time.sleep(1)
print('Init DYPlayer...')
player = DYPlayer()
uart = player.get_uart()
print('Init DYPlayer Success')

while True:
    touchValue = touchPin.value()
    if curTouchVal != touchValue:
        curTouchVal = touchValue
        if curTouchVal == 1:
            if curVolum == 0x14:
                curVolum = 0x1E
            else:
                curVolum = 0x14
            print(curVolum)
            player.set_volume(curVolum)
            print('Change Volume Done')
            _ToPlay(code = 'welcome')

    if uart.any() > 0:
        io3.value(4)
        ptr = uart.read()
        if len(ptr) == 12 :
            if ptr[4] == 0x00 :
                if ptr[0] == 0x04 and ptr[1] == 0x0C and ptr[2] == 0x02 and ptr[3] == 0x20 :
                    nos = bytearray(4)
                    for i in range(4):
                        nos[i] = ptr[i+7]
                    _ToPlay(_ByteToHex(nos))
                    io6.value(4)

    time.sleep_ms(800)
    

