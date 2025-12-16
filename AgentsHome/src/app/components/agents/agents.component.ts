import { Component } from '@angular/core';

interface Agent {
  id: number;
  name: string;
  role: string;
  icon: string;
  image?: string;
  features: string[];
  includes: string[];
  status: 'live' | 'coming-soon';
  roiMetrics: string[];
  successMetrics?: string[];
}

@Component({
  selector: 'app-agents',
  templateUrl: './agents.component.html',
  styleUrls: ['./agents.component.scss']
})
export class AgentsComponent {
  agents: Agent[] = [
    {
      id: 1,
      name: 'The Hunter',
      role: 'Lead Generation Expert',
      icon: '🎯',
      image: 'assets/images/The_Hunter.png',
      features: ['Autonomous lead scraping', 'Multi-source discovery', 'Lead qualification scoring'],
      includes: ['50+ leads/day', 'Multi-source scraping', 'Lead qualification', 'Email discovery', 'Daily reports'],
      status: 'live',
      roiMetrics: ['50+ leads/day', '₹10/lead cost', '24/7 automation'],
      successMetrics: ['2,500+ leads generated', '8 business sectors covered', 'Live on Azure']
    },
    {
      id: 2,
      name: 'The Enricher',
      role: 'Data Enrichment Agent',
      icon: '✨',
      image: 'assets/images/The_Enricher.png',
      features: ['Email discovery', 'Company insights', 'Decision-maker identification'],
      includes: ['95% data accuracy', 'Email validation', 'Company insights', 'Decision-maker data', 'Real-time API'],
      status: 'coming-soon',
      roiMetrics: ['95% data accuracy', 'Real-time enrichment', 'Multi-channel validation']
    },
    {
      id: 3,
      name: 'The Messenger',
      role: 'Email Outreach Agent',
      icon: '📧',
      image: 'assets/images/The_Messanger.png',
      features: ['Personalized emails', 'A/B testing', 'Follow-up automation'],
      includes: ['Personalized emails', 'A/B testing', 'Follow-up automation', 'Deliverability tracking', '30%+ open rates'],
      status: 'coming-soon',
      roiMetrics: ['30%+ open rates', 'Smart scheduling', 'Deliverability optimized']
    }
  ];
}
