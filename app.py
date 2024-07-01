# Import necessary libraries
import streamlit as st
from dotenv import load_dotenv, find_dotenv
import os
import google.generativeai as genai
from PIL import Image

# Load environment variables from the .env file
load_dotenv(find_dotenv())

# Configure Streamlit page settings
st.set_page_config(page_title="Generative Geek's Nutrition Monitor", page_icon="🔮")

# Configure Google Generative AI library with an API key from environment variables
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Apply custom CSS to enhance the Streamlit app's appearance
st.markdown("""
    <style>
    .stApp {
        background-color: #f5f5f5;        # Light grey background for the app
        font-family: Arial, sans-serif;   # Arial font for a clean look
    }
    .stButton>button {
        background-color: #4CAF50;       # Green background for buttons
        color: white;                    # White text for buttons
        font-size: 16px;                 # Larger text for better readability
    }
    .stHeader {
        font-size: 24px;                 # Large font size for headers
        font-weight: bold;               # Bold font weight for headers
    }
    </style>
    """, unsafe_allow_html=True)  # Enable HTML within markdown for custom styles

# Define a function to handle the response from Google Gemini API
def get_gemini_response(input, image):
    # Initialize the Gemini model
    model = genai.GenerativeModel("gemini-1.5-pro-latest")
    # Send input and image data to the model and get textual response
    response = model.generate_content([input, image[0]])
    return response.text

# Define a function to set up image uploading and handle the image data
def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file content
        bytes_data = uploaded_file.getvalue()
        # Create a dictionary to hold image data including MIME type and raw data
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data,
            }
        ]
        return image_parts
    else:
        # Raise an error if no image is uploaded
        raise FileNotFoundError("No image uploaded")

# Sidebar configuration for navigation and file upload
st.sidebar.title("Navigation")
st.sidebar.header("Upload Section")
uploaded_file = st.sidebar.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# Display the main header of the application
st.header("Generative Geek's Nutrition Monitor")
# Check if an image is uploaded and display it
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

# Create a button for triggering the food analysis
submit = st.button("Analyse this Food")
# Set the prompt for the AI model
input_prompt = """
You are an expert nutritionist analyzing the food items in the image.
Start by determining if the image contains food items. 
If the image does not contain any food items, 
clearly state "No food items detected in the image." 
and do not provide any calorie information. 
If food items are detected, 
start by naming the meal based on the image, 
identify and list every ingredient you can find in the image, 
and then estimate the total calories for each ingredient. 
Summarize the total calories based on the identified ingredients. 
Follow the format below:

If no food items are detected:
No food items detected in the image.

If food items are detected:
Meal Name: [Name of the meal]

1. Ingredient 1 - estimated calories
2. Ingredient 2 - estimated calories
----
Total estimated calories: X

Finally, mention whether the food is healthy or not, 
and provide the percentage split of protein, carbs, and fats in the food item. 
Also, mention the total fiber content in the food item and any other important details.

Note: Always identify ingredients and provide an estimated calorie count, 
even if some details are uncertain.
"""

# Action to take when the 'Analyse this Food' button is clicked
if submit:
    with st.spinner("Processing..."):  # Show a processing spinner while processing
        # Prepare the image data
        image_data = input_image_setup(uploaded_file)
        # Get the response from the AI model
        response = get_gemini_response(input_prompt, image_data)
    # Indicate processing is complete
    st.success("Done!")
    # Display the subheader and the response from the AI model
    st.subheader("Food Analysis")
    st.write(response)