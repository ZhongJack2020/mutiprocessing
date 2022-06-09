import multiprocessing
from multiprocessing import Queue,Process
import _thread
import queue
import enumclass as define
import time

def listenToRFID(rx_rfid : multiprocessing.Queue,tx_rfid:multiprocessing.Queue):
    while True:
        time.sleep(5)
        while True:
                try:
                    tx_rfid.put_nowait(define.Request.NW_CHECK)
                    break
                except queue.Full:
                    time.sleep(0.1)
        while True:
                try:
                    r = rx_rfid.get_nowait()
                    break
                except queue.Empty:
                    time.sleep(0.1)
        if r == define.RFIDStatus.FREE:
            print("network:request check success")
        else:
            print("nw: RFID status:",r,"\nplease try later")

def init():
    print("network init")

def networkWork(rx_rfid : multiprocessing.Queue,tx_rfid:multiprocessing.Queue):
    init()
    try:
        _thread.start_new_thread(listenToRFID,(rx_rfid,tx_rfid,))
    except:
        print("network Error: create thread unsuccessfully")
    while True:
        print("network working")
        time.sleep(10)