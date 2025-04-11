# GameStartRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**player_name** | **str** | Name of the player. | 

## Example

```python
from openapi_client.models.game_start_request import GameStartRequest

# TODO update the JSON string below
json = "{}"
# create an instance of GameStartRequest from a JSON string
game_start_request_instance = GameStartRequest.from_json(json)
# print the JSON string representation of the object
print(GameStartRequest.to_json())

# convert the object into a dict
game_start_request_dict = game_start_request_instance.to_dict()
# create an instance of GameStartRequest from a dict
game_start_request_from_dict = GameStartRequest.from_dict(game_start_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


