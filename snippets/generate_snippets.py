import json
import os

# Chemin vers le fichier settings.json de l'utilisateur
settings_path = os.path.expanduser("~/AppData/Roaming/Code/User/settings.json")

# Chemin vers le fichier snippets.code-snippets
snippets_path = "./snippets/snippets.code-snippets"

# Lire le fichier settings.json
with open(settings_path, 'r') as settings_file:
    settings = json.load(settings_file)

# Fonction pour extraire les clés d'une entrée spécifique
def extract_keys(entry_key):
    entries = settings.get(entry_key, {})
    return list(entries.keys())

# Extraire les clés des entrées spécifiques
satus_keys = extract_keys("bomarkdown.satus")
bubbles_keys = extract_keys("bomarkdown.bubbles")
linksdefinition_keys = extract_keys("bomarkdown.Linksdefinition")

# Afficher les clés
print("satus keys:", satus_keys)
print("bubbles keys:", bubbles_keys)
print("linksdefinition keys:", linksdefinition_keys)

# Déclaration en dur des snippets non customisables
static_snippets = {
    "InsertEffectivityExpression": {
        "prefix": "(e:",
        "body": [
            "(e:${1|[Jalon1 ->Jalon2],[Jalon1 ->oo[|})"
        ],
        "description": "Insert a close or open sample effectivity expression"
    },
}

# Générer le contenu des snippets customisables par le user
dynamic_snippets = {
    "InsertStatus": {
        "prefix": "(s:",
        "body": [
            "(s:${1|" + ",".join(satus_keys) + "|})"
        ],
        "description": "Insert a status key from bomarkdown.status"
    },
    "InsertBubbles": {
        "prefix": "(b:",
        "body": [
            "(b:${1|" + ",".join(bubbles_keys) + "|})"
        ],
        "description": "Insert a bubble key from bomarkdown.bubbles"
    },
    "InsertLinks": {
        "prefix": "(l:",
        "body": [
            "(l:${1|" + ",".join(linksdefinition_keys) + "|})"
        ],
        "description": "Insert a link key from bomarkdown.linksdefinition"
    }        
}

# Lire le contenu existant du fichier snippets.code-snippets
if os.path.exists(snippets_path):
    with open(snippets_path, 'r') as snippets_file:
        existing_snippets = json.load(snippets_file)
else:
    existing_snippets = {}

# Mettre à jour le contenu existant avec les snippets statiques et dynamiques
existing_snippets.update(static_snippets)
existing_snippets.update(dynamic_snippets)

# Écrire le contenu mis à jour dans le fichier snippets.code-snippets
with open(snippets_path, 'w') as snippets_file:
    json.dump(existing_snippets, snippets_file, indent=4)

print("Snippets generated successfully.")