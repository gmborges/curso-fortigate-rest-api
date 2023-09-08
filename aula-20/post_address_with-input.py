# From: Hawk
# Curso: "Automatizando FortiGate com Python e REST API"
# Aula: "Prática: Criar objetos 'Address'
# Escopo: Informa a quantidade de "Address' a ser criado e seus dados para criá-los.

import requests
import json
import creds

# Desabilita avisos de certificado digital não confiável
requests.urllib3.disable_warnings()


def define_payload():

    # Define a quantidade de objetos a serem criados
    count_addr = int(input("Quantos endereços deseja configurar? "))

    # Declara a lista para armazenar cada objeto
    l1 = list()

    # Looping para criar cada objeto como dicionário
    for num in range(1, count_addr+1):
        addr_dict = dict()
        addr_dict["name"] = input(f"Nome Objeto {num}: ")
        addr_dict["type"] = "subnet"
        addr_dict["subnet"] = input(f"Subnet Objeto {num}: ")
        l1.append(addr_dict)

    # Visualizar payload completo
    #payload_view = json.dumps(l1, sort_keys=True, indent=2) # Transforma o dicionário "l1" em uma string JSON com identação de 2 espaços
    #print(payload_view)

    # Transforma o dicionário "l1" em string JSON sem identação para enviar como payload ao FortiGate
    payload = json.dumps(l1)

    return payload


def create_address(payload):
    
    # Declaração de variáveis que compõem a URL
    device_url = "https://{{ENDERECO_FGT}}/api/v2/cmdb"
    path = "/firewall"
    name = "/address"
    mkey = ""
    child_name = ""
    child_key = ""
    parameters = f"/?vdom=root&access_token={creds.api_key_FGT740}"

    url_api = f"{device_url}{path}{name}{mkey}{child_name}{child_key}{parameters}"
    
    # Envia o payload através do método POST e registra a resposta na variável 'response'
    response = requests.post(url_api, data=payload, verify=False)

    # Valida se houve erro ou sucesso na criação
    if response.status_code == 200:
        print("Address criado com sucesso!")
    else:
        print("Erro ao criar Address: " + response.text)


def main():

    payload = define_payload()
    create_address(payload)


main()
