import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Network } from "lucide-react";

const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

const AgentNetwork = () => {
  const [edges, setEdges] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);
    fetch(`${API_BASE}/agents/network/`)
      .then(res => res.json())
      .then(data => {
        if (data.network && Array.isArray(data.network.edges)) {
          setEdges(data.network.edges);
        } else {
          setEdges([]);
        }
        setLoading(false);
      })
      .catch(() => {
        setError("Failed to load agent network");
        setLoading(false);
      });
  }, []);

  if (loading) return <div>Loading agent network...</div>;
  if (error) return <div>{error}</div>;

  return (
    <Card className="card-maritime lg:col-span-3">
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-lg">
          <Network className="h-5 w-5 text-primary" />
          Agent Network
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          <div className="text-xs">
            <div className="font-medium mb-2">Network Connections</div>
            <ul>
              {edges.length > 0 ? (
                edges.map((conn, idx) => (
                  <li key={idx}>{conn.source} → {conn.target}</li>
                ))
              ) : (
                <li>No connections found.</li>
              )}
            </ul>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default AgentNetwork;