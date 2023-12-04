import socket

def main():
    host = '127.0.0.1'
    port = 5555

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()

        print(f"Servidor de Envío escuchando en {host}:{port}")
        s.send(b'hola')


if __name__ == "__main__":
    main()
