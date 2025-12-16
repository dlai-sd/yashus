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

interface Release {
  version: string;
  date: string;
  features: string[];
}

interface Feature {
  title: string;
  description: string;
  isNew: boolean;
}

interface UnexploredFeature {
  title: string;
  description: string;
  plan: string;
  icon: string;
}

interface FAQItem {
  question: string;
  answer: string;
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

  // Right panel data
  upcomingReleases: Release[] = [];
  currentReleaseFeatures: Feature[] = [];
  unexploredFeatures: UnexploredFeature[] = [];
  faqItems: FAQItem[] = [];
  
  expandedFAQIndex: number | null = null;

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
    this.loadRightPanelData();
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

  loadRightPanelData(): void {
    // Upcoming releases
    this.upcomingReleases = [
      {
        version: '2.1',
        date: 'Jan 2025',
        features: ['Advanced Analytics', 'Custom Workflows']
      },
      {
        version: '2.2',
        date: 'Feb 2025',
        features: ['AI Insights', 'Team Collaboration']
      }
    ];

    // Current release features
    this.currentReleaseFeatures = [
      {
        title: 'Smart Agent Creation',
        description: 'AI-powered agent setup wizard',
        isNew: true
      },
      {
        title: 'Real-time Analytics',
        description: 'Live performance monitoring dashboard',
        isNew: true
      },
      {
        title: 'API Integration',
        description: 'Connect with external tools and services',
        isNew: false
      }
    ];

    // Unexplored features in subscription
    this.unexploredFeatures = [
      {
        title: 'Advanced AI Training',
        description: 'Custom model training for your specific use case',
        plan: 'Enterprise',
        icon: '🧠'
      },
      {
        title: 'Priority Support',
        description: '24/7 dedicated support team',
        plan: 'Premium',
        icon: '⭐'
      },
      {
        title: 'White-label Solution',
        description: 'Rebrand and resell agents to your clients',
        plan: 'Enterprise',
        icon: '🎨'
      },
      {
        title: 'Advanced Reporting',
        description: 'Custom reports and business intelligence',
        plan: 'Premium',
        icon: '📊'
      }
    ];

    // FAQ items
    this.faqItems = [
      {
        question: 'How do I create a new agent?',
        answer: 'Click on the "Agents" tab in the sidebar, then click "Create New Agent". Follow the wizard to set up your agent configuration.'
      },
      {
        question: 'What is the usage limit?',
        answer: 'Your Pro plan allows 5 agents with 10,000 API calls per agent per month. Monitor your usage in the Overview dashboard.'
      },
      {
        question: 'Can I upgrade my plan?',
        answer: 'Yes! Visit the Subscription section to view upgrade options. Changes take effect immediately.'
      },
      {
        question: 'How do I export my data?',
        answer: 'Go to Settings > Data Export. You can export agent performance, leads, and conversations in CSV or JSON format.'
      },
      {
        question: 'Is there API documentation?',
        answer: 'Yes, comprehensive API docs are available at https://docs.agentshome.com with code examples in multiple languages.'
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

  toggleFAQ(index: number): void {
    this.expandedFAQIndex = this.expandedFAQIndex === index ? null : index;
  }
}
