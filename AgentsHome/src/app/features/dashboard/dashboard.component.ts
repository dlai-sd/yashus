import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService, User } from '../../core/services/auth.service';

interface Agent {
  id: string;
  name: string;
  status: 'active' | 'inactive' | 'paused';
  usagePercentage: number;
  currentUsage: number;
  totalAllowed: number;
  type: string;
}

interface Subscription {
  plan: string;
  agentsAllowed: number;
  agentsUsed: number;
  renewalDate: string;
  status: 'active' | 'expired';
}

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit {
  currentUser: User | null = null;
  sidebarOpen = false; // Hide sidebar by default
  currentView = 'overview'; // overview, agents, leads, subscription, settings
  
  agents: Agent[] = [];
  subscription: Subscription = {
    plan: 'Pro',
    agentsAllowed: 5,
    agentsUsed: 3,
    renewalDate: '2025-01-16',
    status: 'active'
  };

  navigationItems = [
    { id: 'overview', label: 'Overview', icon: '📊' },
    { id: 'agents', label: 'Agents', icon: '🤖' },
    { id: 'leads', label: 'Leads', icon: '📋' },
    { id: 'subscription', label: 'Subscription', icon: '💳' },
    { id: 'settings', label: 'Settings', icon: '⚙️' }
  ];

  constructor(
    private authService: AuthService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.authService.currentUser$.subscribe(user => {
      this.currentUser = user;
      console.log('Dashboard received user:', user);
    });
    
    // Load mock data
    this.loadAgents();
  }

  loadAgents(): void {
    // Mock data - will be replaced with API calls
    this.agents = [
      {
        id: 'agent-1',
        name: 'Sales Hunter Pro',
        status: 'active',
        usagePercentage: 75,
        currentUsage: 7500,
        totalAllowed: 10000,
        type: 'Sales'
      },
      {
        id: 'agent-2',
        name: 'Lead Gen AI',
        status: 'active',
        usagePercentage: 45,
        currentUsage: 4500,
        totalAllowed: 10000,
        type: 'Lead Generation'
      },
      {
        id: 'agent-3',
        name: 'Customer Support Bot',
        status: 'inactive',
        usagePercentage: 0,
        currentUsage: 0,
        totalAllowed: 10000,
        type: 'Support'
      }
    ];
  }

  setView(viewId: string): void {
    this.currentView = viewId;
  }

  toggleSidebar(): void {
    this.sidebarOpen = !this.sidebarOpen;
  }

  logout(): void {
    this.authService.logout();
    this.router.navigate(['/']);
  }

  getStatusClass(status: string): string {
    return `status-${status}`;
  }

  getUsageBarColor(percentage: number): string {
    if (percentage >= 80) return 'critical';
    if (percentage >= 50) return 'warning';
    return 'normal';
  }
}
