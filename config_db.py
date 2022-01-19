import json

with open('C:/Users/mani/Desktop/python/strategy/OptionStrategy/pythonstrategy/parameters.json', 'r') as parameter_json_file:
    y = json.load(parameter_json_file)

Capital = y['Capital']
CapitalAllocation = y['CapitalAllocation']
Portfolio = y['Portfolio']
MaxPortfolio = y['MaxPortfolio']
OCAGroupInside = y ['OCAGroupInside']
OCAGroups = y['OCAGroups']
MinLeverag = y['MinLeverag']
MaxLeverage = y['MaxLeverage']
MinDecimal = y ['MinDecimal']
SignalServer = y ['SignalServer']



Blacklist = []
with open('C:/Users/mani/Desktop/python/strategy/OptionStrategy/pythonstrategy/blacklist.json', 'r') as blacklist_json_file:
    m = json.load(blacklist_json_file)
for i in m :
    Blacklist.append(i)

with open('C:/Users/mani/Desktop/python/strategy/OptionStrategy/pythonstrategy/testopen.json', 'r') as open_json_file:
    s = json.load(open_json_file)
Strangle_open_list = []
for i in s :
    Strangle_open_list.append(s[i])

with open('C:/Users/mani/Desktop/python/strategy/OptionStrategy/pythonstrategy/testclose.json', 'r') as close_json_file:
    l = json.load(close_json_file)
Strangle_close_list = []
for i in l :
    Strangle_close_list.append(l[i])


print(Strangle_close_list)













# import psycopg2
# # connect to database 
# try:
#     connection = psycopg2.connect(database="company",
#         user="postgres",
#         password="mani1234",
#         host="127.0.0.1",
#         port="5432")
    
#     cur = connection.cursor()
    
#     command = """
#     SELECT * FROM adminsite_global_parameters ;
#     """
    
#     cur.execute(command)
    
#     result = cur.fetchall()
#     global_config = []
#     for record in result:
#         for i in record:
#             global_config.append(i)
    
# # give data from database
#     Capital = global_config[1]
#     CapitalAllocation = global_config[2]
#     Portfolio = global_config[3]
#     MaxPortfolio = global_config[4]
#     OCAGroupInside = global_config [5]
#     OCAGroups = global_config[6]
#     MinLeverag = global_config[7]
#     MaxLeverage = global_config[8]
#     MinDecimal = global_config [9]
#     SignalServer = global_config [10]
#     print("Selecting from database succeeded...")
#     connection.close()
# except:
#     connection.rollback()
#     print("Selecting from database failed...")

# # give black list data from database

# try:
#     connection = psycopg2.connect(database="company",
#         user="postgres",
#         password="mani1234",
#         host="127.0.0.1",
#         port="5432")
    
#     cur = connection.cursor()
    
#     command = """
#     SELECT * FROM adminsite_blacklist ;
#     """
    
#     cur.execute(command)
#     result = cur.fetchall()
#     blacklist = []

#     for record in result:
#         blacklist.append(record[1])
#     print("Selecting from database succeeded...")
#     connection.close()
# except:
#     connection.rollback()
#     print("Selecting from database failed...")
