import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-task-create',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './task-create.component.html',
  styleUrl: './task-create.component.scss'
})
export class TaskCreateComponent implements OnInit {
  agentTypes: any[] = [];
  selectedAgentType = 'sales_hunter';
  
  // Sales Hunter specific fields
  searchPhrase = '';
  location = '';
  radius = 5000;
  maxResults = 20;
  
  loading = false;
  error = '';
  success = '';

  constructor(
    private apiService: ApiService,
    private router: Router
  ) {}

  ngOnInit() {
    this.loadAgentTypes();
  }

  loadAgentTypes() {
    this.apiService.getAgentTypes().subscribe({
      next: (data) => {
        this.agentTypes = data.agent_types;
      },
      error: (error) => {
        console.error('Error loading agent types:', error);
        this.error = 'Failed to load agent types';
      }
    });
  }

  createTask() {
    this.error = '';
    this.success = '';
    
    // Validate inputs
    if (!this.searchPhrase.trim()) {
      this.error = 'Search phrase is required';
      return;
    }
    
    if (!this.location.trim()) {
      this.error = 'Location is required';
      return;
    }
    
    this.loading = true;
    
    const config = {
      search_phrase: this.searchPhrase,
      location: this.location,
      radius: this.radius,
      max_results: this.maxResults
    };
    
    this.apiService.createTask(this.selectedAgentType, config).subscribe({
      next: (response) => {
        this.loading = false;
        this.success = `Task created successfully! Task ID: ${response.task_id}`;
        
        // Navigate to results immediately to see progress
        setTimeout(() => {
          this.router.navigate(['/tasks/results']);
        }, 1500);
      },
      error: (error) => {
        this.loading = false;
        this.error = error.error?.detail || 'Failed to create task';
        console.error('Error creating task:', error);
      }
    });
  }
}
