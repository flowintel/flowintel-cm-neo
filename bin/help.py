def help():
    help = "```\n"

    help += "help: Show this output.\n"
    help += "help_case: Show command for case part.\n"
    help += "help_task: Show command for task part.\n"

    ## Basic command
    help += "last_command: Give the last command used.\n"
    help += "url: Give the url for flowintel-cm instance.\n"

    ## Case command
    help += help_case(False)

    ## Task command
    help += help_task(False)

    help = "```\n"
    return help


def help_case(standalone=True):
    ## Case command
    help = ""
    if standalone:
        help = "```\n"

    help += "create_case: Create a new case.\n\t!create_case New case name\n"
    help += "case_title: Search a case by title.\n\t!case_title title to search\n"
    help += "case: Get a case by its id.\n\t!case_id case_id\n"
    help += "modify_title: Modify a title of a case.\n\t!modify_title case_id new title\n"
    help += "modify_description: Modify a description of a case:\n\t!modify_description case_id new description\n"
    help += "complete_case: Mark a case as Finished.\n\t!complete_case case_id\n"
    help += "case_tasks: List all tasks for a case.\n\t!case_tasks case_id\n"
    help += "case_note: Get note of a case.\n\t!case_note case_id\n"
    help += "case_modify_note: Modify note of a case.\n\t!case_modify_note case_id new note\n"
    help += "case_all_notes: Get notes from all tasks in a case.\n\t!case_all_notes case_id\n"
    help += "case_all_users: Get list of user that can be assign.\n\t!case_all_users case_id\n"
    help += "list_status: Get list of status apllicable to a case.\n\t!list_status\n"
    help += "case_status: Get current status of the case.\n\t!case_status case_id\n"
    help += "case_modify_status: Modify status of the case.\n\t!case_modify_status case_id status_id\n"

    if standalone:
        help = "```\n"

    return help


def help_task(standalone=True):
    ## Task command
    help = ""
    if standalone:
        help = "```\n"

    help += "create_task: Create a new task in a case.\n\t!create_task case_id task title\n"
    help += "task: Get a task by its id.\n\t!task_id task_id\n"
    help += "my_assignment: Give task assign to user.\n\t!my_assignment page\n"
    help += "modify_title: Modify a title of a task.\n\t!modify_title task_id new title\n"
    help += "modify_description: Modify a description of a task.\n\t!modify_description task_id new description\n"
    help += "complete_task: Mark a task as Finished.\n\t!complete_task task_id\n"
    help += "create_note: Create a note for a task.\n\t!create_note task_id new note\n"
    help += "task_get_all_notes: Get all notes for a task.\n\t!task_get_all_notes task_id\n"
    help += "task_get_note: Get a note for a task.\n\t!task_get_note task_id\n"
    help += "task_modify_note: Modify a note for a task.\n\t!task_modify_note task_id new note\n"
    help += "delete_note: Delete a note for a task.\n\t!delete_note task_id\n"
    help += "take_task: Assign current user to the task.\n\t!take_task task_id\n"
    help += "remove_assignment: Remove assignment of current user on the task.\n\t!remove_assignment task_id\n"
    help += "task_status: Get current status of the task.\n\t!task_status task_id\n"
    help += "task_modify_status: Modify status of the task.\n\t!task_modify_status task_id status_id\n"

    if standalone:
        help = "```\n"

    return help