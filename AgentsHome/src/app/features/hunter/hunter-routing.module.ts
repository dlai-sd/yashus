import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { HunterContainerComponent } from './containers/hunter-container.component';

const routes: Routes = [
  {
    path: '',
    component: HunterContainerComponent
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class HunterRoutingModule { }
