#!/usr/bin/env python3

from datetime import datetime, timedelta
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

# GraphQL endpoint
transport = RequestsHTTPTransport(
    url="http://localhost:8000/graphql",
    verify=True,
    retries=3,
)

client = Client(transport=transport, fetch_schema_from_transport=False)

# Calculate date 7 days ago
seven_days_ago = (datetime.utcnow() - timedelta(days=7)).isoformat()

# GraphQL query (adjust field names if needed to match your schema)
query = gql(
    """
    query GetRecentOrders($date: DateTime!) {
        orders(orderDate_Gte: $date) {
            id
            orderDate
            customer {
                email
            }
        }
    }
"""
)

params = {"date": seven_days_ago}

try:
    result = client.execute(query, variable_values=params)
    orders = result.get("orders", [])

    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    with open("/tmp/order_reminders_log.txt", "a") as log_file:
        for order in orders:
            log_file.write(
                f"{timestamp} - Order ID: {order['id']}, Customer Email: {order['customer']['email']}\n"
            )

    print("Order reminders processed!")

except Exception as e:
    with open("/tmp/order_reminders_log.txt", "a") as log_file:
        log_file.write(f"{datetime.utcnow()} - Error: {str(e)}\n")
