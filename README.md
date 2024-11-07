## Welcome to my Project 5: Coffee and Honey

## Background and Business Case
I have long been a fan of coffee shops where you can enjoy decent coffee and cake, maybe a freshly made sandwich, and spend time either meeting friends, reading a book
or simply staring out of the window. I am as happy in a good chain or franchise as I am in an independent, but a good independent coffee shop
will always hold a special place in my heart. Sadly, I have seen several such independents go out of business because the margins are so fine 
and the competition is so tough. However I have also seen many independents try to expand their businesses by selling or offering extras, from function rooms in which yoga classes
or toddler groups are held, selling cups and teapots or even installing a bookstore. Some ideas have worked and some have not, but I thought this would be 
an interesting project to take on for P5: how could an independent coffee shop establish an online presence that would help it:

- make money by selling products online  
- advertise extra services such as function room booking
- allow a limited amount of table reservations 
- offer a hive-tour for anyone interested in bees and beekeeing (see below for background)
- and by doing all this, expand its business by becoming better known locally 

These are therefore the aims of my P5 project website Coffee and Honey.

## Why 'Coffee and Honey'?

One of my hobbies is beekeeping, and I briefly considered setting up a website that sells beekeeping equipment; however, I thought there are more possibilities in cafe-style business, such as bookings (tables, function room and hive-tours) than in a straight-forward e-commerce shop, so decided to merge my two ideas and interests. This has some parallels in real-life: many bakeries were I live in southern Germany sell jars of honey from local beekeepers (although these bakeries do not usually have an online presence) and I thought that would be an interesting add-on to the type of coffee shop that are familiar to me from England and Ireland.  

Merging the two ideas also gives (I think) a catchy and memorable name, that describes the website's buisness in concise and clear terms. People are generally well-disposed to either coffe or honey, often both, and 

# Overview: Website and Functionality

As will be clear, the website relies heavily on the Boutique Ado Walk-Through project, particularly for the shopping bag and checkout process. However, my imagined Coffee and Honey shop is a bit more limited in terms of the number of products it offers, and sells a different type of project with different pricing structure. Additionally, I have focused on fleshing out the My Profile section by adding an address book, and linking that to the checkout so that the customers have flexibilty in terms of delivery address; additionally, I have set the checkout up to prepopulate with saved billing / delivery addresses, and enabled a pick-up option for the customers to pickup their order directly from the cafe. 

I have hopefully provided sufficient independent development away from the Boutique Ado example.  

# MVP

## Website functionality 
The MVP allows customers to:
- browse and purchase products 
- add items to the shopping bag, and edit the shopping bag 
- create an account in which their basic details and order history are saved
- choose between home delivery, delivery to friends / family, or pick-up in the cafe
- complete an order as a 'guest', i.e. not logged in
- complete an order using their credit card hosted by Stripe (currently test data only!)
- the account also allows them to add / edit / delete addresses which are saved to their profile.

In this sense, CRUD functionality is available both in the shopping bag and in the profile.  

The MVP version of my project takes orders for the following: 
- bags of coffee beans in different sizes (250g, 500g, 750g, 1000g)
- customers can choose to pay a small surcharge to have them freshly ground before shipping 
- jars of honey in two different sizes: 340g and 500g  
The price of both product category is calculated according to the weight.  

## Admin
The admin interface can be accessed by a superuser who can do the following: 
- TO DO



## Security
All sensitive information such as the secret key is set in env.py which is added to .gitignore in Gitpod, and to the Heroku config vars for deployment. Debug is set to False.  

The front-end and back-end security is provided by the @login_required decorator along with CSRF protection implemented via the {% csrf_token %} template tag.

# Design and UX

## Design and brand image
I wanted to create a slightly warm or cosy image, and settled on the 'goldenrod' base colour as a midway point between coffee brown and the different shades of honey.

I have chosen pictures that transmitted to me a warm and slightly vintage feel which I feel would be appropriate for a typical customer, who I imagine would be between 30 and late 50s (maybe older).  

## Homepage
I designed the homepage to make the navigation basically redundant. Particularly on mobile, I wanted the customer to be able to choose their product and checkout via the shortest possible route; therefore links to the two product categories are listed at the very top of the page and allow the user to access the products directly, without going via the navigation. The navigation is of course still there and functional, but on mobile and tablet it is hopefully not necessary. 

# Site Overview
In this section, I focus on functionalties that were not present in the Boutique Ado project.  

## Products: type and pricing 
Unlike the products on Boutique Ado, the prices of both coffee and honey are linked to their weight; therefore I set up the product model to allow for products with a straight-forward price class (as on Boutique Ado) and for products like mine where the price is linked to the weight (i.e. size).

## Coffee
I offer three types of coffee: Arabia, Colombian and Robusta. Each type is offered in 4 weight variants (250g, 500g, 750g, 1000g) with the price increasing accordingly (5.99, 9.99, 14.99, 19.99)

## Extra Service
For coffee I have implemented an optional extra service called 'Freshly Ground' which allows the customers to have their coffee beans ground on the day of shipping. This is a flat-rate for all weight classes, though the price could be refined in next iterations. It is a good option for the customer who might not have a coffee grinder at home, and it helps increase the basket size for the business.

The 'extra service' option is currently only available for the coffee product cateory. However, it need not be limited to only grinding coffee beans, and could be easily rolled out to  on in the future to offer gift-wrapping, for examplem for both coffee and honey, and any other product categories which could be added to the site (coffee mugs, honey dippers, etc). 

Additionally, a future iteration could see this option remain available in the shopping bag for any customers who didn't choose it on the product detail page. 

