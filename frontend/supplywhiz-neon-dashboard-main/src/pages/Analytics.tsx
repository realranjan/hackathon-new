
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { BarChart3, TrendingUp, TrendingDown, Download, Calendar } from "lucide-react";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, LineChart, Line, PieChart, Pie, Cell, Area, AreaChart } from "recharts";
import Header from "@/components/Dashboard/Header";

const eventTypesData = [
  { name: "Weather", value: 45, color: "#3b82f6" },
  { name: "Traffic", value: 23, color: "#f59e0b" },
  { name: "Supplier", value: 67, color: "#ef4444" },
  { name: "Port", value: 34, color: "#8b5cf6" },
  { name: "Geopolitical", value: 12, color: "#06b6d4" },
  { name: "Cyber", value: 8, color: "#f97316" },
];

const riskScoreData = [
  { month: "Jan", score: 3.2, incidents: 23 },
  { month: "Feb", score: 4.1, incidents: 34 },
  { month: "Mar", score: 3.8, incidents: 28 },
  { month: "Apr", score: 5.2, incidents: 45 },
  { month: "May", score: 4.7, incidents: 39 },
  { month: "Jun", score: 6.1, incidents: 52 },
  { month: "Jul", score: 5.8, incidents: 48 },
];

const vendorImpactData = [
  { name: "Low Impact", value: 156, color: "#22c55e" },
  { name: "Medium Impact", value: 89, color: "#f59e0b" },
  { name: "High Impact", value: 34, color: "#ef4444" },
  { name: "Critical Impact", value: 12, color: "#7c2d12" },
];

const performanceData = [
  { metric: "On-Time Delivery", current: 94.2, target: 95.0, trend: "up" },
  { metric: "Cost Efficiency", current: 87.5, target: 85.0, trend: "up" },
  { metric: "Supplier Reliability", current: 91.8, target: 90.0, trend: "up" },
  { metric: "Risk Mitigation", current: 88.3, target: 92.0, trend: "down" },
];

const regionData = [
  { region: "North America", alerts: 89, resolved: 76, pending: 13 },
  { region: "Europe", alerts: 67, resolved: 54, pending: 13 },
  { region: "Asia-Pacific", alerts: 134, resolved: 98, pending: 36 },
  { region: "Latin America", alerts: 23, resolved: 19, pending: 4 },
  { region: "Middle East", alerts: 45, resolved: 32, pending: 13 },
  { region: "Africa", alerts: 12, resolved: 8, pending: 4 },
];

