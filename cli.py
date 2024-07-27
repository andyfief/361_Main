import requests
import os
import platform

BASE_URL = "http://127.0.0.1:5000/tasks"

def clear_screen():
    # Check the platform and run the appropriate command
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def print_menu():
    print("1. Add Task")
    print("2. Remove Task")
    print("3. Edit Task")
    print("4. Home")
    print("5. Exit")
    
def add_task():
    print("-----------------------\n"
          "Let's add another task!\n"
          "-----------------------")
    title = input("Enter task title: ")
    description = input("Enter task description: ")
    task = {"title": title, "description": description}

    while(True):
        choice = int(input("1. Save\n2. Cancel\n"))
        if(choice == 1):
            response = requests.post(BASE_URL, json=task)
            break
        if(choice == 2):
            clear_screen()
            return
        else:
            clear_screen()
            print("Please enter a valid choice.")
    clear_screen()     
    print(response.json())

def remove_task():
    print("---------------------------------\n"
          "Finished up? Let's remove a task.\n"
          "---------------------------------")
    view_tasks()
    task_id = input("Enter task ID to remove: ")
    
    while(True):
        try:
            choice = int(input(f"Are you sure you want to delete task {task_id}? \n1. Yes\n2. No\n"))
            if choice == 1:
                response = requests.delete(f"{BASE_URL}/{task_id}")
                clear_screen()
                print(response.json())
                break
            elif choice == 2:
                clear_screen()
                return
            else:
                clear_screen()
                print("Please enter a valid choice.")
        except ValueError:
            clear_screen()
            print("Please enter a number.")

def edit_task():
    print("-----------------------------\n"
          "Let's move some things around.\n"
          "-----------------------------")
    view_tasks()
    task_id = input("Enter task ID to edit: ")
    title = input("Enter new task title: ")
    description = input("Enter new task description: ")
    task = {"title": title, "description": description}
    while(True):
        choice = int(input("Save changes?\n1. Yes\n2. No\n"))
        if(choice == 1):
            response = requests.put(f"{BASE_URL}/{task_id}", json=task)
            break
        if(choice == 2):
            clear_screen()
            return
        else:
            clear_screen()
            print("Please enter a valid choice.")
    clear_screen()
    print(response.json())

def view_tasks():
    response = requests.get(BASE_URL)
    try:
        tasks = response.json()
        if not tasks:
            print("You haven't got any tasks.")
        else:
            for task_id, task in tasks.items():
                print(f"ID: {task_id}, Title: {task['title']}, Description: {task['description']}")
    except ValueError:
        print("Error decoding JSON from server response.")

def home_screen():
    clear_screen()
    print(
        "----------------------------------------------------\n"
        "Welcome to TaskFlow! Here's what we've got going on:\n"
        "----------------------------------------------------")
    view_tasks()
    print_menu()

def main():
    while True:
        home_screen()
        choice = input("Enter your choice: ")
        if choice == '1':
            clear_screen()
            add_task()
        elif choice == '2':
            clear_screen()
            remove_task()
        elif choice == '3':
            clear_screen()
            edit_task()
        elif choice == '4':
            home_screen()
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()