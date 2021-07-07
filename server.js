const express = require("express");
const path = require("path");
var multer = require("multer");
const { spawn } = require("child_process");

var sessionActive = false;

const storage = multer.diskStorage({
  destination: function(req, file, cb) {
    console.log(file.fieldname);
    cb(null, "uploads");
  },
  filename: function(req, file, cb) {
    var savefile = "";
    if (file.fieldname == "csv") {
      savefile = "input.csv";
    } else if (file.fieldname == "names") {
      savefile = "names.txt";
    } else {
      savefile = "meta.txt";
    }

    cb(null, savefile);
  }
});

const upload_csv = multer({
  storage: storage
}).fields([
  { name: "csv", maxCount: 1 },
  { name: "names", maxCount: 1 },
  { name: "meta", maxCount: 1 }
]);

//setup env variables
const port = process.env.PORT || 80;
const output_path = `${__dirname}/output/generated-attendance.csv`;

//setup app
const app = express();
app.use(express.static(path.join(__dirname, "static")));
// app.use(express.urlencoded())

//settings of the app
app.set("view engine", "pug");
app.set("views", path.join(__dirname, "views"));

app.listen(port, () => {
  console.log("server started");
});

app.get("/", (req, res) => {
  res.status(200).render("index.pug", {});
});

app.get("/test", async (req, res) => {
  run_test(res);
});

app.post("/fileupload", upload_csv, async (req, res) => {
  console.log(sessionActive);
  if (!sessionActive) {
    console.log("fileupload " + sessionActive);
    await run_script(res);
  } else {
    res.status(200).send(`server is occupied, please try in a few minues`);
  }
});

async function run_script(res) {
  sessionActive = true;
  console.log("running script");
  const python = spawn("python3", ["generator.py"]);
  var process_code = 0;
  python.stdout.on("data", function(data) {});
  python.on("close", code => {
    console.log(`child process closed with code ${code}`);
    sessionActive = false;
    if (code == 0) {
      res.status(200).download(output_path);
    }
  });
}

async function run_test(res){
  sessionActive = true;
  const python = spawn("python3", ["test.py"]);
  python.on("close", code => {
    console.log(`child process closed with code ${code}`);
    sessionActive = false;
    if (code == 0) {
      res.status(200).send("finished testing");
    }
  });
}