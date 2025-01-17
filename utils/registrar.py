from utils.filehandling import read_file, append_to_file


def student_registration(file_path="registrations.txt"):
    """
    This function facilitates the student registration process, collecting user inputs
    such as name, email, passport number, and course applied for. It validates the input fields and,
    if valid, appends data to a specified file. If it detects an invalid input, it raises
    an appropriate error.
    """
    print("Hello, this is student registration page!\n"
          "Please enter your details according to the given format:\n")
    try:
        name = input("Name: ").strip()
        if not name:
            raise ValueError("Name cannot be empty.")
        email = input("Email: ").strip()
        # Validates the email input by checking if it is not empty and contains "@" and ".".
        if not email or "@" not in email or "." not in email:
            raise ValueError("Invalid email format.")
        passport_number = input("Passport Number: ").strip()
        if not passport_number:
            raise ValueError("Passport Number cannot be empty.")
        course = input("What course you want to enroll in?: ").strip()
        if not course:
            raise ValueError("Course cannot be empty.")
        append_to_file(file_path, f"{name},{email},{passport_number},{course}\n")
    except ValueError as e:
        print(f"Error: {e}")
        return
    print(f"Name: {name}, Email: {email}, Passport Number: {passport_number}, Course: {course}")
    print("Thank you for your registration!")
    input("Press Enter to continue...")
    return


def view_registrations(file_path="registrations.txt"):
    """
        Reads and displays user registration details from a provided file.
        Each entry is expected to have a four comma-separated fields.

        If the file does not exist, is empty, or contains formatting issues,
        appropriate error messages will be displayed.
    """
    try:
        file_contents = read_file(file_path)
        # Checks for empty or whitespace lines
        if not file_contents or all(line.strip() == "" for line in file_contents):
            print(f"Error: {file_path} is empty. No registrations to display.")
            return
        # Iterating directly over the list elements
        for line in file_contents:
            fields = line.strip().split(",")
            if len(fields) == 4:
                print(f"Name: {fields[0]:<18} Email: {fields[1]:<28} Department: {fields[3]:<18}")
                input("Press Enter to continue...")
    except FileNotFoundError:
        print("Error: No registrations file found.")


def process_registrations(file_path="registrations.txt"):
    """
    Processes student registration data from a file, allowing the registrar to
    accept or decline each registration and perform additional actions based on the decision.

    The function reads a specified file containing registration details, prompts the user for
    input regarding registration decisions, and updates the corresponding
    files and records accordingly.
    """
    print("Processing registrations:")
    # Call view_registrations() to display the registrations
    view_registrations(file_path)
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
        # If the file has no lines, print an error and exit the function,
        if not lines:
            print(f"Error: {file_path} is empty. No registrations to process.")
            return
        for line in lines:
            fields = line.strip().split(",")
            if len(fields) == 4:
                while True:
                    decision = input(
                        f"Do you want to accept or decline this registration? (accept/decline) for {fields[0]}: ").strip().lower()
                    if decision in ["accept", "decline"]:
                        # Decide the file to write to based on decision
                        file_to_write = "accepted_registrations.txt" if decision == "accept" else "declined_registrations.txt"
                        append_to_file(file_to_write, line)
                        if decision == "accept":
                            # Display the accepted student information
                            print("\nAccepted Student Information (copy this for reference):")
                            print(f"Name: {fields[0]}")
                            print(f"Email: {fields[1]}")
                            print(f"Passport Number: {fields[2]}")
                            print(f"Department: {fields[3]}\n")
                            # Calls add_student() for additional processing
                            from utils.admin import add_student  # Import add_student
                            add_student()
                        else:
                            # Removes the student from registrations.txt
                            print(f"Student {fields[0]} has been declined.\n")

                        # Filter out current line,
                        lines = [l for l in lines if l.strip() != line.strip()]
                        # Overwrites the file,
                        with open(file_path, "w") as file:
                            file.writelines(lines)
                        break
                    else:
                        print("Invalid input. Please enter 'accept' or 'decline'.")
    except FileNotFoundError:
        print("Error: No registrations found.")


def generate_report_accepted(file_path="accepted_registrations.txt"):
    try:
        file_contents = read_file(file_path)
        print("Accepted registrations: ")
        # Directly iterate over each line in the list
        for line in file_contents:
            fields = line.strip().split(",")
            if len(fields) == 4:
                print(f"Name: {fields[0]:<18} Email: {fields[1]:<28} Department: {fields[3]:<18}")

            input("Press Enter to continue...")
    except FileNotFoundError:
        print("No accepted registrations found.")


def generate_report_declined(file_path="declined_registrations.txt"):
    try:
        file_contents = read_file(file_path)
        print("Declined registrations: ")
        # Directly iterate over each line in the list
        for line in file_contents:
            fields = line.strip().split(",")
            if len(fields) == 4:
                print(f"Name: {fields[0]:<18} Email: {fields[1]:<28} Department: {fields[3]:<18}")

            input("Press Enter to continue...")
    except FileNotFoundError:
        print("No declined registrations found.")
