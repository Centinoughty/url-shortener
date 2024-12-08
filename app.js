const express = require("express");
const { connectDb } = require("./config/db");
require("dotenv").config();

const urlRoutes = require("./routes/url");

const app = express();
const PORT = process.env.PORT;

app.use(express.json());

app.use("/", urlRoutes);

connectDb();
app.listen(PORT, () => {
  console.log(`Listening on port ${PORT}`);
});
