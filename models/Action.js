// import

const Item = require('./Item');

// export

module.exports = class Action extends Item {
  constructor(name) {
    super(name, '-2');
    this.items = [];
  }

  style() {
    this.name = `&${this.name.replace('&', '').trim()}`;

    return this;
  }

  flatten(counter) {
    let output = super.flatten(counter);

    if (!this.icon) {
      return output;
    }

    return output + `icon_${counter.count}=${this.icon}\n`;
  }
};