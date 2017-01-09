'use strict';
require("babel/register");

// import

const _ = require('lodash');
const fs = require('fs-extra');
const async = require('async');

const MenuSet = require('./models/MenuSet');

// build

function build(menuset) {

  // main menus

  menuset.menus['Main track'].items = menuset.menus['Track control panel context'].items.slice();
  menuset.menus['Main track'].title = '&Track';

  menuset.menus['Main item'].items = menuset.menus['Media item context'].items.slice();
  menuset.menus['Main item'].title = '&Item';

  menuset.menus['Main insert'].items = menuset.menus['Ruler/arrange context'].items.slice();
  menuset.menus['Main insert'].title = 'Time&line';

  menuset.menus['Main extensions'].title = '&Memory';

  // midi menus

  menuset.menus['MIDI main navigate'].items = menuset.menus['MIDI piano roll context'].items.slice();
  menuset.menus['MIDI main navigate'].title = '&Notes';

  let split = undefined;

  menuset.menus['MIDI main navigate'].items.some((item, i) => {
    if (_.includes(item.name, 'Velocity list')) {
      menuset.menus['MIDI main navigate'].items.splice(i, 1);
      return true;
    }
  });

  menuset.menus['MIDI main menu context'].items.forEach((item) => {
    if (!item.items) {
      return;
    }

    switch (item.name.replace(/&/g, '').trim()) {
      case 'File':
        return item.items = menuset.menus['MIDI main file'].items.slice();
      case 'Edit':
        return item.items = menuset.menus['MIDI main edit'].items.slice();
      case 'Notes':
        return item.items = menuset.menus['MIDI main navigate'].items.slice();
      case 'Options':
        return item.items = menuset.menus['MIDI main options'].items.slice();
      case 'View':
        return item.items = menuset.menus['MIDI main view'].items.slice();
      case 'Contents':
        return item.items = menuset.menus['MIDI main contents'].items.slice();
      case 'Actions':
        return item.items = menuset.menus['MIDI main actions'].items.slice();
    }
  });

  // envelope menus

  menuset.menus['Envelope context'].items.some((envItem, e) => {
    if (envItem.constructor.name != 'Separator') {
      return;
    }

    return menuset.menus['Envelope point context'].items.some((pntItem, p) => {
      if (pntItem.constructor.name != 'Separator') {
        return;
      }

      return menuset.menus['Envelope point context'].items = menuset.menus['Envelope point context'].items.slice(0, e).concat(menuset.menus['Envelope point context'].items.slice(p));
    });
  });

  // track menus

  menuset.menus['Empty TCP context'].items = menuset.menus['Track control panel context'].items.slice();

  // toolbars

  menuset.menus = _.omit(menuset.menus, (menu, name) => {
    return _.includes(name.toLowerCase(), 'toolbar');
  });

  // wrap up

  menuset.style().write();
}

// run

fs.readdir('./input', (err, files) => {
  async.each(files, (menuset) => {
    build(new MenuSet('./input/' + menuset, './output/' + menuset));
  });
});
