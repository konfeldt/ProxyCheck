#!/usr/bin/env python

from socket import socket, AF_INET, SOCK_STREAM, inet_aton, getaddrinfo,\
                   SOL_TCP
from string import letters
from random import choice
from time import clock

import sys

clock() 


def sock_read(sock, n):
    b = "" 
    i = 0  

    while (i < n): 

        c = sock.recv(n - i) 

        if (len(c) < 1): 
                         
            raise Exception("Closed socket") 

        b += c      
        i += len(c) 

    return b 
    

def str2host(addr, ipv = 4):
    for i in letters: 
        if i in addr[0]: 
            d = getaddrinfo(addr[0], addr[1], 0, 0, SOL_TCP)
            
     

            for j in d:
                if (len(j[-1]) == 2) and (ipv == 4): 
                    return inet_aton(j[-1][0])
                elif (len(j[-1]) == 4) and (ipv == 6): 
                    return inet_aton(j[-1][0])
            raise Exception("Host not found")

    
    return inet_aton(addr[0]

def uint16str(n):
    data = [] 
    data.append( chr(n & 255) ) 
    n >>= 8 

    data.append( chr(n & 255) ) 

    data.reverse() 

    return ''.join(data) 


def SOCKS4_ex(ans):

    
    s4_ex = { 91 : "Request rejected or failed",
              92 : "Request rejected becasue SOCKS server cannot connect to identd on the client",
              93 : "Request rejected because the client program and identd report different user-ids"}
    try:
        raise Exception(s4_ex[ord(ans)]) 
    except:
        raise Exception("Unknown error code #" + str(ord(ans)))


def SOCKS5_ex(ans):

    
    s5_ex = { 1 : "General SOCKS server failure",
              2 : "Connection not allowed by ruleset",
              3 : "Network unreachable",
              4 : "Host unreachable",
              5 : "Connection refused",
              6 : "TTL expired",
              7 : "Command not supported",
              8 : "Address type not supported" }
    try:
        raise Exception(s5_ex[ord(ans)]) 
    except:
        raise Exception("Unknown error code #" + str(ord(ans)))


def SOCKS_hop(sock, addr, proto = 4, ipv = 4):
    if (proto == 4): 
        
        sock.send(chr(4) + chr(1) + uint16str(addr[1]) + str2host(addr) +\
             chr(0))

        
        code = sock_read(sock, 8)[1]

        
        if (code != chr(90)):
            
            SOCKS4_ex(code)

    
    elif (proto == 5): 
        atype = None
        if (ipv == 4): 
            atype = chr(1)
        elif (ipv == 6): 
            atype = chr(4)
        else:
            raise Exception("Unknown IP version")

        sock.send(chr(5) + chr(1) + chr(0))

        
        code = sock_read(sock, 2)

        if (code != (chr(5) + chr(0))):
            raise Exception("Require autentication")

        
        l = sock.send(chr(5) + chr(1) + chr(0) + atype + str(str2host(addr)) +\
             uint16str(addr[1]))

        
        code = sock_read(sock, l)[1]

        
        if (code != chr(00)):
            
            SOCKS5_ex(code)

    else: 
        raise Exception("Unknown SOCKS version")

global settings
settings = {}
if __name__=="__main__":
    pass

check_host = "74.125.230.84" # IP  www.google.com
check_port = 80

timings = {}
plist = []
i = 1
while (i < len(sys.argv)):
    f = open(sys.argv[i], "rt")
    while True:
        txt = f.readline()
        if (len(txt) < 1):
            break
        if (txt[-1] == "\n"):
            txt = txt[:-1]
        addr = txt.split(":")
        s = socket()
        print >>sys.stderr,txt,"...",
        sys.stderr.flush()
        try:
            c1 = clock()
            s.connect((addr[0], int(addr[1])))
            c1 = clock() - c1
            print >>sys.stderr,str(c1) + ",",
            sys.stderr.flush()
            c2 = clock()
            SOCKS_hop(s,(check_host,check_port))
            c2 = clock() - c2
            print >>sys.stderr,str(c2)
            sys.stderr.flush()
            timings[txt] = c1 + c2
        except:
            print >>sys.stderr,"[Error]"
        s.close()
    f.close()
    i += 1


timed = sorted(timings, key=lambda key: timings[key])


for i in timed:
    print i