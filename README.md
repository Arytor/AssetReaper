# AssetReaper

Download Termux: https://play.google.com/store/apps/details?id=com.termux

Type the following commands in the command line in the exact order:

cd AssetReaper
pip install requests
pip install BeautifulSoup
pip install base58
easy_install pillow
(edited)
After installing all the "modules" download AssetReaper AND Notepad++
Place it on your desktop or whereever you want it to be.

Open AssetReaper > settings

Once in settings, there are two files: settings and accounts

Settings is where all your configuration will be. Make sure to open it with Notepad++ so your formatting doesn't mess up. It should look like this:

{
  "groupId": 0,
  "namePrefix": "",
  "price": 5,
  "description": ""
}

Change the 0 in groupId to whatever your group's id is
Name prefix is what will be put before your assets, so if you downloaded "Nike Fade Hoodie" and your prefix is "SWAG | ", when you upload, your shift will be named "SWAG | Nike Fade Hoodie"
Price is how much each asset will cost
Description is what the bot will put the asset description as. I recommend putting an ad to join your group and tons of tags.
Python.org
Python Release Python 2.7.9
The official home of the Python Programming Language

Once you have configured your settings file, open accounts with Notepad++ (so formatting doesnt break I figured that out)

All accounts must meet this requirement:
Have permission to upload in the group
BC/TBC/OBC
13+ Age (VITAL)
No PIN/2-step

If your account meets all the requirements, put the accounts in this format:

USERNAME:PASSWORD    example: builderman:roblox123

The bot can only upload 5 shirts per minute per account so the more accounts you have, the faster it uploads.

Now, we move on to the 2 main fuctions of the bot; Download and Upload.

Download is a setting where you download shirts, t-shirts, or pants. You can select a keyword it will type into the catalog to download and how many pages to download. Very straight forward and you will understand it quickly.

Upload is also very simple. It takes your settings/accounts and uploads to the group. Very simple.

IF YOU HAVE A LINUX GUIDE PLEASE DM ME THANKS <3

Thats basically how to use AssetReaper and the main fundimentals of it. Good luck botting!
Launch main.py and you will see two options:
1 Download
2 Upload

Download has many options and here is how to configure it.

The common mistake is that people will type in Download or Upload. You're supposted to type in 1 or 2

Asset Type > What type of asset you want to download. Type in 12, 13, or 14 for whatever you want to download. (Shirt recommended)

Sort-By > What selection the bot will put into the dropbox in the catalog. (Relevance recommended)

Aggregation Frequency > Time you want the bot to sort by (Past day recommended)

Next is keyword. It's what the bot will put into the catalog. Leave blank and press enter if you want to download from front page. (Blank recommended)

Start Page > What page you want the bot to start at (1 recommended)

End Page > What you want the bot to end at (1000 recommended)

Next is upload. There is no configuration and all you need to do is type in 2 and press enter and it will upload from the files folder.

I hope this clears up any confusion that you may have had!
