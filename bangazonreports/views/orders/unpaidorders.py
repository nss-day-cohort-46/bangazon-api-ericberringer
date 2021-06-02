import sqlite3
from django.shortcuts import render
from bangazonapi.models import Order
from bangazonreports.views import Connection

def unpaidorders_list(request):

    if request.method == 'GET':
    # Connect to project database
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute("""
                SELECT
                    SUM(p.price) total_order_price,
                    u.first_name || " " || u.last_name customer_name,
                    o.id order_id
                FROM bangazonapi_order o
                JOIN bangazonapi_orderproduct op ON op.order_id = o.id
                JOIN bangazonapi_product p ON p.id = op.product_id
                JOIN bangazonapi_customer c ON c.id = o.customer_id
                JOIN auth_user u ON u.id = c.user_id
                WHERE o.payment_type_id IS NULL
                GROUP BY order_id
            """)

            dataset = db_cursor.fetchall()

            unpaid_orders = {}

            for row in dataset:

                oid = row["order_id"]

                unpaid_orders[oid] = {}
                unpaid_orders[oid]["id"] = oid
                unpaid_orders[oid]["customer_name"] = row["customer_name"]
                unpaid_orders[oid]["total_order_price"] = row["total_order_price"]

        list_of_unpaid_orders = unpaid_orders.values()

        template = 'orders/list_of_unpaid_orders.html'
        context = {
            'unpaidorder_list': list_of_unpaid_orders
        }


        return render(request, template, context)