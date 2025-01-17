from utils.filehandling import read_file, log_message

def search_course(file_path="courses.txt"):
    try:
        # Read the list of available courses from the file
        courses = read_file(file_path)
        if not courses:
            print(f"No courses available in the file '{file_path}'.")
            input("Press Enter to continue...")
            return
    except FileNotFoundError:
        print(f"The file '{file_path}' does not exist.")
        input("Press Enter to continue...")
        log_message(f"FileNotFoundError: The file '{file_path}' does not exist.")
        return

    # Prompt the user to input the search term
    search_term = input("Enter the course name to search: ").strip().lower()

    # Search courses and filter by name (index 1)
    results = []
    for course in courses:
        parts = course.split(",")
        if len(parts) > 1 and search_term in parts[1].strip().lower():
            results.append(course.strip())

    if results:
        print(f"Matching courses found ({len(results)}):")
        for course in results:
            print(course)
            input("Press Enter to continue...")
    else:
        # No exact matches, suggest similar names
        course_names = [course.split(",")[1].strip() for course in courses if len(course.split(",")) > 1]
        suggestions = []
        for course_name in course_names:
            if search_term in course_name.lower() or course_name.lower().startswith(search_term[:2]):
                suggestions.append(course_name)

        if suggestions:
            print(f"Sorry, no exact matches were found for '{search_term}'. Did you mean:")
            for suggestion in suggestions[:3]:  # Limit to 3 suggestions
                print(f" - {suggestion}")
                input("Press Enter to continue...")
        else:
            print(f"Sorry, no matches or suggestions were found for '{search_term}'.")
            input("Press Enter to continue...")

def search_student_in_module(module_records_file="module_student_records.txt", student_records_file="student_records.txt", modules_file="modules_list.txt"):
    try:
        module_id = input("Enter the module ID: ").strip()
        try:
            modules = read_file(modules_file)
        except FileNotFoundError:
            print(f"Error: '{modules_file}' not found.")
            input("Press Enter to continue...")
            return
        valid_module = None
        for module in modules:
            fields = module.split(",")
            if fields[0].strip() == module_id:
                valid_module = fields[1].strip()
                break
        if not valid_module:
            print(f"Module ID {module_id} not found.")
            input("Press Enter to continue...")
            return
        print(f"Module: {valid_module}")

        student_id = input("Enter the student ID: ").strip()
        try:
            students = read_file(student_records_file)
        except FileNotFoundError:
            print(f"Error: '{student_records_file}' not found.")
            input("Press Enter to continue...")
            return
        valid_student = any(student.split(",")[1].strip() == student_id for student in students)
        if not valid_student:
            print(f"Student ID {student_id} not found.")
            input("Press Enter to continue...")
            return

        try:
            records = read_file(module_records_file)
        except FileNotFoundError:
            print(f"Error: '{module_records_file}' not found.")
            input("Press Enter to continue...")
            return

        matches = [record for record in records if record.startswith(f"{module_id},") and student_id in record]
        if matches:
            print(f"Student ID {student_id} is enrolled in module {module_id}:")
            for match in matches:
                print(match.strip())
                input("Press Enter to continue...")
        else:
            print(f"Student ID {student_id} not found in module {module_id}.")
            input("Press Enter to continue...")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def get_valid_student_id(student_records_file="student_records.txt"):
    while True:
        student_id = input("Enter the student ID: ").strip()

        if not student_id:
            print("Invalid student ID. Please try again.")
        elif not student_id.isalnum():
            print("Student ID must be alphanumeric. Please try again.")
        else:
            try:
                # Open the student records file and validate the student ID
                with open(student_records_file, "r") as file:
                    for line in file:
                        # Ensure the line is well-formed before splitting
                        line = line.strip()
                        if line:
                            record = line.split(",")
                            if len(record) > 1 and record[1].strip() == student_id:
                                return student_id  # Valid student_id found
                print("Student ID not found in the student records. Please try again.")
            except FileNotFoundError:
                print(f"Error: The file '{student_records_file}' does not exist.")
                print("Please make sure the file exists and try again.")
                return None  # Exit gracefully if the file is missing
            except Exception as e:
                print(f"An error occurred: {e}")
                return None  # Handle unexpected errors gracefully