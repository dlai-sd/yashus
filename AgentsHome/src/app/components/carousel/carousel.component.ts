import { Component, OnInit, OnDestroy } from '@angular/core';

interface CarouselItem {
  title: string;
  icon: string;
  image?: string;
  benefits: string[];
}

@Component({
  selector: 'app-carousel',
  templateUrl: './carousel.component.html',
  styleUrls: ['./carousel.component.scss']
})
export class CarouselComponent implements OnInit, OnDestroy {
  carouselItems: CarouselItem[] = [
    {
      title: 'Doctors & Hospitals',
      icon: '🏥',
      image: 'assets/images/doctors-hospitals.png',
      benefits: ['Generate 50+ qualified patient leads monthly', 'Automate appointment booking and confirmations', 'Reduce administrative workload by 70%']
    },
    {
      title: 'Hotels & Resorts',
      icon: '🏨',
      image: 'assets/images/hotels-resorts.png',
      benefits: ['Automate corporate booking inquiries', 'Personalized guest outreach and follow-ups', 'Streamline event inquiry management']
    },
    {
      title: 'Builders & Real Estate',
      icon: '🏗️',
      image: 'assets/images/builders-realestate.png',
      benefits: ['24/7 automated lead qualification', 'Schedule site visits automatically', 'Nurture buyers through sales funnel']
    },
    {
      title: 'Brands & E-commerce',
      icon: '📦',
      image: 'assets/images/brands-ecommerce.png',
      benefits: ['Discover and qualify B2B partners', 'Automate distributor outreach campaigns', 'Match with relevant influencers']
    },
    {
      title: 'Food & Restaurants',
      icon: '🍽️',
      image: 'assets/images/food-restaurants.png',
      benefits: ['Generate catering and event leads', 'Manage supplier relationships efficiently', 'Automate bulk order inquiries']
    },
    {
      title: 'Education & Coaching',
      icon: '📚',
      image: 'assets/images/education-coaching.png',
      benefits: ['Attract and qualify student inquiries', 'Automate course enrollment follow-ups', 'Nurture prospective student leads']
    },
    {
      title: 'IT & Software Services',
      icon: '💻',
      image: 'assets/images/it-software.png',
      benefits: ['Identify qualified tech leads', 'Automate client onboarding process', 'Scale service delivery operations']
    },
    {
      title: 'Finance & Banking',
      icon: '🏦',
      image: 'assets/images/finance-banking.png',
      benefits: ['Generate high-value financial leads', 'Automate compliance and follow-ups', 'Build customer trust through personalization']
    },
    {
      title: 'Manufacturing & Industry',
      icon: '🏭',
      image: 'assets/images/manufacturing-industry.png',
      benefits: ['Find qualified B2B buyers', 'Automate supply chain inquiries', 'Streamline vendor relationships']
    }
  ];

  currentIndex = 0;
  autoRotateInterval: any;
  itemsPerView = 3;

  ngOnInit() {
    this.startAutoRotate();
  }

  ngOnDestroy() {
    if (this.autoRotateInterval) {
      clearInterval(this.autoRotateInterval);
    }
  }

  startAutoRotate() {
    this.autoRotateInterval = setInterval(() => {
      this.nextSlide();
    }, 5000);
  }

  nextSlide() {
    this.currentIndex = (this.currentIndex + 1) % this.carouselItems.length;
  }

  prevSlide() {
    this.currentIndex = (this.currentIndex - 1 + this.carouselItems.length) % this.carouselItems.length;
  }

  goToSlide(index: number) {
    this.currentIndex = index;
    this.restartAutoRotate();
  }

  restartAutoRotate() {
    if (this.autoRotateInterval) {
      clearInterval(this.autoRotateInterval);
    }
    this.startAutoRotate();
  }

  get visibleItems(): CarouselItem[] {
    const items = [];
    for (let i = 0; i < this.itemsPerView; i++) {
      items.push(this.carouselItems[(this.currentIndex + i) % this.carouselItems.length]);
    }
    return items;
  }

  getTotalSlides(): number {
    return this.carouselItems.length;
  }

  getCurrentSlide(): number {
    return this.currentIndex;
  }
}
