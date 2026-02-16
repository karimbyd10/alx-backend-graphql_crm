from datetime import datetime
from celery import shared_task
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport


@shared_task
def generate_crm_report():
    """
    Celery task to generate weekly CRM report via GraphQL.
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
        totalCustomers: customersCount
        totalOrders: ordersCount
        totalRevenue: totalRevenue
    }
    """)

    try:
        result = client.execute(query)
        customers = result.get("totalCustomers", 0)
        orders = result.get("totalOrders", 0)
        revenue = result.get("totalRevenue", 0)

        log_message = f"{timestamp} - Report: {customers} customers, {orders} orders, {revenue} revenue\n"

        with open("/tmp/crm_report_log.txt", "a") as log_file:
            log_file.write(log_message)

    except Exception as e:
        with open("/tmp/crm_report_log.txt", "a") as log_file:
            log_file.write(f"{timestamp} - Error generating report: {str(e)}\n")
