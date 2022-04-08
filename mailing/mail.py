from flask_mail import Mail
from server import build_application

app = build_application()
mail = Mail(app)

