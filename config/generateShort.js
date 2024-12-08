const Url = require("../models/urlModel");

const generateRandom = (n) => {
  const charecters =
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";

  let res = "";
  for (let i = 0; i < n; i++) {
    const randomIdx = Math.floor(Math.random() * charecters.length);
    res += charecters[randomIdx];
  }

  return res;
};

module.exports.generateShort = async () => {
  let short;
  let existingShort;
  do {
    short = generateRandom(process.env.LENGTH);
    existingShort = await Url.findOne({ shortUrl: short });
  } while (existingShort);

  return short;
};
