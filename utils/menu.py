from utils.accountant import *
from utils.admin import *
from utils.lecturer import *
from utils.login import login, register_user, handle_role
from utils.registrar import *
from utils.utility import *
from utils.student import *


def display_menu(menu_options):
    print("\n--- Menu ---")
    for idx, option in enumerate(menu_options, start=1):
        print(f"{idx}. {option}")


def handle_menu(menu_options, actions, logout_message="Logging out..."):
    while True:
        display_menu(menu_options)
        choice = input("Enter your choice (0 to logout): ").strip()
        if choice.isdigit():
            choice = int(choice)
            if choice == 0:
                print(logout_message)
                break
            elif 1 <= choice <= len(actions):
                try:
                    actions[choice - 1]()
                except Exception as error:
                    print(f"An error occurred: {error}")
            else:
                print("Invalid choice. Please select a valid option.")
        else:
            print("Invalid input. Please enter a number.")


def admin_menu():
    menu_options = [
        "Add Course",
        "Remove Course",
        "Add Student",
        "Remove Student",
        "Create Module",
        "Search Student In Module",
        "Search Course",
        "Generate Report",
        "Student Statistics",
        "Logout"
    ]

    actions = [
        add_course,
        remove_course,
        add_student,
        remove_student,
        create_module,
        search_student_in_module,
        search_course,
        generate_report,
        student_statistics
    ]

    handle_menu(menu_options, actions, "Logging out from Admin Menu...")


def lecturer_menu():
    """
    Displays and handles actions for the Lecturer Menu.
    """
    menu_options = [
        "View Assigned Modules",
        "Add Student to Module",
        "Remove Student from Module",
        "View Enrolled Students",
        "Search Student In Module",
        "Give Attendance",
        "View Attendance",
        "Add Grades",
        "View Grades",
        "Logout"
    ]

    actions = [
        view_assigned_modules,
        add_student_to_module,
        remove_student_from_module,
        view_enrolled_students,
        search_student_in_module,
        give_attendance,
        view_attendance,
        add_grade,
        view_grades
    ]

    handle_menu(menu_options, actions, "Logging out from Lecturer Menu...")


def accountant_menu():
    """
    Displays and handles actions for the Accountant Menu.
    """
    menu_options = [
        "Record Tuition Fees",
        "View Outstanding Fees",
        "View Financial Summary",
        "Logout"
    ]

    actions = [
        record_tuition_fees_to_file,
        view_outstanding_fees,
        view_financial_summary
    ]

    handle_menu(menu_options, actions, "Logging out from Accountant Menu...")


def registrar_menu():
    """
    Displays and handles actions for the Registrar Menu.
    """
    menu_options = [
        "Register Student",
        "Update Student Records",
        "Manage Enrolments",
        "Issue Transcript for Student",
        "View Student Information",
        "Logout"
    ]

    actions = [
        student_registration,
        view_registrations,
        process_registrations,
        generate_report_accepted,
        generate_report_declined
    ]

    handle_menu(menu_options, actions, "Logging out from Registrar Menu...")

def student_menu():
    while True:
        print("\nUniversity Management System - Student Role")
        print("1. View Available Modules")
        print("2. Enrol in Module")
        print("3. Unenroll from Module")
        print("4. View Attendance")
        print("5. View Grades")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            view_available_modules()
        elif choice == '2':
            student_id = input("Enter your student ID: ")
            module_id = input("Enter the module ID you want to enroll in: ")
            add_student_module(module_id, student_id)
        elif choice == '3':
            student_id = input("Enter your student ID: ")
            module_id = input("Enter the module name you want to unenroll from: ")
            unenroll_from_module(student_id, module_id)
        elif choice == '4':
            print("View Attendance...")
            view_attendance()
        elif choice == '5':
            print("Viewing Grades...")
            view_grades()
        elif choice == '6':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

def staff_menu(user_file="user_data.txt"):
    """
    Displays the staff menu with role-based access control.
    """
    menu_options = [
        "Admin Menu",
        "Lecturer Menu",
        "Accountant Menu",
        "Registrar Menu",
        "Register",
        "Login",
        "Exit"
    ]

    while True:
        display_menu(menu_options)

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            print("Accessing Admin Menu requires admin login.")
            user_role = login(user_file)
            if user_role == "Admin":
                admin_menu()
            else:
                print("Access denied. You are not authorized to access the Admin Menu.")
        elif choice == "2":
            print("Accessing Lecturer Menu requires lecturer login.")
            user_role = login(user_file)
            if user_role == "Lecturer":
                lecturer_menu()
            else:
                print("Access denied. You are not authorized to access the Lecturer Menu.")
        elif choice == "3":
            print("Accessing Accountant Menu requires accountant login.")
            user_role = login(user_file)
            if user_role == "Accountant":
                accountant_menu()
            else:
                print("Access denied. You are not authorized to access the Accountant Menu.")
        elif choice == "4":
            print("Accessing Registrar Menu requires registrar login.")
            user_role = login(user_file)
            if user_role == "Registrar":
                registrar_menu()
            else:
                print("Access denied. You are not authorized to access the Registrar Menu.")
        elif choice == "5":
            register_user(user_file)
        elif choice == "6":
            role = login(user_file)
            if role:
                handle_role(role)
        elif choice == "7":
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 7.")


def guest_menu():
    """
    Displays the guest menu with limited options.
    """
    menu_options = [
        "View General Information",
        "Register as a Student",
        "Access Staff Menu (Password Required)",
        "Student Menu",
        "Exit"
    ]

    while True:
        display_menu(menu_options)

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            print("General information: Welcome to our University Management System.")
        elif choice == "2":
            print("Redirecting to Student Registration...")
            student_registration()
        elif choice == "3":
            password = input("Enter the staff menu password: ").strip()
            if password == "staff123":
                print("Access granted. Redirecting to Staff Menu...")
                staff_menu()
            else:
                print("Invalid password. Access denied.")
        elif choice == "4":
            print("Redirecting to Student Menu")
            student_menu()
        elif choice == "5":
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")


if __name__ == "__main__":
    guest_menu()
