const { generateShort } = require("../config/generateShort");
const Url = require("../models/urlModel");
const formatDate = require("../util/formatDate");
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

router.get("/:shortUrl", async (req, res) => {
  try {
    const { shortUrl } = req.params;
    const { DAILY_LIMIT, HIT_REDIRECT } = process.env;

    const existingShortUrl = await Url.findOne({ shortUrl });
    if (!existingShortUrl) {
      return res.status(400).json({ message: "Invalid short url" });
    }

    const today = formatDate(new Date());
    if (today !== existingShortUrl.date) {
      existingShortUrl.dailyHit = 0;
      existingShortUrl.date = today;
    }

    existingShortUrl.hitCount++;
    existingShortUrl.dailyHit++;

    await existingShortUrl.save();

    if (existingShortUrl.dailyHit === Number(DAILY_LIMIT)) {
      return res.redirect("/");
    }

    if (existingShortUrl.hitCount % Number(HIT_REDIRECT) === 0) {
      return res.redirect(process.env.REDIRECT_URL);
    }

    res.redirect(existingShortUrl.url);
  } catch (error) {
    console.log(error);
    res.status(500).json({ message: "Internal Server Error" });
  }
});

module.exports = router;
