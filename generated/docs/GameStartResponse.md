# GameStartResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**message** | **str** | Message indicating the game has started. | 
**session_id** | **str** | Unique session ID for the game. | 
**player_id** | **str** | Unique player ID for the game. | 
**client_id** | **str** | Unique client ID for the game. | 
**client_data** | **object** | Client data for the player. | 
**score** | **int** | Starting score of the player. | 

## Example

```python
from openapi_client.models.game_start_response import GameStartResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GameStartResponse from a JSON string
game_start_response_instance = GameStartResponse.from_json(json)
# print the JSON string representation of the object
print(GameStartResponse.to_json())

# convert the object into a dict
game_start_response_dict = game_start_response_instance.to_dict()
# create an instance of GameStartResponse from a dict
game_start_response_from_dict = GameStartResponse.from_dict(game_start_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


