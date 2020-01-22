import os
import time
import socketio

sock = socketio.Client()
sock.connect('http://192.168.43.187:33333')


def tts(msg):
    tt = ''
    msg = str(msg)
    if msg == '0':
        tt = '오른쪽으로 가세요'
    elif msg == '1':
        tt = '직진하세요'
    elif msg == '2':
        tt = '왼쪽으로 가세요'
    elif msg == '3':
        tt = '뒤로 돌아가세요'
    elif msg == '5':
        tt = '물체인식'
    print(tt)
    os.system('say ' + tt)
i = 0

while True:
    sock.emit('putttt', i % 4)
    #print('aaa')
    time.sleep(1)
    sock.on('getttt', tts)
    i = i + 1
