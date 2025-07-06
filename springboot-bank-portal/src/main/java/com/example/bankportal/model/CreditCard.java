package com.example.bankportal.model;

import java.util.List;

public class CreditCard {
    private String cardNumber;
    private double limit;
    private double used;
    private String dueDate;
    private List<CreditCardTransaction> transactions;

    public CreditCard(String cardNumber, double limit, double used, String dueDate, List<CreditCardTransaction> transactions) {
        this.cardNumber = cardNumber;
        this.limit = limit;
        this.used = used;
        this.dueDate = dueDate;
        this.transactions = transactions;
    }
    public String getCardNumber() { return cardNumber; }
    public double getLimit() { return limit; }
    public double getUsed() { return used; }
    public String getDueDate() { return dueDate; }
    public List<CreditCardTransaction> getTransactions() { return transactions; }
}
