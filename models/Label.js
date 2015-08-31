// import

const Item = require('./Item');

// export

module.exports = class Label extends Item {
  constructor(name) {
    super(name, '-4');
  }

  style() {
    this.name = this.name.toUpperCase().trim();

    return this;
  }
};