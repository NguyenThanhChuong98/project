import os
import secrets
from PIL import Image
from flask import render_template, url_for, redirect, flash, request
from shop import app, db, photos
from shop.models import Users, Roles, Products, Categories, Orders, Order_detail, Warehouse, Shipper, Cart
from shop.forms import RegistrationForm, LoginForm, UpdateAccountForm, ProductForm, CategoryForm
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/home")
def home():
    return render_template("customer/home.html")


@app.route("/about")
def about():
    return render_template("customer/about.html", title="About")


@app.route("/contact")
def contact():
    return render_template("customer/contact.html", title="Contact")


@app.route("/login", strict_slashes=False, methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessfully,Please check your account again', 'danger')
    return render_template('customer/login.html', title='Login', form=form)


@app.route("/register", strict_slashes=False, methods=['GET', 'POST'])
def register():
    if current_user.is_authenticate:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = Users(username=form.username.data,
                     email=form.email.data,
                     address=form.address.data,
                     date_of_birth=form.date_of_birth.data,
                     password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created!", 'success')
        return redirect(url_for('login'))
    return render_template("customer/register.html", title="Register", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture_user(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/customer/images/avatar', picture_fn)

    ouput_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(ouput_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture_user(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated!", 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename='customer/images/avatar/' + current_user.image_file)
    return render_template("customer/account.html", title="Account",
                           image_file=image_file, form=form)


@app.route("/admin", strict_slashes=False)
def admin():
    return render_template("staff/layout.html", title="staff")


@app.route("/admin/add_product", strict_slashes=False, methods=['GET', 'POST'])
def add_product():
    categories = Categories.query.all()
    form = ProductForm()
    # if form.validate_on_submit():
    if request.method == 'POST':
        product = Products(categoryname=request.form.get('categoryname'),
                           productname=form.productname.data,
                           quantity=form.quantity.data,
                           price=form.price.data,
                           product_description=form.product_description.data,
                           image_product=photos.save(request.files.get('image_product'))
                           )
        db.session.add(product)
        db.session.commit()
        print('Your product has been created!', 'success')
        return redirect(url_for('add_product'))
    return render_template("staff/admin_product.html", title="staff", form=form, categories=categories)


@app.route("/admin/add_category", strict_slashes=False, methods=['GET', 'POST'])
def add_category():
    form = CategoryForm()
    category = Categories(categoryname=form.categoryname.data,)
    if form.validate_on_submit():
        db.session.add(category)
        db.session.commit()
        flash('Your category has been created!', 'success')
        return redirect(url_for('add_category'))

    return render_template("staff/admin_category.html", title="staff", form=form)


@app.route("/list_product")
def list_product():
    products = Products.query.all()
    return render_template("customer/product.html", title="Product", products=products)


@app.route("/list_product/<int:product_id>")
def product(product_id):
    product = Products.query.get_or_404(product_id)
    return render_template('single_product.html', title='Single Product', product=product)
