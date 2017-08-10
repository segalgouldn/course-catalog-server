# Course Catalog Server
### A part of my Senior Project
Using MongoDB and Flask to serve up some freshly baked courses to students (in a way that is better than [inside.bard.edu](http://inside.bard.edu)).

The project will have three parts:
* Web-scraping course catalogs ✔️
* Better serving course catalogs (compared to the current site) **¯\\_(ツ)_/¯**
* Machine learning to predict future potential course catalogs

At the moment, the server program relies on a preexisting MongoDB database called `courselist`. I created it using the following command in the Bash terminal:

`mongoimport --db courselist --file courselist.json --jsonArray`

This project was partially inspired by [@sabo](https://github.com/sabo).
