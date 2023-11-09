import { ChatPageComponent } from './components/chat-page/chat-page.component';
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import RegisterComponent from './components/register/register.component';
import { LoginComponent } from './components/login/login.component';

const routes: Routes = [
  {
    path: 'chat',
    component: ChatPageComponent,
  },
  {
    path: 'register',
    component: RegisterComponent,
  },
  {
    path: 'login',
    component: LoginComponent,
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
