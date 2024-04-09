function print_hello() {
    document.write("Hello World!");
}

function runScript() {
    var command = "/home/theia/Documents/FYP/FYP_codebase/script.py"; // Specify the path to your Python script
    var child_process = require('child_process');
    
    child_process.exec(command, function(error, stdout, stderr) {
        if (error) {
            console.error('Error:', error);
            return;
        }
        console.log('Output:', stdout);
    });
}


