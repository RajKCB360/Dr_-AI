# File: wellness_ai_advisor.py
from dotenv import load_dotenv
import os
import streamlit as st
import google.generativeai as genai
from PIL import Image

# Load environment variables
load_dotenv()

# Configure the GenAI library with the API key
genai.configure(api_key=os.getenv("AIzaSyDMTOih2NfhCloOXGE4IzPBn9rcw4cyrno"))

# Function to load Google Gemini Pro Vision API and get a response
def get_gemini_response(input_text, image_data):
    model = genai.GenerativeModel("gemini-pro-vision")
    response = model.generative_content([input_text, image_data[0]])
    return response.text

# Function to process the uploaded image
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the MIME type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file was uploaded.")

# Initialize Streamlit app
st.set_page_config(page_title="WellnessAI Advisor")
st.header("WellnessAI Advisor: Let's Ask Me")

# File uploader widget
uploaded_file = st.file_uploader("Choose an Image ..", type=['jpg', 'jpeg', 'png'])

# Display uploaded image
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)

# Submit button
submit = st.button("Tell me about my meal")

# Input prompt for the Generative AI model
input_prompt = '''
You are an expert nutritionist. Analyze the food items from the image and calculate total calories.
Provide details for each food item in the following format:
1. Item 1 - [calories]
2. Item 2 - [calories]
3. Item 3 - [calories]
...
After listing, mention if the meal is healthy or not and provide the percentage ratio split of
carbohydrates, protein, fats, sugar, and calories. Suggest which items to remove/add to make
the meal healthier if it's unhealthy.
'''

# If submit is clicked
if submit:
    try:
        image_data = input_image_setup(uploaded_file)
        response = get_gemini_response(input_prompt, image_data)
        st.subheader("The Response is:")
        st.write(response)
    except Exception as e:
        st.error(f"An error occurred: {e}")