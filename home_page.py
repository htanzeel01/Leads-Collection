import streamlit as st
from matplotlib.dates import DateFormatter

import models as md
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import numpy as np
class HomePage:
    def render(self):
        st.title('Inter Clean Data Collection')
        col1, col2,col3 = st.columns(3)

        with col1:
            if st.button('Browse Catalogue'):
                st.session_state['page'] = 'catalogue'
                st.experimental_rerun()

        with col2:
            if st.button('Enter Client Details'):
                st.session_state['page'] = 'client_details'
                st.experimental_rerun()

        with col3:
            if st.button('View Lead Details'):
                st.session_state['page'] = 'view_leads'
                st.experimental_rerun()

        if st.button('View Data Analysis'):
            self.createPlot()
            self.leadTimeplot()
            self.product_request_visualization()

    def createPlot(self):
        # Fetch data from the database
        # Query the database for customer data
        session = md.Session()
        customers = session.query(md.Customer).all()
        session.close()
        #Plot leads captured by Day
        # Create DataFrame
        df = pd.DataFrame([(c.created_at.date(), 1) for c in customers], columns=['Date', 'Leads'])
        df['Date'] = pd.to_datetime(df['Date'])  # Convert 'Date' column to datetime type
        df['Date'] = df['Date'].dt.date  # Extract date part only
        # Aggregate by date
        df = df.groupby('Date').sum().reset_index()
        # Plot
        st.subheader('Leads Captured per Day')
        fig = px.bar(df, x='Date', y='Leads', title='Leads Captured per Day')
        fig.update_xaxes(type='category')  # Ensure date is treated as categorical
        st.plotly_chart(fig)

    def createheatmap(self):
        # Plot Leads Captured by Time
        session = md.Session()
        customers = session.query(md.Customer).all()
        session.close()

        # Extract time from datetime objects
        df = pd.DataFrame([(c.created_at) for c in customers], columns=['created_at'])

        # Convert created_at column to datetime format
        df['created_at'] = pd.to_datetime(df['created_at'])

        # Group by time and count the number of leads
        time_leads = df.groupby(df['created_at'].dt.hour).size().reset_index(name='Leads')

        # Plot
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.stripplot(x='created_at', y='Leads', data=time_leads, color='blue', ax=ax, jitter=True)

        # Format plot
        plt.title('Leads Captured by Time')
        plt.xlabel('Hour of the Day')
        plt.ylabel('Number of Leads')
        plt.xticks(range(24), range(24))  # Set x-axis ticks to hours of the day
        plt.yticks(range(time_leads['Leads'].max() + 1))  # Set y-axis ticks to whole numbers of leads

        plt.tight_layout()

        st.pyplot(fig)

    def leadTimeplot(self):
        # Plot Leads Captured by Time
        session = md.Session()
        customers = session.query(md.Customer).all()
        session.close()
        st.set_option('deprecation.showPyplotGlobalUse', False)

        # Extract time from datetime objects and convert to string
        data = [(str(c.created_at.time()), 1) for c in customers]
        df = pd.DataFrame(data, columns=['Time', 'Leads'])

        # Convert 'Time' column to datetime
        df['Time'] = pd.to_datetime(df['Time'])

        # Add random noise to the x-axis values
        noise = np.random.uniform(-0.2, 0.2, size=len(df))
        df['Time'] += pd.to_timedelta(noise, unit='m')

        # Group by time and count the number of leads
        time_leads = df.groupby(df['Time'].dt.hour).size().reset_index(name='Leads')

        # Plot
        plt.figure(figsize=(10, 6))
        sns.scatterplot(data=time_leads, x='Time', y='Leads', color='blue', alpha=0.5)

        # Format plot
        plt.title('Leads Captured by Time')
        plt.xlabel('Hour of the Day')
        plt.ylabel('Number of Leads')

        # Customize x-axis ticks to show hours
        plt.xticks(range(24), [f'{hour}:00' for hour in range(24)], rotation=45, ha='right')

        # Set y-axis limits to start from 1
        plt.ylim(1, max(time_leads['Leads']) + 1)

        plt.tight_layout()

        st.pyplot()

    def product_request_visualization(self):
        # Fetch data from the database
        session = md.Session()
        customers = session.query(md.Customer).all()

        # Process data
        product_counts = {}
        for customer in customers:
            requests = customer.product_request.split('\n')  # Assuming requests are separated by new lines
            for request in requests:
                product_counts[request] = product_counts.get(request, 0) + 1
        product_df = pd.DataFrame(product_counts.items(), columns=['Product', 'Count'])
        product_df = product_df.sort_values(by='Count', ascending=False)

        # Visualize
        st.title('Product Request Visualization')
        st.subheader('Most Requested Products')
        st.bar_chart(product_df.set_index('Product'))












