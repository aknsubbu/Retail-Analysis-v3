package com.example.RetailAnalysis.Controller;

import java.io.IOException;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.example.RetailAnalysis.Model.Transaction;
import com.example.RetailAnalysis.Service.TransactionService;

@RestController
@RequestMapping("/transactions")
public class TransactionController {

    @Autowired
    private TransactionService transactionService;

    // Get all transactions
    @GetMapping
    public ResponseEntity<Object> getAllTransactions() {
        List<Transaction> transactions = transactionService.getAllTransactions();
        return ResponseEntity.ok(new ApiResponse<>(true, "Transactions retrieved successfully", transactions));
    }

    // Get transaction by ID
    @GetMapping("/{id}")
    public ResponseEntity<ApiResponse<Transaction>> getTransactionById(@PathVariable String id) {
        List<Transaction> transactions = transactionService.getAllTransactions();
        return transactions.stream()
                .filter(t -> t.getTransactionId().equals(id))
                .findFirst()
                .map(t -> ResponseEntity.ok(new ApiResponse<>(true, "Transaction retrieved successfully", t)))
                .orElse(ResponseEntity.status(HttpStatus.NOT_FOUND).body(new ApiResponse<>(false, "Transaction not found", null)));
    }

    // Add new transaction
    @PostMapping
    public ResponseEntity<Object> createTransaction(@RequestBody Transaction transaction) {
        try {
            System.out.println("Received Transaction: " + transaction);
            transactionService.addTransaction(transaction);
            return ResponseEntity.status(HttpStatus.CREATED).body(new ApiResponse<>(true, "Transaction added successfully", null));
        } catch (IOException e) {
            // Log the error for debugging
            System.err.println("Error adding transaction: " + e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(new ApiResponse<>(false, "Error adding transaction: " + e.getMessage(), null));
        }
    }

    // Update transaction
    @PutMapping("/{id}")
    public ResponseEntity<Object> updateTransaction(@PathVariable String id, @RequestBody Transaction transaction) {
        try {
            transaction.setTransactionId(id);
            transactionService.updateTransaction(transaction);
            return ResponseEntity.ok(new ApiResponse<>(true, "Transaction updated successfully", null));
        } catch (IOException e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(new ApiResponse<>(false, "Error updating transaction", null));
        }
    }

    // Delete transaction
    @DeleteMapping("/{id}")
    public ResponseEntity<Object> deleteTransaction(@PathVariable String id) {
        try {
            transactionService.deleteTransaction(id);
            return ResponseEntity.ok(new ApiResponse<>(true, "Transaction deleted successfully", null));
        } catch (IOException e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(new ApiResponse<>(false, "Error deleting transaction", null));
        }
    }

    // ApiResponse class for consistent response structure
    public static class ApiResponse<T> {

        private boolean success;
        private String message;
        private T data;

        public ApiResponse(boolean success, String message, T data) {
            this.success = success;
            this.message = message;
            this.data = data;
        }

        // Getters and setters
        public boolean isSuccess() {
            return success;
        }

        public void setSuccess(boolean success) {
            this.success = success;
        }

        public String getMessage() {
            return message;
        }

        public void setMessage(String message) {
            this.message = message;
        }

        public T getData() {
            return data;
        }

        public void setData(T data) {
            this.data = data;
        }
    }
}
