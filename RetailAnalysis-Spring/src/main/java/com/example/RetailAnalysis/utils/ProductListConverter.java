package com.example.RetailAnalysis.utils;

import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

import com.opencsv.bean.AbstractBeanField;

public class ProductListConverter extends AbstractBeanField<String, List<String>> {

    // Convert from CSV string to List<String>
    @Override
    protected Object convert(String value) {
        if (value == null || value.isEmpty()) {
            return null;
        }
        // Remove brackets and split by commas
        value = value.replace("[", "").replace("]", "").trim();
        return Arrays.stream(value.split(","))
                .map(String::trim)
                .collect(Collectors.toList());
    }

    // Optional: Convert from List<String> to CSV string (for writing back to CSV)
    @Override
    protected String convertToWrite(Object value) {
        if (value == null) {
            return "";
        }
        @SuppressWarnings("unchecked")
        List<String> productList = (List<String>) value;
        // Convert list to string with comma-separated values
        return productList.stream()
                .map(String::trim)
                .collect(Collectors.joining(", ", "[", "]"));
    }
}
