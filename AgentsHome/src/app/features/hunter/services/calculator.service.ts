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
  // Use proxy route - will be forwarded to TheHunter backend on port 8001
  private apiBaseUrl = '/api/hunter';

  constructor(private http: HttpClient) { }

  calculate(request: CalculationRequest): Observable<Calculation> {
    return this.http.post<Calculation>(`${this.apiBaseUrl}/calculate`, request);
  }

  getHistory(): Observable<Calculation[]> {
    return this.http.get<Calculation[]>(`${this.apiBaseUrl}/history`);
  }

  getCalculation(id: number): Observable<Calculation> {
    return this.http.get<Calculation>(`${this.apiBaseUrl}/calculation/${id}`);
  }
}
