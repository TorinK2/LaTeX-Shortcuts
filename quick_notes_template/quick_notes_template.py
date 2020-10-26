import datetime
from shutil import copyfile

'''
By Torin Kovach
Makes a simple LaTeX notes template to use in class!
'''

def get_valid_input(question, inputs):
    i = input(question)
    if i not in inputs:
        print("Not a proper input")
        return get_valid_input(question, inputs)
    else:
        return i

# Ask user for information:
print("LaTeX Note Template Maker\n\n")
print("Indicate a semester/quarter by these identifiers:\n \
       Spring - SP\n \
       Summer - SU\n \
       Fall - F\n \
       Winter - W")
code_to_semester = {"SP":"Spring", "SU":"Summer", "F":"Fall", "W":"Winter"}
semester = get_valid_input("What semster/quarter? ", ["SP", "SU", "F", "W"])
class_name = input("What is name of class? ")
title = input("What is the title of this document? ")

# Get date information
today = datetime.date.today()
year = str(today.year)
date = (str(today.month) + "/" + str(today.day) + "/" + str(today.year))


# Read from template
with open("template/template.tex", 'r') as reader:
    text = reader.read()

# Modify template with pertinent data
text = text.replace("[CLASS]", class_name)
text = text.replace("[SEMESTER]", semester)
text = text.replace("[NAME]", title)
text = text.replace("[DATE]", date)
text = text.replace("[YEAR]", year)

# Put modified template into new file
with open("new-notes-file.tex", 'w') as writer:
    writer.write(text)

# Final output
print("\nNote template generated")
print("Look in local directory under 'new-notes-file.txt'")
input("Press ENTER to exit")


