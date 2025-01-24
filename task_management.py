import streamlit as st
import requests

# Configurações da API
API_URL = "http://127.0.0.1:8000"

# Função para autenticação
def get_token():
    response = requests.post(f"{API_URL}/token", json={"username": "admin", "password": "admin"})
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        st.error("Erro ao autenticar. Verifique as credenciais.")
        return None

# Obter token de autenticação
token = get_token()

if token:
    headers = {"Authorization": f"Bearer {token}"}

    st.title("Gerenciamento de Tarefas")

    # Aba de navegação
    menu = ["Criar Tarefa", "Visualizar Tarefas", "Atualizar Tarefa", "Deletar Tarefa"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Criar Tarefa":
        st.subheader("Criar Nova Tarefa")
        title = st.text_input("Título")
        description = st.text_area("Descrição")
        status = st.selectbox("Status", ["pending", "in_progress", "completed"])
        due_date = st.date_input("Data de Vencimento")

        if st.button("Criar Tarefa"):
            data = {
                "title": title,
                "description": description,
                "status": status,
                "due_date": str(due_date)
            }
            response = requests.post(f"{API_URL}/tasks", json=data, headers=headers)
            if response.status_code == 200:
                st.success("Tarefa criada com sucesso!")
            else:
                st.error("Erro ao criar a tarefa.")

    elif choice == "Visualizar Tarefas":
        st.subheader("Lista de Tarefas")
        response = requests.get(f"{API_URL}/tasks", headers=headers)
        if response.status_code == 200:
            tasks = response.json()
            for task in tasks:
                st.write(f"**Título:** {task['title']}")
                st.write(f"Descrição: {task['description']}")
                st.write(f"Status: {task['status']}")
                st.write(f"Data de Vencimento: {task['due_date']}")
                st.write("---")
        else:
            st.error("Erro ao carregar as tarefas.")

    elif choice == "Atualizar Tarefa":
        st.subheader("Atualizar Tarefa")
        task_id = st.number_input("ID da Tarefa", step=1, min_value=1)
        title = st.text_input("Novo Título")
        description = st.text_area("Nova Descrição")
        status = st.selectbox("Novo Status", ["pending", "in_progress", "completed"])
        due_date = st.date_input("Nova Data de Vencimento")

        if st.button("Atualizar Tarefa"):
            data = {
                "title": title,
                "description": description,
                "status": status,
                "due_date": str(due_date)
            }
            response = requests.put(f"{API_URL}/tasks/{task_id}", json=data, headers=headers)
            if response.status_code == 200:
                st.success("Tarefa atualizada com sucesso!")
            else:
                st.error("Erro ao atualizar a tarefa.")

    elif choice == "Deletar Tarefa":
        st.subheader("Deletar Tarefa")
        task_id = st.number_input("ID da Tarefa", step=1, min_value=1)

        if st.button("Deletar Tarefa"):
            response = requests.delete(f"{API_URL}/tasks/{task_id}", headers=headers)
            if response.status_code == 200:
                st.success("Tarefa deletada com sucesso!")
            else:
                st.error("Erro ao deletar a tarefa.")
