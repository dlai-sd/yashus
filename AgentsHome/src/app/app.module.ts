import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';

import { AppComponent } from './app.component';
import { AppRoutingModule } from './app-routing.module';
import { HeaderComponent } from './components/header/header.component';
import { HeroComponent } from './components/hero/hero.component';
import { CarouselComponent } from './components/carousel/carousel.component';
import { AgentsComponent } from './components/agents/agents.component';
import { HowItWorksComponent } from './components/how-it-works/how-it-works.component';
import { ResultsComponent } from './components/results/results.component';
import { PricingComponent } from './components/pricing/pricing.component';
import { FAQComponent } from './components/faq/faq.component';
import { FooterComponent } from './components/footer/footer.component';
import { LoginModalComponent } from './components/login-modal/login-modal.component';
import { DemoModalComponent } from './components/demo-modal/demo-modal.component';
import { AuthInterceptor } from './core/interceptors/auth.interceptor';

@NgModule({
  declarations: [
    AppComponent,
    HeaderComponent,
    HeroComponent,
    CarouselComponent,
    AgentsComponent,
    HowItWorksComponent,
    ResultsComponent,
    PricingComponent,
    FAQComponent,
    FooterComponent,
    LoginModalComponent,
    DemoModalComponent
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
    HttpClientModule,
    AppRoutingModule
  ],
  providers: [
    {
      provide: HTTP_INTERCEPTORS,
      useClass: AuthInterceptor,
      multi: true
    }
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
