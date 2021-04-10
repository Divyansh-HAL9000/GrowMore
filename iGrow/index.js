var Express = require("express");
var admin = require("firebase-admin");
var serviceAccount = require("./firebase/service-account.json");
var Firebase = require("firebase");
var morgan = require("morgan");
var bodyParser = require("body-parser");

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount)
});
console.log("connected to service account");
const app = Express();
const port = 3000;

app.get("/", (req, res) => {
  res.send("welcome home");
});


app.get("/monitor", (req, res) => {
    res.sendFile("monitor.html", {root : __dirname});
});

app.get("/about", (req, res) => {
  res.sendFile("axiostest.html", {root : __dirname});
});


app.listen(port, ()=> console.log("listening on port : " + port));