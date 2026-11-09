import os
import json


class ConfigManager:

    # Paleta completa por defecto (Tokyo Night dark). Así nunca crashea si falta algo (ya me pasó xd)
    DEFAULT_THEME = {
        "bg": "#1a1b26",
        "fg": "#c0caf5",
        "primary": "#7aa2f7",
        "secondary": "#24283b",
        "accent": "#bb9af7",
        "red": "#f7768e",
        "orange": "#ff9e64",
        "yellow": "#e0af68",
        "green": "#9ece6a",
        "teal": "#73dacb",
        "cyan": "#7dcfff",
        "blue": "#7aa2f7",
        "purple": "#bb9af7",
        "pink": "#f7768e",
        "comment": "#565f89",
        "selection": "#414868",
        "border": "#414868",
        "muted": "#a9b1d6",
        "subtle": "#9aa5ce",
        "bright": "#b4f9f8",
    }

    def __init__(self, path: str = None):
        self.config_path = path
        self._config = self._load()

    def _load(self):
        if not self.config_path or not os.path.exists(self.config_path):
            return {}
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error al parsear JSON: {e}")
            return {}
        except Exception as e:
            print(f"Error al cargar config: {e}")
            return {}

    def get(self, key: str, default: any = None):
        keys = key.split(".")
        value = self._config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value

    def get_theme(self) -> dict:
        theme_name = self.get("theme.name", "").strip()
        theme_mode = self.get("theme.mode", "dark").strip() or "dark"

        if not theme_name:
            print("theme.name vacío, usando DEFAULT_THEME")
            return dict(self.DEFAULT_THEME)

        themes_dir = os.path.join(os.path.dirname(__file__), "themes")
        theme_path = os.path.join(themes_dir, f"{theme_name}.json")

        if not os.path.exists(theme_path):
            print(f"No se encontró '{theme_name}', usando DEFAULT_THEME")
            return dict(self.DEFAULT_THEME)

        try:
            with open(theme_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"Error al cargar '{theme_name}': {e}")
            return dict(self.DEFAULT_THEME)

        mode_data = data.get("mode")
        if isinstance(mode_data, dict):
            palette = mode_data.get(theme_mode)
            if not isinstance(palette, dict):
                print(f"Variante '{theme_mode}' no existe, usando DEFAULT_THEME")
                return dict(self.DEFAULT_THEME)
            merged = dict(self.DEFAULT_THEME)
            merged.update(palette)
            return merged

        if "bg" in data and "fg" in data:
            merged = dict(self.DEFAULT_THEME)
            merged.update(data)
            return merged

        return dict(self.DEFAULT_THEME)
