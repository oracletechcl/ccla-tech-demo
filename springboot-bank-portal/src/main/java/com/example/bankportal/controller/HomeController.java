package com.example.bankportal.controller;

import com.example.bankportal.model.Account;
import com.example.bankportal.model.CreditCard;
import com.example.bankportal.service.AccountService;
import com.example.bankportal.service.CreditCardService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class HomeController {

    @Autowired
    private AccountService accountService;

    @Autowired
    private CreditCardService creditCardService;

    @GetMapping("/")
    public String index(Model model) {
        model.addAttribute("account", accountService.getAccount());
        model.addAttribute("transactions", accountService.getRecentTransactions());
        model.addAttribute("creditCard", creditCardService.getCreditCard());
        model.addAttribute("cardTransactions", creditCardService.getRecentTransactions());
        return "index";
    }
}
