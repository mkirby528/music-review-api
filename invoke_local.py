import json
from src.main import lambda_handler
# from events.post import event
# from events.get import event
# from events.getAllAlbums import event
# from events.updateAlbum import event
from events.search_spotify import event

response = (lambda_handler(event, None))
print(json.dumps(response, indent=4))
