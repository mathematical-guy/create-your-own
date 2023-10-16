import socket


class Server:
    def __init__(self, HOST="127.0.0.1", PORT=6111, buffer_size=1024):
        self._HOST = HOST
        self._PORT = PORT
        self._buffer_size = buffer_size

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self._HOST, self._PORT))

    def parse_request(self, data: str):
        """
        Request is a string consisting of
        PATH\r\nHeaders\r\n\r\nEND

        'GET / HTTP/1.1\r\nHost: 127.0.0.1:6111\r\nUser-Agent: curl/8.2.1\r\nAccept: */*\r\n\r\n'
        After Parsing it becomes
        GET / HTTP/1.1
        Host: 127.0.0.01:6111
        User-Agent: curl/8.2.1
        Accept: */*

        """
        # Step 1) Remove last \r\n\r\n
        data = data.replace('\r\n\r\n', '')

        # Step 2) Split request string with delimeter as \r\n &
        # 3) You will get PATH & HEADERS
        data = data.split('\r\n')
        return data

    def get_response(self, path: str):
        method, path, protocol = path.split(' ')
        
        paths = {
            "/": "Hello World",
            "/home": "Welcome Home",
        }

        response_fragments = [
            "<!DOCTYPE html>",
            "<html>",
            "<head>",
            # "<title>Sample Web Page</title>",
            "</head>",
            "<body>",
            # "<h1>Hello, World!</h1>",
            "</body>",
            "</html>",
        ]
        
        response_body = paths.get(path, None)
        if response_body is None:          # 404 Page Not Found
            status = "HTTP/1.1 404 Not Found\r\n"                    # First Fragment     
            title = "<title>Page Not Found</title>"                   # Third Fragment
            body = "<body>Oops! Something went wrong</body>"         # Fifth Fragment
        else:
            status = "HTTP/1.1 200 OK\r\n"                    # First Fragment
            title = f"<title>Hello from path {path}</title>"         # Third Fragment
            body = f"<body>Hello from path {path}</body>"            # Fifth Fragment
        
        response_fragments.insert(0, status)
        response_fragments.insert(4, title)
        response_fragments.insert(5, body)

        # string_response = """HTTP/1.1 200 OK\r\n\r\n<!DOCTYPE html>\r\n<html>\r\n<head>\r\n<title>Sample Web Page</title>\r\n</head>\r\n<body>\r\n<h1>Hello, World!</h1>\r\n</body>\r\n</html>\r\n"""
        # for i in range(len(response_fragments)):
        #     response_fragments[i] = f"{response_fragments[i]}\r\n"
        
        string_response = "\r\n".join(response_fragments)

        return string_response.encode()

        # body = f"""<!DOCTYPE html>
        # <html>
        # <head>
        #     <meta charset="UTF-8">
        #     <meta name="viewport" content="width=device-width, initial-scale=1.0">
        #     <title>{response_body if response_body else 404}</title>
        # </head>
        # <body>
        #     <h1>Hello World</h1>
        # </body>
        # </html>"""
        
        # if not response_body:
        #     response_fragments.append("HTTP/1.1 404 Not Found\r\n")
        # else:
        #     response_fragments.append("HTTP/1.1 200 OK\rn")

        # response_fragments.append(body)        
        # string_response = "".join(response_fragments)
        # return string_response.encode('utf-8')

    def listen(self):
        self.sock.listen()

        print("Starting development server ...")
        print(f"Please connect to http://{self._HOST}:{self._PORT}")

        connection, address = self.sock.accept()
        with connection:
            print(f"connected with {address}")

            bytes_data = connection.recv(self._buffer_size)
            if not bytes_data or not isinstance(bytes_data, bytes):
                print(f"Error got request data as {bytes_data}")
                exit()

            data = bytes_data.decode()
            print(data)
            data = self.parse_request(data=data)
            print(data)
            response = self.get_response(path=data[0])
            connection.sendall(response)

        # self.sock.close()

        print('Connnection is closed.')
        print("Stopping server ...")


if __name__ == "__main__":
    s = Server()
    while True:
        print('Listening for new connection')
        s.listen()
