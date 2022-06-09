from multiprocessing import Process,Pipe
import fingerprint
import rfid
import network
import time

if __name__ == "__main__":
    # prepare begin #
    print("main start!")
    process_list = []
    #create pipe for processes to communicate
    #note: the data to transport via pipe(approximately 32 MiB+, though it depends on the OS) may raise a ValueError exception.
    p_rfid_fg_fg,p_rfid_fd_rfid = Pipe()
    p_rfid_nw_rfid,p_rfid_nw_nw = Pipe()

    # create fingerprint process
    fg_process = Process(target=fingerprint.fingerprintWork,name='fingerprint',args=(p_rfid_fg_fg,))
    fg_process.start()
    process_list.append(fg_process)
    print("create process name:",fg_process.name,",pid: ",fg_process.pid)

    # create rfid process
    rfid_process = Process(target=rfid.rfidWork,name='rfid',args=(p_rfid_fd_rfid,p_rfid_nw_rfid))
    rfid_process.start()
    process_list.append(rfid_process)
    print("create process name:",rfid_process.name,",pid: ",rfid_process.pid)

    # create network process
    network_process = Process(target=network.networkWork,name='network',args=(p_rfid_nw_nw,))
    network_process.start()
    process_list.append(network_process)
    print("create process name:",network_process.name,",pid: ",network_process.pid)

    # prepare end #
    while True:
        command = input("press enter to end\n")
        if command == "":
            for p in process_list:
                p.kill()
                time.sleep(0.1)
                print("process :",p.name,"(",p.is_alive(),")","had been killed")
            print("main end!")
            exit()