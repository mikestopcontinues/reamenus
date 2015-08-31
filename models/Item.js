// import

const _ = require('lodash');
const fs = require('fs-extra');
const async = require('async');

// export

module.exports = class Item {
  constructor(name, action) {
    this.name = name;
    this.action = action;
    this.icon = undefined;
  }

  style() {
    return this;
  }

  flatten(counter) {
    return `item_${counter.count}=${this.action} ${this.name || ''}`.trim() + '\n';
  }
};