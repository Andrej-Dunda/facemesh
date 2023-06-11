// Parse the query parameters from the URL
const urlParams = new URLSearchParams(window.location.search);

// Retrieve the values of the "gender" and "age" parameters
const age = urlParams.get('age');

// Do something with the retrieved data
document.getElementById("age").value = age ? parseInt(age) : 18;