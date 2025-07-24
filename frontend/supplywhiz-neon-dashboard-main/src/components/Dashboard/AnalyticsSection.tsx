import { TrendingUp, TrendingDown, AlertTriangle, Package, Clock, MapPin } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, ResponsiveContainer, LineChart, Line, PieChart, Pie, Cell, Tooltip, Legend } from 'recharts';

const MetricCard = ({ title, value, change, trend, icon: Icon, description }: {
  title: string;
  value: string;
  change: string;
  trend: 'up' | 'down';
  icon: any;
  description: string;
}) => {
  const TrendIcon = trend === 'up' ? TrendingUp : TrendingDown;
  const trendColor = trend === 'up' ? 'text-primary' : 'text-destructive';
  
  return (
    <Card className="glass-card card-hover">
      <CardContent className="p-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="p-2 rounded-lg bg-muted/50">
              <Icon className="w-5 h-5 text-accent" />
            </div>
            <div>
              <p className="text-sm text-muted-foreground">{title}</p>
              <p className="text-2xl font-bold">{value}</p>
            </div>
          </div>
          <div className={`flex items-center space-x-1 ${trendColor}`}>
            <TrendIcon className="w-4 h-4" />
            <span className="text-sm font-medium">{change}</span>
          </div>
        </div>
        <p className="text-xs text-muted-foreground mt-2">{description}</p>
      </CardContent>
    </Card>
  );
};

const eventTypeData = [
  { name: 'Weather', value: 45, color: '#ff6b35' },
  { name: 'Traffic', value: 28, color: '#00ff88' },
  { name: 'Supplier', value: 18, color: '#8b5cf6' },
  { name: 'Port', value: 12, color: '#06b6d4' },
  { name: 'Other', value: 8, color: '#f59e0b' }
];

const riskScoreData = [
  { time: '00:00', score: 65 },
  { time: '04:00', score: 72 },
  { time: '08:00', score: 58 },
  { time: '12:00', score: 83 },
  { time: '16:00', score: 76 },
  { time: '20:00', score: 69 },
];

const vendorImpactData = [
  { vendor: 'TechCorp', high: 12, medium: 8, low: 4 },
  { vendor: 'GlobalSupply', high: 8, medium: 15, low: 12 },
  { vendor: 'LogiTrans', high: 6, medium: 10, low: 18 },
  { vendor: 'QuickShip', high: 4, medium: 12, low: 8 },
];

const AnalyticsSection = () => {
  return (
    <div className="space-y-6">
      {/* Metric Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <MetricCard
          title="Total Alerts (24h)"
          value="127"
          change="+12%"
          trend="up"
          icon={AlertTriangle}
          description="Active disruption events"
        />
        <MetricCard
          title="Avg Risk Score"
          value="7.2"
          change="-8%"
          trend="down"
          icon={TrendingUp}
          description="Current supply chain risk level"
        />
        <MetricCard
          title="Common Disruption"
          value="Weather"
          change="45%"
          trend="up"
          icon={Package}
          description="Most frequent event type"
        />
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Event Types Bar Chart */}
        <Card className="glass-card">
          <CardHeader>
            <CardTitle className="text-lg font-semibold flex items-center space-x-2">
              <Package className="w-5 h-5 text-accent" />
              <span>Disruption Events by Type</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={eventTypeData}>
                <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                <XAxis 
                  dataKey="name" 
                  stroke="hsl(var(--muted-foreground))"
                  fontSize={12}
                />
                <YAxis 
                  stroke="hsl(var(--muted-foreground))"
                  fontSize={12}
                />
                <Tooltip 
                  contentStyle={{
                    backgroundColor: 'hsl(var(--card))',
                    border: '1px solid hsl(var(--border))',
                    borderRadius: '8px'
                  }}
                />
                <Bar dataKey="value" fill="hsl(var(--primary))" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Risk Score Line Chart */}
        <Card className="glass-card">
          <CardHeader>
            <CardTitle className="text-lg font-semibold flex items-center space-x-2">
              <TrendingUp className="w-5 h-5 text-accent" />
              <span>Risk Score Trend (24h)</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={riskScoreData}>
                <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                <XAxis 
                  dataKey="time" 
                  stroke="hsl(var(--muted-foreground))"
                  fontSize={12}
                />
                <YAxis 
                  stroke="hsl(var(--muted-foreground))"
                  fontSize={12}
                />
                <Tooltip 
                  contentStyle={{
                    backgroundColor: 'hsl(var(--card))',
                    border: '1px solid hsl(var(--border))',
                    borderRadius: '8px'
                  }}
                />
                <Line 
                  type="monotone" 
                  dataKey="score" 
                  stroke="hsl(var(--primary))" 
                  strokeWidth={3}
                  dot={{ fill: 'hsl(var(--primary))', strokeWidth: 2, r: 4 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      {/* Bottom Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Vendor Impact Pie Chart */}
        <Card className="glass-card">
          <CardHeader>
            <CardTitle className="text-lg font-semibold flex items-center space-x-2">
              <MapPin className="w-5 h-5 text-accent" />
              <span>Event Distribution</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={eventTypeData}
                  cx="50%"
                  cy="50%"
                  outerRadius={100}
                  fill="#8884d8"
                  dataKey="value"
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                  labelLine={false}
                >
                  {eventTypeData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip 
                  contentStyle={{
                    backgroundColor: 'hsl(var(--card))',
                    border: '1px solid hsl(var(--border))',
                    borderRadius: '8px'
                  }}
                />
              </PieChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Vendor Impact Stacked Bar */}
        <Card className="glass-card">
          <CardHeader>
            <CardTitle className="text-lg font-semibold flex items-center space-x-2">
              <Clock className="w-5 h-5 text-accent" />
              <span>Vendor Impact Analysis</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={vendorImpactData}>
                <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                <XAxis 
                  dataKey="vendor" 
                  stroke="hsl(var(--muted-foreground))"
                  fontSize={12}
                />
                <YAxis 
                  stroke="hsl(var(--muted-foreground))"
                  fontSize={12}
                />
                <Tooltip 
                  contentStyle={{
                    backgroundColor: 'hsl(var(--card))',
                    border: '1px solid hsl(var(--border))',
                    borderRadius: '8px'
                  }}
                />
                <Legend />
                <Bar dataKey="high" stackId="a" fill="hsl(var(--destructive))" name="High Risk" />
                <Bar dataKey="medium" stackId="a" fill="hsl(var(--secondary))" name="Medium Risk" />
                <Bar dataKey="low" stackId="a" fill="hsl(var(--primary))" name="Low Risk" />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default AnalyticsSection;