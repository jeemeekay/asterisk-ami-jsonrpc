#!/usr/bin/env python
#coding=utf-8


import threading
import re
import time
import json
import uuid
import signal
import logging
import logging.handlers
import sys, traceback
from asterisk.ami import AMIClient, EventListener, AutoReconnect, AMIClientAdapter
from jsonrpcserver import methods
import signal, os , sys, time


DEBUG_LEVELV_NUM = 9 
logging.addLevelName(DEBUG_LEVELV_NUM, "DEBUGV")
def debugv(self, message, *args, **kws):
    # Yes, logger takes its '*args' as 'args'.
    if self.isEnabledFor(DEBUG_LEVELV_NUM):
        self._log(DEBUG_LEVELV_NUM, message, args, **kws) 
logging.Logger.debugv = debugv

syslog_level = 20

ablogger = logging.getLogger('AMIProxyLogger')
ablogger.setLevel(syslog_level)

print "syslog level: ",syslog_level
#add handler to the logger
handler = logging.handlers.SysLogHandler('/dev/log')

#add formatter to the handler
#formatter = logging.Formatter('Python: { "loggerName":"%(name)s", "asciTime":"%(asctime)s", "pathName":"%(pathname)s", "logRecordCreationTime":"%(created)f", "functionName":"%(funcName)s", "levelNo":"%(levelno)s", "lineNo":"%(lineno)d", "time":"%(msecs)d", "levelName":"%(levelname)s", "message":"%(message)s"}')


formatter = logging.Formatter('%(name)s: [%(created)f] %(levelname)s %(message)s')

handler.formatter = formatter
ablogger.addHandler(handler)



ASTUSER = "admin"
ASTSECRET = "admin"

client = AMIClient(address="127.0.0.1",port=5038)
AutoReconnect(client)
client.login(username=ASTUSER,secret=ASTSECRET)
adapter = AMIClientAdapter(client)

EventCollection = {}

@methods.add
def ConfbridgeListRooms():
    def event_listener(event,**kwargs):
        global EventCollection,client,adapter
        EventCollection[event.keys['ActionID']].append(event)
    myactionid = str(uuid.uuid4())
    EventCollection[myactionid] = []
    mylistener1 = client.add_event_listener(event_listener,white_list=['ConfbridgeListRooms','ConfbridgeListRoomsComplete'])   
    def cancel_wait(signum,frame):
        raise Exception("ConfbridgeListRooms Failed")
    
    signal.signal(signal.SIGALRM, cancel_wait) 
    signal.alarm(2)  
    try: 
        resp = adapter.ConfbridgeListRooms(ActionID=myactionid)
        if resp.response is None: 
            client.remove_event_listener(mylistener1)
            EventCollection.pop(myactionid, None)
            return []
        while 'ConfbridgeListRoomsComplete' not in [keys.name for keys in EventCollection[myactionid] ]: pass
        signal.alarm(0)
        channels = []
        for event in EventCollection[myactionid]:
            if event.name == "ConfbridgeListRooms":
                channels.append(event.keys)
        client.remove_event_listener(mylistener1)
        EventCollection.pop(myactionid, None)
        return channels
    except Exception,e:
        print 'ConfbridgeListRooms failed: ',e
        client.remove_event_listener(mylistener1)
        EventCollection.pop(myactionid, None)
        return []

