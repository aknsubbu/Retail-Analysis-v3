"use client";

import React, { useEffect, useState, useMemo } from "react";
import { CreditCard, DollarSign, MapPin, ShoppingBag } from "lucide-react";
import {
  Area,
  AreaChart,
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import Papa from "papaparse";
import axios from "axios";

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import AIQueryComponent from "@/components/AIQueryComponent";
import { DockDemo } from "@/components/dock-demo";

type TransactionData = {
  Transaction_ID: string;
  Date: string;
  Customer_Name: string;
  Product: string;
  Total_Items: string;
  Total_Cost: string;
  Payment_Method: string;
  City: string;
  Store_Type: string;
  Discount_Applied: string;
  Customer_Category: string;
  Season: string;
  Promotion: string;
};

const COLORS = ["#0088FE", "#00C49F", "#FFBB28", "#FF8042", "#8884d8"];

const useReadCSV = () => {
  const [values, setValues] = useState<TransactionData[]>([]);
  const [loading, setLoading] = useState(true);

  // make the api call to the route and to write to the file
  // try {
  //   const response = axios.get("/api/csv");

  //   console.log(response);
  // } catch (error) {
  //   console.error("Error in fetchAndReadCSV:", error);
  // }

  useEffect(() => {
    setLoading(true);

    Papa.parse("/transactions.csv", {
      header: true,
      download: true,
      skipEmptyLines: true,
      delimiter: ",",
      complete: (results: Papa.ParseResult<TransactionData>) => {
        setValues(results.data);
        setLoading(false);
      },
    });
  }, []);

  return { data: values, loading };
};

const Dashboard: React.FC = () => {
  const { data: csvData, loading: csvLoading } = useReadCSV();
  const [timePeriod, setTimePeriod] = useState<"month" | "week" | "year">(
    "month"
  );
  const [salesData, setSalesData] = useState<{ date: string; sales: number }[]>(
    []
  );
  const [storeTypeData, setStoreTypeData] = useState<
    { name: string; value: number; fill: string }[]
  >([]);
  const [productCategoryData, setProductCategoryData] = useState<
    { name: string; value: number; fill: string }[]
  >([]);
  const [cityDistributionData, setCityDistributionData] = useState<
    { name: string; value: number }[]
  >([]);
  const [paymentMethodData, setPaymentMethodData] = useState<
    { name: string; value: number }[]
  >([]);
  const [totalTransactions, setTotalTransactions] = useState(0);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!csvLoading && csvData.length > 0) {
      setLoading(true);
      const processedSalesData = processDataByTimePeriod(csvData, timePeriod);

      setSalesData(processedSalesData);

      const processedStoreTypeData = processDataForPieChart(
        csvData,
        "Store_Type"
      );

      setStoreTypeData(processedStoreTypeData);

      const processedProductCategoryData = processDataForPieChart(
        csvData,
        "Product"
      );

      setProductCategoryData(processedProductCategoryData);

      const { processCityData, processPaymentMethodData } =
        processDataForBarChart;
      const processedCityData = processCityData(csvData);

      setCityDistributionData(processedCityData);

      const processedPaymentMethodData = processPaymentMethodData(csvData);

      setPaymentMethodData(processedPaymentMethodData);

      setTotalTransactions(csvData.length);
      setLoading(false);
    }
  }, [csvData, csvLoading, timePeriod]);

  const processDataByTimePeriod = useMemo(
    () => (data: TransactionData[], period: "month" | "week" | "year") => {
      const salesByPeriod: { [key: string]: number } = {};

      data.forEach((transaction) => {
        const date = new Date(transaction.Date);

        if (isNaN(date.getTime())) return; // Skip invalid dates

        let key: string;

        switch (period) {
          case "week":
            key = `${date.getFullYear()}-W${getWeekNumber(date)}`;
            break;
          case "month":
            key = `${date.getFullYear()}-${(date.getMonth() + 1).toString().padStart(2, "0")}`;
            break;
          case "year":
            key = date.getFullYear().toString();
            break;
        }

        const cost = parseFloat(transaction.Total_Cost);

        if (!isNaN(cost)) {
          salesByPeriod[key] = (salesByPeriod[key] || 0) + cost;
        }
      });

      return Object.entries(salesByPeriod)
        .map(([date, sales]) => ({ date, sales }))
        .sort((a, b) => a.date.localeCompare(b.date));
    },
    []
  );

  const processDataForPieChart = useMemo(
    () => (data: TransactionData[], key: "Store_Type" | "Product") => {
      const counts: { [key: string]: number } = {};

      data.forEach((transaction) => {
        const value = transaction[key];

        if (value) {
          counts[value] = (counts[value] || 0) + 1;
        }
      });

      return Object.entries(counts)
        .map(([name, value], index) => ({
          name,
          value,
          fill: COLORS[index % COLORS.length],
        }))
        .sort((a, b) => b.value - a.value)
        .slice(0, 5); // Top 5
    },
    []
  );

  const processDataForBarChart = useMemo(() => {
    const processData = (
      data: TransactionData[],
      key: "City" | "Payment_Method"
    ) => {
      const counts: { [key: string]: number } = {};
      let total = 0;

      data.forEach((transaction) => {
        const value = transaction[key];

        if (value) {
          counts[value] = (counts[value] || 0) + 1;
          total++;
        }
      });

      const sortedData = Object.entries(counts)
        .map(([name, value]) => ({
          name,
          value,
          percentage: ((value / total) * 100).toFixed(1) + "%",
        }))
        .sort((a, b) => b.value - a.value);

      // If there are more than 5 types, take top 5 and sum others
      if (sortedData.length > 5) {
        const top5 = sortedData.slice(0, 5);
        const otherValue = sortedData
          .slice(5)
          .reduce((sum, item) => sum + item.value, 0);
        const otherPercentage = ((otherValue / total) * 100).toFixed(1) + "%";

        return [
          ...top5,
          { name: "Other", value: otherValue, percentage: otherPercentage },
        ];
      }

      return sortedData;
    };

    return {
      processCityData: (data: TransactionData[]) => processData(data, "City"),
      processPaymentMethodData: (data: TransactionData[]) =>
        processData(data, "Payment_Method"),
    };
  }, []);

  const getWeekNumber = (date: Date) => {
    const d = new Date(
      Date.UTC(date.getFullYear(), date.getMonth(), date.getDate())
    );
    const dayNum = d.getUTCDay() || 7;

    d.setUTCDate(d.getUTCDate() + 4 - dayNum);
    const yearStart = new Date(Date.UTC(d.getUTCFullYear(), 0, 1));

    return Math.ceil(((d.getTime() - yearStart.getTime()) / 86400000 + 1) / 7);
  };

  const formatXAxis = (tickItem: string) => {
    switch (timePeriod) {
      case "week":
        return `Week ${tickItem.split("-W")[1]}`;
      case "month":
        return new Date(tickItem + "-01").toLocaleString("default", {
          month: "short",
        });
      case "year":
        return tickItem;
      default:
        return tickItem;
    }
  };

  if (loading || csvLoading) {
    return (
      <div className="flex h-screen items-center justify-center">
        <div className="animate-spin-slow size-20 text-white " />
        <div className="animate-pulse text-xl ml-4">Loading data...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100 dark:bg-gray-900">
      <div className="absolute inset-0 overflow-hidden">
        <div className="animate-spin-slow absolute left-1/2 top-1/2 size-full -translate-x-1/2 -translate-y-1/2 rounded-full bg-gradient-to-br from-indigo-500/10 to-purple-500/10 blur-[100px]" />
      </div>
      <div className="">
        <DockDemo />
      </div>
      <div className="container mx-auto px-4 py-8">
        <div className="mb-6 grid grid-cols-1 gap-6 lg:grid-cols-4">
          <Card className="rounded-xl">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total Sales</CardTitle>
              <DollarSign className="size-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                $
                {salesData
                  .reduce((sum, { sales }) => sum + sales, 0)
                  .toLocaleString()}
              </div>
              <p className="text-xs text-muted-foreground">
                total sales in lifetime
              </p>
            </CardContent>
          </Card>
          <Card className="rounded-xl">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                Total Transactions
              </CardTitle>
              <CreditCard className="size-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {totalTransactions.toLocaleString()}
              </div>
              <p className="text-xs text-muted-foreground">
                total number of transactions
              </p>
            </CardContent>
          </Card>
          <Card className="rounded-xl">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                Top Store Type
              </CardTitle>
              <ShoppingBag className="size-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{storeTypeData[0]?.name}</div>
              <p className="text-xs text-muted-foreground">
                {((storeTypeData[0]?.value / totalTransactions) * 100).toFixed(
                  1
                )}
                % of total
              </p>
            </CardContent>
          </Card>
          <Card className="rounded-xl">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Top City</CardTitle>
              <MapPin className="size-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {cityDistributionData[0]?.name}
              </div>
              <p className="text-xs text-muted-foreground">
                {(
                  (cityDistributionData[0]?.value / totalTransactions) *
                  100
                ).toFixed(1)}
                % of total
              </p>
            </CardContent>
          </Card>
        </div>

        <div className="mb-6 grid grid-cols-1 gap-6 lg:grid-cols-2">
          <Card className="col-span-2 rounded-xl">
            <CardHeader>
              <CardTitle className="text-xl">Sales Over Time</CardTitle>
              <div className="flex items-center space-x-2">
                <CardDescription>Showing total sales over time</CardDescription>
                <Select
                  value={timePeriod}
                  onValueChange={(value: any) =>
                    setTimePeriod(value as "month" | "week" | "year")
                  }
                >
                  <SelectTrigger className="w-[180px]">
                    <SelectValue placeholder="Select time period" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="week">Weekly</SelectItem>
                    <SelectItem value="month">Monthly</SelectItem>
                    <SelectItem value="year">Yearly</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </CardHeader>
            <CardContent className="h-[400px]">
              {salesData.length > 0 ? (
                <ResponsiveContainer height="100%" width="100%">
                  <AreaChart data={salesData}>
                    <defs>
                      <linearGradient
                        id="colorSales"
                        x1="0"
                        x2="0"
                        y1="0"
                        y2="1"
                      >
                        <stop
                          offset="5%"
                          stopColor="#8884d8"
                          stopOpacity={0.8}
                        />
                        <stop
                          offset="95%"
                          stopColor="#8884d8"
                          stopOpacity={0}
                        />
                      </linearGradient>
                    </defs>
                    <XAxis
                      allowDuplicatedCategory={false}
                      dataKey="date"
                      tickFormatter={formatXAxis}
                    />
                    <YAxis
                      tickFormatter={(value) => `$${value.toLocaleString()}`}
                      width={80}
                    />
                    <CartesianGrid strokeDasharray="3 3" />
                    <Tooltip
                      formatter={(value: any) => {
                        if (typeof value === "number" && !isNaN(value)) {
                          return `$${value.toLocaleString()}`;
                        }

                        return "N/A";
                      }}
                    />
                    <Area
                      dataKey="sales"
                      fill="url(#colorSales)"
                      fillOpacity={1}
                      stroke="#8884d8"
                      type="monotone"
                    />
                  </AreaChart>
                </ResponsiveContainer>
              ) : (
                <div className="flex h-full items-center justify-center">
                  No sales data available
                </div>
              )}
            </CardContent>
          </Card>

          <Card className="rounded-xl">
            <CardHeader>
              <CardTitle className="text-xl">Store Type Distribution</CardTitle>
              <CardDescription>Top 5 store types</CardDescription>
            </CardHeader>
            <CardContent className="h-[300px]">
              <ResponsiveContainer height="100%" width="100%">
                <PieChart>
                  <Pie
                    cx="50%"
                    cy="50%"
                    data={storeTypeData}
                    dataKey="value"
                    fill="#8884d8"
                    labelLine={false}
                    outerRadius={80}
                  >
                    {storeTypeData.map((entry, index) => (
                      <Cell
                        key={`cell-${index}`}
                        fill={COLORS[index % COLORS.length]}
                      />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>

          <Card className="rounded-xl">
            <CardHeader>
              <CardTitle className="text-xl">
                Product Category Distribution
              </CardTitle>
              <CardDescription>Top 5 product categories</CardDescription>
            </CardHeader>
            <CardContent className="h-[300px]">
              <ResponsiveContainer height="100%" width="100%">
                <PieChart>
                  <Pie
                    cx="50%"
                    cy="50%"
                    data={productCategoryData}
                    dataKey="value"
                    fill="#82ca9d"
                    labelLine={false}
                    outerRadius={80}
                  >
                    {productCategoryData.map((entry, index) => (
                      <Cell
                        key={`cell-${index}`}
                        fill={COLORS[index % COLORS.length]}
                      />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </div>

        <Card className="mb-6 rounded-xl">
          <CardHeader>
            <CardTitle className="text-xl">City Distribution</CardTitle>
            <CardDescription>Top 10 cities by transactions</CardDescription>
          </CardHeader>
          <CardContent className="h-[400px]">
            <ResponsiveContainer height="100%" width="100%">
              <BarChart
                data={cityDistributionData}
                layout="vertical"
                margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
              >
                <XAxis type="number" />
                <YAxis dataKey="name" type="category" width={120} />
                <CartesianGrid strokeDasharray="3 3" />
                <Tooltip />
                <Bar dataKey="value" fill="#8884d8" />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        <Card className="mb-6 rounded-xl">
          <CardHeader>
            <CardTitle className="text-xl">
              Payment Method Distribution
            </CardTitle>
            <CardDescription>Distribution of payment methods</CardDescription>
          </CardHeader>
          <CardContent className="h-[400px]">
            <ResponsiveContainer height="100%" width="100%">
              <BarChart
                data={paymentMethodData}
                layout="vertical"
                margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
              >
                <XAxis type="number" />
                <YAxis dataKey="name" type="category" width={120} />
                <CartesianGrid strokeDasharray="3 3" />
                <Tooltip />
                <Bar dataKey="value" fill="#82ca9d" />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        <AIQueryComponent />
      </div>
    </div>
  );
};

export default Dashboard;
