# -*- coding: utf-8 -*-
import socket
import threading
import time
import random
import json
mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mysocket.bind(('127.0.0.1', 1026))
mysocket.listen(10)
mysocket.setblocking(False)
# mysocket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, 2)
password = ''
for _ in range(20):
    password += random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-=')
print(password)
players = [[None, None],[None, None],[None, None],[None, None],[None, None]]
colorList = ['r','b','y','g']
cardLeft = list(range(1,109))
def getRandomCard():
    global colorList
    if len(cardLeft) == 0:
        raise SystemExit("Out of cards!")
    cardID = cardLeft.pop(random.randint(0,len(cardLeft)-1))
    if cardID>104: # 4
        return 'wild'
    elif cardID > 100:
        return 'wild4'
    # cardID 0-100
    cardColor = colorList[cardID % 4] # 0-3
    cardID = cardID%25 # 0-24
    if cardID == 0:
        return cardColor+'0'
    cardID = cardID%12
    if cardID == 9:
        return cardColor+'reverse'
    elif cardID == 10:
        return cardColor+'skip'
    elif cardID == 11:
        return cardColor+'draw2'
    else: # number
        return cardColor+str(cardID+1)
def cardFun(num):
    tmp = []
    for _ in range(num):
        tmp.append(getRandomCard())
    return tmp
def tcplink(sock, addr):
    print("Accept connection from %s:%s" % addr)
    # sock.send(b'Your password')
    # data = sock.recv(20)
    # if data.decode('utf-8').encode('utf-8'） == password:
    #     sock.send(b'You\'re welcome!')
    # else:
    #     print('Connection from %s:%s password wrong.' % addr)
    #     sock.send(b'Password wrong!')
    #     sock.close()
    #     return
    
    # data = sock.recv(4) 
    ip = addr[0].split('.')
    myaddr = ip[0]+ip[1]+ip[2]+ip[3]+str(addr[1])
    # pid = addr.split(4)
    # sock.send(myaddr.encode('utf-8'))
    while True:
        # p:play e:exit r:replay a:add game 
        dataRecv = ''
        while True:
            try:
                server_replay = sock.recv(1).decode('utf-8')
                dataRecv+=server_replay
                print("debug#1")
            except (BlockingIOError, socket.timeout):
                print("debug#2")
                break
        try:
            print("debug#3")
            data = json.loads(dataRecv)
        except json.decoder.JSONDecodeError:
            print(dataRecv)
            break
        if not data or data['cmd'] == 'e':
            break
        if data['cmd'] == 'a':
            # f: fail s: suscess
            print('a')
            if not players[int(data['table'])-1][0]:
                players[int(data['table'])-1][0] = myaddr
                sock.send(b'{"cmd":"s"}')
                print(players)
            elif not players[int(data['table'])-1][1]:
                players[int(data['table'])-1][1] = myaddr
                sock.send(b'{"cmd":"s"}')
                print(players)
            else:
                sock.send(b'{"cmd":"f","reason":"Table Full"}')
        if data['cmd'] == 'r':
            sock.send(json.dumps(cardFun(7)).encode('utf-8'))
        if data['cmd'] == 'p':
            pass
        dataRecv = ''
    sock.close()
    print('Connection from %s:%s closed.' % addr)
while True:
    # 接受一个新连接:
    try:
        sock, addr = mysocket.accept()
        # 创建新线程来处理TCP连接:
        t = threading.Thread(target=tcplink, args=(sock, addr))
        t.start()
    except BlockingIOError:
        pass