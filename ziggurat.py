from collections import namedtuple
from substrateinterface import Keypair #sudo apt install python3.X-dev
from Crypto.Cipher import AES
from base64 import b64encode, b64decode
import os, inspect
from pathlib import Path
import pandas as pd
import datetime
import json
import regex as re
from substrateinterface import SubstrateInterface
from scalecodec.type_registry import load_type_registry_file
import tables
import time
import traceback
import numpy as np
import requests
import pickle
from timeit import default_timer as timer

def road_to_ziggurat(testing=True):
    testing = testing
    filename = inspect.getframeinfo(inspect.currentframe()).filename
    
    if testing == False:
        acz   = os.path.dirname(os.path.abspath(filename))
        aczv = Path(os.path.dirname(acz),"augchainzigg")
    elif testing == True:
        acz   = os.path.dirname(os.path.abspath(filename))
        aczv = Path(os.path.dirname(os.path.dirname(acz)),"augchainzigg","testing")
        acz = Path(aczv, "testing")
        aczv = Path(aczv,"testing")
        
    pd.set_option('display.float_format','{:.6f}'.format)
    pd.set_option('display.colheader_justify',"left")
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)    
    
    accounts = Path(aczv, "accounts.json")
    database = Path(aczv)
    ticks = Path(database, "ticks")
    aczs = Path(database, "aczs")
    taview = Path(database, "taview")
    historical = Path(database, "historical")
    lstm = Path(database, "lstm")
    remodel = Path(lstm, "remodel")
    substrate_types = Path(acz, "substrate_types.json")
    ststate = Path(database, "ststate")
    #if testing==True:
        #substrate_types = Path(aczv,"substrate_types_v0.json")
    
    hdfgroup_ = "ACZ"
    dateixname_ = "TIME"
    exorders_ = "EXORDERS"
    ticks_ = "TICKS"
    portfolio_ = "PORTFOLIO"
    success_ = "SUCCESS"
    strategies_ = "STRATEGIES"
    
    Tools.exists_path(database)
    Tools.exists_path(ticks)
    Tools.exists_path(taview)
    Tools.exists_path(historical)
    Tools.exists_path(lstm)
    Tools.exists_path(aczs)
    Tools.exists_path(remodel)
    
    globals().update(locals())

class Sora():
    subnodes = ["wss://sora.api.onfinality.io/public-ws","wss://mof.sora.org", "wss://mof2.sora.org", "wss://mof3.sora.org", "wss://ws.alb.sora.org", "wss://sora.lux8.net"]
    def subscan():
        headers = {'content-type':'application/json' , 'x-api-Key':"1fb0094284da4d7907290e669c782b51"}
        payload = {'hash': '0x642e2e614dd29e55bdb658f6f1e759f5ac05861855b4020f1d9a4672db3de974'}
        
        data=requests.post('https://polkadot.api.subscan.io/api/scan/extrinsic',payload=payload,headers=headers)
        print("stop")
    def reconnsub():
        try:Sora.substrate.close()
        except AttributeError: pass
        try: newnode = Sora.subnodes[Sora.subnodes.index(Sora.node)+1]
        except IndexError: newnode = Sora.subnodes[0]
        Sora.connsub(node=newnode)
        return
    def connsub(node=None):
        Sora.node=node
        try:
            substrate = SubstrateInterface(url=node, websocket=None, ss58_format=69, type_registry=load_type_registry_file(substrate_types), type_registry_preset="default", cache_region=None, runtime_config=None, use_remote_preset=False)
            Sora.substrate = substrate
        except Exception as e: Tools.error(exc="!>!>  SORA CONNECTION FAIL  <!<!")
        return
    is_substrate_quote_on=0
    def liquidityProxy_quote(dexid=0, liquidity_source_type="XYKPool", input_asset_id=None, output_asset_id=None, amount=None, swap_variant="WithDesiredInput"):
        quote=Sora.substrate.rpc_request("liquidityProxy_quote",[0, input_asset_id,output_asset_id, str(amount), "WithDesiredInput",["XYKPool"], "Disabled"])
        price = (int(quote["result"]["amount_without_impact"]))/10**18
        return price
    
    def alternative_liquidityProxy_quote(sybl=None):
        if sybl=="XOR": out_sybl = "XSTUSD"
        elif sybl!="XOR": out_sybl="XOR"
        price = requests.get(f"https://stats.sora.org/pairs/{sybl}-{out_sybl}/")
        price = price.json()["last_price"]
        return price
        
    
    def liquidityproxy_swap(input_asset_id=None, output_asset_id=None, desired_amount_out=None, max_amount_in=None, secret=None,):
        try:
            keypair = Keypair.create_from_mnemonic(secret)
            call = Sora.substrate.compose_call(
                call_module='LiquidityProxy',
                call_function='swap',
                call_params={
                    'dex_id': '0',
                    'input_asset_id': input_asset_id,
                    'output_asset_id': output_asset_id,
                    'swap_amount': {'WithDesiredOutput': {'desired_amount_out': desired_amount_out, 'max_amount_in': max_amount_in}},
                    'selected_source_types': ["XYKPool"],
                    'filter_mode': 'Disabled'
                }
            )
            extrinsic = Sora.substrate.create_signed_extrinsic(call=call, keypair=keypair)
            try:
                receipt = Sora.substrate.submit_extrinsic(extrinsic, wait_for_inclusion=False)
            except BrokenPipeError:
                try: raise Exception()
                except: Tools.error(exc="broken pipe, reconnecting...")
                #Sora.reconnsub()
                #receipt = Sora.substrate.submit_extrinsic(extrinsic, wait_for_inclusion=False)
        except:
            Tools.error(exc="? ACZ FAILED TO SWAP ?")
            return None
        return receipt
    
    def assets_totalSupply(id_=None):
        return Sora.substrate.rpc_request("assets_totalSupply",[id_])  
    
    def assets_freebalance(account_id=None, asset_id=None):
        try:
            balance = Sora.substrate.rpc_request(method="assets_freeBalance", params=[account_id, asset_id])
        except Exception as e: 
            try: raise Exception()
            except: Tools.error(exc="broken pipe, reconnecting...")
            #Sora.reconnsub()
            #balance=Sora.substrate.rpc_request("assets_freeBalance", [account_id, asset_id])
        return int(balance["result"]["balance"])/10**18
    
