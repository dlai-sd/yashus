import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.scss'
})
export class DashboardComponent implements OnInit {
  stats = {
    totalAgents: 0,
    activeTasks: 0,
    completedTasks: 0,
    failedTasks: 0
  };
  recentTasks: any[] = [];
  loading = true;

  constructor(private apiService: ApiService) {}

  ngOnInit() {
    this.loadDashboardData();
  }

  loadDashboardData() {
    this.loading = true;

    // Load agents
    this.apiService.getAgents().subscribe({
      next: (data) => {
        this.stats.totalAgents = data.total;
      },
      error: (error) => console.error('Error loading agents:', error)
    });

    // Load tasks
    this.apiService.listTasks().subscribe({
      next: (data) => {
        this.recentTasks = data.tasks.slice(0, 5);
        this.stats.activeTasks = data.tasks.filter((t: any) => 
          t.status === 'pending' || t.status === 'running'
        ).length;
        this.stats.completedTasks = data.tasks.filter((t: any) => 
          t.status === 'completed'
        ).length;
        this.stats.failedTasks = data.tasks.filter((t: any) => 
          t.status === 'failed'
        ).length;
        this.loading = false;
      },
      error: (error) => {
        console.error('Error loading tasks:', error);
        this.loading = false;
      }
    });
  }
}