@methods.add
def DAHDIShowChannels():
    def event_listener(event,**kwargs):
        global EventCollection,client,adapter
        EventCollection[event.keys['ActionID']].append(event)
    myactionid = str(uuid.uuid4())
    EventCollection[myactionid] = []
    mylistener1 = client.add_event_listener(event_listener,white_list=['DAHDIShowChannels','DAHDIShowChannelsComplete'])   
    def cancel_wait(signum,frame):
        raise Exception("DAHDIShowChannels Failed")
    
    signal.signal(signal.SIGALRM, cancel_wait) 
    signal.alarm(2)   
    try: 
        resp = adapter.DAHDIShowChannels(ActionID=myactionid)
        #print "dahdishowchannels response: ", resp.response
        if resp.response is None: 
            client.remove_event_listener(mylistener1)
            EventCollection.pop(myactionid, None)
            return []
        while 1:
            if 'DAHDIShowChannelsComplete' in [keys.name for keys in EventCollection[myactionid]]: break
        signal.alarm(0)
        channels = []
        for event in EventCollection[myactionid]:
            if event.name == "DAHDIShowChannels":
                channels.append(event.keys)
        client.remove_event_listener(mylistener1)
        EventCollection.pop(myactionid, None)
        return channels
    except Exception,e:
        print "error in dahdishowchannel: ",e
        client.remove_event_listener(mylistener1)
        EventCollection.pop(myactionid, None)
        return []


@methods.add
def IAXpeerlist():
    def event_listener(event,**kwargs):
        global EventCollection,client,adapter
        EventCollection[event.keys['ActionID']].append(event)
    myactionid = str(uuid.uuid4())
    EventCollection[myactionid] = []
    def cancel_wait(signum,frame):
        raise Exception("IAXpeerlist Failed")
    
    signal.signal(signal.SIGALRM, cancel_wait) 
    signal.alarm(2)  
    mylistener1 = client.add_event_listener(event_listener,white_list=['PeerEntry','PeerListComplete'])   
    try: 
        resp = adapter.IAXpeers(ActionID=myactionid)
        if resp.response is None: 
            client.remove_event_listener(mylistener1)
            EventCollection.pop(myactionid, None)
            return []
        while 'PeerListComplete' not in [keys.name for keys in EventCollection[myactionid] ]: pass
        signal.alarm(0)
        channels = []
        for event in EventCollection[myactionid]:
            if event.name == "PeerEntry":
                channels.append(event.keys)
        client.remove_event_listener(mylistener1)
        EventCollection.pop(myactionid, None)
        return channels
    except Exception,e:
        print 'IAXPeerlist failed: ',e
        client.remove_event_listener(mylistener1)
        EventCollection.pop(myactionid, None)
        return []


@methods.add
def SIPpeerstatus():
    def event_listener(event,**kwargs):
        global EventCollection,client,adapter
        EventCollection[event.keys['ActionID']].append(event)
    myactionid = str(uuid.uuid4())
    EventCollection[myactionid] = []
    def cancel_wait(signum,frame):
        raise Exception("SIPpeerstatus Failed")
    
    signal.signal(signal.SIGALRM, cancel_wait) 
    signal.alarm(2)  
    mylistener1 = client.add_event_listener(event_listener,white_list=['PeerStatus','SIPpeerstatusComplete'])   
    try: 
        resp = adapter.SIPpeerstatus(ActionID=myactionid)
        if resp.response is None: 
            client.remove_event_listener(mylistener1)
            EventCollection.pop(myactionid, None)
            return []
        while 'SIPpeerstatusComplete' not in [keys.name for keys in EventCollection[myactionid] ]: pass
        signal.alarm(0)
        channels = []
        for event in EventCollection[myactionid]:
            if event.name == "PeerStatus":
                channels.append(event.keys)
        client.remove_event_listener(mylistener1)
        EventCollection.pop(myactionid, None)
        return channels
    except Exception,e:
        print 'SIPpeerstatus failed',e
        client.remove_event_listener(mylistener1)
        EventCollection.pop(myactionid, None)
        return []

