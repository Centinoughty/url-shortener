const mongoose = require("mongoose");
const formatDate = require("../util/formatDate");

const urlSchema = new mongoose.Schema(
  {
    url: {
      type: String,
      required: true,
      unique: true,
    },
    shortUrl: {
      type: String,
      required: true,
      unique: true,
    },
    hitCount: {
      type: Number,
      required: true,
      default: 0,
    },
    dailyHit: {
      type: Number,
      required: true,
      default: 0,
    },
    date: {
      type: String,
      required: true,
      default: () => formatDate(new Date()),
    },
  },
  { timestamps: true }
);

module.exports = mongoose.model("urls", urlSchema);
