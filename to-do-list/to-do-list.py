def add_task():
    time = input("Enter time: ")
    task = input("Enter task: ")

    with open("tasks.txt", "a") as file:
        file.write(f"{time} - {task}\n")

    print("Task added successfully.")


def show_tasks():
    try:
        with open("tasks.txt", "r") as file:
            tasks = file.readlines()

        if len(tasks) == 0:
            print("No tasks found.")
            return

        print("\nYOUR TASKS")
        print("----------")

        for i, task in enumerate(tasks, start=1):
            print(f"{i}. {task.strip()}")

    except FileNotFoundError:
        print("No task file yet.")


def remove_task():
    try:
        with open("tasks.txt", "r") as file:
            tasks = file.readlines()

        show_tasks()

        num = int(input("Enter task number to remove: "))

        if num < 1 or num > len(tasks):
            print("Invalid task number.")
            return

        tasks.pop(num - 1)

        with open("tasks.txt", "w") as file:
            file.writelines(tasks)

        print("Task removed.")

    except:
        print("Error removing task.")


def menu():
    while True:
        print("\nTASK MANAGER")
        print("1 - Add Task")
        print("2 - Show Tasks")
        print("3 - Remove Task")
        print("4 - Exit")

        try:
            choice = int(input("Select option: "))

            if choice == 1:
                add_task()

            elif choice == 2:
                show_tasks()

            elif choice == 3:
                remove_task()

            elif choice == 4:
                print("Goodbye.")
                break

            else:
                print("Invalid choice.")

        except:
            print("Please enter a number.")


menu()

        