from datetime import time
from datetime import datetime
from datetime import timedelta


now = datetime.now()

now2 = '13:43'
now2 = datetime.strptime(now2,"%H:%M")
after_1000h = timedelta(hours=1)
t = now2 + after_1000h

