package com.example.RetailAnalysis;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.ComponentScan;

@SpringBootApplication
@ComponentScan(basePackages = {"com.example.RetailAnalysis"})
public class RetailAnalysisApplication {

    public static void main(String[] args) {
        SpringApplication.run(RetailAnalysisApplication.class, args);
    }

}
