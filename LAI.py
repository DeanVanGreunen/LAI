import os, glob, prettytable, psutil

Version = "1.0.0.0"
# Notices:
# - Data directory format as in data/
# - Atoms will be stored in data/atoms/id.atom
# - Memories will be stored in data/memories/ as a {id}.mem file

def mkdir(path):
	if not os.path.exists(path):
		os.makedirs(path)
	return path

#/////////////////////////////////////////////////////////
# AI - App ClassesAS
#/////////////////////////////////////////////////////////
class Atom():
	def __init(self):
		self.file_path = ""

	def Load(self, file_path):
		self.file_path = file_path
		return self

	def Save(self, file_path):
		self.file_path = file_path
		return self

class Memory():
	def __init__(self):
		self.inputs = []
		self.actions_taken = []
		self.outputs = []
		self.file_path = ""

	def Load(self, file_path):
		self.file_path = file_path
		return self

	def Save(self, file_path):
		self.file_path = file_path
		return self

class AI_MEMORY():
	def __init__(self):
		self.atoms = []
		self.memories = []
		self.path = ""
	
	def getPath(self):
		return os.path.abspath(self.path)

	def Load(self, path):
		self.path = path
		mkdir(path)
		try:
			AtomList = os.listdir(mkdir(path+"atoms"))
			MemoryList = os.listdir(mkdir(path+"memories"))
			for atom_file in AtomList:
				try:
					#load Atom
					self.atoms.append(Atom().Load(atom_file))
				except Exception as e:
					# Log to ai some how
					Log("error", "Cannot Load Atom {name}".format(name=atom_file))
			for memory_file in MemoryList:
				try:
					#load Memory
					self.memories.append(Memory().Load(memory_file))
				except Exception as e:
					# Log to ai some how
					Log("error", "Cannot Load Memory {name}".format(name=atom_file))
		except Exception as e:
			Log("error","Cannot Load Atom or Memory Data, " + e.message)

	def Save(self, path):
		self.path = path
		mkdir(path)
		try:
			AtomPath = mkdir(path+"atoms")
			MemoryPath = mkdir(path+"memories")
			for atom in self.atoms:
				try:
					#load Atom
					atom.Save(AtomPath)
				except Exception as e:
					# Log to ai some how
					Log("error", "Cannot Save Atom {name}".format(name=atom.id))
			for memory in self.memories:
				try:
					#load Memory
					memory.Save(MemoryPath)
				except Exception as e:
					# Log to ai some how
					Log("error", "Cannot Load Memory {name}".format(name=memory.id))
		except Exception as e:
			Log("error","Cannot Save Atom or Memory Data, " + e.message)

#/////////////////////////////////////////////////////////
# End of App Vars
#/////////////////////////////////////////////////////////

#/////////////////////////////////////////////////////////
# AI - App Vars
#/////////////////////////////////////////////////////////
canQuit = False;
loop_counter = 0
temp_input = ""
AI_MEM = AI_MEMORY()
#/////////////////////////////////////////////////////////
# End of App Vars
#/////////////////////////////////////////////////////////

#/////////////////////////////////////////////////////////
# AI - Basic I/O Functions
#/////////////////////////////////////////////////////////
# gets user input
def GetInput(Question="> "):
	return input(Question)

# displays the output to the console
def Output(_format, *args):
	Log("output", _format.format(args))
	print(_format.format(args))

# used to load data from disk to memory
def DataLoad():
	AI_MEM.Load("data/")

# used to save the store data in memory
def DataSave():
	AI_MEM.Save("data/")

# used for the language itself
def LoadAtomByName(atom):
	pass

def SaveAtomByName(atom):
	pass

# used for Logging actions, etc.
def Log(LogType, LogInfo):
	pass
#/////////////////////////////////////////////////////////
# End of Basic I/O Functions
#/////////////////////////////////////////////////////////

def BasicCommands():
	Output("\t\tBasic Commands")
	pt = prettytable.PrettyTable(["Command", "Action"])
	pt.add_row(["\\i","System Info"])
	pt.add_row(["\\l","Load LAI Memory"])
	pt.add_row(["\\s","Save LAI Memory"])
	pt.add_row(["\\c","Copyright Information"])
	pt.add_row(["\\q","Quit LAI"])
	#pt.add_row([,""])
	print(pt)



# process the input
def Proccess(_input):
	global canQuit
	if _input[0:1] == "\\": # \
		if _input == "\\c":
			Output("LAI is a Language Based Audio, Visual Artificial Intellegance Created, Copyrighted and TradeMarked By Dean Van Greunen as of January 1st, 2018.")
		elif _input == "\\q":
			canQuit = True
		elif _input == "\\i":
			pt = prettytable.PrettyTable(["Name","Value"])
			pt.add_row(["Data Path",AI_MEM.getPath()])
			pt.add_row(["Total Atom",len(AI_MEM.atoms)])
			pt.add_row(["Total Memories",len(AI_MEM.memories)])
			pt.add_row(["System Memory Used", str(psutil.Process(os.getpid()).memory_info().rss / 1024) + " KBs"])
			print(pt)
		elif "\\l" in _input:
			path = _input[2:]
			AI_MEM.Load(path)
		elif "\\s" in _input:
			path = _input[2:]
			AI_MEM.Save(path)
		#else if _input == "\q":
		#	canQuit = True
	else: # do processing here
		pass

#/////////////////////////////////////////////////////////
# AI - BuiltIn Functions
#/////////////////////////////////////////////////////////
# required setup
# used to register functions for use by the
def RegF():
	registry = {}
	def registrar(func):
		registry[func.__name__] = func
		return func  # normally a decorator returns a wrapped function, 
		# but here we return func unmodified, after registering it
	registrar.all = registry
	return registrar
# declare Decorator
AIFunction = RegF()

# Get the
@AIFunction
def GetAtom(atom_name):
	return LoadAtomByName(atom)


@AIFunction
def SetAtom(atom):
	SaveAtomByName(atom)


#/////////////////////////////////////////////////////////
# End of Built In Functions
#/////////////////////////////////////////////////////////
def cls():
	os.system('cls' if os.name=='nt' else 'clear')
# main entry point
def Main():
	global canQuit
	global loop_counter
	global version
	cls()
	Output("======================================================================================")
	Output("LAI [Version "+Version+"]")
	Output("(c) 2018 Dean Van Greunen. All Rights Resevred.")
	Output("======================================================================================")
	Output("Starting LAI...")
	BasicCommands() #displays basic stuff to user
	DataLoad()
	while not canQuit:
		loop_counter = loop_counter + 1
		if loop_counter >= 255:
				DataSave()
		temp_input = GetInput()
		Proccess(temp_input)
	DataSave()
	Output("...Exiting")

# call main
Main()