#!/usr/bin/env python
# coding:utf-8

__version__ = '1.2'
__author__ = "phus.lu@gmail.com"

import sys
import os

sys.dont_write_bytecode = True
sys.path += ['.', __file__, '../local']

import re
import getpass
import logging
import socket
import fancy_urllib
import random
import proxy

http = proxy.Http()

_realgetpass = getpass.getpass
def getpass_getpass(prompt='Password:', stream=None):
    try:
        import msvcrt
        password = ''
        sys.stdout.write(prompt)
        while 1:
            ch = msvcrt.getch()
            if ch == '\b':
                if password:
                    password = password[:-1]
                    sys.stdout.write('\b \b')
                else:
                    continue
            elif ch == '\r':
                sys.stdout.write(os.linesep)
                return password
            else:
                password += ch
                sys.stdout.write('*')
    except Exception, e:
        return _realgetpass(prompt, stream)
getpass.getpass = getpass_getpass

_GOOGLE_IPLIST = None
def socket_create_connection((host, port), timeout=None, source_address=None):
    global _GOOGLE_IPLIST
    logging.debug('socket_create_connection connect (%r, %r)', host, port)
    if '.google.com' in host:
        if _GOOGLE_IPLIST is None:
            _GOOGLE_IPLIST = [x[-1][0] for x in socket.getaddrinfo('mail.l.google.com', 443)]
        http.dns[host] = _GOOGLE_IPLIST
    http.window = 60
    return http.create_connection((host, port), timeout)

fancy_urllib._create_connection = socket_create_connection
socket.create_connection = socket_create_connection

def upload(dirname, appid, appaccount):
    assert isinstance(dirname, basestring) and isinstance(appid, basestring) and isinstance(appaccount,basestring)
    filename = os.path.join(dirname, 'app.yaml')
    assert os.path.isfile(filename)
    with open(filename, 'rb') as fp:
        yaml = fp.read()
    yaml=re.sub(r'application:\s*\S+', 'application: '+appid, yaml)
    with open(filename, 'wb') as fp:
        fp.write(yaml)

    filewsgi = os.path.join(dirname, 'wsgi_mail.py')
    assert os.path.isfile(filewsgi)
    with open(filewsgi, 'rb') as fp:
        wsgifile = fp.read()
    wsgifile=re.sub(r'GoAgent<[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})>', "GoAgent<%s>" %appaccount, wsgifile)
    with open(filewsgi, 'wb') as fp:
        fp.write(wsgifile)

    filecron = os.path.join(dirname, 'cron.yaml')
    assert os.path.isfile(filecron)
    with open(filecron, 'rb') as fp:
        cronrd = fp.read()
    cronrd=re.sub(r'\d+:\d+', '%02d:%02d'%(random.randint(0,23),random.randint(0,59)), cronrd)
    with open(filecron, 'wb') as fp:
        fp.write(cronrd)


    import google.appengine.tools.appengine_rpc
    import google.appengine.tools.appcfg
    google.appengine.tools.appengine_rpc.HttpRpcServer.DEFAULT_COOKIE_FILE_PATH = './.appcfg_cookies'
    google.appengine.tools.appcfg.main(['appcfg', 'rollback', dirname])
    google.appengine.tools.appcfg.main(['appcfg', 'update', dirname])

def main():
    appids = raw_input('APPID:')
    if not re.match(r'[0-9a-zA-Z\-|]+', appids):
        print('appid Wrong Format, please login http://appengine.google.com to view the correct appid!')
        sys.exit(-1)
    appaccount = raw_input('Email(google account):')
    if not re.match(r'^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', appaccount):
        print('email format wrong,please input you valid google account!')
        sys.exit(-2)
    for appid in appids.split('|'):
        upload(os.environ.get('uploaddir', 'python').strip(), appid, appaccount)

if __name__ == '__main__':
   try:
       main()
   except KeyboardInterrupt:
       pass