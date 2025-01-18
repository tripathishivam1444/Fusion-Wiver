import streamlit as st
import requests
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

col1, col2, col3 = st.columns([1, 1, 0.9])

with col1:
    st.title("")

with col2:
    st.title("")

with col3:
    st.image("fusion.png")




def make_api_request(mobile_string, discount_percent):
    headers = {
        "api-key": os.getenv("API_KEY"),
        "Content-Type": "application/json"
    }
    
    payload = {
        "mobileString": mobile_string,
        "discountPercent": discount_percent
    }
    
    response = requests.post(
        url=os.getenv("API_URL"),
        headers=headers,
        json=payload
    )
    return response

def main():
    st.title("Poketly Late Fee Waiver Discount API Interface")

    with st.form("discount_form"):
        mobile = st.text_input("Mobile Number", max_chars=10)
        discount = st.number_input("Discount Percentage", min_value=0, max_value=100, value=100)
        
        # Submit button
        submitted = st.form_submit_button("Apply Discount")
        
        if submitted:
            if not mobile or len(mobile) != 10:
                st.error("Please enter a valid 10-digit mobile number")
                return
                
            try:
                response = make_api_request(mobile, discount)
                
                if response.status_code == 200:
                    result = response.json()
                    if result.get("success"):
                        st.success(result["payload"]["message"])
                    else:
                        st.error("API request failed")
                else:
                    st.error(f"Error: {response.status_code}")
                    st.error(response.text)
                    
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
