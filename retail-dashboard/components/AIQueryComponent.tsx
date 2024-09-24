import React, { useCallback, useState } from "react";
import { motion } from "framer-motion";
import { MessageSquare, Send } from "lucide-react";

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

const AIAssistant: React.FC = () => {
  const [query, setQuery] = useState<string>("");
  const [response, setResponse] = useState<AIResponse>("");
  const [isExpanded, setIsExpanded] = useState<boolean>(false);
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const faqQuestions = [
    "What are the top 5 products by total sales?",
    "Can you perform customer segmentation and describe the characteristics of each segment?",
    "Who are our top 10 customers by lifetime value?",
    "What are the seasonal trends in our sales data?",
    "Is there a correlation between discount applied and total cost?",
    "What's the most common payment method for high-value transactions?",
    "How does the average transaction value vary across different store types?",
    "Can you identify any interesting patterns or anomalies in the data?",
    "What are the top products purchased by male and female customers?",
    "What are the top categories of products sold in each location?",
    "What are the top products sold in each location?",
    "What are the most common payment methods used by customers in each location and category?",
    "What are the promotions that cause the greatest increase in sales?",
  ];

  const handleSubmit = useCallback(
    async (e: React.FormEvent<HTMLFormElement>) => {
      e.preventDefault();
      console.log("Form submitted with query:", query);
      setIsLoading(true);
      try {
        const result = await mockApiCall(query);
        setResponse(result);
        setIsExpanded(true);
      } catch (error) {
        console.error("Error fetching response:", error);
        setResponse("An error occurred while fetching the response.");
      } finally {
        setIsLoading(false);
      }
    },
    [query]
  );

  const handleFaqClick = useCallback(
    (question: string) => {
      console.log("FAQ clicked:", question);
      setQuery(question);
      handleSubmit({
        preventDefault: () => {},
      } as React.FormEvent<HTMLFormElement>);
    },
    [handleSubmit]
  );

  const mockApiCall = (query: string): Promise<AIResponse> => {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve(`This is a mock response for: "${query}"`);
      }, 1000);
    });
  };

  return (
    <Card className="w-full rounded-xl">
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-xl">
          <MessageSquare className="h-5 w-5" />
          AI Assistant
        </CardTitle>
        <CardDescription>Ask questions about your retail data</CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="flex space-x-2">
            <Input
              type="text"
              value={query}
              onChange={(e: React.ChangeEvent<HTMLInputElement>) => {
                console.log("Input changed:", e.target.value);
                setQuery(e.target.value);
              }}
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
            {faqQuestions.map((question, index) => (
              <Button
                key={index}
                variant="outline"
                onClick={() => handleFaqClick(question)}
                className="h-auto w-full justify-start px-3 py-2 text-left rounded-xl"
              >
                <span className="line-clamp-2">{question}</span>
              </Button>
            ))}
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default AIAssistant;
