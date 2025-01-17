from datetime import datetime

from utils.filehandling import read_file, overwrite_file, append_to_file, log_message


def find_modules_by_lecturer(lecturer_id, modules_file="modules.txt"):
    """
    Retrieves a list of modules assigned to a specific lecturer.
    """
    modules = []
    try:
        # Read the file contents,
        records = read_file(modules_file)
        # Process each record line by line,
        for record in records:
            # Split each record into fields by comma,
            fields = record.strip().split(",")
            # Check if the record has enough fields and the lecturer ID matches
            if len(fields) >= 5 and fields[3] == lecturer_id:
                # Add the module name (field index 1) to the list
                modules.append(fields[1])
    except Exception as e:
        print(f"An error occurred while searching for modules: {e}")
        log_message(f"Error searching for modules for lecturer ID {lecturer_id}: {e}")
    return modules


def view_assigned_modules(modules_file="modules_list.txt"):
    """
    Displays the list of modules assigned to a specific lecturer based on their Lecturer ID.
    """

    # Prompt the user for their Lecturer ID,
    lecturer_id = input("Enter your Lecturer ID: ").strip()
    # Validate the lecturer ID
    if not lecturer_id:
        print("Lecturer ID cannot be empty.")
        return

    # Fetch the modules assigned to the given Lecturer ID
    assigned_modules = find_modules_by_lecturer(lecturer_id, modules_file)
    if assigned_modules:
        # Displays the modules if any are found
        print(f"Modules assigned to Lecturer ID {lecturer_id}:")
        for module in assigned_modules:
            print(f"- {module}")
        log_message(f"Lecturer ID {lecturer_id} viewed their assigned modules.")
        input("Press Enter to continue...")
    else:
        print("No modules found assigned to your Lecturer ID.")
        input("Press Enter to continue...")


def module_exists(module_id, modules_list_file):
    """
    Checks if a module with the given ID exists in the specified modules list file.
    """
    # Read all module records from the file
    modules = read_file(modules_list_file)
    # Check if any record's first field (module ID) matches the given module_id
    return any(module_id == record.split(",")[0] for record in modules if record.strip())


def get_student_name(student_id, student_records_file):
    """
    Retrieves the name of a student based on their ID from the student records file.
    """

    # Read all student records from the file,
    student_records = read_file(student_records_file)

    # Iterating through each record in the file
    for record in student_records:
        if record.strip():
            fields = record.split(",")
            if len(fields) > 1 and fields[1].strip() == student_id:
                return fields[0].strip()

    # Return None if no matching student ID is found
    return None


def student_in_module(module_id, student_id, module_student_file):
    """
    Checks if a specific student is enrolled in a given module.
    The module_student_file should contain records in CSV format.
    Each record is expected to have at least two fields: module ID and student ID, separated by commas.
    """

    # Read all current entries from the module-student records file,
    current_entries = read_file(module_student_file)

    # Check if any record matches both the module_id and student_id
    return any(f"{module_id},{student_id}" in record for record in current_entries if record.strip())


def add_student_to_module(module_student_file="module_student_records.txt",
                          modules_list_file="modules_list.txt",
                          student_records_file="student_records.txt"):
    """
    Adds a student to a specified module if the module and student exist and the student is not already enrolled.
    The module_student_file should contain records in CSV format with fields: module_id, student_id, student_name.
    The student_records_file should contain student details with the student ID in the second field.
    """
    try:
        # Prompt for module and student IDs
        module_id = input("Enter the Module ID: ").strip()
        student_id = input("Enter the Student ID: ").strip()

        # Check if the module exists
        if not module_exists(module_id, modules_list_file):
            print(f"Error: Module ID '{module_id}' not found in the modules list.")
            log_message(f"Failed to add {student_id} to Module '{module_id}' does not exist.")
            return

        # Get the student's name using their ID
        student_name = get_student_name(student_id, student_records_file)
        if not student_name:
            print(f"Error: Student ID '{student_id}' not found in the student records.")
            log_message(f"Failed to add student: Student ID '{student_id}' does not exist.")
            return

        # Check if the student is already enrolled in the module
        if student_in_module(module_id, student_id, module_student_file):
            print(f"Error: The student ID '{student_id}' is already enrolled in the module '{module_id}'.")
            log_message(
                f"Failed to add student: Duplicate entry for Module ID '{module_id}' and Student ID '{student_id}'.")
            return

        # Append the new enrollment record to the file
        append_to_file(module_student_file, f"{module_id},{student_id},{student_name}")
        print("Student added to module successfully.")
        log_message(f"Student {student_id} ({student_name}) added to module {module_id}.")
        input("Press Enter to continue...")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        log_message(f"An error occurred: {str(e)}")
        input("Press Enter to continue...")


