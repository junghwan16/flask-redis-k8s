import os
from src.presentation.app import create_app
from src.infrastructure.container import Container

container = Container()
app = create_app(container.counter_repository)

if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("DEBUG", "false").lower() == "true"
    
    app.run(host=host, port=port, debug=debug)