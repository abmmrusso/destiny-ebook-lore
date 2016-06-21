import requests
import urlparse
import jsonpath_rw
import urllib
import urllib2
import os
from PIL import Image
from sets import Set

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
	grimoireDefinition = { "themes" : []}

	for theme in grimoireJson["Response"]["themeCollection"]:
		themeToAdd = { "themeName" : theme["themeName"] , "pages" : [] }
		for page in theme["pageCollection"]:
			pageToAdd = { "pageName" : page["pageName"], "cards" : [] }
			for card in page["cardCollection"]:
				pageToAdd["cards"].append(
					{ "cardName" : card["cardName"], 
					"cardIntro" : card["cardIntro"], 
					"cardDescription" : card["cardDescription"],
					"image": { "sourceImage" : "http://www.bungie.net/" + card["highResolution"]["image"]["sheetPath"],
								"regionXStart" : card["highResolution"]["image"]["rect"]["x"],
								"regionYStart" : card["highResolution"]["image"]["rect"]["y"],
								"regionHeight" : card["highResolution"]["image"]["rect"]["height"],
								"regionWidth" : card["highResolution"]["image"]["rect"]["width"]}})
			themeToAdd["pages"].append(pageToAdd)
		grimoireDefinition["themes"].append(themeToAdd)
		
	return grimoireDefinition

def dowloadGrimoireImages(grimoireDefinition, localImageFolder):
	jsonpath_expr = jsonpath_rw.parse('themes[*].pages[*].cards[*].image')

	imagesToDownload = Set([match.value for match in jsonpath_expr.find(grimoireDefinition)])

	os.makedirs(localImageFolder)

	for imageURL in imagesToDownload:
		urllib.urlretrieve(imageURL, os.path.join(localImageFolder, urlparse.urlsplit(imageURL).path.split('/')[-1]))

def generateCardImageFromImageSheet(cardName, sheetImagePath, localImageFolder, dimensions_tuple):
	generatedImagePath = os.path.join(localImageFolder, '%s%s' % (cardName, os.path.splitext(sheetImagePath)[1]))

	sheetImage = Image.open(sheetImagePath)
	print (sheetImage)
	cardImage = sheetImage.crop((dimensions_tuple[0], dimensions_tuple[1], dimensions_tuple[0] + dimensions_tuple[2], dimensions_tuple[1] + dimensions_tuple[3]))
	cardImage.save(generatedImagePath, optimize=True)

	return generatedImagePath

class DestinyContentAPIClientError(Exception):
	NO_API_KEY_PROVIDED_ERROR_MSG = "No API key provided. One is required to refresh the content cache."

	def __init__(self, value):
		self.value = value

	def __str__(self):
		return self.value