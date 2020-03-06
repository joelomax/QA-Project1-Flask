"""Logged-in page routes."""
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user
from flask import current_app as app
from .assets import compile_auth_assets
from .assets import compile_main_assets
from flask_login import login_required, logout_user
from .models import db, User, Playlist
from .forms import SignupForm, PlaylistForm


# Blueprint Configuration
main_bp = Blueprint('main_bp', __name__,
                    template_folder='templates',
                    static_folder='static')
compile_auth_assets(app)
compile_main_assets(app)


@main_bp.route('/', methods=['GET'])
@login_required
def dashboard():
    """Serve logged-in Dashboard."""
    return render_template('dashboard.jinja2',
                           title='Welcome to Songbox!',
                           template='dashboard-template',
                           current_user=current_user,
                           body="You are now logged in!")


@main_bp.route("/logout")
@login_required
def logout():
    """User log-out logic."""
    logout_user()
    return redirect(url_for('auth_bp.login'))


@main_bp.route('/useradmin/', methods=['GET', 'POST'])
@login_required
def useradmin():

	# User list administration.
	action = request.args.get('action')
	id = request.args.get('id')
	userform = SignupForm()

	if request.method == 'GET':
		if action == 'New':
			# New user dialog.
			return render_template('usernew.jinja2',
				title='Create an Account.',
				form=userform,
				template='signup-page',
				body="Create a New User")
		elif action == 'Edit':
			# Edit data for existing user.
			userdata = User.query.filter_by(id=id).first() 	# Get user data from database.
			userform = SignupForm(obj=userdata) 		# Populate user form with data from database.
			return render_template('usernew.jinja2',
				title="Edit User Details.",
				form=userform,
				template='signup-page',
				body="Edit User Details")
		elif action == 'Delete':
			# Delete user record.
			User.query.filter_by(id=id).delete()
			db.session.commit()

		# List users in table
		users = User.query.all()
		return render_template('userlist.jinja2',users=users)

	elif request.method == 'POST':
		if userform.validate_on_submit():
			email = userform.email.data
			if User.query.filter_by(email=email).first() is None:
				# User data does not exist in table
				userdata = User(name=userform.name.data, email=userform.email.data)
				userdata.set_password(userform.password.data)
				db.session.add(userdata) 		# Add the new record
				db.session.commit()
			else:
				# User data already exists in table.
				if action == 'New':
					# Don't allow user data to be overwritten.
					flash('A user already exists with that email address.')
					return redirect(url_for('main_bp.useradmin', action='New'))
				elif action == 'Edit':
					# Do allow user data to be overwritten.
					userdata = User.query.filter_by(id=id).first() 	# Get original database record.
					userform.populate_obj(userdata) 		# Copy edited fields from form to database record.
					userdata.set_password(userform.password.data) 	# Re-encrypt password into database record.
					db.session.commit() 

	return redirect(url_for('main_bp.useradmin'))



@main_bp.route('/playlistadmin/', methods=['GET', 'POST'])
@login_required
def playlistadmin():

	# Playlist administration.
	action = request.args.get('action')
	item_id = request.args.get('item_id')
	form = PlaylistForm()

	if request.method == 'GET':
		if action == 'New':
			# New user dialog.
			return render_template('playlistnew.jinja2',
				title='Create a Playlist',
				form=form,
				template='playlistnew',
				body="Create a Playlist")
		elif action == 'Edit':
			# Edit data for existing playlist
			data = Playlist.query.filter_by(item_id=item_id).first() 	# Get playlist data from database.
			form = PlaylistForm(obj=data) 					# Populate playlist form with data from database.
			return render_template('playlistnew.jinja2',
				title="Edit Playlist Details.",
				form=form,
				template='playlistnew',
				body="Edit Playlist Details")
		elif action == 'Delete':
			# Delete user record.
			Playlist.query.filter_by(item_id=item_id).delete()
			db.session.commit()

		# List users in table
		data = Playlist.query.all()
		return render_template('playlistadmin.jinja2',playlistdata=data)

	elif request.method == 'POST':
		if form.validate_on_submit():
			
			if action == 'Edit':
				# Get original database record
				data = Playlist.query.filter_by(item_id=item_id).first()
				form.populate_obj(data) 		# Copy edited fields from form to database record.
				db.session.commit()
			else:
				# Create empty data record
				data = Playlist()
				form.populate_obj(data) 		# Copy edited fields from form to database record.
				db.session.add(data) 			# Add the new record
				db.session.commit()

	return redirect(url_for('main_bp.playlistadmin'))
