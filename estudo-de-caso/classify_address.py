import requests
import json
import os
from dotenv import load_dotenv
import argparse
from csv import DictReader

# Desabilita avisos de certificado digital não confiável
requests.urllib3.disable_warnings()

load_dotenv()

def parse_arguments():

    parser = argparse.ArgumentParser(description='Criar objeto "Address" com classificação automática de IP por reputação')
    
    parser.add_argument('-d', '--device', type=str, help='Identificação do firewall (740 ou 725)', required=True)
    parser.add_argument('-f', '--file', type=str, help='Nome do arquivo CSV', required=True)

    args = parser.parse_args()
    return args

def get_device_param(device):

    # Define as variáveis consultando as variáveis do arquivo .env
    device_ip = os.getenv(f"{device}_DEVICE_IP")
    device_port = os.getenv(f"{device}_DEVICE_PORT")

    device_param = dict()
    device_param["url"] = f"{device_ip}:{device_port}"
    device_param["api_key"] = os.getenv(f"{device}_DEVICE_API_KEY")

    return device_param

def define_payload(filename):
    with open(filename, "r", encoding="utf-8") as file:
        reader = DictReader(file, delimiter=';')
        return list(reader) #Retorna uma lista de dicionarários, que correspondem a cada linha do csv


def create_address(device_param, payload):

    url_api = f"https://{device_param['url']}/api/v2/cmdb/firewall/address/?vdom=root&access_token={device_param['api_key']}"

    threat_list = list()

    # Percorre cada linha do payload, que corresponde a cada objeto Address
    for address in payload:

        # Chamada a função para validar a reputação do endereço e armazena o resultado na variável 'reputacao'
        reputacao = valida_reputacao(address['subnet'])

        print(f"\nConfigurando {address['name']}")

        # Se o endereço for considerado uma ameaça, modifica o nome e adiciona em uma lista de ameaças
        if reputacao['threat']['is_threat'] is True:
            address['name'] = f"RISK_{address['subnet']}"
            print(f"Endereço identificado como ameaça. Renomeado para: {address['name']}")
            threat_list.append({"name":address['name']})

        # Transforma o dicionário "address" em string JSON para enviar como payload ao FortiGate
        payload = json.dumps(address)

        # Envia o payload através do método POST e registra a resposta na variável 'response'
        response = requests.post(url_api, data=payload, verify=False)

        # Valida se houve erro ou sucesso na criação
        if response.status_code == 200:
            print("Address criado com sucesso!")
        else:
            print("Erro ao criar Address: " + response.text)
    
    # Adiciona a lista de ameaças no grupo "RISK_GROUP"
    address_join_group(device_param, threat_list, "RISK_GROUP")


def valida_reputacao(ip):

    # Remove a informação de máscara "/32" do endereço
    address = ip[:-3]

    # Consulta reputação do endereço IP na plataforma 'ipdata.co'
    url_api = f"https://api.ipdata.co/{address}/?api-key={os.getenv('IPDATA_API_KEY')}"

    # Armazena resultado da consulta através do método GET
    address_info = requests.get(url_api).json()

    return address_info
    

def address_join_group(device_param, addresses, group_name):

    url_api = f"https://{device_param['url']}/api/v2/cmdb/firewall/addrgrp/{group_name}/?vdom=root&access_token={device_param['api_key']}"

    # Formata e transforma o dicionário em string JSON para enviar como payload ao FortiGate
    payload = json.dumps({"member":addresses})

    # Envia o payload ao FortiGate através do método PUT e registra a resposta na variável 'response'
    response = requests.put(url_api, data=payload, verify=False)

    # Valida se houve erro ou sucesso na criação
    if response.status_code == 200:
        print(f"\nAmeaças incluídas no grupo {group_name}!")
    else:
        print(f"\nErro ao incluir Addresses no grupo {group_name}: " + response.text)


def main():

    # Entrada de dados por argumentos
    args = parse_arguments()
    device = args.device

    # Coleta os parâmetros do dispositivo informado
    device_param = get_device_param(device)
    
    # Armazena na variável 'payload' os dados da lista de endereços
    payload = define_payload(args.file)

    # Executa função para criar os endereços
    create_address(device_param, payload)


main()