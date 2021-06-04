import sqlite3
from django.shortcuts import render
from bangazonreports.views import Connection

def expensiveproducts_list(request):

    # ORM expensiveproducts_list = Product.objects.filter(price__gte = 1000)
    # gte = greater than or equal to

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
                WHERE product_price > 999
            """)

            dataset = db_cursor.fetchall()

            expensive_products = {}

            for row in dataset:

                pid = row["product_id"]

                expensive_products[pid] = {}
                expensive_products[pid]["id"] = pid
                expensive_products[pid]["product_name"] = row["product_name"]
                expensive_products[pid]["product_price"] = row["product_price"]

        list_of_expensive_products = expensive_products.values()

        template = 'products/list_of_expensive_products.html'
        context = {
            'expensiveproducts_list': list_of_expensive_products
        }


        return render(request, template, context)