import PIL
import streamlit as st
import models as md
import os

class LeadDetailsPage:

    # Main function to display lead details
    def render(self):
        st.title('All Leads')
        st.button("Go Home", on_click=self.go_home)
        st.button("Enter Client Details", on_click=self.go_to_client_details)

        # Fetch all customers
        customers = self.get_all_customers()

        # Display customer details
        if customers:
            for customer in customers:
                st.subheader(f'Lead ID: {customer.id}')
                st.write(f'Name: {customer.name}')
                st.write(f'Phone: {customer.phone}')
                st.write(f'Company Name: {customer.company_name}')
                st.write(f'Email: {customer.email}')
                st.write(f'Remarks:')
                self.display_remarks(customer.remarks)  # Display remarks with new lines
                st.write(f'Product Request:')
                self.display_product_request(customer.product_request)  # Display product request with new lines

                # Display pictures if available
                if customer.picture:
                    picture_paths = customer.picture.split('\n')  # Split by newline to handle multiple paths
                    for picture_path in picture_paths:
                        try:
                            if os.path.exists(picture_path):
                                PIL.Image.open(picture_path)  # Attempt to open the image
                                st.image(picture_path, caption='Customer Picture', use_column_width=True)
                            else:
                                st.write(f'Error: Image file not found at path: {picture_path}')
                        except PIL.UnidentifiedImageError as e:
                            st.write(f'Error: Unable to identify image file at path: {picture_path}')
                st.write('---')  # Separator between leads

    def get_all_customers(self):
        return md.session.query(md.Customer).all()

    def go_home(self):
        st.session_state['page'] = 'home'

    def go_to_client_details(self):
        st.session_state['page'] = 'client_details'

    def display_remarks(self, remarks):
        # Display remarks with new lines
        remarks_lines = remarks.split('\n')
        for line in remarks_lines:
            st.write(line)

    def display_product_request(self, product_request):
        # Display product request with new lines
        product_request_lines = product_request.split('\n')
        for line in product_request_lines:
            st.write(line)
