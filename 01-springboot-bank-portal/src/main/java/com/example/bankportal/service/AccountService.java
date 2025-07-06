package com.example.bankportal.service;

import com.example.bankportal.model.Account;
import com.example.bankportal.model.AccountTransaction;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.Arrays;
import java.util.List;

@Service
public class AccountService {

    public Account getAccount() {
        return new Account(
            "123456789",
            1234567.89,
            getRecentTransactions()
        );
    }

    public List<AccountTransaction> getRecentTransactions() {
        return Arrays.asList(
            new AccountTransaction("Pago luz", -35000, LocalDateTime.now().minusDays(1)),
            new AccountTransaction("Transferencia recibida", 200000, LocalDateTime.now().minusDays(2)),
            new AccountTransaction("Compra supermercado", -45000, LocalDateTime.now().minusDays(3)),
            new AccountTransaction("Abono nómina", 1200000, LocalDateTime.now().minusDays(7))
        );
    }
}
