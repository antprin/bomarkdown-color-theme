const { exec } = require('child_process');
const path = require('path');
const fs = require('fs');

// Chemin vers le script Python dans le dossier 'snippets'
const pythonScriptPath = path.join(__dirname, 'generate_snippets.py');

// Chemin vers le fichier de log
const logFilePath = path.join(__dirname, 'postinstall.log');

// Fonction pour écrire les logs
function logMessage(message) {
    fs.appendFileSync(logFilePath, `${new Date().toISOString()} - ${message}\n`);
}

// Afficher la valeur de pythonScriptPath
logMessage(`Chemin vers le script Python: ${pythonScriptPath}`);
console.log(`Chemin vers le script Python: ${pythonScriptPath}`);

// Exécuter le script Python
exec(`python "${pythonScriptPath}"`, (error, stdout, stderr) => {
    if (error) {
        logMessage(`Erreur lors de l'exécution du script Python: ${error.message}`);
        console.error(`Erreur lors de l'exécution du script Python: ${error.message}`);
        return;
    }
    if (stderr) {
        logMessage(`Erreur: ${stderr}`);
        console.error(`Erreur: ${stderr}`);
        return;
    }
    logMessage(`Sortie: ${stdout}`);
    console.log(`Sortie: ${stdout}`);
});