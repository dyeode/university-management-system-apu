from datetime import datetime

from utils.filehandling import append_to_file, read_file, overwrite_file, log_message
from utils.utility import get_valid_student_id


def calculate_total_from_records(file_path, record_type, log_file_path):
    """
    Calculates the total amount from a records file.
    Records with invalid formats or non-numeric amounts are logged and skipped.
    """

    # Initializing the total amount at start
    total_amount = 0.0
    try:
        with open(file_path, "r") as file:
            for line in file:
                # Remove leading/trailing whitespace
                line = line.strip()
                if line:
                    split_record = line.split(",", maxsplit=3 if record_type == "paid" else 2)

                    # Ensure the record has at least two fields
                    if len(split_record) >= 2:
                        try:
                            # Add the amount to the total
                            total_amount += float(split_record[1])
                        except ValueError:
                            log_message(f"Invalid {record_type} amount skipped: {line}", log_file_path)
                    else:
                        log_message(f"Invalid {record_type} record skipped: {line}", log_file_path)
    except FileNotFoundError:
        log_message(f"File not found: {file_path}. Unable to process {record_type} records.", log_file_path)
    return total_amount


def display_financial_summary_details(total_paid, total_outstanding):
    print("\nFinancial Summary:\n" + "-" * 50)
    print(f"Total Fees Collected: {total_paid:.2f}")
    print(f"Total Outstanding Fees: {total_outstanding:.2f}")
    print("-" * 50)
    input("Press Enter to continue...")


def view_financial_summary(pending_file_path="tuition_fees_pending.txt",
                           paid_file_path="tuition_fees_paid.txt",
                           log_file_path="accountant_log.txt"):
    """
    Displays a financial summary of total fees collected and outstanding.
    """
    try:
        # Calculates the total fees collected from the paid file
        total_paid = calculate_total_from_records(paid_file_path, "paid", log_file_path)

        # Calculates total outstanding fees from the pending file
        total_outstanding = calculate_total_from_records(pending_file_path, "pending", log_file_path)

        # Displays the financial summary to the user
        display_financial_summary_details(total_paid, total_outstanding)
        log_message(f"Financial Summary: Collected - {total_paid:.2f}, "
                    f"Outstanding - {total_outstanding:.2f}, ", log_file_path)
    except Exception as e:
        print(f"Error: An unexpected issue occurred: {e}")
        log_message(f"Unexpected error in view_financial_summary: {e}", log_file_path)


def generate_receipt(student_id, amount_paid, date_of_payment, receipt_file="fee_receipts.txt",
                     log_file="accountant_log.txt"):
    """
    Generates the receipt for the given student ID using the given amount and date of payment.
    """
    receipt_entry = f"{student_id},{amount_paid},{date_of_payment}\n"
    try:
        append_to_file(receipt_file, receipt_entry)
        print(f"Receipt generated and saved for student {student_id}.")
        input("Press Enter to continue...")
        log_message(f"Receipt generated for student {student_id}: {receipt_entry.strip()}", log_file)
    except Exception as e:
        print(f"Failed to generate receipt: {e}")
        input("Press Enter to continue...")
        log_message(f"Receipt generation failed for student {student_id}: {e}", log_file)


def get_valid_amount_paid():
    """Prompt for and validate the amount paid."""
    while True:
        try:
            amount_paid = float(input("Enter the amount paid: "))
            if amount_paid <= 0:
                print("Amount must be greater than zero. Please try again.")
            else:
                return amount_paid
        except ValueError:
            print("Invalid input. Please enter a numeric value.")


def prompt_user_for_action():
    print("Do you want to 1) Add student to pending record or 2) Mark student as paid?")
    choice = input("Enter your choice (1/2): ").strip()
    if choice not in ("1", "2"):
        print("Invalid choice. Please restart and enter either 1 or 2.")
        return None
    return choice


def remove_empty_lines(file_path, log_file_path):
    """Removes empty lines from a given file."""
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()  # Read all lines

        with open(file_path, "w") as file:
            for line in lines:
                if line.strip():  # Keep lines that are not empty
                    file.write(line)

        log_message(f"Empty lines removed from '{file_path}'.", log_file_path)
    except FileNotFoundError:
        log_message(f"File not found: {file_path}. Could not remove empty lines.", log_file_path)
    except Exception as e:
        log_message(f"Unexpected error while removing empty lines from {file_path}: {e}", log_file_path)


def add_student_to_pending_record(student_id, pending_file, log_file):
    """Add a student's pending fees record and ensure no empty lines in the pending file."""
    pending_amount = get_valid_amount_paid()
    date_of_update = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pending_record_entry = f"{student_id},{pending_amount},{date_of_update}\n"

    # Append the record to the file
    append_to_file(pending_file, pending_record_entry)

    # Remove empty lines from the file to maintain consistency
    remove_empty_lines(pending_file, log_file)

    # Notify and log the operation
    print(f"Student {student_id} added to pending tuition fees record.")
    log_message(f"Student {student_id} added to pending record.", log_file)


