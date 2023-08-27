# From: Hawk
# Curso: "Automatizando FortiGate com Python e REST API"
# Aula: "Prática: Incluir novo membro em grupo de usuário"
# Escopo: Cria usuário baseado no endereço de e-mail inserido e habilita two-factor authentication (2FA).
#         Também adiciona o usuário ao grupo de SSL VPN.

import requests
import json
import re
import creds

# Desabilita avisos de certificado digital não confiável
requests.urllib3.disable_warnings()

# Variável com a expressão regular de um endereço de e-mail
email_pattern = r"^[a-z0-9.]+@[a-z0-9]+\.[a-z]+(\.[a-z]+)?$"


def consulta_usuario(user):
    # Consulta a lista de usuários no firewall no formato JSON e armazena em uma variável do tipo dicionário
    usuarios = requests.get(f"https://{{ENDERECO_FGT}}/api/v2/cmdb/user/local?vdom=root&access_token={creds.api_key_FGT740}", verify=False).json()

    for usuario in usuarios["results"]:
        if usuario["name"] == user:
            raise ValueError(f"Usuario {user} existe na base")


def cria_usuario(user, email_address):

    # Monta o payload do novo usuario e transforma o objeto Python (dict) em uma string JSON
    data = dict()
    data["name"] = user
    data["email-to"] = email_address
    data["status"] = "enable"
    data["two-factor"] = "email"
    data["type"] = "local"
    data["passwd"] = "P@$$w0rD_2023"

    payload = json.dumps(data)

    # Transmite o payload para criar o usuário pelo método POST
    response = requests.post(f"https://{{ENDERECO_FGT}}/api/v2/cmdb/user/local?vdom=root&access_token={creds.api_key_FGT740}", data=payload, verify=False)

    print(f"Código HTTP: {response.status_code}")


def consulta_grupos():
    # Consulta a lista de grupos no firewall no formato JSON e armazena em uma variável do tipo dicionário
    grupos = requests.get(f"https://{{ENDERECO_FGT}}/api/v2/cmdb/user/group?vdom=root&access_token={creds.api_key_FGT740}", verify=False).json()
    groups_list = grupos["results"]
    group_name = list()

    for grp in groups_list:
        print(f"{grp['name']}")
        group_name.append(grp['name'])
        
    return group_name


def user_join_grupo(user, sslvpn_group):

    # Consulta o grupo informado pelo usuário
    grp = requests.get(f"https://{{ENDERECO_FGT}}/api/v2/cmdb/user/group/{sslvpn_group}?vdom=root&access_token={creds.api_key_FGT740}", verify=False).json()
    
    # Coleta a lista de membros atuais do grupo
    grp_members = grp['results'][0]['member']
    
    # Formata o dado para acrescentar o novo usuario
    data = {'name': user}

    # Inclui o novo usuario na lista de membros
    grp_members.append(data)

    # Monta o payload e transforma o objeto Python (dict) em uma string JSON
    payload = json.dumps({"member":grp_members})

    # Transmite o payload ao grupo pelo método PUT
    response = requests.put(f"https://{{ENDERECO_FGT}}/api/v2/cmdb/user/group/{sslvpn_group}?vdom=root&access_token={creds.api_key_FGT740}", data=payload, verify=False)

    print(f"Código HTTP:{response.status_code}")


def main():

    try:
        print(f"\nCRIAÇÃO DE USUÁRIO VPN SSL COM 2FA\n")

        email_address = input(f"\nInsira o endereço de e-mail do usuário: ")

        if not re.match(email_pattern, email_address):
            raise ValueError("Endereço de e-mail inválido.")
        
        user = email_address.split("@")[0]

        consulta_usuario(user)

        print(f"\nCriando usuário {user}...")
        cria_usuario(user, email_address)

        print("\nGRUPOS DE USUÁRIOS EXISTENTES:\n")
        groups = consulta_grupos()

        sslvpn_group = input(f"\nInsira o nome do grupo que deseja adicionar {user}: ")
        
        if sslvpn_group not in groups:
            raise ValueError("O nome do grupo não está correto")

        print(f"\nAdicionando {user} ao grupo {sslvpn_group}...")
        user_join_grupo(user, sslvpn_group)

    except ValueError as error:
        print(f"Falha na execução devido: {error}")


main()