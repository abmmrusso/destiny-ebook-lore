import pytest
import mock
import httpretty
import json
import grimoireebook
from grimoireebook import DestinyContentAPIClientError

__dummyGrimoireDefinition__ = {"themes": [] }
__testApiKey__ = 'testApiKey'

@mock.patch('grimoireebook.loadDestinyGrimoireDefinition', autospec = True)
@mock.patch('grimoireebook.createGrimoireEpub', autospec = True)
def test_shouldTriggerGrimoireEbookGenerationWithDefaultValues(mock_createGrimoireEpub, mock_loadDestinyGrimoireDefinition):
	mock_loadDestinyGrimoireDefinition.return_value = __dummyGrimoireDefinition__
	
	grimoireebook.generateGrimoireEbook(__testApiKey__)

	mock_loadDestinyGrimoireDefinition.assert_called_once_with(__testApiKey__)
	mock_createGrimoireEpub.assert_called_once_with(__dummyGrimoireDefinition__)

@mock.patch('grimoireebook.getDestinyGrimoireFromBungie', autospec = True)
@mock.patch('grimoireebook.getDestinyGrimoireDefinitionFromJson', autospec = True)
def test_shouldLoadDestinyGrimoireDefinition(mock_getDestinyGrimoireDefinitionFromJson, mock_getDestinyGrimoireFromBungie):
	api_key = "apiKey"
	mock_getDestinyGrimoireFromBungie.return_value = __dummyGrimoireDefinition__
	mock_getDestinyGrimoireDefinitionFromJson.return_value = __dummyGrimoireDefinition__

	grimoireDefinition = grimoireebook.loadDestinyGrimoireDefinition(__testApiKey__)

	mock_getDestinyGrimoireFromBungie.assert_called_once_with(__testApiKey__)
	mock_getDestinyGrimoireDefinitionFromJson.assert_called_once_with(__dummyGrimoireDefinition__)

	assert grimoireDefinition == __dummyGrimoireDefinition__

def test_grimoireRetrievalFromBungieShouldTriggerExceptionIfNoAPIKeyIsGiven():
	with pytest.raises(DestinyContentAPIClientError) as expectedException:
		grimoireebook.getDestinyGrimoireFromBungie(None)

	assert str(expectedException.value) == DestinyContentAPIClientError.NO_API_KEY_PROVIDED_ERROR_MSG

	with pytest.raises(DestinyContentAPIClientError) as expectedException:
		grimoireebook.getDestinyGrimoireFromBungie("")

	assert str(expectedException.value) == DestinyContentAPIClientError.NO_API_KEY_PROVIDED_ERROR_MSG

@httpretty.activate
def test_shouldRetrieveGrimoireDataFromBungie():
	httpretty.register_uri(httpretty.GET, 
					'http://www.bungie.net/Platform/Destiny/Vanguard/Grimoire/Definition/', 
					body=json.dumps(__dummyGrimoireDefinition__),
					content_type='application/json',
					status=200)


	retrievedGrimoire = grimoireebook.getDestinyGrimoireFromBungie(__testApiKey__)

	assert httpretty.last_request().headers['X-API-Key'] == __testApiKey__
	assert retrievedGrimoire == __dummyGrimoireDefinition__