import os
from dotenv import load_dotenv
from hindsight_client import Hindsight

load_dotenv()

hindsight = Hindsight(
    base_url="https://api.hindsight.vectorize.io",
    api_key=os.getenv("HINDSIGHT_API_KEY"),
)

BANK_ID = "incident-agent"

past_incidents = [
    {
        "id": "inc-001",
        "content": "Incident: Payment service returning 500 errors on checkout. "
                    "Symptoms: spike in HTTP 500s from payment-service, checkout success rate dropped to 40%. "
                    "Root cause: a config deployment removed the DB_CONNECTION_POOL_SIZE env variable, "
                    "causing the service to fall back to a pool size of 1 and exhaust connections under load. "
                    "Resolution: rolled back the config deployment, restored the env variable, service recovered in 6 minutes.",
    },
    {
        "id": "inc-002",
        "content": "Incident: Payment service latency spike, checkout timeouts. "
                    "Symptoms: p99 latency on payment-service jumped from 200ms to 8s. "
                    "Root cause: a downstream fraud-check API started rate-limiting our requests after a traffic spike. "
                    "Resolution: added a circuit breaker with a 2s timeout and fallback to manual review queue.",
    },
    {
        "id": "inc-003",
        "content": "Incident: Authentication service returning 401 errors for valid users. "
                    "Symptoms: login failures across all regions, support tickets spiking. "
                    "Root cause: JWT signing key rotated but the old key was removed before all services picked up the new one. "
                    "Resolution: restored the old key temporarily, staggered the rollout of the new key across services.",
    },
    {
        "id": "inc-004",
        "content": "Incident: Order service database connection failures. "
                    "Symptoms: intermittent 500 errors, database CPU at 95%. "
                    "Root cause: a new analytics query was running unindexed full table scans against the production orders table. "
                    "Resolution: added an index on order_date and customer_id, moved the analytics query to a read replica.",
    },
    {
        "id": "inc-005",
        "content": "Incident: Payment service connection pool exhaustion during flash sale. "
                    "Symptoms: payment-service 500 errors returned during high traffic event, similar to a past incident. "
                    "Root cause: connection pool size was set correctly but too low for flash-sale-level traffic. "
                    "Resolution: increased DB_CONNECTION_POOL_SIZE and added autoscaling triggered by connection pool usage above 80%.",
    },
]

for inc in past_incidents:
    hindsight.retain(
        bank_id=BANK_ID,
        content=inc["content"],
        context="incident postmortem",
        document_id=inc["id"],
        tags=["incident"],
    )
    print(f"Retained {inc['id']}")

print("Done seeding incidents.") 