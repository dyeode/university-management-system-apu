from utils.filehandling import read_file, overwrite_file, append_to_file, log_message


def get_module_initials(module_name):
    return ''.join(word[0].upper() for word in module_name.split())


def get_lecturer_initials(lecturer_name):
    return ''.join(word[0].upper() for word in lecturer_name.split())


def generate_unique_id(base_value):
    seed = (base_value * 1234) % 10000
    # Ensure the ID is at least 4 digits long
    return str(seed).zfill(4)


def get_current_record_count(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return len(file.readlines())
    except FileNotFoundError:
        return 0


def generate_module_id(module_name, lecturer_name, base_value):
    """
    Creates a unique module identifier, based on the module name and lecturer name,
    and a base value. The module identifier consists of a prefix resulting from the
    module name, base value from which a unique ID will be created and initials for both
    the module and the lecturer.
    """
    prefix = module_name[:2].upper()
    unique_id = generate_unique_id(base_value)
    module_id = f"{prefix}{unique_id}"
    module_initials = get_module_initials(module_name)
    lecturer_initials = get_lecturer_initials(lecturer_name)
    return f"{module_id}-{module_initials}-{lecturer_initials}"


def validate_credits(credits):
    return credits.isdigit()


def create_module(file_path="modules_list.txt"):
    """
    This function creates a module by taking user input and appends its details into a file.
    Also allows the user to input the details of a module including its name,
    lecturer information, credits, and the number of classes needed.

    It checks for valid inputs & generates a unique module ID, and appends the data to the specified file.
    """
    try:
        module_name = input("Enter the Module Name: ").strip()
        if not module_name:
            print("Module Name cannot be empty.")
            return
        lecturer_name = input("Enter the Lecturer Name assigned to this module: ").strip()
        if not lecturer_name:
            print("Lecturer Name cannot be empty.")
            return
        lecturer_id = input("Enter the Lecturer ID assigned to this module: ").strip()
        if not lecturer_id:
            print("Lecturer ID cannot be empty.")
            return
        credits = input("Enter the Credits for this module: ").strip()
        if not validate_credits(credits):
            print("Credits must be a valid number.")
            return
        number_of_classes = int(input("Enter the number of classes to be attended for this module: "))
        if not number_of_classes:
            print("Number of classes to be attended cannot be empty.")
            return
        record_count = get_current_record_count(file_path)
        module_id = generate_module_id(module_name, lecturer_name, record_count)
        module_data = f"{module_id},{module_name},{lecturer_name},{lecturer_id},{credits},{number_of_classes}\n"
        with open(file_path, "a", encoding="utf-8") as file:
            file.write(module_data)
        print(f"Module '{module_name}' created successfully with ID: {module_id}")

    except Exception as e:
        print(f"An error occurred while creating the module: {e}")


def get_course_details():
    """
    Prompts the user to input details for a new course and generates a unique course ID.
    The course code is generated using the initials of the course name.
    A unique ID is created by hashing the course name and appending a random value.
    """
    name = input("Enter the course name: ").strip()
    details = input("Enter course details: ").strip()
    uni_initials = input("Enter university initials: ").strip()

    # Generate the course code from the initials of the course name
    course_code = "".join(word[0].upper() for word in name.split())

    # Generate a unique ID seed using the sum of ASCII values of characters in the name
    id_seed = sum(ord(char) for char in name) * len(name)

    # Calculate a pseudo-random three-digit ID
    random_id = (id_seed * 73) % 1000

    # Ensuring it is zero padded to three digits
    formatted_id = f"{random_id:03d}"

    # Combining into a final generated code
    generated_code = f"{course_code}{formatted_id}-{uni_initials}"
    return f"{generated_code},{name},{details}\n"

def write_to_course_file(file_path, content):
    """
    Appends content to a file with proper formatting by adding a newline if needed.
    If the file is not empty, a newline character is added before appending the content.
    The appended content does not have leading or trailing spaces.
    """
    with open(file_path, "a") as file:
        # Move the file pointer to the end to check the file size
        file.seek(0, 2)

        # If the file is not empty, add a newline before appending the content
        if file.tell() > 0:
            file.write("\n")

        # Write the stripped content to the file
        file.write(content.strip())


def read_and_clean_file(file_path):
    """
    Helper function to read the contents of a file, and removes empty lines and leading whitespace,
    and writes the cleaned content back to the file.
    """
    with open(file_path, "r") as file:
        lines = [line.strip() for line in file if line.strip()]
    with open(file_path, "w") as file:
        for line in lines:
            file.write(line + "\n")
    return lines


def add_course(file_path="courses.txt", log_file="admin_log.txt"):
    """
    Adds a new course to the course file after cleaning the file and validating the input.
    """
    try:
        # If the file exists, open in append mode
        with open(file_path, "a", encoding="utf-8"):
            pass

        # Clean the file to remove empty lines
        read_and_clean_file(file_path)

        # Get new course details from the user
        course_data = get_course_details().strip()

        # Append the new course to the file
        append_to_file(file_path, course_data)

        print("Course added successfully.")
        input("Press Enter to continue...")
        log_message("Course added successfully.", log_file)
    except Exception as e:
        error_message = f"An error occurred while adding the course: {e}"
        print(error_message)
        log_message(error_message, log_file)


def display_courses(file_path):
    """
    Reads and displays a list of courses from the specified file.
    If the file does not exist, an error message is displayed, and an empty list is returned.
    """
    try:
        courses = read_file(file_path)
    except FileNotFoundError:
        print(f"The file '{file_path}' does not exist.")
        return []
    print("Available Courses:")
    for course in courses:
        # Split each course into ID and name using the first comma
        split_course = course.split(",", 1)

        # Validate the line has exactly two fields
        if len(split_course) == 2:
            course_id, course_name = split_course
            print(f"ID: {course_id}, Name: {course_name}")
        else:
            print(f"Invalid entry: {course}")
    return courses


def find_course(courses, identifier):
    """
    Helper function to find the specified course by input.
    """
    matching_courses = []
    for course in courses:
        if identifier in course:
            matching_courses.append(course)
    return matching_courses


def remove_course(file_path="courses.txt", log_file="admin_log.txt"):
    """
    Removes the specified course from the specified file.
    If the file does not exist, an error message is displayed, and an empty list is returned.
    """
    try:
        courses = display_courses(file_path)
        if not courses:
            log_message(f"No courses to display in '{file_path}'.", log_file)
            return
        identifier = input("Enter the course ID or name to remove: ").strip()
        if not identifier:
            print("Invalid input. Operation cancelled.")
            log_message("Invalid course removal attempt (empty identifier).", log_file)
            return
        matching_courses = find_course(courses, identifier)
        if not matching_courses:
            print(f"No course found with the identifier: {identifier}.")
            log_message(f"Attempt to remove non-existent course: {identifier}.", log_file)
            return
        print("Matching Courses:")
        for match in matching_courses:
            print(match)
        confirmation = input("Are you sure you want to remove this course? (yes/no): ").strip().lower()
        if confirmation != "yes":
            print("Operation cancelled.")
            log_message("Course removal cancelled by user.", log_file)
            return
        updated_courses = []
        for course in courses:
            if course not in matching_courses:
                updated_courses.append(course)
        overwrite_file(file_path, updated_courses)
        print("Course(s) removed successfully!")
        for course in matching_courses:
            log_message(f"Course removed: {course}", log_file)
    except FileNotFoundError:
        print(f"The file '{file_path}' does not exist.")
        log_message(f"File '{file_path}' not found. Operation aborted.", log_file)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        log_message("Operation interrupted by user (KeyboardInterrupt).", log_file)
    except Exception as e:
        print(f"An error occurred: {e}")
        log_message(f"Unexpected error: {e}", log_file)


def update_course(file_path="courses.txt", log_file="admin_log.txt"):
    """
    Updates the name or details of an existing course in the specified file.
    """
    try:
        courses = read_file(file_path)
        course_code = input("Enter the course code to update: ").strip()

        if not course_code:
            print("Invalid course code. Operation cancelled.")
            log_message("Invalid course update attempt (empty course code).", log_file)
            return

        updated_courses = []
        course_found = False

        # Iterating through each course in the file
        for course in courses:
            split_course = course.split(",", 2)
            if len(split_course) < 3:
                updated_courses.append(course)
                continue
            current_code, current_name, current_details = split_course

            # If the course code matches, prompt for updates
            if current_code == course_code:
                course_found = True
                print(
                    f"Current Course Data: Code: {current_code}, Name: {current_name}, Details: {current_details.strip()}")
                new_name = input("Enter the updated course name (or press Enter to keep unchanged): ").strip()
                new_details = input("Enter the updated course details (or press Enter to keep unchanged): ").strip()
                updated_name = new_name if new_name else current_name
                updated_details = new_details if new_details else current_details
                updated_course = f"{current_code},{updated_name},{updated_details.strip()}"
                updated_courses.append(updated_course)
            else:
                updated_courses.append(course)
        if course_found:
            overwrite_file(file_path, [f"{line.strip()}\n" for line in updated_courses])
            print("Course updated successfully.")
            log_message(f"Course with code '{course_code}' updated successfully.", log_file)
        else:
            print(f"No course found with the code '{course_code}'.")
            log_message(f"Attempted to update non-existent course with code: '{course_code}'.", log_file)
    except FileNotFoundError:
        print(f"The file '{file_path}' does not exist.")
        log_message(f"File '{file_path}' not found. Course update aborted.", log_file)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        log_message("Course update operation cancelled by user (KeyboardInterrupt).", log_file)
    except Exception as e:
        print(f"An error occurred while updating the course: {e}")
        log_message(f"Error updating course: {e}", log_file)


def read_courses(file_path="courses.txt", log_file="admin_log.txt"):
    """
    Helper function that reads the course file and returns a list of courses.
    """
    try:
        courses = read_file(file_path)
        valid_courses = [course.strip() for course in courses if ',' in course]
        invalid_courses = [course.strip() for course in courses if ',' not in course]
        for invalid in invalid_courses:
            log_message(f"Malformed course line ignored: {invalid}", log_file)
        return valid_courses
    except FileNotFoundError:
        log_message(f"File '{file_path}' not found.", log_file)
        return []


def read_modules(file_path="modules_list.txt", log_file="admin_log.txt"):
    """
    Helper function that reads the modules file and returns a list of modules.
    """
    try:
        modules = read_file(file_path)
        valid_modules = [module.strip() for module in modules if len(module.split(",")) >= 3]
        invalid_modules = [module.strip() for module in modules if len(module.split(",")) < 3]
        for invalid in invalid_modules:
            log_message(f"Malformed module line ignored: {invalid}", log_file)
        return valid_modules
    except FileNotFoundError:
        log_message(f"File '{file_path}' not found.", log_file)
        return []


def validate_course(course, courses):
    return any(course_record.split(",")[0] == course for course_record in courses)


def validate_modules(modules_input, modules, log_file="admin_log.txt"):
    """
    Helper function that validates the modules file and returns a list of modules.
    """
    try:
        valid_module_ids = [module.split(",")[0] for module in modules if len(module.split(",")) >= 1]
        valid_modules = [module for module in modules_input if module in valid_module_ids]
        invalid_modules = [module for module in modules_input if module not in valid_module_ids]
        if invalid_modules:
            log_message(f"Invalid module IDs provided: {', '.join(invalid_modules)}", log_file)
            print(f"The following module IDs are invalid: {', '.join(invalid_modules)}")
        return valid_modules, invalid_modules
    except Exception as e:
        log_message(f"Error occurred while validating modules: {e}", log_file)
        return [], modules_input


def log_error_and_exit(message, log_file="admin_log.txt"):
    print(message)
    log_message(message, log_file)


def add_student(file_path="student_records.txt", courses_file="courses.txt", modules_file="modules_list.txt",
                log_file="admin_log.txt"):
    """
    Helper function that adds a student record to a file.
    """
    try:
        courses = read_courses(courses_file, log_file)
        modules = read_modules(modules_file, log_file)
        if not courses:
            log_error_and_exit(f"No valid courses found in '{courses_file}'.", log_file)
            return
        if not modules:
            log_error_and_exit(f"No valid modules found in '{modules_file}'.", log_file)
            return
        name = get_input("Enter the student's name: ")
        phone_number = get_input("Enter the student's phone number: ")
        email = get_input("Enter the student's email: ")
        address = get_input("Enter the student's address: ")
        age = get_input("Enter the student's age: ")
        student_id = generate_student_id(name)
        course = get_input("Enter the student's course (course code): ").strip()
        if not validate_course(course, courses):
            log_error_and_exit(f"The course code {course} does not exist in {courses_file},"
                               f"An error has occurred while adding {name} to {course}.", log_file)
            return
        modules_input = get_input("Enter modules taken (comma-separated module IDs): ").strip().split(",")
        valid_modules, invalid_modules = validate_modules(modules_input, modules, log_file)
        if invalid_modules:
            log_error_and_exit(
                f"Adding Student: The following module IDs are invalid or not associated with the course '{course}': {', '.join(invalid_modules)}."
            )
            return
        intake_month = get_input("Enter the intake month: ")
        registration_month = get_input("Enter the registration month: ")
        student_data = (f"{name},{student_id},{course},"
                        f"{','.join(valid_modules)},{intake_month},"
                        f"{registration_month},{phone_number},"
                        f"{email},{address},{age}\n")

        # Correcting the append_to_file by ensuring newline format
        with open(file_path, "a", encoding="utf-8") as file:

            # Move the pointer to the end of the file
            file.seek(0, 2)

            # Check if the file already has content
            if file.tell() > 0:
                # Add a newline if not present before appending new data
                file.write("\n")

            file.write(student_data)

        success_message = f"{name} added successfully to {file_path} with ID: {student_id}."
        print(success_message)
        input("Press Enter to continue...")
        log_message(success_message)
    except FileNotFoundError as e:
        log_error_and_exit(f"File not found: {e.filename}. Please check the file path.")
    except Exception as e:
        log_error_and_exit(f"Add student: An error occurred while adding the {name}: {e}")


def get_input(prompt):
    return input(prompt).strip()


def generate_student_id(name):
    """
    Function to generate a student ID,
    Since importing random is not possible, this function will generate a random ID.
    """
    return abs(hash(name)) % 1000000


def filter_records(records, identifier):
    # Check if the identifier is present in each record
    return [record for record in records if identifier not in record]


def remove_student(file_path="student_records.txt", log_file="admin_log.txt"):
    try:
        # Get the identifier from the user
        student_identifier = input("Enter the student name or ID to remove: ").strip()

        # Read the student file
        student_records = read_file(file_path)

        # Filter out the record(s) matching the identifier
        filtered_records = filter_records(student_records, student_identifier)

        # If no records are removed, it means the identifier wasn't found
        if len(filtered_records) == len(student_records):
            print("No matching student found to remove.")
            return

        # Write the updated records back to the file with proper formatting
        with open(file_path, "w", encoding="utf-8") as file:
            for record in filtered_records:
                file.write(record.strip() + "\n")

        success_message = f"{student_identifier} removed successfully."
        print(success_message)
        input("Press Enter to continue...")
        log_message(success_message, log_file)

    except Exception as e:
        error_message = f"An error occurred while removing the {student_identifier}: {e}"
        print(error_message)
        log_message(error_message, log_file)


def print_report(total_courses, total_students):
    print("\n--- University Report ---")
    print(f"Total Courses: {total_courses}")
    print(f"Total Students: {total_students}")
    print("--------------------------")


def generate_report(course_file_path="courses.txt", student_file_path="student_records.txt", log_file="admin_log.txt"):
    try:
        total_courses = len(read_file(course_file_path))
        total_students = len(read_file(student_file_path))
        print_report(total_courses, total_students)
        input("Press Enter to continue...")
        log_message("Report generated successfully.", log_file)

    except Exception as error:
        print(f"An error occurred while generating the report: {error}")
        input("Press Enter to continue...")
        log_message(f"Error generating report: {error}", log_file)


def student_statistics(file_path="student_records.txt"):
    students = read_file(file_path)
    students = [student.strip() for student in students if student.strip()]
    print(f"Total Students: {len(students)}")

    courses = []
    for student in students:
        parts = student.split(",")
        if len(parts) > 2:
            courses.append(parts[2])

    unique_courses = set(courses)
    for course in unique_courses:
        print(f"{course}: {courses.count(course)} student(s)")
        input("Press Enter to continue...")


if __name__ == "__main__":
    print("Admin module loaded.")
