import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

export interface Agent {
  agent_type: string;
  name: string;
  description: string;
  version: string;
  capabilities: string[];
}

export interface Task {
  task_id: string;
  agent_type: string;
  status: string;
  created_at: string;
  updated_at?: string;
  error?: string;
}

export interface TaskResult {
  task_id: string;
  agent_type: string;
  status: string;
  result?: any;
  created_at: string;
  completed_at?: string;
}

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) { }

  // Agent endpoints
  getAgents(): Observable<{ agents: Agent[], total: number }> {
    return this.http.get<{ agents: Agent[], total: number }>(`${this.apiUrl}/agents/`);
  }

  getAgentTypes(): Observable<any> {
    return this.http.get(`${this.apiUrl}/agents/types`);
  }

  // Task endpoints
  createTask(agentType: string, config: any): Observable<Task> {
    return this.http.post<Task>(`${this.apiUrl}/tasks/`, {
      agent_type: agentType,
      config: config
    });
  }

  getTaskStatus(taskId: string): Observable<Task> {
    return this.http.get<Task>(`${this.apiUrl}/tasks/${taskId}`);
  }

  getTaskResult(taskId: string): Observable<TaskResult> {
    return this.http.get<TaskResult>(`${this.apiUrl}/tasks/${taskId}/result`);
  }

  listTasks(): Observable<{ tasks: Task[], total: number }> {
    return this.http.get<{ tasks: Task[], total: number }>(`${this.apiUrl}/tasks/`);
  }
}
