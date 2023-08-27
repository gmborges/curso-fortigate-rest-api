# From: Hawk
# Curso: "Automatizando FortiGate com Python e REST API"
# Aula: "Prática: Realizando backup das configurações"
# Escopo: Realiza backup das configurações do FortiGate dentro do diretório fortigate-backup.

import requests
import datetime
import creds

# Desabilita avisos de certificado digital não confiável
requests.urllib3.disable_warnings()

def main():
    
    # Declaração de variáveis que compõem a URL
    device_url = "https://{{ENDERECO_FGT}}/api/v2/monitor"
    path = "/system"
    name = "/config"
    mkey = "/backup"
    child_name = ""
    child_key = ""
    parameters = f"/?scope=global&vdom=root&access_token={creds.api_key_FGT740}"

    url_api = f"{device_url}{path}{name}{mkey}{child_name}{child_key}{parameters}"
    
    # Armazena as configurações do FortiGate, consultando com o método GET
    data = requests.get(url_api, verify=False)
    
    # Cria e abre um novo arquivo para o backup com permissão de escrita
    with open(f'fortigate-backup/backup_{datetime.date.today()}.conf', 'wb') as f:
        # Escreve cada linha de configuração no novo arquivo
        for line in data:
            f.write(line)

main()