class Symbols:
    idss = {}   
    symbol_fields = ["symbol", "id"]
    
    XOR = namedtuple("XOR", symbol_fields)
    XOR = XOR("XOR", "0x0200000000000000000000000000000000000000000000000000000000000000")
    idss[XOR[0]] = XOR[1]
    
    XSTUSD = namedtuple("XSTUSD", symbol_fields)
    XSTUSD = XSTUSD("XSTUSD", "0x0200080000000000000000000000000000000000000000000000000000000000")
    idss[XSTUSD[0]] = XSTUSD[1]
    
    VAL = namedtuple("VAL", symbol_fields)
    VAL = VAL("VAL", "0x0200040000000000000000000000000000000000000000000000000000000000")
    idss[VAL[0]] = VAL[1]
    
    PSWAP = namedtuple("PSWAP", symbol_fields)
    PSWAP = PSWAP("PSWAP", "0x0200050000000000000000000000000000000000000000000000000000000000")
    idss[PSWAP[0]] = PSWAP[1]
    
    DAI = namedtuple("DAI", symbol_fields)
    DAI = DAI("DAI", "0x0200060000000000000000000000000000000000000000000000000000000000")
    idss[DAI[0]] = DAI[1]
    
    CERES = namedtuple("CERES", symbol_fields)
    CERES = CERES("CERES", "0x008bcfd2387d3fc453333557eecb0efe59fcba128769b2feefdd306e98e66440")
    idss[CERES[0]] = CERES[1]
    
    DEO = namedtuple("DEO", symbol_fields)
    DEO = DEO("DEO", "0x00f2f4fda40a4bf1fc3769d156fa695532eec31e265d75068524462c0b80f674")
    idss[DEO[0]] = DEO[1]
    
    NOIR = namedtuple("NOIR", symbol_fields)
    NOIR = NOIR("NOIR", "0x0044aee0776cfb826434af8ef0f8e2c7e9e6644cfda0ae0f02c471b1eebc2483")
    idss[NOIR[0]] = NOIR[1]
    
    CRV = namedtuple("CRV", symbol_fields)
    CRV = CRV("CRV", "0x002ead91a2de57b8855b53d4a62c25277073fd7f65f7e5e79f4936ed747fcad0")
    idss[CRV[0]] = CRV[1]
    
    GRT = namedtuple("GRT", symbol_fields)
    GRT = GRT("GRT", "0x00d1fb79bbd1005a678fbf2de9256b3afe260e8eead49bb07bd3a566f9fe8355")
    idss[GRT[0]] = GRT[1]
    
    XRT = namedtuple("XRT", symbol_fields)
    XRT = XRT("XRT", "0x0083d5cbb4b90163b6a003e8f771eb7c0e2b706892cd0cbadb03f55cb9e06919")
    idss[XRT[0]] = XRT[1]
    
    ETH = namedtuple("ETH", symbol_fields)
    ETH = ETH("ETH", "0x0200070000000000000000000000000000000000000000000000000000000000")
    idss[ETH[0]] = ETH[1]
    
    UMI = namedtuple("UMI", symbol_fields)
    UMI = UMI("UMI", "0x003252667a82d2dd70fa046eea663eaec1f2e37c20879f113b880b04c5ebd805")
    idss[UMI[0]] = UMI[1]
    
    RLC = namedtuple("RLC", symbol_fields)
    RLC = RLC("RLC", "0x008294f7b08f568a661de2b248c34fc574e7e0012a12ef7959eb1a5c6b349e09")
    idss[RLC[0]] = RLC[1]
    
    MANA = namedtuple("MANA", symbol_fields)
    MANA = MANA("MANA", "0x00449af28b82575d6ac0e8c6d20e095be0917e1b0eaa63962a1dc2c6b81c2b0d")
    idss[MANA[0]] = MANA[1]    
    
    #aave = namedtuple("aave", symbol_fields)
    #self.aave = aave("AAVE", "0x0091bd8d8295b25cab5a7b8b0e44498e678cfc15d872ede3215f7d4c7635ba36")
    
    #akro = namedtuple("akro", symbol_fields)
    #self.akro = akro("AKRO", "0x0091bd8d8295b25cab5a7b8b0e44498e678cfc15d872ede3215f7d4c7635ba36")
    
    #bat = namedtuple("bat", symbol_fields)
    #self.bat = bat("BAT", "0x00e16b53b05b8a7378f8f3080bef710634f387552b1d1916edc578bda89d49e5")
    
    #busd = namedtuple("busd", symbol_fields)
    #self.busd = busd("BUSD", "0x00567d096a736f33bf78cad7b01e33463923b9c933ee13ab7e3fb7b23f5f953a")
    
    #coco = namedtuple("coco", symbol_fields)
    #self.coco = coco("COCO", "0x00374b2e4a72217a919dd1711500cd78f4c6178dc08c196e6c571d8320576c21")
    
    #link = namedtuple("link", symbol_fields)
    #self.link = link("LINK", "0x008484148dcf23d1b48908393e7a00d5fdc3bf81029a73eeca62a15ebfb1205a")
    
    #comp = namedtuple("comp", symbol_fields)
    #self.comp = comp("COMP", "0x00dbd45af9f2ea406746f9025110297469e9d29efc60df8d88efb9b0179d6c2c")
    
    #cream = namedtuple("cream", symbol_fields)
    #self.cream = cream("CREAM", "0x00521ad5caeadc2e3e04be4d4ebb0b7c8c9b71ba657c2362a3953490ebc81410")
    
    #cro = namedtuple("cro", symbol_fields)
    #self.cro = cro("CRO", "0x004d9058620eb7aa4ea243dc6cefc4b76c0cf7ad941246066142c871b376bb7e")
    
    #crv = namedtuple("crv", symbol_fields)
    #self.crv = crv("CRV", "0x002ead91a2de57b8855b53d4a62c25277073fd7f65f7e5e79f4936ed747fcad0")
    
    #dia = namedtuple("dia", symbol_fields)
    #self.dia = dia("DIA", "0x001f7a13792061236adfc93fa3aa8bad1dc8a8e8f889432b3d8d416b986f2c43")
    
    #mana = namedtuple("mana", symbol_fields)
    #self.mana = mana("MANA", "0x002ead91a2de57b8855b53d4a62c25277073fd7f65f7e5e79f4936ed747fcad0")
    
    #eth = namedtuple("eth", symbol_fields)
    #self.eth = eth("ETH", "0x0200070000000000000000000000000000000000000000000000000000000000")
    
    #ftt = namedtuple("ftt", symbol_fields)
    #self.ftt = ftt("FTT", "0x00019977e20516b9f7112cd8cfef1a5be2e5344d2ef1aa5bc92bbb503e81146e")
    
    #husd = namedtuple("husd", symbol_fields)
    #self.husd = husd("HUSD", "0x008ba21aa988b21e86d5b25ed9ea690d28a6ba6c5ba9037424c215fd5b193c32")
    
    #hot = namedtuple("hot", symbol_fields)
    #self.hot = hot("HOT", "0x004baaeb9bf0d5210a51fab72d10c84a34f53bea4e0e102d794d531a45ec50f9")
    
    #ht = namedtuple("ht", symbol_fields)
    #self.ht = ht("HT", "0x009749fbd2661866f0151e367365b7c5cc4b2c90070b4f745d0bb84f2ffb3b33")
    
    #idex = namedtuple("idex", symbol_fields)
    #self.idex = idex("IDEX", "0x006cfd2fb06c15cd2c464d1830c0d247e32f36f34233a6a266d6581ea5677582")
    
    #knc = namedtuple("knc", symbol_fields)
    #self.knc = knc("KNC", "0x001da2678bc8b0ff27d17eb4c11cc8e0def6c16a141d93253f3aa51276aa7b45")
    
    #leo = namedtuple("leo", symbol_fields)
    #self.leo = leo("LEO", "0x009e199267a6a2c8ae075bb8d4c40ee8d05c1b769085ee59ce98e50c2b2d8756")
    
    #mkr = namedtuple("mkr", symbol_fields)
    #self.mkr = mkr("MKR", "0x00ec184ef0b4bd955db05eea5a8489ae72888ab6e63682a15beca1cd39344c8f")
    
    #nexo = namedtuple("nexo", symbol_fields)
    #self.nexo = nexo("NEXO", "0x003005b2417b5046455e73f7fc39779a013f1a33b4518bcd83a790900dca49ff")
    
    #okb = namedtuple("okb", symbol_fields)
    #self.okb = okb("OKB", "0x0080edc40a944d29562b2dea2de42ed27b9047d16eeea27c5bc1b2e02786abe9")
    
    #ocean = namedtuple("ocean", symbol_fields)
    #self.ocean = ocean("OCEAN", "0x002ca40397c794e25dba18cf807910eeb69eb8e81b3f07bb54f7c5d1d8ab76b9")
    
    #pax = namedtuple("pax", symbol_fields)
    #self.pax = pax("PAX", "0x004249314d526b706a2e71e76a6d81911e4e6d7fb6480051d879fdb8ef1dccc9")
    
    #pha = namedtuple("pha", symbol_fields)
    #self.pha = pha("PHA", "0x0033271716eec64234a5324506c4558de27b7c23c42f3e3b74801f98bdfeebf7")
    
    #pdex = namedtuple("pdex", symbol_fields)
    #self.pdex = pdex("PDEX", "0x008a99c642c508f4f718598f32fa9ecbeea854e335312fecdbd298b92de26e21")
    
    #matic = namedtuple("matic", symbol_fields)
    #self.matic = matic("MATIC", "0x009134d5c7b7fda8863985531f456f89bef5fbd76684a8acdb737b3e451d0877")
    
    #ren = namedtuple("ren", symbol_fields)
    #self.ren = ren("REN", "0x00e8a7823b8207e4cab2e46cd10b54d1be6b82c284037b6ee76afd52c0dceba6")
    
    #reef = namedtuple("reef", symbol_fields)
    #self.mkr = reef("REEF", "0x0004d3168f737e96b66b72fbb1949a2a23d4ef87182d1e8bf64096f1bb348e0b")
    
    #xrt = namedtuple("xrt", symbol_fields)
    #self.xrt = xrt("XRT", "0x0083d5cbb4b90163b6a003e8f771eb7c0e2b706892cd0cbadb03f55cb9e06919")
    
    #kobe = namedtuple("kobe", symbol_fields)
    #self.kobe = kobe("KOBE", "0x008146909618facff9642fc591925ef91f10263c250cbae5db504b8b0955435a")
    
    #agi = namedtuple("agi", symbol_fields)
    #self.agi = agi("agi", "0x005e152271f8816d76221c7a0b5c6cafcb54fdfb6954dd8812f0158bfeac900d")
    
    #fis = namedtuple("fis", symbol_fields)
    #self.fis = fis("FIS", "0x00e6df883c9844e34b354b840e3a527f5fc6bfc937138c67908b1c8f2931f3e9")
    
    #sushi = namedtuple("sushi", symbol_fields)
    #self.sushi = sushi("SUSHI", "0x0078f4e6c5113b3d8c954dff62ece8fc36a8411f86f1cbb48a52527e22e73be2")
    
    #chsb = namedtuple("chsb", symbol_fields)
    #self.chsb = chsb("CHSB", "0x007d998d3d13fbb74078fb58826e3b7bc154004c9cef6f5bccb27da274f02724")
    
    #tel = namedtuple("tel", symbol_fields)
    #self.tel = tel("TEL", "0x008f925e3e422218604fac1cc2f06f3ef9c1e244e0d2a9a823e5bd8ce9778434")
    
    #ust = namedtuple("ust", symbol_fields)
    #self.ust = ust("UST", "0x00f8cfb462a824f37dcea67caae0d7e2f73ed8371e706ea8b1e1a7b0c357d5d4")
    
    #tusd = namedtuple("tusd", symbol_fields)
    #self.tusd = tusd("TUSD", "0x00d1fb79bbd1005a678fbf2de9256b3afe260e8eead49bb07bd3a566f9fe8355")
    
    #uma = namedtuple("uma", symbol_fields)
    #self.uma = uma("UMA", "0x00e40bcd6ee5363d3abbb4603273aa2f6bb89e29323729e884a8ef9c991fe73e")
    
    #usdc = namedtuple("usdc", symbol_fields)
    #self.usdc = usdc("USDC", "0x00ef6658f79d8b560f77b7b20a5d7822f5bc22539c7b4056128258e5829da517")
    
    #fans = namedtuple("fans", symbol_fields)
    #self.fans = fans("FANS", "0x00b0afb0e0762b24252dd7457dc6e3bfccfdc7bac35ad81abef31fa9944815f5")
    
    #rare = namedtuple("rare", symbol_fields)
    #self.rare = rare("RARE", "0x0047e323378d23116261954e67836f350c45625124bbadb35404d9109026feb5")
    
    #foto = namedtuple("foto", symbol_fields)
    #self.foto = foto("FOTO","0x008efe4328cba1012cb9ad97943f09cadfbeea5e692871cd2649f0bf4e718088")
    
    #uni = namedtuple("uni", symbol_fields)
    #self.uni = uni("UNI", "0x009be848df92a400da2f217256c88d1a9b1a0304f9b3e90991a67418e1d3b08c")
    
    #wbtc = namedtuple("wbtc", symbol_fields)
    #self.wbtc = wbtc("WBTC", "0x002c48630dcb8c75cc36162cbdbc8ff27b843973b951ba9b6e260f869d45bcdc")
    
    #rlc = namedtuple("rlc", symbol_fields)
    #self.rlc = rlc("RLC", "0x008294f7b08f568a661de2b248c34fc574e7e0012a12ef7959eb1a5c6b349e09")
    
    #renbtc = namedtuple("renbtc", symbol_fields)
    #self.renbtc = renbtc("RENBTC", "0x00438aac3a91cc6cee0c8d2f14e4bf7ec4512ca708b180cc0fda47b0eb1ad538")
    
    #stake = namedtuple("stake", symbol_fields)
    #self.stake = stake("STAKE", "0x005476064ff01a847b1c565ce577ad37105c3cd2a2e755da908b87f7eeb4423b")
    
    #xfund = namedtuple("xfund", symbol_fields)
    #self.xfund = xfund("XFUND", "0x007e908e399cc73f3dad9f02f9c5c83a7adcd07e78dd91676ff3c002e245d8e9")
    
    #yfi = namedtuple("yfi", symbol_fields)
    #self.yfi = yfi("YFI", "0x002676c3edea5b08bc0f9b6809a91aa313b7da35e28b190222e9dc032bf1e662")
    
