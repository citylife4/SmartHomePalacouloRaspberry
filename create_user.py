from app import db, models
import flask_bcrypt

u = models.User(username='admin', email='admin@admin.com', password=flask_bcrypt.generate_password_hash('admin'))
db.session.add(u)
db.session.commit()
