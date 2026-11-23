from app import create_app
from app.extensions import db
from app.models.oauth import OAuth2Client
import os

app = create_app()

with app.app_context():
    secret = os.environ.get("CODEARENA_CLIENT_SECRET")

    if not secret:
        raise RuntimeError("CODEARENA_CLIENT_SECRET is missing. Generate it again in this terminal.")

    client = OAuth2Client.query.filter_by(
        client_id="codearena-client"
    ).first()

    if client:
        print("CodeArena client already exists. No duplicate created.")
    else:
        client = OAuth2Client(
            client_id="codearena-client",
            client_secret=secret
        )

        client.set_client_metadata({
            "client_name": "CodeArena",
            "client_uri": "http://127.0.0.1:5001",
            "grant_types": ["authorization_code"],
            "response_types": ["code"],
            "scope": "profile email",
            "redirect_uris": ["http://127.0.0.1:5001/callback"],
            "token_endpoint_auth_method": "client_secret_basic"
        })

        db.session.add(client)
        db.session.commit()

        print("CodeArena OAuth client registered successfully.")

    print("Client ID: codearena-client")
    print("Client secret configured:", bool(secret))
    print("Redirect URI: http://127.0.0.1:5001/callback")
