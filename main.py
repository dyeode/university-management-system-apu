def ensure_text_files_exist(file_names):
    for file_name in file_names:
        try:
            # Attempt to open the file in append mode to check if it exists
            with open(file_name, 'r') as file:
                pass  # File exists, do nothing
        except FileNotFoundError:
            # If the file does not exist, create it
            with open(file_name, 'w') as file:
                pass  # Create an empty file
            print(f"Created missing file: {file_name}")

if __name__ == "__main__":
    required_files = [
        "tuition_fees_pending.txt",
        "tuition_fees_paid.txt",
        "fee_receipts.txt",
        "modules_list.txt",
        "courses.txt",
        "student_records.txt",
        "module_student_records.txt",
        "attendance_records.txt",
        "grades_records.txt",
        "registrations.txt",
        "accepted_registrations.txt",
        "declined_registrations.txt"
    ]
    ensure_text_files_exist(required_files)
    from utils.menu import guest_menu
    guest_menu()
