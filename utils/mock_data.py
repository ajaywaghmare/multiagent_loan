# def get_customer_profile(customer_id):
#     return {
#         "customer_id": customer_id,
#         "name": "John Doe",
#         "age": 35,
#         "email": "johndoe@example.com",
#         "phone": "555-1234",
#         "address": "123 Main Street, Anytown, USA",
#         "credit_score": 300,
#         "income": 10000,
#         "employment_status": "Employed",
#         "loan_amount_request": 75000
#     }


import json

def get_customer_profile(customer_id):
    return json.dumps({
        "customer_id": customer_id,
        "name": "John Doe",
        "age": 35,
        "email": "johndoe@example.com",
        "phone": "555-1234",
        "address": "123 Main Street, Anytown, USA",
        "credit_score": 300,
        "income": 10000,
        "employment_status": "Employed",
        "loan_amount_request": 110000
    })


