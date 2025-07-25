import { useEffect, useState } from 'react';
import {
  ReactFlow,
  addEdge,
  MiniMap,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  Connection,
  Edge,
  Node,
  Position,
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Network, Eye, Cpu, Target, Zap, Shield, Server, Database, Globe } from "lucide-react";

const initialNodes: Node[] = [
  // Input Sources
  {
    id: 'satellite',
    type: 'input',
    position: { x: 50, y: 50 },
    data: { label: '🛰️ Satellite' },
    style: { background: '#E3F2FD', border: '2px solid #2196F3', fontSize: '12px' }
  },
  {
    id: 'iot',
    type: 'input', 
    position: { x: 50, y: 150 },
    data: { label: '📡 IoT' },
    style: { background: '#E8F5E8', border: '2px solid #4CAF50', fontSize: '12px' }
  },
  {
    id: 'weather',
    type: 'input',
    position: { x: 50, y: 250 },
    data: { label: '🌤️ Weather' },
    style: { background: '#FFF3E0', border: '2px solid #FF9800', fontSize: '12px' }
  },

  // AI Agents
  {
    id: 'watchtower',
    position: { x: 250, y: 50 },
    data: { 
      label: (
        <div className="flex flex-col items-center gap-1">
          <Eye className="h-4 w-4 text-blue-600" />
          <span className="text-xs font-medium">Watchtower</span>
          <Badge variant="secondary" className="text-xs px-1 py-0.5">Active</Badge>
        </div>
      )
    },
    style: { background: '#F3E5F5', border: '2px solid #9C27B0', width: 100, height: 70 }
  },
  {
    id: 'oracle',
    position: { x: 380, y: 50 },
    data: { 
      label: (
        <div className="flex flex-col items-center gap-1">
          <Cpu className="h-4 w-4 text-purple-600" />
          <span className="text-xs font-medium">Oracle</span>
          <Badge variant="outline" className="text-xs px-1 py-0.5">Live</Badge>
        </div>
      )
    },
    style: { background: '#F3E5F5', border: '2px solid #673AB7', width: 100, height: 70 }
  },
  {
    id: 'diplomat',
    position: { x: 315, y: 170 },
    data: { 
      label: (
        <div className="flex flex-col items-center gap-1">
          <Target className="h-4 w-4 text-green-600" />
          <span className="text-xs font-medium">Diplomat</span>
          <Badge variant="secondary" className="text-xs px-1 py-0.5">Ready</Badge>
        </div>
      )
    },
    style: { background: '#E8F5E8', border: '2px solid #4CAF50', width: 100, height: 70 }
  },
  {
    id: 'commander',
    position: { x: 250, y: 290 },
    data: { 
      label: (
        <div className="flex flex-col items-center gap-1">
          <Zap className="h-4 w-4 text-orange-600" />
          <span className="text-xs font-medium">Commander</span>
          <Badge variant="secondary" className="text-xs px-1 py-0.5">Idle</Badge>
        </div>
      )
    },
    style: { background: '#FFF3E0', border: '2px solid #FF9800', width: 100, height: 70 }
  },
  {
    id: 'guardian',
    position: { x: 380, y: 290 },
    data: { 
      label: (
        <div className="flex flex-col items-center gap-1">
          <Shield className="h-4 w-4 text-red-600" />
          <span className="text-xs font-medium">Guardian</span>
          <Badge variant="secondary" className="text-xs px-1 py-0.5">Monitor</Badge>
        </div>
      )
    },
    style: { background: '#FFEBEE', border: '2px solid #F44336', width: 100, height: 70 }
  },

  // Processing Center
  {
    id: 'processing',
    position: { x: 550, y: 170 },
    data: { 
      label: (
        <div className="flex flex-col items-center gap-1">
          <Server className="h-5 w-5 text-blue-600" />
          <span className="text-sm font-medium">Hub</span>
          <div className="text-xs text-muted-foreground">Neural</div>
        </div>
      )
    },
    style: { background: '#E3F2FD', border: '2px solid #2196F3', width: 120, height: 80 }
  },

  // Output Systems
  {
    id: 'dashboard',
    type: 'output',
    position: { x: 720, y: 100 },
    data: { label: '📊 Dashboard' },
    style: { background: '#F3E5F5', border: '2px solid #9C27B0', fontSize: '12px' }
  },
  {
    id: 'alerts',
    type: 'output',
    position: { x: 720, y: 200 },
    data: { label: '🚨 Alerts' },
    style: { background: '#FFEBEE', border: '2px solid #F44336', fontSize: '12px' }
  },
  {
    id: 'automation',
    type: 'output',
    position: { x: 720, y: 300 },
    data: { label: '⚡ Auto' },
    style: { background: '#FFF3E0', border: '2px solid #FF9800', fontSize: '12px' }
  }
];

