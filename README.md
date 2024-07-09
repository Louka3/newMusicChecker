# newMusicChecker

newMusicChecker is a program that I created to notify me if new music was uploaded on Spotify from a band or artist I am a fan of and want to keep up with their most up to date releases.
##
### Technology
I utilized python to make a quick program that uses the spotify api through spotipy.

The program parses the BandList.json file to obtain the band names that will be checked. Using these band names, I get the bands URI string in order to search for and keep a count of all of their albums and released singles. 

If the count is higher than the current album count that is inside of the json file, the count is updated with the new count and an email is sent to a specified email to inform the user that new music may have been released. 


I use a .env file that holds a lot of the constants that should be kept private from the public, such as the username and password for the email account that sends the email to notify me of the new music.
##
### To Do
- Update README with tutorials showcasing how others can use this program for themselves.
- I was playing around with the idea of changing the way band names were obtained. Maybe instead of getting the band names from a json file I could instead have a specific playlist set up inside of my playlists that will be read for all of the artists inside of that playlist. This would make updating and modifying which artists will be checked much easier than opening and editing a json file.
- Possible splash page for the project? Most likely not worth the time though.
##
### Ending Note
Thank you for checking out the program! 

For any questions, tips (I could use a lot of these) or if you just want to chat, shoot me an email (lkuczykowski@gmail.com) or add me on [LinkedIn](https://www.linkedin.com/in/louiskuczykowski/). Much appreciated!