
import streamlit as st
import pandas as pd
import joblib
import sklearn
import category_encoders
from datetime import datetime, time

model = joblib.load('model.pkl')
features = joblib.load('features.pkl')

def make_prediction(airline,source,destination,duration,total_stops,month,day,dep_hour,dep_minute,arrival_hour,arrival_minute):
    df_pred = pd.DataFrame(columns=features)
    df_pred.at[0,'airline'] = airline
    df_pred.at[0,'destination'] = destination
    df_pred.at[0,'duration'] = duration
    df_pred.at[0,'total_stops'] = total_stops
    df_pred.at[0,'month'] = month
    df_pred.at[0,'day'] = day
    df_pred.at[0,'dep_hour'] = dep_hour
    df_pred.at[0,'dep_minute'] = dep_minute
    df_pred.at[0,'arrival_hour'] = arrival_hour
    df_pred.at[0,'arrival_minute'] = arrival_minute
    result = model.predict(df_pred)
    return result[0]


    
def main():
    st.title('India Airline Ticket Price prediction')
    # Departure Date input
    dep_date = st.date_input("Select Departure date", datetime.today())
    # Departure Time input
    dep_time = st.time_input("Select Departure time", time())
    selected_dep_datetime = datetime.combine(dep_date, dep_time)
    # Display the selected departure datetime
    st.write("Selected Departure DateTime:", selected_dep_datetime)
    month = int(pd.to_datetime(selected_dep_datetime, format="%Y-%m-%dt%H:%M").month)
    day = int(pd.to_datetime(selected_dep_datetime, format="%Y-%m-%dt%H:%M").day)
    dep_hour = int(pd.to_datetime(selected_dep_datetime, format="%Y-%m-%dt%H:%M").hour)
    dep_minute = int(pd.to_datetime(selected_dep_datetime, format="%Y-%m-%dt%H:%M").minute)
    
    # Arrivale Date input
    Arrivale_date = st.date_input("Select Arrivale date", datetime.today())
    # Arrivale Time input
    Arrivale_time = st.time_input("Select Arrivale time", time())
    selected_Arrivale_datetime = datetime.combine(Arrivale_date, Arrivale_time)
    # Display the selected Arrivale datetime
    st.write("Selected Arrivale DateTime:", selected_Arrivale_datetime)
    arrival_hour = int(pd.to_datetime(selected_Arrivale_datetime, format="%Y-%m-%dt%H:%M").hour)
    arrival_minute = int(pd.to_datetime(selected_Arrivale_datetime, format="%Y-%m-%dt%H:%M").minute)
    
    # Calculate the duration
    total_duration = selected_Arrivale_datetime - selected_dep_datetime
    # Convert the duration to minutes
    duration = total_duration.total_seconds() / 60
    st.write("Trip Duration in minutes:", duration)
    
    airline = st.selectbox("airline company",['Air India', 'IndiGo', 'SpiceJet', 'Multiple carriers',
       'Jet Airways', 'GoAir', 'Vistara', 'Air Asia', 'other'])
    source = st.selectbox('Source City',['Kolkata', 'Banglore', 'Delhi', 'Chennai', 'Mumbai'])
    destination = st.selectbox('Destination City',['Banglore', 'Delhi', 'Cochin', 'Kolkata', 'Hyderabad'])
    total_stops = st.selectbox('Select Trip total stops (0 for dirct or non stop flight)',[0, 1, 2, 3])
    
    if st.button("Predict"):
        result = make_prediction(airline,source,destination,duration,total_stops,month,day,dep_hour,dep_minute,arrival_hour,arrival_minute)
        st.write("Ticket price in Indina Rubee '₹''")
        st.text(result)
        
main()
