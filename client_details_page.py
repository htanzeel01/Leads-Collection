import os
import uuid

import streamlit as st
from streamlit_webrtc import webrtc_streamer
import models as md

class ClientDetailsPage:
    def render(self):
        st.header("Client Details")
        st.button("Go Home", on_click=self.go_home)
        prodName = ""

        # Start a session to query the database
        session = md.Session()
        categories = session.query(md.Category).all()
        category_options = {category.id: category.name for category in categories}
        # Button to navigate to product selection
        # This button is not part of the form
        if st.button("Select Products"):
            #st.session_state['selected_category_id'] = selected_category_id
            st.session_state['page'] = 'select_products'

        # Create a form for client details
        with st.form(key='client_details'):
            selected_category_id = st.selectbox(
                "Select Category",
                list(category_options.keys()),
                format_func=lambda x: category_options[x]
            )

            # Retrieve previously selected products if any
            selected_products = st.session_state.get('selected_products', [])

            # Display selected products
            if selected_products:
                st.write("Selected Products:")
                for product_id in selected_products:
                    product = session.query(md.Product).get(product_id)
                    st.write(f"- {product.name}")
                    prodName += f"{product.name}\n"

            # Client detail input fields
            name = st.text_input("Name")
            phone = st.text_input("Phone")
            company_name = st.text_input("Company Name")
            email = st.text_input("Email")
            remarks = st.text_area("Remarks")
            product_request = prodName

            # File upload
            uploaded_files = st.file_uploader("Upload Files", accept_multiple_files=True)

            # Webcam capture
            webrtc_streamer(key="example", video_transformer_factory=None, async_transform=False)

            # Submit button for the client details form
            submit_client_details = st.form_submit_button("Submit Client Details")

            if submit_client_details:
                # If the form is submitted, save the client details
                self.save_client_details(session, name, phone, company_name, email,remarks,product_request, uploaded_files)
                st.success("Client details saved!")

        # Close the session after operations
        session.close()

    def save_client_details(self, session, name, phone, company_name, email,remarks,product_request, uploaded_files):
        # This method saves client details to the database
        upload_dir = "uploaded_image"
        try:
            # Save uploaded files to disk and get their file paths
            file_paths = []
            for uploaded_file in uploaded_files:
                file_data = uploaded_file.read()
                # Generate a unique filename using UUID
                unique_filename = str(uuid.uuid4()) + os.path.splitext(uploaded_file.name)[-1]
                # Construct the file path
                file_path = os.path.join(upload_dir, unique_filename)
                # Write the file data to the specified location
                with open(file_path, "wb") as f:
                    f.write(file_data)
                file_paths.append(file_path)

            # Convert the list of file paths to a single string
            # Use a delimiter if you want to separate multiple file paths
            picture = "\n".join(file_paths)

            # Create a new client object with the file paths
            new_client = md.Customer(name=name, phone=phone, company_name=company_name, email=email, remarks=remarks,
                                     product_request=product_request, picture=picture)
            session.add(new_client)
            session.commit()
        except Exception as e:
            st.error(f"An error occurred while saving client details: {e}")
            session.rollback()
        finally:
            # It's important to close the session here if you are not using it further
            session.close()
    def go_home(self):
        st.session_state['page'] = 'home'