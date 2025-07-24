import { useState } from "react";
import { MapPin, Navigation, Layers, Filter, Search, Zap, Globe } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import Header from "@/components/Dashboard/Header";
import Globe3D from "@/components/Map3D/Globe3D";

// Mock map data
const supplyChainNodes = [
  {
    id: "1",
    type: "supplier",
    name: "FOXCONN Manufacturing",
    location: "Shenzhen, China",
    coordinates: { lat: 22.5431, lng: 114.0579 },
    status: "operational",
    risk: "medium",
    capacity: 85,
    activeOrders: 234
  },
  {
    id: "2", 
    type: "port",
    name: "Port of Hong Kong",
    location: "Hong Kong",
    coordinates: { lat: 22.3193, lng: 114.1694 },
    status: "disrupted",
    risk: "high",
    capacity: 45,
    activeOrders: 156
  },
  {
    id: "3",
    type: "warehouse",
    name: "Amazon Fulfillment Center",
    location: "Los Angeles, USA",
    coordinates: { lat: 34.0522, lng: -118.2437 },
    status: "operational",
    risk: "low",
    capacity: 92,
    activeOrders: 89
  },
  {
    id: "4",
    type: "supplier",
    name: "Samsung Electronics",
    location: "Seoul, South Korea",
    coordinates: { lat: 37.5665, lng: 126.9780 },
    status: "operational",
    risk: "low",
    capacity: 95,
    activeOrders: 445
  },
  {
    id: "5",
    type: "port",
    name: "Port of Rotterdam",
    location: "Rotterdam, Netherlands",
    coordinates: { lat: 51.9244, lng: 4.4777 },
    status: "warning",
    risk: "medium",
    capacity: 78,
    activeOrders: 267
  }
];

const tradeRoutes = [
  {
    id: "1",
    name: "Asia-Pacific Corridor",
    from: "Hong Kong",
    to: "Los Angeles",
    status: "active",
    shipments: 156,
    avgTransitTime: "14 days",
    riskLevel: "medium"
  },
  {
    id: "2",
    name: "Trans-Pacific Route",
    from: "Seoul",
    to: "Seattle",
    status: "delayed",
    shipments: 89,
    avgTransitTime: "16 days",
    riskLevel: "high"
  },
  {
    id: "3",
    name: "Transatlantic Corridor",
    from: "Rotterdam",
    to: "New York",
    status: "active",
    shipments: 234,
    avgTransitTime: "10 days",
    riskLevel: "low"
  }
];

