from utils.filehandling import read_file, log_message


def search_course(file_path="courses.txt"):
    """
        Searches for a course by name in a file and displays matching results or suggestions.

        The function reads course information from the courses file, searches for matches based
        on a user-provided search term, and displays the results. If no matches are found, it
        provides up to three suggestions based on partial matches or similar course names.
    """
    try:
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

    search_term = input("Enter the course name to search: ").strip().lower()

    results = []
    for course in courses:
        parts = course.split(",")
        if len(parts) > 1 and search_term in parts[1].strip().lower():
            """
            Checks if the course has more than one part and whether
            the search term is in the second part (case-insensitive).
            """
            results.append(course.strip())

    if results:
        print(f"Matching courses found ({len(results)}):")
        for course in results:
            print(course)
            input("Press Enter to continue...")
    else:
        """
        Extracts course names from courses and adds them to suggestions if they
        match the search term or start with its first two characters.
        """
        course_names = [course.split(",")[1].strip() for course in courses if len(course.split(",")) > 1]
        suggestions = []
        for course_name in course_names:
            if search_term in course_name.lower() or course_name.lower().startswith(search_term[:2]):
                suggestions.append(course_name)

        if suggestions:
            print(f"Sorry, no exact matches were found for '{search_term}'. Did you mean:")
            for suggestion in suggestions[:3]:
                # Displays up to 3 suggestions if available,
                print(f" - {suggestion}")
                input("Press Enter to continue...")
        else:
            # otherwise informs the user that no matches or suggestions were found.
            print(f"Sorry, no matches or suggestions were found for '{search_term}'.")
            input("Press Enter to continue...")


def search_student_in_module(module_records_file="module_student_records.txt",
                             student_records_file="student_records.txt", modules_file="modules_list.txt"):
    try:
        # Searches for a specific student in a specific module by verifying the module ID, student ID,
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
            # and matching records in the module records file. Handles file reading and provides appropriate feedback on results.
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
        # Prompts the user for a valid alphanumeric student ID
        elif not student_id.isalnum():
            print("Student ID must be alphanumeric. Please try again.")
        else:
            try:
                with open(student_records_file, "r") as file:
                    for line in file:
                        line = line.strip()
                        if line:
                            record = line.split(",")
                            # and checks if it exists in the student records file.
                            if len(record) > 1 and record[1].strip() == student_id:
                                return student_id
                print("Student ID not found in the student records. Please try again.")
            except FileNotFoundError:
                print(f"Error: The file '{student_records_file}' does not exist.")
                print("Please make sure the file exists and try again.")
                return None
            except Exception as e:
                print(f"An error occurred: {e}")
                return None
