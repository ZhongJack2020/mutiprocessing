from multiprocessing import Process,Queue
import multiprocessing
import queue
import time

class G():
    num = 0

def fun1(rx:multiprocessing.Queue,tx:multiprocessing.Queue):
    while True:
        tx.put("fun1:give fun2 "+str(G.num))
        G.num += 1
        time.sleep(3)
        try:
            r = rx.get(timeout=1)
            print("fun1 receive:",r)
        except queue.Empty:
            print("fun1: the rx queue is empty")

    
def fun2(rx:multiprocessing.Queue,tx:multiprocessing.Queue):
    while True:
        tx.put("hello fun1 "+str(G.num))
        time.sleep(1)
        G.num += 1

if __name__ == '__main__':
    p1_r_p2 = Queue()
    p1_s_p2 = Queue()
    process_list = []
    p1 = Process(target=fun1,args=(p1_r_p2,p1_s_p2,))
    p1.start()
    process_list.append(p1)
    p2 = Process(target=fun2,args=(p1_s_p2,p1_r_p2,))
    p2.start()
    process_list.append(p2)
    while True:
        command = input("press enter to end\n")
        if command == "":
            for p in process_list:
                p.kill()
                time.sleep(0.1)
                print("process :",p.name,"(",p.is_alive(),")","had been killed")
            print("main end!")
            exit()