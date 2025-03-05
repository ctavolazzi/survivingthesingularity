// Empty polyfill for Node.js stream module
export default {
  Readable: class Readable {
    constructor() {}
    pipe() { return this; }
    on() { return this; }
    once() { return this; }
    read() { return null; }
  },
  Writable: class Writable {
    constructor() {}
    write() { return true; }
    end() {}
    on() { return this; }
  },
  Transform: class Transform {
    constructor() {}
    _transform() {}
    pipe() { return this; }
  },
  PassThrough: class PassThrough {
    constructor() {}
    pipe() { return this; }
  }
};