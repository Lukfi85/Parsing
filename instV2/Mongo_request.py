
from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)
db = client['inst']
parse_user = ['lukfi','joteruso']
# 4) Написать запрос к базе, который вернет список подписчиков только указанного пользователя
for i in db[parse_user[0]].find({'type':'followers'}):
    print(i)

print('*'*10)

# 5) Написать запрос к базе, который вернет список профилей, на кого подписан указанный пользователь

for i in db[parse_user[1]].find({'type':'subscribe'}):
    print(i)