import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';

import { HunterRoutingModule } from './hunter-routing.module';
import { HunterContainerComponent } from './containers/hunter-container.component';
import { CalculatorComponent } from './components/calculator/calculator.component';
import { CalculatorService } from './services/calculator.service';

@NgModule({
  declarations: [
    HunterContainerComponent,
    CalculatorComponent
  ],
  imports: [
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
    HttpClientModule,
    HunterRoutingModule
  ],
  providers: [
    CalculatorService
  ]
})
export class HunterModule { }
