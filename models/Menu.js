// import

const _ = require('lodash');
const fs = require('fs-extra');
const async = require('async');

const Separator = require('./Separator');
const Submenu = require('./Submenu');
const SubmenuEnd = require('./SubmenuEnd');
const Label = require('./Label');
const Action = require('./Action');

// fns

function parseTitle(menu, str) {
  menu.title = /title=(.*)/i.exec(str).pop();
}

function parseIcon(menu, str, icons) {
  let [, index, icon] = /icon_([0-9]+)=(.*)/i.exec(str);
  icons[index] = icon;
}

function parseItem(menu, str, items) {
  let [, index, action, name] = /item_([0-9]+)=([^\s]+)(.*)/i.exec(str);

  index = parseInt(index);
  let length = items.length;

  if (length <= index) {
    for (length; length <= index; length++) {
      items.push(undefined);
    }
  }

  switch(action) {
    case '-1':
      return items.push(new Separator());
    case '-2':
      return items.push(new Submenu(name));
    case '-3':
      return items.push(new SubmenuEnd());
    case '-4':
      return items.push(new Label(name));
    default:
      return items.push(new Action(name, action));
  }
}

// export

module.exports = class Menu {
  constructor(inputText) {
    this.inputText = inputText;
    this.outputText = '';

    this.title = '';
    this.items = [];

    this.parse();
  }

  parse(inputText) {
    if (inputText) {
      this.inputText = inputText;
    }

    let icons = {};
    let items = [];

    this.inputText.split('\n').forEach((str) => {
      switch (str.slice(0, 4)) {
        case 'titl':
          return parseTitle(this, str);
        case 'icon':
          return parseIcon(this, str, icons);
        case 'item':
          return parseItem(this, str, items);
      }
    });

    _.forEach(icons, (icon, i) => {
      if (items[i]) {
        items[i].icon = icon;
      }
    });

    let stack = [this];

    _.compact(items).forEach((item) => {
      switch (item.constructor.name) {
        case 'Submenu':
          if (!_.last(stack)) {
            console.log(item);
          }
          _.last(stack).items.push(item);
          stack.push(item);
          break;

        case 'SubmenuEnd':
          stack.pop();
          break;

        default:
          _.last(stack).items.push(item);
          break;
      }
    });

    return this;
  }

  style() {
    this.items.forEach((item) => {
      item.style();
    });

    return this;
  }

  flatten() {
    this.outputText = this.title ? `title=${this.title}\n` : '';
    let counter = {
      count: 0
    };

    this.items.forEach((item) => {
      this.outputText += item.flatten(counter);
      counter.count++;
    });

    return this.outputText;
  }
};