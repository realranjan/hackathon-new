
import { useState } from "react";
import { AlertTriangle, Clock, MapPin, Filter, Search, Download } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import Header from "@/components/Dashboard/Header";
import ActionPlanPanel from "@/components/Dashboard/ActionPlanPanel";

interface Alert {
  id: string;
  type: "Weather" | "Traffic" | "Supplier" | "Port" | "Geopolitical" | "Cyber" | "Economic";
  title: string;
  location: string;
  severity: "critical" | "high" | "medium" | "low";
  time: string;
  description: string;
  impact: string;
  status: "active" | "resolved" | "investigating";
  affectedRoutes: string[];
  estimatedResolution: string;
}

const mockAlertsData: Alert[] = [
  {
    id: "1",
    type: "Weather",
    title: "Severe Storm Warning",
    location: "Hong Kong Port",
    severity: "critical",
    time: "2 min ago",
    description: "Typhoon Saola approaching major shipping routes with winds up to 185 km/h",
    impact: "37 shipments delayed, 12 vessels diverted",
    status: "active",
    affectedRoutes: ["Asia-Pacific Corridor", "Trans-Pacific Route"],
    estimatedResolution: "72 hours"
  },
  {
    id: "2",
    type: "Supplier",
    title: "Factory Shutdown",
    location: "Shanghai, China",
    severity: "high",
    time: "15 min ago",
    description: "Key electronics supplier FOXCONN experiencing power grid failure",
    impact: "12 suppliers affected, 23,000 units delayed",
    status: "investigating",
    affectedRoutes: ["China-US Corridor", "Intra-Asia Network"],
    estimatedResolution: "48 hours"
  },
  {
    id: "3",
    type: "Traffic",
    title: "Highway Closure",
    location: "I-95 Virginia",
    severity: "medium",
    time: "1 hour ago",
    description: "Multi-vehicle accident blocking all northbound lanes",
    impact: "8 deliveries delayed, 2 hours average delay",
    status: "active",
    affectedRoutes: ["East Coast Corridor"],
    estimatedResolution: "6 hours"
  },
  {
    id: "4",
    type: "Port",
    title: "Container Backlog",
    location: "Port of Los Angeles",
    severity: "medium",
    time: "2 hours ago",
    description: "Increased container volume due to diverted vessels from Long Beach",
    impact: "23 shipments queued, 48-hour processing delay",
    status: "active",
    affectedRoutes: ["Pacific Trade Lane", "West Coast Network"],
    estimatedResolution: "96 hours"
  },
  {
    id: "5",
    type: "Geopolitical",
    title: "Trade Sanctions Announced",
    location: "European Union",
    severity: "high",
    time: "4 hours ago",
    description: "New sanctions affecting technology imports from select regions",
    impact: "156 shipments under review, customs delays expected",
    status: "investigating",
    affectedRoutes: ["EU-Asia Corridor", "Transatlantic Route"],
    estimatedResolution: "168 hours"
  },
  {
    id: "6",
    type: "Cyber",
    title: "Ransomware Attack",
    location: "Singapore Hub",
    severity: "critical",
    time: "6 hours ago",
    description: "Major logistics provider systems compromised, operations halted",
    impact: "89 shipments stuck in transit, tracking unavailable",
    status: "active",
    affectedRoutes: ["Southeast Asia Network", "Singapore-Australia Route"],
    estimatedResolution: "120 hours"
  },
  {
    id: "7",
    type: "Economic",
    title: "Currency Fluctuation",
    location: "Global Markets",
    severity: "low",
    time: "8 hours ago",
    description: "USD strengthening causing procurement cost increases",
    impact: "Contract renegotiations needed for 34 suppliers",
    status: "active",
    affectedRoutes: ["All International Routes"],
    estimatedResolution: "240 hours"
  }
];

const severityConfig = {
  critical: {
    className: "border-l-red-500 bg-red-500/10",
    badge: "bg-red-500 text-white",
    icon: "🔴"
  },
  high: {
    className: "border-l-orange-500 bg-orange-500/10",
    badge: "bg-orange-500 text-white",
    icon: "🟠"
  },
  medium: {
    className: "border-l-yellow-500 bg-yellow-500/10",
    badge: "bg-yellow-500 text-black",
    icon: "🟡"
  },
  low: {
    className: "border-l-green-500 bg-green-500/10",
    badge: "bg-green-500 text-white",
    icon: "🟢"
  }
};

const typeIcons = {
  Weather: "🌪️",
  Traffic: "🚦",
  Supplier: "🏭",
  Port: "⚓",
  Geopolitical: "🌍",
  Cyber: "🔒",
  Economic: "💱"
};

