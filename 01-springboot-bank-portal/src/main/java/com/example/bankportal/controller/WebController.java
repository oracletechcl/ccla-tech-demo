package com.example.bankportal.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;

@Controller
public class WebController {
    // Fallback: send all paths except those with a dot (.) to index.html
    @RequestMapping(value = {"/{path:[^\\.]*}", "/"})
    public String redirect() {
        return "forward:/index.html";
    }
}
