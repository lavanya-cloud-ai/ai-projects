"""
Lambda Function: Product Details API
For: Amazon Bedrock Agent - Gift Recommendation POC
Account: lavanya-cloud-ai-lab
Fix: Corrected Bedrock Agent response format to echo back exact event values
"""

import json

# ---------------------------------------------------------------------------
# Mock Product Catalog
# ---------------------------------------------------------------------------
PRODUCTS = [
    {
        "product_id": "P001",
        "product_name": "Wireless Noise-Cancelling Headphones",
        "category": "electronics",
        "gender": "unisex",
        "age_group": "adults",
        "price": 79.99,
        "occasion": ["birthday", "graduation", "holiday"],
        "interest": ["music", "gaming", "travel"],
        "description": "Premium wireless headphones with active noise cancellation and 30-hour battery life.",
        "rating": 4.7,
        "in_stock": True
    },
    {
        "product_id": "P002",
        "product_name": "Luxury Scented Candle Set",
        "category": "beauty",
        "gender": "female",
        "age_group": "adults",
        "price": 34.99,
        "occasion": ["birthday", "anniversary", "mothers_day", "valentines"],
        "interest": ["art", "cooking"],
        "description": "Set of 3 hand-poured soy candles in lavender, vanilla, and rose scents.",
        "rating": 4.8,
        "in_stock": True
    },
    {
        "product_id": "P003",
        "product_name": "Fitness Resistance Bands Set",
        "category": "sports",
        "gender": "unisex",
        "age_group": "adults",
        "price": 24.99,
        "occasion": ["birthday", "graduation", "holiday"],
        "interest": ["fitness"],
        "description": "Set of 5 resistance bands with varying tension levels for home workouts.",
        "rating": 4.5,
        "in_stock": True
    },
    {
        "product_id": "P004",
        "product_name": "Personalized Travel Journal",
        "category": "books",
        "gender": "unisex",
        "age_group": "adults",
        "price": 19.99,
        "occasion": ["birthday", "graduation", "holiday"],
        "interest": ["travel", "reading", "art"],
        "description": "Leather-bound travel journal with world map pages and packing checklists.",
        "rating": 4.6,
        "in_stock": True
    },
    {
        "product_id": "P005",
        "product_name": "Smart Watch",
        "category": "electronics",
        "gender": "unisex",
        "age_group": "adults",
        "price": 149.99,
        "occasion": ["birthday", "anniversary", "graduation", "fathers_day", "mothers_day"],
        "interest": ["fitness", "travel", "gaming"],
        "description": "Feature-rich smartwatch with health tracking, GPS, and 5-day battery life.",
        "rating": 4.6,
        "in_stock": True
    },
    {
        "product_id": "P006",
        "product_name": "Cooking Masterclass Cookbook",
        "category": "books",
        "gender": "unisex",
        "age_group": "adults",
        "price": 29.99,
        "occasion": ["birthday", "anniversary", "holiday", "mothers_day"],
        "interest": ["cooking"],
        "description": "Award-winning cookbook with 150 recipes from professional chefs around the world.",
        "rating": 4.9,
        "in_stock": True
    },
    {
        "product_id": "P007",
        "product_name": "LEGO Architecture Set",
        "category": "toys",
        "gender": "unisex",
        "age_group": "kids",
        "price": 49.99,
        "occasion": ["birthday", "holiday"],
        "interest": ["art", "gaming"],
        "description": "960-piece LEGO set featuring famous world landmarks. Ages 12+.",
        "rating": 4.8,
        "in_stock": True
    },
    {
        "product_id": "P008",
        "product_name": "Men's Leather Wallet",
        "category": "fashion",
        "gender": "male",
        "age_group": "adults",
        "price": 39.99,
        "occasion": ["birthday", "fathers_day", "graduation", "holiday"],
        "interest": ["travel"],
        "description": "Slim genuine leather bifold wallet with RFID blocking technology.",
        "rating": 4.5,
        "in_stock": True
    },
    {
        "product_id": "P009",
        "product_name": "Watercolor Paint Set",
        "category": "beauty",
        "gender": "unisex",
        "age_group": "teens",
        "price": 27.99,
        "occasion": ["birthday", "holiday", "graduation"],
        "interest": ["art"],
        "description": "Professional 48-color watercolor set with brushes and a mixing palette.",
        "rating": 4.7,
        "in_stock": True
    },
    {
        "product_id": "P010",
        "product_name": "Portable Bluetooth Speaker",
        "category": "electronics",
        "gender": "unisex",
        "age_group": "teens",
        "price": 44.99,
        "occasion": ["birthday", "graduation", "holiday"],
        "interest": ["music", "travel", "fitness"],
        "description": "Waterproof portable speaker with 360-degree sound and 12-hour playtime.",
        "rating": 4.6,
        "in_stock": True
    },
    {
        "product_id": "P011",
        "product_name": "Silk Pajama Set",
        "category": "fashion",
        "gender": "female",
        "age_group": "adults",
        "price": 59.99,
        "occasion": ["birthday", "anniversary", "valentines", "mothers_day", "holiday"],
        "interest": [],
        "description": "Luxurious 100% mulberry silk pajama set in multiple colors.",
        "rating": 4.8,
        "in_stock": True
    },
    {
        "product_id": "P012",
        "product_name": "Gaming Controller Stand",
        "category": "electronics",
        "gender": "male",
        "age_group": "teens",
        "price": 18.99,
        "occasion": ["birthday", "holiday"],
        "interest": ["gaming"],
        "description": "Dual controller charging stand compatible with PS5 and Xbox controllers.",
        "rating": 4.4,
        "in_stock": True
    },
    {
        "product_id": "P013",
        "product_name": "Herb Garden Starter Kit",
        "category": "sports",
        "gender": "unisex",
        "age_group": "adults",
        "price": 32.99,
        "occasion": ["birthday", "mothers_day", "holiday"],
        "interest": ["cooking"],
        "description": "Indoor herb garden kit with basil, mint, parsley, and cilantro seeds.",
        "rating": 4.5,
        "in_stock": True
    },
    {
        "product_id": "P014",
        "product_name": "Yoga Mat Premium",
        "category": "sports",
        "gender": "female",
        "age_group": "adults",
        "price": 55.99,
        "occasion": ["birthday", "mothers_day", "holiday"],
        "interest": ["fitness"],
        "description": "Extra thick non-slip yoga mat with alignment lines and carry strap.",
        "rating": 4.7,
        "in_stock": True
    },
    {
        "product_id": "P015",
        "product_name": "Classic Board Game Bundle",
        "category": "toys",
        "gender": "unisex",
        "age_group": "kids",
        "price": 42.99,
        "occasion": ["birthday", "holiday"],
        "interest": ["gaming"],
        "description": "Bundle of 5 classic family board games including Chess, Checkers, and Scrabble.",
        "rating": 4.6,
        "in_stock": True
    }
]


