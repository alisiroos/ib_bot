from ib_insync import *
from config_db import *
from datetime import datetime
import pytz
from urllib.request import urlopen
import json

ib = IB()
ib.connect('127.0.0.1', 7497)

# get combo order

class bot():    

    @staticmethod
    def GetCombo (signalId,datetime,symbol,exprdate,putstrike,callstrike,lmtprice,notes,contract_size):  
    
        # Create Call Contract 

        CallOpt = Contract(secType='OPT',symbol=symbol,lastTradeDateOrContractMonth=str(exprdate),
                                                strike=callstrike,right='C',exchange='SMART') 
        CallOpt.notes = notes
        # Create Put Contract 

        PutOpt = Contract(secType='OPT',symbol=symbol,lastTradeDateOrContractMonth=exprdate,
                                                strike=putstrike,right='P',exchange='SMART')   
        PutOpt.notes = notes
        ib.qualifyContracts(CallOpt)
        ib.qualifyContracts(PutOpt)

        # give Contract id  
        
        ConIdCall =  ib.reqContractDetails(CallOpt)[0].contract.conId

        ConIdPut =  ib.reqContractDetails(PutOpt)[0].contract.conId  

        # Create Combo Contract

        contract = Contract(symbol=str(symbol),secType='BAG',exchange='SMART',currency='USD',comboLegs=[
            ComboLeg(conId=ConIdCall,ratio=1,action='SELL',exchange='SMART',openClose=0),
            ComboLeg(conId=ConIdPut,ratio=1,action='SELL',exchange='SMART',openClose=0)
            ])
        contract.notes = notes
        testorder = MarketOrder('SELL',contract_size)
        # testorder = LimitOrder('SELL',contract_size,lmtprice)
        # marginorder = ib.whatIfOrder(CallOpt,testorder)
        # print(marginorder)
        # ib.placeOrder(contract,testorder)
        # print(ib.whatIfOrder(contract,testorder))

    
    
        return testorder,contract


    # get OCA order

    @staticmethod
    def GetOCA(ocagroup,ordergroup,ocaname):
        ib.oneCancelsAll(ocagroup,ocaname,1)

        for order in ordergroup:
            ib.placeOrder(order[1],order[0])
            ib.sleep(10)

    # get time data
    def timeMarket():
    
    # get newyork time 
        tz_NY = pytz.timezone('America/New_York') 
        datetime_NY = datetime.now(tz_NY).time()


    # return close time
        if datetime_NY < datetime.strptime('09:00',"%H:%M").time() or datetime_NY > datetime.strptime('16:00',"%H:%M").time() :
            timenow = 'close'
            return timenow
        
    # return preopen time
        elif datetime_NY > datetime.strptime('09:00',"%H:%M").time() and datetime_NY < datetime.strptime('09:30',"%H:%M").time():
            timenow = 'preopen'
            return timenow

    # return open time
        elif datetime_NY > datetime.strptime('09:30',"%H:%M").time() and datetime_NY < datetime.strptime('15:45',"%H:%M").time():
            timenow = 'open'
            return timenow

    # return precolse time
        elif datetime_NY > datetime.strptime('15:45',"%H:%M").time() and datetime_NY < datetime.strptime('16:00',"%H:%M").time():
            timenow = 'precolse'
            return timenow

    # Get holidays
    def Holidays():

        url = "https://financialmodelingprep.com/api/v3/is-the-market-open?apikey=94df3eb1bf30e7b67b9ae9c1e288458c"
        result = urlopen(url)
        data = result.read().decode("utf-8")
        data = json.loads(data)
        holidays = list()

        for i in data['stockMarketHolidays']:
            y = list(i.values())[1:]
            hdays = hdays + y
        return holidays

    # Cancel Order
    @staticmethod
    def cancel_all_orders():
        OrderIdList = []
        for ord in ib.openOrders():
            OrderIdList.append(ord)
            print(ord)
        for ord in OrderIdList:    
            ib.cancelOrder(ord)
            # print(f'order with this orderId : {ord.orderId} canecled ')
            ib.sleep(10)
        
    
                
    # get orders

    def get_orders():
        getorder = ib.orders()
        return getorder
    
    # get trades

    def get_trades():
        get_trade = ib.trades()
        return get_trade

    # get position
    def get_position():
        get_pos = ib.positions()
        return get_pos

    def get_portfolio():
        get_pos = ib.portfolio()
        return get_pos
    

    
    # get margin size
    @staticmethod
    def margin_position(signalId,datetime,symbol,exprdate,putstrike,callstrike,lmtprice):



        CallOpt = Contract(secType='OPT',symbol=symbol,lastTradeDateOrContractMonth=str(exprdate),
                                                strike=callstrike,right='C',exchange='SMART') 

        # Create Put Contract 

        PutOpt = Contract(secType='OPT',symbol=symbol,lastTradeDateOrContractMonth=exprdate,
                                                strike=putstrike,right='P',exchange='SMART')   
        ib.qualifyContracts(CallOpt)
        ib.qualifyContracts(PutOpt)

        # give Contract id  

        ConIdCall =  ib.reqContractDetails(CallOpt)[0].contract.conId

        ConIdPut =  ib.reqContractDetails(PutOpt)[0].contract.conId  

        # Create Combo Contract

        contract = Contract(symbol=str(symbol),secType='BAG',exchange='SMART',currency='USD',comboLegs=[
            ComboLeg(conId=ConIdCall,ratio=1,action='SELL',exchange='SMART',openClose=0),
            ComboLeg(conId=ConIdPut,ratio=1,action='SELL',exchange='SMART',openClose=0)
            ])


        testorder = LimitOrder('SELL',1,lmtprice)
        
        whatif = ib.whatIfOrder(contract,testorder)
        
        print(whatif)
        pos_size = Capital * CapitalAllocation / 100 / Portfolio
        
        margin_size =   pos_size / abs(float(whatif.equityWithLoanChange))

        # rounding size
        if margin_size > 1 :
            margin_size = round(margin_size)
        
        elif margin_size < 1 and margin_size > 0.75:
            margin_size = 1
        
        else :
            margin_size = 0
        
        print(margin_size)
        return margin_size

    # close all positions

    def close_all_positions(list_of_strangle):
        positions = ib.positions()  # A list of positions, according to IB

        for position in positions:
            if position.contract.symbol in Blacklist:
                continue
            if position.contract.conId in list_of_strangle:
                continue
            contract = position.contract
            contract.exchange = 'SMART'

            if position.position > 0: # Number of active Long positions
                action = 'SELL' # to offset the long positions

            elif position.position < 0: # Number of active Short positions
                action = 'BUY' # to offset the short positions

            else:
                assert False

            totalQuantity = abs(position.position)
            order = MarketOrder(action=action, totalQuantity=totalQuantity)
            ib.sleep(10)
            ib.placeOrder(contract, order)
            print(f'Flatten Position: {action} {totalQuantity} {contract.localSymbol}')
        
    def list_of_strangle():
        gettrades = ib.trades()
        listOfStrangles = []
        for i in gettrades:
            for m in i.contract.comboLegs:
                listOfStrangles.append(m.conId)
        
        return listOfStrangles
    # close singel position
    def close_positions(position):
            
        contract = position.contract
        contract.exchange = 'SMART'

        if position.position > 0: # Number of active Long positions
            action = 'SELL' # to offset the long positions

        elif position.position < 0: # Number of active Short positions
            action = 'BUY' # to offset the short positions

        else:
            assert False

        totalQuantity = abs(position.position)
        order = MarketOrder(action=action, totalQuantity=totalQuantity)
        ib.sleep(10)
        ib.placeOrder(contract, order)
        print(f'Flatten Position: {action} {totalQuantity} {contract.localSymbol}')

    # close short strangle
    def close_short_strangle(ConIdCall,ConIdPut,symbol,lmtprice,contract_size):  
     

        # Create Combo Contract

        contract = Contract(symbol=str(symbol),secType='BAG',exchange='SMART',currency='USD',comboLegs=[
            ComboLeg(conId=ConIdCall,ratio=1,action='BUY',exchange='SMART',openClose=0),
            ComboLeg(conId=ConIdPut,ratio=1,action='BUY',exchange='SMART',openClose=0)
            ])
        
        testorder = LimitOrder('BUY',contract_size,lmtprice)

        ib.placeOrder(contract,testorder)
    def number_of_combo():
        numbers = 0
        for i in ib.trades():
            if i.contract.secType == 'BAG':
                numbers += 1

        return numbers



         

        
        
        
        




    
