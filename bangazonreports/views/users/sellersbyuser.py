import sqlite3
from django.shortcuts import render
from bangazonapi.models import Customer, Favorite
from bangazonreports.views import Connection

def favoritebyuser_list(request):

    if request.method == 'GET':
    # Connect to project database
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute("""
                SELECT
                    u.id user_id,
                    u.first_name || " " || u.last_name AS full_name,
                    f.customer_id,
                    f.seller_id
                FROM
                    bangazonapi_customer c
                JOIN
                    bangazonapi_favorite f ON f.customer_id = c.id
                JOIN 
                    auth_user u ON u.id = c.id    
            """)

            dataset = db_cursor.fetchall()

            favorites_by_user = {}

            for row in dataset:

                favorited_seller = Customer.objects.get(pk=row["seller_id"])
                

                uid = row["user_id"]

                if uid in favorites_by_user:

                    favorites_by_user[uid]["sellers"].append(favorited_seller)

                else:

                    favorites_by_user[uid] = {}
                    favorites_by_user[uid]["id"] = uid
                    favorites_by_user[uid]["full_name"] = row["full_name"]
                    favorites_by_user[uid]["sellers"] = [favorited_seller]

        list_of_users_with_sellers = favorites_by_user.values()

        template = 'users/list_of_users_with_sellers.html'
        context = {
            'userfavorite_list': list_of_users_with_sellers
        }


        return render(request, template, context)