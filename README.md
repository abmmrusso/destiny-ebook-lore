# destiny-ebook-lore

This tool to generate ebooks for [Destiny](https://www.destinythegame.com) lore based on info retrieved from the existing [Bungie APIs](www.bungie.net/Platform/Destiny).
It is a rework of [this "hack session" style tool](https://github.com/abmmrusso/destiny-ebook-lore-hacksession).

## Requirements
This software requires the following to be run

1. Python 2.7 (https://www.python.org/download/releases/2.7/)
2. pip (https://pip.pypa.io/en/stable/installing)
3. A created Bungie app credential (https://www.bungie.net/en/Application/Create)

## Running

1. Make a note of the created API Key
2. Install all Python dependencies by running
```bash
pip install -r requirements.txt
```
3. From the base folder of the project, run the following command
```
python grimoireebook.py <BUNGIE_API_KEY>
```

After execution, navigate to you home directory. There should be a _.destinyLore_ folder there. Inside you will find a file called _destinyGrimoire.epub_

## Details on what is happening

When you run the code, the following happens

1. The Destiny Grimoire is downloaded and translated (in-memory) for later use.
2. Using that information, all the image files are then downloaded into the *USER_HOME_DIRECTORY/.destinyLore* folder (it will be created if it does not exist)
3. Because the images that Bungie supplies are actually like composed tapestries, some image manipulation magic is performed to generate the individual page images.
4. All data is poured into an epub file under that same folder.