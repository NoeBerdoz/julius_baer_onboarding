# GameDecisionRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**decision** | **str** | Decision of the player. | 
**session_id** | **str** | Unique session ID for the game. | 
**client_id** | **str** | Unique client ID for the game. | 

## Example

```python
from openapi_client.models.game_decision_request import GameDecisionRequest

# TODO update the JSON string below
json = "{}"
# create an instance of GameDecisionRequest from a JSON string
game_decision_request_instance = GameDecisionRequest.from_json(json)
# print the JSON string representation of the object
print(GameDecisionRequest.to_json())

# convert the object into a dict
game_decision_request_dict = game_decision_request_instance.to_dict()
# create an instance of GameDecisionRequest from a dict
game_decision_request_from_dict = GameDecisionRequest.from_dict(game_decision_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


