import json

# Öffne die JSON-Datei und lade den Inhalt
with open('api_token.json', 'r') as api_file:
    api_token_file = json.load(api_file)

# Extrahiere die Variable aus den Daten
api_token = api_token_file['Hugging_face_token']
open_ai_token = api_token_file['Open_api_token']
print(api_token, open_ai_token)