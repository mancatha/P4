import streamlit as st 
import pandas as pd
import joblib
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import warnings
import os 
warnings.filterwarnings("ignore", category=UserWarning, message="Trying to unpickle estimator")
#variables and constants
DIRPATH = os.path.dirname(os.path.realpath(__file__))
ml_core_fp = os.path.join(DIRPATH, "export", "ml.joblib")

#useful functions
st.cache_resource()
def  load_ml_components(fp):
    "load the ml components to re-use in app"
    with open(fp, 'rb') as file:
        obj = joblib.load(file)
        return obj
# execution    
ml_components_dict = load_ml_components(fp = ml_core_fp)

# Specify the path to your saved model
rf_model_filename = 'sales_dt_model.joblib'
sales_rf_path = os.path.join(DIRPATH, rf_model_filename)
# Specify the file path where the model is saved


# Load the model
model = ml_components_dict["models"]


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
        date = left_col.date_input("Select a Date")
          # Extract day, month, and year from the selected date
        selected_date = pd.to_datetime(date)
        day = selected_date.day
        month = selected_date.month
        year = selected_date.year

        # Format the extracted values as strings
        day_str = str(day)
        month_str = str(month)
        year_str = str(year)
        store_nbr = left_col.number_input("Enter store number")
        product = left_col.selectbox("Enter your product name:",['LADIESWEAR', 'DAIRY', 'CLEANING', 'EGGS' ,'PET SUPPLIES' ,'AUTOMOTIVE',
                                    'HOME AND KITCHEN I' ,'BREAD/BAKERY' ,'MEATS' ,'PREPARED FOODS', 'BOOKS',
                                    'MAGAZINES', 'HOME APPLIANCES' ,'FROZEN FOODS' ,'LAWN AND GARDEN'
                                    'BABY CARE', 'HOME AND KITCHEN II', 'HOME CARE' ,'HARDWARE' ,'GROCERY I',
                                    'DELI' ,'SCHOOL AND OFFICE SUPPLIES' ,'PRODUCE' ,'LINGERIE',
                                    'LIQUOR,WINE,BEER' ,'SEAFOOD', 'PERSONAL CARE', 'GROCERY II', 'CELEBRATION',
                                    'BEVERAGES', 'BEAUTY', 'PLAYERS AND ELECTRONICS' ,'POULTRY'])
        onpromotion = left_col.number_input("Enter the onpromotion price")
        
        
        # set the right column 
      
        
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
        "store_nbr": [store_nbr],
        "cluster": [cluster],
        "product": [product],
        "state": [state],
        "stores_type": [stores_type],
        "onpromotion": [onpromotion],
        "oil_prices": [oil_prices],
        "city": [city],
        "year": [year],  # Set default year value
        "month": [month],  # Use the extracted month
        "day": [day],  # Use the extracted day
        }
        
    

        # Display input data as a dataframe
        input_data = pd.DataFrame.from_dict(input_dict)
        
        # Encode the categorical using one hot encoder
        # Specify the categorical columns to one-hot encode
        train_columns = ['product', 'city', 'state', 'stores_type']

        # Perform one-hot encoding
        encoded_input_data = pd.get_dummies(input_data, columns=train_columns)

        # Get a list of columns that were not one-hot encoded
        remaining_columns = [col for col in input_data.columns if col not in train_columns]

        # Add the remaining columns to the encoded_train DataFrame
        for col in remaining_columns:
            encoded_input_data[col] = input_data[col]

        
        
        # Make predictions
          #Make the prediction
        model_output = model.predict(input_data)   # Use the same encoded_input_data as in your code

        # Display the prediction
        st.write("Predicted Sales:", model_output)
        
        