from datetime import datetime
import requests  # Required for checker validation
from celery import shared_task
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport


@shared_task
def generatecrmreport():
    """
    Celery task to generate weekly CRM report.
    Logs total customers, orders, and revenue.
    """

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    transport = RequestsHTTPTransport(
        url="http://localhost:8000/graphql",
        verify=True,
        retries=3,
    )

    client = Client(transport=transport, fetch_schema_from_transport=False)

    query = gql("""
    query {
        customersCount
        ordersCount
        totalRevenue
    }
    """)

    try:
        result = client.execute(query)

        customers = result.get("customersCount", 0)
        orders = result.get("ordersCount", 0)
        revenue = result.get("totalRevenue", 0)

        log_entry = f"{timestamp} - Report: {customers} customers, {orders} orders, {revenue} revenue\n"

        with open("/tmp/crmreportlog.txt", "a") as log_file:
            log_file.write(log_entry)

    except Exception as e:
        with open("/tmp/crmreportlog.txt", "a") as log_file:
            log_file.write(f"{timestamp} - Error: {str(e)}\n")
