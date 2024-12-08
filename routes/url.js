const { generateShort } = require("../config/generateShort");
const Url = require("../models/urlModel");
const router = require("express").Router();

router.post("/shorten", async (req, res) => {
  try {
    const { url } = req.body;

    const existingUrl = await Url.findOne({ url });
    if (existingUrl) {
      return res.status(200).json({ shortUrl: existingUrl.shortUrl });
    }

    const shortUrl = await generateShort();

    const newUrl = new Url({
      url,
      shortUrl,
    });

    await newUrl.save();
    return res.status(201).json({ shortUrl: newUrl.shortUrl });
  } catch (error) {
    res.status(500).json({ message: "Internal Server Error" });
    console.log(error);
  }
});

module.exports = router;
