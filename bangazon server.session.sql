SELECT
    u.id user_id,
    u.first_name || " " || u.last_name AS full_name,
    c.phone_number,
    f.customer_id,
    f.seller_id
FROM
    bangazonapi_customer c
JOIN
    bangazonapi_favorite f ON f.seller_id = c.id
JOIN 
    auth_user u ON u.id = c.user_id
