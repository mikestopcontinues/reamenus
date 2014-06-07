from pymenuset import config
from pymenuset.menu import *
from pymenuset.item import *

import re
import os


class MenuSet(object):
	def __init__(self, input_file=None, output_file=None):
		self.menus = {}

		self.__input_file = input_file
		self.__input_text = ''

		self.__output_file = output_file
		self.__output_text = ''

		self.read()

	def read(self, input_file=None):
		if type(input_file) is not None:
			self.__input_file = input_file

		if type(self.__input_file) is not str:
			self.__input_file = self._get_newest_input_file()

		return self.parse(open(self.__input_file).read())

	def parse(self, input_text=None):
		if type(input_text) is not None:
			self.__input_text = input_text

		for menu_src in re.findall('\[([^\]]*)\]\n([^\[]+)', self.__input_text, re.MULTILINE):
			loc = menu_src[0].lower()

			if 'toolbar' in loc:
				menu_type = ToolbarMenu
			elif 'context' in loc:
				menu_type = ContextMenu
			else:
				menu_type = Menu

			self.menus[menu_src[0]] = menu_type(menu_src[1])

		return self

	def write(self, output_file=None):
		if type(output_file) is not None:
			self.__output_file = output_file

		if type(self.__output_file) is not str:
			self.__output_file = self._get_newest_output_file()

		file = open(self.__output_file, 'w')
		file.write(self.flatten())
		file.close()

		return self

	def strip_toolbars(self):
		return self.strip_matching('toolbar')

	def strip_context_menus(self):
		return self.strip_matching('context')

	def strip_matching(self, substring=''):
		self.menus = {loc: menu for loc, menu in self.menus.items() if substring.lower() not in loc.lower()}

		return self

	def style(self):
		for loc, menu in self.menus.items():
			menu.style()

		return self

	def flatten(self):
		self.__output_text = ''

		for loc, menu in self.menus.items():
			self.__output_text += "[" + loc + "]\n" + menu.flatten()

		return self.__output_text

	@staticmethod
	def _get_newest_input_file(input_dir=None):
		if type(input_dir) is not str:
			input_dir = config.INPUT_DIR

		return input_dir + os.listdir(input_dir)[-1]

	@staticmethod
	def _get_newest_output_file(input_dir=None, output_dir=None):
		if type(input_dir) is not str:
			input_dir = config.INPUT_DIR

		if type(output_dir) is not str:
			output_dir = config.OUTPUT_DIR

		return output_dir + os.listdir(input_dir)[-1]
