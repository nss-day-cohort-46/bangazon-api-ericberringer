import sqlite3
from django.shortcuts import render
from bangazonreports.views import Connection

def inexpensiveproducts_list(request):

    if request.method == 'GET':
    # Connect to project database
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute("""
                SELECT
                    p.price product_price,
                    p.name product_name,
                    p.id product_id
                FROM bangazonapi_product p
                WHERE product_price < 999
            """)

            dataset = db_cursor.fetchall()

            inexpensive_products = {}

            for row in dataset:

                pid = row["product_id"]

                inexpensive_products[pid] = {}
                inexpensive_products[pid]["id"] = pid
                inexpensive_products[pid]["product_name"] = row["product_name"]
                inexpensive_products[pid]["product_price"] = row["product_price"]

        list_of_inexpensive_products = inexpensive_products.values()

        template = 'products/list_of_inexpensive_products.html'
        context = {
            'inexpensiveproducts_list': list_of_inexpensive_products
        }


        return render(request, template, context)