def remove_student_from_module(module_student_file="module_student_records.txt",
                               modules_list_file="modules_list.txt"):
    student_id = input("Enter the Student ID to remove: ").strip()
    module_id = input("Enter the Module ID: ").strip()
    if not validate_module(module_id, modules_list_file):
        print(f"Error: Module ID '{module_id}' not found in the modules list.")
        log_message(f"Failed to remove student: Module ID '{module_id}' does not exist.")
        return
    try:
        records = read_file(module_student_file)
        updated_records = [
            record
            for record in records
            if not (record.startswith(f"{module_id},") and record.split(",")[1] == student_id)
        ]
        if len(updated_records) == len(records):
            print(f"No matching record found for Student ID '{student_id}' in Module ID '{module_id}'.")
            log_message(f"No record found: Student ID '{student_id}' in Module ID '{module_id}'.")
        else:
            overwrite_file(module_student_file, [f"{record.strip()}\n" for record in updated_records])
            print("Updated Records:")
            for updated_record in updated_records:
                print(f"{updated_record}\n")
            print("Student removed from the module successfully.")
            log_message(f"Student ID '{student_id}' removed from Module ID '{module_id}'.")
        input("Press Enter to continue...")
    except Exception as e:
        print(f"An error occurred while removing the student from the module: {e}")
        log_message(f"Error removing {student_id} from {module_id}: {e}")
        input("Press Enter to continue...")


def view_enrolled_students(module_student_file="module_student_records.txt"):
    module_id = input("Enter the Module ID: ").strip()
    try:
        records = read_file(module_student_file)
        students = [record.strip().split(",")[1] for record in records if record.startswith(module_id)]
        if students:
            print("Enrolled students:")
            for student in students:
                print(f"- {student}")
                input("Press Enter to continue...")
            log_message(f"Viewed enrolled students for module ID: {module_id}")
        else:
            print("No students found for the module.")
    except Exception as e:
        print(f"An error occurred while viewing enrolled students: {e}")
        log_message(f"Error viewing enrolled students: {e}")