@methods.add
def Status():
    def event_listener(event,**kwargs):
        global EventCollection,client,adapter
        EventCollection[event.keys['ActionID']].append(event)
    myactionid = str(uuid.uuid4())
    EventCollection[myactionid] = []
    mylistener1 = client.add_event_listener(event_listener,white_list=['Status','StatusComplete'])
    def cancel_wait(signum,frame):
        raise Exception("Status Failed")
    
    signal.signal(signal.SIGALRM, cancel_wait) 
    signal.alarm(2)     
    try: 
        resp = adapter.Status(ActionID=myactionid)
        if resp.response is None: 
            client.remove_event_listener(mylistener1)
            EventCollection.pop(myactionid, None)
            return []
        while 'StatusComplete' not in [keys.name for keys in EventCollection[myactionid] ]: pass
        signal.alarm(0)
        channels = []
        for event in EventCollection[myactionid]:
            if event.name == "Status":
                channels.append(event.keys)
        client.remove_event_listener(mylistener1)
        EventCollection.pop(myactionid, None)
        return channels
    except Exception,e:
        print 'Status Failed: ',e
        client.remove_event_listener(mylistener1)
        EventCollection.pop(myactionid, None)
        return []



@methods.add
def CoreShowChannels():
    def event_listener(event,**kwargs):
        global EventCollection,client,adapter
        EventCollection[event.keys['ActionID']].append(event)
    myactionid = str(uuid.uuid4())
    EventCollection[myactionid] = []
    mylistener1 = client.add_event_listener(event_listener,white_list=['CoreShowChannel','CoreShowChannelsComplete'])   
    def cancel_wait(signum,frame):
        raise Exception("MyCoreShowChannels Failed")
    
    signal.signal(signal.SIGALRM, cancel_wait) 
    signal.alarm(2)  
    try: 
        resp = adapter.CoreShowChannels(ActionID=myactionid)
        if resp.response is None: 
            client.remove_event_listener(mylistener1)
            EventCollection.pop(myactionid, None)
            return []
        while 'CoreShowChannelsComplete' not in [keys.name for keys in EventCollection[myactionid] ]: pass
        signal.alarm(0)
        channels = []
        for event in EventCollection[myactionid]:
            if event.name == "CoreShowChannel":
                channels.append(event.keys)
        client.remove_event_listener(mylistener1)
        EventCollection.pop(myactionid, None)
        return channels
    except Exception,e:
        print 'MyCoreShowChannels failed: ',e
        client.remove_event_listener(mylistener1)
        EventCollection.pop(myactionid, None)
        return []


@methods.add
def Ping():
    def cancel_wait(signum,frame):
        raise Exception("Ping Failed")
    
    signal.signal(signal.SIGALRM, cancel_wait) 
    signal.alarm(2)  
    try:
        resp = adapter.Ping().response.keys['Ping']
        if resp == "Pong":
            signal.alarm(0)
            return True
        else: return False
    except Exception,e:
        print "Ping: ",e
        return False

@methods.add
def Originate_Context(channel,exten,context,priority,timeout,callerid,variables):
    def cancel_wait(signum,frame):
        raise Exception("Originate Context Failed")
    
    signal.signal(signal.SIGALRM, cancel_wait) 
    signal.alarm(2)  
    try:
        resp = adapter.Originate(Channel=channel,Exten=exten,Context=context,Priority=priority,Timeout=timeout,CallerID=callerid,variables=variables,Async='true')
        signal.alarm(0)
        return resp.response.keys
    except Exception,e:
        print "originate context error: ",e
            

@methods.add
def Originate_App(channel,application,data,timeout=None,callerid=None,variables=[]):
    def cancel_wait(signum,frame):
        raise Exception("Originate App Failed")
    
    signal.signal(signal.SIGALRM, cancel_wait) 
    signal.alarm(2)  
    try:
        resp = adapter.Originate(Channel=channel,Application=application,Data=data,Timeout=timeout,CallerID=callerid,variable=variables,Async='true')
        signal.alarm(0)
        return resp.response.keys
    except Exception,e:
        print "originate context error: ",e


@methods.add
def MuteAudio(channel,direction,state):
    def cancel_wait(signum,frame):
        raise Exception("MuteAudio Failed")
    
    signal.signal(signal.SIGALRM, cancel_wait) 
    signal.alarm(2)  
    try:
        response = adapter.MuteAudio(Channel=channel,Direction=direction,State=state).response
        print response.keys
        signal.alarm(0)
        return "ok"
    except Exception,e:
        print 'muteaudio failed: ',e
        return "error"


