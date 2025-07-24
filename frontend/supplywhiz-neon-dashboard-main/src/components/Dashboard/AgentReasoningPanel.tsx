import { useState } from "react";
import { ChevronDown, ChevronRight, Brain, Code, Lightbulb, CheckCircle2 } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from "@/components/ui/collapsible";

interface ReasoningStep {
  id: string;
  title: string;
  description: string;
  status: "completed" | "processing" | "pending";
  details?: string;
  code?: string;
}

const mockReasoningSteps: ReasoningStep[] = [
  {
    id: "1",
    title: "Data Collection",
    description: "Gathering real-time data from multiple sources",
    status: "completed",
    details: "Collected data from weather APIs, traffic systems, and supplier databases",
    code: `fetch('/api/weather').then(response => {
  const weatherData = response.json();
  analyzeImpact(weatherData);
});`
  },
  {
    id: "2", 
    title: "Risk Assessment",
    description: "Analyzing potential supply chain impacts",
    status: "completed",
    details: "Calculated risk scores based on historical patterns and current conditions",
    code: `const riskScore = calculateRisk({
  severity: weatherData.severity,
  duration: weatherData.duration,
  affectedRoutes: routeData.impacted
});`
  },
  {
    id: "3",
    title: "Alternative Analysis",
    description: "Identifying backup routes and suppliers",
    status: "processing",
    details: "Evaluating 23 alternative routes and 8 backup suppliers",
    code: `const alternatives = await findAlternatives({
  originalRoute: route,
  constraints: ['cost', 'time', 'capacity']
});`
  },
  {
    id: "4",
    title: "Impact Prediction",
    description: "Forecasting downstream effects",
    status: "pending",
    details: "Will analyze cascading effects on delivery schedules and inventory levels"
  }
];

const AgentReasoningPanel = () => {
  const [isExpanded, setIsExpanded] = useState(false);
  const [expandedSteps, setExpandedSteps] = useState<Set<string>>(new Set());

  const toggleStep = (stepId: string) => {
    const newExpanded = new Set(expandedSteps);
    if (newExpanded.has(stepId)) {
      newExpanded.delete(stepId);
    } else {
      newExpanded.add(stepId);
    }
    setExpandedSteps(newExpanded);
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case "completed":
        return <CheckCircle2 className="w-4 h-4 text-primary" />;
      case "processing":
        return <div className="w-4 h-4 border-2 border-secondary border-t-transparent rounded-full animate-spin" />;
      case "pending":
        return <div className="w-4 h-4 border-2 border-muted-foreground/30 rounded-full" />;
      default:
        return null;
    }
  };

  const getStatusBadge = (status: string) => {
    switch (status) {
      case "completed":
        return <Badge className="bg-primary/20 text-primary border-primary/30">Completed</Badge>;
      case "processing":
        return <Badge className="bg-secondary/20 text-secondary border-secondary/30">Processing</Badge>;
      case "pending":
        return <Badge variant="outline" className="border-muted-foreground/30">Pending</Badge>;
      default:
        return null;
    }
  };

  return (
    <Card className="glass-card">
      <CardHeader>
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Brain className="w-5 h-5 text-accent" />
            <CardTitle className="text-lg font-semibold">AI Agent Reasoning</CardTitle>
          </div>
          <Button
            variant="ghost"
            size="sm"
            onClick={() => setIsExpanded(!isExpanded)}
            className="hover:bg-muted/50"
          >
            {isExpanded ? <ChevronDown className="w-4 h-4" /> : <ChevronRight className="w-4 h-4" />}
            <span className="ml-1">
              {isExpanded ? "Collapse" : "Expand"}
            </span>
          </Button>
        </div>
      </CardHeader>
      
      <Collapsible open={isExpanded} onOpenChange={setIsExpanded}>
        <CollapsibleContent>
          <CardContent className="space-y-4">
            {mockReasoningSteps.map((step, index) => (
              <div key={step.id} className="border border-border/50 rounded-lg p-4 glass-panel">
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center space-x-3">
                    <span className="w-6 h-6 rounded-full bg-muted flex items-center justify-center text-xs font-medium">
                      {index + 1}
                    </span>
                    {getStatusIcon(step.status)}
                    <h4 className="font-medium">{step.title}</h4>
                  </div>
                  {getStatusBadge(step.status)}
                </div>
                
                <p className="text-sm text-muted-foreground mb-3 ml-9">{step.description}</p>
                
                {step.details && (
                  <Collapsible>
                    <CollapsibleTrigger asChild>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => toggleStep(step.id)}
                        className="ml-9 text-xs hover:bg-muted/50"
                      >
                        <Lightbulb className="w-3 h-3 mr-1" />
                        {expandedSteps.has(step.id) ? "Hide Details" : "Show Details"}
                      </Button>
                    </CollapsibleTrigger>
                    <CollapsibleContent className="ml-9 mt-2">
                      <div className="p-3 bg-muted/30 rounded-md border border-border/30">
                        <p className="text-xs text-muted-foreground mb-2">{step.details}</p>
                        {step.code && (
                          <div className="mt-2">
                            <div className="flex items-center space-x-1 mb-1">
                              <Code className="w-3 h-3 text-accent" />
                              <span className="text-xs font-medium text-accent">Code Example</span>
                            </div>
                            <pre className="bg-background/50 p-2 rounded text-xs overflow-x-auto border border-border/30">
                              <code className="text-primary">{step.code}</code>
                            </pre>
                          </div>
                        )}
                      </div>
                    </CollapsibleContent>
                  </Collapsible>
                )}
              </div>
            ))}
          </CardContent>
        </CollapsibleContent>
      </Collapsible>
    </Card>
  );
};

export default AgentReasoningPanel;