
import { useState } from "react";
import { Settings as SettingsIcon, User, Bell, Shield, Map, Database, Zap, Save } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Switch } from "@/components/ui/switch";
import { Badge } from "@/components/ui/badge";
import Header from "@/components/Dashboard/Header";

const Settings = () => {
  const [activeTab, setActiveTab] = useState("profile");
  const [settings, setSettings] = useState({
    // Profile Settings
    profile: {
      name: "John Doe",
      email: "john.doe@supplywhiz.com",
      role: "Supply Chain Manager",
      company: "Global Logistics Corp",
      timezone: "UTC-8",
      language: "English"
    },
    
    // Notification Settings
    notifications: {
      emailAlerts: true,
      pushNotifications: true,
      smsAlerts: false,
      weeklyReports: true,
      criticalOnly: false,
      alertTypes: {
        weather: true,
        traffic: true,
        supplier: true,
        port: true,
        geopolitical: false,
        cyber: true
      }
    },
    
    // Security Settings
    security: {
      twoFactorAuth: true,
      sessionTimeout: 30,
      passwordExpiry: 90,
      loginNotifications: true,
      ipWhitelisting: false
    },
    
    // Map Settings
    map: {
      defaultView: "supply-chain",
      autoRefresh: true,
      refreshInterval: 30,
      showRiskOverlay: true,
      showTradeRoutes: true,
      clusterMarkers: true,
      mapProvider: "mapbox"
    },
    
    // Data Settings
    data: {
      dataRetention: 365,
      autoBackup: true,
      backupFrequency: "daily",
      dataExportFormat: "json",
      anonymizeData: false
    },
    
    // AI Agent Settings
    agents: {
      autoMitigation: false,
      confidenceThreshold: 0.8,
      escalationLevel: "high",
      learningMode: true,
      customRules: []
    }
  });

  const tabs = [
    { id: "profile", label: "Profile", icon: User },
    { id: "notifications", label: "Notifications", icon: Bell },
    { id: "security", label: "Security", icon: Shield },
    { id: "map", label: "Map Settings", icon: Map },
    { id: "data", label: "Data Management", icon: Database },
    { id: "agents", label: "AI Agents", icon: Zap }
  ];

  const handleSettingChange = (category: string, key: string, value: any) => {
    setSettings(prev => ({
      ...prev,
      [category]: {
        ...prev[category],
        [key]: value
      }
    }));
  };

  const handleNestedSettingChange = (category: string, parentKey: string, key: string, value: any) => {
    setSettings(prev => ({
      ...prev,
      [category]: {
        ...prev[category],
        [parentKey]: {
          ...prev[category][parentKey],
          [key]: value
        }
      }
    }));
  };

  const renderProfileSettings = () => (
    <Card className="glass-card">
      <CardHeader>
        <CardTitle>Profile Information</CardTitle>
      </CardHeader>
      <CardContent className="space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <Label htmlFor="name">Full Name</Label>
            <Input 
              id="name"
              value={settings.profile.name}
              onChange={(e) => handleSettingChange("profile", "name", e.target.value)}
            />
          </div>
          <div>
            <Label htmlFor="email">Email Address</Label>
            <Input 
              id="email"
              type="email"
              value={settings.profile.email}
              onChange={(e) => handleSettingChange("profile", "email", e.target.value)}
            />
          </div>
          <div>
            <Label htmlFor="role">Role</Label>
            <select 
              id="role"
              value={settings.profile.role}
              onChange={(e) => handleSettingChange("profile", "role", e.target.value)}
              className="w-full px-3 py-2 rounded-lg bg-muted border border-border text-foreground"
            >
              <option value="Supply Chain Manager">Supply Chain Manager</option>
              <option value="Logistics Coordinator">Logistics Coordinator</option>
              <option value="Operations Director">Operations Director</option>
              <option value="Risk Analyst">Risk Analyst</option>
            </select>
          </div>
          <div>
            <Label htmlFor="company">Company</Label>
            <Input 
              id="company"
              value={settings.profile.company}
              onChange={(e) => handleSettingChange("profile", "company", e.target.value)}
            />
          </div>
          <div>
            <Label htmlFor="timezone">Timezone</Label>
            <select 
              id="timezone"
              value={settings.profile.timezone}
              onChange={(e) => handleSettingChange("profile", "timezone", e.target.value)}
              className="w-full px-3 py-2 rounded-lg bg-muted border border-border text-foreground"
            >
              <option value="UTC-8">Pacific Time (UTC-8)</option>
              <option value="UTC-5">Eastern Time (UTC-5)</option>
              <option value="UTC+0">Greenwich Mean Time (UTC+0)</option>
              <option value="UTC+8">China Standard Time (UTC+8)</option>
            </select>
          </div>
          <div>
            <Label htmlFor="language">Language</Label>
            <select 
              id="language"
              value={settings.profile.language}
              onChange={(e) => handleSettingChange("profile", "language", e.target.value)}
              className="w-full px-3 py-2 rounded-lg bg-muted border border-border text-foreground"
            >
              <option value="English">English</option>
              <option value="Chinese">Chinese</option>
              <option value="Spanish">Spanish</option>
              <option value="French">French</option>
            </select>
          </div>
        </div>
      </CardContent>
    </Card>
  );

  const renderNotificationSettings = () => (
    <div className="space-y-6">
      <Card className="glass-card">
        <CardHeader>
          <CardTitle>Notification Preferences</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <Label>Email Alerts</Label>
              <p className="text-sm text-muted-foreground">Receive alerts via email</p>
            </div>
            <Switch 
              checked={settings.notifications.emailAlerts}
              onCheckedChange={(checked) => handleSettingChange("notifications", "emailAlerts", checked)}
            />
          </div>
          
          <div className="flex items-center justify-between">
            <div>
              <Label>Push Notifications</Label>
              <p className="text-sm text-muted-foreground">Browser push notifications</p>
            </div>
            <Switch 
              checked={settings.notifications.pushNotifications}
              onCheckedChange={(checked) => handleSettingChange("notifications", "pushNotifications", checked)}
            />
          </div>
          
          <div className="flex items-center justify-between">
            <div>
              <Label>SMS Alerts</Label>
              <p className="text-sm text-muted-foreground">Critical alerts via SMS</p>
            </div>
            <Switch 
              checked={settings.notifications.smsAlerts}
              onCheckedChange={(checked) => handleSettingChange("notifications", "smsAlerts", checked)}
            />
          </div>
          
          <div className="flex items-center justify-between">
            <div>
              <Label>Weekly Reports</Label>
              <p className="text-sm text-muted-foreground">Summary reports every week</p>
            </div>
            <Switch 
              checked={settings.notifications.weeklyReports}
              onCheckedChange={(checked) => handleSettingChange("notifications", "weeklyReports", checked)}
            />
          </div>
        </CardContent>
      </Card>

      <Card className="glass-card">
        <CardHeader>
          <CardTitle>Alert Types</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {Object.entries(settings.notifications.alertTypes).map(([type, enabled]) => (
            <div key={type} className="flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <span className="capitalize">{type}</span>
                <Badge variant="outline" className="text-xs">
                  {type === "weather" ? "🌪️" : 
                   type === "traffic" ? "🚦" :
                   type === "supplier" ? "🏭" :
                   type === "port" ? "⚓" :
                   type === "geopolitical" ? "🌍" : "🔒"}
                </Badge>
              </div>
              <Switch 
                checked={enabled}
                onCheckedChange={(checked) => handleNestedSettingChange("notifications", "alertTypes", type, checked)}
              />
            </div>
          ))}
        </CardContent>
      </Card>
    </div>
  );

  const renderMapSettings = () => (
    <Card className="glass-card">
      <CardHeader>
        <CardTitle>Map Configuration</CardTitle>
      </CardHeader>
      <CardContent className="space-y-6">
        <div>
          <Label htmlFor="defaultView">Default Map View</Label>
          <select 
            id="defaultView"
            value={settings.map.defaultView}
            onChange={(e) => handleSettingChange("map", "defaultView", e.target.value)}
            className="w-full px-3 py-2 rounded-lg bg-muted border border-border text-foreground mt-2"
          >
            <option value="supply-chain">Supply Chain</option>
            <option value="risk-analysis">Risk Analysis</option>
            <option value="trade-routes">Trade Routes</option>
            <option value="capacity-usage">Capacity Usage</option>
          </select>
        </div>
        
        <div className="flex items-center justify-between">
          <div>
            <Label>Auto Refresh</Label>
            <p className="text-sm text-muted-foreground">Automatically refresh map data</p>
          </div>
          <Switch 
            checked={settings.map.autoRefresh}
            onCheckedChange={(checked) => handleSettingChange("map", "autoRefresh", checked)}
          />
        </div>
        
        <div>
          <Label htmlFor="refreshInterval">Refresh Interval (seconds)</Label>
          <Input 
            id="refreshInterval"
            type="number"
            value={settings.map.refreshInterval}
            onChange={(e) => handleSettingChange("map", "refreshInterval", parseInt(e.target.value))}
            className="mt-2"
          />
        </div>
        
        <div className="flex items-center justify-between">
          <div>
            <Label>Show Risk Overlay</Label>
            <p className="text-sm text-muted-foreground">Display risk heatmap on map</p>
          </div>
          <Switch 
            checked={settings.map.showRiskOverlay}
            onCheckedChange={(checked) => handleSettingChange("map", "showRiskOverlay", checked)}
          />
        </div>
        
        <div className="flex items-center justify-between">
          <div>
            <Label>Show Trade Routes</Label>
            <p className="text-sm text-muted-foreground">Display active trade routes</p>
          </div>
          <Switch 
            checked={settings.map.showTradeRoutes}
            onCheckedChange={(checked) => handleSettingChange("map", "showTradeRoutes", checked)}
          />
        </div>
      </CardContent>
    </Card>
  );

  const renderContent = () => {
    switch (activeTab) {
      case "profile":
        return renderProfileSettings();
      case "notifications":
        return renderNotificationSettings();
      case "map":
        return renderMapSettings();
      default:
        return (
          <Card className="glass-card">
            <CardContent className="p-8 text-center">
              <h3 className="text-lg font-medium mb-2">{tabs.find(t => t.id === activeTab)?.label}</h3>
              <p className="text-muted-foreground">Settings for this section are coming soon.</p>
            </CardContent>
          </Card>
        );
    }
  };

  return (
    <div className="min-h-screen bg-gradient-dark font-inter">
      <Header />
      
      <main className="container mx-auto px-6 py-8">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gradient-primary">Settings</h1>
            <p className="text-muted-foreground mt-2">Manage your account and application preferences</p>
          </div>
          
          <Button variant="cta" className="flex items-center space-x-2">
            <Save className="w-4 h-4" />
            <span>Save Changes</span>
          </Button>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Settings Navigation */}
          <div className="lg:col-span-1">
            <Card className="glass-card">
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <SettingsIcon className="w-5 h-5" />
                  <span>Settings</span>
                </CardTitle>
              </CardHeader>
              <CardContent className="p-0">
                <nav className="space-y-1">
                  {tabs.map((tab) => {
                    const Icon = tab.icon;
                    return (
                      <button
                        key={tab.id}
                        onClick={() => setActiveTab(tab.id)}
                        className={`w-full flex items-center space-x-3 px-4 py-3 text-left rounded-lg transition-colors ${
                          activeTab === tab.id 
                            ? "bg-primary/10 text-primary border-r-2 border-primary" 
                            : "hover:bg-muted/50 text-muted-foreground"
                        }`}
                      >
                        <Icon className="w-4 h-4" />
                        <span>{tab.label}</span>
                      </button>
                    );
                  })}
                </nav>
              </CardContent>
            </Card>
          </div>

          {/* Settings Content */}
          <div className="lg:col-span-3">
            {renderContent()}
          </div>
        </div>
      </main>
    </div>
  );
};

export default Settings;
