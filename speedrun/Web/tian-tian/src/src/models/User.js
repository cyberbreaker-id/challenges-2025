let nextUserId = 1;
const users = [];

class User {
  constructor({ username, password }) {
    this._id = nextUserId++;
    this.username = username;
    this.password = password;
    this.createdAt = new Date();
    
    if (!this.username || !this.password) {
      throw new Error('Username and password are required');
    }
    if (this.username.length < 3 || this.username.length > 30) {
      throw new Error('Username must be between 3 and 30 characters');
    }
    if (this.password.length < 6) {
      throw new Error('Password must be at least 6 characters');
    }
  }

  static findOne(query) {
    if (query.username) {
      return users.find(u => u.username === query.username) || null;
    }
    if (query._id) {
      return users.find(u => u._id === query._id) || null;
    }
    return null;
  }

  static findById(id) {
    return users.find(u => u._id == parseInt(id)) || null;
  }

  save() {
    const existing = users.find(u => u.username === this.username && u._id != this._id);
    if (existing) {
      throw new Error('User with this username already exists');
    }
    users.push(this);
    return this;
  }

  toJSON() {
    const { password, ...userObject } = this;
    return userObject;
  }
}

module.exports = User;