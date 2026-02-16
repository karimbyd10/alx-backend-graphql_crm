#!/bin/bash

# Move to project root (adjust if necessary)
PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$PROJECT_ROOT" || exit 1

# Execute Django shell command to delete inactive customers
DELETED_COUNT=$(python manage.py shell -c "
from django.utils import timezone
from datetime import timedelta
from crm.models import Customer

one_year_ago = timezone.now() - timedelta(days=365)

inactive_customers = Customer.objects.filter(
    orders__isnull=True,
    created_at__lt=one_year_ago
).distinct()

count = inactive_customers.count()
inactive_customers.delete()

print(count)
")

# Log deletion count with timestamp
echo \"$(date '+%Y-%m-%d %H:%M:%S') - Deleted $DELETED_COUNT inactive customers\" >> /tmp/customer_cleanup_log.txt
