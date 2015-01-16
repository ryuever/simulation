# fork_server.py
import os, time, sys, xml.etree.ElementTree as ET
import json
from socket import *                      # get socket constructor and constants
import socket

# {"method":"get", "sender":"First", "date":"2014/07/31", "time":"00:01:00", "type":"int"}
# {"method":"get", "sender":"", "date":"", "time":"", "type":""}
def get_all(dict_ins):
    print(dict_ins)
    print('in get_all')
    pattern = './/'
    if dict_ins['sender']:
        sender_pattern = "data[@sender='{}']/value".format(dict_ins['sender'])
        print(sender_pattern)
        pattern += sender_pattern
    else:
        pattern += 'value'
    if dict_ins['date']:
        date_pattern = "[@date='{}']".format(dict_ins['date'])
        print(date_pattern)
        pattern += date_pattern
    if dict_ins['time']:
        time_pattern = "[@time='{}']".format(dict_ins['time'])
        print(time_pattern)
        pattern += time_pattern
    if dict_ins['type']:
        type_pattern = "[@type='{}']".format(dict_ins['type'])
        print(type_pattern)
        pattern += type_pattern
    print(pattern)
    for item in root.findall(pattern):
        attr = item.attrib
        text = item.text
        print('attr : {}, text :{}'.format(attr, text))        
    return 'attr : {}, text :{}'.format(attr, text)

# {"method":"remove", "sender":"First", "date":"2014/07/31", "time":"00:01:00", "type":"int"}
# {"method":"remove", "sender":"", "date":"", "time":"", "type":""}
def remove(dict_ins):
    print(dict_ins)
    print('in get_all')
    pattern = './/'

    if not (dict_ins['date'] or dict_ins['time'] or dict_ins['type']):
        if dict_ins['sender']:
            parent = '.'
            pattern = "data[@sender='{}']".format(dict_ins['sender'])
            print(parent)
            print(pattern)
        else:
            parent = '.'
            pattern = 'data'
    else:
        if dict_ins['sender']:
            parent = "data[@sender='{}']".format(dict_ins['sender'])
            sender_pattern = "data[@sender='{}']/value".format(dict_ins['sender'])
            print(sender_pattern)
            pattern += sender_pattern
        else:
            pattern += 'value'
            parent = 'data'

        if dict_ins['date']:
            date_pattern = "[@date='{}']".format(dict_ins['date'])
            print(date_pattern)
            pattern += date_pattern
        if dict_ins['time']:
            time_pattern = "[@time='{}']".format(dict_ins['time'])
            print(time_pattern)
            pattern += time_pattern
        if dict_ins['type']:
            type_pattern = "[@type='{}']".format(dict_ins['type'])
            print(type_pattern)
            pattern += type_pattern

    for item in root.findall(parent):
        for child in root.findall(pattern):
            item.remove(child)
            attr = child.attrib
            text = child.text            
    print(ET.dump(root))

    # pending to complete
    return 'attr : {}, text :{}'.format(attr, text)

# 有sender 针对一个
# 没有sender 针对所有
# 如果 date, time, type都不存在的话，报错
# {"method":"insert", "sender":"First", "date":"2014/07/01", "time":"00:01:00", "type":"int", "text":"200"}
# {"method":"insert", "sender":"Second", "date":"2014/06/31", "time":"00:01:00", "type":"int", "text":200}
def insert(dict_ins):
    print(dict_ins)
    print('in get_all')
    pattern = './/'

    if not (dict_ins['date'] or dict_ins['time'] or dict_ins['type']):
        raise Exception("error message")
    else:
        attrib = dict((k, dict_ins[k]) for k in ('date', 'time', 'type') if k in dict_ins)
        if dict_ins['sender']:
            parent = "data[@sender='{}']".format(dict_ins['sender'])
            print(dict_ins['date'])
#            attrib = '"date2":"{}", "time":"{}", "type":"{}"'.format(dict_ins['date'], dict_ins['time'], dict_ins['type'])
        else:
            parent = 'data'
    
    # create new element
    builder = ET.TreeBuilder()
    builder.start('value', attrib)
    print(dict_ins['text'])
    builder.data(dict_ins['text'])
    builder.end('value')
    subele = builder.close()
    
    #....................
    print(parent)
    print(attrib)
    for item in root.findall(parent):
        if item:
            # sub = SubElement(item, 'value',attrib)
            item.append(subele)
            # print(sub)
            
            # ET.SubElement(item,'value',attrib)
    print(ET.dump(root))

    # pending to complete
    return 'attr : {}, text :{}'.format('first', 'second')

def now():                                       # current time on server
    return time.ctime(time.time())

# for zombie process
activeChildren = []
def reapChildren():                              # reap any dead child processes
    while activeChildren:                        # else may fill up system table
        pid, stat = os.waitpid(0, os.WNOHANG)    # don't hang if no child exited
        if not pid: break
        activeChildren.remove(pid)

def handleClient(connection):                    # child process: reply, exit
    while True:                                  # read, write a client socket
        data = connection.recv(1024)             # till eof when socket closed
        if not data: break
        text = data.decode('ascii')
        JSON_str = json.loads(text)
        print(JSON_str)
        method = JSON_str['method']
        if method == 'get':
            print('invoke get_all')
            reply = get_all(JSON_str)
        elif method == 'remove':
            print("remove method")
            reply = remove(JSON_str)            
        elif method == 'insert':
            print("insert method")
            reply = insert(JSON_str)
        else:
            print("error")
            # error                
#        reply = 'Echo=>%s at %s' % (data, now())
        connection.send(reply.encode())
    connection.close()
    os._exit(0)

def launchServer():                                # listen until process killed
    sockobj = socket.socket(AF_INET, SOCK_STREAM)           # make a TCP socket object
    sockobj.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sockobj.bind((clientHost, eval(clientPort)))                   # bind it to server port number
    sockobj.listen(5)                                # allow 5 pending connects

    while True:                                  # wait for next connection,
        connection, address = sockobj.accept()   # pass to process for service
        print('Server connected by', address, end=' ')
        print('at', now())
        reapChildren()                           # clean up exited children now
        childPid = os.fork()                     # copy this process
        if childPid == 0:                        # if in child process: handle
            handleClient(connection)
        else:                                    # else: go accept next connect
            activeChildren.append(childPid)      # add to active child pid list

if __name__=='__main__':
    if len(sys.argv) == 3:
        clientHost = sys.argv[1]
        clientPort = sys.argv[2]
    else:
        clientHost = 'localhost'
        clientPort = 50000

    tree = ET.parse('huji.xml')
    root = tree.getroot()

    launchServer()