def process_pending_to_paid(student_id, pending_file, paid_file, log_file):
    updated_amount = get_valid_amount_paid()
    date_of_update = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    paid_record_entry = f"{student_id},{updated_amount},{date_of_update},paid\n"

    # Read the pending records and find the student's record
    pending_records = read_file(pending_file)  # Assuming this returns a list of lines
    updated_pending_records = []
    record_found = False

    for record in pending_records:
        record = record.strip()
        if record.startswith(student_id + ","):
            record_found = True
        else:
            updated_pending_records.append(record)

    if not record_found:
        print(f"No pending record found for student {student_id}.")
    else:
        # Update the pending file by removing the transferred record
        overwrite_file(pending_file, "\n".join(updated_pending_records) + "\n")
        print(f"Removed student {student_id} from pending records.")

    # Add the record to the paid file
    append_to_file(paid_file, paid_record_entry)

    # Remove any empty lines after appending the record
    remove_empty_lines(paid_file, log_file)

    print(f"Tuition fees recorded as paid for student {student_id}.")
    log_message(f"Tuition fees paid record updated for student {student_id}.", log_file)

    # Generate a receipt for the transaction
    generate_receipt(student_id, updated_amount, date_of_update, log_file=log_file)


def handle_file_access_error(error, log_file):
    print(f"An error occurred while accessing files: {error}")
    log_message(f"File error: {error}", log_file)


def handle_unexpected_program_error(error, log_file):
    print(f"An unexpected error occurred: {error}")
    log_message(f"Unexpected error: {error}", log_file)


def record_tuition_fees_to_file(pending_file="tuition_fees_pending.txt",
                                paid_file="tuition_fees_paid.txt",
                                log_file="accountant_log.txt"):
    try:
        # Get the user's choice of action
        choice = prompt_user_for_action()
        if not choice:
            return  # Exit if the choice was invalid

        # Collect the student ID
        student_id = get_valid_student_id()

        if choice == "1":
            # Add the student to the pending record
            add_student_to_pending_record(student_id, pending_file, log_file)
        elif choice == "2":
            # Mark the student's tuition fees as paid
            process_pending_to_paid(student_id, pending_file, paid_file, log_file)

    except FileNotFoundError as e:
        handle_file_access_error(e, log_file)
    except Exception as e:
        handle_unexpected_program_error(e, log_file)


def view_outstanding_fees(pending_file_path="tuition_fees_pending.txt", log_file_path="accountant_log.txt"):
    try:
        # Prompt user for sorting preference
        print("How would you like to sort the records?")
        print("1. By Amount")
        print("2. By Date")
        print("3. No Sorting")
        sort_choice = input("Enter your choice (1/2/3): ").strip()
        if sort_choice == "1":
            sort_by = "amount"
        elif sort_choice == "2":
            sort_by = "date"
        elif sort_choice == "3":
            sort_by = None
        else:
            print("Invalid choice. Defaulting to no sorting.")
            sort_by = None
        # Read records from file and process line by line
        fee_records = []
        with open(pending_file_path, "r") as file:
            for line in file:
                line = line.strip()
                if line:
                    split_record = line.split(",", maxsplit=2)
                    if len(split_record) == 3:
                        student_id, amount, updated_at = split_record
                        fee_records.append((student_id, float(amount), updated_at))
                    else:
                        log_message(f"Invalid record skipped: {line}", log_file_path)
                        print(f"Skipping invalid record: {line}")
                        input("Press Enter to continue...")
        # Check if no records are found
        if not fee_records:
            print("No outstanding fees found.")
            input("Press Enter to continue...")
            log_message("No outstanding fees to report.", log_file_path)
            return
        # Sorting logic
        if sort_by == "amount":
            fee_records.sort(key=lambda record: record[1])  # Sort by amount
        elif sort_by == "date":
            fee_records.sort(key=lambda record: datetime.strptime(record[2], "%Y-%m-%d %H:%M:%S"))  # Sort by date
        # Display header
        print("\nOutstanding Fees:\n" + "-" * 50)
        # Display and calculate totals
        total_outstanding = 0.0
        for student_id, amount, updated_at in fee_records:
            print(f"Student ID: {student_id}, Amount Due: {amount:.2f}, Last Updated: {updated_at}")
            total_outstanding += amount
        # Print totals
        print("-" * 50)
        print(f"Total Outstanding Amount: {total_outstanding:.2f}")
        input("Press Enter to continue...")
        # Log success
        log_message(f"Outstanding fees listed successfully: {len(fee_records)} records found.", log_file_path)
        log_message(f"Total Outstanding Amount: {total_outstanding:.2f}", log_file_path)
    except FileNotFoundError as e:
        print(f"Error: Could not find the file '{pending_file_path}': {e}")
        log_message(f"File not found: {pending_file_path}: {e}", log_file_path)
    except Exception as e:
        print(f"Error: An unexpected issue occurred: {e}")
        log_message(f"Unexpected error in view_outstanding_fees: {e}", log_file_path)


if __name__ == "__main__":
    print("Accountant Module loaded.")
