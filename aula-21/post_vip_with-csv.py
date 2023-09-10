# From: Hawk
# Curso: "Automatizando FortiGate com Python e REST API"
# Aula: "Prática: Criar objetos 'Virtual IP'"
# Escopo: A partir de um arquivo CSV, criar objetos VIP.

import requests
import json
import creds
from csv import DictReader

# Desabilita avisos de certificado digital não confiável
requests.urllib3.disable_warnings()


def define_payload():
    with open("post_vip_list.csv", "r", encoding="utf-8") as file:
        reader = DictReader(file, delimiter=';')
        return list(reader) #Retorna uma lista de dicionarários, que correspondem a cada linha do csv


def create_vip(payload):

    url_api = f"https://{{ENDERECO_FGT}}/api/v2/cmdb/firewall/vip/?vdom=root&access_token={creds.api_key_FGT740}"
    
    # Percorre cada linha do payload, que corresponde a cada objeto VIP
    for vip in payload:

        # Formata o valor da chave 'mappedip' com a estrutura correta
        vip["mappedip"] = [{"range":vip["mappedip"]}]

        print(f"\nConfigurando {vip['name']}")
        
        # Visualizar payload completo
        # payload_view = json.dumps(l1, sort_keys=True, indent=2) # Transforma o dicionário "l1" em uma string JSON com identação de 2 espaços
        # print(payload_view)
        
        # Transforma o dicionário "vip" em string JSON sem identação para enviar como payload ao FortiGate
        payload = json.dumps(vip)

        # Envia o payload ao FortiGate através do método POST e registra a resposta na variável 'response'
        response = requests.post(url_api, data=payload, verify=False)

        # Valida se houve erro ou sucesso na criação
        if response.status_code == 200:
            print("VIP criado com êxito")
        else:
            print(f"Erro ao criar NAT:\n{response.text}")


def main():

    payload = define_payload()
    create_vip(payload)


main()
