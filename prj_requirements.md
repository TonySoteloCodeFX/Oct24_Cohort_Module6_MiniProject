<h1>Module 6: Mini-Project | E-commerce API</h1>
<hr>

<h2>Project Requirements</h2>

To successfully build our e-commerce application and achieve the learning objectives, we need to establish clear project requirements. These requirements outline the key features and functionalities that our application must encompass. Below, you'll find a comprehensive list of project requirements based on our learning objectives.

<h3>1. Customer and CustomerAccount Management:</h3>

- <b>Create the CRUD</b> (Create, Read, Update, Delete) endpoints for managing Customers and their associated CustomerAccounts:
<br>

- <b>Create Customer:</b> Implement an endpoint to add a new customer to the database. Ensure that you capture essential customer information, including name, email, and phone number.
<br>

- <b>Read Customer:</b> Develop an endpoint to retrieve customer details based on their unique identifier (ID). Provide functionality to query and display customer information.
<br>

- <b>Update Customer:</b> Create an endpoint for updating customer details, allowing modifications to the customer's name, email, and phone number.
<br>

- <b>Delete Customer:</b> Implement an endpoint to delete a customer from the system based on their ID.
<br>

<h1>This is where I left off</h1>

- <b>Create CustomerAccount:</b> Develop an endpoint to create a new customer account. This should include fields for a unique username and a secure password.
<br>

- <b>Read CustomerAccount:</b> Implement an endpoint to retrieve customer account details, including the associated customer's information.
<br>

- <b>Update CustomerAccount:</b> Create an endpoint for updating customer account information, including the username and password.
<br>

- <b>Delete CustomerAccount:</b> Develop an endpoint to delete a customer account.

<h3>2. Product Catalog:</h3>

- <b>Create the CRUD</b> (Create, Read, Update, Delete) endpoints for managing Products:
<br>

- <b>Create Product:</b> Implement an endpoint to add a new product to the e-commerce database. Capture essential product details, such as the product name and price.
<br>

- <b>Read Product:</b> Develop an endpoint to retrieve product details based on the product's unique identifier (ID). Provide functionality to query and display product information.
<br>

- <b>Update Product:</b> Create an endpoint for updating product details, allowing modifications to the product name and price.
<br>

- <b>Delete Product:</b> Implement an endpoint to delete a product from the system based on its unique ID.
<br>

- <b>List Products:</b> Develop an endpoint to list all available products in the e-commerce platform. Ensure that the list provides essential product information.
<br>

- <b>View and Manage Product Stock Levels (Bonus):</b> Create an endpoint that allows to view and manage the stock levels of each product in the catalog. Administrators should be able to see the current stock level and make adjustments as needed.
<br>

- <b>Restock Products When Low (Bonus):</b> Develop an endpoint that monitors product stock levels and triggers restocking when they fall below a specified threshold. Ensure that stock replenishment is efficient and timely.

<h3>3. Order Processing:</h3>

- <b>Develop comprehensive Orders Management:</b> functionality to efficiently handle customer orders, ensuring that customers can place, track, and manage their orders seamlessly.
<br>

- <b>Place Order:</b> Create an endpoint for customers to place new orders, specifying the products they wish to purchase and providing essential order details. Each order should capture the order date and the associated customer.
<br>

- <b>Retrieve Order:</b> Implement an endpoint that allows customers to retrieve details of a specific order based on its unique identifier (ID). Provide a clear overview of the order, including the order date and associated products.
<br>

- <b>Track Order:</b> Develop functionality that enables customers to track the status and progress of their orders. Customers should be able to access information such as order dates and expected delivery dates.
<br>

- <b>Manage Order History (Bonus):</b> Create an endpoint that allows customers to access their order history, listing all previous orders placed. Each order entry should provide comprehensive information, including the order date and associated products.
<br>

- <b>Cancel Order (Bonus):</b> Implement an order cancellation feature, allowing customers to cancel an order if it hasn't been shipped or completed. Ensure that canceled orders are appropriately reflected in the system.
<br>

- <b>Calculate Order Total Price (Bonus):</b> Include an endpoint that calculates the total price of items in a specific order, considering the prices of the products included in the order. This calculation should be specific to each customer and each order, providing accurate pricing information.

<h3>4. Database Integration:</h3>

- <b>Utilize Flask-SQLAlchemy</b> to integrate a MySQL database into the application.
<br>

- <b>Design and create the necessary Model</b> to represent customers, orders, products, customer accounts, and any additional features.
<br>

- <b>Establish relationships</b> between tables to model the application's core functionality.
<br>

- <b>Ensure proper database connections</b> and interactions for data storage and retrieval.

<h3>5. Data Validation and Error Handling:</h3>

- <b>Implement data validation mechanisms</b> to ensure that user inputs meet specified criteria (e.g., valid email addresses, proper formatting).
<br>

- <b>Use try, except, else, and finally blocks</b> to handle errors gracefully and provide informative error messages to guide users.

<h3>6. User Interface (Postman):</h3>

- <b>Develop Postman collections</b> that categorize and group API requests according to their functionality. Separate collections for Customer Management, Product Management, Order Management, and Bonus Features should be created for clarity.

<h3>GitHub Repository:</h3>

- <b>Create a GitHub repository</b> for the project and commit code regularly.
<br>

- <b>Maintain a clean and interactive README.md</b> file in the GitHub repository, providing clear instructions on how to run the application and explanations of its features.
<br>

- <b>Include</b> a link to the GitHub repository in the project documentation.

<h3>Submission</h3>

- Upon completing the project, submit your code, including all source code files, and the README.md file in your GitHub repository to your instructor or designated platform.

<b>Project Rubric:</b> <a href="https://codingtemple.notion.site/Module-6-Mini-Project-9ddc86a0776f4a2fb01ee9ff138c6b27">Module 6 Mini-Project Rubric</a>