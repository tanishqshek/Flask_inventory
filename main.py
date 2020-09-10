from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
import os
app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'inventory'

mysql = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    full_filename = os.path.join('static', 'frappe.png')
    return render_template('index.html', user_image=full_filename)


@app.route('/products', methods=["GET", "POST"])
def products():
    if request.method == "GET":
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, name FROM products")
        products = cur.fetchall()
        print(products)
        mysql.connection.commit()
        cur.close()
        return render_template('products.html', products=products)
    if request.method == "POST":
        product_name = request.form['product-name']
        cur = mysql.connection.cursor()

        try:
            cur.execute("INSERT INTO products(name) VALUES (%s)",
                        [product_name])
            mysql.connection.commit()
            cur.close()
            return redirect("/products")
        except:
            return "Database error"


@app.route('/locations', methods=["GET", "POST"])
def locations():
    if request.method == "GET":
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, name FROM locations")
        locations = cur.fetchall()
        mysql.connection.commit()
        cur.close()
        return render_template('locations.html', locations=locations)
    if request.method == "POST":
        location_name = request.form['location-name']
        cur = mysql.connection.cursor()

        # try:
        cur.execute("INSERT INTO locations(name) VALUES (%s)", [location_name])
        mysql.connection.commit()
        cur.close()
        return redirect("/locations")
        # except:
        #     return "Database error"


