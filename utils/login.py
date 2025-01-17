def encrypt(password, shift=3):
    """
    Encrypts a given password using a Caesar cipher with a given shift.
    :param password: The plain text password to encrypt.
    :param shift: The shift value for the Caesar cipher.
    :return: The encrypted password.
    """
    encrypted = "".join(chr((ord(char) + shift) % 256) for char in password)
    return encrypted


def handle_role(role):
    from utils.menu import (admin_menu, lecturer_menu,
                            registrar_menu, accountant_menu)
    """
    Handles actions based on the user role.
    :param role: The role of the user (Admin, Lecturer, etc.).
    """
    # Normalize role capitalization
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

    print("Available roles: student, lecturer, accountant, admin")
    role = input("Enter your role: ").strip().capitalize()
    if role not in valid_roles:
        print("Invalid role. Please choose from the available roles.")
        return

    encrypted_password = encrypt(password)
    users.append([username, encrypted_password, role])

    if role == "Admin":
        # Require an admin access code for admin role registration
        admin_access_code = "1234"
        entered_code = input("Enter the admin access code to register as admin: ").strip()
        if entered_code != admin_access_code:
            print("Invalid access code. You cannot register as an admin.")
            return

    # Save the user details to the user_data file
    with open(user_file, "w", encoding="utf-8") as file:
        for user in users:
            file.write(",".join(user) + "\n")
    print(f"User '{username}' registered successfully as {role}.")

def login(user_file="user_data.txt"):
    from utils.filehandling import log_message
    """
    Handles user login by verifying credentials against a user data file.
    :param user_file: Path to the user data file.
    :return: The role of the logged-in user if successful, or None if login fails.
    """
    # Load current users
    try:
        with open(user_file, "r", encoding="utf-8") as file:
            users = [line.strip().split(",") for line in file if line.strip()]
    except FileNotFoundError:
        print(f"Error: User data file '{user_file}' not found. Please register first.")
        log_message(f"Error: User data file '{user_file}' not found. Please register first.")
        return None

    # Prompt for credentials
    entered_username = input("Enter your username: ").strip()
    entered_password = input("Enter your password: ").strip()

    # Encrypt the entered password for comparison
    encrypted_entered_password = encrypt(entered_password)

    # Check for matching username and password
    for user in users:
        stored_username, stored_password, stored_role = user
        if entered_username == stored_username and encrypted_entered_password == stored_password:
            print(f"Login successful! Welcome, {entered_username}.")
            return stored_role

    print("Invalid username or password. Please try again.")
    return None


def load_user_data(file_path):
    """
    Loads user data from a file.
    :param file_path: Path to the user data file.
    :return: A list of user data (each entry as [username, password, role]).
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return [line.strip().split(",") for line in file if line.strip()]
    except FileNotFoundError:
        return []


def save_user_data(users, file_path):
    """
    Saves user data to a file.
    :param users: A list of user data (each entry as a dictionary with keys: username, password, role).
    :param file_path: Path to the user data file.
    """
    with open(file_path, "w", encoding="utf-8") as file:
        for user in users:
            file.write(f"{user['username']},{user['password']},{user['role']}\n")