from bottle import route, run, template, static_file, get, post, delete, request
from sys import argv
import json
import pymysql

connection = pymysql.connect(host="localhost",
                             user="root",
                             password="**********",
                             db="store",
                             charset="utf8",
                             cursorclass=pymysql.cursors.DictCursor)


@get("/admin")
def admin_portal():
    return template("pages/admin.html")


@get("/")
def index():
    return template("index.html")


@get('/js/<filename:re:.*\.js>')
def javascripts(filename):
    return static_file(filename, root='js')


@get('/css/<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root='css')


@get('/images/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
    return static_file(filename, root='images')


@post("/category")
def add_category():
    result = {}
    name = request.forms.get("name")
    try:
        with connection.cursor() as cursor:
            sql2 = "SELECT name FROM categories"
            cursor.execute(sql2)
            fetched = cursor.fetchall()
            names_list = [r['name'] for r in fetched]
            if name in names_list:
                result["STATUS"] = "ERROR"
                result["MSG"] = "Category already exists"
                result["CODE"] = 200
            elif name == "":
                result["STATUS"] = "ERROR"
                result["MSG"] = "Name parameter is missing"
                result["CODE"] = 400
            else:
                sql = "INSERT INTO categories (name) VALUES('{0}')".format(name)
                cursor.execute(sql)
                connection.commit()
                result["STATUS"] = "SUCCESS"
                result["CAT_ID"] = cursor.lastrowid
                result["CODE"] = 201
        return json.dumps(result)

    except:
        result["STATUS"] = "ERROR"
        result["MSG"] = "Internal Error"
        result["CODE"] = 500
        return json.dumps(result)


@delete("/category/<id>")
def delete_category(id):
    result = {}
    try:
        with connection.cursor() as cursor:
            sql2 = "SELECT id FROM categories"
            cursor.execute(sql2)
            fetched = cursor.fetchall()
            id_list = [r['id'] for r in fetched]
            if int(id) in id_list:
                sql = "DELETE FROM categories WHERE id = {0}".format(id)
                cursor.execute(sql)
                connection.commit()
                result["STATUS"] = "SUCCESS"
                result["CODE"] = 201
            else:
                result["STATUS"] = "ERROR"
                result["MSG"] = "Category not found"
                result["CODE"] = 404

        return json.dumps(result)
    except:
        result["STATUS"] = "ERROR"
        result["MSG"] = "Internal Error"
        result["CODE"] = 500
        return json.dumps(result)


@get("/categories")
def list_categories():
    result = {}
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM categories"
            cursor.execute(sql)
            fetched = cursor.fetchall()
            result["STATUS"] = "SUCCESS"
            result["CATEGORIES"] = fetched
            result["CODE"] = 200
        return json.dumps(result)
    except:
        result["STATUS"] = "ERROR"
        result["MSG"] = "Internal Error"
        result["CODE"] = 500
        return json.dumps(result)


@post("/product")
def add_product():
    result = {}
    category_id = request.forms.get("category")
    title = request.forms.get("title")
    desc = request.forms.get("desc")
    favorite = request.forms.get("favorite")
    price = request.forms.get("price")
    img_url = request.forms.get("img_url")
    id = request.forms.get("id")
    if favorite == "on":
        fav = 1
    else:
        fav = 0

    try:
        with connection.cursor() as cursor:
            category_query = "SELECT id FROM categories"
            cursor.execute(category_query)
            fetched = cursor.fetchall()
            category_list = [r['id'] for r in fetched]
            product_query = "SELECT id FROM products"
            cursor.execute(product_query)
            product_ids = cursor.fetchall()
            products_list = [r['id'] for r in product_ids]
            if int(category_id) not in category_list:
                result["STATUS"] = "ERROR"
                result["MSG"] = "Category not found"
                result["CODE"] = 404
            elif title == "" or price == "":
                result["STATUS"] = "ERROR"
                result["MSG"] = "missing parameters"
                result["CODE"] = 400
            elif int(id) in products_list:
                update_query = "UPDATE products SET title='{0}',descr='{1}',price={2},img_url='{3}', category={4},favorite={5} WHERE id={6}".format(
                    title, desc, price, img_url, category_id, fav, id)
                cursor.execute(update_query)
                connection.commit()
                result['PRODUCT_ID'] = id
                result['STATUS'] = 'SUCCESS'
                result['CODE'] = 201
            else:
                query = "INSERT INTO products (title, descr, price, img_url, category, favorite) VALUES ('{0}','{1}',{2},'{3}',{4},{5})".format(
                    title, desc, price, img_url, category_id, fav)
                cursor.execute(query)
                connection.commit()
                result["STATUS"] = "SUCCESS"
                result["PRODUCT_ID"] = cursor.lastrowid
                result["CODE"] = 201

        return json.dumps(result)
    except:
        result["STATUS"] = "ERROR"
        result["MSG"] = "Internal Error"
        result["CODE"] = 500
        return json.dumps(result)


@get('/product/<id>')
def get_product(id):
    result = {}
    try:
        with connection.cursor() as cursor:
            products_id_query = 'SELECT id FROM products'
            cursor.execute(products_id_query)
            id_dic_lists = cursor.fetchall()
            products_id_list = [r['id'] for r in id_dic_lists]
            if int(id) not in products_id_list:
                result['STATUS'] = 'ERROR'
                result['MSG'] = 'Product not found'
                result['CODE'] = 404
            else:
                product_query = "SELECT * FROM products WHERE id={}".format(id)
                cursor.execute(product_query)
                prod_dic_lists = cursor.fetchall()
                result['PRODUCT'] = prod_dic_lists[0]
                result['STATUS'] = 'SUCCESS'
                result['CODE'] = 200
        return json.dumps(result)
    except:
        result['STATUS'] = 'ERROR'
        result['MSG'] = 'Internal error'
        result['CODE'] = 500
        return json.dumps(result)


@delete("/product/<id>")
def delete_product(id):
    result = {}
    try:
        with connection.cursor() as cursor:
            sql2 = "SELECT id FROM products"
            cursor.execute(sql2)
            fetched = cursor.fetchall()
            id_list = [r['id'] for r in fetched]
            if int(id) in id_list:
                sql = "DELETE FROM products WHERE id = {0}".format(id)
                cursor.execute(sql)
                connection.commit()
                result["STATUS"] = "SUCCESS"
                result["CODE"] = 201
            else:
                result["STATUS"] = "ERROR"
                result["MSG"] = "Product not found"
                result["CODE"] = 404

        return json.dumps(result)
    except:
        result["STATUS"] = "ERROR"
        result["MSG"] = "Internal Error"
        result["CODE"] = 500
        return json.dumps(result)


@get("/products")
def list_products():
    result = {}
    try:
        with connection.cursor() as cursor:
            product_query = "SELECT * FROM products"
            cursor.execute(product_query)
            products_list = cursor.fetchall()
            result["PRODUCTS"] = products_list
            result["STATUS"] = "SUCCESS"
            result["CODE"] = 200
        return json.dumps(result)
    except:
        result["STATUS"] = "ERROR"
        result["MSG"] = "Internal Error"
        result["CODE"] = 500
        return json.dumps(result)


@get("/category/<id>/products")
def list_products(id):
    result = {}
    cat_prod = []
    try:
        with connection.cursor() as cursor:
            category_query = "SELECT id FROM categories"
            cursor.execute(category_query)
            fetched = cursor.fetchall()
            category_list = [r['id'] for r in fetched]
            if int(id) not in category_list:
                result["CODE"] = 200
            else:
                product_query = "SELECT * FROM products"
                cursor.execute(product_query)
                products_list = cursor.fetchall()
                for dic in products_list:
                    if dic["category"] == int(id):
                        cat_prod.append(dic)
                result["PRODUCTS"] = cat_prod
                result["STATUS"] = "SUCCESS"
                result["CODE"] = 200
        return json.dumps(result)
    except:
        result["STATUS"] = "ERROR"
        result["MSG"] = "Internal Error"
        result["CODE"] = 500
        return json.dumps(result)


run(host='0.0.0.0', port=7001)
