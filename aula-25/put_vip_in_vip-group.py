# From: Hawk
# Curso: "Automatizando FortiGate com Python e REST API"
# Aula: "Prática: Incluir 'Virtual IP' em 'VIP Group'"
# Escopo: Incluir objetos "Virtual IP" de um arquivo CSV dentro de um "Virtual Group"

import requests
import json
from csv import DictReader
import creds

# Desabilita avisos de certificado digital não confiável
requests.urllib3.disable_warnings()


def define_payload():
    with open("vip_list.csv", "r", encoding="utf-8") as file:
        reader = DictReader(file, delimiter=';')
        return list(reader) #Retorna uma lista de dicionarários, que correspondem a cada linha do csv


def create_vip(payload):

    url_api = f"https://{{ENDERECO_FGT}}/api/v2/cmdb/firewall/vip/?vdom=root&access_token={creds.api_key_FGT740}"
    
    vip_list = list()

    # Percorre cada linha do payload, que corresponde a cada objeto VIP
    for vip in payload:

        # Formata o valor da chave 'mappedip' com a estrutura correta
        vip["mappedip"] = [{"range":vip["mappedip"]}]

        print(f"\nConfigurando {vip['name']}")
        
        # Transforma o dicionário "vip" em string JSON sem identação para enviar como payload ao FortiGate
        payload = json.dumps(vip)

        # Envia o payload ao FortiGate através do método POST e registra a resposta na variável 'response'
        response = requests.post(url_api, data=payload, verify=False)

        # Valida se houve erro ou sucesso na criação
        if response.status_code == 200:
            print("VIP criado com êxito")
            vip_list.append({"name":vip['name']})
        else:
            print(f"Erro ao criar NAT: {response.text}")
    
    return vip_list


# def update_vip_group_members(vips, group_name):

#     url_api = f"https://{{ENDERECO_FGT}}/api/v2/cmdb/firewall/vipgrp/{group_name}/?vdom=root&access_token={creds.api_key_FGT740}"

#     # Formata e transforma o dicionário em string JSON para enviar como payload ao FortiGate
#     payload = json.dumps({"member":vips})

#     # Envia o payload ao FortiGate através do método PUT e registra a resposta na variável 'response'
#     response = requests.put(url_api, data=payload, verify=False)

#     # Valida se houve erro ou sucesso na criação
#     if response.status_code == 200:
#         print(f"\nVIPs incluídos no grupo {group_name}!")
#     else:
#         print(f"\nErro ao incluir VIPs no grupo {group_name}: " + response.text)


def vip_join_group(vips, group_name):

    url_api = f"https://{{ENDERECO_FGT}}/api/v2/cmdb/firewall/vipgrp/{group_name}/?vdom=root&access_token={creds.api_key_FGT740}"

    # Armazena os dados do VIP Group consultado, com o método GET
    vipgrp = requests.get(url_api, verify=False).json()

    # Variável com os membros do VIP Group
    vipgrp_members = vipgrp['results'][0]['member']

    # Adiciona os novos VIPs à lista atual de membros do VIP Group
    for vip in vips:
        vipgrp_members.append(vip)

    # Formata e transforma o dicionário em string JSON para enviar como payload ao FortiGate
    payload = json.dumps({"member":vipgrp_members})

    # Envia o payload ao FortiGate através do método PUT e registra a resposta na variável 'response'
    response = requests.put(url_api, data=payload, verify=False)

    # Valida se houve erro ou sucesso na criação
    if response.status_code == 200:
        print(f"\nVIPs incluídos no grupo {group_name}!")
    else:
        print(f"\nErro ao incluir VIPs no grupo {group_name}: " + response.text)


def main():

    payload = define_payload()
    vips = create_vip(payload)

    # Sobrescreve os membros do VIP Group (demonstração)
    #update_vip_group_members(vips, "VIP_GRUPO_TESTE")

    # Adiciona os novos VIP aos membros do VIP Group
    vip_join_group(vips, "VIP_GRUPO_TESTE")

main()