const initialEdges: Edge[] = [
  // Input to Agents
  { id: 'e1', source: 'satellite', target: 'watchtower', animated: true, style: { stroke: '#2196F3' } },
  { id: 'e2', source: 'iot', target: 'watchtower', animated: true, style: { stroke: '#4CAF50' } },
  { id: 'e3', source: 'weather', target: 'oracle', animated: true, style: { stroke: '#FF9800' } },

  // Agent interactions
  { id: 'e4', source: 'watchtower', target: 'oracle', animated: true, style: { stroke: '#9C27B0' } },
  { id: 'e5', source: 'oracle', target: 'diplomat', animated: true, style: { stroke: '#673AB7' } },
  { id: 'e6', source: 'diplomat', target: 'commander', animated: true, style: { stroke: '#4CAF50' } },
  { id: 'e7', source: 'commander', target: 'guardian', animated: true, style: { stroke: '#FF9800' } },

  // To processing hub
  { id: 'e8', source: 'watchtower', target: 'processing', style: { stroke: '#9C27B0' } },
  { id: 'e9', source: 'oracle', target: 'processing', style: { stroke: '#673AB7' } },
  { id: 'e10', source: 'diplomat', target: 'processing', style: { stroke: '#4CAF50' } },
  { id: 'e11', source: 'commander', target: 'processing', style: { stroke: '#FF9800' } },
  { id: 'e12', source: 'guardian', target: 'processing', style: { stroke: '#F44336' } },

  // Processing to outputs
  { id: 'e13', source: 'processing', target: 'dashboard', animated: true, style: { stroke: '#2196F3' } },
  { id: 'e14', source: 'processing', target: 'alerts', animated: true, style: { stroke: '#F44336' } },
  { id: 'e15', source: 'processing', target: 'automation', animated: true, style: { stroke: '#FF9800' } }
];

const nodeClassName = (node: Node) => node.type || 'default';

const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

const AINetworkVisualization = () => {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);
  const [processingCount, setProcessingCount] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);
    fetch(`${API_BASE}/agents/network/`)
      .then(res => res.json())
      .then(data => {
        if (data.network) {
          const newEdges = data.network.map((conn: any, idx: number) => ({
            id: `e${idx + 1}`,
            source: conn.source,
            target: conn.target,
            animated: true,
            style: { stroke: '#2196F3' }
          }));
          setEdges(newEdges);
        }
        setLoading(false);
      })
      .catch(() => {
        setError("Failed to load agent network");
        setLoading(false);
      });
  }, [setEdges]);

  // Simulate real-time data processing
  useEffect(() => {
    const interval = setInterval(() => {
      setProcessingCount(prev => prev + 1);
      
      // Simulate node status updates
      setNodes((nds) =>
        nds.map((node) => {
          if (node.id === 'processing') {
            return {
              ...node,
              data: {
                ...node.data,
                label: (
                  <div className="flex flex-col items-center gap-1">
                    <Server className="h-5 w-5 text-blue-600" />
                    <span className="text-sm font-medium">Hub</span>
                    <div className="text-xs text-muted-foreground">
                      {processingCount} ops
                    </div>
                    <div className="w-4 h-1 bg-blue-200 rounded-full overflow-hidden">
                      <div className="w-full h-full bg-blue-500 animate-pulse" />
                    </div>
                  </div>
                )
              }
            };
          }
          return node;
        })
      );
    }, 2000);

    return () => clearInterval(interval);
  }, [setNodes, processingCount]);

  if (loading) return <div>Loading AI network...</div>;
  if (error) return <div>{error}</div>;

  return (
    <Card className="card-maritime">
      <CardHeader className="pb-3">
        <CardTitle className="flex items-center justify-between text-base">
          <div className="flex items-center gap-2">
            <Network className="h-4 w-4 text-primary" />
            <span className="hidden sm:inline">AI Agent Network Visualization</span>
            <span className="sm:hidden">AI Network</span>
          </div>
          <Badge variant="secondary" className="text-xs px-1.5 py-0.5">
            Real-time
          </Badge>
        </CardTitle>
      </CardHeader>
      <CardContent className="px-4 pb-4">
        <div className="h-64 sm:h-80 lg:h-96 border border-border rounded-lg overflow-hidden">
          <ReactFlow
            nodes={nodes}
            edges={edges}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            fitView
            attributionPosition="bottom-left"
            style={{ backgroundColor: "hsl(var(--muted))" }}
            nodesDraggable={true}
            nodesConnectable={false}
            elementsSelectable={true}
            minZoom={0.3}
            maxZoom={1.5}
            defaultViewport={{ x: 0, y: 0, zoom: 0.5 }}
          >
            <Controls className="hidden sm:flex" />
            <MiniMap 
              zoomable 
              pannable 
              nodeClassName={nodeClassName}
              style={{ backgroundColor: "hsl(var(--background))" }}
              className="hidden lg:block"
            />
            <Background />
          </ReactFlow>
        </div>
        
        <div className="mt-3 grid grid-cols-3 gap-2 text-xs">
          <div className="text-center p-2 bg-muted/30 rounded-lg">
            <div className="font-medium text-sm">Sources</div>
            <div className="text-muted-foreground">3 active</div>
          </div>
          <div className="text-center p-2 bg-blue-500/10 dark:bg-blue-500/20 rounded-lg">
            <div className="font-medium text-sm text-blue-600 dark:text-blue-400">Processing</div>
            <div className="text-muted-foreground">{processingCount} ops/min</div>
          </div>
          <div className="text-center p-2 bg-green-500/10 dark:bg-green-500/20 rounded-lg">
            <div className="font-medium text-sm text-green-600 dark:text-green-400">Outputs</div>
            <div className="text-muted-foreground">3 systems</div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default AINetworkVisualization;