import os
import smtplib
import ssl
import uuid
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import streamlit as st
from streamlit_webrtc import webrtc_streamer
import models as md

class ClientDetailsPage:
    def render(self):
        st.header("Client Details")
        if st.button("Go Home", on_click=self.go_home):
            st.session_state.page = ""
            st.experimental_rerun()
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
            st.experimental_rerun()

        # Create a form for client details
        with st.form(key='client_details'):
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

            #button check for dcs lead
            dcs_checked = st.checkbox('DCS')

            # Submit button for the client details form
            submit_client_details = st.form_submit_button("Submit Client Details")

            if submit_client_details:
                # If the form is submitted, save the client details
                self.save_client_details(session, name, phone, company_name, email, remarks, product_request,
                                         uploaded_files, dcs_checked)
                st.success("Client details saved!")

            session.close()

    def save_client_details(self, session, name, phone, company_name, email,remarks,product_request, uploaded_files,dcs_checked):
        # This method saves client details to the database
        upload_dir = "uploaded_image"

        # Create the directory if it doesn't exist
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
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
            if (dcs_checked):
                # Modify remarks to add a new line and 'Lead for DCS'
                remarks += "\nLead for DCS"
                new_client = md.Customer(name=name, phone=phone, company_name=company_name, email=email,
                                         remarks=remarks,
                                         product_request=product_request, picture=picture)
                session.add(new_client)
                session.commit()
                self.send_email_dcs(name, phone, company_name, email, remarks, product_request, file_paths)
            else:
                # Create a new client object with the file paths
                new_client = md.Customer(name=name, phone=phone, company_name=company_name, email=email, remarks=remarks,
                                     product_request=product_request, picture=picture)
                session.add(new_client)
                session.commit()
                self.send_email(name, phone, company_name, email, remarks, product_request, file_paths)
        except Exception as e:
            st.error(f"An error occurred while saving client details: {e}")
            session.rollback()
        finally:
            # It's important to close the session here if you are not using it further
            session.close()

    def send_email(self, name, phone, company_name, email, remarks, product_request, file_paths):
        # Compose the email
        msg = MIMEMultipart()
        msg['From'] = 'cappahexhibit@zohomail.eu'  # Your Zoho email address
        msg['To'] = 'rabeet@cappah.com'  # Recipient email address
        msg['Subject'] = 'New Client Details'

        # Add text content to the email
        email_body = f"""
        New Client Details:
        Name: {name}
        Phone: {phone}
        Company Name: {company_name}
        Email: {email}
        Remarks: {remarks}
        Product Request: {product_request}
        """
        msg.attach(MIMEText(email_body, 'plain'))

        # Attach uploaded files to the email
        for file_path in file_paths:
            with open(file_path, 'rb') as f:
                attachment = MIMEImage(f.read(), name=os.path.basename(file_path))
            msg.attach(attachment)

        # Send the email via Zoho SMTP
        smtp_server = 'smtp.zoho.eu'  # Zoho SMTP server
        port = 465  # SSL port
        sender_email = 'cappahexhibit@zohomail.eu'  # Sender email address (Zoho)
        password = 'ttgg.mC6rHD98uH'  # Use your Zoho password or app-specific password here

        context = ssl.create_default_context()

        try:
            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, msg['To'], msg.as_string())
            st.success("Email sent successfully!")
        except Exception as e:
            st.error(f"An error occurred while sending the email: {e}")

    def send_email_dcs(self, name, phone, company_name, email, remarks, product_request, file_paths):
        # Compose the email
        msg = MIMEMultipart()
        msg['From'] = 'cappahexhibit@zohomail.eu'  # Your Zoho email address
        msg['To'] = 'htanzeel04@gmail.com'  # DCS recipient email address
        msg['Subject'] = 'New Client Details'

        # Add text content to the email
        email_body = f"""
        New Client Details:
        Name: {name}
        Phone: {phone}
        Company Name: {company_name}
        Email: {email}
        Remarks: {remarks}
        Product Request: {product_request}
        """
        msg.attach(MIMEText(email_body, 'plain'))

        # Attach uploaded files to the email
        for file_path in file_paths:
            with open(file_path, 'rb') as f:
                attachment = MIMEImage(f.read(), name=os.path.basename(file_path))
            msg.attach(attachment)

        # Send the email via Zoho SMTP
        smtp_server = 'smtp.zoho.eu'  # Zoho SMTP server
        port = 465  # SSL port
        sender_email = 'cappahexhibit@zohomail.eu'  # Sender email address (Zoho)
        password = 'ttgg.mC6rHD98uH'  # Use your Zoho password or app-specific password here

        context = ssl.create_default_context()

        try:
            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, msg['To'], msg.as_string())
            st.success("Email sent successfully!")
        except Exception as e:
            st.error(f"An error occurred while sending the email: {e}")

    def go_home(self):
        st.session_state['page'] = 'home'
