#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = [bakery.to_dict() for bakery in Bakery.query.all()]
    return make_response(  bakeries,   200  )

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):

    bakery = Bakery.query.filter_by(id=id).first()
    bakery_serialized = bakery.to_dict()
    return make_response ( bakery_serialized, 200  )

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods_by_price = BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_goods_by_price_serialized = [
        bg.to_dict() for bg in baked_goods_by_price
    ]
    return make_response( baked_goods_by_price_serialized, 200  )
   

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).limit(1).first()
    most_expensive_serialized = most_expensive.to_dict()
    return make_response( most_expensive_serialized,   200  )

@app.route('/baked_goods', methods=['GET', 'POST'])
def creates_baked_goods():
    if request.method == "GET":
        baked_goods_list = [bg.to_dict() for bg in BakedGood.query.all()]  # Query from the database
        return jsonify(baked_goods_list)
    elif request.method == 'POST':
        new_name = request.form['name'],
        new_price = request.form['price']
        new_time = request.form['created_at']
        new_update = request.form['updated_at']
        
        new_product = BakedGood(name=new_name, price=new_price, created_at=new_time, updated_at=new_update)
        db.session.add(new_product)
        db.session.commit()
        return jsonify(new_product.to()), 201 
    else:
        return 'Method Not Allowed', 405 
    
@app.route('/baked_goods/<int:id>')
def delete_baked_good(id):
    baked_good = BakedGood.query.get(id)
    if baked_good:
        db.session.delete(baked_good)
        db.session.commit()
        return jsonify({'message': f'Baked good with id {id} has been deleted successfully.'}), 200
    else:
        return jsonify({'message': 'Baked good not found.'}), 404

if __name__ == '__main__':
    app.run(port=5555, debug=True)