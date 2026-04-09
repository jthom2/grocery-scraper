def select_from_list(items, prompt="Select store number", quit_char='q'):
    while True:
        choice = input(f"{prompt} (or '{quit_char}' to quit): ").strip()
        if choice.lower() == quit_char:
            return None
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(items):
                return items[idx]
            print(f"Please enter a number between 1 and {len(items)}")
        except ValueError:
            print("Invalid input. Please enter a number.")
