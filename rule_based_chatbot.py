import streamlit as st
from streamlit_chat import message
import time

import json
from streamlit_lottie import st_lottie


def load_lottie_animation(file_path):
    with open(file_path, "r") as f:
        return json.load(f)
    
animation1 = load_lottie_animation("assets/quic_rail.json")


stations = ["Banglore", "Delhi", "Mumbai", "Chennai", "Hyderabad", "Kolkata"]

prices = {
    # Fares from Banglore to other city station
    ("Banglore", "Delhi"): 20,
    ("Banglore", "Mumbai"): 30,
    ("Banglore", "Chennai"): 40,
    ("Banglore", "Hyderabad"): 25,
    ("Banglore", "Kolkata"): 35,
    
    # Fares from Delhi to other city station
    ("Delhi", "Banglore"): 20,
    ("Delhi", "Mumbai"): 30,
    ("Delhi", "Chennai"): 40,
    ("Delhi", "Hyderabad"): 25,
    ("Delhi", "Kolkata"): 35,

    # Fares from Mumbai to other city station
    ("Mumbai", "Banglore"): 30,
    ("Mumbai", "Delhi"): 30,
    ("Mumbai", "Chennai"): 40,
    ("Mumbai", "Hyderabad"): 25,
    ("Mumbai", "Kolkata"): 35,

    # Fares from Chennai to other city station
    ("Chennai", "Banglore"): 40,
    ("Chennai", "Delhi"): 40,
    ("Chennai", "Mumbai"): 40,
    ("Chennai", "Hyderabad"): 25,
    ("Chennai", "Kolkata"): 35,

    # Fares from Hyderabad to other city station
    ("Hyderabad", "Banglore"): 25,
    ("Hyderabad", "Delhi"): 25,
    ("Hyderabad", "Mumbai"): 25,
    ("Hyderabad", "Chennai"): 25,
    ("Hyderabad", "Kolkata"): 35,

    # Fares from Kolkata to other city station
    ("Kolkata", "Banglore"): 35,
    ("Kolkata", "Delhi"): 35,
    ("Kolkata", "Mumbai"): 35,
    ("Kolkata", "Chennai"): 35,
    ("Kolkata", "Hyderabad"): 35,
}



def calculate_price(from_station, to_station, passengers):
    return prices.get((from_station, to_station), 50) * passengers


# Streamlit normally reset everything each time the user interacts (e.g. when you click a  button).
# Session state solves this problem by allowing it to remember data between user interactions.
#Helpful in cases where any intermediate results has to be carried out without recalculating.

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'num_passengers' not in st.session_state:
    st.session_state.num_passengers = None
if 'from_station' not in st.session_state:
    st.session_state.from_station = None
if 'to_station' not in st.session_state:
    st.session_state.to_station = None
if 'show_thank_you' not in st.session_state:
    st.session_state.show_thank_you = False
if 'start_time' not in st.session_state:
    st.session_state.start_time = None


