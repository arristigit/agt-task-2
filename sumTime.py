import datetime
t = '20:32:00'
timeList = ['0:45:00', t ]
mysum = datetime.timedelta()
for i in timeList:
    (h, m, s) = i.split(':')
    d = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
    mysum += d
print(datetime.time(mysum))
print(str(mysum))