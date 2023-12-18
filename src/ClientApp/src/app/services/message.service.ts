import { Observable } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BroadcastData } from '../models/message';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class MessageService {

  constructor(private readonly http: HttpClient) { }


  public getMessagesByRoom(roomId: string): Observable<BroadcastData[]> {
    return this.http.get<BroadcastData[]>(`${environment.apiBaseUrl}chat/messages/${roomId}/50/`);
  }
}
