import pickle

#467316370, 465112900 477643858
admin = [467316370]
with open('/home/bot/bot_flower/DB/admin.pickle', 'wb') as f:
    pickle.dump(admin,f)
with open('/home/bot/bot_flower/DB/admin.pickle', 'rb') as f:
    admin = pickle.load(f)

# bouquets = {}
# with open('/home/bot/bot_flower/DB/bouquets.pickle', 'wb') as f:
#     pickle.dump(bouquets,f)
# with open('/home/bot/bot_flower/DB/bouquets.pickle', 'rb') as f:
#     bouquets = pickle.load(f)

# buyer =  {}
# with open('home/bot/bot_flower/DB/buyer.pickle', 'wb') as f:
#     pickle.dump(buyer,f)
# with open('home/bot/bot_flower/DB/buyer.pickle', 'rb') as f:
#     buyer = pickle.load(f)
