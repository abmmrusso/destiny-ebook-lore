import pytest
import mock
import grimoireebook

class TestGrimoireBookGeneration:

	__dummyGrimoireDefinition__ = {"dummyGrimoire": "This is a dummy grimoire"}

	@mock.patch('grimoireebook.loadDestinyGrimoireDefinition', autospec=True)
	@mock.patch('grimoireebook.createGrimoireEpub', autospec=True)
	def test_shouldTriggerGrimoireEbookGenerationWithDefaultValues(self, mock_createGrimoireEpub, mock_loadDestinyGrimoireDefinition):
		api_key = "apiKey"
		mock_loadDestinyGrimoireDefinition.return_value=TestGrimoireBookGeneration.__dummyGrimoireDefinition__
		
		grimoireebook.generateGrimoireEbook(api_key)

		mock_loadDestinyGrimoireDefinition.assert_called_once_with(api_key)
		mock_createGrimoireEpub.assert_called_once_with(TestGrimoireBookGeneration.__dummyGrimoireDefinition__)