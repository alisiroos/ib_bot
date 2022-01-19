from check_market import *
from ib_insync import *
from config_db import *
import datetime
import pytz
import time 
tz_NY = pytz.timezone('America/New_York')

print(bot.timeMarket())
# util.startLoop()
if bot.timeMarket() == 'giz':
    pass
elif bot.timeMarket == 'preopen':
    bot.cancel_all_orders()
    time.sleep(10)
    bot.close_all_positions(bot.list_of_strangle())
    # json_files_close = []
    # for close_strangle in Strangle_close_list:
    #     bot.close_short_strangle(close_strangle['ConIdCall'],close_strangle['ConIdPut'],
    #     close_strangle['Smbol'],close_strangle['limitprice'],close_strangle['Position'])
    num1 = 0
    for orbital in range(Portfolio - bot.number_of_combo()):
        num2 = 0
        ordergroup = []
        ocagroup = []
        for short_strangle in Strangle_open_list.copy():
            Strangle_open_list.pop(Strangle_open_list.index(short_strangle))
            margin_strangle = bot.margin_position(signalId= short_strangle['SignalID'],datetime= short_strangle['SignalDateTime'],
                    symbol=short_strangle['Symbol'],exprdate=short_strangle['ExpirationDate'],
                    putstrike=short_strangle['PStrike'],callstrike=short_strangle['CStrike'],lmtprice=short_strangle['Credit'])
            strangle_order = bot.GetCombo(signalId= short_strangle['SignalID'],datetime= short_strangle['SignalDateTime'],
                    symbol=short_strangle['Symbol'],exprdate=short_strangle['ExpirationDate'],
                    putstrike=short_strangle['PStrike'],callstrike=short_strangle['CStrike'],lmtprice=short_strangle['Credit'],
                    contract_size=margin_strangle,notes= short_strangle['SignalID'])
            strangle_order[1].account = 'DU229542'
            ordergroup.append(strangle_order)
            ocagroup.append(strangle_order[0])
            ib.sleep(5)
            num2 += 1
            if num2 == 8:
                break
        bot.GetOCA(ocagroup,ordergroup,f'{datetime.datetime.now(tz_NY)}')
        num1 += 1
        if num1 == 10:
            break
    



elif bot.timeMarket() == 'open':
    bot.cancel_all_orders()
    time.sleep(10)
    bot.close_all_positions(bot.list_of_strangle())
    # for close_strangle in Strangle_close_list:
    #     bot.close_short_strangle(close_strangle['ConIdCall'],close_strangle['ConIdPut'],
    #     close_strangle['Smbol'],close_strangle['limitprice'],close_strangle['Position'])

    
    
    
    num1 = 0
    for orbital in range(Portfolio - bot.number_of_combo()):
        num2 = 0
        ordergroup = []
        ocagroup = []
        for short_strangle in Strangle_open_list.copy():
            Strangle_open_list.pop(Strangle_open_list.index(short_strangle))
            margin_strangle = bot.margin_position(signalId= short_strangle['SignalID'],datetime= short_strangle['SignalDateTime'],
                    symbol=short_strangle['Symbol'],exprdate=short_strangle['ExpirationDate'],
                    putstrike=short_strangle['PStrike'],callstrike=short_strangle['CStrike'],lmtprice=short_strangle['Credit'])
            strangle_order = bot.GetCombo(signalId= short_strangle['SignalID'],datetime= short_strangle['SignalDateTime'],
                    symbol=short_strangle['Symbol'],exprdate=short_strangle['ExpirationDate'],
                    putstrike=short_strangle['PStrike'],callstrike=short_strangle['CStrike'],lmtprice=short_strangle['Credit'],
                    contract_size=margin_strangle,notes= short_strangle['SignalID'])
            strangle_order[1].account = 'DU229542'
            ordergroup.append(strangle_order)
            ocagroup.append(strangle_order[0])
            ib.sleep(5)
            num2 += 1
            if num2 == 8:
                break
        bot.GetOCA(ocagroup,ordergroup,f'{datetime.datetime.now(tz_NY)}')
        num1 += 1
        if num1 == 10:
            break
# conids = []
# symbols = []
# contractsize = []
# for i in bot.get_position():
#     if i.contract.conId in bot.list_of_strangle():
#         print(i.contract.conId)
#         conids.append(i.contract.conId)
#         symbols.append(i.contract.symbol)
#         contractsize.append(i.position)
# bot.close_short_strangle(conids[0],conids[1],symbols[0],5,contractsize[0])
    



    
# elif bot.timeMarket == 'open':
#     pass

# 

# bot.close_all_positions()
# ordergroup = []
# ocagroup = []
# testlist = [('AAPL',200),('AAPL',160)]
# # test order
# for i in testlist:
#     marginposi = bot.margin_position('mani','mani',i[0],'20220218',i[1],210,5.75)
#     ord = bot.GetCombo('mani','mani',i[0],'20220218',i[1],150,10,'perfact',marginposi)
#     ord[1].account = 'DU229554'
#     ordergroup.append(ord)
#     ocagroup.append(ord[0])
#     ib.sleep(3)
# # print(ib.orders())
# # for i in testlist:
# #     # marginposi = bot.margin_pos('mani','mani',i[0],'20220218',i[1],150,150)
# #     # ord[1].account = 'DU229554'
# #     # ordergroup.append(ord)
# #     # ocagroup.append(ord[0])
# #     ib.sleep(3)

# bot.GetOCA(ocagroup,ordergroup,f'order{datetime.now(tz_NY)}')
# # ib.sleep(10)

# # bot.cancel_order()
# # bot.close_order()
# # return orders 
# print(bot.get_orders())
# # return trades 
# print(bot.get_trades())