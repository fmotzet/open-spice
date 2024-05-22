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
                    thisSocket.close()
                    exit(0)
                else:
                    print(data)
                    conn.sendall(b"received...")
            except Exception as e:
                print(f"An error occurred: {e}")  

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as thisSocket:
    print("""
   ___                   ___      _         __      __       _       
  / _ \\ _ __  ___ _ _   / __|_ __(_)__ ___  \\ \\    / /__ _ _| |__ ___
 | (_) | '_ \\/ -_) ' \\  \\__ \\ '_ \\ / _/ -_)  \\ \\/\\/ / _ \\ '_| / /(_-<
  \\___/| .__/\\___|_||_| |___/ .__/_\\__\\___|   \\_/\\_/\\___/_| |_\\_\\/__/
       |_|                  |_|                                      
          Welcome to Open Spice Works V0.1
          """)
    print("Waiting for connections...")
    thisSocket.bind((host, port))
    thisSocket.listen()
    
    while True:
        try:
            conn, addr = thisSocket.accept()
            client_tread = threading.Thread(target=handle_client, args=(conn, addr))
            client_tread.start()
            # client_tread.daemon = True
            # client_tread.start()
        except Exception as e:
            print(f"An error occurred: {e}")
#hallo