class Terminal():
    
    def regexp(exp = None, txt = None, findall = None):
        match = re.findall(exp, txt)
        return match
    
    def multiple_replace(dict_ = None , text = None):
        regex_ = re.compile("|".join(map(re.escape, dict_.keys())))
        return regex_.sub(lambda mo: dict_[mo.group(0)], text)
    
    def random_digits_symbols(string_length=44):
        password_c = string.ascii_letters + string.digits + string.punctuation
        password_c = Builder.multiple_replace({"/":"#", '"':"*", "\\":"@", "|":".","`":"&", "'":"*", "^":"."}, password_c)
        return ''.join(random.choice(password_c) for i in range(string_length))    
    
    def run(comms = None, sudo = True):
        if sudo == True : comms = "sudo " + "-S " + comms
        try: proc = sub.Popen(comms, shell = True, stdout=sub.PIPE, stdin=sub.PIPE, stderr=sub.PIPE, universal_newlines=True)
        except sub.CalledProcessError as e: print(e.output)
        proc.stdin.write()
        proc.stdin.flush()
        stdout, stderr = proc.communicate()
        print("---STDOUT---")
        print(stdout)
        proc.stdin.close()
        proc_ = {"stdout":stdout, "stderr":stderr, "returncode" : proc.returncode}
        return namedtuple("Process", proc_.keys())(*proc_.values())
    def update(self): self.run(["sudo", "-S", "apt", "update"])
    def source_activate(self):
        self.run(comms = f"/bin/sh {Ziggurat.environment}", sudo=False)
        self.run(comms = "pip -V", sudo=False)
    def dump_log(self):
        with open(str(zigg.BUILD_DUMP_), "w") as log: yaml.dump(self.BUILD_DUMP, log)
        
    def upt_del(self, hdfname=None, ixname=None, start_date=None, end_date=None, updatedf=None, delete=False):
        strp_start, strp_end = self.make_dates(start_date, end_date)
        for year in range(strp_start.year, strp_end.year+1):
            for month in range(strp_start.month, strp_end.month+1):
                upt_df = updatedf.get(f"{year}-{month}", default=None)
                dfdb = self.hdfstore.get(f"_{year}/_{month}")
                dfdb.set_index(ixname, drop=False, inplace=True)
                if delete == False:
                    for ix, row in upt_df.iterrows():
                            for l, v in row.iteritems():
                                dfdb.at[row[ixname], l] = v
                elif delete == True:
                    for ix, row in upt_df.iterrows():
                        for l, v in row.iteritems(): 
                            dfdb.at[row[DELETE_], l] = v                        
                dfdb = dfdb.astype(str)
                dfdb.reset_index(ixname, drop=True, inplace=True)
                dfdb.to_hdf(Path(HDFF_, f"{hdfname}.hdf"), f"{kyear}/{kmonth}/{kday}", append=False, complevel=9)
    def close_hdfstore(self):
        try:
            self.hdfstore.close()
            self.hdfstore = None
        except AttributeError: pass
    def remove_auth_duplicates(self, duplicates=None, newdf=None, currentdb=None):
        try:
            newdf = newdf.drop_duplicates(subset=duplicates, keep="first")
            currentdb = currentdb.drop_duplicates(subset=duplicates, keep="first")
        except KeyError:
            ixname = list(newdf.index.names)
            newdf = newdf.reset_index(drop=False)
            newdf = newdf.drop_duplicates(subset=ixname, keep="first")
            newdf = newdf.set_index(ixname)
            currentdb = currentdb.reset_index(drop=False)
            currentdb = currentdb.drop_duplicates(subset=ixname, keep="first")
            currentdb = currentdb.set_index(ixname)
        return newdf, currentdb
    def join_database(self, pool=None, hdfname1=None, hdfname2=None, index=None):
        df1 = auth_database(pool, hdfname1, ix=index, toopen=True)
        df2 = auth_database(pool, hdfname2, ix=index, toopen=True)
        df1.join(df2, lsuffix="auth_column", rsuffix="auth_column", how="inner")
        df1 = df1.sort_values(["auth_column"], kind="mergesort", ascending=True)#A ORDEM DOS DADOS NAO IMPORTA, ORGANIZAR A FRENTE.
        return df1

