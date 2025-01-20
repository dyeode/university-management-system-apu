from utils.filehandling import read_file


def view_available_modules(file_path="modules_list.txt"):
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()  # Read all lines into a list
            if not lines:
                print("The module list is empty.")
                input("Press enter to continue...")
                return
            print("Module ID - Module Name:")
            for line in lines:
                split_line = line.strip().split(",")  # Split the line by ","
                if len(split_line) >= 2:  # Ensure there are at least two elements
                    module_id = split_line[0].strip()  # Module ID
                    module_name = split_line[1].strip()  # Module Name
                    print(f"{module_id} - {module_name}")
                else:
                    print(f"Invalid line skipped: {line}")  # Handle invalid/malformed records
            # Add a pause here to allow users to view the output before proceeding
            input("\nPress Enter to return to the menu...")
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        input("Press enter to continue...")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        input("Press enter to continue...")


def add_student_module(modules_file="modules_list.txt", students_file="student_records.txt",
                       records_file="module_student_records.txt"):
    try:
        module_id = input("Enter the module ID: ")
        student_id = input("Enter the student ID: ")
        modules = read_file(modules_file)
        students = read_file(students_file)
        module_exists = False
        for module in modules:
            fields = module.split(",")
            if len(fields) > 0 and module_id == fields[0]:  # Match module_id with the first field
                module_exists = True
                break
        if not module_exists:
            print(f"Error: The module ID '{module_id}' does not exist in {modules_file}.")
            return
        student_match = None
        for student in students:
            fields = student.split(",")
            if len(fields) > 1 and student_id == fields[1].strip():  # Match student_id with the second field
                student_match = student
                break
        if not student_match:
            print(f"Error: The student ID '{student_id}' does not exist in {students_file}.")
            return
        student_name = student_match.split(",")[0].strip()
        with open(records_file, "a", encoding="utf-8") as file:
            record = f"{module_id},{student_id},{student_name}\n"
            file.write(record)
        print(f"Successfully added student '{student_name}' with ID '{student_id}' to module '{module_id}'.")

    except FileNotFoundError as e:
        print(f"File not found: {e.filename}. Please make sure it exists and is accessible.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def unenroll_from_module(file_path="module_student_records.txt"):
    """Unenroll a student from the given module."""
    try:
        student_id = input("Enter the student ID: ")
        module_id = input("Enter the module ID: ")
        with open(file_path, "r") as file:
            lines = file.readlines()
        updated_lines = []
        record_found = False
        for line in lines:
            fields = line.strip().split(",")  # Split the line by comma
            if len(fields) >= 2:  # Ensure the line has at least module_id and student_id
                file_module_id = fields[0].strip()  # module_id is at index 0
                file_student_id = fields[1].strip()  # student_id is at index 1
                # Match both module_id and student_id
                if file_module_id == module_id and file_student_id == str(student_id):
                    record_found = True  # Mark record as found, exclude it from updated lines
                else:
                    updated_lines.append(line.strip())  # Keep non-matching lines
            else:
                print(f"Skipping malformed line: {line.strip()}")  # Handle malformed lines (optional)
        if record_found:
            with open(file_path, "w") as file:
                file.write("\n".join(updated_lines) + "\n")  # Write updated lines back to the file
            print(f"Successfully unenrolled student {student_id} from module {module_id}.")
        else:
            print(f"No record found for student {student_id} in module {module_id}.")
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    print("Student Module loaded.")
