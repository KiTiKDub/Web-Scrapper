# README

## Distinctiveness and Complexity

This project allows for the merging of three projects(2, 3, and 4) while allowing it to be it's own distinctive application by bringing the added complexity of the web scraper. The web scraper interacts with websites outside of our own internal server, which is something we have never done before. It also brings about complexity in learning how a new library works, formatting it, and bringing it into a different framework, as well as allowing that to be manipulated by Javascript and CSS. I personally chose to use minimal CSS, as I want this to be quick to read and ready to move nto the next things, similar to how newsletters to your inbox may function

## Layout

The layout file contains a simple navigation bar, as well as the block body to be updated in other pages. This nav contains a section of the user that is logged in, with the ability to log out next to it. The main area is the home, with the scape log, and liked articles next to it. This will be discussed later

## Index

The main index contains the ability to collect and display articles. If the user has no searches, they are met with a drop down, a text area, and a search button. The drop down contains three websites to scrape. (Why those websites were chosen will be discussed in the `Challenges` section.) Once that has been selected, the user may type anything into the text box. This will send a request to that website with the search query of whatever the user typed in. If the user does not select a website, a message will be displayed, prompting the user to select a website.

Once the user has submitted their query, the web scraper will begin to scrape the queries, displaying a headline, the first paragraph of the article, a like & dislike button, as well as a link to the full article on the website. The scrape also stores the category of the article to be used on the `Liked Articles` section of the website. Liking the article will turn the thumbs up blue, and store that information in the db. Disliking the article will turn the thumbs red, and store that information in the the db. The user is unable to like and dislike an article. It will remove the coloring of the the opposite thumb, and delete the entry in the database.

## Scrape Log

When the user clicks on the scrape Log, they will be met with a table of any searches they made. It will include the website, the search query, and the date at which they searched. Clicking any line will call the fetch API in the js file to pull that entry. The user can like and dislike just as they can on the home page. This API will first grab the query name and convert into a Query object. This Query object can then be used to filter the Article objects, which are then returned to the page. The HTML layout is created with javascript, and the created class names allow the CSS to automatically format it to match in a similar way to the home page.

## Like Page

This page shows the user all articles that they have liked. This displays the same format as index, but with a few tweaks. The first tweak is there is no search bar, just a list of the users most liked and disliked categories. This caps out at 5 for both. The other change is there no like button, as the user has already liked the article. There is currently no 'unlike' feature. The user can remove the article from their likes by disliking it and refreshing the page.

## script.js

The script serves two main functions. To allow for the like and dislike button to work, and for the scrape log to update on click. The script will create an array by use of going through each 'interaction' class. On each interaction class, to event listeners are created for each thumb. On click, like will turn the thumb blue, and add it to the database, and remove the red from the dislike button, if it was disliked. The same goes for the dislike button. Since I couldn't get the page to remember the likes (more on that in `Challenges`) I had my API return JSON responses if an entry already existed. That message would replace the thumb to inform the user that they had already done that action. The other event created an event listener on the DOM object, searching for 'TD' element, this allowed any of the values in the row to be clicked to return that value. Once the objects were rendered, the click could also search for a 'div', that would allow the user to return to the search log and load a different set of articles. One small update I added at the end was to provide an alert for the user to select a valid website. That is the first line of the file.

## Challenges

This will also go over talking about views.py. The first challenge that came about was integrating the web scraper. I had to first learn how to use Beautiful Soup, and grab the appropriate items I wanted from the website. Thankfully with the inspect tool, it wasn't too difficult to find the right class or id. The first issue this brought me though is that even if the class was found on inspect, it may not be in the page source. Through trial and error, I found all the right identifiers to grab the correct attributes. The reason that I chose the three sites that I did was because 1) I didn't want to make my code a mile long, and 2) some of the websites I intended on using had pay walls, and would not render the html. Once I got my paths sorted, that finished up the index view. The log view and history API went relatively smoothly, once I jogged my memory on using the fetch API. The biggest challenger was finding the best click event to trigger the change. The likes proved to be most difficult. Between writing the API and the javascript to update it, it took much trial and error to succeed. Even with that, I couldn't get exactly what I wanted. I was unable to retrieve the like information and print the thumb blue, so I settled for a check in the JS. One last small hurdle I faced was getting the dictionary of the likes and dislikes to render properly. After much documentation searching I managed to get the right display to the site.
