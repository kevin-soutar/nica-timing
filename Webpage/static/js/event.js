document.addEventListener("DOMContentLoaded", () => EventSelectionFromJSON())

function EventSelectionFromJSON() {
        // Get the reciever endpoint from Python using fetch:
    fetch("/api/event", 
    {
    method: 'POST',
    headers: {
    'Content-type': 'application/json',
    'Accept': 'application/json'
    },
    // Strigify the payload into JSON:
    body:JSON.stringify({'category': 'test'})})
    .then(res=>res.json()).then(list=>
        {
          var cols = [];
            for (var i = 0; i < list.length; i++) {
                for (var k in list[i]) {
                    if (cols.indexOf(k) === -1) {
                         
                        // Push all keys to the array
                        cols.push(k);
                    }
                }
            }  
          // Create a table element
            var table = document.createElement("table");
             
            // Create table row tr element of a table
            var tr = table.insertRow(-1);
             
            for (var i = 0; i < cols.length; i++) {
                 
                // Create the table header th element
                var theader = document.createElement("th");
                theader.innerHTML = cols[i];
                 
                // Append columnName to the table row
                tr.appendChild(theader);
            }
             
            // Adding the data to the table
            for (var i = 0; i < list.length; i++) {
                 
                // Create a new row
                trow = table.insertRow(-1);
                let href = `/backend/event?event=${list[i][cols[2]]}`
                trow.addEventListener("click", () => { window.location = href; });
                for (var j = 0; j < cols.length; j++) {
                    var cell = trow.insertCell(-1);
                     
                    // Inserting the cell at particular place
                    cell.innerHTML = list[i][cols[j]];
                }
            }
             
            // Add the newly created table containing json data
            var el = document.getElementById("table");
            el.innerHTML = "";
            el.appendChild(table);   
        }
    )};