import multiprocessing
import threading
import enumclass as define
import time

class G():
    KILL_THREAD = False
    STATUS = define.RFIDStatus.FREE
    LOCK = threading.Lock()

def listenToLock(p_fg : multiprocessing.Pipe):
    while True:
        #receive by block method
        r = p_fg.recv()
        G.LOCK.acquire()
        if r == define.Request.LOCK_UNLOCK:
            p_fg.send(G.STATUS)
            #!!!! maybe exist process risk
            if G.STATUS == define.RFIDStatus.FREE:
                G.STATUS = define.RFIDStatus.BUSY_FOR_USER
        G.LOCK.release()
        if G.KILL_THREAD == True:
            break

def listenToNetwork(p_nw : multiprocessing.Pipe):
    while True:
        #receive by block method
        r = p_nw.recv()
        G.LOCK.acquire()
        if r == define.Request.NW_CHECK:
            p_nw.send(G.STATUS)
            if G.STATUS == define.RFIDStatus.FREE:
                G.STATUS = define.RFIDStatus.BUSY_FOR_SERVER
        G.LOCK.release()
        if G.KILL_THREAD == True:
            break

def readerWork():
    print("reader work……")
    time.sleep(1)
    G.LOCK.acquire()
    G.STATUS = define.RFIDStatus.FREE 
    G.LOCK.release()

def init():
    G.STATUS = define.RFIDStatus.FREE
    print("rfid init")

def rfidWork(p_fg : multiprocessing.Pipe,p_nw : multiprocessing.Pipe):
    init()
    try:
        thread_list = []
        t_lock = threading.Thread(target=listenToLock,args=(p_fg,),name='listen to lock')
        t_lock.start()
        thread_list.append(t_lock)
        t_nw = threading.Thread(target=listenToNetwork,args=(p_nw,),name='listen to nw')
        t_nw.start()
        thread_list.append(t_nw)
    except:
        print("rfid Error: create thread unsuccessfully")
    while True:
        G.LOCK.acquire()
        if G.STATUS == define.RFIDStatus.BUSY_FOR_USER:
            G.LOCK.release()
            readerWork()
        elif G.STATUS == define.RFIDStatus.BUSY.BUSY_FOR_SERVER:
            G.LOCK.release()
            readerWork()
        else:
            G.LOCK.release()


# queue method(still exist some bug)
# while True:
#     if not q_rfid_lock.empty():
#         r = q_rfid_lock.get(timeout=1)
#         print("rfid get",r)
#         if r == define.Request.UNLOCK:
#             q_rfid_lock.put(STATUS,timeout=1)
#             time.sleep(0.1)
#             if STATUS == define.RFIDStatus.FREE:
#                 # STATUS = define.RFIDStatus.BUSY_FOR_USER
#                 continue
#         else:
#             continue
#     else:
#         #print("rfid: the queue is empty!")
#         continue