import { useEffect, useState } from "react";
import { Card } from "@/components/ui/card";

const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

const HealthStatus = () => {
  const [status, setStatus] = useState("unknown");
  const [lastChecked, setLastChecked] = useState("");

  useEffect(() => {
    const fetchHealth = async () => {
      try {
        const res = await fetch(`${API_BASE}/healthz`);
        const data = await res.json();
        setStatus(data.status);
        setLastChecked(new Date().toLocaleTimeString());
      } catch {
        setStatus("error");
        setLastChecked(new Date().toLocaleTimeString());
      }
    };
    fetchHealth();
    const interval = setInterval(fetchHealth, 30000);
    return () => clearInterval(interval);
  }, []);

  return (
    <Card className="p-2 text-xs flex items-center gap-2 bg-muted/50 border border-muted-foreground/20 rounded">
      <span className={status === "ok" ? "text-green-600" : "text-red-600"}>
        ●
      </span>
      <span>Backend Health: {status}</span>
      <span className="ml-auto text-muted-foreground">{lastChecked}</span>
    </Card>
  );
};
export default HealthStatus; 