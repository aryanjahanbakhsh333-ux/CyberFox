from app_factory import create_app
from api_routes import register_api_routes


app = create_app()

register_api_routes(app)


@app.get("/")
def home():
    return {
        "service": "Cybersecurity AI Platform",
        "status": "online",
        "version": "1.0.0"
    }


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
