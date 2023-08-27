# From: Hawk
# Curso: "Automatizando FortiGate com Python e REST API"
# Aula: "Prática: Consultando políticas de segurança"
# Escopo: Consultar políticas de segurança, exibindo somente 'policyid' e 'name'.

import requests
import creds

# Desabilita avisos de certificado digital não confiável
requests.urllib3.disable_warnings()

def main():
    
    # Declaração de variáveis que compõem a URL
    device_url = "https://{{ENDERECO_FGT}}/api/v2/cmdb"
    path = "/firewall"
    name = "/policy"
    mkey = ""
    child_name = ""
    child_key = ""
    parameters = f"/?vdom=root&access_token={creds.api_key_FGT740}"

    url_api = f"{device_url}{path}{name}{mkey}{child_name}{child_key}{parameters}"
    
    # Armazena as políticas de segurança consultadas com o método GET
    policies = requests.get(url_api, verify=False).json()

    # Exibe somente o nome e o número de identificação (ID) das políticas de segurança
    for policy in policies["results"]:
        policy_id = policy["policyid"]
        policy_name = policy["name"]
        print("ID: " + str(policy_id))
        print("NAME: " + policy_name)


main()