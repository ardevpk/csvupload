// Check for File API support
if (window.File && window.FileReader && window.FileList && window.Blob) {
    // Great success! All the File APIs are supported.
} else {
    alert('The File APIs are not fully supported in this browser.');
}

// Select and upload file
// Click to select file
function selectFile(event){
    document.getElementById("file").click();
    document.getElementById("dropzoneLoading").className = "hidden";
    document.getElementById("dropzoneContent").className = "hidden";
    document.getElementById("dropzonePlaceholder").className = "";
    document.getElementById("dropzone").className = "";
    document.getElementById("dropzoneContent").innerHTML = "";
}
// Get and read selected file
function openFile(event) {
    // Loading
    document.getElementById("dropzonePlaceholder").className = "hidden";
    document.getElementById("dropzoneLoading").className = "";
    // Get selected file
    var input = event.target;
    var meta = input.files[0];
    var filename =  meta.name;
    // Check for valid file
    if((filename.substring((filename.length-4))).toLowerCase() != ".csv"){
        alert('Invalid file type');
        document.getElementById("dropzoneLoading").className = "hidden";
        document.getElementById("dropzonePlaceholder").className = "";
        return false;
    }
    // Read file
    var reader = new FileReader();
    reader.onload = function(){
        // Add filename to box
        document.getElementById("dropzoneLoading").className = "hidden";
        document.getElementById("dropzoneContent").innerHTML = filename;
        document.getElementById("dropzoneContent").className = "";
        document.getElementById("dropzone").className = "full";
    };
    reader.readAsText(input.files[0]);
    reader.onloadend = function(event){
        // Callback when done reading file
        strToJson(event);
    }
};

// Drag and drop file
function dragFile(event){
    // Prevent default behavior while dragging
    event.stopPropagation();
    event.preventDefault();
    event.dataTransfer.dropEffect = 'copy';
}
// Read file with FileReader
function dropFile(event){
    // Loading
    document.getElementById("dropzonePlaceholder").className = "hidden";
    document.getElementById("dropzoneLoading").className = "";
    // Prevent defaults
    event.stopPropagation();
event.preventDefault();
    // Get dropped file
    var files = event.dataTransfer.files;
    var meta = files[0];
    var filename =  meta.name;
    // Check for valid file
    if((filename.substring((filename.length-4))).toLowerCase() != ".csv"){
        alert('Invalid file type');
        document.getElementById("dropzoneLoading").className = "hidden";
        document.getElementById("dropzonePlaceholder").className = "";
        return false;
    }
    // Read file
    var reader = new FileReader();
    reader.onload = function(){
        // Add filename to box
        document.getElementById("dropzoneLoading").className = "hidden";
        document.getElementById("dropzoneContent").innerHTML = filename;
        document.getElementById("dropzoneContent").className = "";
        document.getElementById("dropzone").className = "full";
    };
    reader.readAsText(files[0]);
    reader.onloadend = function(event){
        // Callback when done reading file
        strToJson(event);
    }
}
// Bind events to functions to enable file drag and drop
var dropZone = document.getElementById('dropzone');
dropZone.addEventListener('dragover', dragFile, false);
dropZone.addEventListener('drop', dropFile, false);

// Process file string into JSON
function strToJson(event){
    // Get file from drop or select method
    var result;
    if("result" in event.target){
        result = event.target.result;
    } else {
        result = event.dataTransfer.files; 
    }
    // Split string into rows then columns
    var json = [], str, arrX, o, q, arr;
    var rows = result.split(/\r\n|\n/);
    for(var i=0, r; r=rows[i]; i++){
        // Only basic double quotes
        str = r.replace(/“|”/g, "\"");
        // Allow for commas if enclosed with double quotes
        arr = [];
        arrX = str.split('');
        o = 0;	// Offset of string
        q = false;	// Monitor if between quotes
        for(var j=0, k; k=arrX[j]; j++){
            if(k == "," && q === false){
                arr.push(str.substring(o, j));
                o = j + 1;
            }
            if(q === false && k == '"'){
                q = true;
                continue;
            }
            if(q === true && k == '"'){
                q = false;
            }
        }
        // String after last comma
        arr.push(str.substring(o, j));
        // Remove double quotes after checking for enclosed commas
        for(var j=0, k; k=arr[j]; j++){
            arr[j] = k.replace(/"/g, "");
        }
        // Add row to JSON array
        json.push(arr);
    }
    //console.log(json);
    // Do something with JSON of file data
    //console.log(JSON.stringify(json));
    jsonTable(json);
}

// JSON to HTML table
function jsonTable(json){
    /*var body = "<table>";
    for(var i=0, r; r=json[i]; i++){
        body += "\t<tr>";
        for(var j=0; j<json[i].length; j++){
            body += "\t\t<td>"+json[i][j]+"</td>";
        }
        body += "\t</tr>";
    }
    body += "</table>";*/
    body=json[json.length-1][0].replace(/,/g,"");
    body=body.replace(/html_point/g,",");
    document.getElementById("data").innerHTML = body;
    //console.log((json[json.length-1]));
}