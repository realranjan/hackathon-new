import DashboardHeader from "@/components/dashboard/DashboardHeader";
import AIAgentsPanel from "@/components/dashboard/AIAgentsPanel";
import GlobalPortStatus from "@/components/dashboard/GlobalPortStatus";
import ToolCallsPanel from "@/components/dashboard/ToolCallsPanel";
import WorkflowProgress from "@/components/dashboard/WorkflowProgress";
import PerformanceMetrics from "@/components/dashboard/PerformanceMetrics";
import AgentNetwork from "@/components/dashboard/AgentNetwork";
import AnalyticsDashboard from "@/components/dashboard/AnalyticsDashboard";
import RealTimeAlerts from "@/components/dashboard/RealTimeAlerts";
import AINetworkVisualization from "@/components/dashboard/AINetworkVisualization";
import ShipmentsTracking from "@/components/dashboard/ShipmentsTracking";
import AuditLog from "@/components/dashboard/AuditLog";
import IntegrationsStatus from "@/components/dashboard/IntegrationsStatus";
import DisruptionSimulator from "@/components/dashboard/DisruptionSimulator";
import AIActionPlan from "@/components/dashboard/AIActionPlan";
import LLMToolsPanel from "@/components/dashboard/LLMToolsPanel";
import HealthStatus from "@/components/dashboard/HealthStatus";
import TraccarDevices from "@/components/dashboard/TraccarDevices";
import { AISimulationProvider } from "@/contexts/AISimulationContext";

const Index = () => {
  return (
    <AISimulationProvider>
      <div className="min-h-screen bg-gradient-to-br from-background to-secondary/20">
        <DashboardHeader />
        <div className="w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 sm:py-6 lg:py-8">
          <div className="mb-4"><HealthStatus /></div>
          {/* Main Dashboard Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-4 lg:gap-6 mb-6 lg:mb-8">
            {/* Left Column - AI Agents */}
            <div className="lg:col-span-3 space-y-4 lg:space-y-6">
              <div id="ai-agents">
                <AIAgentsPanel />
              </div>
              <div id="ai-network">
                <AgentNetwork />
              </div>
              <div className="mt-4"><TraccarDevices /></div>
            </div>
            {/* Center Column - Main Content */}
            <div className="lg:col-span-6 space-y-4 lg:space-y-6">
              <div id="port-status">
                <GlobalPortStatus />
              </div>
              <WorkflowProgress />
              <div className="mt-4"><DisruptionSimulator /></div>
              <div className="mt-4"><AIActionPlan /></div>
              <div className="mt-4"><LLMToolsPanel /></div>
            </div>
            {/* Right Column - Metrics & Tools */}
            <div className="lg:col-span-3 space-y-4 lg:space-y-6">
              <ToolCallsPanel />
              <PerformanceMetrics />
            </div>
          </div>
          {/* Analytics Section */}
          <div id="analytics-section" className="mb-6 lg:mb-8">
            <AnalyticsDashboard />
          </div>
          {/* Alerts and Network Visualization */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 lg:gap-6 mb-6 lg:mb-8">
            <div id="alerts-section">
              <RealTimeAlerts />
            </div>
            <AINetworkVisualization />
          </div>
          {/* Shipments Tracking */}
          <div id="shipments-section" className="mb-6 lg:mb-8">
            <ShipmentsTracking />
          </div>
          {/* Integrations Status */}
          <div id="integrations-section" className="mb-6 lg:mb-8">
            <IntegrationsStatus />
          </div>
          {/* Audit Log */}
          <div id="audit-section" className="mb-6 lg:mb-8">
            <AuditLog />
          </div>
        </div>
      </div>
    </AISimulationProvider>
  );
};

export default Index;
