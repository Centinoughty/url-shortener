const router = require("express").Router();

router.post("/shorten", (req, res) => {
  try {
    const { url } = req.body;
  } catch (error) {
    res.status(500).json({ message: "Internal Server Error" });
  }
});
