package com.example.bankportal.model;

import java.time.LocalDateTime;

public class CreditCardTransaction {
    private String description;
    private double amount;
    private LocalDateTime date;

    public CreditCardTransaction(String description, double amount, LocalDateTime date) {
        this.description = description;
        this.amount = amount;
        this.date = date;
    }
    public String getDescription() { return description; }
    public double getAmount() { return amount; }
    public LocalDateTime getDate() { return date; }
}
