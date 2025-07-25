import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Search, MapPin, Filter, MoreHorizontal, Navigation } from "lucide-react";

const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

const statusColors = {
  normal: "bg-success",
  congested: "bg-warning", 
  strike: "bg-destructive",
  reroute: "bg-primary"
};

const GlobalPortStatus = () => {
  const [ports, setPorts] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);
    fetch(`${API_BASE}/ports/status/`)
      .then(res => res.json())
      .then(data => {
        setPorts(data.ports || []);
        setLoading(false);
      })
      .catch(() => {
        setError("Failed to load port status");
        setLoading(false);
      });
  }, []);

  if (loading) return <div>Loading port status...</div>;
  if (error) return <div>{error}</div>;

  return (
    <Card className="card-maritime lg:col-span-6">
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-lg">
          <MapPin className="h-5 w-5 text-primary" />
          Global Port Status
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {/* Search and Controls */}
          <div className="flex items-center gap-2">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <Input 
                placeholder="Search ports, locations..." 
                className="pl-10 text-sm"
              />
            </div>
            <Button variant="outline" size="sm">
              <Filter className="h-4 w-4" />
            </Button>
            <Button variant="outline" size="sm">
              <Navigation className="h-4 w-4" />
            </Button>
            <Button variant="outline" size="sm">
              <MoreHorizontal className="h-4 w-4" />
            </Button>
          </div>

          {/* Map Visualization */}
          <div className="relative bg-gradient-to-br from-blue-50 to-blue-100 rounded-lg h-64 overflow-hidden">
            {/* World map background simulation */}
            <div className="absolute inset-0 opacity-20">
              <svg viewBox="0 0 1000 500" className="w-full h-full">
                <path 
                  d="M150,200 Q200,150 300,180 T500,160 T700,190 T850,170"
                  stroke="hsl(var(--muted-foreground))"
                  strokeWidth="2"
                  fill="none"
                />
                <path 
                  d="M100,300 Q250,280 400,300 T650,290 T900,310"
                  stroke="hsl(var(--muted-foreground))"
                  strokeWidth="2"
                  fill="none"
                />
              </svg>
            </div>
            
            {/* Port markers */}
            {ports.map((port) => (
              <div
                key={port.id}
                className="absolute transform -translate-x-1/2 -translate-y-1/2"
                style={{ left: port.x, top: port.y }}
              >
                <div className="relative group cursor-pointer">
                  <div className={`w-4 h-4 rounded-full ${statusColors[port.status]} animate-pulse shadow-lg`} />
                  <div className="absolute -top-8 left-1/2 transform -translate-x-1/2 bg-background border border-border rounded px-2 py-1 text-xs font-medium opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">
                    {port.id}
                  </div>
                </div>
              </div>
            ))}
            
            {/* Intelligence indicator */}
            <div className="absolute bottom-4 right-4 bg-background/90 backdrop-blur rounded-lg px-3 py-2 border border-border">
              <div className="text-xs text-muted-foreground">ZeroTouch Port Intelligence</div>
            </div>
          </div>

          {/* Status Legend */}
          <div className="bg-muted/30 rounded-lg p-3">
            <div className="text-sm font-medium mb-2">Port Status</div>
            <div className="flex flex-wrap gap-3 text-xs">
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 rounded-full bg-success" />
                <span>Normal</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 rounded-full bg-destructive" />
                <span>Strike</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 rounded-full bg-warning" />
                <span>Congested</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 rounded-full bg-primary" />
                <span>Reroute</span>
              </div>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default GlobalPortStatus;