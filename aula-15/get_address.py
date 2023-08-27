# From: Hawk
# Curso: "Automatizando FortiGate com Python e REST API"
# Aula: "Prática: Consultando objetos 'Address'"
# Escopo: Consultar objetos "Address" no firewall FortiGate, exibindo somente o campo "name", nomeados com a inicial "HOST".

import requests
import creds

# Desabilita avisos de certificado digital não confiável
requests.urllib3.disable_warnings()

def main():
    
    # Declaração de variáveis que compõem a URL
    device_url = "https://{{ENDERECO_FGT}}/api/v2/cmdb"
    path = "/firewall"
    name = "/address"
    mkey = ""
    child_name = ""
    child_key = ""
    parameters = f"/?vdom=root&access_token={creds.api_key_FGT740}&format=name&filter=name=@HOST"

    url_api = f"{device_url}{path}{name}{mkey}{child_name}{child_key}{parameters}"

    # Armazena os endereços consultados com o método GET conforme os filtros e parâmetros declarados
    addresses = requests.get(url_api, verify=False).json()

    # Exibe somente os nomes dos Objetos
    print("Objetos 'Address' com a inicial 'HOST_' existentes:")
    for address in addresses["results"]:
        print(address["name"])


main()