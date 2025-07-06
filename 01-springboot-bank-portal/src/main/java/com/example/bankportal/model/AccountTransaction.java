package com.example.bankportal.model;

import java.time.LocalDateTime;

public class AccountTransaction {
    private String description;
    private double amount;
    private LocalDateTime date;

    public AccountTransaction(String description, double amount, LocalDateTime date) {
        this.description = description;
        this.amount = amount;
        this.date = date;
    }
    public String getDescription() { return description; }
    public double getAmount() { return amount; }
    public LocalDateTime getDate() { return date; }
}
