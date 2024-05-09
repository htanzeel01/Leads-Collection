import streamlit as st
import models as md

class ProductSelectionPage:

    def __init__(self):
        # Define the fixed height for the images and expander
        self.image_height = 150
        self.text_height = 250  # You might need to adjust this
        self.expander_height = 300  # You might need to adjust this

    def render(self):
        st.header("Select Products")
        # Navigation buttons
        if st.button("Go Home", on_click=self.go_home):
            st.experimental_rerun()
        if st.button("Enter Client Details", on_click=self.go_to_client_details):
            st.experimental_rerun()

        search_query = st.text_input("Search for a product")

        session = md.Session()
        if search_query:
            filtered_products = session.query(md.Product).filter(md.Product.name.contains(search_query)).all()
        else:
            filtered_products = session.query(md.Product).all()

        columns_per_row = 3
        rows = [filtered_products[i:i + columns_per_row] for i in range(0, len(filtered_products), columns_per_row)]

        for row in rows:
            cols = st.columns(columns_per_row)
            for col, product in zip(cols, row):
                with col:
                    if product:
                        with st.container():
                            st.image(product.image, width=self.image_height)
                            st.caption(product.name[:self.text_height])
                            with st.expander("Read more"):
                                st.write(product.description[:self.expander_height])
                            if st.button("Select", key=f"select-{product.id}"):
                                self.select_product(product.id)
        session.close()

    def select_product(self, product_id):
        if 'selected_products' not in st.session_state:
            st.session_state['selected_products'] = []
        if product_id not in st.session_state['selected_products']:
            st.session_state['selected_products'].append(product_id)
            st.success(f"Product {product_id} selected!")

    def go_home(self):
        st.session_state['page'] = 'home'

    def go_to_client_details(self):
        st.session_state['page'] = 'client_details'
