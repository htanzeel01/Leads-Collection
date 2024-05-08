import streamlit as st
from home_page import HomePage
from catalogue_page import CataloguePage
from client_details_page import ClientDetailsPage
from product_selection_page import ProductSelectionPage
from lead_details_page import LeadDetailsPage
import os

st.set_page_config(page_title="Inter Clean Data Collection", layout="wide")
# Path to the image file
image_path = os.path.join("designImage", "cappahlogo.png")

# Check if the image file exists
if os.path.exists(image_path):
    # Display the image
    st.image(image_path, width=350)
PAGES = {
    "home": HomePage,
    "catalogue": CataloguePage,
    "client_details": ClientDetailsPage,
    "select_products": ProductSelectionPage,
    "view_leads": LeadDetailsPage
}


def main():
    # Initialize the page key if it doesn't exist
    if 'page' not in st.session_state:
        st.session_state['page'] = 'home'

    # Instantiate and render the current page class
    page_class = PAGES[st.session_state['page']]
    page = page_class()
    page.render()



if __name__ == "__main__":
    main()












