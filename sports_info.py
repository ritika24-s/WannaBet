import os

from sportspro import create_app

app = create_app()

if __name__ == "__main__":
    app.run(os.environ.get("DEBUG", True))