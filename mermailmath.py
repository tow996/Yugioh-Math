import random
from collections import Counter

def create_deck(card_definitions):
    """
    Creates a deck of cards based on a dictionary of card names and their counts.

    Args:
        card_definitions (dict): A dictionary where keys are card names (str)
                                 and values are their respective counts (int) in the deck.
                                 Example: {"Dormouse": 2, "FieldSpell": 2, "DummyCard": 20}

    Returns:
        list: A shuffled list representing the deck of cards.
    """
    if not isinstance(card_definitions, dict) or not card_definitions:
        raise ValueError("card_definitions must be a non-empty dictionary.")

    deck = []
    for card_name, count in card_definitions.items():
        if not isinstance(card_name, str) or not card_name:
            raise ValueError(f"Card name must be a non-empty string. Found: {card_name}")
        if not isinstance(count, int) or count <= 0:
            raise ValueError(f"Card count for '{card_name}' must be a positive integer. Found: {count}")
        deck.extend([card_name] * count)
    random.shuffle(deck)
    return deck

def open_cards(deck, num_cards_to_open):
    """
    Simulates opening a specified number of cards from a deck.

    Args:
        deck (list): The deck of cards to draw from. This list will be modified (cards removed).
        num_cards_to_open (int): The number of cards to open.

    Returns:
        list: A list of cards that were opened.
    """
    if num_cards_to_open < 0:
        raise ValueError("num_cards_to_open cannot be negative.")

    opened_cards = []
    for _ in range(num_cards_to_open):
        if deck: # Ensure deck is not empty before popping
            opened_cards.append(deck.pop(0)) # Pop from the beginning to simulate drawing
        else:
            # print("Deck is empty. No more cards to open.") # Suppress this print for cleaner simulation output
            break
    return opened_cards

def check_for_combination(opened_cards, combination):
    """
    Checks if a specific combination of cards is present in the opened cards.
    This accounts for multiple instances of the same card in the combination.

    Args:
        opened_cards (list): A list of cards that were opened in a session.
        combination (list): A list of card names that constitute the required combination.
                            Example: ["Card A", "Card B", "Card A"]

    Returns:
        bool: True if the combination is met, False otherwise.
    """
    if not combination:
        return True # An empty combination is always "met"

    opened_counts = Counter(opened_cards)
    combination_counts = Counter(combination)

    for card_name, required_count in combination_counts.items():
        if opened_counts.get(card_name, 0) < required_count:
            return False # Not enough of this card to meet the combination
    return True

def simulate_card_opening(card_definitions, num_cards_to_open, target_combinations_to_track, num_simulations):
    """
    Runs multiple simulations of opening cards and tracks specific combinations.

    Args:
        card_definitions (dict): Dictionary of card names and their counts for deck creation.
        num_cards_to_open (int): Number of cards to open in each simulation.
        target_combinations_to_track (list): A list of lists, where each inner list is a combination
                                             of card names to track.
                                             Example: [["Dormouse", "FieldSpell"], ["Epic Z", "Epic Z"]]
        num_simulations (int): The number of times to run the card opening simulation.

    Returns:
        dict: A dictionary containing simulation results:
              - 'combination_results' (dict): Keys are combination tuples, values are counts of how many
                                              times that combination was met (each combination counted independently).
              - 'hands_with_no_target_combination_met' (int): Count of hands where none of the target combinations were met.
    """
    # Warn if any card in combinations isn't defined
    for combo in target_combinations_to_track:
        for card_in_combo in combo:
            if card_in_combo not in card_definitions:
                print(f"Warning: Card '{card_in_combo}' in combination {combo} is not defined in card_definitions.")

    combination_results = {tuple(sorted(combo)): 0 for combo in target_combinations_to_track} # Use sorted tuple as key
    hands_with_no_target_combination_met = 0

    print(f"\n--- Running {num_simulations} Simulations ---")
    for i in range(num_simulations):
        deck = create_deck(card_definitions)
        opened_cards = open_cards(deck, num_cards_to_open)

        current_hand_met_any_target_combination = False
        for combo in target_combinations_to_track:
            if check_for_combination(opened_cards, combo):
                combination_results[tuple(sorted(combo))] += 1
                current_hand_met_any_target_combination = True
        
        if not current_hand_met_any_target_combination:
            hands_with_no_target_combination_met += 1

    return {
        'combination_results': combination_results,
        'hands_with_no_target_combination_met': hands_with_no_target_combination_met
    }

