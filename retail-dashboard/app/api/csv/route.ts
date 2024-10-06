import path from "path";
import { promises as fs } from "fs";
import { NextResponse } from "next/server";
import axios from "axios";

interface Transaction {
  Transaction_ID: string;
  Date: string;
  Customer_Name: string;
  Product: string | string[];
  Total_Items: number;
  Total_Cost: number;
  Payment_Method: string;
  City: string;
  Store_Type: string;
  Discount_Applied: boolean;
  Customer_Category: string;
  Season: string;
  Promotion: string;
}

export async function GET() {
  try {
    // Fetch transactions from localhost:8080/transactions
    const response = await axios.get<{ data: Transaction[] }>(
      "http://127.0.0.1:8080/transactions"
    );

    // console.log("API Response:", JSON.stringify(response.data, null, 2));

    if (!response.data || !Array.isArray(response.data.data)) {
      throw new Error("Invalid response format from API");
    }

    const transactions = response.data.data;

    console.log(`Received ${transactions.length} transactions`);

    // Convert transactions to CSV format
    const csvContent = convertToCSV(transactions);

    // Define the local file path in the public folder
    const localFilePath = path.join(
      process.cwd(),
      "public",
      "transactions.csv"
    );
    console.log(`Attempting to write CSV to: ${localFilePath}`);

    // Write the CSV content to the local file
    try {
      await fs.writeFile(localFilePath, csvContent, "utf8");
      console.log(`Local CSV file updated successfully at: ${localFilePath}`);
      // Verify the file was created
      const stats = await fs.stat(localFilePath);
      console.log(`File size: ${stats.size} bytes`);
    } catch (writeError) {
      console.error("Error writing to local CSV file:", writeError);
    }

    // Check if the file exists and is readable
    try {
      await fs.access(localFilePath, fs.constants.R_OK);
      console.log("File is readable");
    } catch (accessError) {
      console.error("File is not accessible:", accessError);
    }

    return new NextResponse(csvContent, {
      status: 200,
      headers: {
        "Content-Type": "text/csv",
      },
    });
  } catch (error) {
    console.error("Error processing transactions:", error);
    return new NextResponse(
      JSON.stringify({
        error: "Error processing transactions",
        details: error,
      }),
      {
        status: 500,
        headers: {
          "Content-Type": "application/json",
        },
      }
    );
  }
}

function convertToCSV(transactions: Transaction[]): string {
  const headers = [
    "Transaction_ID",
    "Date",
    "Customer_Name",
    "Product",
    "Total_Items",
    "Total_Cost",
    "Payment_Method",
    "City",
    "Store_Type",
    "Discount_Applied",
    "Customer_Category",
    "Season",
    "Promotion",
  ];

  const csvRows = [
    headers.join(","), // CSV header row
    ...transactions.map((transaction) => {
      const row = [
        transaction.Transaction_ID || "",
        transaction.Date || "",
        transaction.Customer_Name || "",
        Array.isArray(transaction.Product)
          ? transaction.Product.map((p) => p.replace(/'/g, "")).join("|")
          : transaction.Product || "",
        transaction.Total_Items ?? "",
        transaction.Total_Cost ?? "",
        transaction.Payment_Method || "",
        transaction.City || "",
        transaction.Store_Type || "",
        transaction.Discount_Applied ?? "",
        transaction.Customer_Category || "",
        transaction.Season || "",
        transaction.Promotion || "",
      ];

      return row
        .map((value) =>
          typeof value === "string" ? `"${value.replace(/"/g, '""')}"` : value
        )
        .join(",");
    }),
  ];

  return csvRows.join("\r\n");
}
