import { Component } from '@angular/core';

interface FAQItem {
  question: string;
  answer: string;
  open?: boolean;
}

@Component({
  selector: 'app-faq',
  templateUrl: './faq.component.html',
  styleUrls: ['./faq.component.scss']
})
export class FAQComponent {
  faqs: FAQItem[] = [
    {
      question: 'How does The Hunter find leads?',
      answer: 'The Hunter uses advanced web scraping and AI to discover businesses on Google Maps, directories, and industry databases. It analyzes websites, extracts contact info, and qualifies leads based on your criteria.',
      open: false
    },
    {
      question: 'What industries does it work with?',
      answer: 'The Hunter works with any B2B industry: Healthcare, Hospitality, Real Estate, E-commerce, Food & Beverage, Manufacturing, Services, and more. You define the target niche.',
      open: false
    },
    {
      question: 'Can I customize lead criteria?',
      answer: 'Yes. Define target locations, business types, revenue ranges, employee counts, and custom filters. The Hunter learns from your feedback and improves qualification.',
      open: false
    },
    {
      question: 'How many leads can I expect per month?',
      answer: 'On average, 1,500+ qualified leads per month, depending on industry availability and your configuration. The Hunter discovers 50+ leads daily across all niches combined.',
      open: false
    },
    {
      question: 'What data is included with each lead?',
      answer: 'Company name, address, phone, website, email (when found), business category, ratings, website snippets, and custom hooks from their latest content.',
      open: false
    },
    {
      question: 'Can I integrate with my CRM?',
      answer: 'Yes. Leads are exported as CSV daily. Integration with HubSpot, Pipedrive, and other CRMs via API is available in premium plans.',
      open: false
    },
    {
      question: 'Is my data secure?',
      answer: 'Absolutely. All data is encrypted in transit and at rest. We comply with GDPR, CCPA, and Indian data protection laws. No third-party access.',
      open: false
    },
    {
      question: 'What if I\'m not satisfied?',
      answer: 'Try free for 7 days. Cancel anytime with no penalties. If you\'re unhappy, we offer a 30-day satisfaction guarantee for first payments.',
      open: false
    }
  ];

  toggleFAQ(index: number) {
    this.faqs[index].open = !this.faqs[index].open;
  }
}
