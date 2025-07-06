package com.example.bankportal.service;

import org.springframework.stereotype.Service;

@Service
public class LoginService {
    public boolean authenticate(String username, String password) {
        // This mocks the login-ms microservice.
        // In real: Make a REST call here.
        return "user".equals(username) && "pass".equals(password);
    }
}
