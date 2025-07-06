package com.example.bankportal.model;

import java.util.List;

public class Account {
    private String accountNumber;
    private double balance;
    private List<AccountTransaction> transactions;

    // Getters, setters, and constructor
    public Account(String accountNumber, double balance, List<AccountTransaction> transactions) {
        this.accountNumber = accountNumber;
        this.balance = balance;
        this.transactions = transactions;
    }
    public String getAccountNumber() { return accountNumber; }
    public double getBalance() { return balance; }
    public List<AccountTransaction> getTransactions() { return transactions; }
}
