package com.example.backend.controller;

import com.example.backend.service.FunctionService;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api")
public class IntegrationController {

    private final FunctionService functionService;

    public IntegrationController(FunctionService functionService) {
        this.functionService = functionService;
    }

    @GetMapping("/python")
    public String callPythonFunction() {
        return functionService.callPythonFunction();
    }

    @GetMapping("/node")
    public String callNodeFunction() {
        return functionService.callNodeFunction();
    }
}
