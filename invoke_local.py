import json
from src.main import lambda_handler
# from events.add_album import event
# from events.get import event
# from events.getAllAlbums import event
# from events.update_album import event
# from events.search_spotify import event
# from events.delete_album import event
from events.add_vinyl import event
response = (lambda_handler(event, None))
print(json.dumps(response, indent=4))
