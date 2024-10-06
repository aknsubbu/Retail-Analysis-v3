package com.example.RetailAnalysis.Model;

import java.util.List;

import com.example.RetailAnalysis.utils.ProductListConverter;
import com.opencsv.bean.CsvBindByName;
import com.opencsv.bean.CsvCustomBindByName;

public class Transaction {

    @CsvBindByName(column = "Transaction_ID")
    private String transactionId;

    @CsvBindByName(column = "Date")
    private String date;

    @CsvBindByName(column = "Customer_Name")
    private String customerName;

    // Modify the field to be a List<String>
    @CsvCustomBindByName(column = "Product", converter = ProductListConverter.class)
    private List<String> product;

    @CsvBindByName(column = "Total_Items")
    private int totalItems;

    @CsvBindByName(column = "Total_Cost")
    private double totalCost;

    @CsvBindByName(column = "Payment_Method")
    private String paymentMethod;

    @CsvBindByName(column = "City")
    private String city;

    @CsvBindByName(column = "Store_Type")
    private String storeType;

    @CsvBindByName(column = "Discount_Applied")
    private boolean discountApplied;

    @CsvBindByName(column = "Customer_Category")
    private String customerCategory;

    @CsvBindByName(column = "Season")
    private String season;

    @CsvBindByName(column = "Promotion")
    private String promotion;

    // Getters and setters
    public String getTransactionId() {
        return transactionId;
    }

    public void setTransactionId(String transactionId) {
        this.transactionId = transactionId;
    }

    public String getDate() {
        return date;
    }

    public void setDate(String date) {
        this.date = date;
    }

    public String getCustomerName() {
        return customerName;
    }

    public void setCustomerName(String customerName) {
        this.customerName = customerName;
    }

    public List<String> getProduct() {
        return product;
    }

    public void setProduct(List<String> product) {
        this.product = product;
    }

    public int getTotalItems() {
        return totalItems;
    }

    public void setTotalItems(int totalItems) {
        this.totalItems = totalItems;
    }

    public double getTotalCost() {
        return totalCost;
    }

    public void setTotalCost(double totalCost) {
        this.totalCost = totalCost;
    }

    public String getPaymentMethod() {
        return paymentMethod;
    }

    public void setPaymentMethod(String paymentMethod) {
        this.paymentMethod = paymentMethod;
    }

    public String getCity() {
        return city;
    }

    public void setCity(String city) {
        this.city = city;
    }

    public String getStoreType() {
        return storeType;
    }

    public void setStoreType(String storeType) {
        this.storeType = storeType;
    }

    public boolean isDiscountApplied() {
        return discountApplied;
    }

    public void setDiscountApplied(boolean discountApplied) {
        this.discountApplied = discountApplied;
    }

    public String getCustomerCategory() {
        return customerCategory;
    }

    public void setCustomerCategory(String customerCategory) {
        this.customerCategory = customerCategory;
    }

    public String getSeason() {
        return season;
    }

    public void setSeason(String season) {
        this.season = season;
    }

    public String getPromotion() {
        return promotion;
    }

    public void setPromotion(String promotion) {
        this.promotion = promotion;
    }

    @Override
    public String toString() {
        return "Transaction{"
                + "Transaction_ID='" + transactionId + '\''
                + ", Date='" + date + '\''
                + ", Customer_Name='" + customerName + '\''
                + ", Product=" + product
                + ", Total_Items=" + totalItems
                + ", Total_Cost=" + totalCost
                + ", Payment_Method='" + paymentMethod + '\''
                + ", City='" + city + '\''
                + ", Store_Type='" + storeType + '\''
                + ", Discount_Applied=" + discountApplied
                + ", Customer_Category='" + customerCategory + '\''
                + ", Season='" + season + '\''
                + ", Promotion='" + promotion + '\''
                + '}';
    }
}
