"""
{{BUILD}}
install rust
sudo apt install python3.X-dev
sudo apt-get install libffi-dev
"""
from collections import namedtuple
from concurrent.futures import ThreadPoolExecutor
from threading import Timer
import ctypes
import queue
import time
import requests
import json
import inspect
import os
import subprocess as sub
import sh
import datetime
import time
import ziggurat as zigg
import requests
import datetime
import pandas as pd
import numpy as np
import json
import sys
import regex as re
from timeit import default_timer as timer
from pathlib import Path
from functools import reduce
import math
import random
import tradingview_ta as tva
import queue
import torch
import pickle
import threading
import select
zigg.road_to_ziggurat(testing=False)

class Chain:
    #def augment():
        #t_1 = timer()
        #while True:
            #t_1=zigg.Tools.elaps(f=Chain.XOR_PRICES,timer_=t_1,seconds=5)
            #time.sleep(5)
    def agg_aczss():
        pass
        
    def XOR_PRICES():
        show = dict()
        for sybl in AugChainZigg.symbolss:
            xor = Tesseract.tickss[sybl].iloc[-1]['XOR']
            if sybl != "XOR":
                try: usd = xor*Tesseract.tickss["XOR"].iloc[-1]["XOR"]
                except IndexError:usd=np.nan
            elif sybl == "XOR":
                try: usd = xor
                except IndexError:usd=np.nan
            time=Tesseract.tickss[sybl].iloc[-1][zigg.dateixname_]
            try: xbal = Tesseract.balancess.loc[sybl,"XBAL"]
            except (AttributeError, KeyError): xbal = 0
            try: pred = Sts.ststate["acz"][sybl]
            except: pred = 0
            try:
                aczss = Tesseract.aczss[sybl]["+CZ"][-53280:]
                aczss=aczss.groupby(by=pd.Grouper(key='TIME', axis=0, freq='1min')).mean()
                _acz1h = aczss[-60:]
                _acz1h = zigg.Tools.numberformat(round(_acz1h.mean(),4))
            except: _acz1h = 0
            show[sybl] = {"ACZ":round(pred,4),"Z1H":_acz1h,"XOR":round(xor,4),"USD":round(usd,4),"TIME":str(time)}
        zigg.Tools.save_json(path=Path(zigg.ticks,"XOR_PRICES.json"), jss=json.dumps(show))
        return

