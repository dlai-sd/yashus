import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable } from 'rxjs';
import { tap, map } from 'rxjs/operators';

export interface User {
  id: string;
  email: string;
  name: string;
  provider: string; // 'google', 'github', 'microsoft', 'linkedin', 'apple', 'email'
}

export interface AuthResponse {
  token: string;
  user: User;
}

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl: string;
  private currentUserSubject = new BehaviorSubject<User | null>(null);
  public currentUser$ = this.currentUserSubject.asObservable();

  constructor(private http: HttpClient) {
    // Dynamically build API URL based on current hostname
    const hostname = window.location.hostname;
    const port = 8000;
    
    if (hostname === 'localhost' || hostname === '127.0.0.1') {
      // Local development
      this.apiUrl = `http://localhost:${port}/api/auth`;
    } else {
      // GitHub Codespace or deployed environment
      // Example: ubiquitous-waddle-v69grgqwjxq436gv5-4200.app.github.dev
      // Replace -4200. with -8000.
      const baseHostname = hostname.replace(/-\d+\.app\.github\.dev$/, `-${port}.app.github.dev`);
      this.apiUrl = `https://${baseHostname}/api/auth`;
    }
    
    console.log('Auth Service initialized with API URL:', this.apiUrl);
    this.loadUserFromStorage();
  }

  login(email: string, password: string): Observable<AuthResponse> {
    return this.http.post<AuthResponse>(`${this.apiUrl}/login`, { email, password })
      .pipe(
        tap(response => this.setUser(response.token, response.user))
      );
  }

  signup(email: string, password: string, name: string): Observable<AuthResponse> {
    return this.http.post<AuthResponse>(`${this.apiUrl}/signup`, { email, password, name })
      .pipe(
        tap(response => this.setUser(response.token, response.user))
      );
  }

  // SSO Callback handler
  ssoCallback(provider: string, code: string): Observable<AuthResponse> {
    return this.http.post<AuthResponse>(`${this.apiUrl}/sso-callback`, { provider, code })
      .pipe(
        tap(response => this.setUser(response.token, response.user))
      );
  }

  logout(): void {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    this.currentUserSubject.next(null);
  }

  isAuthenticated(): boolean {
    return !!localStorage.getItem('token');
  }

  getToken(): string | null {
    return localStorage.getItem('token');
  }

  getCurrentUser(): User | null {
    return this.currentUserSubject.value;
  }

  private setUser(token: string, user: User): void {
    localStorage.setItem('token', token);
    localStorage.setItem('user', JSON.stringify(user));
    this.currentUserSubject.next(user);
  }

  private loadUserFromStorage(): void {
    const userStr = localStorage.getItem('user');
    if (userStr) {
      this.currentUserSubject.next(JSON.parse(userStr));
    }
  }

  refreshToken(): Observable<AuthResponse> {
    return this.http.post<AuthResponse>(`${this.apiUrl}/refresh`, {})
      .pipe(
        tap(response => this.setUser(response.token, response.user))
      );
  }
}
