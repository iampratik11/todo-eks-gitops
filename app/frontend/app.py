import os
import requests
import streamlit as st


API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(
    page_title="TaskFlow",
    page_icon="✓",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --------------------------------------------------
# Professional light theme
# --------------------------------------------------
st.markdown(
    """
    <style>
    /* Main page */
    .stApp {
        background-color: #f8fafc;
    }

    .main .block-container {
        max-width: 1050px;
        padding-top: 2.5rem;
        padding-bottom: 3rem;
    }

    /* Hide Streamlit branding */
    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        visibility: hidden;
    }

    /* Header */
    .app-header {
        margin-bottom: 2rem;
    }

    .app-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #111827;
        margin-bottom: 0.25rem;
    }

    .app-subtitle {
        color: #6b7280;
        font-size: 1rem;
    }

    /* Statistics */
    .stat-card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 1.25rem;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03);
    }

    .stat-label {
        color: #6b7280;
        font-size: 0.85rem;
        margin-bottom: 0.35rem;
    }

    .stat-number {
        color: #111827;
        font-size: 1.8rem;
        font-weight: 700;
    }

    /* Section headings */
    .section-heading {
        color: #111827;
        font-size: 1.15rem;
        font-weight: 600;
        margin-top: 2rem;
        margin-bottom: 0.8rem;
    }

    /* Input */
    div[data-testid="stTextInput"] input {
        background: white;
        color: #111827;
        border: 1px solid #d1d5db;
        border-radius: 8px;
        min-height: 42px;
    }

    div[data-testid="stTextInput"] input:focus {
        border-color: #2563eb;
        box-shadow: 0 0 0 1px #2563eb;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 8px;
        border: 1px solid #d1d5db;
        background: white;
        color: #374151;
        font-weight: 500;
        min-height: 40px;
    }

    .stButton > button:hover {
        border-color: #2563eb;
        color: #2563eb;
    }

    /* Form submit button */
    .stFormSubmitButton > button {
        background: #2563eb;
        color: white;
        border: 1px solid #2563eb;
        border-radius: 8px;
        font-weight: 600;
        min-height: 42px;
    }

    .stFormSubmitButton > button:hover {
        background: #1d4ed8;
        border-color: #1d4ed8;
        color: white;
    }

    /* Task card */
    .task-card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.7rem;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.02);
    }

    .task-title {
        color: #111827;
        font-size: 1rem;
        font-weight: 500;
        margin-bottom: 0.3rem;
    }

    .task-status {
        color: #6b7280;
        font-size: 0.8rem;
    }

    /* Empty state */
    .empty-state {
        background: white;
        border: 1px dashed #d1d5db;
        border-radius: 12px;
        padding: 3rem;
        text-align: center;
    }

    .empty-title {
        color: #374151;
        font-size: 1.1rem;
        font-weight: 600;
    }

    .empty-text {
        color: #9ca3af;
        margin-top: 0.4rem;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #9ca3af;
        font-size: 0.8rem;
        margin-top: 3rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# API functions
# --------------------------------------------------
def get_todos():
    response = requests.get(
        f"{API_URL}/todos",
        timeout=10,
    )
    response.raise_for_status()
    return response.json()


def create_todo(title):
    response = requests.post(
        f"{API_URL}/todos",
        json={"title": title},
        timeout=10,
    )
    response.raise_for_status()
    return response.json()


def delete_todo(todo_id):
    response = requests.delete(
        f"{API_URL}/todos/{todo_id}",
        timeout=10,
    )
    response.raise_for_status()


# --------------------------------------------------
# Header
# --------------------------------------------------
st.markdown(
    """
    <div class="app-header">
        <div class="app-title">TaskFlow</div>
        <div class="app-subtitle">
            A simple and focused way to manage your daily tasks.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# Get todos
# --------------------------------------------------
try:
    todos = get_todos()

except requests.exceptions.RequestException:
    st.error(
        f"Unable to connect to the backend at `{API_URL}`."
    )
    st.stop()


total = len(todos)
completed = sum(
    1 for todo in todos if todo["completed"]
)
pending = total - completed


# --------------------------------------------------
# Dashboard statistics
# --------------------------------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        f"""
        <div class="stat-card">
            <div class="stat-label">Total tasks</div>
            <div class="stat-number">{total}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        f"""
        <div class="stat-card">
            <div class="stat-label">Pending</div>
            <div class="stat-number">{pending}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        f"""
        <div class="stat-card">
            <div class="stat-label">Completed</div>
            <div class="stat-number">{completed}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# --------------------------------------------------
# Add task
# --------------------------------------------------
st.markdown(
    '<div class="section-heading">Add a task</div>',
    unsafe_allow_html=True,
)

with st.form(
    "add_todo_form",
    clear_on_submit=True,
):
    col1, col2 = st.columns([5, 1])

    with col1:
        title = st.text_input(
            "Task",
            placeholder="e.g. Review AWS architecture",
            label_visibility="collapsed",
        )

    with col2:
        submitted = st.form_submit_button(
            "Add task",
            use_container_width=True,
        )

    if submitted:
        if not title.strip():
            st.warning("Please enter a task.")

        else:
            try:
                create_todo(title.strip())
                st.success("Task added.")
                st.rerun()

            except requests.exceptions.RequestException:
                st.error("Unable to create task.")


# --------------------------------------------------
# Task list
# --------------------------------------------------
st.markdown(
    '<div class="section-heading">Tasks</div>',
    unsafe_allow_html=True,
)

if not todos:

    st.markdown(
        """
        <div class="empty-state">
            <div class="empty-title">No tasks yet</div>
            <div class="empty-text">
                Add your first task above to get started.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

else:

    for todo in todos:

        col1, col2 = st.columns(
            [6, 1],
            vertical_alignment="center",
        )

        with col1:

            if todo["completed"]:
                status_icon = "✓"
                status_text = "Completed"
            else:
                status_icon = "○"
                status_text = "Pending"

            st.markdown(
                f"""
                <div class="task-card">
                    <div class="task-title">
                        {status_icon}&nbsp;&nbsp;{todo["title"]}
                    </div>
                    <div class="task-status">
                        {status_text}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col2:

            if st.button(
                "Delete",
                key=f"delete_{todo['id']}",
                use_container_width=True,
            ):
                try:
                    delete_todo(todo["id"])
                    st.rerun()

                except requests.exceptions.RequestException:
                    st.error("Unable to delete task.")


# --------------------------------------------------
# Footer
# --------------------------------------------------
st.markdown(
    """
    <div class="footer">
        TaskFlow · Python · Streamlit · FastAPI · AWS
    </div>
    """,
    unsafe_allow_html=True,
)
