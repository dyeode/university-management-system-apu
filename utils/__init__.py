from .admin import (
    add_course,
    remove_course,
    update_course,
    add_student,
    remove_student,
    print_report,
    generate_report,
    student_statistics
)

from .filehandling import read_file, overwrite_file, append_to_file, log_message

from .lecturer import (
    view_assigned_modules,
    add_student_to_module,
    remove_student_from_module,
    view_enrolled_students,
    give_attendance,
    view_attendance,
    view_grades
)

from .login import login

from .menu import guest_menu
from .utility import search_student_in_module, search_course, get_valid_student_id
