import { Routes } from '@angular/router';
import { DashboardComponent } from './components/dashboard/dashboard.component';
import { AgentListComponent } from './components/agent-list/agent-list.component';
import { TaskCreateComponent } from './components/task-create/task-create.component';
import { TaskResultsComponent } from './components/task-results/task-results.component';

export const routes: Routes = [
  { path: '', redirectTo: '/dashboard', pathMatch: 'full' },
  { path: 'dashboard', component: DashboardComponent },
  { path: 'agents', component: AgentListComponent },
  { path: 'tasks/create', component: TaskCreateComponent },
  { path: 'tasks/results', component: TaskResultsComponent },
];
