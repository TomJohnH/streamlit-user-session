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
        if (datetime.now() - last_activity).total_seconds() < 10:  # 1-hour timeout
            return True
    return False

def mark_session_as_expired(username):
    session_store = get_active_sessions()
    if username in session_store:
        session_store[username]['expired'] = True

def has_session_expired(username):
    session_store = get_active_sessions()
    session = session_store.get(username)
    if session:
        return session.get('expired', False)
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
        session_store[username] = {
            'session_id': session_id,
            'last_activity': datetime.now(),
            'expired': False
        }
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
        mark_session_as_expired(username)
    # Manually clear the session state
    st.session_state['logged_in'] = False
    st.session_state['username'] = None
    st.session_state['session_id'] = None
    get_session_store.clear()
    st.success("Logged out successfully!")
    st.rerun()

def main():
    st.title("Session Management Example")

    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if st.session_state['logged_in'] and is_session_active(st.session_state['username'],st.session_state['session_id']):
        st.write(has_session_expired(st.session_state['username']))
        st.write(f"Welcome {st.session_state['username']}!")
        
        if st.button("Logout"):
            logout()
        if 'counter' not in st.session_state:
            st.session_state['counter'] = 0
        if st.button("Click me"):
            st.session_state['counter']=st.session_state['counter']+1
            st.write(str(st.session_state['counter']))
            #update_last_activity(st.session_state['username'])
            session_store = get_active_sessions()
            session_id = session_store.get(st.session_state['username'], {}).get('session_id')
            st.write(session_store)
            st.write(st.session_state)

    else:
        username = st.text_input("Username", key="username_input")
        password = st.text_input("Password", type="password", key="password_input")
        if st.button("Login"):
            session_store = get_active_sessions()
            session_id = session_store.get(username, {}).get('session_id')
            st.write(session_store)
            st.write(st.session_state)
            if session_id and (is_session_active(username, session_id)): #or not has_session_expired(username)):
                st.warning("Another session is active. Please logout from other session first.")
            else:
                login(username, password)

if __name__ == "__main__":
    main()