if __name__ == "__main__":
    # --- Configuration ---
    # Define your cards and their exact counts in the deck
    my_card_definitions = {
        "Netabyss": 3,
        "Deep Sea Diva": 2,
        "Minstel": 1,
        "Infantry": 1,
        "Abyss Shrine": 3,
        "Shadow Squad": 3,
        "Dragoons": 3,
        "Abysspike": 3,
        "Abysteus": 3,
        "Poseidra": 3,
        "One for One": 1,
        "Non Engine": 14
    }

    # How many cards do you want to open in each "session" or "pack"?
    num_cards_to_open_per_session = 5

    # Define combinations of cards you want to track. Each combination is a list of card names.
    # The order within the combination doesn't matter, but duplicates *do* matter (e.g., ["Epic Z", "Epic Z"])

    # Malis Combinations that play
    my_target_combinations = [
        ["Netabyss"],
        ["Deep Sea Diva"],
        ["Abyss Shrine", "Infantry"],
        ["Abyss Shrine", "Shadow Squad"],
        ["Abyss Shrine", "Dragoons"],
        ["Abyss Shrine", "Abysspike"],
        ["Abyss Shrine", "Poseidra"],
        ["Shadow Squad", "Dragoons"],
        ["Shadow Squad", "Shadow Squad"],
        ["Abysspike", "Shadow Squad"],
        ["Abysteus", "Abyss Shrine"],
        ["Abysteus", "Dragoons"],
        ["Abysteus", "Shadow Squad"],
        ["Poseidra", "Dragoons"],
        ["Poseidra", "Shadow Squad"]
    ]

    # # Malis Combinations that beat 1 hand trap
    # my_target_combinations = [
    #     ["Dormouse", "Bystial"],
    #     ["Dormouse", "March Hare"],
    #     ["Dormouse", "FieldSpell"],
    #     ["Dormouse", "Gold Sarc"],
    #     ["Dormouse", "MTP"],
    #     ["White Rabbit", "Bystial"],
    #     ["White Rabbit", "March Hare"],
    #     ["White Rabbit", "FieldSpell"],
    #     ["White Rabbit", "Gold Sarc"],
    #     ["White Rabbit", "MTP"],
    #     ["@Ignister", "FieldSpell"],
    #     ["@Ignister", "Gold Sarc"]
    # ]

    # How many times do you want to run the entire simulation?
    number_of_simulations = 100000 # Increased for higher accuracy on probabilities

    # --- Initial Deck Information ---
    total_deck_size = sum(my_card_definitions.values())
    print(f"Card definitions: {my_card_definitions}")
    print(f"Total deck size: {total_deck_size} cards")
    print(f"Number of cards to open per session: {num_cards_to_open_per_session}")
    print(f"Target combinations to track: {my_target_combinations}")

    # --- Run the Simulation ---
    simulation_results = simulate_card_opening(
        my_card_definitions,
        num_cards_to_open_per_session,
        my_target_combinations,
        number_of_simulations
    )

    # --- Display Results ---
    print("\n--- Simulation Summary ---")
    print(f"Total simulations run: {number_of_simulations}")

    print("\n--- Individual Combination Tracking ---")
    for combo_tuple, count in simulation_results['combination_results'].items():
        original_combo = list(combo_tuple) # Convert back to list for display
        print(f"Combination {original_combo} was met in {count} out of {number_of_simulations} simulations.")
        probability = (count / number_of_simulations) * 100 if number_of_simulations > 0 else 0
        print(f"  Probability: {probability:.2f}%")

    # Calculate and display results for "at least one" and "none"
    hands_with_no_combo = simulation_results['hands_with_no_target_combination_met']
    hands_with_at_least_one_combo = number_of_simulations - hands_with_no_combo

    prob_no_combo = (hands_with_no_combo / number_of_simulations) * 100 if number_of_simulations > 0 else 0
    prob_at_least_one_combo = (hands_with_at_least_one_combo / number_of_simulations) * 100 if number_of_simulations > 0 else 0

    print("\n--- Overall Hand Statistics ---")
    print(f"Hands where AT LEAST ONE target combination was met: {hands_with_at_least_one_combo} out of {number_of_simulations} simulations.")
    print(f"  Probability: {prob_at_least_one_combo:.2f}%")

    print(f"Hands where NONE of the target combinations were met: {hands_with_no_combo} out of {number_of_simulations} simulations.")
    print(f"  Probability: {prob_no_combo:.2f}%")