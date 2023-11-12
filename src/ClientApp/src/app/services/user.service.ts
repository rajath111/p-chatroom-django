import { environment } from './../../environments/environment';
import { Observable } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { UserDetails } from '../models/user_details.model';

@Injectable({
  providedIn: 'root'
})
export class UserService {

  constructor(private readonly httpClient: HttpClient) { }

  public getUserDetails(): Observable<UserDetails> {
    return this.httpClient.get<UserDetails>(`${environment.apiBaseUrl}user/`);
  }
}
