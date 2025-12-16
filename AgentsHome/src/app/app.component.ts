import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from './core/services/auth.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  title = 'Yashus Digital Agents';
  showLoginModal = false;
  showSignupModal = false;
  isAuthenticated = false;

  constructor(
    private router: Router,
    private authService: AuthService
  ) {}

  ngOnInit() {
    // Subscribe to user changes to track authentication state
    this.authService.currentUser$.subscribe(user => {
      this.isAuthenticated = !!user;
      console.log('Auth state changed:', { isAuthenticated: this.isAuthenticated, user });
    });
  }

  toggleLoginModal() {
    this.showLoginModal = !this.showLoginModal;
    this.showSignupModal = false;
  }

  toggleSignupModal() {
    this.showSignupModal = !this.showSignupModal;
    this.showLoginModal = false;
  }

  onAuthSuccess() {
    console.log('Auth success - closing modals and navigating to dashboard');
    this.showLoginModal = false;
    this.showSignupModal = false;
    // Navigate to dashboard immediately
    this.router.navigate(['/dashboard']);
  }
}
