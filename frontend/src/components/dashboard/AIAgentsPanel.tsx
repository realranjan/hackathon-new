import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Eye, Cpu, Zap, Target, Shield } from "lucide-react";
import { useAISimulation } from "@/contexts/AISimulationContext";
import { useEffect, useState } from "react";

const iconMap: Record<string, any> = { Eye, Cpu, Zap, Target, Shield };

const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

const AIAgentsPanel = () => {
  const [agentStatus, setAgentStatus] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);
    fetch(`${API_BASE}/agents/list/`)
      .then(res => res.json())
      .then(data => {
        setAgentStatus(data.agents || []);
        setLoading(false);
      })
      .catch(() => {
        setError("Failed to load agent status");
        setLoading(false);
      });
  }, []);

  if (loading) return <div>Loading agent status...</div>;
  if (error) return <div>{error}</div>;

  const getAgentStatus = (agentName: string) => {
    if (!agentStatus || agentStatus.length === 0) return "idle";
    
    const agent = agentStatus.find(a => a.id.toLowerCase() === agentName.toLowerCase());
    if (!agent) return "idle";

    return agent.status;
  };
  return (
    <Card className="card-maritime">
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-lg">
          <Cpu className="h-5 w-5 text-primary" />
          AI Agents
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {agentStatus.map((agent) => {
          const IconComponent = iconMap[agent.icon] || Cpu;
          const isActive = agent.status === "active";
          return (
            <div
              key={agent.id}
              className={`flex items-center justify-between p-3 rounded-lg border transition-all duration-300 ${
                isActive 
                  ? "border-primary bg-primary/5 animate-fade-in" 
                  : "border-border hover:bg-muted/50"
              }`}
            >
              <div className="flex items-center gap-3">
                <div className={`p-2 rounded-lg transition-colors ${
                  isActive ? "bg-primary/20" : "bg-muted"
                }`}>
                  <IconComponent className={`h-4 w-4 transition-colors ${
                    isActive ? "text-primary animate-pulse" : "text-muted-foreground"
                  }`} />
                </div>
                <div>
                  <div className="font-medium text-sm">{agent.name}</div>
                  <div className="text-xs text-muted-foreground">{agent.description}</div>
                </div>
              </div>
              <Badge 
                variant={isActive ? "default" : "secondary"} 
                className={`text-xs ${isActive ? "animate-pulse" : ""}`}
              >
                {agent.status}
              </Badge>
            </div>
          );
        })}
      </CardContent>
    </Card>
  );
};

export default AIAgentsPanel;