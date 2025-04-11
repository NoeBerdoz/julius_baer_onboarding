# openapi_client.DefaultApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**game_decision_game_decision_post**](DefaultApi.md#game_decision_game_decision_post) | **POST** /game/decision | Game Decision
[**game_start_game_start_post**](DefaultApi.md#game_start_game_start_post) | **POST** /game/start | Game Start


# **game_decision_game_decision_post**
> GameDecisionResponse game_decision_game_decision_post(game_decision_request)

Game Decision

Log decision, update the score and proceed with game.

### Example


```python
import openapi_client
from openapi_client.models.game_decision_request import GameDecisionRequest
from openapi_client.models.game_decision_response import GameDecisionResponse
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    game_decision_request = openapi_client.GameDecisionRequest() # GameDecisionRequest | 

    try:
        # Game Decision
        api_response = api_instance.game_decision_game_decision_post(game_decision_request)
        print("The response of DefaultApi->game_decision_game_decision_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->game_decision_game_decision_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **game_decision_request** | [**GameDecisionRequest**](GameDecisionRequest.md)|  | 

### Return type

[**GameDecisionResponse**](GameDecisionResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **game_start_game_start_post**
> GameStartResponse game_start_game_start_post(game_start_request)

Game Start

Start a new game session for the player.

### Example


```python
import openapi_client
from openapi_client.models.game_start_request import GameStartRequest
from openapi_client.models.game_start_response import GameStartResponse
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    game_start_request = openapi_client.GameStartRequest() # GameStartRequest | 

    try:
        # Game Start
        api_response = api_instance.game_start_game_start_post(game_start_request)
        print("The response of DefaultApi->game_start_game_start_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->game_start_game_start_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **game_start_request** | [**GameStartRequest**](GameStartRequest.md)|  | 

### Return type

[**GameStartResponse**](GameStartResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

