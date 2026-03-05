import json
import boto3
from decimal import Decimal

dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
table = dynamodb.Table("productdetailscart")

def lambda_handler(event, context):
    print("FULL EVENT:", json.dumps(event))

    action_group = event.get("actionGroup")
    api_path = event.get("apiPath")
    http_method = event.get("httpMethod", "").upper()
    parameters = event.get("parameters", [])

    params = {p["name"]: p["value"] for p in parameters}
    user_id = params.get("userId")

    if api_path == "/cart" and http_method == "GET":
        response_body = get_cart(user_id)
    else:
        response_body = {"error": "Unknown API path or method"}

    return build_response(action_group, api_path, http_method, response_body)


def get_cart(user_id):
    try:
        response = table.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key("userId").eq(user_id)
        )

        items = response.get("Items", [])

        if not items:
            return {
                "userId": user_id,
                "items": [],
                "totalItems": 0,
                "totalPrice": 0.0,
                "message": "Cart is empty"
            }

        # Build item list and calculate totals
        cart_items = []
        total_items = 0
        total_price = 0.0

        for item in items:
            quantity = int(item.get("quantity", 0))
            price = float(item.get("price", 0))
            cart_items.append({
                "productId": item["productId"],
                "productName": item.get("productName", "Unknown"),
                "quantity": quantity,
                "price": price,
                "subtotal": round(quantity * price, 2)
            })
            total_items += quantity
            total_price += quantity * price

        return {
            "userId": user_id,
            "items": cart_items,
            "totalItems": total_items,
            "totalPrice": round(total_price, 2)
        }

    except Exception as e:
        print("ERROR:", str(e))
        return {
            "userId": user_id,
            "items": [],
            "totalItems": 0,
            "totalPrice": 0.0,
            "message": f"Failed to retrieve cart: {str(e)}"
        }


def build_response(action_group, api_path, http_method, body):
    return {
        "messageVersion": "1.0",
        "response": {
            "actionGroup": action_group,
            "apiPath": api_path,
            "httpMethod": http_method,
            "httpStatusCode": 200,
            "responseBody": {
                "application/json": {
                    "body": json.dumps(body)
                }
            }
        }
    }
