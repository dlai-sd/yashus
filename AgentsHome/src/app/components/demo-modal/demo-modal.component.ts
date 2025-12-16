import { Component, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-demo-modal',
  templateUrl: './demo-modal.component.html',
  styleUrls: ['./demo-modal.component.scss']
})
export class DemoModalComponent {
  @Output() close = new EventEmitter<void>();

  youtubeUrl = 'https://www.youtube.com/embed/dQw4w9WgXcQ'; // Placeholder - replace with actual demo video

  closeModal() {
    this.close.emit();
  }
}
