import streamlit as st
from models import Product, Session


class CataloguePage:
    def __init__(self):
        # Define the fixed height for the images and expander
        self.image_height = 150
        self.text_height = 250  # You might need to adjust this
        self.expander_height = 300  # You might need to adjust this

    def render(self):
        st.header("Product Catalogue")
        # Navigation buttons
        st.button("Go Home", on_click=self.go_home)
        st.button("Enter Client Details", on_click=self.go_to_client_details)

        search_query = st.text_input("Search for a product")

        session = Session()
        if search_query:
            products = session.query(Product).filter(Product.name.contains(search_query)).all()
        else:
            products = session.query(Product).all()

        columns_per_row = 3
        rows = [products[i:i + columns_per_row] for i in range(0, len(products), columns_per_row)]

        for row in rows:
            cols = st.columns(columns_per_row)
            for col, product in zip(cols, row):
                with col:
                    if product:
                        st.image(product.image, width=self.image_height)
                        st.write(f"{product.name[:self.text_height]}")
                        with st.expander("Read more"):
                            st.write(product.description[:self.expander_height])
        session.close()

    def go_home(self):
        st.session_state['page'] = 'home'

    def go_to_client_details(self):
        st.session_state['page'] = 'client_details'
