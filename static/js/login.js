// Parse the query parameters from the URL
const urlParams = new URLSearchParams(window.location.search);

// Retrieve the values of the "gender" and "age" parameters
const gender = urlParams.get('gender');
const age = urlParams.get('age');

// Do something with the retrieved data
gender === "Žena" ? document.getElementById("gender-female").checked = true : document.getElementById("gender-male").checked = true;
document.getElementById("age").value = age ? parseInt(age) : 18;