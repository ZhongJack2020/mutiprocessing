import multiprocessing
import _thread
import enumclass as define
import time

def listenToRFID(p_rfid : multiprocessing.Pipe):
    while True:
        time.sleep(5)
        p_rfid.send(define.Request.NW_CHECK)
        r = p_rfid.recv()
        if r == define.RFIDStatus.FREE:
            print("network:request check success")
        else:
            print("nw: RFID status:",r,"\nplease try later")

def init():
    print("network init")

def networkWork(p_rfid : multiprocessing.Pipe):
    init()
    try:
        _thread.start_new_thread(listenToRFID,(p_rfid,))
    except:
        print("network Error: create thread unsuccessfully")
    while True:
        print("network working")
        time.sleep(10)