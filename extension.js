const vscode = require('vscode');
const { exec } = require('child_process');
const path = require('path');

function activate(context) {
    console.log('Extension "bomarkdown-color-theme" is now active!');

    // Enregistrer la commande
    let disposable = vscode.commands.registerCommand('extension.generateSnippets', function () {
        // Chemin vers le script Python dans le dossier 'src/snippets'
        const pythonScriptPath = path.join(__dirname, 'src', 'snippets', 'generate_snippets.py');

        // Exécuter le script Python
        exec(`python "${pythonScriptPath.replace(/\\/g, '/')}"`, (error, stdout, stderr) => {
            if (error) {
                vscode.window.showErrorMessage(`Erreur lors de l'exécution du script Python: ${error.message}`);
                console.error(`Erreur lors de l'exécution du script Python: ${error.message}`);
                return;
            }
            if (stderr) {
                vscode.window.showErrorMessage(`Erreur: ${stderr}`);
                console.error(`Erreur: ${stderr}`);
                return;
            }
            vscode.window.showInformationMessage('Snippets generated successfully!');
            console.log(`Sortie: ${stdout}`);
        });
    });

    context.subscriptions.push(disposable);
}

function deactivate() {}

module.exports = {
    activate,
    deactivate
};