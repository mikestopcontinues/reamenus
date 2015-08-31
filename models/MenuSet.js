// import

const _ = require('lodash');
const fs = require('fs-extra');
const async = require('async');

const Menu = require('./Menu');
const ToolbarMenu = require('./ToolbarMenu');
const ContextMenu = require('./ContextMenu');

// export

module.exports = class MenuSet {
  constructor(inputFile, outputFile) {
    this.inputFile = inputFile;
    this.inputText = '';

    this.outputFile = outputFile;
    this.outputText = '';

    this.menus = {};
    this.read();
  }

  read(inputFile) {
    if (inputFile) {
      this.inputFile = inputFile;
    }

    let file = fs.readFileSync(this.inputFile, 'utf8');

    if (!file) {
      return console.log('Failed to read ' + this.inputFile);
    }

    this.inputText = file;
    this.parse();

    return this;
  }

  parse() {
    if (!this.inputText) {
      return console.log('Cannot parse empty string ' + this.inputText);
    }

    this.inputText.split('\n[').map((str, i) => {
      return i > 0 ? '[' + str : str;
    }).forEach((str) => {
      let match = /\[([^\]]*)\]\n([^\[]+)/gi.exec(str);

      if (_.includes(match[1].toLowerCase(), 'toolbar')) {
        return this.menus[match[1]] = new ToolbarMenu(match[2]);
      }

      if (_.includes(match[1].toLowerCase(), 'context')) {
        return this.menus[match[1]] = new ContextMenu(match[2]);
      }

      return this.menus[match[1]] = new Menu(match[2]);
    });

    return this;
  }

  findDuplicates() {
    // TODO!
  }

  style() {
    _.forEach(this.menus, (menu) => {
      menu.style();
    });

    return this;
  }

  flatten() {
    this.outputText = '';

    _.forEach(this.menus, (menu, name) => {
      this.outputText += `[${name}]\n${menu.flatten()}\n}`;
    });

    return this.outputText;
  }

  write(outputFile) {
    if (outputFile) {
      this.outputFile = outputFile;
    }

    this.outputText = this.flatten();
    let file = fs.outputFileSync(this.outputFile, this.outputText, 'utf8');

    if (!file) {
      return console.log('Failed to write ' + this.outputFile);
    }

    return this;
  }
};