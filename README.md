# Course Catalog Server
Using MongoDB and Flask to serve up some freshly baked courses to students better than the official [Bard College Course List](http://inside.bard.edu/academic/courses/current/oldlists.html).

At the moment, the server program relies on a preexisting MongoDB database called `courselist`. I created it using the following command in the Bash terminal:

`mongoimport --db courselist --file courselist.json --jsonArray`

This project was partially inspired by [@sabo](https://github.com/sabo).

### TODO
* Scrape the [Bard College Barnes & Noble Bookstore](https://bard.bncollege.com/) for course textbooks
    * Cross-reference and match the book titles and ISBNs with the parsed course titles 
* Student account calendar visualizations and management system
    * Add search functionality for identifying courses which fit into a user's schedule
    * Add user course recommendations based on schedule availabilities
    * Google Calendar integration, maybe?

### Related Repositories:
* [Course Catalog Parser](https://github.com/segalgouldn/course-catalog-parser)
* [Course Catalog Classifier](https://github.com/segalgouldn/course-catalog-classifier)

This was intended as a [Bard College Senior Project](https://github.com/segalgouldn/Senior-Project-Subtweets/blob/master/drafts/senior_project_guidelines.pdf), but I decided to make [this](https://github.com/segalgouldn/Senior-Project-Subtweets) instead.