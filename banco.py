from Site import database,app
from Site.models import Usuario,Post

with app.app_context():
    database.create_all()