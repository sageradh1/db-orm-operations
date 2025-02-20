import os

from dotenv import load_dotenv

from app import create_app

load_dotenv()


host = os.getenv("FLASK_HOST", "0.0.0.0")
port = int(os.getenv("FLASK_PORT", 8765))
isDebug = int(os.getenv("FLASK_DEBUG", True))

app = create_app()

if __name__ == "__main__":
    app.run(debug=isDebug, port=port, host=host)
