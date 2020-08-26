from app_folder import app, db
from app_folder.models import User, Post

@app.shell_context_processor
def make_shell_context():
	return {'db':db, 'User': User, 'Post': Post}
app.run()
