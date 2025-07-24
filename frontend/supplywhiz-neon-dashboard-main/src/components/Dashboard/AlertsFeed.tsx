import { useState } from "react";
import { Clock, MapPin, AlertTriangle, AlertCircle, CheckCircle, ExternalLink } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

interface Alert {
  id: string;
  type: "Weather" | "Traffic" | "Supplier" | "Port" | "Geopolitical";
  title: string;
  location: string;
  severity: "high" | "medium" | "low";
  time: string;
  description: string;
  impact: string;
}

const mockAlerts: Alert[] = [
  {
    id: "1",
    type: "Weather",
    title: "Severe Storm Warning",
    location: "Hong Kong Port",
    severity: "high",
    time: "2 min ago",
    description: "Typhoon approaching major shipping routes",
    impact: "37 shipments delayed"
  },
  {
    id: "2", 
    type: "Supplier",
    title: "Factory Shutdown",
    location: "Shanghai, China",
    severity: "medium",
    time: "15 min ago",
    description: "Key electronics supplier experiencing power outage",
    impact: "12 suppliers affected"
  },
  {
    id: "3",
    type: "Traffic",
    title: "Highway Closure",
    location: "I-95 Virginia",
    severity: "low",
    time: "1 hour ago",
    description: "Construction causing delays on main logistics route",
    impact: "8 deliveries delayed"
  },
  {
    id: "4",
    type: "Port",
    title: "Container Backlog",
    location: "Port of Los Angeles",
    severity: "medium",
    time: "2 hours ago",
    description: "Increased container volume causing processing delays",
    impact: "23 shipments queued"
  }
];

const severityConfig = {
  high: {
    icon: AlertTriangle,
    className: "alert-high",
    badge: "bg-destructive text-destructive-foreground"
  },
  medium: {
    icon: AlertCircle,
    className: "alert-medium", 
    badge: "bg-secondary text-secondary-foreground"
  },
  low: {
    icon: CheckCircle,
    className: "alert-low",
    badge: "bg-primary text-primary-foreground"
  }
};

const typeIcons = {
  Weather: "🌪️",
  Traffic: "🚦",
  Supplier: "🏭",
  Port: "⚓",
  Geopolitical: "🌍"
};

interface AlertsFeedProps {
  onAlertClick?: (alert: Alert) => void;
}

const AlertsFeed = ({ onAlertClick }: AlertsFeedProps) => {
  const [alerts] = useState<Alert[]>(mockAlerts);

  return (
    <Card className="glass-card">
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="text-lg font-semibold">Real-Time Alerts</CardTitle>
          <Badge variant="outline" className="bg-primary/10 text-primary border-primary/20">
            {alerts.length} Active
          </Badge>
        </div>
      </CardHeader>
      <CardContent className="space-y-4 max-h-96 overflow-y-auto">
        {alerts.map((alert) => {
          const config = severityConfig[alert.severity];
          const SeverityIcon = config.icon;
          
          return (
            <div
              key={alert.id}
              className={`p-4 rounded-lg border-l-4 glass-panel card-hover cursor-pointer ${config.className}`}
              onClick={() => onAlertClick?.(alert)}
            >
              <div className="flex items-start justify-between">
                <div className="flex items-start space-x-3 flex-1">
                  <div className="flex items-center space-x-2">
                    <span className="text-lg">{typeIcons[alert.type]}</span>
                    <SeverityIcon className="w-4 h-4" />
                  </div>
                  
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center justify-between mb-1">
                      <h4 className="font-medium text-foreground truncate">{alert.title}</h4>
                      <Badge className={`ml-2 ${config.badge} text-xs`}>
                        {alert.severity.toUpperCase()}
                      </Badge>
                    </div>
                    
                    <div className="flex items-center text-sm text-muted-foreground mb-2">
                      <MapPin className="w-3 h-3 mr-1" />
                      <span>{alert.location}</span>
                      <Clock className="w-3 h-3 ml-3 mr-1" />
                      <span>{alert.time}</span>
                    </div>
                    
                    <p className="text-sm text-muted-foreground mb-2">{alert.description}</p>
                    <p className="text-xs text-accent font-medium">{alert.impact}</p>
                  </div>
                </div>
                
                <Button variant="ghost" size="sm" className="ml-2 hover:bg-primary/10">
                  <ExternalLink className="w-4 h-4" />
                </Button>
              </div>
            </div>
          );
        })}
      </CardContent>
    </Card>
  );
};

export default AlertsFeed;