class Sts:
    def load_strategies():
        Sts.ACZ = "ACZ"
        Sts.LSTM="LSTM"
        Sts.MANUAL="MANUAL"
        Sts.BUY_LOW="BUY_LOW"
        Sts.SELL_HIGH="SELL_HIGH"
        Sts.BUY_TAKE_PROFIT="BUY_TP"
        Sts.BUY_STOP_LOSS="BUY_SL"
        Sts.SELL_TAKE_PROFIT="SELL_TP"
        Sts.SELL_STOP_LOSS="SELL_SL"
        Sts.TA_VIEW="TA_VIEW"
        Sts.stcols=("ST","IN","OUT","XQT","XOR","TP","SL","EXPIRE","TIME","IX")
        Sts.stss=pd.DataFrame(columns=Sts.stcols)
        Sts.stss=pd.concat((Sts.stss,zigg.Tools.pickle(path=zigg.database,name=zigg.strategies_,load=True)),axis=0)
        Sts.ststate=zigg.Tools.pickle(path=zigg.ststate,name="ststate",load=True,json=True)
        Sts.hypothesiss=pd.DataFrame()
    def taview_load():
        statecols=["XQT"]
        Sts.tadfss = {}
        Sts.tavecss={"STRONG_SELL":-2,"SELL":-1,"NEUTRAL":0,"BUY":1,"STRONG_BUY":2}
        if Sts.ststate.get(Sts.TA_VIEW,None)==None:
            Sts.ststate[Sts.TA_VIEW] = {}
        for syblss in AugChainZigg.tasyblss:
            sybl=syblss[0]
            Sts.tadfss[sybl]=pd.DataFrame(columns=["TIME","1M","5M","15M","30M","1H","1D"])
            Sts.tadfss[sybl]=pd.concat((Sts.tadfss[sybl],zigg.Tools.pickle(path=zigg.taview,name=sybl.replace("/",""),load=True)),axis=0)
            if Sts.tadfss[sybl].isnull().values.any() == True:
                try:raise Exception()
                except: zigg.Tools.error(exc="NAN VALUES FOUND WHEN LOADING DATA")
                Sts.tadfss[sybl].dropna(axis=0,inplace=True)
            if Sts.tadfss[sybl].empty == False:
                for col in Sts.tadfss[sybl].columns:
                    try: Sts.tadfss[sybl][col] = tuple(map(float,Sts.tadfss[sybl][col]))
                    except (ValueError,TypeError): pass
                Sts.tadfss[sybl]["TIME"]=pd.to_datetime(Sts.tadfss[sybl]["TIME"])
                Sts.tadfss[sybl]=Sts.tadfss[sybl][-120960:]
            sybl_ = sybl.split("/")[0]
            if Sts.ststate.get(Sts.TA_VIEW).get(sybl_,None)==None:
                Sts.ststate[Sts.TA_VIEW][sybl_]={}
                Sts.ststate[Sts.TA_VIEW][sybl_]["XQT"]=0
            
    def taview_save():
        for sybl,tatk in Sts.tadfss.items():
            sybl=sybl
            tatks=tatk.copy(deep=True)
            tatks=tatks.groupby(by=pd.Grouper(key="TIME", axis=0, freq='1min')).agg(["mean"])
            tatks.columns=tuple(map(lambda x:x[0],list(tatks.columns)))
            tatks.reset_index(drop=False, inplace=True)
            if tatks.isnull().values.any() == True: tatks.dropna(axis=0,inplace=True)
            zigg.Tools.pickle(
                df=tatks,path=zigg.taview,name=sybl.replace("/",""),save=True)
            del tatks   
    
    def mult_lstm_pred(sybl=None, pred=None):
        print(f"<MULT-LSTM-FORWARD>")
        for sybl in AugChainZigg.aczswpss:
            try: Sts.ststate[Sts.LSTM][sybl]["XOR"] = Sts.Lstm.augchainzigg(sybl=sybl,col="XOR",path=zigg.lstm)
            except ValueError: Sts.ststate[Sts.LSTM][sybl]["XOR"] = 0
            except KeyError: 
                Sts.ststate[Sts.LSTM][sybl] = {}
                Sts.ststate[Sts.LSTM][sybl]["XOR"] = 0
                
    def taview_strategie(is_swap=None):
        time.sleep(3600)
        while True:
            for sybl,tatks in Sts.tadfss.items():
                sybl_ = sybl.split("/")[0]
                if sybl_ in AugChainZigg.aczswpss:
                    tatks_=Sts.taview_aggregation(tadf=tatks.copy(deep=True))
                    hit=tatks_.mean(numeric_only=True).sum()
                    if hit < -6.0 and Sts.ststate[Sts.TA_VIEW][sybl_]["XQT"] == 0:
                        is_swap=AugChainZigg.swap(inpsybl="XSTUSD", outsybl=sybl_, desired_amount_out=2.0, st=Sts.TA_VIEW)
                        if is_swap == zigg.success_: Sts.ststate[Sts.TA_VIEW][sybl_]["XQT"] == 2#BUY
                    if hit < 0.0 and Sts.ststate[Sts.TA_VIEW][sybl_]["XQT"] == 1:                  
                        is_swap=AugChainZigg.swap(inpsybl=sybl_, outsybl="XSTUSD", desired_amount_out=1.0, st=Sts.TA_VIEW)
                        if is_swap == zigg.success_: Sts.ststate[Sts.TA_VIEW][sybl_]["XQT"] == 0#SELL      
                    if hit > 0.0 and hit < 2.0 and Sts.ststate[Sts.TA_VIEW][sybl_]["XQT"] == 0:                   
                        is_swap=AugChainZigg.swap(inpsybl="XSTUSD", outsybl=sybl_, desired_amount_out=1.0, st=Sts.TA_VIEW)
                        if is_swap == zigg.success_: Sts.ststate[Sts.TA_VIEW][sybl_]["XQT"] == 1#BUY
                    if hit > 0.0 and hit < 2.0 and Sts.ststate[Sts.TA_VIEW][sybl_]["XQT"] == 2:                   
                        is_swap=AugChainZigg.swap(inpsybl=sybl_, outsybl="XSTUSD", desired_amount_out=1.0, st=Sts.TA_VIEW)
                        if is_swap == zigg.success_: Sts.ststate[Sts.TA_VIEW][sybl_]["XQT"] == 1#SELL           
                    if hit > 2.0 and hit < 4.0 and Sts.ststate[Sts.TA_VIEW][sybl_]["XQT"] == 1:          
                        is_swap=AugChainZigg.swap(inpsybl="XSTUSD", outsybl=sybl_, desired_amount_out=1.0, st=Sts.TA_VIEW)
                        if is_swap == zigg.success_: Sts.ststate[Sts.TA_VIEW][sybl_]["XQT"] == 2#BUY              
                    if hit > 6.0 and Sts.ststate[Sts.TA_VIEW][sybl_]["XQT"] == 2:                  
                        is_swap=AugChainZigg.swap(inpsybl=sybl_, outsybl="XSTUSD", desired_amount_out=2.0, st=Sts.TA_VIEW)
                        if is_swap == zigg.success_: Sts.ststate[Sts.TA_VIEW][sybl_]["XQT"] == 0#SELL
                    if is_swap == zigg.success_: zigg.Tools.save_json(path=zigg.ststate, jss=Sts.ststate)
            time.sleep(60)
    def taview_watcher():
        tavwt=timer()
        multss,analss,analsss=[],{},{}
        for syblss in AugChainZigg.tasyblss:
            multss.append(f"{syblss[1].lower()}:{syblss[0].replace('/','').lower()}")
        while True:
            try:analss["1M"]=tva.get_multiple_analysis("crypto", tva.Interval.INTERVAL_1_MINUTE, symbols=multss,timeout=5)
            except: pass
            time.sleep(2)
            try:analss["5M"]=tva.get_multiple_analysis("crypto", tva.Interval.INTERVAL_5_MINUTES, symbols=multss,timeout=5)
            except: pass
            time.sleep(2)
            try: analss["15M"]=tva.get_multiple_analysis("crypto", tva.Interval.INTERVAL_15_MINUTES, symbols=multss,timeout=5)
            except : pass
            time.sleep(2)
            try:analss["30M"]=tva.get_multiple_analysis("crypto", tva.Interval.INTERVAL_30_MINUTES, symbols=multss,timeout=5)
            except: pass
            time.sleep(2)
            try:analss["1H"]=tva.get_multiple_analysis("crypto", tva.Interval.INTERVAL_1_HOUR, symbols=multss,timeout=5)
            except: pass
            time.sleep(2)
            try:analss["1D"]=tva.get_multiple_analysis("crypto", tva.Interval.INTERVAL_1_DAY, symbols=multss,timeout=5)
            except: pass
            time.sleep(1)
            for syblss in AugChainZigg.tasyblss:
                sybl=syblss[0]
                sybl_=sybl.replace("/","")
                for key,anal in analss["1M"].items():
                    if key.split(":")[1]==sybl_:
                        analsss["1M"]=(anal.summary["RECOMMENDATION"])
                for key,anal in analss["5M"].items():
                    if key.split(":")[1]==sybl_:
                        analsss["5M"]=(anal.summary["RECOMMENDATION"])
                for key,anal in analss["15M"].items():
                    if key.split(":")[1]==sybl_:
                        analsss["15M"]=(anal.summary["RECOMMENDATION"])
                for key,anal in analss["30M"].items():
                    if key.split(":")[1]==sybl_:
                        analsss["30M"]=(anal.summary["RECOMMENDATION"])
                for key,anal in analss["1H"].items():
                    if key.split(":")[1]==sybl_:
                        analsss["1H"]=(anal.summary["RECOMMENDATION"])
                for key,anal in analss["1D"].items():
                    if key.split(":")[1]==sybl_:
                        analsss["1D"]=(anal.summary["RECOMMENDATION"])
                tatick=pd.DataFrame(columns=["TIME","1M","5M","15M","30M","1H","1D"], data=[[tuple(),analsss["1M"],analsss["5M"],analsss["15M"],analsss["30M"],analsss["1H"],analsss["1D"]]])
                tatick=tatick.apply(lambda x:[Sts.tavecss.get(y) for y in x])
                tatick["TIME"]=pd.to_datetime(zigg.Tools.dateformat())
                Sts.tadfss[sybl]=pd.concat((Sts.tadfss[sybl],tatick),axis=0,ignore_index=True)
            tavwt=zigg.Tools.elaps(f=Sts.taview_save,timer_=tavwt,seconds=1800)
            
    def taview_aggregation(tadf=None):
        tadf=tadf.groupby(by=pd.Grouper(key="TIME", axis=0, freq='1min')).agg(["mean"])
        tadf.columns=tuple(map(lambda x:x[0],tuple(tadf.columns)))
        tadf.reset_index(drop=False, inplace=True)
        regress = -20000
        tatks,retry =tadf[regress:],0
        while True:
            tatks=tatks.dropna(axis=0)
            if len(tatks.index) < 20000 and retry < 9:
                regress = regress*2
                tatks=tadf[regress:]
                retry += 1
                continue
            if len(tatks.index) > 20000: tatks=tatks[-20000:]
            break
        return tatks
       
    def strategies_target():
        while True:
            time.sleep(10)
            is_swap, spswp = None, None
            for sybl in AugChainZigg.symbolss:
                try: hit = Tesseract.tickss[sybl].iloc[-1]["XOR"]
                except IndexError: pass
                for srow in Sts.stss.itertuples(index=True):
                    if srow.ST==Sts.BUY_LOW and sybl==srow.OUT and hit<=srow.XOR:
                        is_swap=AugChainZigg.swap(inpsybl=srow.IN,outsybl=srow.OUT,desired_amount_out=float(srow.XQT),st=srow.ST)
                        if is_swap == zigg.success_:
                            Sts.stss.drop(srow.Index,axis=0,inplace=True)
                            if np.isnan(srow.TP) == False: Sts.sell_high(st=Sts.BUY_TAKE_PROFIT,inp=srow.OUT,out=srow.IN,xor=srow.TP,xqt=srow.XQT,ix=srow.IX)
                            if np.isnan(srow.SL) == False: Sts.buy_low(st=Sts.BUY_STOP_LOSS,inp=srow.OUT,out=srow.IN,xor=srow.SL,xqt=srow.XQT,ix=srow.IX)
                    elif srow.ST==Sts.SELL_HIGH and sybl==srow.IN and hit>=srow.XOR:
                        is_swap=AugChainZigg.swap(inpsybl=srow.IN,outsybl=srow.OUT,desired_amount_out=float(srow.XQT),st=srow.ST)
                        if is_swap == zigg.success_:
                            Sts.stss.drop(srow.Index,axis=0,inplace=True)
                            if np.isnan(srow.TP) == False: Sts.buy_low(st=Sts.SELL_TAKE_PROFIT,inp=srow.OUT,out=srow.IN,xor=srow.TP,xqt=srow.XQT,ix=srow.IX)
                            if np.isnan(srow.SL) == False: Sts.sell_high(st=Sts.SELL_STOP_LOSS,inp=srow.OUT,out=srow.IN,xor=srow.SL,xqt=srow.XQT,ix=srow.IX)
                    if isinstance(srow.EXPIRE, tuple):
                        zigg.Tools.elaps(timer_=srow.EXPIRE[1],seconds=float(srow.EXPIRE[0]), f=Sts.stss.drop, labels=srow.Index, axis=0, inplace=True)
                    elif srow.ST == Sts.BUY_TAKE_PROFIT and hit >= srow.XOR and sybl==srow.OUT: spswp = True
                    elif srow.ST == Sts.BUY_STOP_LOSS and hit <= srow.XOR and sybl==srow.OUT: spswp = True
                    elif srow.ST == Sts.SELL_TAKE_PROFIT and hit <= srow.XOR and sybl==srow.OUT: spswp  = True
                    elif srow.ST == Sts.SELL_STOP_LOSS and hit >= srow.XOR and sybl==srow.OUT : spswp = True
                    if spswp == True:
                        is_swap=AugChainZigg.swap(inpsybl=srow.IN,outsybl=srow.OUT,desired_amount_out=float(srow.XQT),st=srow.ST)
                        if is_swap == zigg.success_:
                            ix=Sts.stss.loc[Sts.stss["IX"]==srow.IX]
                            for stprow in ix.itertuples():
                                Sts.stss.drop(stprow.Index,axis=0, inplace=True)
        return
                
    def buy_low(st=None,inp=None,out=None,xor=None,xqt=None,tp=None,sl=None,expire=None,ix=None):
        if (inp==None or out==None or xqt==None or xor==None):
            try: raise Exception()
            except: Menu.error(exc="missing arguments on strategie")
            return
        
        p=Tesseract.tickss[out].iloc[-1]["XOR"]
        
        if str(xor)[0] != "%": xor = float(xor)
        elif str(xor)[0] == "%":
            xor = float(xor[1:])
            if ( xor > 0 and xor < 1): xor = p-(p*xor)
        
        if tp == None: pass
        elif str(tp)[0] != "%": tp = float(tp)
        elif str(tp)[0] == "%":
            tp = float(tp[1:])
            if (tp > 0 and tp < 1): tp = xor+(xor*tp)
            else:
                try: raise Exception()
                except: Menu.error(exc=f"wrong take profit percentage setup for {Sts.BUY_LOW}")
        if tp==None: tp = np.nan
            
        if sl == None: pass
        elif str(sl)[0] != "%": sl = float(sl)
        elif str(sl)[0] == "%":
            sl = float(sl[1:])
            if (sl > 0 and sl < 1): sl = xor-(xor*sl)
            else:
                try: raise Exception()
                except: Menu.error(exc=f"wrong take profit percentage setup for {Sts.BUY_LOW}")
                return
        if sl==None: sl = np.nan
                
        if zigg.testing ==False:
            if xor >= p:
                try: raise Exception()
                except: Menu.error(exc=f"wrong price setup for {Sts.BUY_LOW}")
                return
        if tp != None and tp <= xor:
            try: raise Exception()
            except: Menu.error(exc=f"wrong take profit setup for {Sts.BUY_LOW}")
            return
        if sl != None and sl >= xor:
            try: raise Exception()
            except: Menu.error(exc=f"wrong stop loss setup for {Sts.BUY_LOW}")
            return
        try: 
            zigg.Symbols.idss[inp]
            zigg.Symbols.idss[out]
        except KeyError:
            try: raise Exception()
            except: Menu.error(exc=f"wrong symbol name in {Sts.BUY_LOW}")
            return
        if st == None: st = Sts.BUY_LOW
        if ix == None: ix = random.randint(0,10000000)
        if expire != None: expire = (expire,timer())
        if expire == None: expire = np.nan        
        
        stdf = {"ST":st,"IN":inp,"OUT":out,"XOR":xor,"XQT":xqt,"TP":tp,"SL":sl,"EXPIRE":expire,"TIME":zigg.Tools.dateformat(),"IX":ix}
        stdf=pd.DataFrame(data=[stdf])
        Sts.stss=pd.concat((Sts.stss,stdf),axis=0,ignore_index=True)
        return
    
    def orders_strategie(st=None,inp=None,out=None,xor=None,xqt=None,tp=None,sl=None,expire=None,ix=None):
        if (inp==None or out==None or xqt==None or xor==None):
            try: raise Exception()
            except: Menu.error(exc="missing arguments on strategie")
            return        
        
        if st==Sts.BUY_LOW:
            p=Tesseract.tickss[out].iloc[-1]["XOR"]

            if str(xor)[0] != "%": xor = float(xor)
            elif str(xor)[0] == "%":
                xor = float(xor[1:])
                if ( xor > 0 and xor < 1): xor = p-(p*xor)
            
            if tp == None: pass
            elif str(tp)[0] != "%": tp = float(tp)
            elif str(tp)[0] == "%":
                tp = float(tp[1:])
                if (tp > 0 and tp < 1): tp = xor+(xor*tp)
                else:
                    try: raise Exception()
                    except: Menu.error(exc=f"wrong take profit percentage setup for {Sts.BUY_LOW}")
            if tp==None: tp = np.nan
                
            if sl == None: pass
            elif str(sl)[0] != "%": sl = float(sl)
            elif str(sl)[0] == "%":
                sl = float(sl[1:])
                if (sl > 0 and sl < 1): sl = xor-(xor*sl)
                else:
                    try: raise Exception()
                    except: Menu.error(exc=f"wrong take profit percentage setup for {Sts.BUY_LOW}")
                    return
            if sl==None: sl = np.nan
                    
            if zigg.testing ==False:
                if xor >= p:
                    try: raise Exception()
                    except: Menu.error(exc=f"wrong price setup for {Sts.BUY_LOW}")
                    return
            if tp != None and tp <= xor:
                try: raise Exception()
                except: Menu.error(exc=f"wrong take profit setup for {Sts.BUY_LOW}")
                return
            if sl != None and sl >= xor:
                try: raise Exception()
                except: Menu.error(exc=f"wrong stop loss setup for {Sts.BUY_LOW}")
                return
            
        elif st==Sts.SELL_HIGH:
            p=Tesseract.tickss[inp].iloc[-1]["XOR"]
            
            if str(xor)[0] != "%": xor = float(xor)
            elif str(xor)[0] == "%":
                xor = float(xor[1:])
                if ( xor > 0 and xor < 1): xor = p+(p*xor)
            
            if tp == None: pass
            elif str(tp)[0] != "%": tp = float(tp)
            elif str(tp)[0] == "%":
                tp = float(tp[1:])
                if (tp > 0 and tp < 1): tp = xor-(xor*tp)
                else:
                    try: raise Exception()
                    except: Menu.error(exc=f"wrong take profit percentage setup for {Sts.SELL_HIGH}")
            if tp==None: tp = np.nan
            
            if sl == None: pass
            elif str(sl)[0] != "%": sl = float(sl)
            elif str(sl)[0] == "%":
                sl = float(sl[1:])
                if (sl > 0 and sl < 1): sl = xor+(xor*sl)
                else:
                    try: raise Exception()
                    except: Menu.error(exc=f"wrong take profit percentage setup for {Sts.SELL_HIGH}")
                    return
            if sl==None: sl = np.nan
                    
            if zigg.testing == False:
                if xor <= p:
                    try: raise Exception()
                    except: Menu.error(exc=f"wrong price setup for {Sts.SELL_HIGH}")
                    return
            if tp != None and tp >= xor:
                try: raise Exception()
                except: Menu.error(exc=f"wrong take profit setup for {Sts.SELL_HIGH}")
                return
            if sl != None and sl <= xor:
                try: raise Exception()
                except: Menu.error(exc=f"wrong stop loss setup for {Sts.SELL_HIGH}")
                return
            
        """THE SAME FOR ALL ORDERS"""
        try: 
            zigg.Symbols.idss[inp]
            zigg.Symbols.idss[out]
        except KeyError:
            try: raise Exception()
            except: Menu.error(exc=f"wrong symbol name in {Sts.BUY_LOW}")
            return
        if st == None: st = Sts.BUY_LOW
        if ix == None: ix = random.randint(0,10000000)
        if expire != None: expire = (int(expire),timer())
        if expire == None: expire = np.nan
        
        stdf = {"ST":st,"IN":inp,"OUT":out,"XOR":xor,"XQT":xqt,"TP":tp,"SL":sl,"EXPIRE":expire,"TIME":zigg.Tools.dateformat(),"IX":ix}
        stdf=pd.DataFrame(data=[stdf])
        Sts.stss=pd.concat((Sts.stss,stdf),axis=0,ignore_index=True)
            
    def sell_high(st=None,inp=None,out=None,xor=None,xqt=None,tp=None,sl=None,expire=None,ix=None):
        if (inp==None or out==None or xqt==None or xor==None):
            try: raise Exception()
            except: Menu.error(exc="missing arguments on strategie")
            return
        
        p=Tesseract.tickss[inp].iloc[-1]["XOR"]
        
        if str(xor)[0] != "%": xor = float(xor)
        elif str(xor)[0] == "%":
            xor = float(xor[1:])
            if ( xor > 0 and xor < 1): xor = p+(p*xor)
        
        if tp == None: pass
        elif str(tp)[0] != "%": tp = float(tp)
        elif str(tp)[0] == "%":
            tp = float(tp[1:])
            if (tp > 0 and tp < 1): tp = xor-(xor*tp)
            else:
                try: raise Exception()
                except: Menu.error(exc=f"wrong take profit percentage setup for {Sts.SELL_HIGH}")
        if tp==None: tp = np.nan
        
        if sl == None: pass
        elif str(sl)[0] != "%": sl = float(sl)
        elif str(sl)[0] == "%":
            sl = float(sl[1:])
            if (sl > 0 and sl < 1): sl = xor+(xor*sl)
            else:
                try: raise Exception()
                except: Menu.error(exc=f"wrong take profit percentage setup for {Sts.SELL_HIGH}")
                return
        if sl==None: sl = np.nan
                
        if zigg.testing == False:
            if xor <= p:
                try: raise Exception()
                except: Menu.error(exc=f"wrong price setup for {Sts.SELL_HIGH}")
                return
        if tp != None and tp >= xor:
            try: raise Exception()
            except: Menu.error(exc=f"wrong take profit setup for {Sts.SELL_HIGH}")
            return
        if sl != None and sl <= xor:
            try: raise Exception()
            except: Menu.error(exc=f"wrong stop loss setup for {Sts.SELL_HIGH}")
            return
        try: 
            zigg.Symbols.idss[inp]
            zigg.Symbols.idss[out]
        except KeyError:
            try: raise Exception()
            except: Menu.error(exc=f"wrong symbol name in {Sts.SELL_HIGH}")
            return
        if st == None: st = Sts.SELL_HIGH
        if ix == None: ix = random.randint(0,10000000)
        if expire != None: expire = (expire,timer())
        if expire == None: expire = np.nan
        
        stdf = {"ST":st,"IN":inp,"OUT":out,"XOR":xor,"XQT":xqt,"TP":tp,"SL":sl,"EXPIRE":expire,"TIME":zigg.Tools.dateformat(),"IX":ix}
        stdf=pd.DataFrame(data=[stdf])
        Sts.stss=pd.concat((Sts.stss,stdf),axis=0,ignore_index=True)
        return
    
    class Lstm:   
        mu = None
        std = None
        window_size = 13
        train_split_size = 0.74
        batch_size = 39
        num_epoch = 37
        device = "cpu"
        input_size = 1
        lstm_size = 24
        num_stm_layers = 1
        dropout = 0.13
        learning_rate = 0.0246
        scheduler_step_size = 13
        def augchainzigg(sybl=None,col=None, model=None,path=zigg.lstm):#dont delete model=None
            try:
                if col == "XOR": tick = Tesseract.tickss[sybl]
                elif col == "+CZ": tick = Tesseract.aczss[sybl]
            except KeyError: return
            try:tick=tick.groupby(by=pd.Grouper(key="TIME", axis=0, freq='1min')).agg(["mean"])
            except TypeError: return 0
            tick.columns=tuple(map(lambda x:x[0],tuple(tick.columns)))
            tick.reset_index(drop=False, inplace=True)
            regress = -(AugChainZigg.lstm_data_load)
            tick,retry =tick[regress:],0
            while True:
                tick=tick.dropna(axis=0)
                if len(tick.index) < AugChainZigg.lstm_data_load and retry < 9:
                    regress = int(regress*1.25)
                    tick=tick[regress:]
                    retry += 1
                    continue
                if len(tick.index) > AugChainZigg.lstm_data_load: tick=tick[-(AugChainZigg.lstm_data_load):]
                break
            if Sts.ststate.get(Sts.LSTM,None)==None: Sts.ststate[Sts.LSTM] = {}
            if Sts.ststate.get(Sts.LSTM).get(sybl,None)==None: Sts.ststate[Sts.LSTM][sybl]={}
            if Sts.ststate["LSTM"][sybl].get("MODEL",None) == None: Sts.ststate[Sts.LSTM][sybl]["MODEL"] = {}
            if Sts.ststate["LSTM"][sybl]["MODEL"].get(col,None) == None: 
                Sts.ststate["LSTM"][sybl]["MODEL"][col] = None
                is_model = None
            else: 
                model = Sts.ststate["LSTM"][sybl]["MODEL"][col]
                is_model = True
            try:
                if is_model == None:
                    with open(Path(path,f"[{sybl}]{col}.pkl"),'rb') as m:
                        model=pickle.load(m)
                    Sts.ststate["LSTM"][sybl]["MODEL"][col] = model
                    is_model = True
            except FileNotFoundError: pass
            """normalize_data"""
            Sts.Lstm.mu = np.mean(tick[col], axis=0)
            Sts.Lstm.std = np.std(tick[col], axis=0)
            normtk = ((tick[col] - Sts.Lstm.mu)/Sts.Lstm.std).to_numpy()
            """prepare_data_x"""
            n_row = normtk.shape[0] - Sts.Lstm.window_size + 1
            output = np.lib.stride_tricks.as_strided(normtk, shape=(n_row, Sts.Lstm.window_size), strides=(normtk.strides[0], normtk.strides[0]))
            data_x, data_x_unseen = output[:-1], output[-1]     
            """prepare_data_y"""
            data_y = normtk[Sts.Lstm.window_size:]
            """split dataset"""
            split_index = int(data_y.shape[0]*Sts.Lstm.train_split_size)
            data_x_train = data_x[:split_index]
            data_x_val = data_x[split_index:]
            data_y_train = data_y[:split_index]
            data_y_val = data_y[split_index:]
            """Convert into [batch, sequence, features]"""     
            dataset_train = Sts.Lstm.TimeSeriesDataset(data_x_train, data_y_train)
            dataset_val = Sts.Lstm.TimeSeriesDataset(data_x_val, data_y_val)
            
            train_dataloader = torch.utils.data.DataLoader(dataset_train, batch_size=Sts.Lstm.batch_size, shuffle=True)
            val_dataloader = torch.utils.data.DataLoader(dataset_val, batch_size=Sts.Lstm.batch_size, shuffle=True)
            
            #print(f"{sybl} | {dataset_train.x.shape} | Augment Chain Ziggurat")
            
            train_dataloader = torch.utils.data.DataLoader(dataset_train, batch_size=Sts.Lstm.batch_size, shuffle=True)
            val_dataloader = torch.utils.data.DataLoader(dataset_val, batch_size=Sts.Lstm.batch_size, shuffle=True)
            
            if model == None:
                model = Sts.Lstm.LSTMModel(input_size=Sts.Lstm.input_size, hidden_layer_size=Sts.Lstm.lstm_size, num_layers=Sts.Lstm.num_stm_layers, output_size=1, dropout=Sts.Lstm.dropout)
            model = model.to(Sts.Lstm.device)
        
            criterion = torch.nn.MSELoss()
            optimizer = torch.optim.Adam(model.parameters(), lr=Sts.Lstm.learning_rate, betas=(0.841337, 0.971337), eps=1e-9)
            #optimizer = torch.optim.RMSprop(model.parameters(), lr=Sts.Lstm.learning_rate,momentum=0.37, alpha=0.13, eps=1e-9, centered=False)
            scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=Sts.Lstm.scheduler_step_size, gamma=0.1)
            
            lt_eval,lr_eval=[],[]
            if is_model == None:
                for epoch in range(Sts.Lstm.num_epoch):
                    loss_train, lr_train = Sts.Lstm.run_epoch(loader=train_dataloader,model=model,optimizer=optimizer,criterion=criterion,scheduler=scheduler, is_training=True)
                    loss_val, lr_val = Sts.Lstm.run_epoch(loader=val_dataloader,model=model,optimizer=optimizer,criterion=criterion,scheduler=scheduler)
                    lt_eval.append(loss_train)
                    lr_eval.append(loss_val)
                    scheduler.step()
                    print('{} | Epoch[{}/{}] | loss train:{:.6f}, test:{:.6f} | lr:{:.6f}'.format(sybl, epoch+1, Sts.Lstm.num_epoch, loss_train, loss_val, lr_train))
                print(f"{sybl} | LT : {np.array(lt_eval).mean()} LR : {np.array(lr_eval).mean()} | Augment Chain Ziggurat")
            model.eval()
            Sts.ststate[Sts.LSTM][sybl]["MODEL"][col]=model
            
            if is_model == None:
                with open(Path(path,f"[{sybl}]{col}.pkl"),'wb') as m:
                    pickle.dump(model, m)
            
            x = torch.tensor(data_x_unseen).float().to(Sts.Lstm.device).unsqueeze(0).unsqueeze(2) # this is the data type and shape required, [batch, sequence, feature]
            prediction = model(x)
            prediction = prediction.cpu().detach().numpy()
            pred_=Sts.Lstm.inverse_transform(prediction)[0]
            return pred_
        def inverse_transform(x):
            return ((x*Sts.Lstm.std) + Sts.Lstm.mu)
        def run_epoch(loader=None, model=None,optimizer=None,criterion=None,scheduler=None,is_training=False):
            epoch_loss = 0
            if is_training: model.train()
            else: model.eval()
            for idx, (x, y) in enumerate(loader):
                if is_training: optimizer.zero_grad()
                batchsize = x.shape[0]
                x = x.to(Sts.Lstm.device)
                y = y.to(Sts.Lstm.device)
                out = model(x)
                loss = criterion(out.contiguous(), y.contiguous())
                if is_training:
                    loss.backward()
                    optimizer.step()
                epoch_loss += (loss.detach().item() / batchsize)
            lr = scheduler.get_last_lr()[0]
            return epoch_loss, lr
        class LSTMModel(torch.nn.Module):
            def __init__(self, input_size=1, hidden_layer_size=None, num_layers=2, output_size=1, dropout=0.2):
                super().__init__()
                self.hidden_layer_size = hidden_layer_size
                self.linear_1 = torch.nn.Linear(input_size, hidden_layer_size)
                self.relu = torch.nn.ReLU()
                self.lstm = torch.nn.LSTM(hidden_layer_size, hidden_size=self.hidden_layer_size, num_layers=num_layers, batch_first=True)
                self.dropout = torch.nn.Dropout(dropout)
                self.linear_2 = torch.nn.Linear(num_layers*hidden_layer_size, output_size)
                self.bias=True
                self.bidirectional=False
                self.return_sequences=False
                self.init_weights()          
            def init_weights(self):
                for name, param in self.lstm.named_parameters():
                    if 'bias' in name:
                        torch.nn.init.constant_(param, 0.13)
                    elif 'weight_ih' in name:
                        torch.nn.init.kaiming_normal_(param)
                    elif 'weight_hh' in name:
                        torch.nn.init.orthogonal_(param)
            def forward(self, x):
                batchsize = x.shape[0]
                # layer 1
                x = self.linear_1(x)
                x = self.relu(x)
                # LSTM layer
                lstm_out, (h_n, c_n) = self.lstm(x)
                # reshape output from hidden cell into [batch, features] for `linear_2`
                x = h_n.permute(1, 0, 2).reshape(batchsize, -1) 
                # layer 2
                x = self.dropout(x)
                predictions = self.linear_2(x)
                return predictions[:,-1]
        class TimeSeriesDataset(torch.utils.data.Dataset):
            def __init__(self, x, y):
                x = np.expand_dims(x, 2) # in our case, we have only 1 feature, so we need to convert `x` into [batch, sequence, features] for LSTM
                self.x = x.astype(np.float32)
                self.y = y.astype(np.float32)
            def __len__(self):
                return len(self.x)
            def __getitem__(self, idx):
                return (self.x[idx], self.y[idx]) 

