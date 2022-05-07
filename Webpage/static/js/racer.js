document.addEventListener("DOMContentLoaded", () => CreateTableFromJSON())
document.addEventListener("DOMContentLoaded", () => CreateDropdownFromJSON(dropdown_url = 'category',dropdown = 'category'))

setInterval(() => CreateTableFromJSON(), 1000)

function CreateTableFromJSON() {
    const params = new Proxy(new URLSearchParams(window.location.search), {
        get: (searchParams, prop) => searchParams.get(prop),
      });
      // Get the value of "some_key" in eg "https://example.com/?some_key=some_value"
      let event = params.event; // "some_value"

    var category = document.getElementById('category').value;
        // Get the reciever endpoint from Python using fetch:
    fetch("/api/race", 
    {
    method: 'POST',
    headers: {
    'Content-type': 'application/json',
    'Accept': 'application/json'
    },
    // Strigify the payload into JSON:
    body:JSON.stringify({'event':event,'category': category})})
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
    )}

function CreateDropdownFromJSON(dropdown_url,dropdown_location) {
        let dropdown = document.getElementById(dropdown_location);
        dropdown.length = 0;
        let defaultOption = document.createElement('option');
        defaultOption.text = 'Choose Category';
    
        dropdown.add(defaultOption);
        dropdown.selectedIndex = 0;
    
        const url = '/api/dropdown/'+ dropdown_url;
    
        fetch(url,{method: 'POST'})  
        .then(  
            function(response) {  
            if (response.status !== 200) {  
                console.warn('Looks like there was a problem. Status Code: ' + 
                response.status);  
                return;  
            }
    
            // Examine the text in the response  
            response.json().then(function(data) {  
                let option;
            
                for (let i = 0; i < data.length; i++) {
                option = document.createElement('option');
                option.text = data[i].f2;
                option.value = data[i].f1;
                dropdown.add(option);
                }    
            });  
            }  
        )  
        .catch(function(err) {  
            console.error('Fetch Error -', err);  
        });
}