#
#
#   This version has a slight issue that after timout one user can have 2 sessions opened
#
#

import streamlit as st
from uuid import uuid4
from datetime import datetime, timedelta

@st.cache_resource
def get_session_store():
    return {}

def get_active_sessions():
    return get_session_store()

def is_session_active(username, session_id):
    session_store = get_active_sessions()
    session = session_store.get(username)
    if session and session['session_id'] == session_id:
        last_activity = session['last_activity']
        if (datetime.now() - last_activity).total_seconds() < 3600:  # 1-hour timeout
            return True
    return False

def update_last_activity(username):
    session_store = get_active_sessions()
    if username in session_store:
        session_store[username]['last_activity'] = datetime.now()

def login(username, password):
    # Dummy authentication check
    if username == "user" and password == "pass":
        session_id = str(uuid4())
        session_store = get_active_sessions()
        session_store[username] = {'session_id': session_id, 'last_activity': datetime.now()}
        st.session_state['logged_in'] = True
        st.session_state['username'] = username
        st.session_state['session_id'] = session_id
        st.success("Logged in successfully!")
        st.rerun()
    else:
        st.error("Invalid username or password")

def logout():
    username = st.session_state.get('username')
    if username:
        session_store = get_active_sessions()
        if username in session_store:
            del session_store[username]
    st.session_state.clear()
    st.success("Logged out successfully!")

def main():
    st.title("Session Management Example")
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if st.session_state['logged_in']:
        st.write(f"Welcome {st.session_state['username']}!")
        update_last_activity(st.session_state['username'])
        if 'counter' not in st.session_state:
            st.session_state['counter'] = 0
        if st.button("Click me"):
            st.session_state['counter']=st.session_state['counter']+1
            st.write(str(st.session_state['counter']))
        if st.button("Logout"):
            logout()
    else:
        username = st.text_input("Username", key="username_input")
        password = st.text_input("Password", type="password", key="password_input")
        if st.button("Login"):     
            session_store = get_active_sessions()
            session_id = session_store.get(username, {}).get('session_id')
            if session_id and is_session_active(username, session_id):
                st.warning("Another session is active. Please logout from other session first.")
                st.caption("Debug:")
                st.caption(session_store.get(username))
            else:
                login(username, password)

if __name__ == "__main__":
    main()

