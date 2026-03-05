import json
import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# ── Personalize Runtime client ──
personalize_runtime = boto3.client("personalize-runtime", region_name="us-east-1")

# ── Your Personalize Campaign ARN ──
# Replace this with your actual Campaign ARN from Amazon Personalize console
CAMPAIGN_ARN = "arn:aws:personalize:us-east-1:578575721667:campaign/YOUR_CAMPAIGN_NAME"

def lambda_handler(event, context):
    logger.info("FULL EVENT: %s", json.dumps(event))

    action_group = event.get("actionGroup")
    api_path     = event.get("apiPath")
    http_method  = event.get("httpMethod", "").upper()
    parameters   = event.get("parameters", [])

    # Extract query parameters
    params = {p["name"]: p["value"] for p in parameters}
    logger.info("Extracted params: %s", json.dumps(params))

    if api_path == "/personalize-recommendation" and http_method == "GET":
        response_body = get_personalize_recommendations(params)
    else:
        response_body = {"error": f"Unknown api_path '{api_path}' or method '{http_method}'"}

    return build_response(action_group, api_path, http_method, response_body)


def get_personalize_recommendations(params):
    product_name = params.get("product_name")
    user_id      = params.get("user_id")
    num_results  = int(params.get("num_results", 5))

    # Validate required fields
    if not product_name:
        return {"error": "Missing required parameter: product_name"}
    if not user_id:
        return {"error": "Missing required parameter: user_id"}

    try:
        logger.info("Calling Personalize for user_id=%s, product_name=%s, num_results=%d",
                    user_id, product_name, num_results)

        # ── Call Amazon Personalize ──
        personalize_response = personalize_runtime.get_recommendations(
            campaignArn=CAMPAIGN_ARN,
            userId=user_id,
            numResults=num_results,
            # Pass product_name as context for better relevance
            context={
                "product_name": product_name
            }
        )

        item_list = personalize_response.get("itemList", [])
        logger.info("Personalize returned %d items", len(item_list))

        # ── Enrich recommendations with product details ──
        # Personalize returns item IDs — fetch product details from DynamoDB
        recommendations = enrich_recommendations(item_list)

        return {
            "recommendations": recommendations,
            "user_id": user_id,
            "total_results": len(recommendations)
        }

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        error_msg  = e.response["Error"]["Message"]
        logger.error("Personalize ClientError: %s - %s", error_code, error_msg)
        return {
            "error": f"Personalize error: {error_code} - {error_msg}",
            "recommendations": [],
            "user_id": user_id,
            "total_results": 0
        }

    except Exception as e:
        logger.error("Unexpected error: %s", str(e))
        return {
            "error": f"Unexpected error: {str(e)}",
            "recommendations": [],
            "user_id": user_id,
            "total_results": 0
        }


def enrich_recommendations(item_list):
    """
    Personalize returns only item IDs and scores.
    This function fetches product details from DynamoDB to enrich the response.
    Replace 'ProductsTable' with your actual products table name.
    """
    if not item_list:
        return []

    dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
    table    = dynamodb.Table("ProductsTable")  # Replace with your products table name

    recommendations = []

    for item in item_list:
        product_id = item.get("itemId")
        score      = float(item.get("score", 0))

        try:
            # Fetch product details from DynamoDB using product_id
            db_response = table.get_item(
                Key={"product_id": product_id}
            )
            product = db_response.get("Item", {})

            recommendations.append({
                "product_id":           product_id,
                "product_name":         product.get("product_name", "Unknown"),
                "category":             product.get("category", "Unknown"),
                "price":                float(product.get("price", 0)),
                "rating":               float(product.get("rating", 0)),
                "recommendation_score": round(score, 4)
            })

        except Exception as e:
            logger.warning("Could not fetch details for product_id=%s: %s", product_id, str(e))
            # Still include the item with minimal info rather than dropping it
            recommendations.append({
                "product_id":           product_id,
                "product_name":         "Unknown",
                "category":             "Unknown",
                "price":                0,
                "rating":               0,
                "recommendation_score": round(score, 4)
            })

    return recommendations


def build_response(action_group, api_path, http_method, body):
    return {
        "messageVersion": "1.0",
        "response": {
            "actionGroup": action_group,
            "apiPath":     api_path,
            "httpMethod":  http_method,
            "httpStatusCode": 200,
            "responseBody": {
                "application/json": {
                    "body": json.dumps(body)
                }
            }
        }
    }
