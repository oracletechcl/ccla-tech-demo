package com.example.backend.service;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

@Service
public class FunctionService {

    @Value("${function.python.url}")
    private String pythonFunctionUrl;

    @Value("${function.node.url}")
    private String nodeFunctionUrl;

    private final RestTemplate restTemplate = new RestTemplate();

    public String callPythonFunction() {
        return restTemplate.getForObject(pythonFunctionUrl, String.class);
    }

    public String callNodeFunction() {
        return restTemplate.getForObject(nodeFunctionUrl, String.class);
    }
}
