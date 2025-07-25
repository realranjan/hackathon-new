import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { BarChart, Bar, XAxis, YAxis, ResponsiveContainer, LineChart, Line, PieChart, Pie, Cell, AreaChart, Area } from "recharts";
import { TrendingUp, AlertTriangle, DollarSign, Package, Truck, Clock } from "lucide-react";
import { Button } from "@/components/ui/button";

const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

const AnalyticsDashboard = () => {
  const [kpis, setKpis] = useState<any>(null);
  const [riskData, setRiskData] = useState<any[]>([]);
  const [portPerformance, setPortPerformance] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchAnalytics = () => {
    setLoading(true);
    Promise.all([
      fetch(`${API_BASE}/analytics/kpis/`).then(res => res.json()),
      fetch(`${API_BASE}/analytics/risk_trends/`).then(res => res.json()),
      fetch(`${API_BASE}/analytics/port_performance/`).then(res => res.json()),
    ]).then(([kpisData, riskTrendsData, portPerfData]) => {
      setKpis(kpisData);
      setRiskData(riskTrendsData.riskData || []);
      setPortPerformance(portPerfData.ports || []);
      setLoading(false);
    }).catch(() => {
      setError("Failed to load analytics");
      setLoading(false);
    });
  };

  useEffect(() => {
    fetchAnalytics();
    const interval = setInterval(fetchAnalytics, 10000); // auto-refresh every 10s
    return () => clearInterval(interval);
  }, []);

  if (loading) return <div>Loading analytics...</div>;
  if (error) return <div>{error}</div>;

const riskCategories = [
  { name: "Weather", value: 35, color: "#3B82F6" },
  { name: "Geopolitical", value: 25, color: "#EF4444" },
  { name: "Infrastructure", value: 20, color: "#F59E0B" },
  { name: "Labor", value: 15, color: "#10B981" },
  { name: "Cyber", value: 5, color: "#8B5CF6" }
];

const shipmentVolume = [
  { month: "Jan", volume: 1200, forecast: 1150 },
  { month: "Feb", volume: 1100, forecast: 1200 },
  { month: "Mar", volume: 1350, forecast: 1300 },
  { month: "Apr", volume: 1450, forecast: 1400 },
  { month: "May", volume: 1320, forecast: 1380 },
  { month: "Jun", volume: 1580, forecast: 1520 }
];

  // Defensive: filter out invalid/empty data for charts
  const safeRiskData = Array.isArray(riskData) && riskData.length > 0 && riskData.every(d => typeof d.incidents === 'number' && typeof d.resolved === 'number') ? riskData : null;
  const safePortPerformance = Array.isArray(portPerformance) && portPerformance.length > 0 && portPerformance.every(d => typeof d.efficiency === 'number' && typeof d.capacity === 'number') ? portPerformance : null;

  return (
    <div className="space-y-6">
      <div className="flex justify-end mb-2">
        <Button size="sm" variant="outline" onClick={fetchAnalytics}>Refresh</Button>
      </div>
      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card className="card-maritime">
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-2xl font-bold text-foreground">{kpis?.cost_savings ? `$${(kpis.cost_savings/1e6).toFixed(1)}M` : "—"}</div>
                <div className="text-sm text-muted-foreground">Cost Savings</div>
                <div className="flex items-center gap-1 mt-1">
                  <TrendingUp className="h-3 w-3 text-success" />
                  <span className="text-xs text-success">+12.5%</span>
                </div>
              </div>
              <div className="p-2 rounded-lg bg-muted">
                <DollarSign className="h-5 w-5 text-primary" />
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="card-maritime">
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-2xl font-bold text-foreground">{kpis?.active_shipments ?? "—"}</div>
                <div className="text-sm text-muted-foreground">Active Shipments</div>
                <div className="flex items-center gap-1 mt-1">
                  <Badge variant="secondary" className="text-xs">Real-time</Badge>
                </div>
              </div>
              <div className="p-2 rounded-lg bg-muted">
                <Package className="h-5 w-5 text-primary" />
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="card-maritime">
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-2xl font-bold text-foreground">23</div>
                <div className="text-sm text-muted-foreground">Risk Alerts</div>
                <div className="flex items-center gap-1 mt-1">
                  <div className="w-2 h-2 rounded-full bg-warning animate-pulse" />
                  <span className="text-xs text-warning">5 Critical</span>
                </div>
              </div>
              <div className="p-2 rounded-lg bg-muted">
                <AlertTriangle className="h-5 w-5 text-warning" />
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="card-maritime">
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-2xl font-bold text-foreground">94.7%</div>
                <div className="text-sm text-muted-foreground">On-Time Delivery</div>
                <div className="flex items-center gap-1 mt-1">
                  <TrendingUp className="h-3 w-3 text-success" />
                  <span className="text-xs text-success">+2.1%</span>
                </div>
              </div>
              <div className="p-2 rounded-lg bg-muted">
                <Truck className="h-5 w-5 text-success" />
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Risk Incidents Trend */}
        <Card className="card-maritime">
          <CardHeader>
            <CardTitle className="text-lg">Risk Incidents Trend</CardTitle>
          </CardHeader>
          <CardContent>
            {safeRiskData ? (
              <ResponsiveContainer width="100%" height={250}>
                <BarChart data={safeRiskData}>
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Bar dataKey="incidents" fill="hsl(var(--primary))" radius={[4, 4, 0, 0]} />
                  <Bar dataKey="resolved" fill="hsl(var(--success))" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <div className="text-muted-foreground text-center">No risk trend data available.</div>
            )}
          </CardContent>
        </Card>

        {/* Risk Categories */}
        <Card className="card-maritime">
          <CardHeader>
            <CardTitle className="text-lg">Risk Distribution</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={250}>
              <PieChart>
                <Pie
                  data={riskCategories}
                  cx="50%"
                  cy="50%"
                  outerRadius={80}
                  dataKey="value"
                  label={({ name, value }) => `${name}: ${value}%`}
                >
                  {riskCategories.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
              </PieChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Port Performance */}
        <Card className="card-maritime">
          <CardHeader>
            <CardTitle className="text-lg">Port Performance Metrics</CardTitle>
          </CardHeader>
          <CardContent>
            {safePortPerformance ? (
              <ResponsiveContainer width="100%" height={250}>
                <BarChart data={safePortPerformance} layout="horizontal">
                  <XAxis type="number" domain={[0, 100]} />
                  <YAxis dataKey="port" type="category" width={80} />
                  <Bar dataKey="efficiency" fill="hsl(var(--primary))" radius={[0, 4, 4, 0]} />
                  <Bar dataKey="capacity" fill="hsl(var(--accent))" radius={[0, 4, 4, 0]} />
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <div className="text-muted-foreground text-center">No port performance data available.</div>
            )}
          </CardContent>
        </Card>

        {/* Shipment Volume Forecast */}
        <Card className="card-maritime">
          <CardHeader>
            <CardTitle className="text-lg">Shipment Volume & Forecast</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={250}>
              <AreaChart data={shipmentVolume}>
                <XAxis dataKey="month" />
                <YAxis />
                <Area
                  type="monotone"
                  dataKey="volume"
                  stackId="1"
                  stroke="hsl(var(--primary))"
                  fill="hsl(var(--primary))"
                  fillOpacity={0.6}
                />
                <Area
                  type="monotone"
                  dataKey="forecast"
                  stackId="2"
                  stroke="hsl(var(--accent))"
                  fill="hsl(var(--accent))"
                  fillOpacity={0.3}
                  strokeDasharray="5 5"
                />
              </AreaChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default AnalyticsDashboard;