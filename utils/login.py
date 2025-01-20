def encrypt(password, shift=3):
    """
    Encrypts a password using a Caesar cipher-like encryption technique. Each character
    in the password is shifted by a specified value, wrapping around within the range of
    valid character codes.
    """
    encrypted = "".join(chr((ord(char) + shift) % 256) for char in password)
    return encrypted


def handle_role(role):
    """
    Handles user role and redirects to the appropriate role menu interface.
    This function processes an input role, normalizes the format, and calls the
    corresponding role-specific menu function. If the role is not valid, it
    prints an error message stating there is no menu for the specified role.
    """
    from utils.menu import (admin_menu, lecturer_menu,
                            registrar_menu, accountant_menu)
    role = role.strip().capitalize()
    if role == "Admin":
        print("Accessing Admin Menu.")
        admin_menu()  # Call the relevant menu function
    elif role == "Lecturer":
        print("Accessing Lecturer Menu.")
        lecturer_menu()  # Call the relevant menu function
    elif role == "Accountant":
        print("Accessing Accountant Menu.")
        accountant_menu()
    elif role == "Registrar":
        print("Accessing Registrar Menu.")
        registrar_menu()
    elif role == "Student":
        print("Accessing Student Menu.")
    else:
        print(f"Invalid role: {role}. No menu available.")


def register_user(user_file="user_data.txt"):
    """
    This interface registers a new user by storing his credentials and role in the system. Validates user details
    for unique usernames, password matching, and proper role selection. Handles special
    Test cases to register admin users by requiring a valid admin access code.
    """
    valid_roles = ["Student", "Lecturer", "Accountant", "Admin", "Registrar"]
    try:
        with open(user_file, "r", encoding="utf-8") as file:
            users = [line.strip().split(",") for line in file if line.strip()]
    except FileNotFoundError:
        users = []

    username = input("Enter a username: ").strip()
    if any(user[0] == username for user in users):
        print("Error: Username already exists. Please try another.")
        return

    password = input("Enter a password: ").strip()
    confirm_password = input("Re-enter your password: ").strip()
    if password != confirm_password:
        print("Error: Passwords do not match.")
        return

    print("Available roles: student, lecturer, accountant, registrar and admin")
    role = input("Enter your role: ").strip().capitalize()
    if role not in valid_roles:
        print("Invalid role. Please choose from the available roles.")
        return

    encrypted_password = encrypt(password)
    users.append([username, encrypted_password, role])

    if role == "Admin":
        admin_access_code = "1234"
        entered_code = input("Enter the admin access code to register as admin: ").strip()
        if entered_code != admin_access_code:
            print("Invalid access code. You cannot register as an admin.")
            return

    with open(user_file, "w", encoding="utf-8") as file:
        for user in users:
            file.write(",".join(user) + "\n")
    print(f"User '{username}' registered successfully as {role}.")


def login(user_file="user_data.txt"):
    """
    Logs a user in with a check against stored user data via their username and password.
    It reads the user data from a specified file. Passwords are encrypted for security.
    It returns the role of the authenticated user in case of a match.
    """
    from utils.filehandling import log_message
    try:
        with open(user_file, "r", encoding="utf-8") as file:
            users = [line.strip().split(",") for line in file if line.strip()]
    except FileNotFoundError:
        print(f"Error: User data file '{user_file}' not found. Please register first.")
        log_message(f"Error: User data file '{user_file}' not found. Please register first.")
        return None

    entered_username = input("Enter your username: ").strip()
    entered_password = input("Enter your password: ").strip()

    encrypted_entered_password = encrypt(entered_password)

    for user in users:
        stored_username, stored_password, stored_role = user
        if entered_username == stored_username and encrypted_entered_password == stored_password:
            print(f"Login successful! Welcome, {entered_username}.")
            return stored_role

    print("Invalid username or password. Please try again.")
    return None


def load_user_data(file_path):
    """
    The function load_user_data reads user data from a file, processes it line by line, and
    returns a list of lists containing user data entries split by commas. In case the file
    if it is not found, an empty list is returned instead of raising an error.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return [line.strip().split(",") for line in file if line.strip()]
    except FileNotFoundError:
        return []


def save_user_data(users, file_path):
    """
    The user data should be provided as a list of lists, where each inner list contains
    the username, password, and role.
    """
    with open(file_path, "w", encoding="utf-8") as file:
        for user in users:
            # Write each user's data as a comma-separated line
            file.write(",".join(user) + "\n")
