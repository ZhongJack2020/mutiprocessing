from multiprocessing import Process,Queue
import multiprocessing
import queue
from socket import timeout
import threading
import time
import enumclass as define

class G():
    KILL_THREAD = False
    STATUS = define.LockStatus.CHECKING
    LOCK = threading.Lock()

def listenToRFID(rx_rfid:multiprocessing.Queue,tx_rfid:multiprocessing.Queue):
    while True:
        G.LOCK.acquire()
        if G.STATUS == define.LockStatus.UNLOCK_REQ:
            G.LOCK.release()
            while True:
                try:
                    tx_rfid.put_nowait(define.Request.LOCK_UNLOCK)
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
                G.LOCK.acquire()
                G.STATUS = define.LockStatus.UNLOCKING
                G.LOCK.release()
            else:
                G.LOCK.acquire()
                G.STATUS = define.LockStatus.CHECKING
                G.LOCK.release()
                print("fg: RFID status:",r,"\nplease try later")
        if G.LOCK.locked() == True:
            G.LOCK.release()
        if G.KILL_THREAD == True:
            break


def init():
    G.STATUS = define.LockStatus.CHECKING
    print("fingerprint init")

def open_door():
    print("open the door")
    G.LOCK.acquire()
    G.STATUS = define.LockStatus.UNLOCKED
    G.LOCK.release()

def close_door():
    print("close the door")
    G.LOCK.acquire()
    G.STATUS = define.LockStatus.CHECKING
    G.LOCK.release()

def fingerprintWork(rx_rfid:multiprocessing.Queue,tx_rfid:multiprocessing.Queue):
    init()
    try:
        thread_list = []
        t_rfid = threading.Thread(target=listenToRFID,args=(rx_rfid,tx_rfid,),name='listen to rfid')
        t_rfid.start()
        thread_list.append(t_rfid)
    except:
        print("fingerprint Error: create thread unsuccessfully")

    while True:
        print("fingerprint check")
        time.sleep(1)
        print("check correct, request unlock")
        G.LOCK.acquire()
        G.STATUS = define.LockStatus.UNLOCK_REQ
        G.LOCK.release()
        while G.STATUS == define.LockStatus.UNLOCK_REQ or G.STATUS == define.LockStatus.UNLOCKING:
            if G.STATUS == define.LockStatus.UNLOCKING:
                open_door()
        if G.STATUS == define.LockStatus.UNLOCKED:
            time.sleep(1)
            close_door()
