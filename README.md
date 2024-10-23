# Welcome to my project 5: Coffee and Honey

# Background and Business Case
I have long been a fan of coffee shops where you can enjoy decent coffee and cake, maybe a freshly made sandwich, and spend time either meeting friends, reading a book
or simply staring out of the window. I am as happy in a good chain or franchise as I am in an independent, but a good independent coffee shop
will always hold a special place in my heart. Sadly, I have seen several such independents go out of business because the margins are so fine 
and the competition is so tough. However I have also seen many independents try to expand their businesses by selling or offering extras, from function rooms in which yoga classes
or toddler groups are held, selling cups and teapots or even installing a bookstore. Some ideas have worked and some have not, but I thought this would be 
an interesting project to take on for P5: how could an independent coffee shop establish an online presence that would help it:

- make money by selling products online  
- offering extra services such as function room booking
- allow a limited amount of table reservations 
- offer a hive-tour for anyone interested in bees and beekeeing (see below for background)
- and by doing all this, expand its business by becoming better known locally 

These are therefore the aims of my P5 project website Coffee and Honey.

# Project Overview: Coffee and Honey

As will be clear, the website relies heavily on the Boutique Ado Walk-Through project, particularly for the shopping bag and checkout process. However, as my imagined Coffee and Honey shop is a bit more limited in terms of the number of products it offers, and sells a different type of project with different pricing structure. Additionally, I have expanded the MyAccount page with more delivery and pick-up options, and an expanded account section with CRUD functionality for saved delivery addresses. I have hopefully provided sufficient independent development away from the Boutique Ado example.  

As with Project 4, it is built on mobile-first principles around a Django framework and supported by a PostgreSQL database from the Code Institute; I generated the secret key using this tool: https://randomkeygen.com/

## Why 'Coffee and Honey'?

One of my hobbies is beekeeping, and I briefly considered setting up a website that sells beekeeping equipment; however, I thought there are more possibilities in cafe-style business, such as bookings (tables, function room and hive-tours) than in a straight-forward e-commerce shop, so decided to merge my two ideas and interests. This has some parallels in real-life: many bakeries where I live in southern Germany sell jars of honey from local beekeepers (although these bakeries do not usually have an online presence) and I thought that would be an interesting add-on to the type of coffee shop that are familiar to me from England and Ireland.  

Merging the two ideas also gives (I think) a catchy and memorable name, that describes the website's buisness in concise and clear terms. People are generally well-disposed to either coffe or honey, often both, and 


# MVP

## Website functionality 
The MVP allows customers to:
- browse and purchase products 
- add items to the shopping bag, and edit the shopping bag 
- create an account in which their basic details and order history are saved
- choose between home delivery, delivery to friends / family, or pick-up in the cafe
- complete an order using their credit card hosted by Stripe (currently test data only!)
- the account also allows them to add / edit / delete addresses which are saved to their profile.

In this sense, CRUD functionality is available both in the shopping bag and in the profile.  

The MVP version of my project takes orders for the following: 
- bags of coffee beans in different sizes (250g, 500g, 750g, 1000g)
- customers can choose to pay a small surcharge to have them freshly ground before shipping 
- bags of pre-ground coffee 
- jars of honey in two different sizes: 340g and 500g  
The price of both products is calculated according to the weight.  

## Admin
The admin interface can be accessed by a superuser who can do the following: 
- TO DO



## Security
All sensitive information such as the secret key is set in env.py which is added to .gitignore in Gitpod, and to the Heroku config vars for deployment. Debug is set to False.  

The front-end and back-end security is provided by the @login_required decorator along with CSRF protection implemented via the {% csrf_token %} template tag.

# UX

# Agile

# Version Control

## A note on commit messages
Following feedback on my 4th project on 1st October, I started writing them according to the conventions listed here: https://www.conventionalcommits.org/en/v1.0.0/#summary
Therefore there is a change in the style of the commit messages from that date. However, I think it is worth making the change in order to improve as a developer.



