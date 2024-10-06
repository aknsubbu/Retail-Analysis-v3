# Retail Analysis API Service

## Overview

The **Retail Analysis API** is a Spring Boot application designed to manage transactions in a retail environment. It provides various endpoints to perform CRUD (Create, Read, Update, Delete) operations on transaction data stored in a CSV file.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Run the Application](#run-the-application)
- [API Endpoints](#api-endpoints)
  - [Get All Transactions](#get-all-transactions)
  - [Get Transaction by ID](#get-transaction-by-id)
  - [Create Transaction](#create-transaction)
  - [Update Transaction](#update-transaction)
  - [Delete Transaction](#delete-transaction)
- [Data Structure](#data-structure)
- [Sample JSON Requests and Responses](#sample-json-requests-and-responses)

## Prerequisites

- Java Development Kit (JDK) 11 or higher
- Apache Maven
- IDE (e.g., IntelliJ IDEA, Eclipse) for development (optional)

## Run the Application

To run the application, follow these steps:

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd <project-directory>
   ```

2. Build the project using Maven:

   ```bash
   mvn clean install
   ```

3. Run the Spring Boot application:
   ```bash
   mvn spring-boot:run
   ```

The application will start on `http://localhost:8080`.

## API Endpoints

### Get All Transactions

- **Endpoint**: `GET /transactions`
- **Response**:
  ```json
  {
    "success": true,
    "message": "Transactions retrieved successfully",
    "data": [
      /* array of transactions */
    ]
  }
  ```

### Get Transaction by ID

- **Endpoint**: `GET /transactions/{id}`
- **Parameters**:
  - `id`: The ID of the transaction to retrieve.
- **Response**:
  - **Success**:
    ```json
    {
      "success": true,
      "message": "Transaction retrieved successfully",
      "data": {
        /* transaction object */
      }
    }
    ```
  - **Not Found**:
    ```json
    {
      "success": false,
      "message": "Transaction not found",
      "data": null
    }
    ```

### Create Transaction

- **Endpoint**: `POST /transactions`
- **Request Body**:
  ```json
  {
    "transactionId": "12345",
    "date": "2024-10-05",
    "customerName": "John Doe",
    "product": "Smartphone",
    "totalItems": 1,
    "totalCost": 799.99,
    "paymentMethod": "Credit Card",
    "city": "New York",
    "storeType": "Retail",
    "discountApplied": true,
    "customerCategory": "Regular",
    "season": "Fall",
    "promotion": "Black Friday Sale"
  }
  ```
- **Response**:
  ```json
  {
    "success": true,
    "message": "Transaction added successfully",
    "data": null
  }
  ```

### Update Transaction

- **Endpoint**: `PUT /transactions/{id}`
- **Parameters**:
  - `id`: The ID of the transaction to update.
- **Request Body**:
  ```json
  {
    "transactionId": "12345",
    "date": "2024-10-05",
    "customerName": "Jane Doe",
    "product": "Laptop",
    "totalItems": 1,
    "totalCost": 1200.0,
    "paymentMethod": "Debit Card",
    "city": "San Francisco",
    "storeType": "Online",
    "discountApplied": false,
    "customerCategory": "VIP",
    "season": "Fall",
    "promotion": "Cyber Monday Sale"
  }
  ```
- **Response**:
  ```json
  {
    "success": true,
    "message": "Transaction updated successfully",
    "data": null
  }
  ```

### Delete Transaction

- **Endpoint**: `DELETE /transactions/{id}`
- **Parameters**:
  - `id`: The ID of the transaction to delete.
- **Response**:
  ```json
  {
    "success": true,
    "message": "Transaction deleted successfully",
    "data": null
  }
  ```

## Data Structure

The `Transaction` class has the following attributes:

- `transactionId`: String
- `date`: String (formatted as YYYY-MM-DD)
- `customerName`: String
- `product`: String
- `totalItems`: Integer
- `totalCost`: Float
- `paymentMethod`: String
- `city`: String
- `storeType`: String
- `discountApplied`: Boolean
- `customerCategory`: String
- `season`: String
- `promotion`: String

## Sample JSON Requests and Responses

### Create Transaction Sample

- **Request**:

  ```json
  {
    "transactionId": "12346",
    "date": "2024-10-05",
    "customerName": "Alice Smith",
    "product": "Tablet",
    "totalItems": 2,
    "totalCost": 499.99,
    "paymentMethod": "PayPal",
    "city": "Los Angeles",
    "storeType": "Retail",
    "discountApplied": false,
    "customerCategory": "New",
    "season": "Fall",
    "promotion": "End of Season Sale"
  }
  ```

- **Response**:
  ```json
  {
    "success": true,
    "message": "Transaction added successfully",
    "data": null
  }
  ```

### Update Transaction Sample

- **Request**:

  ```json
  {
    "transactionId": "12346",
    "date": "2024-10-06",
    "customerName": "Alice Smith",
    "product": "Tablet",
    "totalItems": 3,
    "totalCost": 749.97,
    "paymentMethod": "PayPal",
    "city": "Los Angeles",
    "storeType": "Retail",
    "discountApplied": true,
    "customerCategory": "New",
    "season": "Fall",
    "promotion": "Holiday Sale"
  }
  ```

- **Response**:
  ```json
  {
    "success": true,
    "message": "Transaction updated successfully",
    "data": null
  }
  ```
