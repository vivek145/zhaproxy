#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 15:34:34 2017

@author: wilson.varaschin
"""
import signal
import time
import multiprocessing
import logging
import json, argparse, sys
from bottle import Bottle, run, request
from haproxyadmin import haproxy


webservice = Bottle()
"""
ERRRO 404
"""
@webservice.error(404)
def error404(error):
    return('sem suporte - 404')

@webservice.error(500)
def error500(error):
    return('-500')

"""
informação de processo
"""
@webservice.route('/process/<info>')
def pr_haproxy(info):
    global happrocess
    if info in ['nodename', 'releasedate', 'version', 'uptime', \
                'totalrequests', 'uptimesec']:
        return(str(getattr(happrocess,info)))
    return('-1')

"""
discovery = FRONTEND
"""
@webservice.route('/frontend')
def frontend_to_json():
    global happrocess
    jsonfrontend={}
    jsonfrontend['data']=[]
    frontends = happrocess.frontends()
    for frontend in frontends:
        jsonfrontend['data'].append({
        '{#FRNAME}':frontend.name
        })
    return(jsonfrontend)

#http://127.0.0.1:8081/frontend/zimbra-admin?metrica=bin
@webservice.route('/frontend/<ftname>')
def ft_srv_metric(ftname):
    global happrocess
    metrica = request.query.metrica
    try:
        frontend = happrocess.frontend(ftname)
    except:
        return('-1')
    if metrica in ['bin', 'bout', 'comp_byp', 'comp_in',\
                   'comp_out', 'comp_rsp', 'dreq', 'dresp', 'ereq',\
                   'hrsp_1xx', 'hrsp_2xx', 'hrsp_3xx', 'hrsp_4xx',\
                   'hrsp_5xx', 'hrsp_other', 'rate', 'rate_lim',\
                   'rate_max', 'req_rate', 'req_rate_max',\
                   'req_tot', 'scur', 'slim', 'smax', 'stot']:
        return(str(frontend.metric(metrica)))
    return('-404')

"""
discovery = BACKEND
"""
@webservice.route('/backend')
def backend_to_json():
    global happrocess
    jsonbackend={}
    jsonbackend['data']=[]
    backends=happrocess.backends()
    for backend in backends:
        servers=backend.servers()
        for server in servers:
            jsonbackend['data'].append({
            '{#BKNAME}':backend.name,
            '{#SRVNAME}':server.name
            })
    return(jsonbackend)


#http://127.0.0.1:8081/backend/sig-outros?srvname=preto-sig&metrica=act
#http://127.0.0.1:8081/backend/sig-outros?metrica=bin
@webservice.route('/backend/<bkname>')
def bk_srv(bkname):
    global happrocess
    metrica = request.query.metrica
    srvname = request.query.srvname
    try:
        backend = happrocess.backend(bkname)
    except:
        return('-1')
    if srvname:
        try:
            server = backend.server(srvname)
        except:
            return('-1')
        if metrica in ['act','bck','bin','bout',\
                       'check_duration','chkdown','chkfail',\
                       'cli_abrt','ctime','downtime',\
                       'dresp','econ','eresp','hrsp_1xx',\
                       'hrsp_2xx','hrsp_3xx','hrsp_4xx',\
                       'hrsp_5xx','hrsp_other','lastchg',\
                       'lastsess','lbtot','qcur','qlimit',\
                       'qmax','qtime','rate','rate_max',\
                       'rtime','scur','smax','srv_abrt',\
                       'stot','throttle','ttime','weight',\
                       'wredis','wretr']:
            return(str(server.metric(metrica)))
        elif metrica in ['check_status','status','requests']:
            return(str(getattr(server,metrica)))
    elif metrica in ['act','bck', 'bin', 'bout',\
                     'chkdown', 'cli_abrt', 'comp_byp',\
                     'comp_in', 'comp_out', 'comp_rsp',\
                     'ctime', 'downtime', 'dreq',\
                     'dresp', 'econ', 'eresp',\
                     'hrsp_1xx', 'hrsp_2xx', 'hrsp_3xx',\
                     'hrsp_4xx', 'hrsp_5xx',\
                     'hrsp_other', 'lastchg',\
                     'lastsess', 'lbtot', 'qcur', 'qmax',\
                     'qtime', 'rate', 'rate_max',\
                     'rtime', 'scur', 'slim', 'smax',\
                     'srv_abrt', 'stot', 'ttime',\
                     'weight', 'wredis', 'wretr']:
        return(str(backend.metric(metrica)))
    elif metrica in ['check_status','status','requests','weight']:
        metrica_list = []
        if len(backend.servers())>1:
            for server in backend.servers():
                metrica_list.append(getattr(server,metrica))
            if 'UP' in metrica_list:
                return('UP')
            return(metrica_list[0])
        else:
            server = backend.servers()[0]
            return(str(getattr(server,metrica)))
    return('-404')


if __name__ == "__main__":
    happrocess=haproxy.HAProxy(socket_dir='/var/lib/haproxy')
    run(webservice, host='localhost', port=8081, debug=True)