def give_attendance(attendance_file="attendance_records.txt",
                    modules_list_file="modules_list.txt",
                    student_records_file="student_records.txt"):
    try:
        # Input Module ID and validate using `module_exists`
        module_id = input("Enter the Module ID: ").strip()
        if not module_exists(module_id, modules_list_file):  # Check if module exists
            print(f"Error: Module ID '{module_id}' not found in the modules list.")
            log_message(f"Failed to record attendance: Module ID '{module_id}' does not exist.")
            return

        # Input Student ID and validate using `get_student_name`
        student_id = input("Enter the Student ID: ").strip()
        student_name = get_student_name(student_id, student_records_file)  # Get the student's name
        if not student_name:  # No match found
            print(f"Error: Student ID '{student_id}' not found in the student records.")
            log_message(f"Failed to record attendance: Student ID '{student_id}' does not exist.")
            return

        # Input Date and validate format using `datetime`
        date_input = input("Enter the Date (YYYY-MM-DD): ").strip()
        try:
            attendance_date = datetime.strptime(date_input, "%Y-%m-%d").date()  # Parse and validate date
        except ValueError:
            print("Invalid date format. Please enter the date in YYYY-MM-DD format.")
            return

        # Input Attendance Status and validate options
        status = input("Enter Attendance Status (Present/Absent): ").strip().lower()
        if status not in ["present", "absent"]:  # Validate attendance status
            print("Invalid attendance status. Use 'Present' or 'Absent'.")
            return

        # Format and append the attendance record to the file
        attendance_record = f"{module_id},{student_id},{attendance_date},{status}"  # Create record
        append_to_file(attendance_file, attendance_record)  # Append record to file
        print("Attendance recorded successfully.")  # Success message
        input("Press Enter to continue...")

        # Log message for successfully recorded attendance
        log_message(f"Attendance recorded for student {student_id} ({student_name}) in module {module_id}.")

    except Exception as error:  # Catch and log unexpected errors
        print(f"An error occurred while recording attendance: {error}")
        log_message(f"Error recording attendance: {error}")


def parse_and_validate_record(record, module_id, min_fields):
    """This pretty much parses and validates a single record,
    I found this on closed thread in stackoverflow."""
    fields = record.strip().split(",")
    if len(fields) < min_fields:
        raise ValueError(f"Invalid record format: {record}")
    return fields if fields[0].strip() == module_id else None


def validate_student(student_id, student_records_file="student_records.txt"):
    """Check if student_id exists in student_records.txt."""
    records = read_file(student_records_file)
    for record in records:
        fields = record.strip().split(",")
        if len(fields) > 1 and fields[1].strip() == student_id:
            return True
    return False


def validate_module(module_id, modules_list_file="modules_list.txt"):
    """Check if module_id exists in modules_list.txt."""
    records = read_file(modules_list_file)
    for record in records:
        fields = record.strip().split(",")
        if fields[0].strip() == module_id:
            return True
    return False


def get_total_classes(module_id, modules_list_file="modules_list.txt"):
    """Fetch number of classes to be attended for the module."""
    records = read_file(modules_list_file)
    for record in records:
        fields = record.strip().split(",")
        if fields[0].strip() == module_id:
            return int(fields[5])  # Index 5 is number of classes to attend
    return 0


def calculate_attendance(student_id, module_id, attendance_file="attendance_records.txt"):
    """Calculate attendance percentage."""
    try:
        records = read_file(attendance_file)
        attended_classes = 0
        total_classes_attended = 0

        for record in records:
            fields = record.strip().split(",")
            if len(fields) == 4 and fields[0] == module_id and fields[1] == student_id:
                if fields[3].strip().lower() == "present":
                    attended_classes += 1  # Increment for each present
                total_classes_attended += 1  # Increment for all classes attended by the student

        module_classes = get_total_classes(module_id)
        if module_classes == 0:
            print(f"Module {module_id} does not have valid class data.")
            return

        # Calculate percentage
        attendance_percentage = (attended_classes / module_classes) * 100 if module_classes > 0 else 0

        print(f"Attendance for Student ID {student_id} in Module ID {module_id}:")
        print(f"Attended {attended_classes} out of {module_classes} classes.")
        print(f"Attendance Percentage: {attendance_percentage:.2f}%")

    except Exception as e:
        print(f"An error occurred while calculating attendance: {e}")


def view_attendance():
    student_id = input("Enter Student ID: ").strip()
    module_id = input("Enter Module ID: ").strip()

    if not validate_student(student_id):
        print(f"Error: Student ID '{student_id}' not found in records.")
        return

    if not validate_module(module_id):
        print(f"Error: Module ID '{module_id}' not found in modules list.")
        return

    calculate_attendance(student_id, module_id)


