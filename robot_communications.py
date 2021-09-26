#JTM 2021
#socket robot command class
#used to format basic commands into dictionary objects to be sent over network socket

import json

class commands:
    #create dictionary objects with specified left and right motor values
    #return formatted dictionary objects in an array
    def motor(left_motor_val=None, right_motor_val=None):
        arr = []
        if left_motor_val is not None:
            arr.append({"left_speed": left_motor_val})
        if right_motor_val is not None:
            arr.append({"right_speed": right_motor_val})
        return arr

    #create an auger_lift message dictionary object
    #should be used change the auger lift direction
    def auger_lift(value):
        return [{"auger_lift": value}]

    #create an auger_slide message dictionary object
    #should be used change the auger slide direction
    def auger_slide(value):
        return [{"auger_slide": value}]

    #create an auger_drive message dictionary object
    #should be used to change the auger drive direction
    def auger_drive(value):
        return [{"auger_drive": value}]

    #create an belt_lift message dictionary object
    #should be used to change the belt lift direction
    def belt_lift(value):
        return [{"belt_lift": value}]

    #create an belt_drive message dictionary object
    #should be used change the belt drive direction
    def belt_drive(value):
        return [{"belt_drive": value}]

    #create an "OK" message dictionary object
    #should be used as an acknowledgement
    def ok():
        return [{"OK": "OK"}]

    #create a "STOP" command
    #should be used to signify the end of a socket connection
    def stop():
        return [{"STOP":"STOP"}]

    #function to format an array of commands into a json field "arr"
    #and convert it to a byte string object
    #byte string object is returned
    def format_arr(pay_arr):
        msg = json.dumps({"arr":pay_arr})
        return bytes(msg+',', 'utf-8')
