import boto3
import random
import time
from decimal import Decimal
from datetime import datetime, timezone

# Initialize DynamoDB
session = boto3.Session(profile_name='default', region_name='ap-south-1')
dynamodb = session.resource('dynamodb')
table = dynamodb.Table('OrdersRawTable')

# Track active orders for modify/delete
existing_orders = {}

# Product attributes
PRODUCTS = ['Laptop', 'Phone', 'Tablet', 'Headphones', 'Charger']
PAYMENT_METHODS = ['Credit Card', 'UPI', 'Net Banking', 'COD']
STATUSES = ['pending', 'confirmed', 'shipped', 'cancelled']

def generate_new_order():
    orderid = str(random.randint(1000, 9999))
    product_name = random.choice(PRODUCTS)
    quantity = random.randint(1, 5)
    price = Decimal(str(round(random.uniform(10.0, 500.0), 2)))
    customer_id = str(random.randint(1000, 9999))
    payment_method = random.choice(PAYMENT_METHODS)
    timestamp = datetime.utcnow().isoformat() + 'Z'
    status = 'pending'

    return {
        'orderid': orderid,
        'product_name': product_name,
        'quantity': quantity,
        'price': price,
        'customer_id': customer_id,
        'payment_method': payment_method,
        'timestamp': timestamp,
        'status': status
    }

def insert_order(order):
    table.put_item(Item=order)
    existing_orders[order['orderid']] = order
    print(f"[INSERT] Order inserted: {order}")

def modify_order(orderid):
    if orderid not in existing_orders:
        return
    updates = {
        'quantity': random.randint(1, 5),
        'status': random.choice(STATUSES),
        'timestamp': datetime.now(timezone.utc).isoformat()
    }
    table.update_item(
        Key={'orderid': orderid},
        UpdateExpression="SET quantity = :q, #s = :s, #t = :t",
        ExpressionAttributeNames={
            '#s': 'status',
            '#t': 'timestamp'
        },
        ExpressionAttributeValues={
            ':q': updates['quantity'],
            ':s': updates['status'],
            ':t': updates['timestamp']
        }
    )

    existing_orders[orderid]['quantity'] = updates['quantity']
    existing_orders[orderid]['status'] = updates['status']
    existing_orders[orderid]['timestamp'] = updates['timestamp']
    print(f"[MODIFY] Order {orderid} updated: {updates}")

def delete_order(orderid):
    if orderid not in existing_orders:
        return
    table.delete_item(Key={'orderid': orderid})
    del existing_orders[orderid]
    print(f"[REMOVE] Order {orderid} deleted.")

if __name__ == '__main__':
    try:
        while True:
            action = random.choices(
                ['insert', 'modify', 'delete'],
                weights=[60, 30, 10],  # 60% insert, 30% modify, 10% delete
                k=1
            )[0]

            if action == 'insert':
                order = generate_new_order()
                insert_order(order)

            elif action == 'modify' and existing_orders:
                orderid = random.choice(list(existing_orders.keys()))
                modify_order(orderid)

            elif action == 'delete' and existing_orders:
                orderid = random.choice(list(existing_orders.keys()))
                delete_order(orderid)

            time.sleep(1)  # Send one event per second

    except KeyboardInterrupt:
        print("Script stopped by user.")