def add_grade(grades_file="grades_records.txt",
              student_records_file="student_records.txt",
              modules_list_file="modules_list.txt",
              module_student_file="module_student_records.txt"):
    try:
        # Input Student ID and validate
        student_id = input("Enter the Student ID: ").strip()
        if not get_student_name(student_id, student_records_file):
            print(f"Error: Student ID '{student_id}' not found in the student records.")
            log_message(f"Failed to add grade: Student ID '{student_id}' does not exist.")
            return

        # Input Module ID and validate
        module_id = input("Enter the Module ID: ").strip()
        if not module_exists(module_id, modules_list_file):
            print(f"Error: Module ID '{module_id}' not found in the modules list.")
            log_message(f"Failed to add grade: Module ID '{module_id}' does not exist.")
            return

        # Ensure the student is enrolled in the module
        if not student_in_module(module_id, student_id, module_student_file):
            print(f"Error: Student ID '{student_id}' is not enrolled in Module ID '{module_id}'.")
            log_message(
                f"Failed to add grade: Student ID '{student_id}' not enrolled in Module ID '{module_id}'.")
            return

        # Input Grade Percentage and Validate
        try:
            grade_percentage = float(input("Enter the Grade Percentage: ").strip())
            if grade_percentage < 0 or grade_percentage > 100:
                print("Grade percentage must be between 0 and 100.")
                return
        except ValueError:
            print("Invalid grade percentage. Please enter a numeric value.")
            return

        # Determine Distinction
        if 30 <= grade_percentage < 45:
            distinction = "D-"
        elif 45 <= grade_percentage < 55:
            distinction = "D+"
        elif 55 <= grade_percentage < 60:
            distinction = "C-"
        elif 60 <= grade_percentage < 65:
            distinction = "C+"
        elif 65 <= grade_percentage < 70:
            distinction = "B-"
        elif 70 <= grade_percentage < 80:
            distinction = "B+"
        elif 80 <= grade_percentage < 90:
            distinction = "A-"
        elif 90 <= grade_percentage <= 100:
            distinction = "A+"
        else:
            distinction = "Fail"

        # Save the Grade Record
        grade_record = f"{student_id},{module_id},{grade_percentage},{distinction}"
        append_to_file(grades_file, grade_record)
        print(f"Grade successfully added: {distinction}")
        log_message(f"Grade added for student {student_id} in module {module_id}: {grade_percentage}%, {distinction}")

    except Exception as e:
        print(f"An error occurred while adding the grade: {str(e)}")
        log_message(f"Error adding grade: {e}")


def view_grades(grades_file="grades_records.txt"):
    module_id = input("Enter the Module ID: ").strip()
    if not module_id:
        print("Module ID cannot be empty.")
        return
    try:
        records = read_file(grades_file)
        if not records:
            print("The grades file is empty or missing.")
            input("Press Enter to continue...")
            log_message("Attempt to view grades failed: empty or missing file")
            return
        grades = []
        for record in records:
            try:
                fields = record.strip().split(",")
                if len(fields) < 4:
                    raise ValueError(f"Invalid record format: {record}")
                if fields[1].strip() == module_id:
                    grades.append(fields)
            except ValueError as ve:
                log_message(f"Skipped invalid record: {ve}")
        if grades:
            print(f"Grades for Module ID: {module_id}")
            for grade in grades:
                print(f"Student ID: {grade[0]}, Grade: {grade[2]}%, Distinction: {grade[3]}")
            input("Press Enter to continue...")
            log_message(f"Viewed grades for module ID: {module_id}")
        else:
            print("No grades found for the module.")
            input("Press Enter to continue...")
            log_message(f"No grades found for module ID: {module_id}")
    except FileNotFoundError:
        print(f"Grades file '{grades_file}' not found.")
        input("Press Enter to continue...")
        log_message(f"Grades file not found: {grades_file}")
    except Exception as e:
        print(f"An unexpected error occurred while viewing grades: {e}")
        log_message(f"Unexpected error viewing grades: {e}")


if __name__ == "__main__":
    print("Lecturer module loaded.")
