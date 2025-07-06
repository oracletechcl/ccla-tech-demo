package com.example.bankportal.service;

import com.example.bankportal.model.CreditCard;
import com.example.bankportal.model.CreditCardTransaction;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.Arrays;
import java.util.List;

@Service
public class CreditCardService {

    public CreditCard getCreditCard() {
        return new CreditCard(
            "**** **** **** 9876",
            2000000,
            850000,
            "2025-07-30",
            getRecentTransactions()
        );
    }

    public List<CreditCardTransaction> getRecentTransactions() {
        return Arrays.asList(
            new CreditCardTransaction("Restaurante", -45000, LocalDateTime.now().minusDays(1)),
            new CreditCardTransaction("Bencina", -60000, LocalDateTime.now().minusDays(2)),
            new CreditCardTransaction("Pago anterior", 500000, LocalDateTime.now().minusDays(10))
        );
    }
}
