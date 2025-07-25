import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Textarea } from "@/components/ui/textarea";
import { Progress } from "@/components/ui/progress";
import { 
  Truck, 
  MapPin, 
  Clock, 
  Package, 
  AlertTriangle, 
  CheckCircle, 
  Navigation,
  Filter,
  Search,
  MoreVertical,
  ChevronRight
} from "lucide-react";

const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

const statusConfig = {
  "in-transit": { color: "bg-blue-500", variant: "default" as const, icon: Truck },
  "delayed": { color: "bg-red-500", variant: "destructive" as const, icon: AlertTriangle },
  "arrived": { color: "bg-green-500", variant: "secondary" as const, icon: CheckCircle },
  "loading": { color: "bg-yellow-500", variant: "outline" as const, icon: Package }
};

const priorityConfig = {
  "critical": { color: "text-red-600 dark:text-red-400", bg: "bg-red-500/10 border-red-500/20 dark:bg-red-500/20 dark:border-red-500/30" },
  "high": { color: "text-orange-600 dark:text-orange-400", bg: "bg-orange-500/10 border-orange-500/20 dark:bg-orange-500/20 dark:border-orange-500/30" },
  "medium": { color: "text-blue-600 dark:text-blue-400", bg: "bg-blue-500/10 border-blue-500/20 dark:bg-blue-500/20 dark:border-blue-500/30" }
};

const riskConfig = {
  "high": { color: "text-red-600 dark:text-red-400", bg: "bg-red-500/10 dark:bg-red-500/20" },
  "medium": { color: "text-yellow-600 dark:text-yellow-400", bg: "bg-yellow-500/10 dark:bg-yellow-500/20" },
  "low": { color: "text-green-600 dark:text-green-400", bg: "bg-green-500/10 dark:bg-green-500/20" }
};

