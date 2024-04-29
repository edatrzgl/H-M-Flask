from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///e_commerce.db'
db = SQLAlchemy(app)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_no = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    image_url = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    new = db.Column(db.Boolean, default=True)
    price = db.Column(db.Float, nullable=False)
    size = db.Column(db.String(10), nullable=False)

# Ana sayfa
@app.route('/')
def home():
    new_categories = db.session.query(Product.category).filter_by(new=True).distinct()
    products = Product.query.filter_by(new=True).all()
    return render_template('home.html', categories=new_categories, products=products)

# Arama sonuçları sayfası
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_query = request.form.get('search_query')
        selected_price_order = request.form.get('price_order')
        selected_size = request.form.get('size')
        products = Product.query.filter(Product.description.ilike(f'%{search_query}%')).all()

        if selected_size:  
            products = Product.query.filter(Product.size == selected_size).all()

        if selected_price_order == 'asc':
            products = Product.query.order_by(Product.price.asc()).all()
        elif selected_price_order == 'desc':
            products = Product.query.order_by(Product.price.desc()).all()
    

        return render_template('search_results.html', products=products)
    else:
        return render_template('search_results.html')

# Ürün detay sayfası
@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product)

if __name__ == '__main__':
    try:
        with app.app_context():
            db.create_all()

            # Örnek ürünler oluştur
            product1 = Product(product_no='001', description='T-shirt', image_url='askili.jpeg', category='NEW', new=True, price=19.99, size='S')
            product2 = Product(product_no='002', description='Blazer', image_url='blazer.jpeg', category='NEW', new=True, price=39.99, size='M')
            product3 = Product(product_no='003', description='Bluz', image_url='bluz.jpeg', category='NEW', new=True, price=29.99, size='L')
            product4 = Product(product_no='004', description='Canta', image_url='canta.jpeg', category='NEW', new=True, price=49.99, size='L')
            product5 = Product(product_no='005', description='Ceket', image_url='ceket.jpeg', category='NEW', new=True, price=59.99, size='M')
            product6 = Product(product_no='006', description='Elbise', image_url='elbise.jpeg', category='NEW', new=True, price=69.99, size='S')
            product7 = Product(product_no='007', description='Elbise', image_url='elbise2.jpeg', category='NEW', new=True, price=79.99, size='M')
            product8 = Product(product_no='008', description='Etek', image_url='etek.jpeg', category='NEW', new=True, price=24.99, size='L')
            product9 = Product(product_no='009', description='Gömlek', image_url='gomlek.jpeg', category='NEW', new=True, price=34.99, size='M')
            product10 = Product(product_no='010', description='Pantolon', image_url='pantolon.jpeg', category='NEW', new=True, price=44.99, size='S')
            product11 = Product(product_no='011', description='Pantolon', image_url='pantolon2.jpeg', category='NEW', new=True, price=54.99, size='M')
            product12 = Product(product_no='012', description='Sandalet', image_url='sandalet.jpeg', category='NEW', new=True, price=29.99, size='L')
            product13 = Product(product_no='013', description='Şort', image_url='sort.jpeg', category='NEW', new=True, price=19.99, size='S')
            product14 = Product(product_no='014', description='T-shirt', image_url='tisort.jpeg', category='NEW', new=True, price=14.99, size='M')
            product15 = Product(product_no='015', description='T-shirt', image_url='tisort2.jpeg', category='NEW', new=True, price=14.99, size='L')
            product16= Product(product_no='016', description='Tulum', image_url='tulum.jpeg', category='NEW', new=True, price=49.99, size='S')



            # Veritabanına ekleyin
            db.session.add(product1)
            db.session.add(product2)
            db.session.add(product3)
            db.session.add(product4)
            db.session.add(product5)
            db.session.add(product6)
            db.session.add(product7)
            db.session.add(product8)
            db.session.add(product9)
            db.session.add(product10)
            db.session.add(product11)
            db.session.add(product12)
            db.session.add(product13)
            db.session.add(product14)
            db.session.add(product15)
            db.session.add(product16)

            db.session.commit()
    except Exception as e:
        print("An error occurred:", e)

    app.run(debug=True)