import json
import os

class LanguagePresets:
    def __init__(self):
        self.presets_file = os.path.join('resources', 'language_presets.json')
        self.presets = self.load_presets()

    def load_presets(self):
        if os.path.exists(self.presets_file):
            with open(self.presets_file, 'r') as f:
                return json.load(f)
        return {}

    def get_supported_languages(self):
        return list(self.presets.keys())

    def get_presets(self, language):
        return self.presets.get(language, {})
