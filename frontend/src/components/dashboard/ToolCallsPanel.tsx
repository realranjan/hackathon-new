import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { ChevronRight, Wrench, Activity, Clock } from "lucide-react";
import { useAISimulation } from "@/contexts/AISimulationContext";

const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

const ToolCallsPanel = () => {
  const [toolCalls, setToolCalls] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);
    fetch(`${API_BASE}/tool_calls/`)
      .then(res => res.json())
      .then(data => {
        setToolCalls(data.calls || []);
        setLoading(false);
      })
      .catch(() => {
        setError("Failed to load tool calls");
        setLoading(false);
      });
  }, []);

  if (loading) return <div>Loading tool calls...</div>;
  if (error) return <div>{error}</div>;

  return (
    <Card className="card-maritime lg:col-span-3">
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-lg">
          <Wrench className="h-5 w-5 text-primary" />
          Tool Calls
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          <div className="flex items-center justify-between text-sm">
            <div className="flex items-center gap-2">
              <ChevronRight className="h-4 w-4 text-muted-foreground" />
              <span>Live Tool Calls</span>
            </div>
            <Badge variant={toolCalls.length > 0 ? "default" : "secondary"} className="text-xs">
              {toolCalls.length > 0 ? `${toolCalls.length} active` : "0 calls"}
            </Badge>
          </div>
          {toolCalls.length > 0 ? (
            <div className="space-y-3">
              {toolCalls.map((call, idx) => (
                <div key={idx} className="flex items-center gap-3 p-3 rounded-lg bg-muted/30 animate-fade-in">
                  <div className="p-1.5 rounded-full bg-primary/20">
                    <Activity className="h-3 w-3 text-primary animate-pulse" />
                  </div>
                  <div className="flex-1">
                    <div className="text-sm font-medium">{call.agent}</div>
                    <div className="text-xs text-muted-foreground flex items-center gap-1">
                      <Clock className="h-3 w-3" />
                      {call.tool} ({call.status})
                    </div>
                  </div>
                  <Badge variant="outline" className="text-xs">
                    {call.status}
                  </Badge>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-8">
              <div className="text-muted-foreground text-sm mb-2">No tool calls yet</div>
              <div className="text-xs text-muted-foreground">
                Start the demo to see AI agents in action
              </div>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
};

export default ToolCallsPanel;