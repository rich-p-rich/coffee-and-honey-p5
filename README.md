## Welcome to my Project 5: Coffee and Honey

![responsive](readme_images/responsive.PNG)


**Link to deployed site:**  https://coffee-and-honey-p5-fc5ef8bcd788.herokuapp.com/ 


## A Note on Testing
I have separated the results of my site testing into a different file called Test Results that covers lighthouse testing, code validators and a detailed overview of the site's functionality here: [Test Results](test-results.md).

## Why 'Coffee and Honey', and what is it?

One of my hobbies is beekeeping, and I briefly considered setting up a website that sells beekeeping equipment; however, I thought there are more possibilities in cafe-style business, such as bookings (tables, function room and hive-tours) than in a straight-forward e-commerce shop, so decided to merge my two ideas and interests. This has some parallels in real-life: many bakeries where I live in southern Germany sell jars of honey from local beekeepers (although these bakeries do not usually have an online presence) and I thought that would be an interesting add-on to the type of coffee shops that are familiar to me from England and Ireland.  

Merging the two ideas also gives a catchy and memorable name that describes the website's buisness in concise and clear terms. 

A further note on my background: I worked in e-commerce from 2011 - 2019, primarily in operations and logistics. However, as my first job in e-commerce was at a start-up company, and IT was central everywhere I worked, I developed a long-standing interest in the subject. This is why I chose the e-commerce option for my P5.  

## Background and goals
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

These are therefore the aims of my P5 project website and fictional company Coffee and Honey.

## Business Case
Coffee and Honey is imagined as a local indpendent coffee shop. It is a B2C business focusing primarily on adults aged 30 and up. It opens 8:00 - 17:00 Monday - Friday, 09:00 - 15:00 on Saturdays, and10:00 - 15:00 on Sundays. During the week, local people, office workers, parents and retired people are the likely clientele, whereas Saturdays and Sundays might well have a younger audience of people who want to meet friends or revive themselves with a leisurely coffee after a busy night out / long week.  

Social media would certainly be necessary and I envisage both Facebook and Instagram being popular:
- Facebook as a business page with business details (opening hours, reviews, interactions etc)
- Instagram because the subjects are photogenic and interesting. People who enjoy coffee often enjoy photos of coffee and coffee-related items, from the raw beans to the foam on a cappucinno. Honey and beekeeping is also photogenic and it would be fairly straightforward to post interesting photos and videos on a regular basis to generate interest and appeal to the customers. In this sense, Instagram would be a channel for pursing a content marketing strategy: regular and visually appealing posts about these topics would be designed to keep the audience engaged, attract new followers, and help generate a brand image or identity.
- The type of content would be a mix of information (basic business information) but primarily enterainment, with enjoyable and interesting photos of Coffee and Honey's primary products: coffee and honey, plus cake as a natural and fun extra offering in the cafe.

As it is a small independent business, I removed the 'free shipping' threshold. I imagine the basket size would not be much more than 30 - 40€, and probably more likely around the 20€ mark; free shipping would be a cost that business could probably not afford, and I'm doubtful that it would work as an incentive for customers to buy either more coffee or more honey. Instead, I have offered the customers the chance to pick up their order for free in the cafe as an alternative to having it shipped by post.  

As the website in this case would start off being more supplementary to the company rather than the main source of revenue, there would be little marketing budget to spend on online advertising. Given the subject matter, however, clever use of social media and SEO would be a cost-effective and overall effective way of raising the coffee shop's profile amongst local people, and triggering some word-of-mouth marketing.  

Since gift-wrapping would be a nice add-on in a future iteration of this project, an occasional newsletter with gift ideas at Christmas, or a monthly newsletter letting people know about the beekeeping year and suggesting birthday gift ideas, would be a realistic option. 

I got further into the marketing requirements of this project in the "Marketing: Facebook, MailChimp and SEO" section below.  