class Tesseract:
    def xbal(pss=None,sybl=None):
        """Log 0.01"""
        if sybl != "XOR":
            try: pss.loc[sybl,"XBAL"]=round( Tesseract.balancess.loc[sybl,"BALANCE"]*(Tesseract.tickss[sybl]["XOR"].iloc[-1]), 2)
            except AttributeError:pss.loc[sybl,"XBAL"]=0.0
        elif sybl == "XOR":
            try: pss.loc[sybl,"XBAL"]=Tesseract.balancess.loc["XOR","BALANCE"].round(decimals=2)
            except AttributeError:pss.loc[sybl,"XBAL"]=0.0
        pss.loc[sybl,"XBAL"]=round( (pss.loc[sybl,"XBAL"]*0.01), 2 )#Log0.1
        return pss.loc[sybl,"XBAL"]#RETURN ROW X COLUM!
    def load_tickss():
        Tesseract.tickss={}
        Tesseract.tickscols = [zigg.dateixname_,"XOR","POOL"]
        for sybl in AugChainZigg.symbolss:
            Tesseract.tickss[sybl]=pd.DataFrame(columns=Tesseract.tickscols)
            Tesseract.tickss[sybl]=pd.concat((Tesseract.tickss[sybl],zigg.Tools.pickle(path=zigg.ticks,name=sybl,load=True)),axis=0)
            if Tesseract.tickss[sybl].isnull().values.any() == True:
                try:raise Exception()
                except: zigg.Tools.error(exc="NAN VALUES FOUND WHEN LOADING DATA")
                Tesseract.tickss[sybl].dropna(axis=0,inplace=True)
            if Tesseract.tickss[sybl].empty == False:
                for col in Tesseract.tickss[sybl].columns:
                    try: Tesseract.tickss[sybl][col] = tuple(map(float,Tesseract.tickss[sybl][col]))
                    except (ValueError,TypeError): pass
                Tesseract.tickss[sybl]["TIME"]=pd.to_datetime(Tesseract.tickss[sybl]["TIME"])
                Tesseract.tickss[sybl]=Tesseract.tickss[sybl][-106560:]
    def load_aczss():
        Tesseract.aczss={}
        Tesseract.aczscols = [zigg.dateixname_,"+CZ"]
        for sybl in AugChainZigg.symbolss:
            Tesseract.aczss[sybl]=pd.DataFrame(columns=Tesseract.aczscols)
            Tesseract.aczss[sybl]=pd.concat((Tesseract.aczss[sybl],zigg.Tools.pickle(path=zigg.aczs,name=sybl,load=True)),axis=0)
            if Tesseract.aczss[sybl].isnull().values.any() == True:
                try:raise Exception()
                except: zigg.Tools.error(exc="NAN VALUES FOUND WHEN LOADING DATA")
                Tesseract.aczss[sybl].dropna(axis=0,inplace=True)
            if Tesseract.aczss[sybl].empty == False:
                for col in Tesseract.aczss[sybl].columns:
                    try: Tesseract.aczss[sybl][col] = tuple(map(float,Tesseract.aczss[sybl][col]))
                    except (ValueError,TypeError): pass
                Tesseract.aczss[sybl]["TIME"]=pd.to_datetime(Tesseract.aczss[sybl]["TIME"])
                Tesseract.aczss[sybl]=Tesseract.aczss[sybl][-106560:]
    def save_tickss():
        for sybl,stk in Tesseract.tickss.items():
            tkss=stk.copy(deep=True)
            tkss=tkss.groupby(by=pd.Grouper(key='TIME', axis=0, freq='1min')).mean()
            if tkss.isnull().values.any() == True: tkss.dropna(axis=0,inplace=True)
            tkss.reset_index(drop=False, inplace=True)
            Tesseract.tickss[sybl]=tkss.copy(deep=True)
            zigg.Tools.pickle(
                df=tkss,path=zigg.ticks,name=sybl,save=True)
            del tkss
        print("<TICKS SAVED>")
            
    def reset_lstm(sybl):
        try: os.remove(Path(zigg.lstm,f"[{sybl}]XOR.pkl"))
        except FileNotFoundError: pass
        Sts.Lstm.augchainzigg(sybl=sybl,col="XOR",path=zigg.lstm)
        
    def save_aczss():
        for sybl,stk in Tesseract.aczss.items():
            tkss=stk.copy(deep=True)
            tkss["TIME"]=pd.to_datetime(tkss["TIME"])
            tkss=tkss.groupby(by=pd.Grouper(key='TIME', axis=0, freq='1min')).mean()
            if tkss.isnull().values.any() == True: tkss.dropna(axis=0,inplace=True)
            tkss.reset_index(drop=False, inplace=True)
            Tesseract.aczss[sybl]=tkss.copy(deep=True)
            zigg.Tools.pickle(
                df=tkss,path=zigg.aczs,name=sybl,save=True)
            del tkss
            
    def save_state():
        zigg.Tools.pickle(df=Tesseract.portfolioss,path=zigg.database,name=zigg.portfolio_,save=True)
        exopkl = Tesseract.exorderss[["IN","OUT","IN_QT","OUT_QT","IN_XOR","OUT_XOR","OUT_XQT","ST","EXT_HASH",zigg.dateixname_]].copy(deep=True)
        zigg.Tools.pickle(df=exopkl,path=zigg.database,name=zigg.exorders_,save=True)
        for sybl in AugChainZigg.aczswpss:
            Sts.ststate["LSTM"][sybl]["MODEL"] = None
        zigg.Tools.pickle(df=Sts.ststate, path=zigg.ststate, save=True, load=None, json=True)
        print("<STATE SAVED>")
            
    def save_portfolioss():
        zigg.Tools.pickle(df=Tesseract.portfolioss,path=zigg.database,name=zigg.portfolio_,save=True)
        exopkl = Tesseract.exorderss[["IN","OUT","IN_QT","OUT_QT","IN_XOR","OUT_XOR","OUT_XQT","ST","EXT_HASH",zigg.dateixname_]].copy(deep=True)
        zigg.Tools.pickle(df=exopkl,path=zigg.database,name=zigg.exorders_,save=True)
        
        
    def sora_watcher():
        while True:
            for sybl in AugChainZigg.symbolss:
                id_ = zigg.Symbols.idss[sybl]
                if sybl=="XOR":
                    inpid=id_
                    outid=zigg.Symbols.idss["XSTUSD"]
                elif sybl!="XOR":
                    inpid=id_
                    outid=zigg.Symbols.idss["XOR"]
                price = zigg.Sora.liquidityProxy_quote(input_asset_id=inpid, output_asset_id=outid, amount=10**18)
                price = int(price["result"]["amount_without_impact"])
                price=price/10**18
                
                tick = pd.DataFrame(columns=Tesseract.tickscols, data=[[zigg.Tools.dateformat(),price,0]])
                tick["TIME"]=pd.to_datetime(tick["TIME"])
                
                time.sleep(1)
                
                Tesseract.tickss[sybl]=pd.concat((Tesseract.tickss[sybl],tick),axis=0,ignore_index=True)
    
    def correlation():
        corrdf=pd.DataFrame(columns=[AugChainZigg.symbolss])
        n_rows = {}
        for sybl in AugChainZigg.symbolss:
            tkss = Tesseract.tickss[sybl].copy(deep=True)
            tkss=tkss.groupby(by=pd.Grouper(key='TIME', axis=0, freq='1min')).mean()
            #tkss=tkss.groupby(by=pd.Grouper(key="TIME", axis=0, freq='1min')).agg(["mean"])
            tkss.columns=tuple(map(lambda x:x[0],tuple(tkss.columns)))
            tkss.reset_index(drop=False, inplace=True)            
            tkss=tkss[-1440:]
            corrdf[sybl]=tkss["XOR"].values
            corrdf.dropna(axis=0, inplace=True)
        #corrdf.dropna(axis=0,inplace=True)
        try: 
            corr_d=corrdf.corr(method="pearson")
            print(corr_d)
        except : Zigg.Tools.error(exc="Axis are misaligned, wait for 1440 ticks or fix the code.")   
    def load_exorderss():
        Tesseract.exordercols = ["IN","IN_BQT","IN_AQT","IN_QT", "IN_BXQT","IN_AXQT","IN_XQT","IN_BXOR","IN_AXOR","IN_XOR","OUT","OUT_BQT", "OUT_AQT","OUT_QT","OUT_BXQT","OUT_AXQT","OUT_XQT","OUT_BXOR","OUT_AXOR","OUT_XOR","ST","TX_COST","EXT_HASH",zigg.dateixname_]
        Tesseract.exorderss=None
        Tesseract.exorderss=zigg.Tools.pickle(path=zigg.database, name=zigg.exorders_,load=True)
        if Tesseract.exorderss.empty == True:
            Tesseract.exorderss = pd.DataFrame(columns=Tesseract.exordercols)
        else:
            for col in Tesseract.exorderss.columns:
                try: Tesseract.exorderss[col] = tuple(map(float,Tesseract.exorderss[col]))
                except ValueError: pass
    def load_portfolioss():
        """LOAD PORTFOLIOSS"""
        portfoliocols = ["CHG%","QT","XQT","XOR", "XPRF"]
        Tesseract.portfolioss=None
        Tesseract.portfolioss=zigg.Tools.pickle(path=zigg.database,name=zigg.portfolio_,load=True)
        if Tesseract.portfolioss.empty == True:
            Tesseract.portfolioss = pd.DataFrame(data=(np.zeros((len(AugChainZigg.symbolss), len(portfoliocols)))),columns=portfoliocols,index=[AugChainZigg.symbolss])        
        if isinstance(Tesseract.portfolioss.index,pd.MultiIndex):
            Tesseract.portfolioss.index=Tesseract.portfolioss.reset_index(level=0).set_index("level_0").index
            Tesseract.portfolioss.index.name=None
        for col in Tesseract.portfolioss.columns:
            try:
                Tesseract.portfolioss[col] = tuple(map(float,Tesseract.portfolioss[col]))
            except ValueError: pass
        for sybl in AugChainZigg.symbolss:
            if sybl not in Tesseract.portfolioss.index:
                miss=pd.DataFrame(data=(np.zeros((1, len(portfoliocols)))),columns=portfoliocols,index=[sybl])
                Tesseract.portfolioss=pd.concat((Tesseract.portfolioss,miss),axis=0)
    def load_aczdata():
        AugChainZigg.aczdatacols=(zigg.dateixname_,"TASK")
        AugChainZigg.aczdata=pd.DataFrame(columns=AugChainZigg.aczdatacols)
        AugChainZigg.aczdata=pd.concat((AugChainZigg.aczdata,zigg.Tools.pickle(path=zigg.database,name="ACZDATA",load=True)),axis=0)
        if AugChainZigg.aczdata.empty==True:
            today=pd.DataFrame(data=[[zigg.Tools.dateformat(),"TODAY"]],columns=AugChainZigg.aczdatacols,dtype=str)
            alphav=pd.DataFrame(data=[[zigg.Tools.dateformat(past=1),"HISTORICALSS"]],columns=AugChainZigg.aczdatacols,dtype=str)
            AugChainZigg.aczdata=pd.concat((AugChainZigg.aczdata,today),axis=0)
            AugChainZigg.aczdata=pd.concat((AugChainZigg.aczdata,alphav),axis=0)
        AugChainZigg.aczdata["TIME"]=pd.to_datetime(AugChainZigg.aczdata["TIME"])
    def load_historicalss():
        alpha_sybls = ("ETH","BTC","GRT","KSM","RLC")
        Tesseract.avc=0
        Tesseract.historicalss , histsybls = {},[]
        avtss=CryptoCurrencies(key='UQXKR9SNHY12OVKV',output_format='pandas')
        Tesseract.ohlccolss=[zigg.dateixname_,"OPEN","HIGH","LOW","CLOSE","VOL"]
        for sybl in alpha_sybls:
            Tesseract.historicalss[sybl] = pd.DataFrame(columns=Tesseract.ohlccolss)
            Tesseract.historicalss[sybl]=Tesseract.historicalss[sybl].append( zigg.Tools.pickle(path=zigg.historical,name=sybl,load=True) )
            Tesseract.historicalss[sybl].drop_duplicates(subset=["TIME"],keep="first",inplace=True)
            if Tesseract.historicalss[sybl].isnull().values.any() == True:
                try:raise Exception()
                except: zigg.Tools.error(exc="NAN VALUES FOUND WHEN LOADING DATA")
                Tesseract.historicalss[sybl].dropna(axis=0,inplace=True)
            if AugChainZigg.aczdata[AugChainZigg.aczdata["TASK"]=="HISTORICALSS"]["TIME"][0].day!=pd.Timestamp(datetime.datetime.today()).day:
                df,meta_data = avtss.get_digital_currency_daily(symbol=sybl, market="USD")
                df=df.drop(['1b. open (USD)','2b. high (USD)','3b. low (USD)','4b. close (USD)','6. market cap (USD)'],axis=1)
                df.rename(mapper = {'1a. open (USD)':'OPEN' ,'2a. high (USD)':'HIGH',"3a. low (USD)":"LOW","4a. close (USD)":"CLOSE","5. volume":"VOL"},axis=1,inplace=True)
                df=df.iloc[::-1]
                df.index.name=zigg.dateixname_
                df.reset_index(inplace=True, drop=False)
                Tesseract.historicalss[sybl]=df
                time.sleep(0.1)
        if Tesseract.historicalss[sybl].empty == False:
            for col in Tesseract.historicalss[sybl].columns:
                try: Tesseract.historicalss[sybl][col] = Tesseract.historicalss[sybl][col].apply(lambda x : float(x))
                except (ValueError,TypeError): pass
            Tesseract.historicalss[sybl]["TIME"]=Tesseract.historicalss[sybl]["TIME"].apply(lambda x:f'{x} 00:00:00')
            Tesseract.historicalss[sybl]["TIME"]=pd.to_datetime(Tesseract.historicalss[sybl]["TIME"])
        else: zigg.Tools.error(exc="EMPTY HISTORICALSS")
        if AugChainZigg.aczdata[AugChainZigg.aczdata["TASK"]=="HISTORICALSS"]["TIME"][0].day!=pd.Timestamp(datetime.datetime.today()).day:
            for sybl,stk in Tesseract.historicalss.items():
                htss=stk.copy(deep=True)
                htss=htss.astype(str)
                if htss.isnull().values.any() == True:
                    htss.dropna(axis=0,inplace=True)
                    try:raise Exception()
                    except: zigg.Tools.error(exc="NAN VALUES FOUND WHEN SAVING DATA")
                zigg.Tools.pickle(df=htss,path=zigg.historical,name=sybl,save=True)
                del htss
        AugChainZigg.aczdata[AugChainZigg.aczdata["TASK"]=="HISTORICALSS"]=pd.Series(data=[zigg.Tools.dateformat(),"HISTORICALSS"],index=AugChainZigg.aczdatacols,dtype=str)
        zigg.Tools.pickle(df=AugChainZigg.aczdata, path=zigg.database, name="ACZDATA", save=True)
    def quantity(desired_amount_out=None,inpsybl=None,outsybl=None,st=None,menu=False):
        exord=pd.Series(index=Tesseract.exordercols, data=([0.0]*len(Tesseract.exordercols)),dtype=float)
        exord["ST"]=st
        exord["IN"] = inpsybl
        exord["OUT"] = outsybl
        if outsybl == "XOR":
            while True:
                try:
                    exord["IN_BXOR"]=Tesseract.tickss[inpsybl].iloc[-1]['XOR']
                    exord["OUT_BXOR"]=Tesseract.tickss[inpsybl].iloc[-1]['XOR']
                except IndexError:
                    time.sleep(0.25)
                    continue
                break
        elif inpsybl != "XOR" and outsybl != "XOR":     
            while True:
                try:
                    exord["IN_BXOR"]=Tesseract.tickss[inpsybl].iloc[-1]['XOR']
                    exord["OUT_BXOR"]=Tesseract.tickss[outsybl].iloc[-1]['XOR']
                except IndexError: 
                    time.sleep(0.25)
                    continue           
                break
        elif outsybl != "XOR":
            while True:
                try:
                    exord["IN_BXOR"]=Tesseract.tickss[outsybl].iloc[-1]['XOR']
                    exord["OUT_BXOR"]=Tesseract.tickss[outsybl].iloc[-1]['XOR']
                except IndexError:
                    time.sleep(0.25)
                    continue            
                break
        """OUT_QUANTITY"""#NEVER CHANGE
        try:desired_amount_out=float(desired_amount_out)
        except ValueError: return None
        exord["OUT_BQT"]=desired_amount_out/exord["OUT_BXOR"]
        exord["OUT_BXQT"]=exord["OUT_BQT"]*exord["OUT_BXOR"]
        """INP QUANTITY"""#NEVER CHANGE
        exord["IN_BQT"]=desired_amount_out/exord["IN_BXOR"]
        exord["IN_BXQT"]=exord["IN_BQT"]*exord["IN_BXOR"]
        if zigg.testing==False:
            try: Tesseract.balancess
            except AttributeError: Tesseract.balance(all=False,sybls=(inpsybl,outsybl))
            if Tesseract.balancess.loc[inpsybl].isnull()[0]==True or Tesseract.balancess.loc[outsybl].isnull()[0]==True:
                Tesseract.balance(all=False,sybls=(inpsybl,outsybl))
        if inpsybl != "XOR":
            in_balance=(Tesseract.balancess.loc[inpsybl][0]*Tesseract.tickss[inpsybl].iloc[-1]["XOR"])
        else: in_balance=Tesseract.balancess.loc[inpsybl][0]
        if outsybl != "XOR":
            out_balance=(Tesseract.balancess.loc[outsybl][0]*Tesseract.tickss[outsybl].iloc[-1]["XOR"])
        else: out_balance=Tesseract.balancess.loc[outsybl][0]
        try:
            if Tesseract.portfolioss.loc[inpsybl,"XOR"] != 0:
                in_chg=(((Tesseract.tickss[inpsybl].iloc[-1]["XOR"]/Tesseract.portfolioss.loc[inpsybl,"XOR"])-1)*100)
            else: in_chg = 0
            if Tesseract.portfolioss.loc[outsybl,"XOR"] != 0:
                out_chg=(((Tesseract.tickss[outsybl].iloc[-1]["XOR"]/Tesseract.portfolioss.loc[outsybl,"XOR"])-1)*100 )
            else: out_chg = 0
        except KeyError: in_chg, out_chg = 0,0
        if inpsybl=="XOR":
            in_bqt=exord["IN_BXQT"]
            in_xor=Tesseract.tickss["XOR"].iloc[-1]["XOR"]
        else:
            in_bqt=exord["IN_BQT"]
            in_xor=exord["IN_BXOR"]
        if outsybl=="XOR":
            out_bqt=exord["OUT_BXQT"]
            out_xor=Tesseract.tickss["XOR"].iloc[-1]["XOR"]
        else:
            out_bqt=exord["OUT_BQT"]
            out_xor=exord["OUT_BXOR"]
        show_swap=pd.DataFrame(index=[inpsybl,outsybl],columns=["XBALANCE","CHG%","QT","XQT","XOR"],data=[[in_balance,in_chg,exord["IN_BQT"],exord["IN_BXQT"],exord["IN_BXOR"]],[out_balance, out_chg,exord["OUT_BQT"],exord["OUT_BXQT"],exord["OUT_BXOR"]]])
        if st == Sts.MANUAL: print(show_swap)
        if not in_balance >= (exord["IN_BXQT"]*AugChainZigg.slippage):
            try: raise Exception()
            except:
                if st == Sts.MANUAL:zigg.Tools.error(exc="not enough balance", normal=True)
            if menu == True: exord=Tesseract.quantity(desired_amount_out=1.01, inpsybl=inpsybl, outsybl=outsybl, menu=False)
            elif menu == False: return None#AugChainZigg.swap(inpsybl=inpsybl, outsybl=outsybl, desired_amount_out=desired_amount_out, st=st, test=test, menu=menu)
            return None
        return exord
    def upt_portfolio(exord:pd.DataFrame=None, test=None):
        exord[zigg.dateixname_] = zigg.Tools.dateformat()  
        pss = Tesseract.portfolioss.copy(deep=True)
        inpsybl,outsybl = exord["IN"], exord["OUT"]
        x=1
        if outsybl == "XOR":
            exord["IN_AXOR"]=Tesseract.tickss[inpsybl].iloc[-1]['XOR']
            exord["OUT_AXOR"]=Tesseract.tickss[inpsybl].iloc[-1]['XOR']
        if outsybl != "XOR" and inpsybl != "XOR":
            exord["IN_AXOR"]=Tesseract.tickss[inpsybl].iloc[-1]['XOR']
            exord["OUT_AXOR"]=Tesseract.tickss[outsybl].iloc[-1]['XOR']
        elif outsybl != "XOR":
            exord["IN_AXOR"]=Tesseract.tickss[outsybl].iloc[-1]['XOR']
            exord["OUT_AXOR"]=Tesseract.tickss[outsybl].iloc[-1]['XOR']
        exord["IN_XOR"]=(exord["IN_AXOR"]+exord["IN_BXOR"])/2
        try:exord["IN_AQT"]=((exord["IN_BQT"]*exord["IN_BXOR"])/(exord["IN_BQT"]*exord["IN_AXOR"]))*exord["IN_BQT"]
        except RuntimeWarning: exord["IN_AQT"]=exord["IN_BQT"]
        exord["IN_QT"]=(exord["IN_BQT"]+exord["IN_AQT"])/2
        exord["IN_AXQT"]=exord["IN_BQT"]*exord["IN_AXOR"]
        try:exord["IN_XQT"]=(exord["IN_BXQT"]+exord["IN_AXQT"])/2
        except RuntimeWarning: exord["IN_XQT"]=exord["IN_XQT"]
        exord["OUT_XOR"]=(exord["OUT_AXOR"]+exord["OUT_BXOR"])/2
        exord["OUT_AQT"]=((exord["OUT_BQT"]*exord["OUT_BXOR"])/(exord["OUT_BQT"]*exord["OUT_AXOR"]))*exord["OUT_BQT"]
        exord["OUT_QT"]=(exord["OUT_BQT"]+exord["OUT_AQT"])/2
        exord["OUT_AXQT"]=exord["OUT_BQT"]*exord["OUT_AXOR"]
        exord["OUT_XQT"]=(exord["OUT_BXQT"]+exord["OUT_AXQT"])/2
        if inpsybl == "XOR" or outsybl == "XOR":
            exord["TX_COST"]=0.0007+(exord["OUT_XQT"]*0.0003)
        elif inpsybl != "XOR" and outsybl != "XOR":
            exord["TX_COST"]=0.0007+0.0007+(exord["OUT_XQT"]*0.0006)
        if pss.loc[inpsybl, "XQT"] == 0:
            if inpsybl == "XOR":
                """IS XOR"""
                pss.loc["XOR","XQT"]=pss.loc["XOR","XQT"]-exord["IN_XQT"]
                pss.loc["XOR","QT"]=pss.loc["XOR","XQT"]
                """NOT XOR"""
                pss.loc[outsybl,"XQT"]=pss.loc[outsybl,"XQT"]+exord["OUT_XQT"]
                pss.loc[outsybl,"QT"]=pss.loc[outsybl,"QT"]+exord["OUT_QT"]
                pss.loc[outsybl,"XOR"]=exord["OUT_XOR"]
                pss.loc[outsybl,"XPRF"]=pss.loc[outsybl,"XPRF"]-exord["TX_COST"]
            elif inpsybl != "XOR" and outsybl == "XOR":
                """NOT XOR"""
                pss.loc[inpsybl,"QT"]=pss.loc[inpsybl,"QT"]-exord["IN_QT"]
                pss.loc[inpsybl,"XQT"]=pss.loc[inpsybl,"XQT"]-exord["IN_XQT"]
                pss.loc[inpsybl,"XOR"]=exord["IN_XOR"]
                pss.loc[inpsybl,"XPRF"]=pss.loc[inpsybl,"XPRF"]-exord["TX_COST"]
                """IS XOR"""
                pss.loc["XOR","XQT"]=pss.loc["XOR", "XQT"]+exord["OUT_XQT"]
                pss.loc["XOR","QT"]=pss.loc["XOR", "XQT"]
                pss.loc["XOR","XOR"]=((abs(pss.loc["XOR","XQT"])*Tesseract.tickss["XOR"].iloc[-1]['XOR'])+(exord["OUT_XQT"]*Tesseract.tickss["XOR"].iloc[-1]['XOR']))/(abs(pss.loc["XOR","QT"])+exord["OUT_XQT"])
            elif inpsybl != "XOR" and outsybl != "XOR":
                """NOT XOR"""
                pss.loc[inpsybl,"QT"]=pss.loc[inpsybl,"QT"]-exord["IN_QT"]
                pss.loc[inpsybl,"XQT"]=pss.loc[inpsybl,"XQT"]-exord["IN_XQT"]
                pss.loc[inpsybl,"XOR"]=exord["IN_XOR"]
                """NOT XOR"""
                pss.loc[outsybl,"QT"]=pss.loc[outsybl,"QT"]+exord["OUT_QT"]
                pss.loc[outsybl,"XQT"]=pss.loc[outsybl,"XQT"]+exord["OUT_XQT"]
                pss.loc[outsybl,"XOR"]=exord["OUT_XOR"]
                pss.loc[outsybl,"XPRF"]=pss.loc[outsybl,"XPRF"]-exord["TX_COST"]
        elif pss.loc[inpsybl, "XQT"] != 0:
            if outsybl != 'XOR':
                """average_price"""
                pss.loc[outsybl,"XOR"] = ((abs(pss.loc[outsybl,"QT"])*pss.loc[outsybl,"XOR"])+(exord["OUT_QT"]*exord["OUT_XOR"]))/(abs(pss.loc[outsybl,"QT"])+exord["OUT_QT"])
            elif outsybl == "XOR":
                pss.loc["XOR","XOR"] = ((abs(pss.loc["XOR","XQT"])*Tesseract.tickss["XOR"].iloc[-1]['XOR'])+(exord["OUT_XQT"]*Tesseract.tickss["XOR"].iloc[-1]['XOR']))/(abs(pss.loc["XOR","XQT"])+exord["OUT_XQT"])
            if inpsybl != "XOR":
                """profit"""
                pss.loc[inpsybl, "XPRF"]=(((((exord["IN_XOR"]-pss.loc[inpsybl,"XOR"])/pss.loc[inpsybl,"XOR"]))*abs(exord["IN_XQT"]))+pss.loc[inpsybl, "XPRF"])-exord["TX_COST"]
            elif inpsybl == "XOR":
                try: 
                    pss.loc[inpsybl, "XPRF"]=(((((Tesseract.tickss["XOR"].iloc[-1]['XOR']-pss.loc["XOR","XOR"])/pss.loc["XOR","XOR"]))*abs(exord["IN_XQT"]))+pss.loc["XOR","XPRF"])-exord["TX_COST"]
                except ZeroDivisionError: pss.loc[inpsybl, "XPRF"] = 0
            """QT IN | QT OUT"""
            if inpsybl == "XOR":
                """IS XOR"""
                pss.loc["XOR","XQT"]=pss.loc["XOR","XQT"]-exord["IN_XQT"]
                pss.loc["XOR","QT"]=pss.loc["XOR","XQT"]
                """NOT XOR"""
                pss.loc[outsybl, "XQT"] = pss.loc[outsybl, "XQT"]+exord["OUT_XQT"]
                pss.loc[outsybl, "QT"] = pss.loc[outsybl, "QT"] + exord["OUT_QT"]
            elif inpsybl != "XOR" and outsybl == "XOR":
                """NOT XOR"""
                pss.loc[inpsybl, "XQT"]=pss.loc[inpsybl, "XQT"]-exord["IN_XQT"]
                pss.loc[inpsybl, "QT"]=pss.loc[inpsybl, "QT"]-exord["IN_QT"]
                """IS XOR"""
                pss.loc["XOR","XQT"] = pss.loc["XOR", "XQT"]+exord["OUT_XQT"]
                pss.loc["XOR","QT"] = pss.loc["XOR", "XQT"]
            elif inpsybl != 'XOR' and outsybl != "XOR":
                """NOT XOR"""
                pss.loc[inpsybl, "XQT"]=pss.loc[inpsybl, "XQT"]-exord["IN_XQT"]
                pss.loc[inpsybl, "QT"]=pss.loc[inpsybl, "QT"]-exord["IN_QT"]
                """NOT XOR"""
                pss.loc[outsybl, "XQT"]=pss.loc[outsybl, "XQT"]+exord["OUT_XQT"]
                pss.loc[outsybl, "QT"]=pss.loc[outsybl, "QT"]+exord["OUT_QT"]
        Tesseract.portfolioss = pss.copy(deep=True)
        Tesseract.exorderss = pd.concat((Tesseract.exorderss,exord.to_frame().T),axis=0, ignore_index=True)
        return zigg.success_
    def balance(all=True,sybls:tuple=None):
        if all==True:
            balancess = dict()
            for sybl in AugChainZigg.symbolss:
                balancess[sybl] = zigg.Sora.assets_freebalance(account_id=AugChainZigg.account[1], asset_id=zigg.Symbols.idss[sybl])
                time.sleep(0.1)
            Tesseract.balancess = pd.DataFrame(data=balancess.values(), index=balancess.keys(), columns=["BALANCE"])
        if all!=True:
            assert sybls!=None
            for sbl in sybls:
                balance = zigg.Sora.assets_freebalance(account_id=AugChainZigg.account[1], asset_id=zigg.Symbols.idss[sbl])
                time.sleep(0.1)
                try: Tesseract.balancess.loc[sbl,"BALANCE"]=balance
                except AttributeError:
                    Tesseract.balancess = pd.DataFrame(index=AugChainZigg.symbolss,columns=["BALANCE"])
                    Tesseract.balancess.loc[sbl,"BALANCE"]=balance
        return
        
