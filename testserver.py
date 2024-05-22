import socket
import threading

host = "127.0.0.1"
port = 65432


def handle_client(conn, addr):
    print(f"Connected by {addr}")
    with conn:
        while True:
            try: 
                data = conn.recv(1024)
                if not data:
                    break
                if data == b"bye":
                    print("Received termination request, closing connection")
                    conn.send(b"terminating connection")
                    break
                elif data == b"kill":
                    print("Received termination request, killing server")
                    conn.send(b"terminating connection")
                    conn.close()
                    exit(0)
                else:
                    print(data)
                    conn.sendall(b"received...")
            except Exception as e:
                print(f"An error occurred: {e}")  

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as thisSocket:
        print("""               
    ,----..            ,--.             
   /   /   \\         ,--.'|  .--.--.    
  /   .     :    ,--,:  : | /  /    '.  
 .   /   ;.  \\,`--.'`|  ' :|  :  /`. /  
.   ;   /  ` ;|   :  :  | |;  |  |--`   
;   |  ; \\ ; |:   |   \\ | :|  :  ;_     
|   :  | ; | '|   : '  '; | \\  \\    `.  
.   |  ' ' ' :'   ' ;.    ;  `----.   \\ 
'   ;  \\; /  ||   | | \\   |  __ \\  \\  | 
 \\   \\  ',  / '   : |  ; .' /  /`--'  / 
  ;   :    /  |   | '`--'  '--'.     /  
   \\   \\ .'   '   : |        `--'---'   
    `---`     ;   |.'                   
              '---'                                                   
          Welcome to Open Spice Works V0.1
          """)
        print("Waiting for connections...")
        thisSocket.bind((host, port))
        thisSocket.listen()
        
        while True:
            try:
                conn, addr = thisSocket.accept()
                client_tread = threading.Thread(target=handle_client, args=(conn, addr))
                client_tread.daemon = True
                client_tread.start()
            except Exception as e:
                print(f"An error occurred: {e}")

if __name__ == "__main__":
    start_server()