import streamlit as st
import os

class HomePage:
    def render(self):
        st.title('Inter Clean Data Collection')
        col1, col2,col3 = st.columns(3)

        with col1:
            if st.button('Browse Catalogue'):
                st.session_state['page'] = 'catalogue'

        with col2:
            if st.button('Enter Client Details'):
                st.session_state['page'] = 'client_details'

        with col3:
            if st.button('View Lead Details'):
                st.session_state['page'] = 'view_leads'

