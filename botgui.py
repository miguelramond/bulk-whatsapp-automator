from tkinter import *

# Create root window
root = Tk()
root.title("StreetBot")

# Create form input field
e = Entry(root, width=35, borderwidth=5)
e.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

global f_num
global math


# Button click function
def button_click(number):
    # Store in variable number in field
    current = e.get()
    # Delete number in field once stores
    e.delete(0, END)
    # Insert previous number in field and andd number pressed
    e.insert(0, str(current) + str(number))


# Clear button funciton
def button_clear():
    e.delete(0, END)


def button_add():
    first_number = e.get()
    global f_num
    global math
    math = "addition"
    f_num = int(first_number)
    e.delete(0, END)


def button_subtract():
    first_number = e.get()
    global f_num
    global math
    math = "subtraction"
    f_num = int(first_number)
    e.delete(0, END)


def button_multiply():
    first_number = e.get()
    global f_num
    global math
    math = "multiplication"
    f_num = int(first_number)
    e.delete(0, END)


def button_divide():
    first_number = e.get()
    global f_num
    global math
    math = "division"
    f_num = int(first_number)
    e.delete(0, END)


def button_equals():
    second_number = e.get()
    e.delete(0, END)

    if math == "addition":
        e.insert(0, f_num + int(second_number))

    if math == "subtraction":
        e.insert(0, f_num - int(second_number))

    if math == "multiplication":
        e.insert(0, f_num * int(second_number))

    if math == "division":
        e.insert(0, f_num / int(second_number))


# Create list to store buttons
buttons = {}

# Variables created in order to dynamically asign button position
rowheight = 4
colposition = 0

# Button creation loop
for i in range(0, 10):
    # Add button to list and then grid
    # In command parameter a c variable is assigned to "lock" the value of the button when created
    buttons[i] = Button(root, text=i, padx=40, pady=20, command=lambda c=i: button_click(c))

    # Special case for '0' button positioning
    if i == 0:
        buttons[i].grid(row=rowheight, column=colposition)
        rowheight -= 1

    # Regular assignment of rest of buttons
    if i != 0:
        buttons[i].grid(row=rowheight, column=colposition)
        # Add to column variable in order to move one col right
        colposition += 1

    # When third columin in row is added, reset to start in new row
    if colposition == 3:
        # Since calculators have buttons starting with nine and counting to zero, row starts in pos 3 and moves up
        rowheight -= 1
        colposition = 0


# Non-integer buttons creation
button_add = Button(root, text="+", padx=40, pady=20, command=button_add)
button_equals = Button(root, text="=", padx=99, pady=20, command=button_equals)
button_clear = Button(root, text="Clear", padx=88, pady=20, command=button_clear)

button_subtract = Button(root, text="-", padx=41, pady=20, command=button_subtract)
button_multiply = Button(root, text="*", padx=42, pady=20, command=button_multiply)
button_divide = Button(root, text="/", padx=42, pady=20, command=button_divide)

button_add.grid(row=5, column=0)
button_equals.grid(row=5, column=1, columnspan=2)
button_clear.grid(row=4, column=1, columnspan=2)

button_subtract.grid(row=6, column=0)
button_multiply.grid(row=6, column=1)
button_divide.grid(row=6, column=2)


# Program loop
root.mainloop()
