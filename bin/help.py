def help():
    help = "```\n"

    ## Basic command
    help += "last_command: Give the last command used.\n"
    help += "url: Give the url for flowintel-cm instance.\n"

    ## Case command
    help += "create_case: Create a new case.\n\t!create_case New case name\n"
    help += "case_title: Search a case by title.\n\t!case_title title to search\n"
    help += "case_id: Get a case by its id.\n\t!case_id 1\n"
    help += "modify_title: Modify a title of a case:\n\t!modify_title case_id new title\n"
    help += "modify_description: Modify a description of a case:\n\t!modify_description case_id new description\n"
    help += "complete_case: Mark a case as Finished.\n\t!complete_case case_id\n"

    ## Task command
    help += "create_task: Create a new task in a case.\n\t!create_task case_id task title\n"
    help += "my_assignment: Give task assign to user.\n\t!my_assignment page\n"

    help += "```"
    return help
