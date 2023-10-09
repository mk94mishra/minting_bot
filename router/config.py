proxy = [
    "proxy_one",
    "proxy_two",
    "proxy_three",
    "proxy_four",
    ]

database = {
    "db":'../db_proxy.db'
}

custom = {
    "proxy_max_time":60000, # 60 second
    "proxy_max_weightage":5500  
}

proxy_url ={
    'proxy_one':'http://3.145.60.97:80',
    'proxy_two':'http://3.12.123.111:80',
    'proxy_three':'http://18.220.46.156:80',
    'proxy_four':'http://18.116.51.129:80'
    # 'proxy_five':'http://18.116.51.129:80'
}

# proxy_url ={
#     'proxy_one':'http://127.0.0.1:8000',
#     'proxy_two':'http://127.0.0.1:8000',
#     'proxy_three':'http://127.0.0.1:8000',
#     'proxy_four':'http://127.0.0.1:8000',
#     'proxy_five':'http://127.0.0.1:8000'
# }


#[apiurl, weightage,weightage_minut,event_time,proxy_name]
proxy_details = [
    	['https://api.binance.com',0,0,0,'proxy_one'],
        ['https://api1.binance.com',0,0,0,'proxy_one'],
        ['https://api2.binance.com',0,0,0,'proxy_one'],
        ['https://api3.binance.com',0,0,0,'proxy_one'],
        ['https://api.binance.com',0,0,0,'proxy_two'],
        ['https://api1.binance.com',0,0,0,'proxy_two'],
        ['https://api2.binance.com',0,0,0,'proxy_two'],
        ['https://api3.binance.com',0,0,0,'proxy_two'],
        ['https://api.binance.com',0,0,0,'proxy_three'],
        ['https://api1.binance.com',0,0,0,'proxy_three'],
        ['https://api2.binance.com',0,0,0,'proxy_three'],
        ['https://api3.binance.com',0,0,0,'proxy_three'],
        ['https://api.binance.com',0,0,0,'proxy_four'],
        ['https://api1.binance.com',0,0,0,'proxy_four'],
        ['https://api2.binance.com',0,0,0,'proxy_four'],
        ['https://api3.binance.com',0,0,0,'proxy_four']
    ]