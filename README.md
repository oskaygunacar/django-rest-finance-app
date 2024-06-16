# Tradehub (Trade App) (Crypto - Stocks Trade Logger with Average Cost Calculator)
![Cover image](./assets/images/django-tradehub-cover.webp)

## Project Description
A trading app designed for users who want to track the average costs of their assets, such as cryptocurrencies and stocks, through a dashboard with graphical support, and keep a log of their transaction history.

## Features
- **PostgreSQL Database**: PostgreSQL is used throughout the project due to extensive operations on decimal values.
- **Asset Category Variety**: Initially, the project includes two basic asset categories: Crypto and Stocks. However, the structure of the project allows for an increase in the number of asset categories as needed.
- **Various Types and Numbers of Assets**: Users can create as many new assets as they want in the static categories provided (crypto, stocks) and keep transaction logs within these assets.
- **Asset Category Page/Dashboard**: The Asset Category Dashboard lists all assets created by the user in the selected category (e.g., under the Crypto category: Solana, IOTA, etc.).
- **Asset Detail Pages**: The asset detail pages display all transactions related to the user-created asset within a dashboard. Additionally, they show the total number of assets owned, total cost, and average cost based on the total amount held.
- **Asset Detail Dashboard**: Dashboards are created on the asset detail pages based on the user's transaction logs, showing all transactions and average costs.
- **Automatic Average Cost Calculation**: When entering a new asset transaction on an asset detail page, the average cost is calculated based on the total amount and cost for both buy and sell transactions. Users only need to enter the total asset amount and cost for the transaction they are performing.
- **Average Cost Graph**: An average cost graph is created on the asset detail page based on all purchases, showing the costs of transactions visually. This allows users to track whether their costs are increasing or decreasing.
- **Buy & Sell Transactions**: Users can log both buy and sell transactions in the system.
- **Privacy**: Only logged-in users can access their asset transaction activities and asset categories.
- **Rest API**: Restful API support will be added shortly.

## API Endpoints Documentation

### GET URLs
- **List All Categories**:  
  `/api/categories/`  
  Lists all active categories on the site where assets can be created.

- **List All Assets in a Category**:  
  `/api/<category_slug>/assets/`  
  Lists all assets created under the specified category.  
  Example URL: `/api/crypto/assets/`

- **Asset Details and Transaction Logs**:  
  `/api/<category_slug>/assets/<asset_slug>`  
  Lists details and transaction logs for the specified asset under the specified category.  
  Example URL: `/api/crypto/assets/yyizuhvhayrwxjp/`

### POST URLs
- **Create an Asset in a Category**:  
  `/api/<category_slug>/assets/create/`  
  Creates an asset with the name sent in a POST request in the specified category.  
  Example URL: `/api/crypto/assets/create/`

- **Add a Transaction to an Asset**:  
  `/api/<category_slug>/assets/<asset_slug>/transaction/`  
  Adds a new transaction (buy or sell) to the specified asset in the specified category. The transaction is recorded directly in the database, and the asset data is updated.

### DELETE URLs
- **Delete a Specific Transaction**:  
  `/api/<category_slug>/assets/<asset_slug>/transaction/delete/<transaction_id>/`  
  Deletes the transaction with the specified `transaction_id` for the asset in the specified category using an HTTP Delete Request. No data needs to be sent in the request body, just an authentication token.

- **Delete an Asset**:  
  `/api/<slug:category_slug>/assets/<slug:asset_slug>/delete/`  
  Permanently deletes the specified asset from the specified category using an HTTP Delete Request.

## Limitations
- Users need to register to use the app.

## Getting Started

To get started with this project, follow these steps:

**Step 1**: Clone the project
```bash
git clone https://github.com/oskaygunacar/django-finance-app.git
```

**Step 2**: Navigate to the directory
```bash
cd django-finance-app
```

**Step 3**: Create and activate a virtual environment
```bash
# Create
python -m venv env

# Activate for MacOS & Linux
source env/bin/activate

# Activate for Windows
env\Scripts\activate
```

**Step 4**: Install dependencies
```bash
pip install -r requirements.txt
```
**Step 5**: Configure Settings.py Database Configurations

**If you are planning to use PostgreSQL or other databases, please configure the Settings.py database config first.**

**Step 6**: Migrate the database and create a superuser
```bash
python manage.py migrate
python manage.py createsuperuser
```

**Step 7**: Run the server
```bash
python manage.py runserver
```

## Usage

- Navigate to the site URL to create an account and login to site.
- After login process, you are free to create/log any amount of asset and asset transaction.

## Contributing

Contributions to improve the project are welcome. Please follow the standard fork-and-pull request workflow.


## App Images:
### Homepage
![Homepage](./assets/images/homepage.png)
### Homepage Authenticated
![Homepage Authenticated](./assets/images/homepage-authenticated.png)
### Login Page of the App
![Login page](./assets/images/login.png)
### Signup Page of the App
![Signup page](./assets/images/signup.png)
### Profile Actions on Site Navbar
![Profile Actions](./assets/images/profile-actions.png)
### Asset Category Dashboard
![Asset Category Dashboard](./assets/images/asset-category-dashboard.png)
### Add New Asset Transaction Page
![Add New Asset Transaction](./assets/images/add-new-asset-transaction.png)
### Asset Detail / Dashboard
![Asset Detail / Dashboard](./assets/images/asset-dashboard-detail.png)

