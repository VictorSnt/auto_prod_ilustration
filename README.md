# Automated Product Image Registration Script

## Description
This script automates the registration of product images in a local web ERP system that uses a PostgreSQL database. The script is designed to respect the logic of the ERP system, storing binary data in the database for display on the system screen.

## Status
**In Development**

## Table of Contents
1. [Description](#description)
2. [Status](#status)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Products Description](#products-description)
6. [Contribution](#contribution)
7. [License](#license)
8. [Contact](#contact)

## Installation
To install the script, follow these steps:

1. **Clone the Repository**
    ```bash
    git clone https://github.com/VictorSnt/auto_prod_ilustration/
    cd auto_prod_ilustration
    ```

2. **Create a Python Virtual Environment**
    ```bash
    python -m venv venv
    ```

3. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

## Usage
To use the script for product image registration, follow these instructions:

1. **Set Up Your Environment Variables**
    - Copy the `.env.example` file as `.env` and configure it with your specific details.

2. **Adapt Database Queries**
    - Modify the database queries in the script to match your database structure.

3. **Adapt the img_insersion_routine.py**
    - You will need to reimplement this logic based on your needs. If you have an old legacy system that you can't work on the front code, this solution is basically ready for you.

4. **Run the Script**
    - Execute the script to automate product image registration.
    ```bash
    python img_inserter/img_download_routine.py
    ```

## Products Description
Before running the script, make sure you have a comprehensive description of the products you intend to webscrape for images. Ensure you have details such as product names, IDs, and any other relevant information needed for the script to identify and register the images correctly.

## Contact
For more information or questions, contact Victor Santos via [victoorsantos266@gmail.com](mailto:victoorsantos266@gmail.com).
