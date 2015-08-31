// import

const Item = require('./Item');

// export

module.exports = class Separator extends Item {
  constructor() {
    super(undefined, '-1');
  }
};