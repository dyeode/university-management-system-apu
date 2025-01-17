def read_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError as e:
        raise e
    except Exception as e:
        raise RuntimeError(f"An error occurred while reading the file: {e}") from e


def overwrite_file(file_path, lines):
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            file.writelines(lines)
        log_message(f"File '{file_path}' overwritten successfully.")
    except Exception as e:
        print(f"An error occurred while overwriting the file: {e}")
        log_message(f"Error overwriting file '{file_path}': {e}")


def append_to_file(file_path, data):
    try:
        with open(file_path, "a", encoding="utf-8") as file:
            if isinstance(data, list):
                file.writelines([f"{line.strip()}\n" for line in data if line.strip()])
            else:
                file.write(f"{data}\n")
        log_message(f"Data appended to file '{file_path}' successfully.")
    except Exception as e:
        print(f"An error occurred while appending to the file: {e}")
        log_message(f"Error appending to file '{file_path}': {e}")


def log_message(message, log_file="filehandling_log.txt"):
    from datetime import datetime
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted_message = f"[{timestamp}] [Log File: {log_file}] {message}"
        with open(log_file, "a", encoding="utf-8") as log:
            log.write(formatted_message + "\n")
    except Exception as e:
        print(f"An error occurred while writing to the log file: {e}")
