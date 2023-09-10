# API de Autenticação e CRUD com Flask e JWT

Esta é um exemplo de uma API construída com o Flask que oferece funcionalidades de autenticação de usuário e operações CRUD (Create, Read, Update, Delete) em To-Dos (tarefas) usando tokens JWT (JSON Web Tokens).

## Tecnologias Utilizadas

- **Flask**: Flask é um framework web em Python para o desenvolvimento rápido de aplicativos web.

- **SQLAlchemy**: SQLAlchemy é uma biblioteca Python que fornece uma maneira conveniente de acessar e interagir com bancos de dados SQL.

- **Passlib**: Passlib é uma biblioteca Python que é usada para armazenar senhas com segurança, neste caso, usando a função de hash sha256_crypt.

- **Flask-JWT-Extended**: Flask-JWT-Extended é uma extensão do Flask que simplifica a geração e validação de tokens JWT para autenticação.

- **uuid**: A biblioteca UUID é usada para gerar identificadores exclusivos para os usuários.

## Funcionalidades

A API possui as seguintes funcionalidades:

- **Listar Todos os Usuários**: Rota `/user` (GET) que lista todos os usuários registrados. Apenas usuários com privilégios de administrador podem acessar esta rota.

- **Listar um Único Usuário**: Rota `/user/<public_id>` (GET) que lista os detalhes de um único usuário com base em seu identificador público.

- **Criar Usuário**: Rota `/user` (POST) que permite a criação de novos usuários. Apenas usuários com privilégios de administrador podem acessar esta rota.

- **Promover Usuário**: Rota `/user/<public_id>` (PUT) que permite a promoção de um usuário comum para o status de administrador. Apenas usuários com privilégios de administrador podem acessar esta rota.

- **Excluir Usuário**: Rota `/user/<public_id>` (DELETE) que permite a exclusão de um usuário. Apenas usuários com privilégios de administrador podem acessar esta rota.

- **Login de Usuário**: Rota `/login` (GET) que permite que os usuários façam login fornecendo um nome de usuário e senha. Um token JWT é gerado e retornado como parte da resposta.

- **Listar Todos os To-Do**: Rota `/todo` (GET) que lista todos os To-Dos (tarefas) registrados. Apenas usuários autenticados podem acessar esta rota.

- **Listar um Único To-Do**: Rota `/todo/<todo_id>` (GET) que lista os detalhes de um único To-Do com base em seu identificador.

- **Criar To-Do**: Rota `/todo` (POST) que permite a criação de novos To-Dos. Apenas usuários autenticados podem acessar esta rota.

- **Atualizar To-Do**: Rota `/todo/<todo_id>` (PUT) que permite a atualização de um To-Do existente. Apenas usuários autenticados podem acessar esta rota.

- **Concluir To-Do**: Rota `/todo/<todo_id>` (PUT) que permite marcar um To-Do como concluído. Apenas usuários autenticados podem acessar esta rota.

- **Excluir To-Do**: Rota `/todo/<todo_id>` (DELETE) que permite a exclusão de um To-Do. Apenas usuários autenticados podem acessar esta rota.

## Executando a API

Para executar a API, utilize o seguinte comando:


    python api.py



## Uso
Para usar a API, siga as instruções de autenticação e utilize os endpoints conforme descrito nas funcionalidades acima.


## Etiquetas

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://opensource.org/licenses/)
[![AGPL License](https://img.shields.io/badge/license-AGPL-blue.svg)](http://www.gnu.org/licenses/agpl-3.0)

