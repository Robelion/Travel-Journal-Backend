# Travel-Journal-Backend
Cornell AppDev Hackchallenge

App Name: 
Travel Journal 

App Tagline: 
A way to keep track of your adventures and activities!

Link(s) to any other public GitHub repo(s) of your app: 
https://github.com/sophiaxu-code/traveljournal

Link to Screenshot Photos: 
https://github.com/sophiaxu-code/traveljournal/issues/1

Short Description: 
Our app's purpose is to allow a user to keep track of all of their trips. On the home screen, there's an option to add a trip, and it also shows all of their past trips. Once you click on a trip, a new screen appears with information about the trip (i.e trip dates, summary, and a timeline of all of the attractions, accomodations, etc. that they did during each trip). There's an option to add to the timeline and an option to edit the information within a trip.

A list of how your app addresses each of the requirements (iOS / Backend):

  SQLAlchemy models/Data Modelling / API:

    I used classes to create a table for User, Trip, Events, and Categories. I also have one-to-many and many-to-many relationships between these classes(tables).

  At least one GET, POST, and DELETE request route / API routes:

    There is a get all trips (GET), create a new trip (POST), delete a trip (DELETE) route funtion in app.py.

  Deploy to Google Cloud:
  
    I used docker to create images and pushed them to docker hub and then pulled them using docker pull in order to deploy it to the server so that I could integrate with iOS.

  AutoLayout using NSLayoutConstraint or SnapKit

    We used SnapKit and NSLayoutConstraint for everything we implemented from labels to buttons to collection views to table views.

  At least one UICollectionView or UITableView

    We implemented multiple collection views (trips, categories) as well as one table view (timeline).

  Some form of navigation (UINavigationController or UITabBarController) to navigate between screens
    
    We have multiple screens that users can navigate to in order to edit their trips, add to their trips, and add to their timelines.
  
  Integration with an API - this API must provide some meaningful value to your app. For example, if you’re creating a music     app, you could use the Apple Music API. Most of you will integrate with an API written by students in the backend course.
    
    We have NetworkManager set up to get and store code from the API that backend wrote. Unfortunately, Backend's implementation differed from what we had implemented, so while we have Network Manager set up with all the proper functions, it does not actually connect with Backend.

