import { AuthInterceptor } from './interceptors/AuthInterceptor';
import { importProvidersFrom, NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { ChatPageComponent } from './components/chat-page/chat-page.component';
import RegisterComponent from './components/register/register.component';
import { LoginComponent } from './components/login/login.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';

@NgModule({
  declarations: [
    AppComponent,
    ChatPageComponent,
    RegisterComponent,
    LoginComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    NgbModule,
    FormsModule,
    ReactiveFormsModule,
  ],
  providers: [
    importProvidersFrom(HttpClientModule),
    { provide: HTTP_INTERCEPTORS, useClass: AuthInterceptor, multi: true },
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
