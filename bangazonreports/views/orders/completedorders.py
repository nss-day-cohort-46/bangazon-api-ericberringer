import sqlite3
from django.shortcuts import render
from bangazonreports.views import Connection

def completedorders_list(request):

    if request.method == 'GET':
    # Connect to project database
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            # ORM layout orders = Order.objects.filter(payment_type__isnull = False).annotate(total=Sum("lineitems__products__price"))

            db_cursor.execute("""
                SELECT
                    SUM(p.price) total_order_price,
                    u.first_name || " " || u.last_name customer_name,
                    o.id order_id,
                    pay.merchant_name payment_method
                FROM bangazonapi_order o
                JOIN bangazonapi_orderproduct op ON op.order_id = o.id
                JOIN bangazonapi_product p ON p.id = op.product_id
                JOIN bangazonapi_customer c ON c.id = o.customer_id
                JOIN bangazonapi_payment pay ON pay.id = o.payment_type_id
                JOIN auth_user u ON u.id = c.user_id
                WHERE o.payment_type_id IS NOT NULL
            """)

            dataset = db_cursor.fetchall()

            completed_orders = {}

            for row in dataset:

                oid = row["order_id"]

                completed_orders[oid] = {}
                completed_orders[oid]["id"] = oid
                completed_orders[oid]["customer_name"] = row["customer_name"]
                completed_orders[oid]["total_order_price"] = row["total_order_price"]
                completed_orders[oid]["payment_method"] = row["payment_method"]

        list_of_completed_orders = completed_orders.values()

        template = 'orders/list_of_completed_orders.html'
        context = {
            'completedorder_list': list_of_completed_orders
        }


        return render(request, template, context)