# ---------------------------------------------------------------------------
# Filter Logic
# ---------------------------------------------------------------------------
def filter_products(params):
    results = PRODUCTS

    if params.get("product_name"):
        name_filter = params["product_name"].lower()
        results = [p for p in results if name_filter in p["product_name"].lower()]

    if params.get("category"):
        results = [p for p in results if p["category"] == params["category"].lower()]

    if params.get("gender"):
        gender = params["gender"].lower()
        results = [p for p in results if p["gender"] == gender or p["gender"] == "unisex"]

    if params.get("age_group"):
        results = [p for p in results if p["age_group"] == params["age_group"].lower()]

    if params.get("occasion"):
        occasion = params["occasion"].lower()
        results = [p for p in results if occasion in p["occasion"]]

    if params.get("interest"):
        interest = params["interest"].lower()
        results = [p for p in results if interest in p["interest"]]

    if params.get("min_price"):
        results = [p for p in results if p["price"] >= float(params["min_price"])]

    if params.get("max_price"):
        results = [p for p in results if p["price"] <= float(params["max_price"])]

    return results


# ---------------------------------------------------------------------------
# Parse parameters from Bedrock Agent event
# ---------------------------------------------------------------------------
def parse_parameters(event):
    params = {}
    # Bedrock sends parameters as a list of {name, type, value} dicts
    for param in event.get("parameters", []):
        params[param["name"]] = param["value"]
    return params


# ---------------------------------------------------------------------------
# Lambda Handler
# ---------------------------------------------------------------------------
def lambda_handler(event, context):
    print(f"Event received: {json.dumps(event)}")

    # Extract event fields — echo these back exactly in the response
    action_group = event.get("actionGroup", "")
    api_path     = event.get("apiPath", "")
    http_method  = event.get("httpMethod", "GET")

    try:
        params   = parse_parameters(event)
        products = filter_products(params)

        response_body = {
            "products": products,
            "total_count": len(products)
        }

        http_status = 200

    except Exception as e:
        print(f"Error: {str(e)}")
        response_body = {"error": str(e)}
        http_status   = 500

    # -----------------------------------------------------------------------
    # CRITICAL: Bedrock requires this exact response structure
    # - messageVersion must be "1.0"
    # - actionGroup, apiPath, httpMethod must echo back what Bedrock sent
    # - body must be a STRING (json.dumps), not a dict
    # -----------------------------------------------------------------------
    return {
        "messageVersion": "1.0",
        "response": {
            "actionGroup": action_group,
            "apiPath": api_path,
            "httpMethod": http_method,
            "httpStatusCode": http_status,
            "responseBody": {
                "application/json": {
                    "body": json.dumps(response_body)
                }
            }
        }
    }
