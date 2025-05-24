from cassandra.cluster import Cluster


def conectar():
    cluster = Cluster(['127.0.0.1']) 
    session.execute("""
        CREATE KEYSPACE IF NOT EXISTS crud_keyspace
        WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 }
    """)
    session.set_keyspace('crud_keyspace')

    session.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id UUID PRIMARY KEY,
            nome TEXT
        )
    """)
    session.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id UUID PRIMARY KEY,
            id_usuario UUID,
            titulo TEXT,
            conteudo TEXT
        )
    """)
    return session

import uuid


def adicionar_usuario(session):
    nome = input("Digite o nome do usuário: ")
    id_usuario = uuid.uuid4()
    session.execute("INSERT INTO usuarios (id, nome) VALUES (%s, %s)", (id_usuario, nome))
    print("Usuário adicionado com sucesso!")


def listar_usuarios(session):
    rows = session.execute("SELECT id, nome FROM usuarios")
    for row in rows:
        print(f"ID: {row.id}, Nome: {row.nome}")


def adicionar_post(session):
    listar_usuarios(session)
    id_usuario = input("Digite o ID do usuário que está criando o post: ")
    titulo = input("Digite o título do post: ")
    conteudo = input("Digite o conteúdo do post: ")
    id_post = uuid.uuid4()
    session.execute("INSERT INTO posts (id, id_usuario, titulo, conteudo) VALUES (%s, %s, %s, %s)",
                    (id_post, uuid.UUID(id_usuario), titulo, conteudo))
    print("Post adicionado com sucesso!")


def listar_posts(session):
    id_usuario = input("Digite o ID do usuário: ")
    rows = session.execute("SELECT id, titulo, conteudo FROM posts WHERE id_usuario = %s ALLOW FILTERING", [uuid.UUID(id_usuario)])
    for row in rows:
        print(f"\nID do Post: {row.id}\nTítulo: {row.titulo}\nConteúdo: {row.conteudo}\n")


def atualizar_post(session):
    id_post = input("Digite o ID do post que deseja atualizar: ")
    novo_titulo = input("Digite o novo título: ")
    novo_conteudo = input("Digite o novo conteúdo: ")
    session.execute("UPDATE posts SET titulo = %s, conteudo = %s WHERE id = %s",
                    (novo_titulo, novo_conteudo, uuid.UUID(id_post)))
    print("Post atualizado com sucesso!")


def excluir_post(session):
    id_post = input("Digite o ID do post que deseja excluir: ")
    session.execute("DELETE FROM posts WHERE id = %s", [uuid.UUID(id_post)])
    print("Post excluído com sucesso!")


def menu():
    session = conectar()
    while True:
        print("""
===== MENU =====
1. Adicionar Usuário
2. Listar Usuários
3. Adicionar Post
4. Listar Posts de um Usuário
5. Atualizar Post
6. Excluir Post
7. Sair
""")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            adicionar_usuario(session)
        elif opcao == '2':
            listar_usuarios(session)
        elif opcao == '3':
            adicionar_post(session)
        elif opcao == '4':
            listar_posts(session)
        elif opcao == '5':
            atualizar_post(session)
        elif opcao == '6':
            excluir_post(session)
        elif opcao == '7':
            print("Encerrando o programa.")
            break
        else:
            print("Opção inválida, tente novamente.")

if __name__ == '__main__':
    menu()
