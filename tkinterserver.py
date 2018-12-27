
import socket,threading,time

def player(conn,socketobj):
    global player_mapping
    print('Child thread under execution')
    data = conn.recv(1024)
    data = data.decode()
    print('Name entered is:',data,"decoded: ",data)
    playerinfo.update({threading.currentThread().getName():data})   #thread:player_name
    player_scores.update({playerinfo.get(threading.currentThread().getName()):0})  #player_name :0 
   
    
def player2(conn):
    global answers
    global player_mapping
    global ans_list
    print('Child thread. function 2',threading.current_thread().name)
    to_send = (0,question_list[question_no])
    conn.sendall(str(to_send).encode())
    print("Sent to",playerinfo.get(threading.currentThread().getName()))
    data = conn.recv(1024)
    print(data)
    data=data.decode()
    answers.update({playerinfo.get(threading.currentThread().getName()):data})    #player_name:answer_he_gave
        
    ans_list = list(answers.values())
    

def player3(conn):
    global question_no
    global player_scores
    global psych_list
    global answers
    print("Recieving answers..")
    data = conn.recv(1024)
    data = data.decode()
    print(data)
    for key,val in answers.items():
        print('keys',key,"data ",data,"fff",answers[key])
        if answers[key] == data:
            psych_list.update({playerinfo.get(threading.currentThread().getName()):key})   #name_of_thr_player: whose answer he/she chose
            if key=='did not get psyched':
                print("________________________________________correct____________________________________________")
                player_scores[playerinfo.get(threading.currentThread().getName())]+=10
                #res=(3,"You got it right!! :)")
                res="You got it right!! :)"
                #conn.sendall(result.encode())
            else:
                print("________________________________________wrong_____________________________________________")
                player_scores[playerinfo.get(threading.currentThread().getName())]-=5
                res="You got psyched by "+key+"!"
                
            break
    result_list[playerinfo.get(threading.currentThread().getName())] = res
    #conn.sendall(result.encode())
    #conn.sendall(player_scores)

def send_res(conn):
    to_send = (3,result_list[playerinfo.get(threading.currentThread().getName())])
    conn.sendall(str(to_send).encode())
    time.sleep(3)
    to_send = (2,player_scores)
    conn.sendall(str(to_send).encode())

if __name__ == '__main__':
    
    host = ''
    port = 2022
    ans_list=[]
    player_scores = {}
    answers = {}
    psych_list = {}
    result_list = {}
    client_threads = []
    connection_objects = []
    count = 0
    playerinfo = {}
    question_no = 0
    #question_list = ["Which chess piece is of the lowest theoretical value?","What is the capital of Canada?","Firmware is what kind of storage?"]
    #correct_ans = ["pawn","ottawa","ROM"]
    question_list = ["Which chess piece is of the lowest theoretical value?"]
    correct_ans = ["pawn"]
    #Create socket for server process,bind etc
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as socketobj:
        socketobj.bind((host,port))
        socketobj.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        socketobj.listen() #Listen for connections, start a new thread everytime a new
        #connection is made
        while True:
            conn,addr = socketobj.accept()
            connection_objects.append(conn)
            count += 1
            newThread = threading.Thread(target = player,name = 'thread'+str(count),args=(conn,socketobj,))
            client_threads.append(newThread)
            #q.put(newThread)
            newThread.start()
            print('Number of threads created:',len(client_threads))
            print(type(client_threads[0]))
            #print('Current list of players:',playerinfo)
            if count >= 2:
                break
        for thread in client_threads:
            thread.join()
        
        for i in range(3):
            try:
                answers["did not get psyched"] = correct_ans[question_no]
                print(answers)
            except:
                pass
            client_threads = []
            count = 1
            for connection in connection_objects:
                newThread = threading.Thread(target = player2,name = 'thread'+str(count),args=(connection,))
                count += 1
                client_threads.append(newThread)
                newThread.start()
            for thread in client_threads:
                thread.join()
            
            for connec in connection_objects:
                to_send = (1,ans_list)
                connec.sendall(str(to_send).encode())

            client_threads = []
            count = 1
            for connection in connection_objects:
                newThread = threading.Thread(target = player3,name = 'thread'+str(count),args=(connection,))
                count += 1
                client_threads.append(newThread)
                newThread.start()
            
            for thread in client_threads:
                thread.join()

            question_no+=1

            client_threads = []
            count = 1
            for connection in connection_objects:
                newThread = threading.Thread(target = send_res,name = 'thread'+str(count),args=(connection,))
                count += 1
                client_threads.append(newThread)
                newThread.start()
            
            for thread in client_threads:
                thread.join()
        for connection in connection_objects:
            to_send = sorted(list(player_scores.items()),key=lambda x:x[1])
            to_send = (3,to_send[-1][0] + ", Congratulations! You won!! :)")
            connection.sendall(str(to_send).encode())
            time.sleep(3)
            to_send = (4,"rdt")

            connection.sendall(str(to_send).encode())


        print(player_scores)
        print('Control passed back to main thread')
        print(playerinfo)
        print(answers.keys())
        print(answers)
