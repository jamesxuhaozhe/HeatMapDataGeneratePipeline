package com.haozhexu.heatmapgeneratepipeline.logprocess.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class TestController {

    @PostMapping(value = "/test")
    public String test(String input) {
        return input;
    }

    @GetMapping(value = "/tt")
    public String testGet() {
        return "test";
    }
}
