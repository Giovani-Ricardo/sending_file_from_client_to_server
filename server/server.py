import base64
import socket
import json
import magic
import mimetypes


def start_server(server_adress, server_port):
    while True:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((server_adress, server_port))
        server_socket.listen()

        print(f'Server is listenning on {server_adress}:{server_port}')

        client_socket, client_address = server_socket.accept()

        print(f'Client {client_address[0]}:{client_address[1]} connected sucessfully')

        received_data = client_socket.recv(99999)
        received_data = received_data.decode()
        request = received_data.split('\r\n\r\n')
        request_headers = request[0].split('\r\n')
        request_body = json.loads(request[1])
        response = verify_request_format(request_headers, request_body)

        if response['status'] != 200:
            print(f'{response["message"]}')
        else:
            decode_and_write_file_from_base64(request_body)
            print(f'{request_body}')

        client_socket.sendall(response['message'].encode('utf-8'))
        server_socket.close()
        client_socket.close()


def verify_request_format(request_headers, request_body):
    print(request_body['base64Document'])
    if request_headers[0].split(' ')[0].strip() != 'POST':
        return {'message': f'HTTP/1.1 404 Method Not Allowed\r\n\r\n', 'status': 404}
    elif not 'base64Document' in request_body.keys():
        return {'message': f'HTTP/1.1 400 Bad request\r\n\r\n', 'status': 400}
    else:
        return {'message': f'HTTP/1.1 200 OK\r\n\r\n', 'status': 200}


def decode_and_write_file_from_base64(request_body):
    encoded_string = request_body['base64Document']
    decoded_string = base64.b64decode(encoded_string, validate=True)
    file_name = request_body['newFileName']

    file_type = magic.from_buffer(decoded_string, mime=True)
    sulfix = mimetypes.guess_extension(file_type)

    file_name = f'{file_name}{sulfix}'

    with open(file_name, 'wb') as file:
        file.write(decoded_string)


class main():
    if __name__ == '__main__':
        start_server('localhost', 8000)