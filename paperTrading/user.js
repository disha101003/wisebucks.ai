const { Model, DataTypes } = require('sequelize');
const sequelize = new Sequelize('sqlite::memory:'); // Example for SQLite

class User extends Model {}

User.init({
  // Assuming you have an auto-incrementing primary key
  userId: {
    type: DataTypes.INTEGER,
    primaryKey: true,
    autoIncrement: true,
    allowNull: false
  },
  fullName: {
    type: DataTypes.STRING,
    allowNull: false
  },
  email: {
    type: DataTypes.STRING,
    allowNull: false,
    unique: true,
    validate: {
      isEmail: true
    }
  },
  mobile: {
    type: DataTypes.STRING,
    allowNull: false,
    unique: true
  },
  password: {
    type: DataTypes.STRING,
    allowNull: false
  },
  availableFunds: {
    type: DataTypes.DECIMAL(10, 2), // Adjust precision and scale according to requirements
    allowNull: false,
    defaultValue: 100000.00
  }
}, {
  sequelize,
  modelName: 'User',
  timestamps: true, // Enable timestamps
  createdAt: 'created_at', // Rename field if you want to match MongoDB's `timestamps`
  updatedAt: 'updated_at'
});

// Syncs with the database, creating the table if it doesn't exist
sequelize.sync();

module.exports = User;
