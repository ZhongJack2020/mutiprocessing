import multiprocessing
import threading
import time
import enumclass as define

class G():
    KILL_THREAD = False
    STATUS = define.LockStatus.CHECKING
    LOCK = threading.Lock()

def listenToRFID(p_rfid:multiprocessing.Pipe):
    while True:
        G.LOCK.acquire()
        if G.STATUS == define.LockStatus.UNLOCK_REQ:
            G.LOCK.release()
            p_rfid.send(define.Request.LOCK_UNLOCK)
            #receive by block method
            r = p_rfid.recv()
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

def fingerprintWork(p_rfid:multiprocessing.Pipe):
    init()
    try:
        thread_list = []
        t_rfid = threading.Thread(target=listenToRFID,args=(p_rfid,),name='listen to rfid')
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



# queue method(still exist some bug)
    # try_time = 0
    # while try_time < REQUEST_TIME:
    #     q_rfid_fp.put(define.Request.LOCK_UNLOCK,timeout=1)
    #     time.sleep(0.5)
    #     if not q_rfid_fp.empty():
    #         r = q_rfid_fp.get(timeout=1)
    #         if r == define.RFIDStatus.FREE:
    #             open_door()
    #             break
    #         elif r == define.Request.LOCK_UNLOCK:
    #             print("no respond")
    #             try_time += 1
    #         elif r == define.RFIDStatus.BUSY:
    #             print("rfid is busy now, try again")
    #             break
    #         else:
    #             print("fingerprint receive error!!!")
    #             break
    #     else:
    #         print("fingerprint: the queue is empty!")
    #         break
        