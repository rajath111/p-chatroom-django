import { environment } from './../../environments/environment';
import { HttpClient } from '@angular/common/http';
import { RoomDetails } from './../models/room/room-details.mode';
import { Observable } from 'rxjs';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class RoomService {

  constructor(private readonly httpClient: HttpClient) { }

  public createRoom(roomName: string): Observable<RoomDetails> {
    return this.httpClient.post<RoomDetails>(`${environment.apiBaseUrl}chat/room/`, {'room_name': roomName});
  }

  public getRoom(roomId: string): Observable<RoomDetails> {
    return this.httpClient.get<RoomDetails>(`${environment.apiBaseUrl}chat/room/${roomId}`);
  }

  public getAllRooms(): Observable<RoomDetails[]> {
    return this.httpClient.get<RoomDetails[]>(`${environment.apiBaseUrl}chat/room/`);
  }

  public updateRoomStatus(id: string, status: string): Observable<RoomDetails> {
    return this.httpClient.put<RoomDetails>(`${environment.apiBaseUrl}chat/room/`, {'room_status': status, 'room_id': id});
  }
}
