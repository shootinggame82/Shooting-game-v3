#!/usr/bin/python
# Props to user brechmos for sharing the code here: https://www.raspberrypi.org/forums/viewtopic.php?t=55100

# Tested with the following barcode scanner
# macbook# ioreg -p IOUSB 
# <snip>
#   | +-o WIT 122-UFS V2.03@14200000  <class AppleUSBDevice, id 0x10000c3c4, registered, matched, active, busy 0 (6 ms), retain 14>

#        WIT 122-UFS V2.03:
#          Product ID: 0x1010
#          Vendor ID: 0x05fe  (CHIC TECHNOLOGY CORP)
#          Version: 0.01
#          Speed: Up to 12 Mb/sec
#          Manufacturer: WIT Electron Company
#          Location ID: 0x14200000 / 4
#          Current Available (mA): 500
#          Current Required (mA): 500
#          Extra Operating Current (mA): 0

import sys
import mysql.connector as mysql
# Open the DB Connection
time.sleep(10)
db = mysql.connect(
    host="localhost",
    user="admin",
    passwd="tantamalia",
    database="shooting"
)

done1 = False


while not done1:
    hid = { 4: 'a', 5: 'b', 6: 'c', 7: 'd', 8: 'e', 9: 'f', 10: 'g', 11: 'h', 12: 'i', 13: 'j', 14: 'k', 15: 'l', 16: 'm', 17: 'n', 18: 'o', 19: 'p', 20: 'q', 21: 'r', 22: 's', 23: 't', 24: 'u', 25: 'v', 26: 'w', 27: 'x', 28: 'y', 29: 'z', 30: '1', 31: '2', 32: '3', 33: '4', 34: '5', 35: '6', 36: '7', 37: '8', 38: '9', 39: '0', 44: ' ', 45: '-', 46: '=', 47: '[', 48: ']', 49: '\\', 51: ';' , 52: '\'', 53: '~', 54: ',', 55: '.', 56: '/'  }

    hid2 = { 4: 'A', 5: 'B', 6: 'C', 7: 'D', 8: 'E', 9: 'F', 10: 'G', 11: 'H', 12: 'I', 13: 'J', 14: 'K', 15: 'L', 16: 'M', 17: 'N', 18: 'O', 19: 'P', 20: 'Q', 21: 'R', 22: 'S', 23: 'T', 24: 'U', 25: 'V', 26: 'W', 27: 'X', 28: 'Y', 29: 'Z', 30: '!', 31: '@', 32: '#', 33: '$', 34: '%', 35: '^', 36: '&', 37: '*', 38: '(', 39: ')', 44: ' ', 45: '_', 46: '+', 47: '{', 48: '}', 49: '|', 51: ':' , 52: '"', 53: '~', 54: '<', 55: '>', 56: '?'  }

    fp = open('/dev/hidraw0', 'rb')


    ss = ""
    shift = False

    done = False

    totquick = 0
    tottime = 0
    totrapid = 0
    #Keep all in loop

    while not done:
        ## Get the character from the HID
        buffer = fp.read(8)
        for c in buffer:
            if ord(c) > 0:
                ##  40 is carriage return which signifies
                ##  we are done looking for characters
                if int(ord(c)) == 40:
                    done = True
                    break;
                ##  If we are shifted then we have to 
                ##  use the hid2 characters.
                if shift: 
                    ## If it is a '2' then it is the shift key
                    if int(ord(c)) == 2 :
                        shift = True
                    ## if not a 2 then lookup the mapping
                    else:
                        ss += hid2[ int(ord(c)) ]
                        shift = False
                ##  If we are not shifted then use
                ##  the hid characters
                else:
                    ## If it is a '2' then it is the shift key
                    if int(ord(c)) == 2 :
                        shift = True
                    ## if not a 2 then lookup the mapping
                    else:
                        ss += hid[ int(ord(c)) ]
    print(ss)
    codestring = str(ss)
    db.commit()
    tacur = db.cursor()
    sqlo = "SELECT * FROM savedquick WHERE gamecode = %s"
    val = (codestring,)
    tacur.execute(sqlo, val)
    resa = tacur.fetchall()
    totquick = tacur.rowcount
    #Check timed also
    tacur1 = db.cursor()
    sqlo1 = "SELECT * FROM savedtimed WHERE gamecode = %s"
    val1 = (codestring,)
    tacur1.execute(sqlo, val)
    resa1 = tacur1.fetchall()
    tottimed = tacur1.rowcount
    #Check rapid also
    tacur2 = db.cursor()
    sqlo2 = "SELECT * FROM savedrapid WHERE gamecode = %s"
    val2 = (codestring,)
    tacur2.execute(sqlo, val)
    resa2 = tacur1.fetchall()
    totrapid = tacur2.rowcount
    #Now we need to update sql if exist somewere
    if totquick > 0 or tottimed > 0 or totrapid > 0:
        #We have some games with it so inform websystem to open
        print("We got some game saved")
        cura = db.cursor()
        savesql = "UPDATE settings SET eancodescan = %s, eancode = %s WHERE id =%s"
        val = ("1", codestring, "1")
        cura.execute(savesql, val)
        db.commit()
        ss = ""
        done = False
    else:
        print("Nothing saved")
        cura = db.cursor()
        savesql = "UPDATE settings SET eancodescan = %s WHERE id =%s"
        val = ("0", "1")
        cura.execute(savesql, val)
        db.commit()
        ss = ""
        done = False