const ShipmentsTracking = () => {
  const [shipments, setShipments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState("");
  const [statusFilter, setStatusFilter] = useState("all");
  const [selectedShipment, setSelectedShipment] = useState(null);
  const [realTimeUpdates, setRealTimeUpdates] = useState(true);

  useEffect(() => {
    fetch(`${API_BASE}/shipments/`)
      .then(res => res.json())
      .then(data => {
        setShipments(data.shipments || []);
        setLoading(false);
      })
      .catch(err => {
        setError("Failed to load shipments");
        setLoading(false);
      });
  }, []);

  useEffect(() => {
    if (!realTimeUpdates) return;
    const interval = setInterval(() => {
      const inTransitShipments = shipments.filter(s => s.status === 'in-transit');
      if (inTransitShipments.length > 0) {
        const randomShipment = inTransitShipments[Math.floor(Math.random() * inTransitShipments.length)];
        console.log(`Real-time update: ${randomShipment.id} progress updated`);
      }
    }, 5000);
    return () => clearInterval(interval);
  }, [realTimeUpdates, shipments]);

  if (loading) return <div>Loading shipments...</div>;
  if (error) return <div>{error}</div>;

  const filteredShipments = shipments.filter(shipment => {
    const matchesSearch =
      String(shipment.id || "").toLowerCase().includes(searchTerm.toLowerCase()) ||
      String(shipment.origin || "").toLowerCase().includes(searchTerm.toLowerCase()) ||
      String(shipment.destination || "").toLowerCase().includes(searchTerm.toLowerCase());
    const matchesStatus = statusFilter === "all" || shipment.status === statusFilter;
    return matchesSearch && matchesStatus;
  });

  return (
    <Card className="card-maritime">
      <CardHeader className="pb-3">
        <CardTitle className="flex items-center justify-between text-base">
          <div className="flex items-center gap-2">
            <Navigation className="h-4 w-4 text-primary" />
            <span className="hidden sm:inline">Shipment Tracking</span>
            <span className="sm:hidden">Shipments</span>
          </div>
          <div className="flex items-center gap-1 sm:gap-2">
            <Badge variant={realTimeUpdates ? "default" : "secondary"} className="text-xs px-1.5 py-0.5">
              {realTimeUpdates ? "Live" : "Static"}
            </Badge>
            <Button
              variant="outline"
              size="sm"
              onClick={() => setRealTimeUpdates(!realTimeUpdates)}
              className="text-xs h-6 px-2"
            >
              {realTimeUpdates ? "Pause" : "Resume"}
            </Button>
          </div>
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-3 px-4 pb-4">
        {/* Filters - Mobile Optimized */}
        <div className="flex items-center gap-2">
          <div className="relative flex-1">
            <Search className="absolute left-2 top-1/2 transform -translate-y-1/2 h-3 w-3 text-muted-foreground" />
            <Input
              placeholder="Search..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-7 h-8 text-xs"
            />
          </div>
          <Select value={statusFilter} onValueChange={setStatusFilter}>
            <SelectTrigger className="w-24 h-8 text-xs">
              <SelectValue placeholder="All" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Status</SelectItem>
              <SelectItem value="in-transit">In Transit</SelectItem>
              <SelectItem value="delayed">Delayed</SelectItem>
              <SelectItem value="arrived">Arrived</SelectItem>
              <SelectItem value="loading">Loading</SelectItem>
            </SelectContent>
          </Select>
          <Button variant="outline" size="sm" className="h-8 w-8 p-0">
            <Filter className="h-3 w-3" />
          </Button>
        </div>

        {/* Stats Row - Mobile Optimized */}
        <div className="grid grid-cols-4 gap-2">
          <div className="text-center p-2 bg-muted/30 rounded-lg">
            <div className="text-sm sm:text-lg font-bold text-foreground">{shipments.length}</div>
            <div className="text-xs text-muted-foreground">Total</div>
          </div>
          <div className="text-center p-2 bg-blue-500/10 dark:bg-blue-500/20 rounded-lg">
            <div className="text-sm sm:text-lg font-bold text-blue-600 dark:text-blue-400">
              {shipments.filter(s => s.status === 'in-transit').length}
            </div>
            <div className="text-xs text-muted-foreground">In Transit</div>
          </div>
          <div className="text-center p-2 bg-red-500/10 dark:bg-red-500/20 rounded-lg">
            <div className="text-sm sm:text-lg font-bold text-red-600 dark:text-red-400">
              {shipments.filter(s => s.status === 'delayed').length}
            </div>
            <div className="text-xs text-muted-foreground">Delayed</div>
          </div>
          <div className="text-center p-2 bg-green-500/10 dark:bg-green-500/20 rounded-lg">
            <div className="text-sm sm:text-lg font-bold text-green-600 dark:text-green-400">
              {shipments.filter(s => s.status === 'arrived').length}
            </div>
            <div className="text-xs text-muted-foreground">Delivered</div>
          </div>
        </div>

        {/* Shipments List - Mobile Optimized */}
        <div className="space-y-2 max-h-80 overflow-y-auto">
          {filteredShipments.slice(0, 3).map((shipment) => {
            const statusConf = statusConfig[shipment.status] || { color: '', variant: 'default', icon: Truck };
            const priorityConf = priorityConfig[shipment.priority] || { color: '', bg: '' };
            const riskConf = riskConfig[shipment.riskLevel] || { color: '', bg: '' };
            const StatusIcon = statusConf.icon || Truck;

            return (
              <div
                key={shipment.id}
                className={`border rounded-lg p-3 hover:shadow-md transition-all cursor-pointer ${priorityConf.bg}`}
                onClick={() => setSelectedShipment(shipment)}
              >
                <div className="flex items-start justify-between mb-2">
                  <div className="flex items-start gap-2 flex-1 min-w-0">
                    <div className="flex flex-col items-center flex-shrink-0">
                      <StatusIcon className="h-4 w-4 text-muted-foreground" />
                      <div className={`w-1.5 h-1.5 rounded-full mt-1 ${statusConf.color} ${realTimeUpdates ? 'animate-pulse' : ''}`} />
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-1 mb-1 flex-wrap">
                        <h4 className="font-semibold text-sm truncate">{shipment.id}</h4>
                        <Badge variant={statusConf.variant} className="text-xs px-1.5 py-0.5">
                          {shipment.status === 'in-transit' ? 'IN TRANSIT' : 
                           shipment.status === 'delayed' ? 'DELAYED' : 
                           shipment.status.replace('-', ' ').toUpperCase()}
                        </Badge>
                        <Badge variant="outline" className={`text-xs px-1.5 py-0.5 ${priorityConf.color}`}>
                          {shipment.priority === 'critical' ? 'HIGH' : 
                           shipment.priority === 'high' ? 'MED' : 
                           (shipment.priority && typeof shipment.priority === 'string' ? shipment.priority.substring(0, 3).toUpperCase() : '—')}
                        </Badge>
                      </div>
                      
                      <div className="text-xs mb-2 space-y-1">
                        <div className="flex items-center gap-1">
                          <span className="text-muted-foreground">From:</span>
                          <span className="truncate">{shipment.origin}</span>
                        </div>
                        <div className="flex items-center gap-1">
                          <span className="text-muted-foreground">To:</span>
                          <span className="truncate">{shipment.destination}</span>
                        </div>
                        <div className="flex items-center justify-between">
                          <div className="flex items-center gap-1">
                            <Package className="h-3 w-3 text-muted-foreground" />
                            <span>{shipment.containers} containers</span>
                          </div>
                          <div className="flex items-center gap-1">
                            <Clock className="h-3 w-3 text-muted-foreground" />
                            <span>ETA: {shipment.eta}</span>
                          </div>
                        </div>
                      </div>

                      {shipment.status === 'in-transit' && (
                        <div className="space-y-1">
                          <div className="flex items-center justify-between text-xs">
                            <span>Progress</span>
                            <span>{shipment.progress}%</span>
                          </div>
                          <Progress value={shipment.progress} className="h-1.5" />
                        </div>
                      )}

                      {shipment.estimatedDelay > 0 && (
                        <div className="mt-1 p-1.5 bg-red-500/10 dark:bg-red-500/20 rounded text-xs text-red-600 dark:text-red-400">
                          ⚠️ Delay: {shipment.estimatedDelay}h
                        </div>
                      )}
                    </div>
                  </div>
                  
                  <div className="text-right flex-shrink-0 ml-2">
                    <div className={`text-xs font-medium ${riskConf.color} mb-1`}>
                      {(shipment.riskLevel && typeof shipment.riskLevel === 'string') ? shipment.riskLevel.toUpperCase() : '—'}
                    </div>
                    <div className="text-xs text-muted-foreground">
                      {(shipment.lastUpdate && typeof shipment.lastUpdate === 'string') ? shipment.lastUpdate.replace(' ago', '') : ''}
                    </div>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
        
        {filteredShipments.length > 3 && (
          <div className="text-center pt-2">
            <Button variant="outline" size="sm" className="gap-2 text-xs">
              View All ({filteredShipments.length}) Shipments
              <ChevronRight className="h-3 w-3" />
            </Button>
          </div>
        )}
      </CardContent>
    </Card>
  );
};

export default ShipmentsTracking;