@app.route('/products/<int:id>/update', methods=["GET", "POST"])
def updateProduct(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT name FROM products WHERE id = (%s)", [id])
    name = cur.fetchone()
    prod_name = str(name).strip('(,\')')
    if request.method == "GET":
        return render_template("updateProduct.html", product_id=id, product_name=prod_name)
    if request.method == "POST":
        product_name = request.form['product-name']

        try:
            cur = mysql.connection.cursor()
            cur.execute("UPDATE products SET name = (%s) WHERE id=(%s)", [
                        product_name, id])
            mysql.connection.commit()
            cur.close()
            return redirect("/products")
        except:
            return "Database error"


@app.route('/locations/<int:id>/update', methods=["GET", "POST"])
def updateLocation(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT name FROM locations WHERE id = (%s)", [id])
    name = cur.fetchone()
    loc_name = str(name).strip('(,\')')
    if request.method == "GET":
        return render_template("updateLocation.html", location_id=id, location_name=loc_name)
    if request.method == "POST":
        location_name = request.form['location-name']

        try:
            cur = mysql.connection.cursor()
            cur.execute("UPDATE locations SET name = (%s) WHERE id=(%s)", [
                        location_name, id])
            mysql.connection.commit()
            cur.close()
            return redirect("/locations")
        except:
            return "Database error"


@app.route('/movements', methods=["GET", "POST"])
def movements():
    if request.method == "GET":
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM products")
        products = cur.fetchall()
        cur.execute("SELECT * FROM locations")
        locations = cur.fetchall()
        cur.execute("SELECT * FROM movements")
        movements = cur.fetchall()
        return render_template('movements.html', products=products, locations=locations, movements=movements)
    if request.method == "POST":
        cur = mysql.connection.cursor()
        to_location = request.form['to-location']
        cur.execute("SELECT name FROM locations WHERE id = (%s)",
                    [to_location])
        to_loc_name = cur.fetchone()
        print(to_loc_name)
        from_location = request.form['from-location']
        cur.execute("SELECT name FROM locations WHERE id = (%s)",
                    [from_location])
        from_loc_name = cur.fetchone()
        product = request.form['product']
        cur.execute("SELECT name FROM products WHERE id = (%s)", [product])
        product_name = cur.fetchone()
        quantity = request.form['quantity']

        if from_location == 'none':
            cur = mysql.connection.cursor()
            try:
                cur.execute("INSERT INTO movements(prod_id, prod_name, to_location_id, to_location_name, quantity) VALUES (%s, %s, %s, %s, %s)", [
                            product, product_name, to_location, to_loc_name, quantity])
                mysql.connection.commit()
                cur.close()
                return redirect('/movements')
            except:
                return "Database error"
        else:
            quantity_at_location = get_quantity(from_location, product)
            if quantity_at_location < int(quantity):
                return "Short of quantity"
            else:
                cur = mysql.connection.cursor()
                cur.execute("SELECT quantity FROM movements WHERE from_location_id = (%s) AND prod_id = (%s)", [
                            from_location, product])
                x = cur.fetchone()
                quantity_at_location = str(x).strip('(,\')')

                try:

                    cur.execute("INSERT INTO movements(prod_id, prod_name, to_location_id, to_location_name, from_location_id, from_location_name, quantity) VALUES (%s, %s, %s, %s, %s, %s,%s)", [
                                product, product_name, to_location, to_loc_name, from_location, from_loc_name, quantity])
                    mysql.connection.commit()
                    cur.close()
                    return redirect('/movements')
                except:
                    return "Database error"


def get_quantity(location, product):
    cur = mysql.connection.cursor()
    cur.execute("SELECT SUM(quantity) FROM movements WHERE to_location_id = (%s) AND prod_id = (%s)", [
                location, product])
    added = cur.fetchone()
    if ''.join(map(str, added)) == 'None':
        added = 0
    else:
        print(int(str(added[0])))
        added = int(str(added[0]))
    cur = mysql.connection.cursor()
    cur.execute("SELECT SUM(quantity) FROM movements WHERE from_location_id = (%s) AND prod_id = (%s)", [
                location, product])
    removed = cur.fetchone()
    if removed == None:
        removed = 0
    return added


@app.route('/report')
def report():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM products")
    products = cur.fetchall()
    cur.execute("SELECT * FROM locations")
    locations = cur.fetchall()
    report = []

    for location in locations:
        for product in products:
            row = {}
            row["product"] = product[1]
            row["location"] = location[1]
            row["quantity"] = get_quantity(location[0], product[0])
            report.append(row)
    return render_template('report.html', report=report)


@app.route('/movements/<int:id>/update', methods=["GET", "POST"])
def updateMovement(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM movements WHERE movement_id = (%s)", [id])
    old_movement = cur.fetchone()
    if request.method == "GET":
        cur.execute("SELECT * FROM products")
        products = cur.fetchall()
        cur.execute("SELECT * FROM locations")
        locations = cur.fetchall()
        cur.execute("SELECT * FROM movements")
        movements = cur.fetchall()
        return render_template('updateMovements.html', products=products, locations=locations, movement=old_movement)

    if request.method == 'POST':
        cur = mysql.connection.cursor()
        new_to_location_id = request.form["to_location"]
        new_from_location_id = request.form["from_location"]
        new_product_id = request.form["product"]
        new_quantity = request.form["quantity"]

        cur.execute("SELECT name FROM locations WHERE id = (%s)",
                    [new_to_location_id])
        new_to_loc_name = cur.fetchone()
        cur.execute("SELECT name FROM locations WHERE id = (%s)",
                    [new_from_location_id])
        new_from_loc_name = cur.fetchone()
        cur.execute("SELECT name FROM products WHERE id = (%s)",
                    [new_product_id])
        new_product_name = cur.fetchone()

        try:

            cur.execute("UPDATE movements SET to_location_id = (%s) ,to_location_name = (%s), from_location_id = (%s) ,from_location_name = (%s), prod_id = (%s) ,prod_name = (%s),quantity = (%s) WHERE movement_id = (%s)", [
                        new_to_location_id, new_to_loc_name, new_from_location_id, new_from_loc_name, new_product_id, new_product_name, new_quantity, id])
            mysql.connection.commit()
            cur.close()
            return redirect("/movements")
        except:
            return "Database Error"


if __name__ == '__main__':
    app.run(debug=True)
