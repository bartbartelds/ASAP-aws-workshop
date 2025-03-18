import boto3
import random
import string
import time
import json

s3 = boto3.client('s3', region_name='eu-central-1')

# Pregenerated customer IDs
customer_ids = [
    'CUST123456', 'CUST789012', 'CUST345678', 'CUST901234',
    'CUST567890', 'CUST123789', 'CUST456012', 'CUST789345',
    'CUST012678', 'CUST345901'
]

# Pregenerated item-price combinations
item_price_combinations = [
    {'description': 'Item A', 'price': 10.0},
    {'description': 'Item B', 'price': 20.0},
    {'description': 'Item C', 'price': 30.0},
    {'description': 'Item D', 'price': 40.0},
    {'description': 'Item E', 'price': 50.0},
    {'description': 'Item F', 'price': 60.0},
    {'description': 'Item G', 'price': 70.0},
    {'description': 'Item H', 'price': 80.0},
    {'description': 'Item I', 'price': 90.0},
    {'description': 'Item J', 'price': 100.0}
]

def generate_random_data():
    # Generate a unique 15-number identifier
    identifier = ''.join(random.choices(string.digits, k=15))
    # Select a random customer ID from the pregenerated list
    customer_id = random.choice(customer_ids)
    # Generate an order ID
    order_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    # Randomly select a subset of item-price combinations
    items = random.sample(item_price_combinations, k=random.randint(1, 5))
    # Assign a random amount to each selected item
    for item in items:
        item['amount'] = random.randint(1, 10)
    return identifier, customer_id, order_id, items

def lambda_handler(event, context):
    try:
        bucket_name = event.get('bucket_name', 'bart.bartelds-391614831370')
        identifier, customer_id, order_id, items = generate_random_data()
        
        content = {
            'customerID': customer_id,
            'orderID': order_id,
            'items': items
        }
        
        s3.put_object(Bucket=bucket_name, Key=f"data_{identifier}.json", Body=json.dumps(content))
        
        return {
            'statusCode': 200,
            'body': json.dumps('Data uploaded successfully!')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {str(e)}')
        }

if __name__ == '__main__':
    while True:
        lambda_handler({'bucket_name': 'bart.bartelds-391614831370'}, None)
        time.sleep(1)