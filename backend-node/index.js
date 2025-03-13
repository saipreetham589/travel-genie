const express = require("express");
const axios = require("axios");
const dotenv = require("dotenv");
const cors = require("cors");

dotenv.config();
const app = express();

app.use(cors());
app.use(express.json());

app.get("/", (req, res) => {
  res.send("Travel Genie Node.js API is Running!");
});

app.get("/ai-itinerary", async (req, res) => {
  try {
    const response = await axios.get("http://backend-python:8000/");
    res.json(response.data);
  } catch (error) {
    res.status(500).send("Error connecting to AI service");
  }
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`Node.js server running on port ${PORT}`);
});