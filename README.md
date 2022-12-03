# Discord.NetEmojiUpdater
A small python script to get and add new emojis into Discord.Net. Takes a URL for Emoji version from Emojipedia.org, takes the newly added emojis, searches for them on Emojiterra (to get the JSON value of the emoji), gets their value and transforms the emojis name into Discords format.

## Usage:
- Get a chromedriver for the version of chrome you're using (for example from [here](https://chromedriver.chromium.org/downloads)) and put it in the same folder as the script
- From Discord.Net/src/Discord.Net.Core/Entities/Emotes/Emoji.cs get the contents of the NamesAndUnicodes dictionary and copy it into a text file in the same folder
- Go to [Emojipedia](https://emojipedia.org/emoji-versions/) and get the links to the versions from which you want to add emojis (e.g. https://emojipedia.org/emoji-14.0/)
- Run the script
- Enter the Emojipedia version URL and wait for the script to finish getting the emojis from that version
- Repeat the last step with any other Emoji version from Emojipedia
- Type "end" to move to adding the new emojis to the old ones
- Enter the name of the file in which you saved NamesAndUnicodes
- After the script finished the updated emojis will be in the file from the previous step, copy the contents of the file back into Emoji.cs/NamesAndUnicodes
