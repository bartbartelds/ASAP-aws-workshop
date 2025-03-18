import random
import string
import time
import json
import os

# Pregenerated customer IDs
customer_ids = [
    'CUST123456', 'CUST789012', 'CUST345678', 'CUST901234',
    'CUST567890', 'CUST123789', 'CUST456012', 'CUST789345',
    'CUST012678', 'CUST345901'
]

def generate_random_data():
    # Generate a unique 15-number identifier
    identifier = ''.join(random.choices(string.digits, k=15))
    # Select a random customer ID from the pregenerated list
    customer_id = random.choice(customer_ids)
    # Generate an order ID
    order_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    # Generate a list of random items
    items = []
    for _ in range(random.randint(1, 5)):
        item = {
            'description': ''.join(random.choices(string.ascii_letters, k=20)),
            'amount': random.randint(1, 10),
            'price': round(random.uniform(1.0, 100.0), 2)
        }
        items.append(item)
    return identifier, customer_id, order_id, items

def lambda_handler(event, context):
    try:
        # Create output directory if it doesn't exist
        output_dir = 'output'
        os.makedirs(output_dir, exist_ok=True)
        
        identifier, customer_id, order_id, items = generate_random_data()
        
        content = {
            'customerID': customer_id,
            'orderID': order_id,
            'items': items
        }
        
        # Write to local file
        filename = f'{output_dir}/data_{identifier}.json'
        with open(filename, 'w') as f:
            f.write(json.dumps(content))
        
        return {
            'statusCode': 200,
            'body': json.dumps(f'Data written to {filename} successfully!')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {str(e)}')
        }

if __name__ == '__main__':
    result = lambda_handler({}, None)
    print('Lambda result:', result)