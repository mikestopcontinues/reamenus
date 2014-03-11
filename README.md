! REAPER ReaMenus

ReaMenus is a community menuset for Cockos' digital audio workstation REAPER. This repository serves as an archive of source files for ReaMenus as well as the module pymenuset, written to help automate the process of generating new versions.

See the REAPER [forum thread](http://forum.cockos.com/showthread.php?t=58672) for discussion.
See [my website](http://mikestopcontinues.com/project/reaper-reamenus/) for download and menus changelog.

!! pymenuset

This module parses .reapermenu and .reapermenuset files for easy modification.

Basic usage:

	# IMPORT PYMENUSET
	from pymenuset import *

	# CREATE NEW MENUSET
	menuset = MenuSet()

	# PULL INPUT BY
	menuset.read('path/to/input.reapermenuset')
	# OR
	menuset.parse('menuset-as-string')

	# DO SOME STUFF. E.G.
	menuset.menus['Main view'].items.append(Action(id, name, action))

	# PUSH OUTPUT BY
	menuset.write('path/to/output.reapermenuset')
	# OR
	string = menuset.flatten()
	
!! reamenus.py

This script does all the stuff necessary to generate a version of ReaMenus. If `__main__`, you don't even have to run `reamenus.build()`. Outputs to `output/`.