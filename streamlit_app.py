import streamlit as st
from typing import List

# Shared state for the game
@st.cache_resource
def get_game_state():
    return {
        "player_inputs": [],  # Store player numbers here
        "mean_guesses": [],  # Store player guesses for the mean
        "round_active": False,  # Track if a round is currently active
        "round_result": None,  # Store the result of the round
        "submitted_players": set(),  # Track players who have submitted their entries
    }

# Initialize the shared game state
game_state = get_game_state()

# Admin access control
admin_access = st.text_input("Enter 'ADMIN' to access admin console:")
if admin_access == "ADMIN":
    # Admin area
    st.sidebar.header("Admin Area")
    if st.sidebar.button("Start New Round"):
        game_state["player_inputs"] = []
        game_state["mean_guesses"] = []
        game_state["round_active"] = True
        game_state["round_result"] = None
        game_state["submitted_players"] = set()
        st.sidebar.success("New round started!")

    if st.sidebar.button("End Current Round"):
        if game_state["round_active"]:
            game_state["round_active"] = False
            if len(game_state["player_inputs"]) > 0:
                actual_mean = sum(game_state["player_inputs"]) / len(game_state["player_inputs"])
                closest_guess = min(
                    game_state["mean_guesses"], key=lambda x: abs(x["guess"] - actual_mean)
                )
                game_state["round_result"] = {
                    "actual_mean": actual_mean,
                    "closest_player": closest_guess["player"],
                    "closest_guess": closest_guess["guess"]
                }
                st.sidebar.success(f"Round ended! Closest guess: Player {closest_guess['player']} with guess {closest_guess['guess']:.2f}. Actual mean: {actual_mean:.2f}")
            else:
                st.sidebar.warning("No player inputs were provided for this round.")
                game_state["round_result"] = None
        else:
            st.sidebar.warning("No round is currently active.")

# Player area
@st.fragment(run_every=2)
def display_player_area():
    if game_state["round_result"] is None:
        st.header("Player Area")
    if game_state["round_active"]:
        player_name = st.text_input("Enter your name:")
        if player_name in game_state["submitted_players"]:
            st.info("Your entry has been submitted! Please wait for the round to end ..")
            st.markdown("<div class='spinner'></div>", unsafe_allow_html=True)
        else:
            player_number = st.number_input("Enter a number between 1 and 100:", min_value=1, max_value=100, step=1)
            mean_guess = st.number_input("Guess the mean of all players' numbers (between 1 and 100):", min_value=1.0, max_value=100.0, step=0.01)

            if st.button("Submit Entry"):
                if player_name:
                    game_state["player_inputs"].append(player_number)
                    game_state["mean_guesses"].append({"player": player_name, "guess": mean_guess})
                    game_state["submitted_players"].add(player_name)
                    st.rerun()
                else:
                    st.error("Please enter your name before submitting.")
    elif game_state["round_result"] is None:
        st.warning("No active round. Please wait for the admin to start a new round.")
display_player_area()

# Display end game state if available
@st.fragment(run_every=2)
def display_result():
    if game_state["round_result"] is not None:
        st.header("Round Result")
        st.write(f"Actual mean: {game_state['round_result']['actual_mean']:.2f}")
        st.write(f"Closest guess: Player {game_state['round_result']['closest_player']} with guess {game_state['round_result']['closest_guess']:.2f}")
display_result()

# Display current game state (for debugging purposes or transparency)
#st.header("Current Game State")
#st.write(game_state)