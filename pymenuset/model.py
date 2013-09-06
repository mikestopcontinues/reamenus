import re, os

# ready
class MenuSet(object):
	def __init__(self, input = None, output = None):
		self.menus = {}

		# input
		self.read(input)

		# menuset
		self.weave()
		self.trim()
		self.style()

		# output
		self.write(output)

	def weave(self):
		# main menus
		self.menus['Main track'].items = self.menus['Track control panel context'].items[:]
		self.menus['Main track'].title = '&Track'

		self.menus['Main item'].items = self.menus['Media item context'].items[:]
		self.menus['Main item'].title = '&Item'

		self.menus['Main insert'].items = self.menus['Ruler/arrange context'].items[:] #TODO: Why this title in output?
		self.menus['Main insert'].title = 'Time&line'

		self.menus['Main extensions'].title = '&Memory'

		# MIDI main navigate
		self.menus['MIDI main navigate'].items = self.menus['MIDI piano roll context'].items[:]
		self.menus['MIDI main navigate'].title = '&Notes'

		for item in self.menus['MIDI main navigate'].items:
			if type(item) is Submenu and 'Velocity list' in item.name:
				velBreak = self.menus['MIDI main navigate'].items.index(item)
				break

		del self.menus['MIDI main navigate'].items[velBreak]

		# Empty TCP context
		self.menus['Empty TCP context'].items = self.menus['Track control panel context'].items[:]

		# Envelope context
		for item in self.menus['Envelope context'].items:
			if type(item) is Separator:
				envBreak = self.menus['Envelope context'].items.index(item)
				break

		for item in self.menus['Envelope point context'].items:
			if type(item) is Separator:
				pntBreak = self.menus['Envelope point context'].items.index(item)
				break

		self.menus['Envelope point context'].items = self.menus['Envelope point context'].items[:pntBreak] + self.menus['Envelope context'].items[envBreak:]

		# MIDI main menu context
		for item in self.menus['MIDI main menu context'].items:
			if type(item) is not Submenu:
				continue

			if   'File' in item.name:
				item.items = self.menus['MIDI main file'].items[:]
			elif 'Edit' in item.name:
				item.items = self.menus['MIDI main edit'].items[:]
			elif 'Notes' in item.name:
				item.items = self.menus['MIDI main navigate'].items[:]
			elif 'Options' in item.name:
				item.items = self.menus['MIDI main options'].items[:]
			elif 'View' in item.name:
				item.items = self.menus['MIDI main view'].items[:]
			elif 'Actions' in item.name:
				item.items = self.menus['MIDI main actions'].items[:]

	def trim(self):
		remove = []

		for loc, menu in self.menus.items():
			if 'toolbar' in loc.lower():
				remove.append(loc)

		for loc in remove:
			del self.menus[loc]

	def style(self):
		for loc, menu in self.menus.items():
			menu.style()

	def read(self, input):
		if type(input) is not str:
			input = 'work/input/'+os.listdir('work/input/')[-1]

		try:
			file = open(input).read()
		except IOError as e:
			return False

		file = re.findall('\[([^\]]*)\]\n([\s\S]+?)\n\n', file, re.MULTILINE)

		for menuSource in file:
			if   'toolbar' in menuSource[0].lower():
				self.menus[menuSource[0]] = ToolbarMenu(self, menuSource[1])
			elif 'context' in menuSource[0].lower():
				self.menus[menuSource[0]] = ContextMenu(self, menuSource[1])
			else:
				self.menus[menuSource[0]] = Menu(self, menuSource[1])

		return True

	def write(self, output):
		if type(output) is not str:
			output = 'work/output/'+os.listdir('work/input/')[-1]

		open(output, 'w').close()
		file = open(output, 'w')

		out = self.flatten()

		file.write(out)
		file.close()

		return True

	def flatten(self):
		out = ''

		for loc, menu in self.menus.items():
			out += "["+loc+"]\n"+menu.flatten()

		return out

