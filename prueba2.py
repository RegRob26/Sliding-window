import socket

def main():
    host = '127.0.0.1'
    port = 5556

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()

        print(f"Servidor de Reenvío escuchando en {host}:{port}")

        conn, addr = s.accept()
        with conn:
            print(f"Conexión establecida desde {addr}")

            while True:
                data = conn.recv(1024)
                if not data:
                    break

                # Aquí puedes agregar lógica adicional si es necesario
                print(f"Mensaje recibido: {data.decode()}")

if __name__ == "__main__":
    main()
