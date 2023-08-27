# From: Hawk
# Curso: "Automatizando FortiGate com Python e REST API"
# Aula: "Prática: Incluir 'Address' em 'Address Group'"
# Escopo: Adicionar objetos "Address" declarados em um arquivo CSV dentro de um "Address Group".

import requests
import json
from csv import DictReader
import creds

# Desabilita avisos de certificado digital não confiável
requests.urllib3.disable_warnings()


def define_payload():
    with open("address_list.csv", "r", encoding="utf-8") as file:
        reader = DictReader(file, delimiter=';')
        return list(reader) #Retorna uma lista de dicionarários, que correspondem a cada linha do csv


def create_address(payload):

    url_api = f"https://{{ENDERECO_FGT}}/api/v2/cmdb/firewall/address/?vdom=root&access_token={creds.api_key_FGT740}"

    address_list = list()

    # Percorre cada linha do payload, que corresponde a cada objeto Address
    for address in payload:

        print(f"\nConfigurando {address['name']}")

        # Transforma o dicionário "address" em string JSON sem identação para enviar como payload ao FortiGate
        payload = json.dumps(address)

        # Envia o payload através do método POST e registra a resposta na variável 'response'
        response = requests.post(url_api, data=payload, verify=False)

        # Valida se houve erro ou sucesso na criação
        if response.status_code == 200:
            print("Address criado com sucesso!")
            address_list.append({"name":address['name']}) # Adiciona à lista "address_list" um novo dicionário contendo somente a chave "name"
        else:
            print("Erro ao criar Address: " + response.text)
    
    return address_list


def address_join_group(addresses, group_name):

    url_api = f"https://{{ENDERECO_FGT}}/api/v2/cmdb/firewall/addrgrp/{group_name}/?vdom=root&access_token={creds.api_key_FGT740}"

    # Formata e transforma o dicionário em string JSON para enviar como payload ao FortiGate
    payload = json.dumps({"member":addresses})

    # Envia o payload ao FortiGate através do método PUT e registra a resposta na variável 'response'
    response = requests.put(url_api, data=payload, verify=False)

    # Valida se houve erro ou sucesso na criação
    if response.status_code == 200:
        print(f"\nAddresses incluídos no grupo {group_name}!")
    else:
        print(f"\nErro ao incluir Addresses no grupo {group_name}: " + response.text)


def main():

    payload = define_payload()
    addresses = create_address(payload)
    address_join_group(addresses, "GRUPO_TESTE")


main()