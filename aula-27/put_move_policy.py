# From: Hawk
# Curso: "Automatizando FortiGate com Python e REST API"
# Aula: "Prática: Mover posição de política de segurança"
# Escopo: Movimentar política de firewall 1 antes da política 2.

import requests
import creds

# Desabilita avisos de certificado digital não confiável
requests.urllib3.disable_warnings()

# Parâmetros:
# action=move
# after=[policy_id]
# before=[policy_id]
url_api = f"https://{{ENDERECO_FGT}}/api/v2/cmdb/firewall/policy/1/?action=move&before=2&vdom=root&access_token={creds.api_key_FGT740}"

response = requests.put(url_api, verify=False)
print(response)