class Tools:
    class Hdfdb:
        """Must save and load as str"""
        def __init__(self, path=None, hdfname=None, mode="a"):
            self.path,self.hdfname = path,hdfname
            try: self.hdfstore = pd.HDFStore(Path(path, f"{hdfname}.hdf"), mode="a")
            except (IOError, tables.exceptions.HDF5ExtError): 
                pd.DataFrame().to_hdf(Path(path, f"{hdfname}.hdf"), append=True, key=hdfgroup_, complevel=9, mode="w")
                self.hdfstore = pd.HDFStore(Path(path, f"{hdfname}.hdf"), mode="a")
        def make_dates(self, start_date=None, end_date=None):
            strp_start = datetime.datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')
            strp_end = datetime.datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')
            return (strp_start, strp_end)
        def sync_columns(self, writedf):
            self.close_hdfstore()
            olddf = Hdfdb(path=self.path, hdfname=self.hdfname).load(start_date="2000-01-01-01:01:01", end_date=Tools.dateformat())
            writedf.reset_index(drop=True, inplace=True)
            newdf = olddf.append(writedf)
            newdf.index = np.arange(0, len(newdf))
            os.remove(Path(self.path, f"{self.hdfname}.hdf"))
            Hdfdb(path=self.path, hdfname=self.hdfname).save(writedf=newdf, dateix=False)
        def save(self, start_date:str=None, end_date:str=None, writedf:pd.DataFrame=None, dateix=True, astype=str):
            if start_date == None: start_date=Tools.dateformat()
            if end_date == None: end_date = Tools.dateformat()
            writedf = writedf.astype(astype)      
            if dateix == True:
                writedf.set_index(dateixname_, drop=False, inplace=True)
                writedf.index = writedf.index.map(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))
                writedf.resample("M")
                strp_start, strp_end = self.make_dates(start_date=start_date, end_date=end_date)
                for year in range(strp_start.year, strp_end.year+1):
                    for month in range(strp_start.month, strp_end.month+1):
                        newdf = writedf.loc[f"{year}-{month}"]
                        try:
                            self.hdfstore.append(key=f"_{year}/_{month}", value=newdf, complevel=9)
                        except ValueError:
                            self.sync_columns(writedf)
            elif dateix == False:
                writedf = writedf.astype(astype)
                self.hdfstore.put(key=hdfgroup_, value=writedf, complevel=9, format="fixed")
            self.close_hdfstore()
            return
        def load(self, start_date=None, end_date=None, dateix=True):
            if dateix == True:
                dfdb = pd.DataFrame()
                strp_start, strp_end = self.make_dates(start_date=start_date, end_date=end_date)
                for year in range(strp_start.year, strp_end.year+1):
                    for month in range(strp_start.month, strp_end.month+1):
                        try:
                            dfget = self.hdfstore.get(f"_{year}/_{month}")
                            #dfdb = dfget.append(dfdb)
                            dfdb = pd.concat((dfget, dfdb), axis=0, sort=False)
                        except KeyError: pass
                dfdb.reset_index(drop=True, inplace=True)
                dfdb.index = np.arange(0, len(dfdb))
            elif dateix == False:
                try: dfdb = self.hdfstore.get(key=hdfgroup_)
                except KeyError: dfdb = pd.DataFrame()
            self.close_hdfstore()
            return dfdb
        
    def pickle(df=None,path=None,name=None,save=None,load=None,json=None):
        if save==None and load==None:
            try:raise Exception()
            except:zigg.Tools.error(exc="SAVE pickle or LOAD pickle ?")
        if save!=None and load!=None:
            try:raise Exception()
            except:zigg.Tools.error(exc="SAVE pickle or LOAD pickle ?")
        if save != None:
            #df=df.astype(str)
            if json == None:
                df.to_pickle(Path(path,f'{name}.pkl'))
            else: pickle.dump(df, open(f'{path}.pkl', 'wb'))
                
            return
        elif load != None:
            if json == None:
                try: df=pd.read_pickle(Path(path,f'{name}.pkl'))
                except FileNotFoundError: return pd.DataFrame()
                return df
            else: 
                try: return pickle.load(open(f"{Path(path)}.pkl", 'rb'))
                except FileNotFoundError: return dict()
        
    def df_re_build(path=None,name=None,rename:dict=None,
                    insert:tuple[int,str]=None,remove=None):
        if path == None or name == None: 
            try: raise Exception()
            except: Tools.error(exc="no path or name")
        df=Tools.pickle(path=path,name=name,load=True)
        if insert != None:
            if not isinstance(insert,tuple):
                try: raise Exception()
                except: Tools.error(exc="insert not a tuple")
            if not isinstance(insert[0],int):
                try: raise Exception()
                except: Tools.error(exc="no ix to insert new column")
            if not insert[0] >= 0:
                try: raise Exception()
                except: Tools.error(exc="ix must be positive")                
            df.insert(insert[0],insert[1],(np.nan,)*len(df.index))
        if rename != None:
            df.rename(mapper=rename,axis=1, inplace=True)
        print("df_re_building...")
        time.sleep(5)
        Tools.pickle(df=df,path=path,name=name,save=True)
            
    def numberformat(val:str):
        val = str(val)
        if ("0." in val[0:2]) or ("-0." in val[0:3]) :
            if "-0." in val: val = f"-{val[2:-1]}"
            elif "0." in val: val = val[1:]
            deci = True
        else: deci = False
        if deci == False:
            if "." in val[0:6]:val = val[0:4]
        return val
    
    def elaps(timer_=None,seconds=None,e=None, **kw):
        if timer_==None or seconds==None or e==None:
            try: raise Exception()
            except: Tools.error(exc="ARGUMENT MISSING")
            return
        elaps_ = datetime.timedelta(seconds=timer()-timer_)
        if elaps_ > datetime.timedelta(seconds=seconds):
            e(**kw)
            return timer()
        else: return timer_
    
    def error(exc:str=None,normal=False):
        assert exc != None
        trace = traceback.format_exc().split("\n")
        error = trace[1:2]
        exception = Tools.multiple_replace({"'":"",'"':'',")":""},"".join(trace[1:2]).split("(")[0])
        error[0] = (error[0].split("/"))[-1]
        error = ''.join(error).replace('"', "")
        if normal == False:
            print(f"ERROR-> {exc}, {error}")
        elif normal == True:
            print(f"{exc}, {error}")
            
    def exists_path(path): 
        if not os.path.exists(path) : os.makedirs(path)
    
    def dateformat(past:int=None,source=None):
        if source == None:strftime=lambda x:x.strftime('%Y-%m-%d %H:%M:%S')
        elif source == "investpy":strftime=lambda x:x.strftime('%d/%m/%Y')
        if past != None: return strftime(datetime.datetime.now()-datetime.timedelta(days=past))
        else: return strftime(datetime.datetime.now())
    
    def save_json(path=None, jss:dict=None):
        assert str(path)[-4:] == "json"
        with open(path, "w") as j: json.dump(obj=jss, fp=j)
    
    def load_json(path=None):
        assert str(path)[-4:] == "json"
        try:
            with open(path,"r") as j: 
                try:return json.loads(json.load(j))
                except TypeError: 
                    try: return json.load(j)
                    except json.decoder.JSONDecodeError: return dict() 
        except FileNotFoundError:
            Tools.save_json(path=path, jss={})
            return dict()
    
    def encrypt(encrypt=None, key=None, salt="Um*CWEVqi*6axa8J"):
        try:
            aes_obj = AES.new(bytes(key,"utf-8"), AES.MODE_CFB, bytes(salt,"utf-8"))
            hx_enc = aes_obj.encrypt(bytes(encrypt,"utf-8"))
            mret = b64encode(hx_enc).decode("utf-8")
            return mret
        except ValueError as value_error:
            if value_error.args[0] == 'IV must be 16 bytes long':
                raise ValueError('Encryption Error: SALT must be 16 characters long')
            elif value_error.args[0] == 'AES key must be either 16, 24, or 32 bytes long':
                raise ValueError('Encryption Error: Encryption key must be either 16, 24, or 32 characters long')
            else: raise ValueError(value_error)
    
    def decrypt(decrypt=None, key=None, salt="Um*CWEVqi*6axa8J"):
        try:
            aes_obj = AES.new(bytes(key,"utf-8"), AES.MODE_CFB, bytes(salt,"utf-8"))
            str_tmp = b64decode(decrypt.encode("utf-8"))
            str_dec = aes_obj.decrypt(str_tmp)
            mret = str_dec.decode("utf-8")
            return mret
        except ValueError as value_error:
            if value_error.args[0] == 'IV must be 16 bytes long':
                raise ValueError('Decryption Error: SALT must be 16 characters long')
            elif value_error.args[0] == 'AES key must be either 16, 24, or 32 bytes long':
                raise ValueError('Decryption Error: Encryption key must be either 16, 24, or 32 characters long')
            else: raise ValueError(value_error)
            
    def multiple_replace(dict_, text):
        regex_ = re.compile("|".join(map(re.escape, dict_.keys())))
        return regex_.sub(lambda mo: dict_[mo.group(0)], text)
    
    def fake_df(delta=None, data:dict=None):
        delta =  delta
        #date_today = datetime.datetime.now()
        #days = pd.date_range(date_today - datetime.timedelta(delta), date_today + datetime.timedelta(delta), freq='H').strftime('%Y-%m-%d-%H:%M')
        if data == None: 
            data={"LOL":1231231231, "LOL11": 88888888.0, "LOL222":1723987123.0, "LOL333":456546.0, "LOL5555": 111111111.0, "IMP. SEM DI": 555555.0}      
        date_today = datetime.datetime.now()
        days = pd.date_range(start=(datetime.datetime.now()-datetime.timedelta(days=delta)),end=datetime.datetime.now(), freq='1min')
        np.random.seed(seed=1+delta)
        df = pd.DataFrame(data=data, index=days)
        df.index.name=dateixname_
       # df.insert(0, dateixname_, days)
        #df = pd.DataFrame(
            #data={"ASSET" : ["LINK"], "VOLUME" : [round(1.727638914912, 10)], "BEFORE" : [round(18.473069157812, 10)], "AFTER" : [round(18.913956156799, 10)]},
                          #index=[Tools.dateformat()],
                          #columns=["DATA", "PRICE", "BEFORE", "AFTER"], dtype=str
        #)
        return df
    
    
"""
TO BUILD:
install rust
sudo apt-get install libffi-dev


"""