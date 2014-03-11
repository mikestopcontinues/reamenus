from pymenuset import config
from pymenuset.item import *

import re


class Menu(object):
	def __init__(self, input_text=None):
		self.title = ''
		self.items = []

		self.__input_text = ''
		self.__output_text = ''

		self.parse(input_text)

	def parse(self, input_text=None):
		if type(input_text) is not None:
			self.__input_text = input_text

		items = []
		icons = {}

		for line in self.__input_text.split("\n"):
			search = line[:4]

			if search == 'titl':
				self.__parse_title(line)
			elif search == 'icon':
				self.__parse_icon(line, icons)
			elif search == 'item':
				self.__parse_item(line, items)

		# connect icons with actions
		for id in icons.keys():
			try:
				items[int(id)].icon = icons[id]
			except AttributeError:
				pass

		# properly nest submenus
		stack = [self]

		for item in items:
			if type(item) is Submenu:
				stack[-1].add(item)
				stack.append(item)
			elif type(item) is SubmenuEnd:
				del stack[-1]
			else:
				stack[-1].add(item)

		return self

	def __parse_title(self, line):
		match = re.match('title=(.*)', line)
		self.title = match.group(1)

	def __parse_icon(self, line, icons):
		match = re.match('icon_([0-9]+)=(.*)', line)
		icons[match.group(1)] = match.group(2)

	def __parse_item(self, line, items):
		match = re.match('item_([0-9]+)=([^\s]+)(.*)', line)

		id = int(match.group(1))
		action = match.group(2)

		try:
			match.group(3)
		except AttributeError:
			name = None
		else:
			name = match.group(3)

		try:
			items[id]
		except IndexError:
			items.extend([None] * (id - len(items) + 1))

		item_lookup = {
			'-1': Separator,
			'-2': Submenu,
			'-3': SubmenuEnd,
			'-4': Label,
		}

		try:
			items[id] = item_lookup[action](id, name, action)
		except KeyError:
			items[id] = Action(id, name, action)

	def style(self):
		for item in self.items:
			item.style()

		return self

	def strip_labels(self):
		return self.strip_matching('label')

	def strip_matching(self, item_type=''):
		self.items = {loc: menu for loc, menu in self.items.items() if item_type.lower() != loc.__class__.__name__.lower()}

		return self

	def add(self, item):
		self.items.append(item)

	def flatten(self):
		self.__output_text = 'title=' + self.title + "\n"
		count = -1

		for item in self.items:
			count += 1
			count, more = item.flatten(count)
			self.__output_text += more

		self.__output_text += "\n"

		return self.__output_text


class ToolbarMenu(Menu):
	pass


class ContextMenu(Menu):
	pass
