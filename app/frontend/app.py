import os
import requests
import streamlit as st


API_URL = os.getenv("API_URL", "http://localhost:8000")


st.set_page_config(
    page_title="Todo App",
    page_icon="✅",
    layout="centered"
)

st.title("✅ Todo Application")
st.write("Python Streamlit Frontend")


def get_todos():
    response = requests.get(f"{API_URL}/todos")
    response.raise_for_status()
    return response.json()


def create_todo(title):
    response = requests.post(
        f"{API_URL}/todos",
        json={"title": title}
    )
    response.raise_for_status()
    return response.json()


def delete_todo(todo_id):
    response = requests.delete(
        f"{API_URL}/todos/{todo_id}"
    )
    response.raise_for_status()


st.subheader("Add Todo")

title = st.text_input(
    "Todo title",
    placeholder="Enter a task..."
)

if st.button("Add Todo"):
    if title.strip():
        create_todo(title.strip())
        st.success("Todo added!")
        st.rerun()
    else:
        st.warning("Please enter a todo.")


st.subheader("Todo List")

try:
    todos = get_todos()

    if not todos:
        st.info("No todos yet.")

    for todo in todos:
        col1, col2 = st.columns([4, 1])

        with col1:
            status = "✅" if todo["completed"] else "⬜"
            st.write(f"{status} {todo['title']}")

        with col2:
            if st.button("Delete", key=f"delete_{todo['id']}"):
                delete_todo(todo["id"])
                st.rerun()

except requests.exceptions.RequestException:
    st.error(
        f"Cannot connect to backend at {API_URL}"
    )