## Key Technology
- Django Web Framework
- Python
- Bootstrap front-end framework, with Bootstrap CSS and JS
- HTML
- CSS
- Javascript
- PostgreSQL supported by the CodeInstitute (https://dbs.ci-dbs.net/)
- Stripe for payment processing
- Amazon Webservices for hosting product images and static files
- Heroku for hosting the deployed version of my site 


# Overview: Website and Functionality

As will be clear, the website relies heavily on the Boutique Ado Walk-Through project, particularly for the shopping bag and checkout process. However, my imagined Coffee and Honey cafe is a bit more limited in terms of the number of products it offers, and sells a different type of project with different pricing structure. Additionally, I have focused on fleshing out the My Profile section by adding an address book, and linking that to the checkout so that the customers have flexibilty in terms of delivery address; additionally, I have set the checkout up to prepopulate with saved billing / delivery addresses, and enabled a pick-up option for the customers to pickup their order directly from the cafe. 

I have hopefully provided sufficient independent development away from the Boutique Ado example.  

# MVP

## Website functionality 
The MVP allows customers to:
- browse and purchase products 
- add items to the shopping bag, and edit the shopping bag 
- create an account in which their basic details and order history are saved
- choose between home delivery, delivery to friends / family, or pick-up in the cafe
- checkout as a 'guest', i.e. not logged in
- or checkout as an authenticated user
- complete an order using their credit card hosted by Stripe (currently test data only!)
- reach an order success page after the purchase
- the account also allows them to add / edit / delete addresses which are saved to their profile.

In this sense, CRUD functionality is available both in the shopping bag and in the profile.  

The MVP version of my project takes orders for the following: 
- bags of coffee beans in different sizes (250g, 500g, 750g, 1000g)
- customers can choose to pay a small surcharge to have them freshly ground before shipping 
- jars of honey in two different sizes: 340g and 500g  
The price of both product category is calculated according to the weight.  

## What is live for the MVP and what not
The homepage has several section:
- The links to the coffee and honey products are live
- The links to the visit us, function room, about us and bee hive tour are not live 

## Admin
The admin interface can be accessed by a superuser who can do the following: 
- Add categories
- Add products to the categories
- Upload product images, add descriptive text, provide product details and set the price 
- Set extra services (such as coffee bean grinding or gitf wrapping)
- View user information (username, email address, etc)
- Set different permission levels: staff and superuser  

## Security
All sensitive information such as the secret key is set in env.py which is added to .gitignore in Gitpod, and to the Heroku config vars for deployment. Debug is set to False.  

The front-end and back-end security is provided by the @login_required decorator along with CSRF protection implemented via the {% csrf_token %} template tag.

# Design and UX

A PDF of my wireframes is available in the readme_documentation folder: the file is called wireframes_coffee-and-honey.pdf

## Design and brand image
I wanted to create a slightly warm or cosy image, and settled on the 'goldenrod' base colour as a midway point between coffee brown and the different shades of honey.


![base-colour](readme_images/goldenrod.PNG)

![base-colour-details](readme_images/goldenrod_details.PNG)

I have chosen pictures that transmitted to me a warm and slightly vintage feel which I feel would be appropriate for a typical customer, who I imagine would be between 30 and late 50s (maybe older).

## Images on the website
As I struggled to find product images for the coffee and honey, I used OpenAI's Dall-E image creation functionality to generate product images of coffee and honey appropriate to my website. All other images are from Pexels and have been acknowledged with comments in the code.  

In case I have overseen any in the code, the Pexels images I used are:

pexels-daniel-reche-718241-1556665 : for favicon
pexels-shottrotter-1309778 : for order coffee image on homepage
amelia-bartlett-9HajXdvKpIk-unsplash : for honey image on homepage
pexels-apgpotr-683039 : fir visit us on hompage
pexels-thngocbich-2362392 : for function room on hompage
pexels-chris-clark-1933184-12062925 : for 404 page

## Homepage
I designed the homepage to make the navigation redundant for customers who know what they want, and who want to checkout as quickly as possible. Particularly on mobile, I wanted the customer to be able to choose their product and checkout via the shortest possible route; therefore the two main product categories are listed at the very top of the page and allow the user to access the products directly, without going via the navigation. The navigation is of course still there and functional, but on mobile and tablet it is hopefully not necessary. 

![wireframe](readme_images/homepage-vs-navbar.PNG)


![mobile-home-links](readme_images/homepage_mobile.PNG)


![tablet-home-links](readme_images/homepage_tablet.PNG)


## Checkout
I made a few changes to the Boutique Ado format in order to streamline the checkout process for the customer:

Firstly: users who are logged in and have a billing address will have the billing address prepopulated for them. As this is assumed to be the default shipping address, unless otherwise stated by the customer, this saves the customer time and avoids the repetitive entry of data which the shop already has stored. This is a good way to optimise the conversion rate.  

I took inspiration from two large corporations for two other features on the checkout page:

- Address book: I find Amazon's address book incredibly useful, especially as I live abroad away from my family and many of my friends. I decided to integrate a similar functionality to my website project so that customers can ship the products as gifts, and save the address information for future purchases.

- Pick up option: Lego's German site has the option to have your delivery shipped to a pick-up shop; as Coffee and Honey is imagined to be a local cafe, I thought this would be a realistic and useful feature to implement in the checkout. It also saves the customer money on shipping costs, which they might well spend in the cafe on food and drink.

Lego Germany -> add item to cart, proceed to checkout (English language version): https://www.lego.com/en-de/

![lego-pickup](readme_images/lego-checkout.PNG)


# Site Overview
In this section, I focus on other functionalties that were not present in the Boutique Ado project.  

## Products: type and pricing 
Unlike the products on Boutique Ado, the prices of both coffee and honey are linked to their weight; therefore I set up the product model to allow for products with a straight-forward price class (as on Boutique Ado) and for products like mine where the price is linked to the weight (i.e. size).

Originally, I planned to offer both pre-ground coffee and as well as beans, which is why I have kept the navbar link to first the category and then the product detail page. Similarly with honey, I planned to offer both creamed set honey in addition to the more common liquid honey. Due to lack of time I could not do this, but thought it worth keeping the category alive for this MVP project and building on that in a later itertion.  

## Coffee
I offer three types of coffee: Arabia, Colombian and Robusta. Each type is offered in 4 weight variants (250g, 500g, 750g, 1000g) with the price increasing accordingly (5.99, 9.99, 14.99, 19.99)

## Extra Service
For coffee I have implemented an optional extra service called 'Freshly Ground' which allows the customers to have their coffee beans ground on the day of shipping. This is a flat-rate for all weight classes, though the price could be refined in next iterations. It is a good option for the customer who might not have a coffee grinder at home, and it helps increase the basket size for the business.

The 'extra service' option is currently only available for the coffee product cateory. However, it need not be limited to only grinding coffee beans, and could be easily rolled out to  on in the future to offer gift-wrapping, for example for people sending either both coffee or honey (or both!) to friends or family. 

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

 ![address-book](readme_images/address.book.PNG)


![delete-address-modal](readme_images/delete-address-modal.PNG)

## Welcome Message and Toasts
I liked the feature introduced to us in Project 4 whereby the user is welcomed with their username if logged in, or prompted to log in, at the top right of the screen, if they are not. I therefore added it to this project as well as a reminder to the customer where they are in the process.  

I also implemented the Toast functionality from the Boutique Ado with some minor changes, such as changing the 'Go to Checkout' at the PDP to 'Go to Bag' to more accurately reflect the process (this could also have been my misunderstanding of the walk-through project, however. )

## Bag
In the Bag, the customer can change the quantity of the products or empty the bag altogether. I have tried to line up the overview a bit more precisely by using a table.

The customer can proceed to the checkout from the bag as a guest user, but I added a modal to the 'proceed to checkout' button to prompt them to log in, or confirm the checkout as guest, if that's what they want.

![guest-modal](readme_images/guest-modal.PNG)

Finally, there was some horizontal scroll in the mobile version of the Boutique Ado Bag - this was probably due to my faulty implementation of it! I worked on eliminating it by changing button sizes and responsiveness, but at a width of 320px there is still some minor horizontal scroll that I could not quite eliminate for this MVP.

## Checkout
Upon reaching the checkout, the customer has an overview of the products in the bag, and three shipping options: to billing, friends and family or pick-up at the cafe itsef.

![shipping-options](readme_images/checkout-top-shipping-options.PNG)   

An overview of the differences: 
- Billing Address: this should be the default with the billing name and address pre-populated so the customer doesn't have to repeat themselves. *Bug* At the time of writing, the checkout opens at the delivery address and the billing name does not prepopulate.  

- Shipping to Friends and Family: the billing address remains visible so that the customer can check this; additionally, credit card purchases may require this information to be transferred to be present in the purchase. Depending on whether the customer is logged in or purchasing as a guest, three things happen. 

For logged-in customers: 
1. Delivery address fields appear for the customer to fill in the different delivery address.

![different-address](readme_images/delivery-different-address.PNG)  

2. If the customer is logged in and has set a default shipping address that is different to their billing address, this is prepopulated as can be seen in the above screenshot.

3. A drop-down menu appears for the customer to choose from an existing saved address. If they choose one, it prepopulates all fields apart from the country field.  

![address-dropdown](readme_images/delivery-dropdown.PNG)  

4. If they want to ship to a new address, they can simply complete the fields with the new details.

For the guest customer: 
1. The address fields appear for them to complete, but no dropdown menu with saved addresses is shown.  

- Pick-up at the Cafe:
In this case, the billing address remains constant on-screen, but the delivery price switches to zero as there is no charge for a pick-up.  

Whatever option is chosen, the delivery address is shown on the checkout success page as appropriate.  

![pick-up-confirmed](readme_images/pick-up-confirmation.PNG)  

## Features not implemented

- **Emails and Social Media Account Log-in**: although this was a key aim, I ran out of time to implement the automated email feature and social media account log-in. I will however add my superuser details to the submission, as well as the log-in of an existing regular user, in case the assessors need to verify an account / email for test purchases.

- **Function Room:**
The function room would be the next feature to implement on this website. It would would be set up like the appointments function in my P4, with fields to capture basic details
like name, address, time, number of people and type of catering. This would not go through the checkout as payment would be conducted by invoice and bank transfer, and the cafe business would want to speak to the booker before confirming all details. Here is a screenshot from the Wireframe I sketched out: 

![function-room](readme_images/function-room.PNG)  

- **Table reservation:** 
I wanted to include an option to offer a certain number of tables in the cafe as reservable and thought I could base this on the appointments booking from my P4. It would need date validation, number of people (max 4) and time of arrival. Here is a sketch from my wireframes: 

![table-reserve](readme_images/table-reservation.PNG)  

- **Bee hive tour:**  
This would have been a limited offer available only 1 day per week, either Saturday or Sunday, from April through to September; there would have been only 1 - 2 slots available on the day, each 10:00 - 11:00, and 11:30 - 12:30; each slot would be limited to 10 participants with a standard price for adults, and discounts for kids and pensioniers. Since this would have involved a charge, it would have needed to go through the checkout. I did not flesh out a wireframe for this, but I will add it when I come to revise this project in the future. I view this as more of a marketing move to generate interest among the local community rather than a source of revenue, but it would be  a nice addition for a local independent business.

# Database and Models

My database is supported by a PostgreSQL database issued by the Code Institute. Here follows an overview of the models I created, the methods I added to the models I took from Boutique Ado together with any other important changes I made to the fields in the models from Boutique Ado.

## The Products App

The base products model (based on Boutique Ado): for orientation with the two new models below:

![product-model](readme_images/models_Products.PNG)  

**Product Variant model:** 

![product-variant-model](readme_images/models_product-Variant.PNG)  

This model was necessary as I wanted to offer variations of the same product based on different weight categories, e.g. coffee beans in weight classes of 250g, 500g, 750g and 1000g, and honey in 340g and 500g. In this model, the product field is a FK, structuring a weight class variant to a specific product, allowing for the above weight structure, and allowing the admin to structure multiple price categories per product per weight.  

This approach enables a drop-down display of the different weights / prices on the PDP without requiring a different page per weight class, which would naturally be rather clunky. In a future iteration it should also be possible to filter relevant products by weight class via a search field or the navigation bar.

I could not fit this into the standard Product model in a neat way, which is why I created a separate model. Additionally, this approach supports future maintenance by clearly distinguishing products with weight categories from those without, making it easier to add new products.

**Services model:** 

![product-services-model](readme_images/models_product-service.PNG)  

This model defines optional service add-ons for products. In this MVP, I’ve included only bean grinding, but this could easily be expanded to options like gift-wrapping in the future—an attractive feature for customers and a potential revenue stream for the business.

The Service model is linked to the Product model through a Many-to-Many relationship in a field called extra_services. This setup is important because it allows certain services to be offered only for specific products (e.g., coffee bean grinding should not appear on honey product detail pages). However, other services, like gift-wrapping, could be made available across multiple product categories. This approach is straightforward and supports both scalability and reusability as the product portfolio grows.

# Product Management
For this MVP, I thought it was enough to manage the creation, editing and deletion of products and services via the admin section using superuser access. I will add these credentials to my submission for the assessors.  

## The Profile App
**Recipient Address model:** 

![recipients-model](readme_images/model_recipients.PNG) 

I added a RecipientAddresses model to my profiles app to enable an 'Address Book' type feature for my customers. It is linked to the UserProfile, which serves as the FK for this model, linking any details stored in the model to the relevant user, and only to that user. The Django framework sets an id to each address, which serves as the PK within the model itself.  

I wanted to make the checkout process as smooth as possible; Amazon's checkout inspired this section, as the Address Book feature is excellent. I also wanted to avoid the customers having to re-type in addresses they have already used on the site in order to encourage repeat business from returning customers.  

The model itself is quite straightforward in the sense that it is simply the recipient address details, together with an optional nickname to save the address under, and the option to set it as the default shipping address. This I thought would be a nice option for people ordering for family or even for businesses.   

## Checkout: Order model and Delivery Options method
**Order Model**: 

![order-model](readme_images/models_checkout-Order.PNG)

I have expanded the Order model and added several methods to make the checkout process as seamless as possible for customers. 

To start with: in order to differentiate between billing and delivery addresses, I have prefixed each address-related field with "billing_". This  helps clearly distinguish the default billing address from a separate delivery address, in cases where they differ. 

Additionally, I added a number of new fields to manage delivery and pick-up options:

- different_delivery_address (models.BooleanField(default=False)): This field allows the database to capture a different delivery address if specified by the customer. By default, this field is set to False, meaning that the billing address is used as the delivery address unless the customer specifies otherwise. When the customer chooses to have their order delivered to a different address, this field is set to True, and opens the way to capturing the customer's delivery address details in the fields prefixed with 'delivery_' listed further down the model. This provides flexibility for cases where the order needs to be shipped to a different location.

- pick_up (models.BooleanField(default=False)): This field enables a pick-up option, allowing customers to collect their orders 'in-store' at the cafe instead of having them delivered. When pick_up is selected, delivery costs are set to zero, and the system bypasses the delivery address fields, making the checkout experience simpler and more efficient for local customers. Given that "Coffee and Honey" is a local independent cafe, this feature offers a realistic and user-friendly option, catering to customers who prefer pick-up to avoid shipping costs.

**Delivery Options method:** This method (delivery_options) provides flexibility in the checkout process by catering to different delivery and pick-up scenarios:

![order-delivery-model-1](readme_images/models_checkout-Order_del-options.PNG)

![order-delivery-model-2](readme_images/models_checkout-Order_del-options-2.PNG)

- self.pick_up: This flag handles the scenario described above where the customer wants to pick up their order at the cafe. When selected, the delivery cost is set to zero, and only the billing address fields are shown.  

- self.different_delivery_address: This flag opens up three options for delivery:
i. Saved Address: If the customer has saved delivery addresses in their profile, they can select one from a drop-down menu in the checkout.
ii. New or Unsaved Address: If the customer doesn’t have any saved addresses, is checking out as a guest, or if they wish to ship to a new address, they can enter a new delivery address here.
iii. The else condition - Default Billing Address: In the absence of any specific delivery address, the else condition pre-fills the delivery fields with the billing address by default.

For instances where the address fields are to be populated with saved data, this method makes a call to the 'copy_address' helper method (see below).

This method is designed to react to the customer’s chosen options, whether they’re using saved addresses, entering a new address, or opting for in-store pick-up. This flexibility should in theory help optimise the conversion rate from baskets into actual sales.  


**Copy Address method**: 

![copy-address-model](readme_images/models_helper_copy.PNG)


This (copy_address) is a helper method designed to populate the delivery address fields (or billing fields if adapted) with address information that the customer has saved to their profile. It supports the logic in the delivery_options method by allowing saved delivery or billing address details to be copied directly into the delivery address fields without manually setting each one individually.


## Remaining bugs and issues
There are several things which I have not been able to fix before submission, despite the help of the tutoring service, my mentor and many of my own independent attempts. 
Key among them are: 

- The checkout opens with the default shipping address as 'Delivery to friends and family' when I want it to open at 'Ship to billing address' as default. 
- I cannot get the billing name to prepopulate in the relevant field.
- The 'save to profile' link does not work for delivery addresses in the checkout. By clicking the checkbox at the end of the delivery fields, the customer should be able to save this address information to their 'saved addresses' page, but this currently does not work.  
- When the customer chooses 'pickup from cafe' as their preferred shipping option, my code is still transmitting the shipping price of €4.99 to Stripe and charging them for it, even though everything is correct on the frontend. I cannot get to the bottom of this.
- Finally, when 'pick up' is chose, the checkout success page still itemises the delivery cost as €4.99, even though I have set it as €0.00.

Unfornately, I have had to cut my losses with these bugs as I do not have time to fix them for this MVP before submission.

## Marketing: Facebook, MailChimp and SEO

**Facebook:** I set up a functioning Facebook business page and have fully documented it in this document. It is also linked from my footer although, as is known, it may get taken down by Facebook as it is not a genuine company. Given that it will probably get taken down, I have added a nofollow link to it. If this were a real business, however, I would not link it via nofollow, as I would want the Facebook page to be fully linked to my website.

Link to page: https://www.facebook.com/profile.php?id=61567575580447

A PDF of the mock-ups for my Facebook site can be found in the readme_documentation folder: the file is called coffee-and-honey_facebook.pdf


![facebook](readme_images/facebook-page.PNG)


**MailChimp and Newsletter sign-up:** I have set up a MailChimp account and embedded the newsletter sign-up in the footer of my project. The following screenshots demonstrate its functionality.


![mailchimp-1](readme_images/mailchimp-footer-1.PNG)


![mailchimp-2](readme_images/mailchimp-footer-2.PNG)


![mailchimp-2](readme_images/mailchimp-admin-1.PNG)


![mailchimp-2](readme_images/mailchimp-admin-2.PNG)

**404 Page:** I have set up and tested a custom 404 page that directs the user back to the homepage. As per the relevant part of the project walk-through, I added the the handler to views.py in the Coffee and Honey app, and imported it to the main urls file.

The html is stored in my main templates folde and is called 404.html, as shown in the guidance. I have added a photo of some swarming bees and some custom text, plus a button to guide the user back to the homepage.

**SEO:**
- No-follow links: the footer contains links to the company's Facebook page (see above), Instagram homepage, Fairtrade Coffee and MailChimp, all of which include the rel="nofollow" attribute. 
- There are no orphan pages: all pages can be reached from another findable page either through the navigation menu, footer or in-page links.
- Block meta in base.html contains the meta title, keywords and description.
- All images are named in a way that that search engines can identify them as site-relevant

![meta](readme_images/meta-info.PNG)


- A sitemap is available in the root directory.
- A robots.txt file is available in the root directory.
- There is no lorem ipsum text at all.  


# Planning and Agile Methodologies

I followed the Agile methodlogoy as outlined in the "I think therefore I blog" according to the MoSCow proiritization. Following feedback on my Project 4, I also tried to make use of epics and milestones in my workflow.  

## Commit messages
Also following feedback on my 4th project on 1st October, I started writing my commit messages according to the conventions listed here: https://www.conventionalcommits.org/en/v1.0.0/#summary
Therefore there is a change in the style of the commit messages from that date.

## User Stories, Epics and Milestones
Here is the link to my Kanban board: https://github.com/users/rich-p-rich/projects/7

At the time of writing, I have completed 47 user stories which I divided up into 10 epics and 8 milestones. Here are the epics; I completed the MVP for each of them apart from Epic 10 'The Function Room', for which I ran out of time.

![epics](readme_images/kanban_epics.PNG)


I also followed the MoSCow prorisation principle for organising my work, as I did with Project 4. One difference between Project 4 and 5 that I cut my stories up into smaller slices which I think helped keep a better overview; additionally, it provided a welcome feeling of momentum and I feel that the Kanban board was well integrated into my project this time around as it served as my primary planning tool throughout the project.  

Similarly, I used Milestones to keep track of the bigger picture throughout my project. I set them up as follows:
- Milestone 1: basic website layout, navigation, user registration, basic bag functionality 
- Milestone 2: edit bag, Toasts, proceed to checkout, Stripe implementation with Webhook handlers 
- Milestone 3: profile app fleshed out with view account details, order history, save addresses, CRUD functionality for saved addresses 
- Milestone 4: checkout aoo fleshed out with address fields pre-population from saved addresses, fix delivery prices, default shipping 
- Milestone 5: Heroku connection, deployment in stages, deployment testing 
- Milestone 6: marketing including sitemap and robots.txt, Facebook page, newsletter signup, meta keyword optimisation, no-follow links and 404 page
- Milestone 7: code validation (e.g. PEP8) and ighthouse testing
- Milestone 8: site testing, documentation of results, complete ReadMe

This helped me break down the tasks into what felt were realistic and unified goals; like the rest of the Kanban board, it felt a genuine part of my project planning and I made regular updates to it.  

# Resubmission 
As mentioned above, I failed my first attempt at this project based on criteria 1.7 and 4.1; it was not possible to test 4.3, 4.4 and 4.6 given the problems with 4.1. Here is an overview of my fixes:
- 1.7. Problem: broken 'Bookings' link in the navbar. 
    - Solution: I have removed that link altogether. I originally included it to show the scope of the site, but clicking on it just refreshed the page. As the 'Bookings' page is not ready, I have removed the link. 

- 4.1. Problem: new users cannot register
    - Solution: I have implemented a verification by email functionality by linking a gmail account set up for this purpose. 
    - When the user registers, he or she will receive a verification email sent to their email address. 
    - By clicking on this link, the user is taken to a 'confirmation page'; the user is invited to click 'confirm', at which point the email address is verified. 
    - The account is now validated, and the new user can log in as required.

- 4.3. Could not be assessed: prevent non-admin users from acessing the data store.
    - Solution: admin level credentials are required to access the admin section, which is where I implemented the product management.
    - The default role given to anyone signing up is customer; when the customer has verified their account and signs in, he or she can access ony their own data.
    - Testing: it is only possible to access admin with super-user credentials. It is not possible to access admin with, for example, customer credentials. 

- 4.4. Could not be assessed: apply role-based login and registration functionality
    - Solution: users are assigned the 'customer' role during registration, as per the built-in Django system. 
    - It is only possible to access the admin with super-user access 
    - Super-users can access the admin account, where they can add, delete or modify products, product variants and prices, as well as user details

- 4.6. Could not be assessed: use role-based log to determine whether users are allowed to access restricted content
    - Solution: access to profile details and order history are only available to registered users who are verified and logged-in; access to admin is available only to users with super-user credentials. 
    - Users who are not logged in, or who purchase as a guest user, cannot access any account details, including order history and address book. 
    - Customers who are logged in can access only their own order history and address book  
    - Any user logging in with a customer account cannot access the admin section at all; super-user credentials are required for this 

## Resubmission: backlog
I added a separate column to the backlog for this resubmission to clarify exactly what I changed in order to fulfil the missing criteria. This column is called 'Done: resubmission.' The functionality for 4.3, 4.4 and 4.6 was already present, but as I did not fulfil 4.1 properly in my original submission, it could not be seen. 

# Deployment

Here follows an overview of the steps I took to deploy the project.

## GitHub and GitPod
- Find and use the CodeInstitute's 'Gitpod' template: https://github.com/Code-Institute-Org/ci-full-template
- Use this template -> create new repository
- Ensure visibility is set to public
- Create repository 
- Open in GitPod
- Run initial commit to ensure the GitPod repository is correctly linked to GitHub

## GitHub User Stories
- I chose to create my user stories on GitHub
- In your project: click 'Board template' -> name it 
- Go to the ellipses in the top-right and  choose 'Workflows' 
- Click 'item added to project' -> edit -> deslect 'pull request'
- Define as 'Status: ToDo' 
- Save
- Turn on workflow 
- Create your user stories  

## Django
- Install Django with the pip3 install command
- Create a new app
- Update settings.py Installed_Apps with the app name
- Import HttpReponse in views.py
- Import the app into urls.py
- Run the server at port 8000
- Copy the hostname between square brackets and add it to the 'Allowed_Hosts' section of settings.py
- Add requirements.txt file with pip3 freeze local > requirements.txt
- Create the project with django-admin startproject <project name>
- Create the env.py file, add to .gitignore, commit changes to check that env.py has been ignored
- If successful, create a secret key and add to env.py

## Database
Sign-up to a database provider and get your database link
- I chose to go with the CodeInstitute for this project: https://dbs.ci-dbs.net/
- Add the database URL to env.py

## Heroku: set up
- First in your GitPod repo, install gunicorn and add to requirements
- Then add the Procfile
- Set DEBUG to False 
- add '.herokuapp.com' to allowed_hosts in your settings file 
- Create a new app on by going to the Heroku homepage -> 'new' -> 'create new app'.
- Name it accordingly: I chose to give it the same name as my GitPod repository for clarity  
- Go to Config Vars: add the secret key, port 8000  and database_url

## Heroku: deploy
- Enure your GitPushes are up-to-date
- Disable collect static in Heroku's config vars
- Enable automatic deloyment from GitHub
- Deploy app and check
- The remove the 'disable static' value from config vars
- Re-deploy

## AWS and Stripe
I relied on the walk-though project for the implementation of these, as well as help and advice from the tutoring service. And as shown in the tutor videos:
- I added my product images to a media file in my AWS bucket
- I added the deployed version of my app's checkout as an endpoint to Stripe's webhooks

## Other technologies used
- Am I responsive for the device image at the top of the ReadMe: [Am I Responsive? (ui.dev](https://ui.dev/amiresponsive)
- Google Fonts: https://fonts.google.com/: Roboto and Libre Franklin
- For generating the Favicon: https://favicon.io/
- To generate a random secret key: https://randomkeygen.com/
- Pexels for images: https://www.pexels.com/
- Dall-E for generating product and Facebook images: https://openai.com/index/dall-e-3/
- I HEART IMG for resizing images: https://www.iloveimg.com/resize-image
- CloudConvert for converting images to webp files: https://cloudconvert.com/jpg-to-webp
- Zoho for creating product SKUs: https://www.zoho.com/de-de/inventory/sku-generator/


# Acknowledgements
As ever, a huge thank you to my mentor, Dick Vlaanderen, who saved me from many errors and made many helpful and creative suggestions. All errors remaining in the site are of course my own responsibility.  Thanks also to the CI Tutoring Team for their help on several occassions which saw me through some challenges! Big thanks to my wife Patricia and three kids, Zacharias, Valerie and Livia who have been very patient and forgiving while I completed this project.

# Some useful resources 
I relied heavily on the 'Boutique Ado' walk-through, which was great. Some other resources include the following: 
- On Forms: https://docs.djangoproject.com/en/5.0/topics/forms/
- On CSRF: https://docs.djangoproject.com/en/4.2/ref/csrf/
- AllAuth: https://allauth.org/
- Installed Apps: https://docs.djangoproject.com/en/1.8/ref/settings/#std:setting-INSTALLED_APPS
- The Data Attribute: https://www.w3schools.com/tags/att_global_data.asp
- The bootstrap colours: https://github.com/meetdilip/Bootstrap-5-colours
- Bootstrap grids: https://getbootstrap.com/docs/5.0/layout/grid/
- Custom 404 page: https://stackoverflow.com/questions/35156134/how-to-properly-setup-custom-handler404-in-djang

The documenation for Bootstrap and Django were in general helpful, as was W3Schools:
- https://docs.djangoproject.com/en/5.1/
- https://getbootstrap.com/docs/4.1/getting-started/introduction/
- https://www.w3schools.com/
