from crontab import CronTab
from sys import argv


argument = None

time = None
command = None
comment = None
user = None
tab_file = None
delete_all = False


def fail(prompt):
    print(prompt)
    exit(1)


def get_args():
    global argument
    global time
    global command
    global comment
    global user
    global tab_file
    global delete_all

    i = 0
    while i < len(argv):
        if argv[i][:2] == "--":
            if argv[i] == "--time":
                time = argv[i + 1]
                i += 2
            elif argv[i] == "--command":
                command = argv[i + 1]
                i += 2
            elif argv[i] == "--comment":
                comment = argv[i + 1]
                i += 2
            elif argv[i] == "--user":
                user = argv[i + 1]
                i += 2
            elif argv[i] == "--tabfile":
                tab_file = argv[i + 1]
                i += 2
            elif argv[i] == "--all":
                delete_all = True
                i += 1
            else:
                fail("\"" + argv[i] + "\" is not a valid option")
        else:
            if argv[i] == "create":
                argument = argv[i]
            elif argv[i] == "delete":
                argument = argv[i]
            else:
                fail("\"" + argv[i] + "\" is an unknown argument")


def find_job(tab, time=None, command=None, comment=None):
    jobs = list()
    for job in tab:
        if time is not None and job != time:
            continue
        if command is not None and job.command != command:
            continue
        if comment is not None and job.comment != comment:
            continue
        jobs.append(job)
    return jobs


def get_crontab():
    if user is not None and tab_file is not None:
        fail("Both user and tabfile options cannot be set")

    if user is not None:
        return CronTab(user)
    elif tab_file is not None:
        return CronTab(tab_file)
    return CronTab()


def write_crontab(tab):
    if tab_file is not None:
        tab.write(tab_file)
    elif user is not None:
        tab.write_to_user(user=user)
    else:
        tab.write()


def create_crontab():
    if command is None or time is None:
        fail("Time and command options must be set")

    tab = get_crontab()
    job = tab.new(command, comment, user)
    job.setall(time)
    write_crontab(tab)
    return 0


def delete_crontab():
    if time is None and command is None and comment is None:
        fail("No search criteria specified (time, command, comment)")

    tab = get_crontab()
    if delete_all:
        if command is not None:
            tab.remove_all(command)
        if time is not None:
            tab.remove_all(time=time)
        if comment is not None:
            tab.remove_all(comment=comment)
    else:
        jobs = find_job(tab, time, command, comment)
        for job in jobs:
            tab.remove(job)
    write_crontab(tab)
    return 0


def main_procedure():
    exit_status = 1
    get_args()
    if argument == "create":
        exit_status = create_crontab()
    elif argument == "delete":
        exit_status = delete_crontab()
    exit(exit_status)

main_procedure()
