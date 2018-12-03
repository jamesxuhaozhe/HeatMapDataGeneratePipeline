package com.haozhexu.heatmapgeneratepipeline.logprocess.controller;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class TestController {

    private static final Logger logger = LoggerFactory.getLogger(TestController.class);

    @PostMapping(value = "/test")
    public String test(String input) {
        logger.info("input:" + input);
        return input;
    }


    public static void main(String[] args) {
        int i = 0;
        while (true) {
            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            i++;

            logger.info("input:" + i);
        }

    }
}
