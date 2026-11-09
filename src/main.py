import sys
from pathlib import Path
from src.app import App


def main():
    try:
        project_root = Path(__file__).parent.parent
        config_path = project_root / "config.json"

        if not config_path.exists():
            print("No se encontró config.json, usando defaults")
            config_path = None

        app = App(config_path=str(config_path) if config_path else None)
        app.run()

    except KeyboardInterrupt:
        print("Aplicación cerrada por usuario")
    except Exception as e:
        print(f"Error fatal {e}")
        sys.exit(1)
