// import

const Item = require('./Item');

// export

module.exports = class Submenu extends Item {
  constructor(name) {
    super(name, '-2');
    this.items = [];
  }

  style() {
    this.name = `&${this.name.replace('&', '').trim()}`;

    this.items.forEach((item) => {
      item.style();
    });

    return this;
  }

  flatten(counter) {
    let output = super.flatten(counter);

    this.items.forEach((item) => {
      counter.count++;
      output += item.flatten(counter);
    });

    return output + `item_${++counter.count}=-3\n`;
  }
};