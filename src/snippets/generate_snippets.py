import os
import json

# Chemin vers le fichier settings.json de l'utilisateur
settings_path = os.path.join(os.path.expanduser('~'), 'AppData', 'Roaming', 'Code', 'User', 'settings.json')

# Chemin vers le fichier snippets.code-snippets dans le dossier src/snippets de l'extension
snippets_path = os.path.join(os.path.dirname(__file__), 'snippets.code-snippets')

# Chemin vers le dossier extensions de Visual Studio Code
vscode_extensions_path = os.path.join(os.path.expanduser('~'), '.vscode', 'extensions')
icon_config_file = None

# Trouver le dossier de l'extension utilisateur qui commence par 'roeperni.bomarkdown'
for item in os.listdir(vscode_extensions_path):
    if item.startswith('roeperni.bomarkdown'):
        icon_config_file = os.path.join(vscode_extensions_path, item, 'IconConfig', 'UserIcons.json')
        break

# Lire le fichier settings.json
with open(settings_path, 'r', encoding='utf-8') as f:
    settings = json.load(f)

# Fonction pour extraire les clés d'une entrée spécifique
def extract_keys(entry_key):
    entries = settings.get(entry_key, {})
    return list(entries.keys())

# Extraire les clés des entrées spécifiques
satus_keys = extract_keys('bomarkdown.satus')
bubbles_keys = extract_keys('bomarkdown.bubbles')
linksdefinition_keys = extract_keys('bomarkdown.Linksdefinition')

# Afficher les clés
print('satus keys:', satus_keys)
print('bubbles keys:', bubbles_keys)
print('linksdefinition keys:', linksdefinition_keys)

# Fonction pour extraire les clés 'name' du fichier UserIcons.json
def extract_icon_names(icon_config_file):
    if icon_config_file and os.path.exists(icon_config_file):
        with open(icon_config_file, 'r', encoding='utf-8') as f:
            icon_config = json.load(f)
            return [icon['name'] for icon in icon_config]
    return []

# Extraire les noms des icônes
icon_names = extract_icon_names(icon_config_file)
print('icon names:', icon_names)

# Déclaration en dur des snippets non customisables
static_snippets = {
    "InsertEffectivityExpression": {
        "prefix": "(e:",
        "body": [
            "(e:${1|[Jalon1 ->Jalon2],[Jalon1 ->oo[|}"
        ],
        "description": "Insert a close or open sample effectivity expression"
    },
    "InsertAlias": {
        "prefix": "(a:",
        "body": [
            "(a:"
        ],
        "description": "Insert an alias key"
    }
}

# Fonction pour générer des snippets dynamiques
def generate_dynamic_snippet(prefix, keys, description):
    return {
        "prefix": prefix,
        "body": [
            f"{prefix}${{1|{','.join(keys)}|}}"
        ],
        "description": description
    }

# Générer le contenu des snippets customisables par l'utilisateur
dynamic_snippets = {
    "InsertStatus": generate_dynamic_snippet("(s:", satus_keys, "Insert a status key from bomarkdown.status"),
    "InsertBubbles": generate_dynamic_snippet("(b:", bubbles_keys, "Insert a bubble key from bomarkdown.bubbles"),
    "InsertLinks": generate_dynamic_snippet("(l:", linksdefinition_keys, "Insert a link key from bomarkdown.linksdefinition"),
    "InsertIcons": generate_dynamic_snippet("(i:", icon_names, "Insert an icon name from UserIcons.json")
}

# Lire le contenu existant du fichier snippets.code-snippets
if os.path.exists(snippets_path):
    with open(snippets_path, 'r', encoding='utf-8') as snippets_file:
        existing_snippets = json.load(snippets_file)
else:
    existing_snippets = {}

# Mettre à jour le contenu existant avec les snippets statiques et dynamiques
existing_snippets.update(static_snippets)
existing_snippets.update(dynamic_snippets)

# Écrire le contenu mis à jour dans le fichier snippets.code-snippets
with open(snippets_path, 'w', encoding='utf-8') as snippets_file:
    json.dump(existing_snippets, snippets_file, ensure_ascii=False, indent=4)

print('Snippets generated successfully.')