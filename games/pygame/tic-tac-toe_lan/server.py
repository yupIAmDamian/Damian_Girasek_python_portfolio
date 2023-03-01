
import socket
import threading
import time
class SERVER:
    #server vars
    HEADER = 64
    hostname = socket.gethostname()
    HOST = socket.gethostbyname(hostname)
    PORT = 9090
    ADDR = (HOST,PORT)
    FORMAT = 'utf-8'
    active_conn = []
    
    #playground grid
    playground = [[0,0,0],[0,0,0],[0,0,0]]
    
    def __init__(self):
        #set up server
        self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server.bind(self.ADDR)
        
    def send_msg(self,msg,conn):
        #info how long the message is. Better dealing on client side
        msg_len = len(msg)
        send_len = str(msg_len).encode(self.FORMAT)
        send_len += b' '* (self.HEADER-len(send_len))
        conn.send(send_len)
        
        #message
        message = msg.encode(self.FORMAT)
        conn.send(message)
        
    def check_if_winner(self):
        #row winner
        for pattern in ["x","o"]:
            if self.playground[0] == [pattern,pattern,pattern]:
                self.end(pattern,f"{0}{0}{2}{0}")
                return 
            if self.playground[1] == [pattern,pattern,pattern]:
                self.end(pattern,f"{0}{1}{2}{1}")
                return
            if self.playground[2] == [pattern,pattern,pattern]:
                self.end(pattern,f"{0}{2}{2}{2}")
                return    
        #column winner    
        i = 0
        for pattern in ["x","o"]: 
            for i in range(len(self.playground)):
                if self.playground[0][i] == self.playground[1][i] == self.playground[2][i] == pattern:
                    self.end(pattern,f"{i}{0}{i}{2}")
                    return
        #from topleft to bottomright winner                     
        for pattern in ["x","o"]:        
            if self.playground[0][0] == self.playground[1][1] == self.playground[2][2] == pattern:
                self.end(pattern,f"{0}{0}{2}{2}")
                return
            
        #from topright to bottomleft winner    
        for pattern in ["x","o"]:        
            if self.playground[0][2] == self.playground[1][1] == self.playground[2][0] == pattern:
                self.end(pattern,f"{2}{0}{0}{2}")
                return
                
    def end(self,pattern,pos):
        #this method will be called if there is winner 
        
        print(f"winner is {pattern}")
        self.playground = [[0,0,0],[0,0,0],[0,0,0]]
        self.send_to_connections(f"?LINE{pos}")  
        time.sleep(2.5)
        self.send_to_connections("?NEWGAME")   

    def find_conn(self,conn):
        for i in self.active_conn:
            if i['CONN'] == conn:
                return i
                
    def handle_client(self,conn,addr):
        print(f"[SERVER INFO] client {addr} connected", end='\n')
        
        running = True
        while running:
            msg_len = conn.recv(self.HEADER).decode(self.FORMAT)
            
            if msg_len:
                msg_len = len(msg_len)
                msg = conn.recv(msg_len).decode(self.FORMAT)
                if msg == '!DISCONNECT':
                    connect = self.find_conn(conn)
                    running = False
                    self.active_conn.remove(connect)
                    print(f"[[SERVER INFO] clients connected:  {len(self.active_conn)}]", end='\n')
                if msg[0] == "!" and len(msg)==4:
                    y = int(msg[1])
                    x = int(msg[2])
                    if  self.playground[y][x] == 0:
                        self.playground[y][x] = msg[3]
                        self.send_to_connections(f"!{self.playground}")
                        print(self.playground)
                    self.check_if_winner()
                    for i in self.active_conn:
                        if i["CONN"] != conn:
                            self.send_msg("?PERMISSION",i["CONN"])
                
        conn.close()
    def send_to_connections(self,msg):
        for i in self.active_conn:
            t = threading.Thread(target=self.send_msg(msg,i["CONN"]))
            t.start()
            
    def run_server(self):
        self.server.listen()
        print(f"[SERVER LISTENING] server is listening on {self.HOST}", end='\n')
    
        while True:
            conn, addr = self.server.accept()

            if len(self.active_conn)  <= 1 :
                self.active_conn.append({'ADDR':addr, 'CONN':conn,"PATTERN":"o"})
                print(len(self.active_conn))
                t = threading.Thread(target=self.handle_client, args=(conn,addr))
                t.start()
                print(f"[[SERVER INFO] clients connected: {len(self.active_conn)}]", end='\n')
                if len(self.active_conn) == 2:
                    self.send_to_connections("?GAMEPOSSIBLE")
                    self.send_msg("!x",self.active_conn[0]["CONN"])
                    for index, i in enumerate(["x","o"]):
                        t = threading.Thread(target=self.send_msg("!{i}",i["CONN"]))
                        t.start()
                        self.active_conn[index]["PATTERN"] = i
                else:
                    self.send_to_connections("?NOTPLAYABLE")
                    self.playground = [[0,0,0],[0,0,0],[0,0,0]]
            else:
                self.send_msg("[SERVER] You can't join the server because server it is full",conn)
                conn.close()
                
server = SERVER()

print("[SERVER] server is starting...")
server.run_server()