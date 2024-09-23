import streamlit as st
from home_page import HomePage
from catalogue_page import CataloguePage
from client_details_page import ClientDetailsPage
from product_selection_page import ProductSelectionPage
from lead_details_page import LeadDetailsPage
import os

st.set_page_config(page_title="Inter Clean Data Collection", layout="wide")
# Path to the image files
image_path1 = os.path.join("designImage", "cappahlogo.png")
image_path2 = os.path.join("designImage", "greenway.jpg")

# Check if the image files exist
if os.path.exists(image_path1) and os.path.exists(image_path2):
    # Display images side by side with a little gap between them
    col1, col2 = st.columns(2)
    with col1:
        st.image(image_path1, width=350)
    with col2:
        st.image(image_path2, width=350)
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












