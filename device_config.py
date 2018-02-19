import requests
import time
from dados_estacao import pegarestacoes


def get_token_sys():
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }

    data = '{"username":"tenant@thingsboard.org", "password":"tenant"}'

    response = requests.post('http://localhost:8080/api/auth/login', headers=headers, data=data)

    t = str(response.content)
    t = t.split('"')
    token = str(t[3])
    return token


def create_device(name):
    token = 'Bearer ' + get_token_sys()
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'X-Authorization': token,
    }

    data = '{ \n   "additionalInfo": null, \n   "createdTime": 0, \n   "name": "' + str(
        name) + '",\n   "type": "default" \n }'

    response = requests.post('http://localhost:8080/api/device', headers=headers, data=data)

    t = str(response.content)
    t = t.split('"')
    device_id = t[9]
    device_name = t[-8]

    g = open("devices.txt", "a")
    g.write(device_name + "\n")
    g.write(device_id + "\n")
    g.close()
    print(device_id)
    return str(device_id)


def get_credentials(device):
    token = 'Bearer ' + get_token_sys()
    headers = {
        'Accept': 'application/json',
        'X-Authorization': token,
    }

    response = requests.get('http://localhost:8080/api/device/' + str(device) + '/credentials', headers=headers)
    t = str(response.content)
    t = t.split('"')
    credential = str(t[-4])
    g = open("credentials.txt", "a")
    g.write(credential + "\n")
    g.close
    return credential


def create_base_devices():
    dic = pegarestacoes()
    dic_list = list(dic.keys())
    time.sleep(2)
    for i in range(4):
        item = dic_list[i]
        print("Create device with id: {}".format(i))
        device = create_device(item)
        time.sleep(0.5)
        print("Device created.")
        time.sleep(0.5)
        print("Geting credencials.")
        cred = get_credentials(device)
        print("Credencials of the device: {}".format(cred))
        time.sleep(2)


create_base_devices()