## Honey
Like coffee, I offer three types of honey: Flower, Forest and Heather. Flower and Forest honey are offered in two price / weight classes (340g for 4.99 and 500g for 6.99). Heather honey is only offered at the 500g class for 9.99 given the more time-consuming method of extracting the honey from the honey comb.  

# My Account: Address Book
I spent a significant amount of time on the account as I wanted to make the checkout process as smooth and flexible as possible. Building on the 'my orders' section of Boutique Ado, I have added a 'my addresses' section so that customers can save the address of friends and family to whom they might send the products.

Unless the customer signifies otherwise, the default shipping address is the billing address, but the customer has the option to select another address as their default by clicking on 'Set as Default'. They can change the default shipping address either by choosing another saved address, or by clicking the 'set as default' to remove it and reset to the billing address. The customer receives on-screen acknowledgment for each change, either by a toast or by an on-screen message. Finally the default delivery prepopulates the address fields in the checkout. 

## Addresses: CRUD functionality 

## Add Address 
In this page, you can simply add an existing address; you can also click on a 'set as default' button here to make this delivery address default.  

## Edit Address
In this page, you can simply change an existing address; you can also click on a 'set as default' button here to make this delivery address default.  

## Delete Address
By clicking on delete address, you trigger a modal to check that you want to really want to delete it, in which you can either cancel the deletion or confirm it. If you delete a default delivery address, the default resorts to the billing address.  

# Checkout
Upon reaching the checkout, the customer has an overview of the products in the bag, and three shipping options: to billing, friends and family or pick-up at the cafe itsef.

An overview of the differences: 
- Billing Address: this should be the default with the billing name and address pre-populated so the customer doesn't have to repeat themselves. *Bug* At the time of writing, the checkout opens at the delivery address and the billing name does not prepopulate.  

- Shipping to Friends and Family: the billing address remains visible so that the customer can check this; additionally, credit card purchases may require this information to be transferred to be present in the purchase. Depending on whether the customer is logged in or purchasing as a guest, three things happen. 

For logged-in customers: 
1. A drop down field appears for the customer to fill in the different delivery address.
2. If the customer is logged in and has set a default shipping address that is different to their billing address, this is prepopulated.
3. A drop-down menu appears for the customer to choose from an existing saved address. If they choose one, it prepopulates all fields apart from the country field.  
4. If they want to ship to a new address, they can simply complete the fields with the new details.

For the guest purchaser: 
1. The address fields appear to be filled in, but no dropdown menu with saved addresses is shown.  

- Pick-up at the Cafe:
In this case, the billing address remains constant on-screen, but the delivery price switches to zero as there is no charge for a pick-up.   

Whatever option is chosen, the delivery address is shown on the checkout success page as appropriate.  

## Features not implemented 
- Function Room
- Bee hive tour  


# Database and Models

My database is supported by a PostgreSQL database issued by the Code Institute. Here follows an overview of the models I created, the methods I added to the models I took from Boutique Ado together with any other important changes I made to the fields in the models from Boutique Ado.

## The Products App
**Product Variant model:** This model was necessary as I wanted to offer the same product but in different weight categories, e.g. coffee beans in weight classes of 250g, 500g, 750g and 1000g, and honey in 340g and 500g. The price increases along with the weight. In this model, the product field is a FK, structuring a weight class variant to a specific product, allowing for the above weight structure, and allowing the admin to structure multiple price categories per product per weight.  

This model also allows filtering and display of product variants via the navigation bar, as well as enabling a drop-down display of the different weights / prices on the PDP without requiring a different page per weight class, which would naturally be rather clunky. 

I could not fit this into the standard Product model in a neat way, which is why I created a separate model. Additionally, this approach supports future maintenance by clearly distinguishing products with weight categories from those without, making it easier to add new products as needed.

**Services model:** This model defines optional service add-ons for products. In this MVP, I’ve included only bean grinding, but this could easily be expanded to options like gift-wrapping in the future—an attractive feature for customers and a potential revenue stream for the business.

The Service model is linked to the Product model through a Many-to-Many relationship in a field called extra_services. This setup is important because it allows certain services to be offered only for specific products (e.g., coffee bean grinding should not appear on honey product detail pages). However, other services, like gift-wrapping, could be made available across multiple product categories. This approach is straightforward and supports both scalability and reusability as the product portfolio grows.
 
## The Profile App
**Recipient Address model:** I added a RecipientAddresses model to my profiles app to enable an 'Address Book' type feature for my customers. It is linked to the UserProfile, which serves as the FK for this model, linking any details stored in the model to the relevant user, and only to that user. The Django framework sets an id to each address, which serves as the PK within the model itself.  

I wanted to make the checkout process as smooth as possible; Amazon's checkout inspired this section, as the Address Book feature is excellent. I also wanted to avoid the customers having to re-type in addresses they have already used on the site in order to encourage repeat business from returning customers.  

The model itself is quite straightforward in the sense that it is simply the recipient address details, together with an optional nickname to save the address under, and the option to set it as the default shipping address. This I thought would be a nice option for people ordering for family or even for businesses.   

## Checkout: Order model and Delivery Options method

## Products: Product model add-ons
Extra services 

## Products: Product Variant model

## Products: Service model

## User Profile: Recipient Addresses model



# Planning and Agile Methodologies

I followed the Agile methodlogoy as outlined in the "I think therefore I blog" according to the MoSCow proiritization. Following feedback on my Project 4, I also tried to make use of epics and milestones in my workflow.  

Here is the link to my project board.  

## Commit messages
Following feedback on my 4th project on 1st October, I started writing my commit messages according to the conventions listed here: https://www.conventionalcommits.org/en/v1.0.0/#summary
Therefore there is a change in the style of the commit messages from that date. However, I think it is worth making the change in order to improve as a developer.




