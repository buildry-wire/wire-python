# wirepayment (Python)

Official Python SDK for the [Wire](https://wire.mn) payment API.

## Install
```bash
pip install wirepayment
```

## Quickstart
```python
import wire

client = wire.Client("sk_live_...")

pi = client.payment_intents.create(amount=50000, currency="MNT")  # minor units
print(pi.id, pi.status)
```

## Auto-pagination
```python
for charge in client.charges.list(limit=50):
    print(charge.id)
```

## Webhook verification
```python
import wire

event = client.webhooks.verify(
    request.body,                       # raw bytes
    request.headers[wire.SIGNATURE_HEADER],
    endpoint_secret,
)
print(event.type)
```

## Errors
```python
try:
    client.payment_intents.create(amount=-1)
except wire.WireError as e:
    print(e.code, e.request_id, e.status_code)
```

## License
MIT
