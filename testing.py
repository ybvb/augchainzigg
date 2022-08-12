import pandas as pd
from pathlib import Path
import os, inspect
import ziggurat as zigg
import numpy as np
import datetime
from collections import namedtuple
import random
import numpy as np
import time
from timeit import default_timer as timer
import json
import requests
import augchainzigg as acz
import functools
import matplotlib as mp
import pickle
from matplotlib import pyplot as plt

class Testing:
    def fk_sora_tick(sybl:str=None, xor:float=None):
        tick = pd.DataFrame(columns=acz.Tesseract.tickscols, data=[[zigg.Tools.dateformat(), xor]])
        acz.Tesseract.tickss[sybl] = pd.concat((acz.Tesseract.tickss[sybl],tick),axis=0,ignore_index=True)
    def fk_balance(balancess:dict=None):
        acz.Tesseract.balancess=pd.DataFrame(data=balancess.values(),index=balancess.keys(), columns=["BALANCE"])
        
class _Menu:
    def aczss_sum():# Menu sora_tick_display
        print("stop")

class _Sts:
    def lstm_strategie():
        acz.AugChainZigg.__setup__()
        acz.AugChainZigg.infinite_load()
        rng=np.random.default_rng()
        days = pd.date_range(
            start = (datetime.datetime.now()-datetime.timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S'),
            end = datetime.datetime.now(),freq="1min")
        
        xor = rng.uniform(low=-1.0,high=1.0,size=len(days))
        vol = rng.uniform(low=-1.0,high=1.0,size=len(days))
        liq = rng.uniform(low=-1.0,high=1.0,size=len(days))
        acz.Tesseract.tickss["XOR"] = pd.DataFrame.from_dict(data={"TIME":days,"XOR":xor, "VOL":vol, "LIQ":liq}).round(decimals=2)
        
        acz.Sts.Lstm.augchainzigg(sybl="XOR")
        print("stop")
        
        #acz.Sts.Lstm.augchainzigg(sybl=sybl)
        
        
    def taview_strategie():
        try:os.remove(Path(zigg.database, f"{zigg.exorders_}.pkl"))
        except FileNotFoundError: pass
        try:os.remove(Path(zigg.database, f"{zigg.portfolio_}.pkl"))
        except FileNotFoundError: pass
        acz.AugChainZigg.__setup__()
        acz.AugChainZigg.infinite_load()
        rng=np.random.default_rng()
        days = pd.date_range(
            start = (datetime.datetime.now()-datetime.timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S'),
            end = datetime.datetime.now(),freq="1min")
        tadss = {}
        slpss={"1M":None,"5M":None,"15M":None,"30M":None,"1H":None,"1D":None}
        balancess = {}
        for couple in acz.AugChainZigg.tasyblss:
            sybl = couple[0].split("/")[0]
            balancess[sybl] = 99999
            slp=rng.uniform(low=0.0,high=100.0,size=len(days))
            acz.Tesseract.tickss["XSTUSD"] = pd.DataFrame.from_dict(data={"TIME":days,"XOR":slp}).round(decimals=2)            
            if sybl in acz.AugChainZigg.aczswpss:
                slp=rng.uniform(low=0.0,high=100.0,size=len(days))
                acz.Tesseract.tickss[sybl] = pd.DataFrame.from_dict(data={"TIME":days,"XOR":slp}).round(decimals=2)                
                tadss[couple[0]]=pd.DataFrame(columns=["TIME","1M","5M","15M","30M","1H","1D"])
                slpss["1M"]=rng.integers(low=-2,high=3,size=len(days))
                slpss["5M"]=rng.integers(low=-2,high=3,size=len(days))
                slpss["15M"]=rng.integers(low=-2,high=3,size=len(days))
                slpss["30M"]=rng.integers(low=-2,high=3,size=len(days))
                slpss["1H"]=rng.integers(low=-2,high=3,size=len(days))
                slpss["1D"]=rng.integers(low=-2,high=3,size=len(days))
                
                tatick=pd.DataFrame.from_dict(data={"TIME":days,"1M":slpss["1M"],"5M":slpss["5M"],"15M":slpss["15M"],"30M":slpss["30M"],"1H":slpss["1H"],"1D":slpss["1D"]})
                tadss[couple[0]]=pd.concat((tadss[couple[0]],tatick),axis=0)
                acz.Sts.tadfss[couple[0]] = pd.DataFrame.from_dict(tadss[couple[0]])
        balancess["XSTUSD"]=99999
        Testing.fk_balance(balancess=balancess)
        """TRUE LOGIC"""
        """After 1800 seconds..."""
        acz.Sts.taview_strategie()
        print(acz.Tesseract.exorderss)
        print(acz.Tesseract.portfolioss)
    def simple_strategies():
        t=time.time()
        inp,out,d="XOR","PSWAP",1
        rng=np.random.default_rng(seed=70)
        try:os.remove(Path(zigg.database, f"{zigg.exorders_}.pkl"))
        except FileNotFoundError: pass
        try:os.remove(Path(zigg.database, f"{zigg.portfolio_}.pkl"))
        except FileNotFoundError: pass        
        acz.AugChainZigg.infinite_load()
        Testing.fk_balance(balancess={inp:99999,out:99999})
        days = pd.date_range(
            start = (datetime.datetime.now()-datetime.timedelta(days=d)).strftime('%Y-%m-%d %H:%M:%S'),
            end = datetime.datetime.now(),freq="5min")
        
        xorslp=rng.uniform(low=0.0,high=100.0,size=len(days))
        acz.Tesseract.tickss["XOR"] = pd.DataFrame.from_dict(data={"TIME":days,"XOR":xorslp}).round(decimals=2)
        
        pswapslp=rng.uniform(low=0.0,high=100.0,size=len(days))
        acz.Tesseract.tickss["PSWAP"] = pd.DataFrame.from_dict(data={"TIME":days,"XOR":pswapslp}).round(decimals=6)
        xor,tp,sl="0.1%","0.1%","0.2%"
        
        acz.Sts.buy_low(inp="XOR",out="PSWAP",xor=xor,xqt="1",tp=tp,sl=sl)
        p = acz.Tesseract.tickss[out].iloc[-1]["XOR"]
        
        assert acz.Sts.stss["XOR"].iloc[-1]==p-(p*float(xor[0:-1]))
        assert acz.Sts.stss["TP"].iloc[-1]==p+(p*float(tp[0:-1]))
        assert acz.Sts.stss["SL"].iloc[-1]==p-(p*float(sl[0:-1]))
        
        acz.Sts.sell_high(inp="XOR",out="PSWAP",xor=xor,xqt="1",tp=tp,sl=sl)
        p = acz.Tesseract.tickss[inp].iloc[-1]["XOR"]
        
        assert acz.Sts.stss["XOR"].iloc[-1]==p+(p*float(xor[0:-1]))
        assert acz.Sts.stss["TP"].iloc[-1]==p-(p*float(tp[0:-1]))
        assert acz.Sts.stss["SL"].iloc[-1]==p+(p*float(sl[0:-1]))
        
        print("Strategies")
        print(acz.Sts.stss)
        
        for xor,pswap in zip(tuple(acz.Tesseract.tickss["XOR"]["XOR"]),tuple(acz.Tesseract.tickss["PSWAP"]["XOR"])):
            acz.Tesseract.tickss["XOR"]["XOR"].iat[-1]=xor
            acz.Sts.strategies_target(sybl="XOR",hit=xor)            
            acz.Tesseract.tickss["PSWAP"]["XOR"].iat[-1]=pswap
            acz.Sts.strategies_target(sybl="PSWAP",hit=pswap)
            
        """TEST STOP LOGIC"""
            
        print("Exorders")
        acz.Menu.display_exorderss()
        print("Portfolio")
        print(acz.Tesseract.portfolioss)
        print("Strategies")
        print(acz.Sts.stss)
        print("Count")
        print(acz.Tesseract.tickss["PSWAP"].count())
        print(f"TIME : {time.time()-t}")
        print("stop")
    
    def reset_lstm():
        sybl = "CERES"
        try: os.remove(Path(zigg.lstm,f"[{sybl}]XOR.pkl"))
        except FileNotFoundError: pass
        acz.Sts.Lstm.augchainzigg(sybl=sybl,col="XOR",path=zigg.lstm)
            
        
class _Tesseract:
    LOL="NONE"
    def correlation():
        acz.AugChainZigg.infinite_load()
        acz.Tesseract.correlation()
    def save_ticks():
        d=600
        days = pd.date_range(
            start = (datetime.datetime.now()-datetime.timedelta(days=d)),
            end = datetime.datetime.now(),freq="1min")
        rng = np.random.default_rng(seed=d)
        xorslp=rng.uniform(low=0.0,high=100.0,size=len(days))
        volslp=rng.uniform(low=0.0,high=100.0,size=len(days))
        df = pd.DataFrame.from_dict(data={zigg.dateixname_:days,"XOR":xorslp,"VOL":volslp,"LOL":volslp}).round(decimals=2)
        
        df.to_pickle(Path(zigg.database,'TEST.pkl'))
        t= time.time()
        
        dfp=pd.read_pickle(Path(zigg.database,'TEST.pkl'))
        
        df.groupby(by=pd.Grouper(key='TIME', axis=0, freq='1min')).mean()
        print(len(dfp))
        print(time.time()-t)
        print("stop")
    def test_pickle():
        days = pd.date_range(start = (datetime.datetime.now()-datetime.timedelta(days=5)),end = datetime.datetime.now(),freq="1min")
        df = pd.DataFrame.from_dict(data={zigg.dateixname_:days})
        zigg.Tools.pickle(df=df, path=zigg.database, name="TEST", save=True)
        df = zigg.Tools.pickle(df=df, path=zigg.database, name="TEST", load=True)
        print(df)        
    
class _Ziggurat:
    pass

class _AugChainZigg:
    def testnetconn(node="wss://ws.framenode-6.s3.stg1.sora2.soramitsu.co.jp", account="tacz1",fake=False):#TESTNET
        #if fake == False:not working because no **kw
            #acz.AugChainZigg(
        #account="tacz1", 
        #node="wss://ws.framenode-6.s3.stg1.sora2.soramitsu.co.jp")
        if fake == True: acz.AugChainZigg.__setup__()
    def account():# AugChainZigg save_account / load_account
        name = "tacz1"
        public_address = "Ckadiajsdiashd"
        encrypt = "NEVER TYPE YOUR KEY HERE, COPY FROM MAIN INSTEAD"
        acz.AugChainZigg.save_account(
            name=name,
            public_address=public_address,
            encrypt=encrypt)
        acz.AugChainZigg.load_account(name=name)
        acc = acz.AugChainZigg.account
        assert acc == (name, public_address, encrypt)
    def test_feeds():
        acz.AugChainZigg.infinite_load()
        acz.AugChainZigg.test_feeds()
        
    def menu_swap_order_portfolio():
        def setup(test=None):
            Testing.fk_balance(balancess={test["input"]:99999,test["output"]:99999})
            Testing.fk_sora_tick(sybl=zigg.Symbols.XOR[0], xor=100)
            if test["output"] == "XOR":
                Testing.fk_sora_tick(sybl=test["input"], xor=test["before_inp_xor"])
                Testing.fk_sora_tick(sybl=test["input"], xor=test["before_out_xor"])
            elif test["input"] !="XOR" and test["output"]!="XOR":
                Testing.fk_sora_tick(sybl=test["input"], xor=test["before_inp_xor"])
                Testing.fk_sora_tick(sybl=test["output"], xor=test["before_out_xor"])
            elif test["output"] != "XOR":
                Testing.fk_sora_tick(sybl=test["output"], xor=test["before_inp_xor"])
                Testing.fk_sora_tick(sybl=test["output"], xor=test["before_out_xor"])
        try:os.remove(Path(zigg.database, f"{zigg.exorders_}.pkl"))
        except FileNotFoundError: pass
        try:os.remove(Path(zigg.database, f"{zigg.portfolio_}.pkl"))
        except FileNotFoundError: pass        
        acz.AugChainZigg.infinite_load()
        test={"input":"VAL", #QUANTITY 0
              "output":"XOR",
              "quantity_out" :"1.33",
              "before_inp_xor":0.0031,
              "after_inp_xor"  :0.0030,
              "before_out_xor":0.0031,
              "after_out_xor"  :0.0030}
        setup(test=test)
        acz.Menu.ttswap(argss=test,test=test)
        print(acz.Tesseract.portfolioss)
        exord = acz.Tesseract.exorderss.iloc[-1]
        assert exord["IN"]  == test["input"]
        assert exord["OUT"] == test["output"]
        desired_amount_out = float(test["quantity_out"])
        in_bqt=(desired_amount_out/test["before_inp_xor"])
        out_bqt = desired_amount_out/exord["OUT_BXOR"]
        assert exord["IN_BXQT"]==(in_bqt)*(test["before_inp_xor"])
        assert exord["IN_AQT"]==((in_bqt*test["before_inp_xor"])/(exord["IN_BQT"]*test["before_inp_xor"]))*in_bqt
        assert exord["OUT_AQT"]==((out_bqt*exord["OUT_BXOR"])/(out_bqt*exord["OUT_AXOR"]))*out_bqt
        test={"input":"XOR",#VENDENDO PREJUIZO!
              "output":"VAL",
              "quantity_out"  :"0.5",
              "before_inp_xor": 0.0029,
              "after_inp_xor" : 0.0027,
              "before_out_xor": 0.0029,
              "after_out_xor" : 0.0027}
        bpss = acz.Tesseract.portfolioss
        before_xor = bpss.loc[test["input"],"XOR"]
        setup(test=test)
        Testing.fk_sora_tick(sybl=zigg.Symbols.XOR[0], xor=200)
        acz.Menu.ttswap(argss=test,test=test)
        print(acz.Tesseract.portfolioss)
        exord = acz.Tesseract.exorderss.iloc[-1]
        profit = ((((((exord["IN_XOR"]-before_xor)/before_xor))*abs(exord["IN_XQT"]))+bpss.loc[test["input"], "XPRF"])-exord["TX_COST"])
        if acz.Tesseract.portfolioss.loc[test["input"], "XPRF"] !=0 and test["input"]!="XOR":
            assert profit == acz.Tesseract.portfolioss.loc[test["input"], "XPRF"]
        assert acz.Tesseract.balancess.loc[test["input"],"BALANCE"]==acz.Tesseract.balancess.loc[test["input"],"BALANCE"]-exord["IN_QT"]+exord["OUT_QT"]
        assert acz.Tesseract.balancess.loc[test["output"],"BALANCE"]==acz.Tesseract.balancess.loc[test["output"],"BALANCE"]+exord["OUT_QT"]-exord["IN_QT"]
        test={"input":"VAL",
              "output":"XOR",
              "quantity_out"  :"1",
              "before_inp_xor": 0.0023,
              "after_inp_xor" : 0.0023,
              "before_out_xor": 0.0024,
              "after_out_xor" : 0.0024}
        bpss = acz.Tesseract.portfolioss
        setup(test=test)
        Testing.fk_sora_tick(sybl=zigg.Symbols.XOR[0], xor=50)
        acz.Menu.ttswap(argss=test,test=test)
        print(acz.Tesseract.portfolioss)
        exord = acz.Tesseract.exorderss.iloc[-1]
        avgxor = ((abs(bpss.loc[test["output"],"QT"])*bpss.loc[test["output"],"XOR"])+(exord["OUT_QT"]*exord["OUT_XOR"]))/(abs(bpss.loc[test["output"],"QT"])+exord["OUT_QT"])
        if bpss.loc[test["input"],"XQT"]!=0 and test["output"]!="XOR":
            assert avgxor == acz.Tesseract.portfolioss.loc[test["output"],"XOR"]
        test={"input":"VAL",
              "output":"XOR",
              "quantity_out"  :"1.9",
              "before_inp_xor": 0.0031,
              "after_inp_xor" : 0.0032,
              "before_out_xor": 0.0031,
              "after_out_xor" : 0.0032}
        bavgxor = avgxor
        setup(test=test)
        Testing.fk_sora_tick(sybl=zigg.Symbols.XOR[0], xor=50)
        acz.Menu.ttswap(argss=test,test=test)
        print(acz.Tesseract.portfolioss)
        test={"input":"XOR",
              "output":"VAL",
              "quantity_out"  :"0.1",
              "before_inp_xor": 0.0018,
              "after_inp_xor" : 0.0019,
              "before_out_xor": 0.0018,
              "after_out_xor" : 0.0019}
        setup(test=test)
        acz.Menu.ttswap(argss=test,test=test)
        print(acz.Tesseract.portfolioss)
        test={"input":"VAL",
              "output":"XOR",
              "quantity_out"  :"1",
              "before_inp_xor": 0.0034,
              "after_inp_xor" : 0.0035,
              "before_out_xor": 0.0034,
              "after_out_xor" : 0.0035}
        setup(test=test)
        acz.Menu.ttswap(argss=test,test=test)
        print(acz.Tesseract.portfolioss)
        print("stop")
        
class _Sora:
    def subscan():
        zigg.Sora.subscan()
    def assets_totalSupply(id_=None):
        quote=Sora.substrate.rpc_request("assets_totalSupply",[id_])
        print("stop")
        
    
class _All():
    def __init__(self):
        _AugChainZigg.account()
        sora_tick_display()
        _Ziggurat.hdfdb()
        _AugChainZigg.menu_swap_order_portfolio()
        
def picke():
    with open( Path(zigg.lstm,"ETH"),'wb') as m:
        pickle.dump(_Tesseract, m)
    
    with open( Path(zigg.lstm,"ETH"),'r') as l:
        lol = pickle.load(l)
    print("stop")
        
        
if __name__ ==  "__main__" :
    zigg.road_to_ziggurat(testing=True)
    """--------------------------"""
    _AugChainZigg.testnetconn(fake=True)
    """--------------------------"""
    acz.AugChainZigg.__setup__()
    acz.AugChainZigg.infinite_load()
    _Sts.reset_lstm()
    #acz.Tesseract.correlation()
    print("stop")
    #picke()