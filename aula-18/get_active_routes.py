# From: Hawk
# Curso: "Automatizando FortiGate com Python e REST API"
# Aula: "Prática: Consultando rotas ativas na tabela de roteamento"
# Escopo: Consultar rotas ativas na tabela de roteamento e realizar Route Lookup.

import requests
import creds

# Desabilita avisos de certificado digital não confiável
requests.urllib3.disable_warnings()

def consulta_rotas_ativas():

   # Declaração de variáveis que compõem a URL
    device_url = "https://{{ENDERECO_FGT}}/api/v2/monitor"
    path = "/router"
    name = "/ipv4"
    mkey = ""
    child_name = ""
    child_key = ""
    parameters = f"/?vdom=root&access_token={creds.api_key_FGT740}"

    url_api = f"{device_url}{path}{name}{mkey}{child_name}{child_key}{parameters}"

    # Armazena as rotas ativas, consultando com o método GET
    rotas_ativas = requests.get(url_api, verify=False).json()

    # Exibe as rotas ativas de acordo com a formatação da saída de dados
    indice = 0
    for rota in rotas_ativas['results']:
        indice += 1
        print(f"\n# {indice} --")
        print(f"Rede: {rota['ip_mask']}")
        print(f"Gateway: {rota['gateway']}")
        print(f"Interface: {rota['interface']}")
        print(f"Distância: {rota['distance']}")
        print(f"Prioridade: {rota['priority']}")
        

def route_lookup(destino):
    # Declaração de variáveis que compõem a URL
    device_url = "https://{{ENDERECO_FGT}}/api/v2/monitor"
    path = "/router"
    name = "/lookup"
    mkey = ""
    child_name = ""
    child_key = ""
    parameters = f"/?destination={destino}&vdom=root&access_token={creds.api_key_FGT740}"

    url_api = f"{device_url}{path}{name}{mkey}{child_name}{child_key}{parameters}"

    # Armazena a rota responsável por alcançar o destino informado, consultando com o método GET
    get_rota = requests.get(url_api, verify=False).json()
    rota_selecionada = get_rota['results']

    # Exibe a rota correspondente
    print(f"")
    print(f"Rede: {rota_selecionada['network']}")
    print(f"Gateway: {rota_selecionada['gateway']}")
    print(f"Interface: {rota_selecionada['interface']}")


def main():

    while True:
        print(
            "\n1) Listar rotas ativas na tabela de roteamento (FIB)"
            "\n2) Realizar um Route Lookup"
        )
        opcao = input("\nEscolha a opção desejada: ")

        if opcao == "1":
            consulta_rotas_ativas()
            break
        elif opcao == "2":
            destino = input("\nDigite o endereço de destino: ")
            route_lookup(destino)
            break
        else:
            print("\n\nDigite uma opção válida.\n")


main()
