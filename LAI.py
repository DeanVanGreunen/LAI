import os, glob, prettytable, psutil

Version = "1.0.0.0"
# Notices:
# - Data directory format as in data/
# - Atoms will be stored in data/atoms/id.atom
# - Memories will be stored in data/memories/ as a {id}.mem file

def mk_dir(path):
	dir = os.path.dirname(path)
	if not os.path.exists(dir):
		os.makedirs(dir)
	return path

#/////////////////////////////////////////////////////////
# AI - App ClassesAS
#/////////////////////////////////////////////////////////
#format = "[id]|[data]|<chil_id>,<child_id>"
class Atom():
	def __init(self):
		self.id = 0
		self.file_path = ""
		self.data = ""
		self.children_atom_ids = [] #Adam = A,d,a,m and adam = a,d,a,m

	def Save(self, file_path):
		self.file_path = file_path
		f = open(file_path, "w")
		data = f.write(self.id+"|"+self.data+"|"+','.join(self.children_atom_ids))
		f.truncate()
		f.close()

		return self

	def Load(self, file_path):
		self.file_path = file_path
		f = open(file_path, "r")
		data = f.readline()
		f.close()
		data = data.split('|')
		self.id = data[0]
		self.data = data[1]
		if ',' in data[2]:
			self.children_atom_ids = data[2].split(',')
		elif len(data[2]) >=1:
			self.children_atom_ids = [data[2]]
		else:
			self.children_atom_ids = []
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
		self.threads = []
	
	def getPath(self):
		return os.path.abspath(self.path)

	def Load(self, path):
		self.path = path
		mk_dir(path)
		try:
			AtomList = os.listdir(mk_dir(path+"/atoms"))
			MemoryList = os.listdir(mk_dir(path+"/memories"))
			for atom_file in AtomList:
				try:
					#load Atom
					self.atoms.append(Atom().Load(path+"/atoms/"+atom_file))
				except Exception as e:
					# Log to ai some how
					Log("error", "Cannot Load Atom {name}".format(name=atom_file))
			for memory_file in MemoryList:
				try:
					#load Memory
					self.memories.append(Memory().Load(path+"/memories/"+memory_file))
				except Exception as e:
					# Log to ai some how
					Log("error", "Cannot Load Memory {name}".format(name=memory_file))
		except Exception as e:
			Log("error","Cannot Load Atom or Memory Data, " + str(e.args))

	def Save(self, path):
		self.path = path
		mk_dir(path)
		try:
			AtomPath = mk_dir(path+"/atoms/")
			MemoryPath = mk_dir(path+"/memories/")
			total = len(self.atoms) + len(self.memories)
			counter = 0
			for atom in self.atoms:
				path = AtomPath+atom.data+".atom"
				try:
					counter=counter+1
					#load Atom
					atom.Save(path)
					Output("# {0:1.0f}% Processing ".format(float(100.0/(total/counter)))+path)
				except Exception as e:
					# Log to ai some how
					Log("error", "Cannot Save Atom {id}:{name} -> {path}".format(id=atom.id, name=atom.data, path=path) + " "+ str(e.args))
			for memory in self.memories:
				path = MemoryPath+memeory.data+".mem"
				try:
					counter=counter+1
					#load Memory
					memory.Save(path)
					Output("# {0:1.0f}% Processing ".format(float(100.0/(total/counter)))+path)
				except Exception as e:
					# Log to ai some how
					Log("error", "Cannot Load Memory {name}".format(name=memory.id)+ str(e.args))
		except Exception as e:
			Log("error","Cannot Save Atom or Memory Data,"  + " "+ str(e.args))

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
	Output("Log {0} | {1}".format(LogType, LogInfo))
#/////////////////////////////////////////////////////////
# End of Basic I/O Functions
#/////////////////////////////////////////////////////////

def BasicCommands():
	Output("\t\tBasic Commands")
	pt = prettytable.PrettyTable(["Command", "Action"])
	pt.add_row(["\\i","System Info"])
	pt.add_row(["\\g","Generate First 26 Atoms"])
	pt.add_row(["\\s","Save LAI Memory"])
	pt.add_row(["\\s+ <path>","Save LAI Memory To A Particular Directory"])
	pt.add_row(["\\l","Load LAI Memory"])
	pt.add_row(["\\l+ <path>","Load LAI Memory From A Particular Directory"])
	pt.add_row(["\\c","Copyright Information"])
	pt.add_row(["\\h","Displays This Menu"])
	pt.add_row(["\\q","Quit LAI"])
	pt.align = "l"
	#pt.add_row([,""])
	print(pt)



# process the input
def Proccess(_input):
	Output("======================================================================================")
	global canQuit
	if _input[0:1] == "\\": # \
		if _input == "\\c":
			Output("LAI is a Language Based Audio, Visual Artificial Intellegance Created, Copyrighted and TradeMarked By Dean Van Greunen as of January 1st, 2018.")
		elif _input == "\\h":
			BasicCommands()
		elif _input == "\\g":
			for id in range(1, 27):
				data = chr(96+id)
				Output("Making: "+ AI_MEM.getPath().replace('\\','/')+"/atoms/"+str(data)+".atom")
				f = open(AI_MEM.getPath()+"/atoms/"+str(data)+".atom", "w")
				f.write(str(id)+"|"+data+"|")
				f.truncate()
				f.close()
			Output("DONE!")
		elif _input == "\\q":
			canQuit = True
		elif _input == "\\i":
			pt = prettytable.PrettyTable(["Name","Value"])
			pt.add_row(["Data Path",AI_MEM.getPath()])
			pt.add_row(["Total Atom",len(AI_MEM.atoms)])
			pt.add_row(["Total Memories",len(AI_MEM.memories)])
			pt.add_row(["Total Threads", 1 + len(AI_MEM.threads)])
			pt.add_row(["System Memory Used", str(psutil.Process(os.getpid()).memory_info().rss / 1024) + " KBs"])
			pt.align = "l"
			print(pt)
		elif "\\l" in _input:
			path = _input[2:]
			AI_MEM.Load(AI_MEM.getPath())
		elif "\\l+" in _input:
			path = _input[3:]
			AI_MEM.Load(path)
		elif "\\s" in _input:
			path = _input[2:]
			AI_MEM.Save(AI_MEM.getPath())
		elif "\\s+" in _input:
			path = _input[3:]
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