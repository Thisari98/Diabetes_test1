# -*- coding: utf-8 -*-
"""
Created on Sun Mar 20 16:52:26 2022

@author: Thisu
"""



import streamlit as st
import joblib
import pyrebase
#from pyrebase import pyrebase
from datetime import datetime

#configuration key
firebaseConfig = {
  'apiKey': "AIzaSyCkvgBeGi3fTQ6WBmI_Oema4E-AblXbQX0",
  'authDomain': "drbigbot-f0e94.firebaseapp.com",
  'projectId': "drbigbot-f0e94",
  'databaseURL':"https://drbigbot-f0e94-default-rtdb.europe-west1.firebasedatabase.app/",
  'storageBucket': "drbigbot-f0e94.appspot.com",
  'messagingSenderId': "577415504336",
  'appId': "1:577415504336:web:e3480f5c66346c8e2359d5",
  'measurementId': "G-4JLDK9H86L"
};
#Firebase Authentication
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

#Database
db = firebase.database()
storage = firebase.storage()


# Authentication

choice = st.sidebar.selectbox('Login/Signup', ['Login', 'Sign Up'])

email = st.sidebar.text_input('Please input your email')
password = st.sidebar.text_input('Please enter your password', type = 'password')



# Sign up Block

if choice == 'Sign Up':
    handle = st.sidebar.text_input('Please input your app handle name', value= 'Default')
    submit = st.sidebar.button('Create my account')
    
    if submit:
        user = auth.create_user_with_email_and_password(email, password)
        st.success('Your account is created sucsessfully')
        st.balloons()
        #sign in
        user = auth.sign_in_with_email_and_password(email, password)
        db.child(user['localId']).child("Handle").set(handle)
        db.child(user['localId']).child("ID").set(user['localId'])
        st.title('Welcome ' + handle)
        st.info('login via login drop down selection')

# Login Block
        
if choice == 'Login':
    login = st.sidebar.checkbox('Login')
    if login:
        user = auth.sign_in_with_email_and_password(email, password)
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
        
        bio = st.radio('Jump to', ['Home', 'Recomandation', 'Settings'])
        
        

exp1 = st.expander('Input/Change Bio details')
with exp1:   

        p1 = st.slider('Enter Your Age',18,100)
        
        p2 = st.number_input("Enter your Blood Sugar Fast(mmol/L):")
    
        p3 = st.number_input("Enter your BS pp(mmol/L):")
        
        p4 = st.number_input("Enter your Plasma R(mmol/L):")
    
        p5 = st.number_input("Enter your Plasma F(mmol/L):")
    
        p6 = st.number_input("Enter your HbA1c(mmol/mol):")
    
        save_bio = st.button('Save')
    
        #send user static bio to DataBase
        if save_bio:
            age = db.child(user['localId']).child("p1").push(p1)
            bs_fast = db.child(user['localId']).child("p2").push(p2)
            bs_pp = db.child(user['localId']).child("p3").push(p3)
            plasma_r = db.child(user['localId']).child("p4").push(p4)
            plasma_f = db.child(user['localId']).child("p5").push(p5)
            hb1ac = db.child(user['localId']).child("p6").push(p6)
                        
                # load the model
model = joblib.load('Diabetes_Type_model')
                
if st.button('Predict'):
                    
                   #calling db user bio data 
                   
    db_age = db.child(user['localId']).child("p1").get().val()         
    if db_age is not None:
        val = db.child(user['localId']).child("p1").get()
        for child_val in val.each():
            p1_get = child_val.val()   
    else:
        st.info("Error!")
 
    db_bs_fast = db.child(user['localId']).child("p2").get().val()
    if db_bs_fast is not None:
           val = db.child(user['localId']).child("p2").get()
           for child_val in val.each():
               p2_get = child_val.val()
    else:
        st.info("Error!")
                
    db_bs_pp = db.child(user['localId']).child("p3").get().val()
    if db_bs_pp is not None:
          val = db.child(user['localId']).child("p3").get()
          for child_val in val.each():
              p3_get = child_val.val()
    else:
         st.info("Error!")
                   
    db_plasma_r = db.child(user['localId']).child("p4").get().val()
    if db_plasma_r is not None:
          val = db.child(user['localId']).child("p4").get()
          for child_val in val.each():
              p4_get = child_val.val()
    else:
          st.info("Error!")
                       
    db_plasma_f = db.child(user['localId']).child("p5").get().val()
    if db_plasma_f is not None:
         val = db.child(user['localId']).child("p5").get()
         for child_val in val.each():
             p5_get = child_val.val()
    else:
         st.info("Error!")
                   
    db_hb1ac = db.child(user['localId']).child("p6").get().val()
    if db_hb1ac is not None:
        val = db.child(user['localId']).child("p6").get()
        for child_val in val.each():
            p6_get = child_val.val()
    else:
         st.info("Error!")
                   
                   
                   
    #run Diabetes type model
    prediction = model.predict([[p1_get,p2_get,p3_get,p4_get,p5_get,p6_get]])
                   
    st.success('Your Diabetes Type is: {} '.format(prediction[0]))

    