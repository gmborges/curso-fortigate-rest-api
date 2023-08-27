# From: Hawk
# Curso: "Automatizando FortiGate com Python e REST API"
# Aula: "Prática: Desligando o FortiGate"
# Escopo: Desligar o firewall FortiGate.

import requests
import creds

# Desabilita avisos de certificado digital não confiável
requests.urllib3.disable_warnings()

def main():

    # Declaração de variáveis que compõem a URL
    device_url = "https://{{ENDERECO_FGT}}/api/v2/monitor"
    path = "/system"
    name = "/os"
    mkey = "/shutdown"
    child_name = ""
    child_key = ""
    parameters = f"/?vdom=root&access_token={creds.api_key_FGT740}"

    url_api = f"{device_url}{path}{name}{mkey}{child_name}{child_key}{parameters}"

    requests.post(url_api, verify=False)


main()