class Menu(object):
	def __init__(self, menuset, source):
		self.menuset = menuset
		self.items = []

		self.parseSource(source)

	def style(self):
		for item in self.items:
			item.style()

	def parseSource(self, source):
		self.source = source.split("\n")

		self.tempItems = []
		self.tempIcons = {}

		for line in self.source:
			self.parseLine(line)

		self.parseEnd()

	def parseLine(self, line):
		if   line[:4] == 'titl':
			self.parseLineTitle(line)
		elif line[:4] == 'icon':
			self.parseLineIcon(line)
		elif line[:4] == 'item':
			self.parseLineItem(line)

	def parseLineTitle(self, line):
		match = re.match('title=(.*)', line)

		self.title = match.group(1)

	def parseLineIcon(self, line):
		match = re.match('icon_([0-9]+)=(.*)', line)

		self.tempIcons[match.group(1)] = match.group(2)

	def parseLineItem(self, line):
		match = re.match('item_([0-9]+)=([^\s]+)(.*)', line)

		id = int(match.group(1))
		action = match.group(2)

		try:
			match.group(3)
		except AttributeError:
			name = None
		else:
			name = match.group(3)

		self.addTempItem(id, action, name)

	def addTempItem(self, id, action, name):
		try:
			self.tempItems[id]
		except IndexError:
			self.tempItems = self.tempItems + [None]*(id - len(self.tempItems) + 1)

		if   action == '-1':
			self.tempItems[id] = Separator(self, id, name, action)
		elif action == '-2':
			self.tempItems[id] = Submenu(self, id, name, action)
		elif action == '-3':
			self.tempItems[id] = Item(self, id, name, action)
		elif action == '-4':
			self.tempItems[id] = Label(self, id, name, action)
		else:
			try:
				self.tempIcons[id]
			except KeyError:
				icon = None
			else:
				icon = self.tempIcons[id]
				del self.tempIcons[id]

			self.tempItems[id] = Action(self, id, name, action, icon)

	def parseEnd(self):
		# wrap up icons
		for id, icon in self.tempIcons.items():
			try:
				self.tempItems[int(id)].setIcon(icon)
			except AttributeError:
				pass

		del self.tempIcons

		# wrap up items
		menuStack = [self]
		for item in self.tempItems:
			if   type(item) is Submenu:
				menuStack[-1].addItem(item)
				menuStack.append(item)
			elif type(item) is Item:
				del menuStack[-1]
			else:
				menuStack[-1].addItem(item)

		del self.tempItems

	def addItem(self, item):
		self.items.append(item)

	def flatten(self):
		count = -1
		out = ''

		try:
			self.title
		except AttributeError:
			pass
		else:
			out += "title="+self.title+"\n"

		for item in self.items:
			count += 1

			count, more = item.flatten(count)
			out += more

		return out+"\n"

class ToolbarMenu(Menu):
	pass

class ContextMenu(Menu):
	pass

class Item(object):
	def __init__(self, menu, id, name, action):
		self.id = id
		self.name = name
		self.menu = menu
		self.action = action
		self.icon = None

	def style(self):
		pass

	def flatten(self, count):
		out = "item_"+str(count)+"="+self.action+" "+self.name+"\n"

		if type(self.icon) is str:
			out += "icon_"+str(count)+"="+self.icon+"\n"

		return count, out

class Separator(Item):
	def style(self):
		self.name = None

	def flatten(self, count):
		out = "item_"+str(count)+"="+self.action+"\n"

		return count, out

class Submenu(Item):
	def __init__(self, menu, id, name, action):
		super().__init__(menu, id, name, action)

		self.items = []

	def style(self):
		# remove menu walk
		self.name = self.name.replace('&', '').strip()

		if type(self.menu) is Menu:
			self.name = '&' + self.name

		# do children
		for item in self.items:
			item.style()

	def addItem(self, item):
		self.items.append(item)

	def flatten(self, count):
		out = "item_"+str(count)+"="+self.action+" "+self.name+"\n"

		for item in self.items:
			count += 1
			count, more = item.flatten(count)
			out += more

		count += 1
		out += "item_"+str(count)+"=-3\n"

		return count, out

class Label(Item):
	def style(self):
		# remove old wrap
		self.name = self.name.replace('::', '').strip().upper()

class Action(Item):
	def __init__(self, menu, id, name, action, icon):
		super().__init__(menu, id, name, action)

		self.icon = icon

	def style(self):
		# smooth menu walk
		self.name = self.name.replace('&', '').strip()

		if type(self.menu) is Menu:
			self.name = '&' + self.name
