# from datetime import time
# from datetime import datetime
# from datetime import timedelta
#
#
# now = datetime.now()
#
# now2 = '22:43'
# now2 = datetime.strptime(now2,"%H:%M")
# after_1000h = timedelta(hours=5)
# t = now2 + after_1000h
#
# print(t)

import os, sys, time

def main():
    print("AutoRes is starting")

    executable = sys.executable
    args = sys.argv[:]
    args.insert(0, sys.executable)

    time.sleep(1)
    print("Respawning")
    os.execvp(executable, args)
    print(list)


if __name__ == "__main__":
    main()