def app():

    col01, col02 = st.columns([1, 0.4])
    with col01:
        st.title("QuickRail - Train Ticket Booking Chatbot")
        st.write(":orange[Tired of long queues for train tickets?] Don't worry, that's a thing of the past!  \nBook tickets instantly from anywhere. Just chat, choose your destination, pay, and enjoy a hassle-free booking experience.")
        st.markdown("---")
    with col02:
        st_lottie(animation1, height=210, key="animation1")
    
    

    col11, col22 = st.columns([1, 0.5])
    
    with col11:
        # Step 0: Initial state, displaying the "Book your Tickets Now" button
        if st.session_state.step == 0:
            if st.button("Book your Tickets Now"):
                # Add the first chatbot message to prompt for the number of passengers
                st.session_state.messages.append({"content": "Hello! How many passengers are traveling? ", "is_user": False})
                # Move to the next step
                st.session_state.step = 1
                st.experimental_rerun()

        # Display previous messages from the chatbot and user
        for msg in st.session_state.messages:
            role = "assistant" if not msg["is_user"] else "user"
            avatar_image = "train.png" if role == "assistant" else "user.jpg"
            col1, col2 = st.columns([2, 4]) if role == "assistant" else st.columns([4, 2])  # Adjust alignment
            
            with col1 if role == "assistant" else col2:
                with st.chat_message(role, avatar=avatar_image):
                    st.write(msg["content"] + (" 🚆" if role == "assistant" else " ✅"))

        # Step 1: Ask for the number of passengers
        if st.session_state.step == 1:
            col1, col2 = st.columns([2, 1])  
            with col2:
                # Dropdown to select the number of passengers (1-5)
                user_input = st.selectbox("Number of passengers:", list(range(1, 6)))
                if st.button("Submit"):
                    # Save the number of passengers to session state
                    st.session_state.num_passengers = user_input
                    # Add user's selection to the chat history
                    st.session_state.messages.append({"content": f"{user_input}", "is_user": True})
                    # Prompt the user for the departure station
                    st.session_state.messages.append({"content": "Please select your departure station.", "is_user": False})
                    st.session_state.step = 2
                    st.experimental_rerun()

        # Step 2: Ask for the departure station
        elif st.session_state.step == 2:
            col1, col2 = st.columns([2, 1])
            with col2:
                # Dropdown to select the departure station
                user_input = st.selectbox("Departure station:", stations)
                if st.button("Submit"):
                    # Save the departure station to session state
                    st.session_state.from_station = user_input
                    # Add user's selection to the chat history
                    st.session_state.messages.append({"content": user_input, "is_user": True})
                    # Prompt the user for the destination station
                    st.session_state.messages.append({"content": "Please select your destination station.", "is_user": False})
                    st.session_state.step = 3
                    st.experimental_rerun()

        # Step 3: Ask for the destination station
        elif st.session_state.step == 3:
            col1, col2 = st.columns([2, 1])
            with col2:
                # Dropdown to select the destination station
                user_input = st.selectbox("Destination station:", stations)
                # Validate if the source and destination are the same
                if st.session_state.from_station == user_input:
                    st.error("Departure and destination stations cannot be the same!")
                else:
                    if st.button("Submit"):
                        # Save the destination station to session state
                        st.session_state.to_station = user_input
                        # Add user's selection to the chat history
                        st.session_state.messages.append({"content": user_input, "is_user": True})
                        # Calculate the total price based on inputs
                        ticket_price = calculate_price(st.session_state.from_station, st.session_state.to_station, st.session_state.num_passengers)
                        # Add the price information to the chat history
                        st.session_state.messages.append({"content": f"Your total price for {st.session_state.num_passengers} passenger(s) from {st.session_state.from_station} to {st.session_state.to_station} is ₹{ticket_price}.", "is_user": False})
                        st.session_state.step = 4
                        st.experimental_rerun()

        # Step 4: Display the payment option
        if st.session_state.step == 4:
            col1, col2 = st.columns([2, 1])
            with col2:
                if st.button("Make Payment"):
                    # Display a QR code for payment
                    st.image('payment.jpg')  # Example QR code image
                    time.sleep(40)
                    st.session_state.show_thank_you = True
                    st.experimental_rerun()

        if st.session_state.show_thank_you:
            col1, col2 = st.columns([2, 1])  
            with col2:
                if st.button("Thank You"):
                    # Reset session state when Thank You button is clicked
                    st.session_state.messages = []
                    st.session_state.step = 0
                    st.session_state.num_passengers = None
                    st.session_state.from_station = None
                    st.session_state.to_station = None
                    st.session_state.start_time = None
                    st.session_state.show_thank_you = False  # Hide the Thank You button again
                    st.experimental_rerun()

    with col22:
        with st.form('Question2'):
            st.write("  - :orange[About this Chatbot]")
            st.write("This chatbot follows a rule-based approach to guide users through ticket booking. It provides predefined responses based on user inputs. Errors like selecting the same departure and destination are flagged. The chatbot is structured, interactive, and calculates ticket prices dynamically.")
            if st.form_submit_button("Hope it helped"):
                st.write("Feel free to customise and use it. Push any improvements to the repo!")
                linkedin_url = "https://www.linkedin.com/in/deekshith2912/"
                linkedin_link = f"[Deekshith B]({linkedin_url})"
                st.markdown(f"###### Developed by {linkedin_link}")

        

    

if __name__ == "__main__":
    app()

