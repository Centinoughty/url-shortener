const mongoose = require("mongoose");

module.exports.connectDb = async () => {
  try {
    await mongoose.connect(process.env.MONGO_URL);
    console.log("connection success");
  } catch (error) {
    console.log("connection failed");
  }
};
