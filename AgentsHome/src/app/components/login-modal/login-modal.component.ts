import { Component, Output, EventEmitter } from '@angular/core';
import { AuthService } from '../../core/services/auth.service';

@Component({
  selector: 'app-login-modal',
  templateUrl: './login-modal.component.html',
  styleUrls: ['./login-modal.component.scss']
})
export class LoginModalComponent {
  @Output() close = new EventEmitter<void>();
  @Output() onSuccess = new EventEmitter<void>();

  showPassword = false;
  isLoading = false;
  email = '';
  password = '';
  errorMessage = '';

  // Test credentials
  testEmail = 'test@agentshome.com';
  testPassword = 'TestPassword123';

  constructor(private authService: AuthService) {}

  testLogin() {
    this.isLoading = true;
    this.errorMessage = '';
    
    console.log('Test login attempt:', { email: this.testEmail });
    
    this.authService.login(this.testEmail, this.testPassword).subscribe({
      next: (response) => {
        console.log('Test login successful:', response);
        this.isLoading = false;
        this.onSuccess.emit(); // Parent will navigate to dashboard
      },
      error: (error) => {
        console.error('Test login error:', error);
        this.isLoading = false;
        this.errorMessage = error?.error?.detail || 'Test login failed. Backend may be unavailable.';
      }
    });
  }

  onSubmit() {
    if (this.email && this.password && !this.isLoading) {
      this.isLoading = true;
      this.errorMessage = '';
      
      console.log('Login attempt:', { email: this.email });
      
      this.authService.login(this.email, this.password).subscribe({
        next: (response) => {
          console.log('Login successful:', response);
          this.isLoading = false;
          this.onSuccess.emit(); // Parent will navigate to dashboard
        },
        error: (error) => {
          console.error('Login error:', error);
          this.isLoading = false;
          this.errorMessage = error?.error?.detail || 'Login failed. Please check your credentials.';
        }
      });
    }
  }

  togglePasswordVisibility() {
    this.showPassword = !this.showPassword;
  }

  closeModal() {
    this.close.emit();
  }
}
