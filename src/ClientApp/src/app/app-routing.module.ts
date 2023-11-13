import { AddRoomComponent } from './components/home/add-room/add-room.component';
import { HomeComponent } from './components/home/home.component';
import { ChatPageComponent } from './components/chat-page/chat-page.component';
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import RegisterComponent from './components/register/register.component';
import { LoginComponent } from './components/login/login.component';
import { EditRoomComponent } from './components/home/edit-room/edit-room.component';

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
  {
    path: 'home',
    component: HomeComponent,
    children: [
      {
        path: 'add', component: AddRoomComponent,
      },
      {
        path: 'edit/:roomId', component: EditRoomComponent,
      }
    ],
  },
  {
    path: '**',
    component: LoginComponent,
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
