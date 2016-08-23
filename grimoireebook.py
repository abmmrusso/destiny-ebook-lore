import requests
import urlparse
import jsonpath_rw
import urllib
import urllib2
import os
import collections
from PIL import Image
from sets import Set
from ebooklib import epub

DEFAULT_PAGE_STYLE = '''
	cardname {
		display: block;
		text-align: center;
		font-size:150%;
	}
	cardimage {
		float: left;
		margin-right: 5%;
		width: 40%;
		height: 40%;
	}
	cardintro {
		display: block;
		padding: 5%;
	}
	carddescription {}
	container {
		width: 100%;
		clear: both;
	}
'''

DEFAULT_IMAGE_FOLDER = 'images'

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

def generateGrimoirePageContent(pageData, pageImagePath):
	return u'''<cardname">%s</cardname>
			   <cardintro>%s</cardintro>
			   <container>
				<cardimage><img src="%s"/></cardimage>
				<carddescription">%s</carddescription>
			   </container>''' % ( pageData["cardName"], pageData["cardIntro"], pageImagePath, pageData["cardDescription"] )

def generateGrimoirePageImage(imageName, imageData, imagesFolder):
	imageBaseFileName = '%s_img' % (imageName)
	imagePath = generateCardImageFromImageSheet(imageBaseFileName, os.path.join(imagesFolder, os.path.basename(imageData["sourceImage"])),imagesFolder, (imageData["regionXStart"], imageData["regionYStart"], imageData["regionWidth"], imageData["regionHeight"]))
	return epub.EpubItem(uid=imageBaseFileName, file_name=imagePath, content=open(imagePath, 'rb').read())

def createGrimoireCardPage(pageData, pageCSS):
	bookPage = epub.EpubHtml(title=pageData["cardName"], file_name='%s.%s' % (pageData["cardName"], 'xhtml'), lang='en', content="")
	bookPage.add_item(pageCSS)
	pageImage = generateGrimoirePageImage(pageData["cardName"], pageData["image"], DEFAULT_IMAGE_FOLDER)
	bookPage.content = generateGrimoirePageContent(pageData, pageImage.file_name)
	return collections.namedtuple('GrimoirePage', ['page', 'image'])(page=bookPage, image=pageImage)

def addPageItemsToEbook(ebook, pageData):
	pageCards = ()
	for cardData in pageData['cards']:
		cardPage = createGrimoireCardPage(cardData, DEFAULT_PAGE_STYLE)
		ebook.add_item(cardPage)
		ebook.spine.append(cardPage)
		pageCards = pageCards + (cardPage,)
	return pageCards

class DestinyContentAPIClientError(Exception):
	NO_API_KEY_PROVIDED_ERROR_MSG = "No API key provided. One is required to refresh the content cache."

	def __init__(self, value):
		self.value = value

	def __str__(self):
		return self.value