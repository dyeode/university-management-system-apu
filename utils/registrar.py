from utils.filehandling import read_file, append_to_file


def display_paginated_courses(file_path, page_size=5):
    """
    Displays courses from a file in a paginated menu for easier browsing.
    If the file is empty or not formatted correctly, appropriate messages are displayed.
    """
    try:
        courses = read_file(file_path)
        if not courses:
            print("No courses available in the file.")
            return None

        total_courses = len(courses)
        current_page = 0

        while True:
            start_index = current_page * page_size
            end_index = start_index + page_size

            print("\nAvailable Courses:")
            print("-" * 40)
            for i in range(start_index, min(end_index, total_courses)):
                course = courses[i].strip().split(",", 1)
                if len(course) == 2:
                    # Using list indexing
                    course_id = course[0]
                    course_name = course[1]
                    print(f"{i + 1}. {course_name.strip()} (ID: {course_id.strip()})")
                else:
                    print(f"{i + 1}. Invalid course entry: {courses[i]}")
            print("-" * 40)

            print("\nOptions:")
            if end_index < total_courses:
                print("N. Next Page")
            if current_page > 0:
                print("P. Previous Page")
            print("Enter the number corresponding to a course to select it.")
            print("E. Exit Course Selection")

            choice = input("Enter your choice: ").strip().lower()

            if choice == "n" and end_index < total_courses:
                current_page += 1
            elif choice == "p" and current_page > 0:
                current_page -= 1
            elif choice.isdigit():
                selected_index = int(choice) - 1
                if 0 <= selected_index < total_courses:
                    course_entry = courses[selected_index].strip().split(",", 1)
                    if len(course_entry) == 2:
                        return course_entry[1].strip()  # Return course name
                    print("Invalid course entry. Please select again.")
                else:
                    print("Invalid selection. Please try again.")
            elif choice == "e":
                return None
            else:
                print("Invalid option. Please try again.")
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None


def student_registration(file_path="registrations.txt", courses_file="courses.txt"):
    selected_course = display_paginated_courses(courses_file)
    if not selected_course:
        print("No course selected or course selection cancelled.")
        return

    print("\nWelcome to the Student Registration Page!")
    try:
        name = input("Name: ").strip()
        if not name:
            raise ValueError("Name cannot be empty.")
        email = input("Email: ").strip()
        if not email or "@" not in email or "." not in email:
            raise ValueError("Invalid email format.")
        passport_number = input("Passport Number: ").strip()
        if not passport_number:
            raise ValueError("Passport Number cannot be empty.")

        append_to_file(file_path, f"{name},{email},{passport_number},{selected_course}\n")

        print("\nRegistration Successful!")
        print(f"Name: {name}\nEmail: {email}\nPassport Number: {passport_number}\nCourse: {selected_course}")
        input("Press Enter to return to the main menu...")
    except ValueError as e:
        print(f"Error: {e}")


def view_registrations(file_path="registrations.txt"):
    try:
        file_contents = read_file(file_path)
        if not file_contents or all(line.strip() == "" for line in file_contents):
            print(f"Error: {file_path} is empty. No registrations to display.")
            return

        print("\nCurrent Registrations:")
        print("-" * 50)
        for line in file_contents:
            fields = line.strip().split(",")
            if len(fields) >= 4:
                # Using list indexing
                name = fields[0].strip()
                email = fields[1].strip()
                passport = fields[2].strip()
                course = fields[3].strip()
                print(f"Name: {name:<18} Email: {email:<28} Course: {course:<18}")
            else:
                print(f"Malformed entry skipped: {line.strip()}")
        print("-" * 50)

        input("Press Enter to continue...")
    except FileNotFoundError:
        print("Error: No registrations file found.")


def process_registrations(file_path="registrations.txt", courses_file="courses.txt"):
    print("Processing registrations...")

    try:
        with open(courses_file, "r") as file:
            # Modified list comprehension to avoid tuple creation
            courses = [[split_line[0].strip(), split_line[1].strip()]
                      for line in file
                      if "," in line
                      for split_line in [line.strip().split(",", 1)]]

        file_contents = read_file(file_path)
        if not file_contents or all(line.strip() == "" for line in file_contents):
            print(f"Error: {file_path} is empty. No registrations to process.")
            return

        for line in file_contents:
            fields = line.strip().split(",")
            if len(fields) < 4:
                print(f"Malformed entry skipped: {line.strip()}")
                continue

            name = fields[0].strip()
            email = fields[1].strip()
            passport = fields[2].strip()
            course = ",".join(fields[3:]).strip()

            course_id = None
            for course_entry in courses:
                if len(course_entry) == 2 and course_entry[1] == course:
                    course_id = course_entry[0]
                    break

            while True:
                decision = input(
                    f"Do you want to accept or decline this registration? (accept/decline) for {name}: "
                ).strip().lower()

                if decision in ["accept", "decline"]:
                    file_to_write = (
                        "accepted_registrations.txt"
                        if decision == "accept"
                        else "declined_registrations.txt"
                    )
                    append_to_file(file_to_write, line)

                    if decision == "accept":
                        print("\nAccepted Student Information (copy this for reference):")
                        print(f"Name: {name}")
                        print(f"Email: {email}")
                        print(f"Passport Number: {passport}")
                        print(f"Course: {course}")
                        print(f"Course ID: {course_id if course_id else 'Not Found'}")

                        try:
                            from utils.admin import add_student
                            add_student()
                        except ImportError:
                            print("Error: Could not import 'add_student'. Ensure the module exists.")
                    else:
                        print(f"Student {name} has been declined.\n")

                    remaining_lines = [l for l in file_contents if l.strip() != line.strip()]
                    with open(file_path, "w") as file:
                        file.writelines(remaining_lines)
                    break
                else:
                    print("Invalid input. Please enter 'accept' or 'decline'.")
    except FileNotFoundError as e:
        print(f"Error: {e.filename} was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def generate_report_accepted(file_path="accepted_registrations.txt"):
    try:
        file_contents = read_file(file_path)
        print("Accepted registrations: ")
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
        for line in file_contents:
            fields = line.strip().split(",")
            if len(fields) == 4:
                print(f"Name: {fields[0]:<18} Email: {fields[1]:<28} Department: {fields[3]:<18}")

        input("Press Enter to continue...")
    except FileNotFoundError:
        print("No declined registrations found.")


def check_student_acceptance(accepted_file="accepted_registrations.txt", declined_file="declined_registrations.txt"):
    passport_number = input("Enter the Passport Number: ").strip()
    if not passport_number:
        print("Error: Passport number cannot be empty.")
        return

    try:
        with open(accepted_file, "r", encoding="utf-8") as file:
            for line in file:
                fields = line.strip().split(",")
                if len(fields) >= 3 and fields[2] == passport_number:
                    print("The student has been accepted.")
                    return

        with open(declined_file, "r", encoding="utf-8") as file:
            for line in file:
                fields = line.strip().split(",")
                if len(fields) >= 3 and fields[2] == passport_number:
                    print("The student has been declined.")
                    return

        print("The student is not found in the records.")

    except FileNotFoundError as e:
        print(f"Error: File '{e.filename}' not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    print("Registrar Module loaded.")