
import { useState, useEffect } from "react";
import { Activity, Zap, Pause, Play, RefreshCw, Filter } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";
import Header from "@/components/Dashboard/Header";

// Mock real-time data
const generateRealTimeData = () => ({
  timestamp: new Date().toLocaleTimeString(),
  shipments: Math.floor(Math.random() * 1000) + 5000,
  alerts: Math.floor(Math.random() * 20) + 5,
  riskScore: (Math.random() * 10).toFixed(1),
  activeRoutes: Math.floor(Math.random() * 50) + 150,
  suppliers: Math.floor(Math.random() * 100) + 800,
});

const Monitoring = () => {
  const [isLive, setIsLive] = useState(true);
  const [realTimeData, setRealTimeData] = useState([]);
  const [currentMetrics, setCurrentMetrics] = useState(generateRealTimeData());

  useEffect(() => {
    if (!isLive) return;

    const interval = setInterval(() => {
      const newData = generateRealTimeData();
      setCurrentMetrics(newData);
      setRealTimeData(prev => [...prev.slice(-19), newData]);
    }, 2000);

    return () => clearInterval(interval);
  }, [isLive]);

  const liveEvents = [
    {
      id: "1",
      type: "shipment",
      message: "Container MSKU123456 departed Hong Kong Port",
      timestamp: "2 seconds ago",
      severity: "info"
    },
    {
      id: "2", 
      type: "alert",
      message: "Weather warning issued for Pacific Route 7",
      timestamp: "15 seconds ago",
      severity: "warning"
    },
    {
      id: "3",
      type: "resolution",
      message: "Port congestion at Los Angeles resolved",
      timestamp: "1 minute ago",
      severity: "success"
    },
    {
      id: "4",
      type: "disruption",
      message: "Supplier factory in Shanghai reports equipment failure",
      timestamp: "3 minutes ago",
      severity: "error"
    },
    {
      id: "5",
      type: "shipment",
      message: "Bulk cargo vessel entered Rotterdam harbor",
      timestamp: "5 minutes ago", 
      severity: "info"
    }
  ];

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case "error": return "bg-red-500";
      case "warning": return "bg-orange-500";
      case "success": return "bg-green-500";
      default: return "bg-blue-500";
    }
  };

  const getEventIcon = (type: string) => {
    switch (type) {
      case "shipment": return "🚢";
      case "alert": return "⚠️";
      case "resolution": return "✅";
      case "disruption": return "🚨";
      default: return "📋";
    }
  };

  return (
    <div className="min-h-screen bg-gradient-dark font-inter">
      <Header />
      
      <main className="container mx-auto px-6 py-8">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gradient-primary">Live Monitoring</h1>
            <p className="text-muted-foreground mt-2">Real-time supply chain visibility and tracking</p>
          </div>
          
          <div className="flex space-x-4">
            <Button 
              variant={isLive ? "destructive" : "cta"}
              onClick={() => setIsLive(!isLive)}
              className="flex items-center space-x-2"
            >
              {isLive ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4" />}
              <span>{isLive ? "Pause" : "Resume"} Live Feed</span>
            </Button>
            <Button variant="outline" className="flex items-center space-x-2">
              <Filter className="w-4 h-4" />
              <span>Filters</span>
            </Button>
          </div>
        </div>

        {/* Live Status Indicator */}
        <div className="flex items-center space-x-4 mb-8">
          <div className="flex items-center space-x-2">
            <div className={`w-3 h-3 rounded-full ${isLive ? "bg-green-500 animate-pulse" : "bg-gray-500"}`}></div>
            <span className="text-sm font-medium">
              {isLive ? "Live" : "Paused"} • Updated {isLive ? "now" : "paused"}
            </span>
          </div>
          {isLive && (
            <Button variant="ghost" size="sm" onClick={() => window.location.reload()}>
              <RefreshCw className="w-4 h-4 mr-2" />
              Refresh
            </Button>
          )}
        </div>

        {/* Real-time Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-5 gap-6 mb-8">
          <Card className="glass-card">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-muted-foreground">Active Shipments</p>
                  <p className="text-2xl font-bold text-primary">{currentMetrics.shipments?.toLocaleString()}</p>
                </div>
                <div className="text-2xl">🚢</div>
              </div>
            </CardContent>
          </Card>

          <Card className="glass-card">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-muted-foreground">Live Alerts</p>
                  <p className="text-2xl font-bold text-orange-500">{currentMetrics.alerts}</p>
                </div>
                <div className="text-2xl">🚨</div>
              </div>
            </CardContent>
          </Card>

          <Card className="glass-card">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-muted-foreground">Risk Score</p>
                  <p className="text-2xl font-bold text-red-500">{currentMetrics.riskScore}</p>
                </div>
                <div className="text-2xl">⚡</div>
              </div>
            </CardContent>
          </Card>

          <Card className="glass-card">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-muted-foreground">Active Routes</p>
                  <p className="text-2xl font-bold text-blue-500">{currentMetrics.activeRoutes}</p>
                </div>
                <div className="text-2xl">🗺️</div>
              </div>
            </CardContent>
          </Card>

          <Card className="glass-card">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-muted-foreground">Connected Suppliers</p>
                  <p className="text-2xl font-bold text-green-500">{currentMetrics.suppliers}</p>
                </div>
                <div className="text-2xl">🏭</div>
              </div>
            </CardContent>
          </Card>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Live Event Feed */}
          <div className="lg:col-span-2">
            <Card className="glass-card">
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Activity className="w-5 h-5 text-accent" />
                  <span>Live Event Stream</span>
                  {isLive && <Badge variant="outline" className="bg-green-500/10 text-green-500 border-green-500/20">Live</Badge>}
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4 max-h-96 overflow-y-auto">
                  {liveEvents.map((event) => (
                    <div key={event.id} className="flex items-start space-x-4 p-4 rounded-lg glass-panel">
                      <div className="flex items-center space-x-2">
                        <span className="text-lg">{getEventIcon(event.type)}</span>
                        <div className={`w-2 h-2 rounded-full ${getSeverityColor(event.severity)}`}></div>
                      </div>
                      <div className="flex-1">
                        <p className="text-foreground">{event.message}</p>
                        <p className="text-xs text-muted-foreground mt-1">{event.timestamp}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Real-time Chart */}
            <Card className="glass-card mt-6">
              <CardHeader>
                <CardTitle>Real-time Risk Score</CardTitle>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <LineChart data={realTimeData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                    <XAxis dataKey="timestamp" stroke="#9ca3af" />
                    <YAxis stroke="#9ca3af" />
                    <Tooltip 
                      contentStyle={{ 
                        backgroundColor: '#1f2937', 
                        border: '1px solid #374151',
                        borderRadius: '8px'
                      }} 
                    />
                    <Line 
                      type="monotone" 
                      dataKey="riskScore" 
                      stroke="#ef4444" 
                      strokeWidth={2}
                      dot={{ fill: '#ef4444', strokeWidth: 2, r: 4 }}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </div>

          {/* System Health */}
          <div className="lg:col-span-1 space-y-6">
            <Card className="glass-card">
              <CardHeader>
                <CardTitle>System Health</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex items-center justify-between">
                  <span className="text-sm">API Status</span>
                  <Badge className="bg-green-500">Operational</Badge>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm">Data Pipeline</span>
                  <Badge className="bg-green-500">Healthy</Badge>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm">AI Agents</span>
                  <Badge className="bg-green-500">Active</Badge>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm">External APIs</span>
                  <Badge className="bg-orange-500">Partial</Badge>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm">Database</span>
                  <Badge className="bg-green-500">Online</Badge>
                </div>
              </CardContent>
            </Card>

            <Card className="glass-card">
              <CardHeader>
                <CardTitle>Quick Actions</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <Button variant="outline" className="w-full justify-start">
                  <Zap className="w-4 h-4 mr-2" />
                  Trigger Alert Test
                </Button>
                <Button variant="outline" className="w-full justify-start">
                  <RefreshCw className="w-4 h-4 mr-2" />
                  Refresh All Data
                </Button>
                <Button variant="outline" className="w-full justify-start">
                  <Activity className="w-4 h-4 mr-2" />
                  Export Live Data
                </Button>
              </CardContent>
            </Card>

            <Card className="glass-card">
              <CardHeader>
                <CardTitle>Data Sources</CardTitle>
              </CardHeader>
              <CardContent className="space-y-2">
                <div className="flex items-center justify-between text-sm">
                  <span>Weather API</span>
                  <div className="w-2 h-2 rounded-full bg-green-500"></div>
                </div>
                <div className="flex items-center justify-between text-sm">
                  <span>Traffic Data</span>
                  <div className="w-2 h-2 rounded-full bg-green-500"></div>
                </div>
                <div className="flex items-center justify-between text-sm">
                  <span>Port Systems</span>
                  <div className="w-2 h-2 rounded-full bg-orange-500"></div>
                </div>
                <div className="flex items-center justify-between text-sm">
                  <span>Supplier APIs</span>
                  <div className="w-2 h-2 rounded-full bg-green-500"></div>
                </div>
                <div className="flex items-center justify-between text-sm">
                  <span>Shipping Tracking</span>
                  <div className="w-2 h-2 rounded-full bg-green-500"></div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </main>
    </div>
  );
};

export default Monitoring;
