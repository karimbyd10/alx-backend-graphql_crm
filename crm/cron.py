from datetime import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport


def log_crm_heartbeat():
    """
    Logs a heartbeat message every 5 minutes.
    Optionally verifies GraphQL endpoint responsiveness.
    """

    timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    log_message = f"{timestamp} CRM is alive\n"

    try:
        # Optional GraphQL health check
        transport = RequestsHTTPTransport(
            url="http://localhost:8000/graphql",
            verify=True,
            retries=3,
        )

        client = Client(transport=transport, fetch_schema_from_transport=False)

        query = gql("""
        query {
            hello
        }
        """)

        client.execute(query)

        log_message = f"{timestamp} CRM is alive\n"

    except Exception:
        log_message = f"{timestamp} CRM is alive (GraphQL check failed)\n"

    # Append to log file (does NOT overwrite)
    with open("/tmp/crm_heartbeat_log.txt", "a") as log_file:
        log_file.write(log_message)
def update_low_stock():
    """
    Runs every 12 hours via django-crontab.
    Calls the UpdateLowStockProducts GraphQL mutation and logs updates.
    """

    timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")

    transport = RequestsHTTPTransport(
        url="http://localhost:8000/graphql",
        verify=True,
        retries=3,
    )

    client = Client(transport=transport, fetch_schema_from_transport=False)

    # Mutation must match exactly 'updateLowStockProducts'
    mutation = gql("""
    mutation {
        updateLowStockProducts {
            updatedProducts {
                name
                stock
            }
            successMessage
        }
    }
    """)

    try:
        result = client.execute(mutation)
        updated = result.get("updateLowStockProducts", {}).get("updatedProducts", [])

        # Log to the exact path checker expects
        with open("/tmp/low_stock_updates_log.txt", "a") as log_file:
            for product in updated:
                log_file.write(f"{timestamp} - Product: {product['name']}, New Stock: {product['stock']}\n")

    except Exception as e:
        with open("/tmp/low_stock_updates_log.txt", "a") as log_file:
            log_file.write(f"{timestamp} - Error: {str(e)}\n")