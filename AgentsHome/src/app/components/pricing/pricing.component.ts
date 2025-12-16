import { Component } from '@angular/core';

interface Plan {
  agent: string;
  price: number;
  icon: string;
  description: string;
  features: string[];
}

@Component({
  selector: 'app-pricing',
  templateUrl: './pricing.component.html',
  styleUrls: ['./pricing.component.scss']
})
export class PricingComponent {
  plans: Plan[] = [
    {
      agent: 'The Hunter',
      price: 4999,
      icon: '🎯',
      description: 'Lead Generation',
      features: ['50+ leads/day', 'Multi-source scraping', 'Lead qualification', 'Email discovery', 'Daily reports']
    },
    {
      agent: 'The Enricher',
      price: 4999,
      icon: '✨',
      description: 'Data Enrichment',
      features: ['95% data accuracy', 'Email validation', 'Company insights', 'Decision-maker data', 'Real-time API']
    },
    {
      agent: 'The Messenger',
      price: 4999,
      icon: '📧',
      description: 'Email Outreach',
      features: ['Personalized emails', 'A/B testing', 'Follow-up automation', 'Deliverability tracking', '30%+ open rates']
    },
    {
      agent: 'The Amplifier',
      price: 4999,
      icon: '📱',
      description: 'Social Media',
      features: ['LinkedIn automation', 'Multi-platform posting', 'Engagement tracking', 'Content scheduling', 'Analytics']
    },
    {
      agent: 'The Analyst',
      price: 4999,
      icon: '📊',
      description: 'Analytics & Reporting',
      features: ['Real-time dashboards', 'Custom reports', 'ROI tracking', 'Predictive analytics', 'CSV exports']
    }
  ];

  bundleDiscount = 'Buy 8 agents, get 1 FREE';
  
  getTotalPrice(agentsCount: number): number {
    const basePrice = 4999 * agentsCount;
    if (agentsCount >= 8) {
      return basePrice - 4999; // One free
    }
    return basePrice;
  }

  getSavings(agentsCount: number): number {
    if (agentsCount >= 8) {
      return 4999;
    }
    return 0;
  }
}
