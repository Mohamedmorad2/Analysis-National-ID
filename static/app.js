document.getElementById('nationalIdForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const nationalId = document.getElementById('nationalId').value;

    const response = await fetch('/validate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ nationalId })
    });
    
    const result = await response.json();
    
    if (result.valid) {
        displayResult(result);
    } else {
        document.getElementById('result').innerHTML = "<p>Invalid National ID. Please correct and try again.</p>";
    }
});

function clearFields() {
    document.getElementById('nationalIdForm').reset();
    document.getElementById('result').innerHTML = '';
}
function displayResult(data) {
    var table = "<h3>Analysis Results</h3>";
    table += "<style>table { width: 100%; border-collapse: collapse; } th, td { padding: 8px; text-align: left; }</style>"; // CSS for table styling
    table += "<table border='1'>";
    table += "<tr><th>Category</th><th>Details</th></tr>";
    table += "<tr><td>Date of Birth</td><td>" + data.birthYear + "/" + data.birthMonth + "/" + data.birthDay + "</td></tr>";
    table += "<tr><td>Age</td><td>" + data.age + "</td></tr>";
    table += "<tr><td>Gender</td><td>" + data.gender + "</td></tr>";
    table += "<tr><td>Governorate</td><td>" + data.governorate + "</td></tr>";
    table += "</table>";

    document.getElementById('result').innerHTML = table;
}

