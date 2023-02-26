#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import pandas as pd
import numpy as np
import os
from Page.SARIMA import*
import random
import PIL
from PIL import Image
import time
from Page.Preprocessing import *
from Page.EDA import *
import requests

# Define the path to your image
def overview():
    import streamlit as st

    st.write("Welcome to Energy Consumption Forecasting app!",style={"font-size": "100px"})
    img_url  = "https://astanatimes.com/wp-content/uploads/2022/10/BEST-WAYS-TO-MINIMIZE-ENERGY-CONSUMPTION-AT-HOME-796x448.jpg"
    response = requests.get(img_url)

    image = Image.open(BytesIO(response.content))

    st.image(image)


def save_uploadedfile(uploadedfile):
    st.session_state['key'] = random.randint(0,99999)
    with open(os.path.join("temp"+str(st.session_state['key'])+".csv"),"wb") as f:
        f.write(uploadedfile.getbuffer())
    return st.success("Saved File:{}".format(uploadedfile.name))

def main_page2():
    st.markdown("## Data Upload")
    func_check()


def page2():
    st.markdown("## Cleaning & Pre-processing")
    if "key" in st.session_state:
        if os.path.isfile("temp"+str(st.session_state['key'])+".csv"):
            if os.path.isfile("temp_cleaned"+str(st.session_state['key'])+".csv"):
                data = pd.read_csv("temp_cleaned"+str(st.session_state['key'])+".csv",encoding='cp1252')
                st.write(data)
            else:
                data = pd.read_csv("temp"+str(st.session_state['key'])+".csv",encoding='cp1252')
                Preprocessing(data)
        else:
            st.write("Please upload data to proceed further")
    else:
        st.write("Please upload data to proceed further")

def page3():
    st.markdown("## EDA")
    if "key" in st.session_state:
        if os.path.isfile("temp"+str(st.session_state['key'])+".csv"):
            if os.path.isfile("temp_cleaned"+str(st.session_state['key'])+".csv"):
                data = pd.read_csv("temp_cleaned"+str(st.session_state['key'])+".csv",encoding='cp1252')
                st.write(data)
            else:
                data = pd.read_csv("temp"+str(st.session_state['key'])+".csv",encoding='cp1252')
                EDA(data)
        else:
            st.write("Please upload data to proceed further")
    else:
        st.write("Please upload data to proceed further")
        


def page4():
    st.markdown("## SARIMA")
    if "key" in st.session_state:
        if os.path.isfile("temp"+str(st.session_state['key'])+".csv"):
            if os.path.isfile("temp_cleaned"+str(st.session_state['key'])+".csv"):
                data = pd.read_csv("temp_cleaned"+str(st.session_state['key'])+".csv",encoding='cp1252')
                st.write(data)
            else:
                data = pd.read_csv("temp"+str(st.session_state['key'])+".csv",encoding='cp1252')
                SARIMA(data,30)
        else:
            st.write("Please upload data to proceed further")
    else:
        st.write("Please upload data to proceed further")
        


        
page_names_to_funcs = {
    "overview":overview,
    "Upload": main_page2,
    "Pre-processing": page2,
    "EDA":page3,
    "SARIMA":page4
}

def func_check():
    
    
    st.write('')
    with open('Total_consumption_coal_Alaska_all_commercial_(total)_monthly.csv', 'rb') as f:
        st.download_button(
         label="Download data for this app",
         data = f,
         file_name='Total_consumption_coal_Alaska_all_commercial_(total)_monthly.csv',
         mime='text/csv')
    
    uploaded_file = st.file_uploader("Choose a file",type=["csv"])
    
    if uploaded_file is not None:
         # To read file as bytes:
         try:
             data = pd.read_csv(uploaded_file,encoding='cp1252')
         except Exception as e:
             st.write("Error",e)
         finally:
             save_uploadedfile(uploaded_file)
             st.dataframe(data)
    else:
        if "key" in st.session_state:
            if os.path.isfile("temp"+str(st.session_state['key'])+".csv"):
                os.remove("temp"+str(st.session_state['key'])+".csv")
            if os.path.isfile("temp_cleaned"+str(st.session_state['key'])+".csv"):
                os.remove("temp_cleaned"+str(st.session_state['key'])+".csv")
    
    
  
def main():
    selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
    with st.spinner('Wait for it...'):
        time.sleep(0.5)
        page_names_to_funcs[selected_page]()
        
if __name__ == '__main__':
    main()

