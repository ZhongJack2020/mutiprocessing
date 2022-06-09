import multiprocessing
from multiprocessing import Queue,Process
import queue
import threading
import enumclass as define
import time

class G():
    KILL_THREAD = False
    STATUS = define.RFIDStatus.FREE
    LOCK = threading.Lock()

def listenToLock(rx_fg : multiprocessing.Queue,tx_fg : multiprocessing.Queue):
    while True:
        while True:
                try:
                    r = rx_fg.get_nowait()
                    break
                except queue.Empty:
                    time.sleep(0.1)
        G.LOCK.acquire()
        if r == define.Request.LOCK_UNLOCK:
            while True:
                try:
                    tx_fg.put_nowait(G.STATUS)
                    break
                except queue.Full:
                    time.sleep(0.1)
            if G.STATUS == define.RFIDStatus.FREE:
                G.STATUS = define.RFIDStatus.BUSY_FOR_USER
        G.LOCK.release()
        if G.KILL_THREAD == True:
            break

def listenToNetwork(rx_nw:multiprocessing.Queue,tx_nw:multiprocessing.Queue):
    while True:
        while True:
            try:
                r = rx_nw.get_nowait()
                break
            except queue.Empty:
                time.sleep(0.1)
        G.LOCK.acquire()
        if r == define.Request.NW_CHECK:
            while True:
                try:
                    tx_nw.put_nowait(G.STATUS)
                    break
                except queue.Full:
                    time.sleep(0.1)
            if G.STATUS == define.RFIDStatus.FREE:
                G.STATUS = define.RFIDStatus.BUSY_FOR_SERVER
        G.LOCK.release()
        if G.KILL_THREAD == True:
            break

def readerWork(server):
    print("reader work for",server,"......")
    time.sleep(1)
    G.LOCK.acquire()
    G.STATUS = define.RFIDStatus.FREE 
    G.LOCK.release()

def init():
    G.STATUS = define.RFIDStatus.FREE
    print("rfid init")

def rfidWork(rx_fg : multiprocessing.Queue,tx_fg : multiprocessing.Queue,rx_nw:multiprocessing.Queue,tx_nw:multiprocessing.Queue):
    init()
    try:
        thread_list = []
        t_lock = threading.Thread(target=listenToLock,args=(rx_fg,tx_fg,),name='listen to lock')
        t_lock.start()
        thread_list.append(t_lock)
        t_nw = threading.Thread(target=listenToNetwork,args=(rx_nw,tx_nw,),name='listen to nw')
        t_nw.start()
        thread_list.append(t_nw)
    except:
        print("rfid Error: create thread unsuccessfully")
    while True:
        G.LOCK.acquire()
        if G.STATUS == define.RFIDStatus.BUSY_FOR_USER:
            G.LOCK.release()
            readerWork("user")
        elif G.STATUS == define.RFIDStatus.BUSY.BUSY_FOR_SERVER:
            G.LOCK.release()
            readerWork("server")
        else:
            G.LOCK.release()
