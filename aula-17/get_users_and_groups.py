# From: Hawk
# Curso: "Automatizando FortiGate com Python e REST API"
# Aula: "Prática: Consultando usuários e grupos"
# Escopo: Consulta se determinado usuário existe na base de dados do FortiGate e quais grupos ele faz parte.

import requests
import creds

# Desabilita avisos de certificado digital não confiável
requests.urllib3.disable_warnings()

def consulta_usuario(user):
    # Consulta a lista de usuários no firewall no formato JSON e armazena em uma variável do tipo dicionário
    usuarios = requests.get(f"https://{{ENDERECO_FGT}}/api/v2/cmdb/user/local?vdom=root&access_token={creds.api_key_FGT740}", verify=False).json()

    # Verifica se o usuario procurado existe na base de usuarios do FortiGate
    for usuario in usuarios["results"]:
        if usuario["name"] == user:
            print(f"Usuario {user} existe na base")
        else:
            raise ValueError("Usuario inexistente")


def consulta_grupo(user):
    # Consulta a lista de grupos no firewall no formato JSON e armazena em uma variável do tipo dicionário
    grupos = requests.get(f"https://{{ENDERECO_FGT}}/api/v2/cmdb/user/group?vdom=root&access_token={creds.api_key_FGT740}", verify=False).json()

    # Consulta cada grupo existente no firewall
    for grupo in grupos['results']:

        # Consulta cada membro existente no grupo
        membros = grupo['member']
        for membro in membros:

            # Verifica se o usuario procurado é membro do grupo
            if membro['name'] == user:
                print(f"O usuario '{user}' é membro do grupo '{grupo['name']}'")
        

def main():

    try:
        user = input("Informe o nome de usuario que deseja consultar: ")
        consulta_usuario(user)
        consulta_grupo(user)
    
    except ValueError as error:
        print(f"Falha na execução devido: {error}")


main()