"use client";

import React, { useEffect, useState } from "react";
import { CreditCard, DollarSign, MapPin, ShoppingBag } from "lucide-react";
import Papa from "papaparse";
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

  useEffect(() => {
    Papa.parse("/retail_data.csv", {
      header: true,
      download: true,
      skipEmptyLines: true,
      delimiter: ",",
      complete: (results: Papa.ParseResult<TransactionData>) => {
        setValues(results.data);
      },
    });
  }, []);

  return values;
};

const Dashboard: React.FC = () => {
  const csvData = useReadCSV();
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
  const [totalTransactions, setTotalTransactions] = useState(0);

  useEffect(() => {
    if (csvData.length > 0) {
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
      const processedCityData = processDataForBarChart(csvData, "City");

      setCityDistributionData(processedCityData);
      setTotalTransactions(csvData.length);
    }
  }, [csvData, timePeriod]);

  const processDataByTimePeriod = (
    data: TransactionData[],
    period: "month" | "week" | "year"
  ) => {
    const salesByPeriod: { [key: string]: number } = {};

    data.forEach((transaction) => {
      const date = new Date(transaction.Date);
      let key: string;

      switch (period) {
        case "week":
          key = `${date.getFullYear()}-W${getWeekNumber(date)}`;
          break;
        case "month":
          key = `${date.getFullYear()}-${(date.getMonth() + 1)
            .toString()
            .padStart(2, "0")}`;
          break;
        case "year":
          key = date.getFullYear().toString();
          break;
      }

      const cost = parseFloat(transaction.Total_Cost);

      salesByPeriod[key] = (salesByPeriod[key] || 0) + cost;
    });

    return Object.entries(salesByPeriod)
      .map(([date, sales]) => ({ date, sales }))
      .sort((a, b) => a.date.localeCompare(b.date));
  };

  const processDataForPieChart = (
    data: TransactionData[],
    key: "Store_Type" | "Product"
  ) => {
    const counts: { [key: string]: number } = {};

    data.forEach((transaction) => {
      counts[transaction[key]] = (counts[transaction[key]] || 0) + 1;
    });

    return Object.entries(counts)
      .map(([name, value], index) => ({
        name,
        value,
        fill: COLORS[index % COLORS.length],
      }))
      .sort((a, b) => b.value - a.value)
      .slice(0, 5); // Top 5
  };

  const processDataForBarChart = (data: TransactionData[], key: "City") => {
    const counts: { [key: string]: number } = {};

    data.forEach((transaction) => {
      counts[transaction[key]] = (counts[transaction[key]] || 0) + 1;
    });

    return Object.entries(counts)
      .map(([name, value]) => ({ name, value }))
      .sort((a, b) => b.value - a.value)
      .slice(0, 10); // Top 10 cities
  };

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

  return (
    <div className="min-h-screen bg-gray-100 dark:bg-gray-900 ">
      <div className="absolute inset-0 overflow-hidden">
        {/* <div className="absolute -top-1/4 -left-1/4 w-1/2 h-1/2 bg-indigo-700 rounded-full filter blur-[100px] opacity-30 animate-pulse"></div> */}
        {/* <div className="absolute -bottom-1/4 -right-1/4 w-1/2 h-1/2 bg-purple-700 rounded-full filter blur-[100px] opacity-30 animate-pulse"></div> */}
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
              <div className="text-2xl font-bold ">
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
                    <XAxis dataKey="date" tickFormatter={formatXAxis} />
                    <YAxis
                      tickFormatter={(value) => `$${value.toLocaleString()}`}
                    />
                    <CartesianGrid strokeDasharray="3 3" />
                    <Tooltip />
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
                  Loading sales data...
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
                    label
                    cx="50%"
                    cy="50%"
                    data={storeTypeData}
                    dataKey="value"
                    fill="#8884d8"
                    nameKey="name"
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
                    label
                    cx="50%"
                    cy="50%"
                    data={productCategoryData}
                    dataKey="value"
                    fill="#82ca9d"
                    nameKey="name"
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

        <Card className="rounded-xl">
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
        <br />
        <AIQueryComponent />
      </div>
    </div>
  );
};

export default Dashboard;
