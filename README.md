# REAPER ReaMenus

ReaMenus is a community menuset for Cockos' digital audio workstation REAPER. This repository serves as an archive of source files for ReaMenus as well as the module pymenuset, written to help automate the process of generating new versions.

See the REAPER [forum thread](http://forum.cockos.com/showthread.php?t=58672) for discussion.
See [my website](http://mikestopcontinues.com/project/reaper-reamenus/) for download and menus changelog.

## reamenus.js

This script does all the stuff necessary to generate a version of ReaMenus. If `__main__`, you don't even have to run `reamenus.build()`. Outputs to `output/`.

To convert the newest file in `/input` to reamenus format in `/output`, do:

```
npm install && npm start
```
