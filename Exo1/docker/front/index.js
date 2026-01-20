const express = require('express');
const axios = require('axios');

const app = express();
const PORT = 3000;
const BACKEND_URL = "http://backend:5000/api/hello";

app.get("/", async (req, res) => {
  try {
    const response = await axios.get(BACKEND_URL);
    res.send(`<h1>${response.data.message}</h1>`);
  } catch (err) {
    res.status(500).send("Erreur lors de la récupération du message");
  }
});

app.listen(PORT, () => console.log(`Frontend running on http://localhost:${PORT}`));