@methods.add
def CoreStatus():
    def cancel_wait(signum,frame):
        raise Exception("CoreStatus Failed")
    
    signal.signal(signal.SIGALRM, cancel_wait) 
    signal.alarm(2)  
    try:
        response = adapter.CoreStatus().response.keys
        signal.alarm(0)
    except Exception,e:
        print 'CoreStatus failed: ',e
        response = {}
    return response


@methods.add
def AbsoluteTimeout(channel):
    def cancel_wait(signum,frame):
        raise Exception("AbsoluteTimeout Failed")
    
    signal.signal(signal.SIGALRM, cancel_wait) 
    signal.alarm(2)  
    try:
        response = adapter.AbsoluteTimeout(Channel=channel,Timeout=timeout).response.keys['Value']
        signal.alarm(0)
    except Exception,e:
        print 'absolutetimeout failed: ',e
        response = ""
    return response

@methods.add
def Hangup(channel):
    def cancel_wait(signum,frame):
        raise Exception("Hangup Failed")
    
    signal.signal(signal.SIGALRM, cancel_wait) 
    signal.alarm(2)  
    try:
        response = adapter.Hangup(Channel=channel).response.keys['Value']
        signal.alarm(0)
    except Exception,e:
        print 'hangup failed: ',e
        response = ""
    return response
            
@methods.add
def Getvar(channel,variable):
    def cancel_wait(signum,frame):
        raise Exception("Getvar Failed")
    
    signal.signal(signal.SIGALRM, cancel_wait) 
    signal.alarm(2)  
    try:
        response = adapter.Getvar(Channel=channel,Variable=variable).response.keys['Value']
        signal.alarm(0)
    except Exception,e:
        print 'getvar failed: ',e
        response = ""
    return response

@methods.add
def ConfbridgeList(conference):
    def event_listener(event,**kwargs):
        global EventCollection,client,adapter
        EventCollection[event.keys['ActionID']].append(event)
    myactionid = str(uuid.uuid4())
    EventCollection[myactionid] = []
    channels = []
    def cancel_wait(signum,frame):
        raise Exception("ConfbridgeList Failed")
    
    signal.signal(signal.SIGALRM, cancel_wait) 
    signal.alarm(2)  
    try:
        mylistener1 = client.add_event_listener(event_listener,white_list=['ConfbridgeList','ConfbridgeListComplete']) 
        
        print 'confbridgelist: ',conference
        resp = adapter.ConfbridgeList(ActionID=myactionid,Conference=conference)
        print resp
        if resp.response is None: return channels
        if resp.response.keys['Message'] != "Confbridge user list will follow":
            client.remove_event_listener(mylistener1)
            EventCollection.pop(myactionid, None)
            return channels     
        while 'ConfbridgeListComplete' not in [keys.name for keys in EventCollection[myactionid] ]: pass
        signal.alarm(0)
        for event in EventCollection[myactionid]:
            if event.name == "ConfbridgeList":
                channels.append(event.keys)
        client.remove_event_listener(mylistener1)
        EventCollection.pop(myactionid, None)
        print "channels in conf",conference,channels
        return channels
    except Exception,e:
        print "ConfbridgeList: ", e
        client.remove_event_listener(mylistener1)
        EventCollection.pop(myactionid, None)
        return channels     
        
     
    
 

def validate_ip(s): 
    valid_ip = re.match("^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$", s) 
    valid_host = re.match("^(([a-zA-Z]|[a-zA-Z][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z]|[A-Za-z][A-Za-z0-9\-]*[A-Za-z0-9])$", s)
    if valid_ip or valid_host: return True
    else: return False



if __name__ == '__main__':
    ablogger.log(syslog_level,'asterisk-ami-jsonrpc proxy loaded... ')
    methods.serve_forever()