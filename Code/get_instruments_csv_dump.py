import kiteconnect
import metaData
import corefunctions

api_key = metaData.getApiKey()
api_secret = metaData.getApiSecret()
request_token = metaData.getRequestToken()

#Setting up session
kite = kiteconnect.KiteConnect(api_key,api_secret)
#data = kite.generate_session(request_token,api_secret)
#kite.set_access_token(data["access_token"])

instruments = kite.instruments(exchange = kite.EXCHANGE_NFO)

hat = True
for i in instruments:
    s = ""
    p = ""
    for k in i.keys():
        if hat:
            p+=str(k)+"\t"
            #print(k)
        s+=str(i[k])+"\t"
    if hat:
        hat = False
        print(p)
    print(s)
