
from flask import Flask, redirect, url_for, session, render_template_string
from authlib.integrations.flask_client import OAuth
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv(Path(__file__).with_name(".env"))

app = Flask(__name__)
app.config["SESSION_COOKIE_NAME"] = "codearena_session"
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.secret_key = os.environ.get("CODEARENA_SESSION_SECRET") or os.urandom(32)

oauth = OAuth(app)

oauth.register(
    name="authvanta",
    client_id="codearena-client",
    client_secret=os.environ.get("CODEARENA_CLIENT_SECRET"),
    authorize_url="http://127.0.0.1:5000/oauth/authorize",
    access_token_url="http://127.0.0.1:5000/oauth/token",
    client_kwargs={
        "scope": "profile email",
        "code_challenge_method": "S256"
    }
)

STYLE = """
<style>
*{box-sizing:border-box}
body{
    margin:0;min-height:100vh;
    font-family:Arial,sans-serif;
    color:#172033;
    background:linear-gradient(135deg,#f7f7ff,#eef2ff,#f8faff);
}
nav{
    height:75px;padding:0 8%;
    display:flex;align-items:center;justify-content:space-between;
    background:#ffffffd9;border-bottom:1px solid #e7e9f4;
}
.logo{font-size:25px;font-weight:800;color:#6938e8}
.logo span{color:#182238}
.navtag{color:#68738a;font-size:13px}
main{
    min-height:calc(100vh - 135px);
    display:flex;align-items:center;justify-content:center;
    padding:35px 20px;
}
.card{
    width:100%;max-width:470px;padding:45px;
    text-align:center;background:white;border:1px solid #e8e9f4;
    border-radius:20px;box-shadow:0 15px 50px #313c6812;
}
.symbol{
    width:76px;height:76px;margin:0 auto 20px;
    display:flex;align-items:center;justify-content:center;
    border-radius:22px;background:#f0eaff;color:#713ee9;
    font-size:42px;font-weight:bold;
}
h1{font-size:29px;margin:12px 0;color:#172033}
p{color:#69748a;line-height:1.7;font-size:14px}
.btn{
    display:block;width:100%;padding:15px;margin-top:25px;
    border:0;border-radius:9px;background:linear-gradient(90deg,#7040e9,#5830d5);
    color:white;text-decoration:none;font-weight:bold;font-size:15px;
    cursor:pointer;
}
.btn:hover{opacity:.92}
.secondary{
    display:block;width:100%;padding:14px;margin-top:12px;
    border:1px solid #e0e3ed;border-radius:9px;
    color:#293247;text-decoration:none;font-weight:bold;
}
.secure{margin-top:24px;font-size:12px;color:#8992a5}
.success{
    width:76px;height:76px;margin:0 auto 20px;
    display:flex;align-items:center;justify-content:center;
    background:#dcfce8;color:#16a34a;border-radius:50%;font-size:42px;
}
.details{
    margin-top:25px;padding:20px;text-align:left;
    background:#fafaff;border:1px solid #e8e9f4;border-radius:12px;
}
.detail{
    display:flex;justify-content:space-between;gap:15px;
    padding:10px 0;font-size:13px;border-bottom:1px solid #eceef5;
}
.detail:last-child{border:0}
.detail span:first-child{color:#778198}
.detail span:last-child{font-weight:bold;color:#263149}
.notice{
    padding:15px;margin-top:22px;text-align:left;
    border:1px solid #a7efc0;background:#f0fdf4;
    color:#176b37;border-radius:9px;font-size:13px;line-height:1.6;
}
footer{text-align:center;padding:20px;color:#929bad;font-size:12px}
@media(max-width:500px){.card{padding:30px 22px}nav{padding:0 5%}}
</style>
"""

HOME_PAGE = """
<!DOCTYPE html>
<html>
<head>
<title>CodeArena | Secure Coding Platform</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
""" + STYLE + """
</head>
<body>
<nav>
    <div class="logo">Code<span>Arena</span></div>
    <div class="navtag">SECURE DEVELOPER PLATFORM</div>
</nav>
<main>
    <section class="card">
        <div class="symbol">&lt;/&gt;</div>
        <h1>Welcome to <span style="color:#7040e9">CodeArena</span></h1>
        <p>Practice. Compete. Improve.</p>
        <p>Sign in securely with AUTHVANTA to access your coding platform.</p>
        <a class="btn" href="/login">♙ &nbsp; Sign in with AUTHVANTA</a>
        <div class="secure">♙ &nbsp; Secure &nbsp; • &nbsp; Simple &nbsp; • &nbsp; Seamless</div>
    </section>
</main>
<footer>© 2026 CodeArena | Secure authentication powered by AUTHVANTA</footer>
</body>
</html>
"""

SUCCESS_PAGE = """
<!DOCTYPE html>
<html>
<head>
<title>Authentication Successful | CodeArena</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
""" + STYLE + """
</head>
<body>
<nav>
    <div class="logo">Code<span>Arena</span></div>
    <div class="navtag">SECURE DEVELOPER PLATFORM</div>
</nav>
<main>
    <section class="card">
        <div class="success">✓</div>
        <h1>Authentication Successful!</h1>
        <p>You have successfully authenticated with AUTHVANTA.</p>
        <div class="notice">
            ✓ &nbsp; CodeArena received an OAuth 2.0 access token.
            You can now continue to the application.
        </div>
        <div class="details">
            <div class="detail"><span>Provider</span><span>AUTHVANTA</span></div>
            <div class="detail"><span>Status</span><span style="color:#16a34a">Success</span></div>
            <div class="detail"><span>Scope</span><span>profile, email</span></div>
            <div class="detail"><span>Authenticated at</span><span>__TIME__</span></div>
        </div>
        <a class="btn" href="/">⌂ &nbsp; Go to CodeArena Home</a>
        <a class="secondary" href="/logout">Logout</a>
        <div class="secure">♙ &nbsp; Secured by AUTHVANTA OAuth 2.0</div>
    </section>
</main>
<footer>© 2026 CodeArena | Secure Identity. Smarter Access.</footer>
</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(HOME_PAGE)


@app.route("/login")
def login():
    if not os.environ.get("CODEARENA_CLIENT_SECRET"):
        return "CodeArena client secret is not configured.", 500

    redirect_uri = url_for("callback", _external=True)
    return oauth.authvanta.authorize_redirect(
        redirect_uri,
        code_challenge_method="S256"
    )


@app.route("/callback")
def callback():
    try:
        token = oauth.authvanta.authorize_access_token()

        if not token or not token.get("access_token"):
            return "Authentication failed: access token not received.", 400

        session["access_token"] = token["access_token"]
        session["authenticated_at"] = datetime.now().strftime("%d %b %Y, %H:%M:%S")

        success_page = SUCCESS_PAGE.replace(
            "__TIME__",
            session["authenticated_at"]
        )
        return render_template_string(success_page)

    except Exception:
        app.logger.exception("AUTHVANTA OAuth callback failed")
        return "Authentication failed. Check the AUTHVANTA server and terminal logs.", 400


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=False)