const Alerts = () => {
  const [alerts] = useState<Alert[]>(mockAlertsData);
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedSeverity, setSelectedSeverity] = useState<string>("all");
  const [selectedAlert, setSelectedAlert] = useState<Alert | null>(null);
  const [showActionPlan, setShowActionPlan] = useState(false);

  const filteredAlerts = alerts.filter(alert => {
    const matchesSearch = alert.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         alert.location.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesSeverity = selectedSeverity === "all" || alert.severity === selectedSeverity;
    return matchesSearch && matchesSeverity;
  });

  const handleAlertClick = (alert: Alert) => {
    setSelectedAlert(alert);
    setShowActionPlan(true);
  };

  return (
    <div className="min-h-screen bg-gradient-dark font-inter">
      <Header />
      
      <main className="container mx-auto px-6 py-8">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gradient-primary">Alert Management</h1>
            <p className="text-muted-foreground mt-2">Monitor and respond to supply chain disruptions</p>
          </div>
          
          <div className="flex space-x-4">
            <Button variant="outline" className="flex items-center space-x-2">
              <Download className="w-4 h-4" />
              <span>Export</span>
            </Button>
            <Button variant="cta">
              <AlertTriangle className="w-4 h-4 mr-2" />
              Create Alert
            </Button>
          </div>
        </div>

        {/* Filters */}
        <Card className="glass-card mb-6">
          <CardContent className="p-6">
            <div className="flex flex-col md:flex-row gap-4">
              <div className="flex-1">
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground w-4 h-4" />
                  <Input
                    placeholder="Search alerts..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="pl-10"
                  />
                </div>
              </div>
              
              <div className="flex space-x-4">
                <select
                  value={selectedSeverity}
                  onChange={(e) => setSelectedSeverity(e.target.value)}
                  className="px-4 py-2 rounded-lg bg-muted border border-border text-foreground"
                >
                  <option value="all">All Severities</option>
                  <option value="critical">Critical</option>
                  <option value="high">High</option>
                  <option value="medium">Medium</option>
                  <option value="low">Low</option>
                </select>
                
                <Button variant="outline" size="sm">
                  <Filter className="w-4 h-4 mr-2" />
                  More Filters
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <Card className="glass-card">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-muted-foreground text-sm">Total Alerts</p>
                  <p className="text-2xl font-bold text-primary">{alerts.length}</p>
                </div>
                <div className="text-2xl">🚨</div>
              </div>
            </CardContent>
          </Card>
          
          <Card className="glass-card">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-muted-foreground text-sm">Critical</p>
                  <p className="text-2xl font-bold text-red-500">
                    {alerts.filter(a => a.severity === "critical").length}
                  </p>
                </div>
                <div className="text-2xl">🔴</div>
              </div>
            </CardContent>
          </Card>
          
          <Card className="glass-card">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-muted-foreground text-sm">Active</p>
                  <p className="text-2xl font-bold text-orange-500">
                    {alerts.filter(a => a.status === "active").length}
                  </p>
                </div>
                <div className="text-2xl">⚡</div>
              </div>
            </CardContent>
          </Card>
          
          <Card className="glass-card">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-muted-foreground text-sm">Avg Resolution</p>
                  <p className="text-2xl font-bold text-green-500">24h</p>
                </div>
                <div className="text-2xl">⏱️</div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Alerts List */}
        <div className="space-y-4">
          {filteredAlerts.map((alert) => {
            const config = severityConfig[alert.severity];
            
            return (
              <Card 
                key={alert.id} 
                className={`glass-card border-l-4 cursor-pointer card-hover ${config.className}`}
                onClick={() => handleAlertClick(alert)}
              >
                <CardContent className="p-6">
                  <div className="flex items-start justify-between">
                    <div className="flex items-start space-x-4 flex-1">
                      <div className="text-2xl">{typeIcons[alert.type]}</div>
                      
                      <div className="flex-1">
                        <div className="flex items-center justify-between mb-2">
                          <h3 className="font-semibold text-lg">{alert.title}</h3>
                          <div className="flex items-center space-x-2">
                            <Badge className={config.badge}>
                              {alert.severity.toUpperCase()}
                            </Badge>
                            <Badge variant="outline">
                              {alert.status.toUpperCase()}
                            </Badge>
                          </div>
                        </div>
                        
                        <div className="flex items-center text-sm text-muted-foreground mb-3 space-x-4">
                          <div className="flex items-center">
                            <MapPin className="w-3 h-3 mr-1" />
                            <span>{alert.location}</span>
                          </div>
                          <div className="flex items-center">
                            <Clock className="w-3 h-3 mr-1" />
                            <span>{alert.time}</span>
                          </div>
                        </div>
                        
                        <p className="text-foreground mb-3">{alert.description}</p>
                        <p className="text-accent font-medium mb-3">{alert.impact}</p>
                        
                        <div className="flex flex-wrap gap-2">
                          <span className="text-xs text-muted-foreground">Affected Routes:</span>
                          {alert.affectedRoutes.map((route, idx) => (
                            <Badge key={idx} variant="outline" className="text-xs">
                              {route}
                            </Badge>
                          ))}
                        </div>
                        
                        <div className="mt-3 text-sm">
                          <span className="text-muted-foreground">Est. Resolution: </span>
                          <span className="text-secondary font-medium">{alert.estimatedResolution}</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            );
          })}
        </div>
      </main>

      <ActionPlanPanel 
        isOpen={showActionPlan}
        onClose={() => setShowActionPlan(false)}
        alertTitle={selectedAlert?.title}
      />
    </div>
  );
};

export default Alerts;
