class TasksCommand:
    TASKS_FILE = "tasks.txt"
    COMPLETED_TASKS_FILE = "completed.txt"

    current_items = {}
    completed_items = []

    def read_current(self):
        try:
            file = open(self.TASKS_FILE, "r")
            for line in file.readlines():
                item = line[:-1].split(" ")
                self.current_items[int(item[0])] = " ".join(item[1:])
            file.close()
        except Exception:
            pass

    def read_completed(self):
        try:
            file = open(self.COMPLETED_TASKS_FILE, "r")
            self.completed_items = file.readlines()
            file.close()
        except Exception:
            pass

    def write_current(self):
        with open(self.TASKS_FILE, "w+") as f:
            f.truncate(0)
            for key in sorted(self.current_items.keys()):
                f.write(f"{key} {self.current_items[key]}\n")

    def write_completed(self):
        with open(self.COMPLETED_TASKS_FILE, "w+") as f:
            f.truncate(0)
            for item in self.completed_items:
                f.write(f"{item}\n")

    def sort_current_items(self):
        temp_keys=list(self.current_items.keys())
        temp_keys.sort()
        self.current_items={ i:self.current_items[i] for i in temp_keys}

    def rearrage_priority(self,priority):
        temp_task=self.current_items[priority]
        del self.current_items[priority]
        if priority+1 in self.current_items:
            self.rearrage_priority(priority+1)
        self.current_items[priority+1]=temp_task

    def run(self, command, args):
        self.read_current()
        self.read_completed()
        if command == "add":
            self.add(args)
        elif command == "done":
            self.done(args)
        elif command == "delete":
            self.delete(args)
        elif command == "ls":
            self.ls()
        elif command == "report":
            self.report()
        elif command == "help":
            self.help()

    def help(self):
        print(
            """Usage :-
$ python tasks.py add 2 hello world # Add a new item with priority 2 and text "hello world" to the list
$ python tasks.py ls # Show incomplete priority list items sorted by priority in ascending order
$ python tasks.py del PRIORITY_NUMBER # Delete the incomplete item with the given priority number
$ python tasks.py done PRIORITY_NUMBER # Mark the incomplete item with the given PRIORITY_NUMBER as complete
$ python tasks.py help # Show usage
$ python tasks.py report # Statistics"""
        )

    def add(self, args):
        if len(args)<2:
            print('Sorry, Enter task in format: python tasks.py add 2 "task"')
            return
        if int(args[0]) in self.current_items:
            self.rearrage_priority(int(args[0]))
        
        self.current_items[int(args[0])]=args[1]
        self.write_current()
        print(f'Added task: "{args[1]}" with priority {args[0]}')

    def done(self, args):
        if len(args)<1:
            print('Sorry, Enter task in format: python tasks.py done 2')
            return
        if int(args[0]) not in self.current_items:
            print(f'Error: no incomplete item with priority {args[0]} exists.')
            return
        self.completed_items.append(self.current_items[int(args[0])])
        del self.current_items[int(args[0])]
        self.write_current()
        self.write_completed()
        print(f"Marked item as done.") 
        

    def delete(self, args):
        if len(args)<1:
            print('Sorry, Enter task in format: python tasks.py delete 2')
            return
        if int(args[0]) not in self.current_items:
            print(f'Error: item with priority {args[0]} does not exist. Nothing deleted.')
            return
        del self.current_items[int(args[0])]
        self.write_current()
        print(f"Deleted item with priority {args[0]}")
        

    def ls(self):
        if len(self.current_items) == 0:
            print("No tasks")
            return
        
        self.sort_current_items()
        for index, key in enumerate(self.current_items):
            print(f"{index+1}. {self.current_items[key]} [{key}]")

    def report(self):
        self.sort_current_items()
        print(f"Pending : {len(self.current_items)}")
        for index, key in enumerate(self.current_items):
            print(f"{index+1}. {self.current_items[key]} [{key}]")

        print(f"\nCompleted : {len(self.completed_items)}")
        for index, item in enumerate(self.completed_items):
            print(f"{index+1}. {item}")
