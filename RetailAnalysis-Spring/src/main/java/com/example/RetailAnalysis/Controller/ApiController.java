package com.example.RetailAnalysis.Controller;

import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

class response1 {

    public String message;

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }
}

@RestController
@RequestMapping("/api")
public class ApiController {

    @GetMapping("/hello")
    ResponseEntity<response1> sendResponse() {
        response1 response = new response1();
        response.setMessage("HEllo world");
        return ResponseEntity.ok().contentType(MediaType.APPLICATION_JSON).body(response);
    }
}
