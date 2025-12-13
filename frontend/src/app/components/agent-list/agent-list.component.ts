import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService, Agent } from '../../services/api.service';

@Component({
  selector: 'app-agent-list',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './agent-list.component.html',
  styleUrl: './agent-list.component.scss'
})
export class AgentListComponent implements OnInit {
  agents: Agent[] = [];
  loading = true;

  constructor(private apiService: ApiService) {}

  ngOnInit() {
    this.loadAgents();
  }

  loadAgents() {
    this.apiService.getAgents().subscribe({
      next: (data) => {
        this.agents = data.agents;
        this.loading = false;
      },
      error: (error) => {
        console.error('Error loading agents:', error);
        this.loading = false;
      }
    });
  }
}