class AugChainZigg:
    def __setup__(account="acz2",
    symbolss=["XSTUSD","XOR","CERES","DEO","ETH","PSWAP","NOIR","VAL"],
    tasyblss = (("ETH/USD","BINANCE"),("XOR/WETH","UNISWAP"),("CRV/USD","BINANCE"),("WETH/XSTUSD","UNISWAP"),("DAI/USDT","FTX")),
    aczswpss = ("XSTUSD","XOR","CERES","DEO","ETH","PSWAP","NOIR","VAL"),#ENOUGH LIQUIDITY
    stopacz = None,
    slippage=1.01337,
    dpred = 0.00333,
    #-------------------
    lstm_data_load=42640,
    aczswxpq = 1.001337,#Quantity for AMM,
    ):
        """SETUP__INIT__(TESTING)"""
        AugChainZigg.account  = account
        AugChainZigg.symbolss = symbolss
        AugChainZigg.tasyblss = tasyblss
        AugChainZigg.slippage = slippage
        AugChainZigg.dpred = dpred
        AugChainZigg.symbolss.sort(reverse=True)
        AugChainZigg.aczswpss = aczswpss
        AugChainZigg.stopacz = stopacz
        AugChainZigg.aczswxpq = aczswxpq
        AugChainZigg.lstm_data_load = lstm_data_load
        assert AugChainZigg.slippage > 1.0
    def __init__(self, node="wss://sora.api.onfinality.io/public-ws",**kw):
        """THREADS"""
        AugChainZigg.__setup__()
        AugChainZigg.Zthread.pool = ThreadPoolExecutor(max_workers=16)
        print("load -> sora accounts")
        AugChainZigg.load_account(name=AugChainZigg.account)
        print("load -> data")
        AugChainZigg.infinite_load()
        print("connect -> sora blockchain")
        zigg.Sora.connsub(node="wss://sora.api.onfinality.io/public-ws")        
        print("request -> infinite data")
        #Tsora = AugChainZigg.Zthread.zsyncd(f=Tesseract.sora_watcher)
        print("auto -> trade strategies")
        #Tacz = AugChainZigg.Zthread.zsyncd(f=AugChainZigg.augchainzigg)
        AugChainZigg.augchainzigg()
        print("backup -> connections")
        #back=threading.Thread(target=AugChainZigg.backup_feeds,kwargs={"Tacz":Tacz})
        #back.start()
        #AugChainZigg.Zthread.zsyncd(f=AugChainZigg.backup_feeds, Tsora=Tsora, Tacz=Tacz, Tchain=Tchain)        
        #AugChainZigg.Zthread.zsyncd(AugChainZigg.backup_feeds,Tacz=Tacz)
        if zigg.testing==False: Menu()
        
    def augchainzigg():
        if Sts.ststate.get("dpred",None)==None: Sts.ststate["dpred"] = dict()
        if Sts.ststate.get("dprices",None)==None: Sts.ststate["dprices"] = dict()
        if Sts.ststate.get("acz",None)==None: Sts.ststate["acz"] = dict()
        if Sts.ststate.get("+cz",None)==None: Sts.ststate["+cz"] = dict()
        if Sts.ststate.get(Sts.LSTM,None)==None: Sts.ststate["LSTM"] = {}
        if Sts.ststate.get("xbalss",None)==None:
            Sts.ststate["xbalss"] = dict()
            for sybl in AugChainZigg.aczswpss:
                Sts.ststate["acz"][sybl] = 0
                Sts.ststate["dprices"][sybl] = {}
                Sts.ststate["dpred"][sybl]=0
                Sts.ststate["+cz"][sybl]=0
                Sts.ststate["xbalss"][sybl] = 0
            for sybl in AugChainZigg.aczswpss:
                Sts.ststate["dprices"][sybl]["inp_bprice"]=1
                Sts.ststate["dprices"][sybl]["inp_aprice"]=0                
            #AugChainZigg.xbal() DONT FORGET TO REACTIVATE!
        Sts.mult_lstm_pred()
        aczt,xbalt,lstmt,statet,xbalt,savet,raczt,rlstmt,chaint,backt,repred = timer(),timer(),timer(),timer(),timer(),timer(),timer(),timer(),timer(),timer(),0
        AugChainZigg.xor_prices(sybl="XSTUSD")
        #maxbal = AugChainZigg.maxbal()
        while True:
            for sybl in AugChainZigg.aczswpss:
                AugChainZigg.acz(sybl)
                rebalx,out_ssp,is_swap=None,None,None
                pred = Sts.ststate["acz"][sybl]
                #xstusd = round(Tesseract.tickss["XSTUSD"].iloc[-1]["XOR"]*Tesseract.tickss["XOR"].iloc[-1]["XOR"],18)
                #if xstusd > 0.991337 and sybl != "XSTUSD":
                    #if (pred < -0.001337 and pred > -0.1337):
                        #xqt,XXQT = AugChainZigg.xqt(sybl=sybl)
                        #if xqt > XXQT:
                            #rebalpss={}
                            #for sybl_, pred_ in Sts.ststate["acz"].items():
                                #if sybl != sybl_:
                                    #if (pred_ > 0.001337) and (pred_ < 0.1337): rebalpss[sybl_] = pred_
                            #try:
                                #sybl_ = min(rebalpss)
                                #rebalx = True
                            #except ValueError: rebalx = False
                            #if rebalx == True:
                                #try:#REBAL SELL
                                    #AugChainZigg.swap(inpsybl=sybl, outsybl=sybl_, desired_amount_out=AugChainZigg.aczswxpq, st=Sts.ACZ, test=None, menu=False)
                                    ##print(f"ACZ | {sybl} | {round(pred,4)} <-> {round(rebalpss[sybl_],4)} | {sybl_}")
                                    #print(f"ACZ | {sybl} -> {sybl_} | {round(pred,4)} | <-0.01")
                                #except : zigg.Tools.error(exc="? ACZ FAILED TO SWAP ?")
                                #Sts.ststate["xbalss"][sybl] -= AugChainZigg.aczswxpq
                                #Sts.ststate["xbalss"][sybl_] += AugChainZigg.aczswxpq
                                #Sts.ststate["dpred"][sybl] += abs(AugChainZigg.dpred)
                                #Sts.ststate["dpred"][sybl_] -= abs(AugChainZigg.dpred)                 
                                #is_swap=True
                                #out_ssp=sybl_
                                #repred +=1
                            #elif rebalx == False:
                                #try:#REBAL SELL
                                    #AugChainZigg.swap(inpsybl=sybl, outsybl="XSTUSD", desired_amount_out=AugChainZigg.aczswxpq, st=Sts.ACZ, test=None, menu=False)
                                    #print(f"ACZ | {sybl} -> XSTUSD | {round(pred,4)} | rebalx | <-0.01")
                                #except : zigg.Tools.error(exc="? ACZ FAILED TO SWAP ?")                                
                                #Sts.ststate["xbalss"][sybl] -= AugChainZigg.aczswxpq
                                #Sts.ststate["xbalss"]["XSTUSD"] += AugChainZigg.aczswxpq
                                #Sts.ststate["dpred"][sybl] += abs(AugChainZigg.dpred)
                                #Sts.ststate["dpred"]["XSTUSD"] -= abs(AugChainZigg.dpred)
                                #AugChainZigg.xor_prices(sybl="XSTUSD")                                 
                                #is_swap=True
                                #out_ssp="XSTUSD"
                                #repred +=1                     
                    #elif (pred > 0.001337 and pred < 0.1337):
                        #xqt,XXQT = AugChainZigg.xqt(sybl="XSTUSD")
                        #if xqt > XXQT:
                            #rebalpss={}
                            #for sybl_, pred_ in Sts.ststate["acz"].items():
                                #if sybl != sybl_ and sybl != "XSTUSD":
                                    #if (pred_ > 0.001337) and (pred_ < 0.1337): rebalpss[sybl_] = pred_
                            #try:
                                #sybl_ = min(rebalpss)
                                #rebalx = True
                            #except ValueError: rebalx = False
                            #if rebalx == True:
                                #try:#BUY
                                    #AugChainZigg.swap(inpsybl="XSTUSD", outsybl=sybl, desired_amount_out=AugChainZigg.aczswxpq, st=Sts.ACZ, test=None, menu=False)#is_swap=AugChainZigg.swap(inpsybl="XSTUSD", outsybl=sybl, desired_amount_out=1.01, st=Sts.ACZ, test=None, menu=False)   #AuggChainZigg.swap(inpsybl="XSTUSD", outsybl=sybl, desired_amount_out=1.01, st=Sts.ACZ, test=None, menu=False)
                                    #print(f"ACZ | XSTUSD -> {sybl} | {round(pred,4)} | > 0.01") 
                                #except : zigg.Tools.error(exc="? ACZ FAILED TO SWAP ?")                            
                                #Sts.ststate["xbalss"]["XSTUSD"] -= AugChainZigg.aczswxpq
                                #Sts.ststate["xbalss"][sybl] += AugChainZigg.aczswxpq
                                #Sts.ststate["dpred"]["XSTUSD"] -= abs(AugChainZigg.dpred)
                                #Sts.ststate["dpred"][sybl] -= abs(AugChainZigg.dpred)                           
                                #is_swap=True
                                #out_ssp=sybl
                                #repred +=1
                            #elif rebalx == False:
                                #rebalpss={}
                                #for sybl_, pred_ in Sts.ststate["acz"].items():
                                    #if sybl != "XSTUSD":
                                        #if (pred_ > 0.001337) and (pred_ < 0.1337): rebalpss[sybl_] = pred_
                                #try:
                                    #sybl_ = min(rebalpss)
                                    #AugChainZigg.swap(inpsybl="XSTUSD", outsybl=sybl_, desired_amount_out=AugChainZigg.aczswxpq, st=Sts.ACZ, test=None, menu=False)#is_swap=AugChainZigg.swap(inpsybl="XSTUSD", outsybl=sybl, desired_amount_out=1.01, st=Sts.ACZ, test=None, menu=False)   #AuggChainZigg.swap(inpsybl="XSTUSD", outsybl=sybl, desired_amount_out=1.01, st=Sts.ACZ, test=None, menu=False)
                                    #print(f"ACZ | XSTUSD -> {sybl_} | {round(pred,4)} | rebalx | >0.01") 
                                #except : zigg.Tools.error(exc="? ACZ FAILED TO SWAP ?")                            
                                #Sts.ststate["xbalss"]["XSTUSD"] -= AugChainZigg.aczswxpq
                                #Sts.ststate["xbalss"][sybl_] += AugChainZigg.aczswxpq
                                #Sts.ststate["dpred"]["XSTUSD"] -= abs(AugChainZigg.dpred)
                                #Sts.ststate["dpred"][sybl_] -= abs(AugChainZigg.dpred)                       
                                #is_swap=True
                                #out_ssp=sybl_
                                #repred +=1
                #elif sybl == "XSTUSD" and xstusd < 0.991337:
                    #rebalpss={}
                    #for sybl_, pred_ in Sts.ststate["acz"].items():
                        #if sybl_ != "XOR" and sybl_ != "XSTUSD":                              
                            #if (pred_ < -0.01) and (pred_ > -0.1337):
                                #xqt,XXQT = AugChainZigg.xqt(sybl=sybl_)
                                #if xqt > XXQT: rebalpss[sybl_] = pred_
                            #elif (pred_ > 0.01) and (pred_ < 0.1337):
                                #xqt,XXQT = AugChainZigg.xqt(sybl=sybl_)
                                #if xqt > XXQT: rebalpss[sybl_] = pred_
                    #try:
                        #sybl_ = max(rebalpss)
                        #rebalx = True
                    #except ValueError: rebalx = False
                    #if rebalx == True:
                        #try:#REBAL SELL
                            #AugChainZigg.swap(inpsybl=sybl_, outsybl="XSTUSD", desired_amount_out=AugChainZigg.aczswxpq, st=Sts.ACZ, test=None, menu=False)
                            #print(f"ACZ | {sybl_} -> XSTUSD | {round(pred,4)} | XSTUSD | <0.991337") 
                        #except : zigg.Tools.error(exc="? ACZ FAILED TO SWAP ?")
                        #Sts.ststate["xbalss"]["XSTUSD"] -= AugChainZigg.aczswxpq
                        #Sts.ststate["xbalss"][sybl_] += AugChainZigg.aczswxpq
                        #Sts.ststate["dpred"]["XSTUSD"] -= abs(AugChainZigg.dpred)
                        #Sts.ststate["dpred"][sybl_] += abs(AugChainZigg.dpred)              
                        #is_swap=True
                        #out_ssp="XSTUSD"
                        #repred +=1
                savet,aczt,lstmt,statet,chaint,backt=AugChainZigg.end_augchainzigg(sybl=sybl,lstmt=lstmt,statet=statet,savet=savet,aczt=aczt,rebalx=rebalx,chaint=chaint,backt=backt,out_ssp=out_ssp,is_swap=is_swap)
                    
    def end_augchainzigg(sybl=None,rebalx=None,out_ssp=None,is_swap=None,savet=None,aczt=None,lstmt=None,statet=None,chaint=None,backt=None):
        time.sleep(1)
        try:
            if Sts.ststate["dpred"][sybl] > 0.1337 or Sts.ststate["dpred"][sybl] <-0.1337: Sts.ststate["dpred"][sybl]=0
        except KeyError: Sts.ststate["dpred"][sybl] = 0
        if out_ssp == None: AugChainZigg.Zthread.zsyncd(f=AugChainZigg.xor_prices, sybl=sybl)
        else: AugChainZigg.Zthread.zsyncd(f=AugChainZigg.xor_prices, sybl=out_ssp)
        #if repred >= 30:
            #Sts.mult_lstm_pred()
            #repred = 0
        AugChainZigg.aczss(sybl=sybl)
        #-------------------
        if is_swap == None:
            if Sts.ststate["dpred"][sybl] > 0.33 or Sts.ststate["dpred"][sybl] <-0.33: Sts.ststate["dpred"][sybl]=0
            #DONT FORGET TO REACTIVATE! xbalt=zigg.Tools.elaps(f=AugChainZigg.xbal,timer_=xbalt,seconds=295)
            #130 seconds for lazy aggregation
            savet=zigg.Tools.elaps(e=AugChainZigg.Zthread.zsyncd,f=Tesseract.save_tickss,timer_=savet,seconds=130)
            aczt=zigg.Tools.elaps(e=AugChainZigg.Zthread.zsyncd,f=Tesseract.save_aczss,timer_=aczt,seconds=130)
            lstmt=zigg.Tools.elaps(e=AugChainZigg.Zthread.zsyncd,f=Sts.mult_lstm_pred,timer_=lstmt,seconds=600)
            statet=zigg.Tools.elaps(e=AugChainZigg.Zthread.zsyncd,f=Tesseract.save_state,timer_=statet,seconds=600)
            chaint=zigg.Tools.elaps(e=Menu.display_data,timer_=chaint,seconds=10)
            backt=zigg.Tools.elaps(e=AugChainZigg.backup_feeds,timer_=backt,seconds=35)
            for s in set(AugChainZigg.symbolss).difference(set(AugChainZigg.aczswpss)):
                AugChainZigg.xor_prices(sybl=s)                    
        return savet,aczt,lstmt,statet,chaint,backt        
        
    def aczss(sybl=None):
        try: _acz = Sts.ststate["acz"][sybl]
        except KeyError: 
            Sts.ststate["LSTM"][sybl] = {}
            Sts.ststate["dpred"][sybl] = 0
            return
        p = pd.DataFrame(columns=Tesseract.aczscols, data=[[zigg.Tools.dateformat(),_acz]])
        p["TIME"]=pd.to_datetime(p["TIME"])
        Tesseract.aczss[sybl]=pd.concat((Tesseract.aczss[sybl],p),axis=0,ignore_index=True)
    
    def xor_prices(sybl=None):
        id_ = zigg.Symbols.idss[sybl]
        if sybl=="XOR": outid=zigg.Symbols.idss["XSTUSD"]
        elif sybl!="XOR": outid=zigg.Symbols.idss["XOR"]
        price = zigg.Sora.liquidityProxy_quote(input_asset_id=id_, output_asset_id=outid, amount=10**18)
        #price = zigg.Sora.alternative_liquidityProxy_quote(sybl=sybl)
        tick = pd.DataFrame(columns=Tesseract.tickscols, data=[[zigg.Tools.dateformat(),price,0]])
        tick["TIME"]=pd.to_datetime(tick["TIME"])
        Tesseract.tickss[sybl]=pd.concat((Tesseract.tickss[sybl],tick),axis=0,ignore_index=True)    
    
    def xbal():             
        for sybl in AugChainZigg.aczswpss:
            Tesseract.balance(all=False,sybls=(sybl,))
            if sybl != "XOR":
                xbal = ((Tesseract.balancess.loc[sybl][0]*Tesseract.tickss[sybl].iloc[-1]["XOR"]))
            else: xbal=(Tesseract.balancess.loc[sybl][0]-1)
            Sts.ststate["xbalss"][sybl] = ((xbal-((xbal*AugChainZigg.slippage)-xbal))/2)
    
    def maxbal():
        balss = {}
        for sybl in AugChainZigg.aczswpss:
            balss[sybl] = Tesseract.portfolioss.loc[sybl,"XBAL"]
        maxbal = sum(balss.values()) / len(AugChainZigg.aczswpss)
        return maxbal
    
    def acz(sybl):
        try:
            pred = ((Sts.ststate["LSTM"][sybl]["XOR"]/Tesseract.tickss[sybl].iloc[-1]["XOR"]-1)*100)+Sts.ststate["dpred"][sybl]        
            if sybl != "XSTUSD" and sybl != "XOR": Sts.ststate["acz"][sybl] = round(pred,18) + (Sts.ststate["acz"]["XSTUSD"]*-0.66) + (Sts.ststate["acz"]["XOR"]*0.33)
            else: Sts.ststate["acz"][sybl] = round(pred,18)
            if Sts.ststate["acz"][sybl] > 1.337: Sts.ststate["acz"][sybl] = 1.337
            elif Sts.ststate["acz"][sybl] < -1.337: Sts.ststate["acz"][sybl] = -1.337            
            
            a24 = Tesseract.tickss[sybl]["XOR"].iloc[-1500:-60].mean()
            pred = ((Sts.ststate["LSTM"][sybl]["XOR"]/a24-1)*10)+Sts.ststate["dpred"][sybl]
            #if sybl != "XSTUSD" and sybl != "XOR": Sts.ststate["acz"]["a24"][sybl] = round(pred,18) + (Sts.ststate["acz"]["a24"]["XSTUSD"]*-1) + (Sts.ststate["acz"]["a24"]["XOR"]*-0.337)
            #else: Sts.ststate["acz"]["a24"][sybl] = round(pred,18)
            Sts.ststate["acz"]["a24"][sybl] = round(pred,18)
            if Sts.ststate["acz"]["a24"][sybl] > 1.337: Sts.ststate["acz"]["a24"][sybl] = 1.337
            elif Sts.ststate["acz"]["a24"][sybl] < -1.337: Sts.ststate["acz"]["a24"][sybl] = -1.337
        
            a7d = Tesseract.tickss[sybl]["XOR"].iloc[-10140:-60].mean()
            pred = ((Sts.ststate["LSTM"][sybl]["XOR"]/a7d-1)*1)+Sts.ststate["dpred"][sybl]
            #if sybl != "XSTUSD" and sybl != "XOR": Sts.ststate["acz"]["a7d"][sybl] = round(pred,18) + (Sts.ststate["acz"]["a7d"]["XSTUSD"]*-1) + (Sts.ststate["acz"]["a7d"]["XOR"]*-0.337)
            #else: Sts.ststate["acz"]["a7d"][sybl] = round(pred,18)
            Sts.ststate["acz"]["a7d"][sybl] = round(pred,18)
            if Sts.ststate["acz"]["a7d"][sybl] > 1.337: Sts.ststate["acz"]["a7d"][sybl] = 1.337
            elif Sts.ststate["acz"]["a7d"][sybl] < -1.337: Sts.ststate["acz"]["a7d"][sybl] = -1.337     
        
            a21d = Tesseract.tickss[sybl]["XOR"].iloc[-30300:-60].mean()
            pred = ((Sts.ststate["LSTM"][sybl]["XOR"]/a21d-1)*1)+Sts.ststate["dpred"][sybl]
            #if sybl != "XSTUSD" and sybl != "XOR": Sts.ststate["acz"]["a21d"][sybl] = round(pred,18) + (Sts.ststate["acz"]["a21d"]["XSTUSD"]*-1) + (Sts.ststate["acz"]["a21d"]["XOR"]*-0.337)
            #else: Sts.ststate["acz"]["a21d"][sybl] = round(pred,18)
            Sts.ststate["acz"]["a21d"][sybl] = round(pred,18)
            if Sts.ststate["acz"]["a21d"][sybl] > 1.337: Sts.ststate["acz"]["a21d"][sybl] = 1.337
            elif Sts.ststate["acz"]["a21d"][sybl] < -1.337: Sts.ststate["acz"]["a21d"][sybl] = -1.337                 
            
            #Sts.ststate["acz"]["aaz"] = Sts.ststate["acz"][sybl]
        except KeyError:
            Sts.ststate["acz"][sybl] = 0
            Sts.ststate["acz"]["a24"] = {}
            Sts.ststate["acz"]["a24"][sybl] = 0
            Sts.ststate["acz"]["a7d"] = {}
            Sts.ststate["acz"]["a7d"][sybl] = 0
            Sts.ststate["acz"]["a21d"] = {}
            Sts.ststate["acz"]["a21d"][sybl] = 0              
            #Sts.ststate["a7d"][sybl] = 0
    
    def xqt(sybl=None):
        xqt=Sts.ststate["xbalss"][sybl]
        if sybl == "XOR": XXQT = 2
        else : XXQT = AugChainZigg.aczswxpq
        return (xqt, XXQT)
    
    def terminate_thread(thread):
        """Terminates a python thread from another thread.
    
        :param thread: a threading.Thread instance
        """
        if not thread.is_alive():
            return
    
        exc = ctypes.py_object(SystemExit)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
            ctypes.c_long(thread.ident), exc)
        if res == 0:
            raise ValueError("nonexistent thread id")
        elif res > 1:
            # """if it returns a number greater than one, you're in trouble,
            # and you should call it again with exc=NULL to revert the effect"""
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread.ident, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")

        
    def backup_feeds(Tacz=None):
        def reconn():
            zigg.Sora.reconnsub()
            AugChainZigg.xor_prices(sybl="XOR")
        if datetime.datetime.now()-Tesseract.tickss["XOR"].iloc[-1]["TIME"] > datetime.timedelta(seconds=60):
            try:raise Exception()
            except: zigg.Tools.error(exc="!>!>  SORA CONNECTION FAIL  <!<!")
            AugChainZigg.Zthread.pool.shutdown(wait=False)
            for t in AugChainZigg.Zthread.pool._threads:
                AugChainZigg.terminate_thread(t)
            AugChainZigg.Zthread.pool = ThreadPoolExecutor(max_workers=16)
            AugChainZigg.Zthread.zsyncd(f=reconn)
            #zigg.Sora.substrate.close()
            #zigg.Sora.connsub(node="wss://sora.api.onfinality.io/public-ws")
            #AugChainZigg.Zthread.pool = ThreadPoolExecutor(max_workers=16)
            #AugChainZigg.xor_prices(sybl="XOR")
            #if (datetime.datetime.now()-Sts.tadfss["ETHUSD"].iloc[-1]["TIME"] > datetime.timedelta(seconds=60)) and tavieww != None:
                #try:raise Exception()
                #except:zigg.Tools.error(exc="TAVIEW FEED STOPPED DATA")
                #retry = 0
                #while True:
                    #if tavieww.cancel() != True and retry <= 10:
                        #try: raise Exception()
                        #except: zigg.Tools.error(exc="backup_feeds failed to cancel tavieww and restart, retrying...")
                        #time.sleep(1)
                        #continue
                #tavieww=AugChainZigg.Zthread.zsyncd(f=Sts.taview_watcher)
                        
    def infinite_load():
        Sts.load_strategies()
        #Sts.taview_load()
        Tesseract.load_aczdata()
        #Tesseract.load_historicalss()#Inactive for now
        Tesseract.load_tickss()
        Tesseract.load_aczss()
        Tesseract.load_portfolioss()
        Tesseract.load_exorderss()
                
    def save_account(name=None, public_address=None, encrypt=None, key="gyFUUFA@E5pF@7e8xbyPy^dEmo3DUgGG"):
        accounts = zigg.Tools.load_json(path=zigg.accounts)
        print("convert -> public address to ss58 adress")
        try: sora_address = zigg.Sora.substrate.ss58_encode(public_address)
        except ValueError: zigg.Tools.error(exc="not transformed to ss58 address")        
        accounts[name] = [sora_address, zigg.Tools.encrypt(encrypt=encrypt, key=key)]
        zigg.Tools.save_json(path=zigg.accounts, jss=accounts)
    
    def load_account(name=None, key=None):
        try:
            accounts = zigg.Tools.load_json(path=zigg.accounts)
            account = namedtuple(typename=name, field_names=["name","public_address", "secret"])
            AugChainZigg.account = account(
                name, 
                accounts[name][0], 
                zigg.Tools.decrypt(decrypt=accounts[name][1], key="gyFUUFA@E5pF@7e8xbyPy^dEmo3DUgGG"))
            print(f"selected account -> {name}")
        except KeyError:
            try: raise Exception()
            except: zigg.Tools.error(exc="account not selected")
        return AugChainZigg.account
    
    def swap(inpsybl=None,outsybl=None, desired_amount_out=None,st=None,test=None,menu=False):
        try:
            assert st != None
            exord = Tesseract.quantity(desired_amount_out=desired_amount_out, inpsybl=inpsybl, outsybl=outsybl,st=st,menu=menu)
            if isinstance(exord,pd.Series):
                if outsybl == "XOR":
                    max_amount_in = int(((exord["IN_BQT"])*(AugChainZigg.slippage))*10**18)
                    desired_amount_out = exord["OUT_BXQT"]*10**18
                elif inpsybl != "XOR" and outsybl != "XOR":
                    max_amount_in = int((exord["IN_BQT"]*AugChainZigg.slippage)*10**18)
                    desired_amount_out = int(exord["OUT_BQT"]*10**18)
                elif inpsybl == "XOR":
                    max_amount_in = int(((exord["IN_BXQT"])*(AugChainZigg.slippage))*10**18)
                    desired_amount_out = int(exord["OUT_BQT"]*10**18)
                if zigg.testing == False:
                    receipt = zigg.Sora.liquidityproxy_swap(input_asset_id=zigg.Symbols.idss[inpsybl], output_asset_id=zigg.Symbols.idss[outsybl], desired_amount_out=desired_amount_out, max_amount_in=max_amount_in, secret=AugChainZigg.account[2])
                    exord["EXT_HASH"] = receipt.extrinsic_hash
                is_swap=Tesseract.upt_portfolio(exord=exord, test=test)
                return is_swap
        except: return None
        return None
    class Zthread:
        def zsyncd(f = None, **kwargs):
            result = AugChainZigg.Zthread.pool.submit(f, **kwargs)
            return result
    
