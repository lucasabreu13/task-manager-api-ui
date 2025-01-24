# Task Manager API & UI

Sistema de gerenciamento de tarefas com uma **API RESTful** desenvolvida em **FastAPI** e uma interface interativa construída com **Streamlit**. Este projeto demonstra a integração entre backend e frontend, além de boas práticas de desenvolvimento.

## 🛠 Funcionalidades

### API:
- CRUD (Criar, Ler, Atualizar, Deletar) de tarefas.
- Autenticação JWT para proteger os endpoints.
- Banco de dados SQLite para persistência dos dados.
- Documentação automática da API com Swagger (disponível em `/docs`).

### Interface (UI):
- Criar novas tarefas.
- Visualizar todas as tarefas existentes.
- Atualizar informações de tarefas existentes.
- Deletar tarefas com base no ID.
- Navegação simples e intuitiva.

---

## 🚀 Tecnologias Utilizadas
- **FastAPI**: Para criação da API RESTful.
- **Streamlit**: Para construção da interface interativa.
- **SQLite**: Banco de dados relacional.
- **JWT (PyJWT)**: Autenticação segura.
- **Requests**: Comunicação entre frontend e backend.
- **Uvicorn**: Servidor ASGI para rodar a API.

---

## 🖥 Pré-requisitos
Certifique-se de ter o Python instalado (versão 3.10 ou superior).

### Instale as dependências:
```bash
pip install -r requirements.txt
