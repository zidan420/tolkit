#!/usr/bin/python3
from colorama import Fore, Style
from tabulate import tabulate
import os

SCRIPTNAME = os.path.basename(__file__)
FILENAME = 'tools.txt'
BACKUPNAME = 'backup.txt'

MODE = 'relax'
RACTIVE = ' (Active)'
SACTIVE = ''

def get_input(text):
	return input(Fore.BLUE + text + Fore.RESET)

def match_option(option, num, text):
	if (option == num or option == text):
		return True

def add_tool():
	# get the last id
	ID = 0
	if (os.path.exists(FILENAME)):
		with open(FILENAME, 'r') as f:
			for line in f:
				line = line.strip()
				# skip empty lines
				if (not line):
					continue
				ID = int(line.split('$@$')[0])

	# set new id
	ID = str(ID+1)

	name = get_input("Name: ")
	purpose = get_input("Purpose: ")
	url = get_input("Url: ")

	with open(FILENAME, "a") as f:
		f.write(ID+'$@$'+name+'$@$'+purpose+'$@$'+url+'\n')

def list_tool():
	if (not os.path.exists(FILENAME)):
		return

	headers = [Fore.GREEN+'ID', 'Name', 'Purpose', 'URL'+ Style.RESET_ALL]
	table = []

	with open(FILENAME, "r") as f:
		for line in f:
			line = line.strip()
			line = line.replace('\\n', '\n')
			# skip empty lines
			if (not line):
				continue

			table.append([line.split('$@$')[0], line.split('$@$')[1],
							line.split('$@$')[2], line.split('$@$')[3]])
	if len(table):
		print(tabulate(table, headers=headers, tablefmt="grid", colalign=("center", "center", "left")))

def edit_tool():
	if (not os.path.exists(FILENAME)):
		return
	ID = get_input("ID to edit: ")
	name = get_input("Name: ")
	purpose = get_input("Purpose: ")
	url = get_input("Url: ")

	# Read all tools into memory
	lines = ''
	with open(FILENAME, "r") as f:
		lines = f.readlines()

	# Backup FILENAME
	os.replace(FILENAME, BACKUPNAME)

	# Write (edited) to file
	with open(FILENAME, "w") as f:
		for line in lines:
			if (ID == line.split('$@$')[0]):
				f.write(ID+'$@$'+name+'$@$'+purpose+'$@$'+url+'\n')
			else:
				f.write(line)

	# Remove Backup file
	os.remove(BACKUPNAME)

def config_search():
	global MODE
	global RACTIVE
	global SACTIVE
	print(Fore.CYAN+"\tModes allowed:")
	print("\t\t1. Relax"+RACTIVE)
	print("\t\t2. Strict"+SACTIVE)
	print(Fore.RESET)

	temp = get_input("mode: ")
	if match_option(temp, '1', 'relax'):
		MODE = 'relax'
		RACTIVE = ' (Active)'
		SACTIVE = ''
	elif match_option(temp, '2', 'strict'):
		MODE = 'strict'
		RACTIVE = ''
		SACTIVE = ' (Active)'
	else:
		return

	# Save changes permanently
	# Read whole file into memory
	lines = ''
	with open(SCRIPTNAME, "r") as f:
		lines = f.readlines()

	# Backup THIS PYTHON SCRIPT
	os.replace(SCRIPTNAME, BACKUPNAME)

	# Write (edited) to file
	with open(SCRIPTNAME, "w") as f:
		for line in lines:
			line = line.rstrip()
			if ("MODE = " in line[:7]):
				f.write("MODE = '{}'\n".format(MODE))

			elif ("RACTIVE = " in line[:10]):
				if (MODE == 'relax'):
					f.write("RACTIVE = ' (Active)'\n")
				else:
					f.write("RACTIVE = ''\n")

			elif ("SACTIVE = " in line[:10]):
				if (MODE == 'strict'):
					f.write("SACTIVE = ' (Active)'\n")
				else:
					f.write("SACTIVE = ''\n")

			else:
				f.write(line+'\n')

	# Remove Backup file
	os.remove(BACKUPNAME)

def search_tool():
	if (not os.path.exists(FILENAME)):
		return

	headers = [Fore.GREEN+'ID', 'Name', 'Purpose', 'URL'+ Style.RESET_ALL]
	table = []

	keywords = get_input("Search: ")
	if (MODE == 'relax'):
		if ' ' in keywords:
			keywords = keywords.split(' ')
		else:
			keywords = [keywords]
	with open(FILENAME, 'r') as f:
		for line in f:
			line = line.strip()
			line = line.replace('\\n', '\n')
			if (not line):
				continue
			if (MODE == 'relax'):
				match = False
				for keyword in keywords:
					if (keyword.lower() in line.lower()):
						match = True
				if match:
					table.append([line.split('$@$')[0], line.split('$@$')[1],
								line.split('$@$')[2], line.split('$@$')[3]])
			else:
				if (keywords.lower() in line.lower()):
					table.append([line.split('$@$')[0], line.split('$@$')[1],
								line.split('$@$')[2], line.split('$@$')[3]])
	if len(table):
		print(tabulate(table, headers=headers, tablefmt='grid', colalign=("center", "center", "left")))

def delete_tool():
	if (not os.path.exists(FILENAME)):
		return
	ID = get_input("ID to delete: ")

	# Read all tools into memory
	lines = ''
	with open(FILENAME, "r") as f:
		lines = f.readlines()

	# Backup FILENAME
	os.replace(FILENAME, BACKUPNAME)

	# Write (edited) to file
	with open(FILENAME, "w") as f:
		for line in lines:
			if (ID != line.split('$@$')[0]):
				f.write(line)

	# Remove Backup file
	os.remove(BACKUPNAME)

if __name__ == '__main__':
	while True:
		print(Fore.CYAN + "1. List all tools")
		print("2. Add a new tool")
		print("3. Edit a tool")
		print("4. Search a tool")
		print("5. Configure Search")
		print("6. Delete a tool")
		print("7. Clear Screen")
		print("8. Exit" + Fore.RESET)

		option = input(Fore.YELLOW + ">>> " + Fore.RESET)

		if match_option(option, '1', 'list'):
			list_tool()
		elif match_option(option, '2', 'add'):
			add_tool()
		elif match_option(option, '3', 'edit'):
			edit_tool()
		elif match_option(option, '4', 'search'):
			search_tool()
		elif match_option(option, '5', 'config'):
			config_search()
		elif match_option(option, '6', 'rm'):
			delete_tool()
		elif match_option(option, '7', 'cls'):
			os.system("clear")
		elif match_option(option, '8', 'exit'):
			exit()