class Menu:
    def __init__(self):
        i = input("acz !>")
        if i[0:4]=="eval":Menu.eval(i=i)
        i = i.lower()
        if i=="save account": Menu.save_account()
        if i=="swap" or i == ".s": Menu.ttswap()
        if i=="ttswap": Menu.ttswap()
        if i=="exorders" or i == ".exo": Menu.display_exorderss()
        if i=="portfolio" or i == ".p": Menu.display_portfolioss()
        if i=="dbg": raise Exception("DEBUGGING")
        if i=="strategies" or i == ".sts":Menu.strategies()
        if i=="balance" or i==".b":Menu.display_balance()
        if i=="taview" or i==".tv": Menu.display_taview()
        if i=="correlation" or i==".corr":Tesseract.correlation()
        if i=="quit": Menu.quit()
        if i == "ticks" or i ==".t":
            try: print(Sts.ststate["dfshow"])
            except: pass        
        i = i.split(".")
        if i[0] != "":
            if i[0] == "sts": Menu.strategies(i=i)
            
        Menu()
        return
    def error(exc:str=None):
        zigg.Tools.error(exc=exc)
        Menu()
    def eval(i=None):
        w=i.split(" ")
        try: print(eval(w[1]))
        except Exception: pass
    def quit():
        print("<< saving >>")
        Tesseract.save_state()
        Tesseract.save_tickss()
        Tesseract.save_aczss()
        print("<< quit >>")
        try: raise Exception()
        except : sys.exit()
    #def strategies_delete(i=None):
        
    def display_taview():
        dss={}
        for sybl,tatks in Sts.tadfss.items():
            try:ss=tatks.iloc[-1].copy(deep=True)
            except IndexError:
                zigg.Tools.error(exc="taview not ready")
                return
            time=ss["TIME"]
            ss.drop("TIME", inplace=True)
            ss.replace(to_replace=-2, value="SS", inplace=True)
            ss.replace(to_replace=-1, value="S", inplace=True)
            ss.replace(to_replace=0, value="__", inplace=True)
            ss.replace(to_replace=1, value="B", inplace=True)
            ss.replace(to_replace=2, value="BB", inplace=True)
            dss[sybl]=ss
            tatks=Sts.taview_aggregation(tadf=tatks)
            hit=tatks.mean(numeric_only=True).sum()
            ss["TASUM"]=round(hit,2)
            ss["TIME"]=time
        tadf=pd.DataFrame.from_dict(dss).T
        print(tadf)
    def display_balance():
        Tesseract.balance(all=True)
        print(Tesseract.balancess.round(decimals=2))
    def display_portfolioss():
        try: pss=Tesseract.portfolioss.copy(deep=True)
        except AttributeError: 
            zigg.Tools.error(exc="portfolio not ready")
            return
        pss.rename(mapper={"XQT":"XBAL"},axis=1, inplace=True)
        for sybl in AugChainZigg.symbolss:
            try:
                if not pss.loc[sybl,"XOR"] == 0:
                    pss.loc[sybl,"CHG%"]=((Tesseract.tickss[sybl].iloc[-1]["XOR"]/pss.loc[sybl,"XOR"])-1)*1#Log1
                else: pss.loc[sybl,"CHG%"] = 0
            except IndexError: pss.loc[sybl,"CHG%"]=0.0
            except KeyError: pss.loc[sybl,"CHG%"]=0.0
            Tesseract.xbal(pss=pss,sybl=sybl)
            if sybl != "XOR":
                try: pss.loc[sybl,"XBAL"]=round( Tesseract.balancess.loc[sybl,"BALANCE"]*(Tesseract.tickss[sybl]["XOR"].iloc[-1]), 2)
                except AttributeError:pss.loc[sybl,"XBAL"]=0.0
            elif sybl == "XOR":
                try: pss.loc[sybl,"XBAL"]=Tesseract.balancess.loc["XOR","BALANCE"].round(decimals=2)
                except AttributeError:pss.loc[sybl,"XBAL"]=0.0
            pss.loc[sybl,"QT"]=pss.loc[sybl,"QT"]*0.01#Log0.1
            pss.loc[sybl,"XOR"]=pss.loc[sybl,"XOR"]*0.01#Log0.1
        pss=pss.round(decimals=2)
        pss=pss.astype(str)
        print(pss.to_string())
    def display_exorderss():
        #edf=Tesseract.exorderss[["IN","OUT","IN_QT","OUT_QT","IN_XOR","OUT_XOR","OUT_XQT","ST",zigg.dateixname_,"EXT_HASH"]]
        edf=Tesseract.exorderss[["IN","OUT","IN_XOR","OUT_XOR"]]
        print(edf.to_string())
    def inputparse(args:list=None, upper=False, rf=None):
        args_names, args_len = args, len(args)
        args = ((((str(args).replace("'", "")).replace("[","")).replace("]",""))).lower()
        args_inputs =  input(f"({args})-> ")
        args_inputs = args_inputs.split(",")
        if not len(args_names) == len(args_inputs):
            try: raise Exception('number of arguments')
            except: Menu.error(exc='number of arguments')
        if upper == False:
            argss = {args_names[i]: args_inputs[i] for i in range(len(args_names))}
        else:
            argss = {args_names[i]: args_inputs[i].upper() for i in range(len(args_names))}
        for k,v in argss.items():
            try: 
                if v[0] == " " : argss[k] = v[1:]
            except (IndexError, TypeError): argss[k] = None
        for k,v in argss.items():
            try:
                if v[-1] == " ": argss[k]=v[:-1]
            except (IndexError, TypeError): argss[k] = None
        for k,v in argss.items():
            if v == ".": argss[k] = None
            elif v == "": argss[k] = None
        return argss
    def display_data():
        show = dict()
        for sybl in AugChainZigg.symbolss:
            try: xor = round(Tesseract.tickss[sybl].iloc[-1]['XOR'],4)
            except:
                show[sybl] = pd.Series(data=(np.nan,)*len(Tesseract.tickscols), index=Tesseract.tickscols, dtype=str)
                continue
            if sybl != "XOR":
                try: usd = zigg.Tools.numberformat(round(xor*Tesseract.tickss["XOR"].iloc[-1]["XOR"],4))
                except IndexError:usd=np.nan
            elif sybl == "XOR":
                try: usd = zigg.Tools.numberformat(round(Tesseract.tickss[sybl].iloc[-1]['XOR'], 4))
                except IndexError:usd=np.nan
            time=Tesseract.tickss[sybl].iloc[-1][zigg.dateixname_]
            time=str(time)[11:]
            #try:
                #if not Tesseract.portfolioss.loc[sybl,"XOR"] == 0:
                    #chg = zigg.Tools.numberformat(round(((Tesseract.tickss[sybl].iloc[-1]["XOR"]/Tesseract.portfolioss.loc[sybl,"XOR"])-1),4))
                #else: chg = 0
            #except IndexError: chg = 0
            try: 
                acz = zigg.Tools.numberformat(round(Sts.ststate["acz"][sybl],4))
                a24 = zigg.Tools.numberformat(round(Sts.ststate["acz"]["a24"][sybl],4))
                a7d = zigg.Tools.numberformat(round(Sts.ststate["acz"]["a7d"][sybl],4))
                a21d = zigg.Tools.numberformat(round(Sts.ststate["acz"]["a21d"][sybl],4))
            except KeyError: acz,a24 = 0,0
            try:
                aczss = Tesseract.aczss[sybl]              
                _acz21d = aczss[-30300:-60]
                _acz21d = zigg.Tools.numberformat(round(_acz21d["+CZ"].sum(),4))
                _acz7d = aczss[-10140:-60]
                _acz7d = zigg.Tools.numberformat(round(_acz7d["+CZ"].sum(),4))                
            except: _acz7d,_acz21d = 0,0
            #try:_acz = zigg.Tools.numberformat(round(Sts.ststate["dpred"][sybl],4))
            #except:_acz=0
            #try:__acz = zigg.Tools.numberformat(round(Sts.ststate["+cz"][sybl],4))
            #except:__acz=0
            xor = zigg.Tools.numberformat(xor)
            show[sybl] = pd.Series(data=[acz,a24,a7d,a21d,_acz7d,_acz21d,xor,usd,time], index=["ACZ","A24","A7D","A21D","z7D","z21D","XOR","USD","TIME"], dtype=str)
            #zigg.Tools.save_json(path=Path(zigg.ticks,"XOR_PRICES.json"), jss=json.dumps({sybl:show[sybl].to_dict()}))
        dfshow = pd.DataFrame(data=show).T
        dfshow = dfshow.astype(str)
        dfshow = dfshow.replace(to_replace="0.0", value="0", inplace=False)
        dfshow=dfshow.applymap(lambda x:x.replace("(","").replace(")","").replace(", ","|"))
        Sts.ststate["dfshow"] = dfshow
        print(dfshow.to_string())
        return
    def save_account():
        argss = Menu.inputparse(args=["name", "public_address" ,"secret"])
        AugChainZigg.save_account(name=argss["name"], public_address=argss["public_address"], encrypt=argss["secret"])
        AugChainZigg.load_account(name=argss["name"])
        print(f"({argss['name']}) account saved and selected")
        return
    def strategies(i=None):
        if i == None:
            argss=Menu.inputparse(args=["ST","IN","OUT","XQT","XOR","TP","SL","EXPIRE"],upper=True)
            if argss["ST"]==Sts.BUY_LOW or argss["ST"] == Sts.BUY_LOW.replace("_"," "):
                Sts.orders_strategie(st=Sts.BUY_LOW,inp=argss["IN"],out=argss["OUT"],xqt=float(argss["XQT"]),xor=argss["XOR"],tp=argss["TP"],sl=argss["SL"],expire=argss["EXPIRE"])
            elif argss["ST"]==Sts.SELL_HIGH or argss["ST"] == Sts.SELL_HIGH.replace("_"," "):
                Sts.orders_strategie(st=Sts.SELL_HIGH,inp=argss["IN"],out=argss["OUT"],xqt=float(argss["XQT"]),xor=argss["XOR"],tp=argss["TP"],sl=argss["SL"],expire=argss["EXPIRE"])
            print(Sts.stss)
            zigg.Tools.pickle(df=Sts.stss,path=zigg.database,name=zigg.strategies_,save=True)
        if i != None:
            if i[1] == "del":
                if i[2] == "all":
                    Sts.stss = pd.DataFrame(columns=Sts.stcols)
                    zigg.Tools.pickle(df=Sts.stss,path=zigg.database,name=zigg.strategies_,save=True)
                print(Sts.stss)
            if i[1] == "lstm":
                if i[2] == "all": Sts.mult_lstm_pred()
                if i[2] == "remodel":
                    try:os.remove(zigg.lstm)
                    except FileNotFoundError: pass
                    zigg.Tools.exists_path(zigg.lstm)
                    for sybl in AugChainZigg.aczswpss:
                        Sts.Lstm.augchainzigg(sybl=sybl, col="XOR")
                    Sts.mult_lstm_pred()
                #if i[2] == "remodel":
                    #for sybl in AugChainZigg.aczswpss:
                        #Sts.Lstm.augchainzigg(sybl=sybl, col="XOR", path=zigg.remodel)
        
    def ttswap(test=None, argss=None):
        print("\n")
        if zigg.testing == False:
            if argss == None:
                argss = Menu.inputparse(args=["input","output","quantity_out"],upper=True)
        inpsybl = argss["input"]
        outsybl = argss["output"]
        try:
            assert inpsybl == zigg.Symbols.__dict__[inpsybl][0]
            assert outsybl == zigg.Symbols.__dict__[outsybl][0]
        except KeyError:
            try:raise Exception()
            except: Menu.error(exc=f"symbols {inpsybl},{outsybl} not found")
        exorder=Tesseract.quantity(desired_amount_out=argss["quantity_out"], inpsybl=inpsybl, outsybl=outsybl, menu=True)
        if zigg.testing == False:
            confirm = Menu.inputparse(args=["Swap /Y /N ?"])
        elif zigg.testing == True: confirm = {"Swap /Y /N ?":"Y"}
        if confirm["Swap /Y /N ?"].upper() == "Y":
            inp_aprice=0
            if zigg.testing==False:
                TQT = float(argss["quantity_out"])
                SQT = 0                
                while (SQT+0.1) < TQT:
                    #inp_bprice=Tesseract.tickss[inpsybl].iloc[-1]['XOR']
                    #if inp_bprice != inp_aprice:
                    AugChainZigg.swap( inpsybl=inpsybl, outsybl=outsybl,desired_amount_out=AugChainZigg.aczswxpq, test=test, st=Sts.MANUAL, menu=True)
                    inp_aprice = Tesseract.tickss[inpsybl].iloc[-1]['XOR']
                    SQT += AugChainZigg.aczswxpq
                Menu()
        elif confirm["Swap /Y /N ?"] == None: Menu.ttswap(argss=argss)
        elif confirm["Swap /Y /N ?"].upper() == "N": Menu()
        return
        
if __name__ ==  "__main__" :
    AugChainZigg()