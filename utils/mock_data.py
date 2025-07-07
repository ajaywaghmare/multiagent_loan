import json

def get_customer_profile(customer_id):
    try:
        with open("customers.json", "r") as file:
            customers = json.load(file)
        for customer in customers:
            if customer["customer_id"] == customer_id:
                return json.dumps(customer)
        return json.dumps({"error": f"Customer ID {customer_id} not found"})
    except Exception as e:
        return json.dumps({"error": f"Failed to read customer data: {str(e)}"})