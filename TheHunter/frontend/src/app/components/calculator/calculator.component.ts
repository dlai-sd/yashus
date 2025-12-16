import { Component, OnInit } from '@angular/core';
import { CalculatorService, Calculation } from '../../services/calculator.service';

@Component({
  selector: 'app-calculator',
  templateUrl: './calculator.component.html',
  styleUrls: ['./calculator.component.css']
})
export class CalculatorComponent implements OnInit {
  operand1: number | null = null;
  operand2: number | null = null;
  operation: string = 'add';
  result: number | null = null;
  history: Calculation[] = [];
  loading: boolean = false;
  error: string | null = null;

  constructor(private calculatorService: CalculatorService) { }

  ngOnInit(): void {
    this.loadHistory();
  }

  onCalculate(): void {
    if (this.operand1 === null || this.operand2 === null) {
      this.error = 'Please enter both numbers';
      return;
    }

    this.loading = true;
    this.error = null;

    this.calculatorService.calculate({
      operation: this.operation,
      operand1: this.operand1,
      operand2: this.operand2
    }).subscribe({
      next: (response) => {
        this.result = response.result;
        this.loading = false;
        this.loadHistory();
      },
      error: (err) => {
        this.error = err.error?.detail || 'An error occurred during calculation';
        this.loading = false;
      }
    });
  }

  loadHistory(): void {
    this.calculatorService.getHistory().subscribe({
      next: (data) => {
        this.history = data.reverse(); // Show newest first
      },
      error: (err) => {
        console.error('Failed to load history', err);
      }
    });
  }
}
