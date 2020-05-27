import requests
import json


dic = {}
b=[]
url = 'https://taskator12.firebaseio.com/.json'
getti = requests.get(url=url)
request = getti.json()
data = {'kiri': False}
data1 = {'kiri2': {None: None}}
dd = json.dumps(data)
y = json.loads(dd)


requests.patch(url=url, json=y)

print(request, type(request))
if request:
    for key, value in request.items():
        dic[key] = {}
        if value == False:
            dic[key] = {}
        if value != False:
            print(key)
            for items in value.keys():
                print(dic)
                print(key, '----', items)
                dic[key][items] = True
            

print(dic)

  
tab = input('key:   ')
key = input(' value:  ')
dic[tab][key] = True
print(dic) 


data = json.dumps(dic)
print(data)

y = json.loads(data)
print(y)



requests.patch(url=url, json=y) 
#requests.delete(url=url[:-5]+'germ'+'/'+'3'+'.json')

"""



rem_note = input('which note to remove:   ')
for tab, key in request.items():
    print(tab)

    for value in key:
        print(value)
        print(rem_note)
        if value == rem_note:
            dic[tab].remove(rem_note)
print(dic)          




data = json.dumps(dic)
print(data)

y = json.loads(data)
print(y)

requests.patch(url=url, json=y)
"""