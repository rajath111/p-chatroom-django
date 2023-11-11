import { UserLoginModel } from './../models/user-login.model';
import { environment } from './../../environments/environment';
import { Observable } from 'rxjs';
import { UserRegisterationModel } from './../models/user-registeration.model';
import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  constructor(private readonly httpClient: HttpClient) {
    
  }

  public registerUser(userModel: UserRegisterationModel): Observable<UserRegisterationModel> {
    return this.httpClient.post<UserRegisterationModel>(environment.apiBaseUrl + 'auth/register/', userModel);
  }

  public login(loginModel: UserLoginModel): Observable<any> {
    return this.httpClient.post<any>(`${environment.apiBaseUrl}auth/login/`, loginModel);
  }
}
