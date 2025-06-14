import base64
import json

def lambda_handler(event, context):
    output = []

    for record in event['records']:
        try:
            # Decode base64 record data
            payload = base64.b64decode(record['data'])
            data = json.loads(payload)

            # Check for supported CDC event type
            event_name = data.get('eventName')
            if event_name not in ['INSERT', 'MODIFY']:
                    output.append({
                        'recordId': record['recordId'],
                        'result': 'Dropped',
                        'data': record['data']
                    })
                    continue

            # Extract and flatten NewImage
            new_image = data['dynamodb']['NewImage']
            transformed_data = {
                'orderid': new_image['orderid']['S'],
                'product_name': new_image['product_name']['S'],
                'quantity': int(new_image['quantity']['N']),
                'price': float(new_image['price']['N']),
                'customer_id': new_image['customer_id']['S'],
                'payment_method': new_image['payment_method']['S'],
                'status': new_image['status']['S'],
                'order_timestamp': new_image['timestamp']['S'],
                'cdc_event_type': event_name,
                'total_price': round(float(new_image['price']['N']) * int(new_image['quantity']['N']), 2)
            }

            # Convert the transformed data to a JSON string and then encode it as base64
            transformed_data_str = json.dumps(transformed_data) + '\n'
            transformed_data_encoded = base64.b64encode(transformed_data_str.encode('utf-8')).decode('utf-8')

            # Append the transformed record to the output using 'eventID' as 'recordId'
            output.append({
                'recordId': record['recordId'],
                'result': 'Ok',
                'data': transformed_data_encoded
            })

        except Exception as e:
            print(f"Error processing record: {e}")
            output.append({
                'recordId': record['recordId'],
                'result': 'ProcessingFailed',
                'data': record['data']
            })

    return {'records': output}
