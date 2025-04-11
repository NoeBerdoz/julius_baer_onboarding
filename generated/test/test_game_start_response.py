# coding: utf-8

"""
    Master

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)

    The version of the OpenAPI document: 0.1.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from openapi_client.models.game_start_response import GameStartResponse

class TestGameStartResponse(unittest.TestCase):
    """GameStartResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> GameStartResponse:
        """Test GameStartResponse
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `GameStartResponse`
        """
        model = GameStartResponse()
        if include_optional:
            return GameStartResponse(
                message = 'Game started successfully.',
                session_id = '92ab2b1a-a3b5-4e36-af59-2d4083a18ee6',
                player_id = 'some_key',
                client_id = '42048bf6-5947-4797-bac9-348e23dcc904',
                client_data = {data={}},
                score = 0
            )
        else:
            return GameStartResponse(
                message = 'Game started successfully.',
                session_id = '92ab2b1a-a3b5-4e36-af59-2d4083a18ee6',
                player_id = 'some_key',
                client_id = '42048bf6-5947-4797-bac9-348e23dcc904',
                client_data = {data={}},
                score = 0,
        )
        """

    def testGameStartResponse(self):
        """Test GameStartResponse"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
