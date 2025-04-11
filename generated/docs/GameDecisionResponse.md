# GameDecisionResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **str** | Status of the game after the decision. | 
**score** | **int** | Current score of the player. | 
**client_id** | **str** |  | [optional] 
**client_data** | **object** | Client data for the player. | [optional] 

## Example

```python
from openapi_client.models.game_decision_response import GameDecisionResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GameDecisionResponse from a JSON string
game_decision_response_instance = GameDecisionResponse.from_json(json)
# print the JSON string representation of the object
print(GameDecisionResponse.to_json())

# convert the object into a dict
game_decision_response_dict = game_decision_response_instance.to_dict()
# create an instance of GameDecisionResponse from a dict
game_decision_response_from_dict = GameDecisionResponse.from_dict(game_decision_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


