import React, { useCallback, useState } from "react";
import { motion } from "framer-motion";
import { MessageSquare, Send } from "lucide-react";
import axios from "axios";

import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";

type AIResponse = string;

type AnalysisType =
  | "product"
  | "customer"
  | "seasonal"
  | "financial"
  | "transaction"
  | "anomaly"
  | "gender_based_item"
  | "location_based_category"
  | "location_based_item"
  | "payment_method"
  | "promotion"
  | "custom";

interface FAQItem {
  question: string;
  analysisType: AnalysisType;
}

// Create an Axios instance with default configuration
const api = axios.create({
  baseURL: "http://localhost:8000",
  headers: {
    "Content-Type": "application/json",
    Accept: "application/json",
  },
  withCredentials: true,
});

const AIAssistant: React.FC = () => {
  const [query, setQuery] = useState<string>("");
  const [response, setResponse] = useState<AIResponse>("");
  const [isExpanded, setIsExpanded] = useState<boolean>(false);
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const faqQuestions: FAQItem[] = [
    {
      question: "What are the top 5 products by total sales?",
      analysisType: "product",
    },
    {
      question:
        "Can you perform customer segmentation and describe the characteristics of each segment?",
      analysisType: "customer",
    },
    {
      question: "What are the seasonal trends in our sales data?",
      analysisType: "seasonal",
    },
    {
      question:
        "Is there a correlation between discount applied and total cost?",
      analysisType: "financial",
    },
    {
      question:
        "What's the most common payment method for high-value transactions?",
      analysisType: "transaction",
    },
    {
      question:
        "Can you identify any interesting patterns or anomalies in the data?",
      analysisType: "anomaly",
    },
    {
      question:
        "What are the top products purchased by male and female customers?",
      analysisType: "gender_based_item",
    },
    {
      question:
        "What are the top categories of products sold in each location?",
      analysisType: "location_based_category",
    },
    {
      question: "What are the top products sold in each location?",
      analysisType: "location_based_item",
    },
    {
      question:
        "What are the most common payment methods used by customers in each location and category?",
      analysisType: "payment_method",
    },
    {
      question:
        "What are the promotions that cause the greatest increase in sales?",
      analysisType: "promotion",
    },
  ];

  const fetchAIResponse = useCallback(
    async (
      query: string,
      analysisType: AnalysisType = "custom"
    ): Promise<AIResponse> => {
      try {
        const response = await api.post("/analyze", {
          analysis_type: analysisType,
          custom_question: analysisType === "custom" ? query : undefined,
        });

        return response.data.result;
      } catch (error) {
        if (axios.isAxiosError(error)) {
          if (error.response?.status === 429) {
            throw new Error("Rate limit exceeded. Please try again later.");
          }
          throw new Error(`Failed to fetch AI response: ${error.message}`);
        }
        throw new Error("An unexpected error occurred");
      }
    },
    []
  );

  const handleQuery = useCallback(
    async (queryText: string, analysisType: AnalysisType = "custom") => {
      setIsLoading(true);
      setQuery(queryText);
      try {
        const result = await fetchAIResponse(queryText, analysisType);
        setResponse(result);
        setIsExpanded(true);
      } catch (error) {
        console.error("Error fetching response:", error);
        setResponse("An error occurred while fetching the response.");
      } finally {
        setIsLoading(false);
      }
    },
    [fetchAIResponse]
  );

  const handleSubmit = useCallback(
    (e: React.FormEvent<HTMLFormElement>) => {
      e.preventDefault();
      handleQuery(query);
    },
    [query, handleQuery]
  );

  const handleFaqClick = useCallback(
    (faqItem: FAQItem) => {
      handleQuery(faqItem.question, faqItem.analysisType);
    },
    [handleQuery]
  );

  return (
    <Card className="w-full rounded-xl">
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-xl">
          <MessageSquare className="h-5 w-5" />
          Retail Analysis AI Assistant
        </CardTitle>
        <CardDescription>Ask questions about your retail data</CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="flex space-x-2">
            <Input
              type="text"
              value={query}
              onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                setQuery(e.target.value)
              }
              placeholder="Ask a question..."
              className="flex-grow rounded-xl bg-white/10"
            />
            <Button type="submit" disabled={isLoading} className="rounded-xl">
              {isLoading ? (
                "Loading..."
              ) : (
                <>
                  <Send className="mr-2 h-4 w-4 " />
                  Send
                </>
              )}
            </Button>
          </div>
        </form>

        <motion.div
          initial={{ height: 0, opacity: 0 }}
          animate={{
            height: isExpanded ? "auto" : 0,
            opacity: isExpanded ? 1 : 0,
          }}
          transition={{ duration: 0.3 }}
          className="mt-4 overflow-hidden"
        >
          <Card className="bg-secondary">
            <CardContent className="p-4">
              <p className="text-sm">{response}</p>
            </CardContent>
          </Card>
        </motion.div>

        <div className="mt-8">
          <h3 className="mb-2 text-lg font-semibold">
            Frequently Asked Questions
          </h3>
          <div className="grid grid-cols-1 gap-2 md:grid-cols-2">
            {faqQuestions.map((faqItem, index) => (
              <Button
                key={index}
                variant="outline"
                onClick={() => handleFaqClick(faqItem)}
                className="h-auto w-full justify-start px-3 py-2 text-left rounded-xl"
              >
                <span className="line-clamp-2">{faqItem.question}</span>
              </Button>
            ))}
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default AIAssistant;
