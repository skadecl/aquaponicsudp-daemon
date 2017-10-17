# Logger lib
# Roberto Roman

import datetime

def AQLog(type = "", text = "", info = ""):
    if type != "" and text != "":
        if info != "":
            info = "(" + info + ")"
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print "[%s | %s] %s %s" % (type, now, text, info)
