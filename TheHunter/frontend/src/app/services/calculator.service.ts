import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Calculation {
  id: number;
  operation: string;
  operand1: number;
  operand2: number;
  result: number;
  created_at: string;
}

export interface CalculationRequest {
  operation: string;
  operand1: number;
  operand2: number;
}

@Injectable({
  providedIn: 'root'
})
export class CalculatorService {
  // Auto-detect API URL based on environment
  private apiUrl = this.getApiUrl();

  constructor(private http: HttpClient) { }

  private getApiUrl(): string {
    const hostname = window.location.hostname;
    const isAzure = hostname.includes('azurecontainer');
    
    if (isAzure) {
      // Running on Azure - use Azure backend URL
      return 'http://yashus-backend-api.westus2.azurecontainer.io:8000/api/v1/calculator';
    } else if (hostname === 'localhost' || hostname === '127.0.0.1') {
      // Running locally
      return 'http://localhost:8000/api/v1/calculator';
    } else {
      // Default fallback
      return 'http://localhost:8000/api/v1/calculator';
    }
  }

  calculate(request: CalculationRequest): Observable<Calculation> {
    return this.http.post<Calculation>(`${this.apiUrl}/calculate`, request);
  }

  getHistory(): Observable<Calculation[]> {
    return this.http.get<Calculation[]>(`${this.apiUrl}/history`);
  }

  getCalculation(id: number): Observable<Calculation> {
    return this.http.get<Calculation>(`${this.apiUrl}/calculation/${id}`);
  }
}
