import requests

def generateGrimoireEbook(apiKey):
	createGrimoireEpub(loadDestinyGrimoireDefinition(apiKey))

def loadDestinyGrimoireDefinition(apiKey):
	return getDestinyGrimoireDefinitionFromJson(getDestinyGrimoireFromBungie(apiKey))

def createGrimoireEpub(destinyGrimoireDefinition):
	return

def getDestinyGrimoireFromBungie(apiKey):
	if apiKey is None or not apiKey:
			raise DestinyContentAPIClientError(DestinyContentAPIClientError.NO_API_KEY_PROVIDED_ERROR_MSG)
	return requests.get('http://www.bungie.net/Platform/Destiny/Vanguard/Grimoire/Definition/', headers={'X-API-Key': apiKey}).json()

def getDestinyGrimoireDefinitionFromJson(grimoireJson):
	return

class DestinyContentAPIClientError(Exception):
	NO_API_KEY_PROVIDED_ERROR_MSG = "No API key provided. One is required to refresh the content cache."

	def __init__(self, value):
		self.value = value

	def __str__(self):
		return self.value