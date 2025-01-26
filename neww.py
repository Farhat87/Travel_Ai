import streamlit as st
import openai
import os
from dotenv import load_dotenv


load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=prompt,
            temperature=0.7,
            max_tokens=1000
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Error: {e}"

#System Prompt to Understand User Context
system_prompt = {
    "role": "system",
    "content": "You are an AI travel planner that creates highly personalized travel itineraries. Ask for the user's details to generate a travel plan that matches their preferences."
}

# Step 2: Streamlit UI for user input
st.title("Your Travel Planner")
st.write("Plan your perfect trip with our AI-powered itinerary generator.")

# Collect user inputs
with st.form("user_preferences_form"):
    destination = st.text_input("Enter your destination:")
    trip_duration = st.number_input("Enter trip duration (in days):", min_value=1, step=1)
    budget = st.selectbox("Select your budget range:", ["Low", "Moderate", "Luxury"])
    purpose = st.text_area("What is the purpose of your trip (e.g., relaxation, adventure, cultural exploration, etc.)?")
    preferences = st.text_area("Describe your preferences (e.g., food, activities, nature, etc.):")
    dietary_preferences = st.text_area("Any dietary preferences or restrictions?")
    accommodation = st.selectbox("Preferred accommodation type:", ["Luxury", "Budget", "Central location"])
    mobility = st.selectbox("Walking tolerance:", ["Low", "Moderate", "High"])
    submit = st.form_submit_button("Generate Itinerary")

if submit:
    user_prompt = [
        system_prompt,
        {
            "role": "user",
            "content": (
                f"I am planning a trip to {destination} for {trip_duration} days. "
                f"My budget is {budget}. The purpose of my trip is {purpose}. "
                f"I enjoy {preferences}. My dietary preferences are {dietary_preferences}. "
                f"I prefer {accommodation} accommodation and have a {mobility} walking tolerance."
            )
        }
    ]

    with st.spinner("Generating your personalized itinerary..."):
        itinerary = generate_response(user_prompt)
    if itinerary:
        st.subheader("Your Personalized Travel Itinerary:")
        st.write(itinerary)
    else:
        st.error("Something went wrong. Please try again.")

# Hosting instructions
st.sidebar.title("Hosting Instructions")
st.sidebar.info("To test this application live, deploy it using Streamlit Cloud or another free hosting provider.")
st.sidebar.markdown("1. Set up your `.env` file with your API key.\n"
                   "2. Run the script using `streamlit run script_name.py`.\n"
                   "3. Test and share the link to your hosted application.")
