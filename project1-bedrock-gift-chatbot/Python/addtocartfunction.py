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

    request_body = event.get("requestBody", {})
    content = request_body.get("content", {})
    json_body = content.get("application/json", {}).get("properties", [])

    body_params = {p["name"]: p["value"] for p in json_body}

    if api_path == "/cart/items" and http_method == "POST":
        response_body = add_to_cart(body_params)
    else:
        response_body = {"error": "Unknown API path or method"}

    return build_response(action_group, api_path, http_method, response_body)


def add_to_cart(body_params):
    print("body_params received:", json.dumps(body_params))
    user_id = body_params.get("userId")
    product_id = body_params.get("productId")
    quantity = int(body_params.get("quantity", 1))
    product_name = body_params.get("productName", "Unknown Product")
    price = Decimal(str(body_params.get("price", 0)))

    try:
        # If item exists, increment quantity. If not, create it.
        table.update_item(
            Key={
                "userId": user_id,
                "productId": product_id
            },
            UpdateExpression="""
                SET productName = :name,
                    price = :price,
                    quantity = if_not_exists(quantity, :zero) + :qty
            """,
            ExpressionAttributeValues={
                ":name": product_name,
                ":price": price,
                ":qty": Decimal(quantity),
                ":zero": Decimal(0)
            },
            ReturnValues="ALL_NEW"
        )

        # Get updated cart count for this user
        response = table.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key("userId").eq(user_id)
        )
        cart_item_count = sum(int(item["quantity"]) for item in response["Items"])

        return {
            "success": True,
            "message": f"Added {quantity} x {product_name} to cart for user {user_id}",
            "cart": {
                "userId": user_id,
                "updatedItem": {
                    "productId": product_id,
                    "productName": product_name,
                    "quantity": quantity,
                    "price": float(price)
                },
                "cartItemCount": cart_item_count
            }
        }

    except Exception as e:
        print("ERROR:", str(e))
        return {
            "success": False,
            "message": f"Failed to add item to cart: {str(e)}"
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
