import { Component } from '@angular/core';

interface Step {
  number: number;
  title: string;
  description: string;
  icon: string;
}

@Component({
  selector: 'app-how-it-works',
  templateUrl: './how-it-works.component.html',
  styleUrls: ['./how-it-works.component.scss']
})
export class HowItWorksComponent {
  steps: Step[] = [
    {
      number: 1,
      title: 'Login',
      description: 'Sign up with your business details. Verify your email and secure your account with 2FA.',
      icon: '🔐'
    },
    {
      number: 2,
      title: 'Subscribe',
      description: 'Choose your agents and subscription plan. Select from individual agents or agent bundles.',
      icon: '💳'
    },
    {
      number: 3,
      title: 'Configure',
      description: 'Set parameters for lead generation. Define target industries, regions, and qualification criteria.',
      icon: '⚙️'
    },
    {
      number: 4,
      title: 'Start Working',
      description: 'Agents run 24/7 and deliver results. Monitor performance via dashboards and receive daily summaries.',
      icon: '🚀'
    }
  ];
}
