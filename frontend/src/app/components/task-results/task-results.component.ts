import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService, Task, TaskResult } from '../../services/api.service';

@Component({
  selector: 'app-task-results',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './task-results.component.html',
  styleUrl: './task-results.component.scss'
})
export class TaskResultsComponent implements OnInit {
  tasks: Task[] = [];
  selectedTask: Task | null = null;
  selectedResult: TaskResult | null = null;
  loading = true;
  loadingResult = false;

  constructor(private apiService: ApiService) {}

  ngOnInit() {
    this.loadTasks();
  }

  loadTasks() {
    this.loading = true;
    this.apiService.listTasks().subscribe({
      next: (data) => {
        this.tasks = data.tasks.reverse(); // Show newest first
        this.loading = false;
      },
      error: (error) => {
        console.error('Error loading tasks:', error);
        this.loading = false;
      }
    });
  }

  viewResult(task: Task) {
    this.selectedTask = task;
    this.selectedResult = null;
    this.loadingResult = true;

    this.apiService.getTaskResult(task.task_id).subscribe({
      next: (result) => {
        this.selectedResult = result;
        this.loadingResult = false;
      },
      error: (error) => {
        console.error('Error loading task result:', error);
        this.loadingResult = false;
        
        // If task is still running, show that message
        if (error.status === 202) {
          this.selectedResult = null;
        }
      }
    });
  }

  closeResult() {
    this.selectedTask = null;
    this.selectedResult = null;
  }
}
