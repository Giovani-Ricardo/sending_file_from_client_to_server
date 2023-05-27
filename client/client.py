import requests
import base64
import json


def make_request(url, file_path, file_name):
    encoded_string = encode_file_to_base64(file_path)
    json_data = json.dumps({'base64Document': encoded_string, 'newFileName': file_name}, sort_keys=True)
    return requests.post(url, json_data)


def encode_file_to_base64(file_path):
    try:
        with open(file_path, 'rb') as file:
            encoded_string = base64.b64encode(file.read())
            return encoded_string.decode('utf-8')
    except FileNotFoundError as error:
        print(error)


class main:
    if __name__ == '__main__':
        file_path = ''
        while file_path != 'exit':
            file_path = input('Type the file path or type exit to quit: ')
            file_name = input('Type the new file name: ')
            response = make_request('http://localhost:8000', file_path, file_name)
            print(response)
