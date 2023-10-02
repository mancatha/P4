import streamlit as st 
import pandas as pd
import pickle
import numpy as np
from sklearn.ensemble import RandomForestRegressor 
import warnings
warnings.filterwarnings("ignore", category=UserWarning, message="Trying to unpickle estimator")

# Specify the file path where the model is saved
# Load the model from the saved file
model_filename = "C:/Users/manca/OneDrive/Desktop/P41/P4/sales_pred_model.pkl" # Specify the correct file path
with open(model_filename, 'rb') as model_file:
    model = pickle.load(model_file)

# Set the page title and add some style
st.set_page_config(
    page_title="Retail Store Sales ",
    page_icon="💰",
    layout="wide",  # Adjust layout to wide
)
# Title and description
st.write("# Retail Store Sales ")
st.write("Impact sales of a retail store.")
prediction = st.container()

# set up the sidebar
st.sidebar.header("Data Dictionary")
#st.sidebar.twxt()
st.sidebar.markdown("""
                    We will paste the data dictionary here later
                    """)
# Define the form 
form = st.form(key = "Information", clear_on_submit=True)

# create a key list 
expected_input= ["store_nbr", "product", "sales", "onpromotion", "oil_prices", "city", "state", "stores_type", "cluster", "Year", "Month", "Day"]
numerics= ["sales","oil_prices","onpromotion"]
categories= ["store_nbr","product","city","state","stores_type","cluster"]

# set up the prediction section 
with prediction:
    prediction.subheader("Inputs")
    prediction.write("This section will recieve inputs")
    left_col,right_col = prediction.columns(2)
    
    #set up the form 
    with form:
        left_col.write("Inputs part 1:")
        date = st.date_input("Select a Date")
        store_nbr = left_col.number_input("Enter store number")
        product = left_col.selectbox("Enter your product name:",['LADIESWEAR', 'DAIRY', 'CLEANING', 'EGGS' ,'PET SUPPLIES' ,'AUTOMOTIVE',
                                    'HOME AND KITCHEN I' ,'BREAD/BAKERY' ,'MEATS' ,'PREPARED FOODS', 'BOOKS',
                                    'MAGAZINES', 'HOME APPLIANCES' ,'FROZEN FOODS' ,'LAWN AND GARDEN'
                                    'BABY CARE', 'HOME AND KITCHEN II', 'HOME CARE' ,'HARDWARE' ,'GROCERY I',
                                    'DELI' ,'SCHOOL AND OFFICE SUPPLIES' ,'PRODUCE' ,'LINGERIE',
                                    'LIQUOR,WINE,BEER' ,'SEAFOOD', 'PERSONAL CARE', 'GROCERY II', 'CELEBRATION',
                                    'BEVERAGES', 'BEAUTY', 'PLAYERS AND ELECTRONICS' ,'POULTRY'])
        sales = left_col.number_input("Enter amount of sales")
        onpromotion = left_col.number_input("Enter the onpromotion price")
        
        
        # set the right column 
        right_col.write("Inputs part 2:")
        
        oil_prices = right_col.number_input("Enter the current oil prices")
        
        city = right_col.selectbox("Enter your city:",['Quito', 'Loja', 'Manta', 'Guaranda' ,'Playas', 'Daule' ,'Latacunga',
                                    'Guayaquil', 'Babahoyo', 'Santo Domingo', 'Riobamba', 'Ibarra', 'Ambato',
                                    'Cuenca' ,'El Carmen', 'Puyo', 'Libertad' ,'Machala', 'Quevedo' ,'Cayambe',
                                    'Salinas', 'Esmeraldas'])
        state = right_col.selectbox("Enter your state:",['Pichincha', 'Loja' ,'Manabi', 'Bolivar', 'Guayas', 'Cotopaxi', 'Los Rios',
                                    'Santo Domingo de los Tsachilas', 'Chimborazo', 'Imbabura', 'Tungurahua',
                                    'Azuay', 'Pastaza', 'El Oro', 'Santa Elena', 'Esmeraldas'])
        stores_type = right_col.selectbox("Enter the store type:",['A', 'D', 'C' ,'B' ,'E'])
        cluster = right_col.slider("Enter the cluster", min_value=1, value= 1)
        
        # create a submitted button
        submitted = form.form_submit_button("Submit")


# Dataframe creation
if submitted:
    with prediction:
        #formate input 
        input_dict  ={
        "Store Number": [store_nbr],
            "Cluster Number": [cluster],
            "Product": [product],
            "State": [state],
            "Store Type": [stores_type],
            "Date": [date],
            "Amount": [sales],
            "onpromotion": [onpromotion],
            "oil_prices": [oil_prices],
            "city": [city],
        }
    

        # Display input data as a dataframe
        input_data = pd.DataFrame.from_dict(input_dict)
        
        # Encode the categorical using one hot encoder
   

    # Perform your prediction or analysis here if needed

