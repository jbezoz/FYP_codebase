const express = require('express');
const { exec } = require('child_process');

const app = express();

app.use(express.static('public'));

app.post('/runScript', (req, res) => {
    const command = 'python /home/theia/Documents/FYP/FYP_codebase/script.py';

    exec(command, (error, stdout, stderr) => {
        if (error) {
            console.error('Error:', error);
            res.status(500).send('Internal Server Error');
            return;
        }
        console.log('Output:', stdout);
        res.send(stdout);
    });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server is listening on port ${PORT}`);
});
