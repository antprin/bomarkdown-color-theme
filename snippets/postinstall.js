const { exec } = require('child_process');
const path = require('path');

// Chemin vers le script Python
const pythonScriptPath = path.join(__dirname, 'generate_snippets.py');

// Exécuter le script Python
exec(`python "${pythonScriptPath}"`, (error, stdout, stderr) => {
    if (error) {
        console.error(`Erreur lors de l'exécution du script Python: ${error.message}`);
        return;
    }
    if (stderr) {
        console.error(`Erreur: ${stderr}`);
        return;
    }
    console.log(`Sortie: ${stdout}`);
});