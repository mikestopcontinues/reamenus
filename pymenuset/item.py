

class Item(object):
	def __init__(self, id, name, action):
		self.id = id
		self.name = name
		self.action = action
		self.icon = None

	def style(self):
		return self

	def flatten(self, count):
		return count, "item_" + str(count) + "=" + self.action + " " + self.name + "\n"


class Separator(Item):
	def __init__(self, id, name, action):
		super().__init__(id, name, action)

		self.name = None

	def flatten(self, count):
		return count, "item_" + str(count) + "=" + self.action + "\n"


class Submenu(Item):
	def __init__(self, id, name, action):
		super().__init__(id, name, action)

		self.items = []

	def style(self):
		self.name = '&' + self.name.strip('&').strip()

		for item in self.items:
			item.style()

	def add(self, item):
		self.items.append(item)

	def flatten(self, count):
		count, out = super().flatten(count)

		for item in self.items:
			count += 1
			count, more = item.flatten(count)
			out += more

		count += 1
		out += "item_" + str(count) + "=-3\n"

		return count, out


class SubmenuEnd(Item):
	pass


class Label(Item):
	def style(self):
		self.name = self.name.strip().upper()


class Action(Item):
	def style(self):
		self.name = '&' + self.name.strip('&').strip()

	def flatten(self, count):
		count, out = super().flatten(count)

		if type(self.icon) is str:
			out += "icon_" + str(count) + "=" + self.icon + "\n"

		return count, out