const Analytics = () => {
  return (
    <div className="min-h-screen bg-gradient-dark font-inter">
      <Header />
      
      <main className="container mx-auto px-6 py-8">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gradient-primary">Analytics Dashboard</h1>
            <p className="text-muted-foreground mt-2">Deep insights into supply chain performance and risks</p>
          </div>
          
          <div className="flex space-x-4">
            <Button variant="outline" className="flex items-center space-x-2">
              <Calendar className="w-4 h-4" />
              <span>Time Range</span>
            </Button>
            <Button variant="outline" className="flex items-center space-x-2">
              <Download className="w-4 h-4" />
              <span>Export Report</span>
            </Button>
          </div>
        </div>

        {/* KPI Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          {performanceData.map((item, index) => (
            <Card key={index} className="glass-card">
              <CardContent className="p-6">
                <div className="flex items-center justify-between mb-2">
                  <h3 className="text-sm font-medium text-muted-foreground">{item.metric}</h3>
                  {item.trend === "up" ? (
                    <TrendingUp className="w-4 h-4 text-green-500" />
                  ) : (
                    <TrendingDown className="w-4 h-4 text-red-500" />
                  )}
                </div>
                <div className="flex items-baseline space-x-3">
                  <span className="text-2xl font-bold text-primary">{item.current}%</span>
                  <span className="text-sm text-muted-foreground">Target: {item.target}%</span>
                </div>
                <div className="mt-2">
                  <div className="w-full bg-muted rounded-full h-2">
                    <div 
                      className={`h-2 rounded-full ${item.trend === "up" ? "bg-green-500" : "bg-red-500"}`}
                      style={{ width: `${(item.current / item.target) * 100}%` }}
                    />
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Charts Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          {/* Event Types Distribution */}
          <Card className="glass-card">
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <BarChart3 className="w-5 h-5 text-accent" />
                <span>Event Types Distribution</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={eventTypesData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                  <XAxis dataKey="name" stroke="#9ca3af" />
                  <YAxis stroke="#9ca3af" />
                  <Tooltip 
                    contentStyle={{ 
                      backgroundColor: '#1f2937', 
                      border: '1px solid #374151',
                      borderRadius: '8px'
                    }} 
                  />
                  <Bar dataKey="value" fill="#22c55e" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>

          {/* Risk Score Trend */}
          <Card className="glass-card">
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <TrendingUp className="w-5 h-5 text-secondary" />
                <span>Risk Score Trend</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <AreaChart data={riskScoreData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                  <XAxis dataKey="month" stroke="#9ca3af" />
                  <YAxis stroke="#9ca3af" />
                  <Tooltip 
                    contentStyle={{ 
                      backgroundColor: '#1f2937', 
                      border: '1px solid #374151',
                      borderRadius: '8px'
                    }} 
                  />
                  <Area 
                    type="monotone" 
                    dataKey="score" 
                    stroke="#f59e0b" 
                    fill="#f59e0b" 
                    fillOpacity={0.3}
                  />
                </AreaChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </div>

        {/* Second Row Charts */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          {/* Vendor Impact */}
          <Card className="glass-card">
            <CardHeader>
              <CardTitle>Vendor Impact Analysis</CardTitle>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={vendorImpactData}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {vendorImpactData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip 
                    contentStyle={{ 
                      backgroundColor: '#1f2937', 
                      border: '1px solid #374151',
                      borderRadius: '8px'
                    }} 
                  />
                </PieChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>

          {/* Regional Performance */}
          <Card className="glass-card">
            <CardHeader>
              <CardTitle>Regional Alert Distribution</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {regionData.map((region, index) => (
                  <div key={index} className="flex items-center justify-between p-4 rounded-lg bg-muted/20">
                    <div className="flex-1">
                      <div className="flex items-center justify-between mb-2">
                        <span className="font-medium">{region.region}</span>
                        <Badge variant="outline">{region.alerts} total</Badge>
                      </div>
                      <div className="flex space-x-4 text-sm">
                        <span className="text-green-500">Resolved: {region.resolved}</span>
                        <span className="text-orange-500">Pending: {region.pending}</span>
                      </div>
                      <div className="mt-2 w-full bg-muted rounded-full h-2">
                        <div 
                          className="h-2 bg-green-500 rounded-full"
                          style={{ width: `${(region.resolved / region.alerts) * 100}%` }}
                        />
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Detailed Metrics Table */}
        <Card className="glass-card">
          <CardHeader>
            <CardTitle>Monthly Performance Metrics</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-border">
                    <th className="text-left p-4">Month</th>
                    <th className="text-left p-4">Risk Score</th>
                    <th className="text-left p-4">Total Incidents</th>
                    <th className="text-left p-4">Avg Resolution Time</th>
                    <th className="text-left p-4">Cost Impact</th>
                    <th className="text-left p-4">Efficiency Score</th>
                  </tr>
                </thead>
                <tbody>
                  {riskScoreData.map((month, index) => (
                    <tr key={index} className="border-b border-border/50">
                      <td className="p-4 font-medium">{month.month}</td>
                      <td className="p-4">
                        <Badge 
                          className={month.score > 5 ? "bg-red-500" : month.score > 3 ? "bg-orange-500" : "bg-green-500"}
                        >
                          {month.score}
                        </Badge>
                      </td>
                      <td className="p-4">{month.incidents}</td>
                      <td className="p-4">{Math.floor(Math.random() * 24) + 12}h</td>
                      <td className="p-4">${(Math.random() * 50000 + 10000).toFixed(0)}</td>
                      <td className="p-4">{(Math.random() * 20 + 80).toFixed(1)}%</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </CardContent>
        </Card>
      </main>
    </div>
  );
};

export default Analytics;
