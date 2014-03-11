from pymenuset import *


def build(menuset=None):
	if menuset is None:
		menuset = MenuSet()

	# Main menus
	menuset.menus['Main track'].items = menuset.menus['Track control panel context'].items[:]
	menuset.menus['Main track'].title = '&Track'

	menuset.menus['Main item'].items = menuset.menus['Media item context'].items[:]
	menuset.menus['Main item'].title = '&Item'

	menuset.menus['Main insert'].items = menuset.menus['Ruler/arrange context'].items[:]
	menuset.menus['Main insert'].title = 'Time&line'

	menuset.menus['Main extensions'].title = '&Memory'

	# MIDI main navigate
	menuset.menus['MIDI main navigate'].items = menuset.menus['MIDI piano roll context'].items[:]
	menuset.menus['MIDI main navigate'].title = '&Notes'

	for item in menuset.menus['MIDI main navigate'].items:
		if type(item) is Submenu and 'Velocity list' in item.name:
			vel_split = menuset.menus['MIDI main navigate'].items.index(item)
			break

	del menuset.menus['MIDI main navigate'].items[vel_split]

	# Empty TCP context
	menuset.menus['Empty TCP context'].items = menuset.menus['Track control panel context'].items[:]

	# Envelope context
	for item in menuset.menus['Envelope context'].items:
		if type(item) is Separator:
			env_index = menuset.menus['Envelope context'].items.index(item)
			env_split = menuset.menus['Envelope context'].items[env_index:]
			break

	for item in menuset.menus['Envelope point context'].items:
		if type(item) is Separator:
			pnt_index = menuset.menus['Envelope point context'].items.index(item)
			pnt_split = menuset.menus['Envelope point context'].items[:pnt_index]
			break

	menuset.menus['Envelope point context'].items = pnt_split + env_split

	# MIDI main menu context
	for item in menuset.menus['MIDI main menu context'].items:
		if type(item) is not Submenu:
			continue

		if 'File' in item.name:
			item.items = menuset.menus['MIDI main file'].items[:]
		elif 'Edit' in item.name:
			item.items = menuset.menus['MIDI main edit'].items[:]
		elif 'Notes' in item.name:
			item.items = menuset.menus['MIDI main navigate'].items[:]
		elif 'Options' in item.name:
			item.items = menuset.menus['MIDI main options'].items[:]
		elif 'View' in item.name:
			item.items = menuset.menus['MIDI main view'].items[:]
		elif 'Actions' in item.name:
			item.items = menuset.menus['MIDI main actions'].items[:]

	# wrap it up
	menuset.strip_toolbars().style().write()


if __name__ == '__main__':
	build()
