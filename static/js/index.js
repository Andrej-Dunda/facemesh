const sqlite3 = require('sqlite3').verbose();
const db = new sqlite3.Database('facemesh.db');

db.run('CREATE TABLE fotos (foto_id INT PRIMARY KEY AUTOINCREMENT, elo_general INTEGER DEFAULT 1400, elo_male INTEGER DEFAULT 1400, elo_female INTEGER DEFAULT 1400)');
for(let i = 0; i < 32; i++) {
  db.run('INSERT INTO fotos DEFAULT VALUES', (err) => {
    if (err) {
      console.log(err.message);
      return;
    }
    console.log("Data inserted succesfully")
  });
}

db.all('SELECT * FROM fotos', (err, rows) => {
  if (err) {
    console.error(err.message);
    return;
  }
  console.log(rows);
});


// Parse the query parameters from the URL
const urlParams = new URLSearchParams(window.location.search);

// Retrieve the values of the "gender" and "age" parameters
const gender = urlParams.get('gender');
const age = urlParams.get('age');

// Do something with the retrieved data
age ? document.getElementById("age").innerText = age : window.location.href = "login.html";
gender ? document.getElementById("gender").innerText = gender : window.location.href = "login.html";

const changeData = () => {
  // Construct the URL with the variables as query parameters
  const url = 'login.html?gender=' + encodeURIComponent(gender) + '&age=' + encodeURIComponent(age);

  // Redirect to the URL
  window.location.href = url;
}