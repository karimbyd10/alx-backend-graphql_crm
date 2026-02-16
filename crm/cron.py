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
