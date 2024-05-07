import streamlit as st
from PIL import Image as PILImage

def load_images():
    """ Load images from the database """
    return session.query(Image).all()

def add_customer(name, phone, company_name, email):
    """ Add a customer to the database """
    customer = Customer(name=name, phone=phone, company_name=company_name, email=email)
    session.add(customer)
    session.commit()
    return customer.id

def add_transaction(customer_id, image_id):
    """ Add a transaction linking a customer and an image """
    transaction = Transaction(customer_id=customer_id, image_id=image_id)
    session.add(transaction)
    session.commit()

def main():
    st.title("Customer Catalogue Form")

    # Display images as a catalogue
    st.header("Product Catalogue")
    images = load_images()
    for img in images:
        st.image(PILImage.open(img.path), caption=img.name, width=300)

    # Customer form
    st.header("Customer Details")
    with st.form(key='customer_form'):
        name = st.text_input("Name")
        phone = st.text_input("Phone")
        company_name = st.text_input("Company Name")
        email = st.text_input("Email")
        selected_image_id = st.selectbox("Select Product", [img.id for img in images], format_func=lambda x: session.query(Image).get(x).name)
        submit_button = st.form_submit_button("Submit")

        if submit_button:
            customer_id = add_customer(name, phone, company_name, email)
            add_transaction(customer_id, selected_image_id)
            st.success("Customer and transaction added successfully!")

if __name__ == "__main__":
    main()
