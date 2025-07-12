from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import os
from werkzeug.utils import secure_filename
from config import Config
from models import db, User, ClothingItem
from forms import ItemForm

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    items = ClothingItem.query.filter_by(status='available').all()
    return render_template('index.html', items=items)

@app.route('/dashboard')
@login_required
def dashboard():
    my_items = ClothingItem.query.filter_by(uploader_id=current_user.id).all()
    return render_template('dashboard.html', user=current_user, items=my_items)

@app.route('/item/<int:item_id>')
def item_detail(item_id):
    item = ClothingItem.query.get_or_404(item_id)
    return render_template('item_detail.html', item=item)

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_item():
    form = ItemForm()
    if form.validate_on_submit():
        filename = secure_filename(form.image.data.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        form.image.data.save(image_path)
        
        new_item = ClothingItem(
            title=form.title.data,
            description=form.description.data,
            category=form.category.data,
            size=form.size.data,
            condition=form.condition.data,
            tags=form.tags.data,
            image=filename,
            uploader_id=current_user.id
        )
        db.session.add(new_item)
        db.session.commit()
        flash('Item added successfully!')
        return redirect(url_for('dashboard'))
    return render_template('add_item.html', form=form)

@app.route('/admin')
@login_required
def admin():
    if not current_user.is_admin:
        return "Access Denied", 403
    items = ClothingItem.query.all()
    return render_template('admin.html', items=items)

# Add login, register, and logout routes as needed

if __name__ == '__main__':
    app.run(debug=True)
