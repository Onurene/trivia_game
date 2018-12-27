import socket,threading,tkinter
host = '127.0.0.1'
port = 2021

user_ans =''
user_sel =''
def func_code():
    print(user_inp.get())
    m = user_inp.get()
    global s
    global root
    
    s.sendall(str.encode(m))
    label = tkinter.Label(root,text="Welcome to trivia quiz")
    label.grid(row=4)
    questions = tkinter.Button(root,text="Click to display questions",width=50,command=questions_code)
    questions.grid(row=5)

#question sent
def questions_code():
    global s   
    global root
    global user_ans
    data = s.recv(1024)
    data = eval(data.decode())

    if data[0]==0:         
        print(data[1])
        q = tkinter.Label(root,text=data[1])
        q.grid(row=6)
        text = tkinter.Label(root,text="Your Answer:")
        text.grid(row=7)
        user_ans = tkinter.Entry(root)
        user_ans.grid(row=8)
        print(user_ans.get())
        
        c = tkinter.Button(root,text ="Choose the correct answer",width=30,command=ans_list)
        c.grid(row=9)
        
#answer list sent
def ans_list():
    global s 
    global root
    global user_ans
    global user_sel
    s.sendall(str.encode(user_ans.get()))
    data = s.recv(1024)
    data = eval(data.decode())
    
    if data[0]==1:
        print()
        print("Select!!")
        for i,value in enumerate(data[1]):
            print(i+1,value)
            r = tkinter.Label(root,text=value)
            r.grid(row=10+i)

        user_sel = tkinter.Entry(root)
        user_sel.grid(row=13) 
        m = user_sel.get()
       


        d = tkinter.Button(root,text ="Click to proceed",width=30,command=status)
        d.grid(row=14)


def status(): 
    global s
    global root
    global user_sel

    s.sendall(str.encode(user_sel.get()))
    data = s.recv(1024)
    print('entered into status')
    data = eval(data.decode())
    print(data)
    print (data[0])
    if data[0]==3:
        print(data[1])
        print("Scores are: ")
        dis = tkinter.Label(root,text=data[1])
        dis.grid(row=15)
        d = tkinter.Button(root,text ="click to see score",width=30,command=score_code)
        d.grid(row=17)


def score_code():
    global s
    global root
    print('entered into score_code')
    data = s.recv(1024)
    print(data)
 
    data1 = data.decode()
    datastr=""
    for i in data1:
        datastr+=i
        if i==")":
            break
    print(datastr)
    data = eval(datastr)
    print(data)

    if data[0]==2:
        print(data[1])
        print()
        r = tkinter.Label(root,text=data[1])
        r.grid(row=19)
        max_key=''
        min_val = -99
        for i in data[1]:
            if data[1][i]>min_val:
                max_key=i
                min_val=data[1][i]
            elif  data[1][i]==min_val:
                max_key+=";"+i
        m = tkinter.Label(root,text="Winner")
        m.grid(row=20)
        q = tkinter.Label(root,text=max_key)
        q.grid(row=21)
 
def win_code():
    global s
    global root
    print('entered into win_code')

    r = tkinter.Label(root,text="YOU WON")
    r.grid(row=21)

       

        

root = tkinter.Tk()
root.title("Psych")
frame = tkinter.Frame(root)

user_inp_label = tkinter.Label(root,text="Enter your name",width=20)
user_inp_label.grid(row=1)

user_inp = tkinter.Entry(root)
user_inp.grid(row=2)

b = tkinter.Button(root,text ="Click",width=10,command=func_code)
b.grid(row=3)



with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
    s.connect((host,port))
    text = input('Enter your name:')
    s.sendall(str.encode(text))
    
    data = s.recv(1024)
    data = data.decode()
    print("Hi,",text,data)
    print("Waiting for others to join")

    
