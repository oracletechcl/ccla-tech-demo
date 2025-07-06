package com.example.bankportal.controller;

import com.example.bankportal.service.LoginService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;
import org.springframework.ui.Model;

@Controller
public class LoginController {

    @Autowired
    private LoginService loginService;

    @GetMapping("/login")
    public String loginPage(@RequestParam(value = "error", required = false) String error, Model model) {
        model.addAttribute("error", error != null);
        return "login";
    }

    @PostMapping("/login")
    public String doLogin(@RequestParam String username, @RequestParam String password, Model model) {
        boolean authenticated = loginService.authenticate(username, password);
        if (authenticated) {
            // In a real app: Set user in session or security context
            return "redirect:/";
        } else {
            return "redirect:/login?error";
        }
    }
}
