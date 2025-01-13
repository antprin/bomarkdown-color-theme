import os
import json


def get_vscode_paths():
    """Retourne les chemins principaux de VS Code selon l'OS."""
    if os.name == 'nt':  # Windows
        user_settings = os.path.join(os.getenv('APPDATA', ''), 'Code', 'User', 'settings.json')
        extensions_path = os.path.join(os.getenv('USERPROFILE', ''), '.vscode', 'extensions')
    else:  # MacOS/Linux
        user_settings = os.path.join(os.path.expanduser('~'), '.config', 'Code', 'User', 'settings.json')
        extensions_path = os.path.join(os.path.expanduser('~'), '.vscode', 'extensions')
    return user_settings, extensions_path


def find_file(extension_path, extension_name, target_file):
    """Recherche un fichier spécifique dans une extension VSC donnée."""
    for root, _, files in os.walk(extension_path):
        if extension_name in root and target_file in files:
            return os.path.join(root, target_file)
    return None


def load_json_file(file_path):
    """Charge le contenu d'un fichier JSON s'il existe."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Erreur lors du chargement du fichier {file_path} : {e}")
        return {}


def generate_snippet(prefix, keys, description):
    """Génère un snippet dynamique."""
    return {
        "prefix": prefix,
        "body": [f"{prefix}${{1|{','.join(keys)}|}}"],
        "description": description,
    }


def main():
    # Obtenir les chemins principaux
    user_settings_path, extensions_path = get_vscode_paths()

    # Charger le fichier settings.json
    settings = load_json_file(user_settings_path)
    if not settings:
        print("Impossible de charger les paramètres utilisateur du settings.json.")
        return

    # Extraire les clés des paramètres spécifiques
    status_keys = settings.get("bomarkdown.status", {}).keys()
    bubbles_keys = settings.get("bomarkdown.bubbles", {}).keys()
    links_keys = settings.get("bomarkdown.Linksdefinition", {}).keys()

    # Trouver le fichier UserIcons.json
    extension_name = "bomarkdown"
    target_file = "UserIcons.json"
    user_icons_path = find_file(extensions_path, extension_name, target_file)

    # Charger les icônes si le fichier existe
    icon_names = []
    if user_icons_path:
        icon_data = load_json_file(user_icons_path)
        icon_names = [icon.get('name', '') for icon in icon_data if 'name' in icon]

    # Générer les snippets dynamiques
    dynamic_snippets = {
        "InsertStatus": generate_snippet("(s:", status_keys, "Insert a status key from bomarkdown.status"),
        "InsertBubbles": generate_snippet("(b:", bubbles_keys, "Insert a bubble key from bomarkdown.bubbles"),
        "InsertLinks": generate_snippet("(l:", links_keys, "Insert a link key from bomarkdown.Linksdefinition"),
        "InsertIcons": generate_snippet("(i:", icon_names, "Insert an icon name from UserIcons.json"),
    }

    # Déclaration des snippets statiques
    static_snippets = {
        "InsertEffectivityExpression": {
            "prefix": "(e:",
            "body": ["(e:${1|[Jalon1 ->Jalon2],[Jalon1 ->oo[|}"],
            "description": "Insert a close or open sample effectivity expression",
        },
        "InsertAlias": {
            "prefix": "(a:",
            "body": ["(a:"],
            "description": "Insert an alias key",
        },
    }

    # Chemin du fichier snippets
    snippets_path = os.path.join(os.path.dirname(__file__), 'snippets.code-snippets')

    # Charger et mettre à jour les snippets existants
    existing_snippets = load_json_file(snippets_path)
    existing_snippets.update(static_snippets)
    existing_snippets.update(dynamic_snippets)

    # Sauvegarder les snippets mis à jour
    with open(snippets_path, 'w', encoding='utf-8') as f:
        json.dump(existing_snippets, f, ensure_ascii=False, indent=4)

    print(f">>> Snippets générés avec succès dans {snippets_path}")


if __name__ == "__main__":
    main()