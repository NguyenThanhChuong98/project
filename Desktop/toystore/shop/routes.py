import os
import secrets
import datetime
from PIL import Image
from flask import render_template, url_for, redirect, flash, request
from shop import app, db, photos, bcrypt
from shop.models import Users, Roles, Products, Categories, Orders, Order_detail, Warehouse, Shipper, Cart
from shop.forms import RegistrationForm, LoginForm, UpdateAccountForm, ProductForm, CategoryForm, ShipperForm
from flask_login import login_user, current_user, logout_user, login_required
 

@app.route("/")
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
    if current_user.is_authenticated:
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
        form.address.data = current_user.address
        form.date_of_birth.data = current_user.date_of_birth

    image_file = url_for('static', filename='customer/images/avatar/' + current_user.image_file)
    return render_template("customer/account.html", title="Account",
                           image_file=image_file, form=form)


@app.route("/admin", strict_slashes=False)
def admin():
    return render_template("staff/layout.html", title="staff")


@app.route("/admin/add_user", strict_slashes=False, methods=['GET', 'POST'])
def add_user():
    users = Users.query.all()
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Users(username=form.username.data,
                     email = form.email.data,
                     address = form.address.data,
                     date_of_birth = form.date_of_birth.data,
                     password = form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Your product has been created!', 'success')
        return redirect(url_for('add_user'))
    return render_template("staff/add_user.html", title="staff", form = form, users = users)


@app.route("/admin/view_all_users", strict_slashes=False, methods=['GET'])
def view_all_users():
    users = Users.query.all()
    return render_template("staff/view_all_users.html", users = users)


@app.route("/admin/view_all_products", strict_slashes=False, methods=['GET'])
def view_all_products():
    products = Products.query.all()
    return render_template("staff/view_all_products.html", products=products)


@app.route("/admin/add_product", strict_slashes=False, methods=['GET', 'POST'])
def add_product():
    categories = Categories.query.all()
    form = ProductForm()
    if request.method == 'POST':
        product = Products(category_name = form.category_name.data,
                           product_name=form.product_name.data,
                           quantity=form.quantity.data,
                           price=form.price.data,
                           age_recommendation = form.age_recommendation.data,
                           dimensions = form.dimensions.data,
                           country_of_design = form.country_of_design.data,
                           country_of_manufacture = form.country_of_design.data,
                           primary_material = form.primary_material.data,
                           assembly_required = form.assembly_required.data,
                           gift_wrap = form.gift_wrap.data,
                           image_product=photos.save(request.files.get('image_product'))
                           )
        db.session.add(product)
        db.session.commit()
        flash(f'Your product has been created!', 'success')
        return redirect(url_for('add_product'))
    return render_template("staff/add_product.html", title="staff", form=form, categories=categories)


@app.route("/admin/delete_product/<int:product_id>", strict_slashes=False, methods=['GET', 'POST'])
def delete_product_by_id(product_id):
    product = Products.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash(f"Product deleted", "success")
    return redirect(url_for('view_all_products'))


@app.route("/admin/update_product/<int:product_id>", strict_slashes=False, methods=['GET', 'POST'])
def update_product_by_id(product_id):
    categories = Categories.query.all()
    form = ProductForm()
    update_product = Products.query.get_or_404(product_id)
    if form.validate_on_submit():
        update_product.product_name = form.product_name.data
        update_product.quantity = form.quantity.data
        update_product.price = form.price.data
        update_product.age_recommendation = form.age_recommendation.data
        update_product.dimensions = form.dimensions.data
        update_product.country_of_design = form.country_of_design.data
        update_product.country_of_manufacture = form.country_of_manufacture.data
        update_product.primary_material = form.primary_material.data
        update_product.assembly_required = form.assembly_required.data
        update_product.gift_wrap = form.gift_wrap.data
        update_product.image_product = photos.save(request.files.get('image_product'))
        update_product.update_date = datetime.datetime.utcnow()
        db.session.add(update_product)
        db.session.commit()
        flash(f"Product has been updated", "success")
        return redirect(url_for('view_all_products', product_id=update_product.id))
    elif request.method == "GET":
        form.product_name.data = update_product.product_name
        form.quantity.data = update_product.quantity
        form.price.data = update_product.price
        form.age_recommendation.data = update_product.age_recommendation
        form.dimensions.data = update_product.dimensions
        form.country_of_design.data = update_product.country_of_design
        form.country_of_manufacture.data = update_product.country_of_manufacture
        form.primary_material.data = update_product.primary_material
        form.assembly_required.data = update_product.assembly_required
        form.gift_wrap.data =  update_product.gift_wrap
    return render_template("staff/update_product.html", title="update product", form=form, categories=categories)


@app.route("/admin/view_all_categories", strict_slashes=False, methods=['GET'])
def view_all_categories():
    categories = Categories.query.all()
    return render_template("staff/view_all_categories.html", categories=categories)


@app.route("/admin/add_category", strict_slashes=False, methods=['GET', 'POST'])
def add_category():
    form = CategoryForm()
    category = Categories(category_name=form.category_name.data,)
    if form.validate_on_submit():
        db.session.add(category)
        db.session.commit()
        flash('Your category has been created!', 'success')
        return redirect(url_for('add_category'))

    return render_template("staff/add_category.html", title="staff", form=form)


@app.route("/admin/delete_category/<int:category_id>", strict_slashes=False, methods=['GET', 'POST'])
def delete_category_by_id(category_id):
    category = Categories.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    flash(f"Category deleted", "success")
    return redirect(url_for('view_all_categories'))


@app.route("/admin/update_category/<int:category_id>", strict_slashes=False, methods=['GET', 'POST'])
def update_category_by_id(category_id):
    form = CategoryForm()
    update_category = Categories.query.get_or_404(category_id)
    if form.validate_on_submit():
        update_category.category_name = form.category_name.data
        update_category.update_date = datetime.datetime.utcnow()
        db.session.add(update_category)
        db.session.commit()
        flash(f"Category has been updated", "success")
        return redirect(url_for('view_all_categories', category_id=update_category.id))
    elif request.method == "GET":
        form.category_name.data = update_category.category_name

    return render_template("staff/update_category.html", title="Update category", update_category=update_category, form=form)


@app.route("/admin/add_shipper", strict_slashes=False, methods=['GET', 'POST'])
def add_shipper():
    form = ShipperForm()
    shipper = Shipper(shipper_name = form.shipper_name.data,
                      date_of_birth = form.date_of_birth.data,
                      address = form.address.data)
    if form.validate_on_submit():
        db.session.add(shipper)
        db.session.commit()
        flash('Your shipper has been created!', 'success')
        return redirect(url_for('add_shipper'))
    else:
        flash('Something wrong occured, please input again')

    return render_template("staff/add_shipper.html", title="staff", form=form)


@app.route("/admin/delete_shipper/<int:shipper_id>", strict_slashes=False, methods=['GET', 'POST'])
def delete_shipper_by_id(shipper_id):
    shipper = Shipper.query.get_or_404(shipper_id)
    db.session.delete(shipper)
    db.session.commit()
    flash(f"Shipper deleted", "success")
    return redirect(url_for('view_all_shippers'))


@app.route("/admin/update_shipper/<int:shipper_id>", strict_slashes=False, methods=['GET', 'POST'])
def update_shipper_by_id(shipper_id):
    form = ShipperForm()
    update_shipper = Shipper.query.get_or_404(shipper_id)
    if form.validate_on_submit():
        update_shipper.shipper_name = form.shipper_name.data
        update_shipper.date_of_birth = form.date_of_birth.data
        update_shipper.address = form.address.data
        update_shipper.update_date = datetime.datetime.utcnow()
        db.session.add(update_shipper)
        db.session.commit()
        flash(f"Shipper has been updated", "success")
        return redirect(url_for('view_all_shippers',shipper_id=update_shipper.id))
    elif request.method == "GET":
        form.shipper_name.data = update_shipper.shipper_name
        form.date_of_birth.data =  update_shipper.date_of_birth
        form.address.data =  update_shipper.address
    return render_template("staff/update_shipper.html", title="Update Shipper", update_shipper=update_shipper, form=form)


@app.route("/admin/view_all_shippers", strict_slashes=False, methods=['GET'])
def view_all_shippers():
    shippers = Shipper.query.all()
    return render_template("staff/view_all_shippers.html", shippers=shippers)


@app.route("/list_product")
def list_product():
    products = Products.query.all()
    return render_template("customer/product.html", title="Product", products=products)


@app.route("/list_product/<int:product_id>")
def product_info(product_id):
    product = Products.query.get_or_404(product_id)
    return render_template('customer/single_product.html', title='Single Product', product=product)

