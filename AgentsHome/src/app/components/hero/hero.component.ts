import { Component, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-hero',
  templateUrl: './hero.component.html',
  styleUrls: ['./hero.component.scss']
})
export class HeroComponent {
  @Output() openSignup = new EventEmitter<void>();

  onFreeTrialClick() {
    this.openSignup.emit();
  }

  onScheduleConsultationClick() {
    this.openSignup.emit();
  }
}
