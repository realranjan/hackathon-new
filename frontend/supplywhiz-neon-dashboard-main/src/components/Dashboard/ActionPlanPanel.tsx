
import { useState } from "react";
import { X, MapPin, Truck, Factory, CheckCircle2, AlertTriangle, Copy, Share, Download } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { Checkbox } from "@/components/ui/checkbox";
import { toast } from "sonner";

interface ActionPlanPanelProps {
  isOpen: boolean;
  onClose: () => void;
  alertTitle?: string;
}

const ActionPlanPanel = ({ isOpen, onClose, alertTitle }: ActionPlanPanelProps) => {
  const [checkedItems, setCheckedItems] = useState<Set<string>>(new Set());

  if (!isOpen) return null;

  const handleItemCheck = (itemId: string) => {
    const newChecked = new Set(checkedItems);
    if (newChecked.has(itemId)) {
      newChecked.delete(itemId);
    } else {
      newChecked.add(itemId);
    }
    setCheckedItems(newChecked);
  };

  const alternativeRoutes = [
    {
      id: "route1",
      name: "Hamburg → Antwerp → UK",
      duration: "16 days (+2 days)",
      cost: "€1,250 per container (+15%)",
      capacity: "Available: 89 containers",
      risk: "Low"
    },
    {
      id: "route2", 
      name: "Bremerhaven → Le Havre → UK",
      duration: "18 days (+4 days)",
      cost: "€1,180 per container (+8%)",
      capacity: "Available: 124 containers",
      risk: "Medium"
    },
    {
      id: "route3",
      name: "Felixstowe Direct",
      duration: "21 days (+7 days)",
      cost: "€1,050 per container (-3%)",
      capacity: "Available: 67 containers",
      risk: "Low"
    }
  ];

  const alternativeSuppliers = [
    {
      id: "supplier1",
      name: "Nordic Logistics AB",
      location: "Stockholm, Sweden",
      capacity: "High",
      leadTime: "3-5 days",
      reliability: "98%"
    },
    {
      id: "supplier2",
      name: "Baltic Supply Chain",
      location: "Gdansk, Poland", 
      capacity: "Medium",
      leadTime: "5-7 days",
      reliability: "94%"
    }
  ];

  const mitigationChecklist = [
    { id: "check1", task: "Contact affected customers immediately", priority: "High" },
    { id: "check2", task: "Secure alternative shipping capacity", priority: "High" },
    { id: "check3", task: "Update inventory forecasts", priority: "Medium" },
    { id: "check4", task: "Negotiate expedited customs clearance", priority: "Medium" },
    { id: "check5", task: "Activate backup supplier contracts", priority: "High" },
    { id: "check6", task: "Monitor strike negotiations", priority: "Low" },
    { id: "check7", task: "Prepare customer communications", priority: "Medium" },
    { id: "check8", task: "Review insurance coverage", priority: "Low" }
  ];

  const handleCopyPlan = () => {
    toast.success("Action plan copied to clipboard!");
  };

  const handleSharePlan = () => {
    toast.success("Action plan shared with team!");
  };

  const handleDownloadPlan = () => {
    toast.success("Action plan downloaded as PDF!");
  };

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="bg-background/95 backdrop-blur-lg border border-border rounded-xl w-full max-w-6xl max-h-[90vh] overflow-y-auto">
        <div className="p-6 border-b border-border">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-2xl font-bold text-gradient-primary">AI-Generated Action Plan</h2>
              <p className="text-muted-foreground mt-1">
                Disruption: {alertTitle || "Port Strike - Rotterdam"}
              </p>
            </div>
            <div className="flex items-center space-x-2">
              <Button variant="outline" size="sm" onClick={handleCopyPlan}>
                <Copy className="w-4 h-4 mr-2" />
                Copy
              </Button>
              <Button variant="outline" size="sm" onClick={handleSharePlan}>
                <Share className="w-4 h-4 mr-2" />
                Share
              </Button>
              <Button variant="outline" size="sm" onClick={handleDownloadPlan}>
                <Download className="w-4 h-4 mr-2" />
                Export
              </Button>
              <Button variant="ghost" size="icon" onClick={onClose}>
                <X className="w-5 h-5" />
              </Button>
            </div>
          </div>
        </div>

        <div className="p-6 space-y-8">
          {/* Impact Summary */}
          <Card className="glass-card border-l-4 border-l-destructive">
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <AlertTriangle className="w-5 h-5 text-destructive" />
                <span>Impact Assessment</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div className="text-center">
                  <div className="text-2xl font-bold text-destructive">156</div>
                  <div className="text-sm text-muted-foreground">Shipments at Risk</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-destructive">€2.3M</div>
                  <div className="text-sm text-muted-foreground">Potential Losses</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-orange-500">48hrs</div>
                  <div className="text-sm text-muted-foreground">Strike Duration</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-primary">23</div>
                  <div className="text-sm text-muted-foreground">Customers Affected</div>
                </div>
              </div>
            </CardContent>
          </Card>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Alternative Routes */}
            <Card className="glass-card">
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <MapPin className="w-5 h-5 text-accent" />
                  <span>Alternative Routes</span>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {alternativeRoutes.map((route) => (
                  <div key={route.id} className="p-4 rounded-lg bg-muted/20 border border-border/50">
                    <div className="flex items-center justify-between mb-2">
                      <h4 className="font-medium">{route.name}</h4>
                      <Badge className={route.risk === "Low" ? "bg-green-500" : "bg-orange-500"}>
                        {route.risk} Risk
                      </Badge>
                    </div>
                    <div className="space-y-1 text-sm text-muted-foreground">
                      <div className="flex justify-between">
                        <span>Duration:</span>
                        <span>{route.duration}</span>
                      </div>
                      <div className="flex justify-between">
                        <span>Cost:</span>
                        <span>{route.cost}</span>
                      </div>
                      <div className="flex justify-between">
                        <span>Capacity:</span>
                        <span>{route.capacity}</span>
                      </div>
                    </div>
                  </div>
                ))}
              </CardContent>
            </Card>

            {/* Alternative Suppliers */}
            <Card className="glass-card">
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Factory className="w-5 h-5 text-secondary" />
                  <span>Backup Suppliers</span>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {alternativeSuppliers.map((supplier) => (
                  <div key={supplier.id} className="p-4 rounded-lg bg-muted/20 border border-border/50">
                    <div className="flex items-center justify-between mb-2">
                      <h4 className="font-medium">{supplier.name}</h4>
                      <Badge variant="outline">{supplier.capacity} Capacity</Badge>
                    </div>
                    <div className="space-y-1 text-sm text-muted-foreground">
                      <div className="flex justify-between">
                        <span>Location:</span>
                        <span>{supplier.location}</span>
                      </div>
                      <div className="flex justify-between">
                        <span>Lead Time:</span>
                        <span>{supplier.leadTime}</span>
                      </div>
                      <div className="flex justify-between">
                        <span>Reliability:</span>
                        <span className="text-green-500">{supplier.reliability}</span>
                      </div>
                    </div>
                  </div>
                ))}
              </CardContent>
            </Card>
          </div>

          {/* Mitigation Checklist */}
          <Card className="glass-card">
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <CheckCircle2 className="w-5 h-5 text-primary" />
                <span>Mitigation Checklist</span>
                <Badge variant="outline">
                  {checkedItems.size}/{mitigationChecklist.length} Complete
                </Badge>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {mitigationChecklist.map((item) => (
                  <div key={item.id} className="flex items-center space-x-3 p-3 rounded-lg hover:bg-muted/20">
                    <Checkbox
                      checked={checkedItems.has(item.id)}
                      onCheckedChange={() => handleItemCheck(item.id)}
                    />
                    <div className="flex-1">
                      <span className={`${checkedItems.has(item.id) ? 'line-through text-muted-foreground' : ''}`}>
                        {item.task}
                      </span>
                    </div>
                    <Badge 
                      className={
                        item.priority === "High" ? "bg-destructive" :
                        item.priority === "Medium" ? "bg-orange-500" : "bg-muted"
                      }
                    >
                      {item.priority}
                    </Badge>
                  </div>
                ))}
              </div>
              
              <div className="mt-6 p-4 rounded-lg bg-primary/10 border border-primary/20">
                <div className="flex items-start space-x-3">
                  <CheckCircle2 className="w-5 h-5 text-primary mt-0.5" />
                  <div>
                    <h4 className="font-medium text-primary">Recommended Action</h4>
                    <p className="text-sm text-muted-foreground mt-1">
                      Immediately activate Route 1 (Hamburg → Antwerp → UK) and contact Nordic Logistics AB 
                      for emergency capacity. This combination provides the best balance of speed, cost, and reliability.
                    </p>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default ActionPlanPanel;