const Map = () => {
  const [selectedNode, setSelectedNode] = useState<any>(null);
  const [mapView, setMapView] = useState("3d-globe");
  const [filterType, setFilterType] = useState("all");

  const handlePointClick = (data: any) => {
    setSelectedNode(data);
    console.log("Selected supply chain point:", data);
  };

  const statusColors = {
    operational: "bg-green-500",
    warning: "bg-orange-500", 
    disrupted: "bg-red-500"
  };

  const riskColors = {
    low: "text-green-500",
    medium: "text-orange-500",
    high: "text-red-500"
  };

  const typeIcons = {
    supplier: "🏭",
    port: "⚓",
    warehouse: "📦",
    distribution: "🚚"
  };

  const filteredNodes = supplyChainNodes.filter(node => 
    filterType === "all" || node.type === filterType
  );

  return (
    <div className="min-h-screen bg-gradient-dark font-inter">
      <Header />
      
      <main className="container mx-auto px-6 py-8">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gradient-primary">3D Supply Chain Map</h1>
            <p className="text-muted-foreground mt-2">Interactive 3D visualization of global supply network with real-time disruption tracking</p>
          </div>
          
          <div className="flex space-x-4">
            <Button variant="outline" className="flex items-center space-x-2">
              <Layers className="w-4 h-4" />
              <span>View Options</span>
            </Button>
            <Button variant="cta">
              <Globe className="w-4 h-4 mr-2" />
              3D Globe View
            </Button>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Map Controls */}
          <div className="lg:col-span-1 space-y-6">
            <Card className="glass-card">
              <CardHeader>
                <CardTitle className="text-lg">Map Controls</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground w-4 h-4" />
                  <Input placeholder="Search locations..." className="pl-10" />
                </div>
                
                <div>
                  <label className="text-sm font-medium mb-2 block">View Type</label>
                  <select 
                    value={mapView}
                    onChange={(e) => setMapView(e.target.value)}
                    className="w-full px-3 py-2 rounded-lg bg-muted border border-border text-foreground"
                  >
                    <option value="3d-globe">3D Globe View</option>
                    <option value="supply-chain">Supply Chain Network</option>
                    <option value="risk-analysis">Risk Heat Map</option>
                    <option value="trade-routes">Trade Routes</option>
                  </select>
                </div>
                
                <div>
                  <label className="text-sm font-medium mb-2 block">Filter by Status</label>
                  <div className="space-y-2">
                    <Button variant="ghost" className="w-full justify-start">
                      <div className="w-3 h-3 rounded-full bg-green-500 mr-2"></div>
                      Operational (3)
                    </Button>
                    <Button variant="ghost" className="w-full justify-start">
                      <div className="w-3 h-3 rounded-full bg-orange-500 mr-2"></div>
                      Warning (1)
                    </Button>
                    <Button variant="ghost" className="w-full justify-start">
                      <div className="w-3 h-3 rounded-full bg-red-500 mr-2"></div>
                      Disrupted (1)
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Legend */}
            <Card className="glass-card">
              <CardHeader>
                <CardTitle className="text-lg">Live Data</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-sm">Active Ports</span>
                    <Badge className="bg-primary">5</Badge>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm">Total Shipments</span>
                    <Badge className="bg-secondary">880</Badge>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm">At Risk</span>
                    <Badge className="bg-destructive">156</Badge>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm">Avg Risk Score</span>
                    <Badge className="bg-orange-500">7.2</Badge>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Interactive Controls */}
            <Card className="glass-card">
              <CardHeader>
                <CardTitle className="text-lg">3D Controls</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="text-xs text-muted-foreground space-y-1">
                  <div>🖱️ Click & Drag: Rotate globe</div>
                  <div>🔍 Scroll: Zoom in/out</div>
                  <div>📍 Click Points: View details</div>
                  <div>🔄 Auto-rotate: Enabled</div>
                </div>
                <Button variant="outline" size="sm" className="w-full">
                  <Zap className="w-4 h-4 mr-2" />
                  Reset View
                </Button>
              </CardContent>
            </Card>
          </div>

          {/* 3D Map Visualization */}
          <div className="lg:col-span-3">
            <Card className="glass-card h-[700px]">
              <CardContent className="p-0 h-full">
                <Globe3D onPointClick={handlePointClick} />
              </CardContent>
            </Card>
          </div>
        </div>

        {/* Selected Node Details */}
        {selectedNode && (
          <Card className="glass-card mt-6">
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <MapPin className="w-5 h-5 text-accent" />
                <span>{selectedNode.name}</span>
                <Badge 
                  className={
                    selectedNode.status === "operational" ? "bg-green-500" :
                    selectedNode.status === "warning" ? "bg-orange-500" : "bg-red-500"
                  }
                >
                  {selectedNode.status}
                </Badge>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                <div>
                  <h4 className="font-medium mb-2">Location</h4>
                  <p className="text-muted-foreground">{selectedNode.country}</p>
                </div>
                <div>
                  <h4 className="font-medium mb-2">Active Shipments</h4>
                  <p className="text-2xl font-bold text-primary">{selectedNode.shipments}</p>
                </div>
                <div>
                  <h4 className="font-medium mb-2">Risk Level</h4>
                  <Badge className={
                    selectedNode.risk === "low" ? "bg-green-500" :
                    selectedNode.risk === "medium" ? "bg-orange-500" : "bg-red-500"
                  }>
                    {selectedNode.risk.toUpperCase()}
                  </Badge>
                </div>
                <div>
                  <h4 className="font-medium mb-2">Status</h4>
                  <p className="text-sm text-muted-foreground">{selectedNode.description}</p>
                </div>
              </div>
            </CardContent>
          </Card>
        )}
      </main>
    </div>
  );
};

export default Map;
