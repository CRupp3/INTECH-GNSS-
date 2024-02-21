from datetime import datetime, timezone

print(datetime.utcnow().replace(tzinfo=timezone.utc).strftime('%m%d%y%H%M'))
