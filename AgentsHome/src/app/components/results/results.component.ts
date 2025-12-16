import { Component } from '@angular/core';

interface ResultMetric {
  label: string;
  value: string;
  icon: string;
}

@Component({
  selector: 'app-results',
  templateUrl: './results.component.html',
  styleUrls: ['./results.component.scss']
})
export class ResultsComponent {
  metrics: ResultMetric[] = [
    {
      label: 'Leads Generated',
      value: '2,500+',
      icon: '🎯'
    },
    {
      label: 'Industry Coverage',
      value: '8 Sectors',
      icon: '🏢'
    },
    {
      label: 'Cost Per Lead',
      value: '₹10',
      icon: '💰'
    },
    {
      label: 'Automation Hours',
      value: '24/7',
      icon: '⏰'
    }
  ];
}
