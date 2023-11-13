import { RoomMembership } from './../models/membership.model';
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
    return this.httpClient.get<RoomDetails>(`${environment.apiBaseUrl}chat/room/${roomId}/`);
  }

  public deleteRoom(roomId: string): Observable<void> {
    return this.httpClient.delete<void>(`${environment.apiBaseUrl}chat/room/${roomId}/`);
  } 

  public getAllRooms(): Observable<RoomDetails[]> {
    return this.httpClient.get<RoomDetails[]>(`${environment.apiBaseUrl}chat/room/`);
  }

  public updateRoom(id: string, roomDetails: RoomDetails): Observable<RoomDetails> {
    return this.httpClient.put<RoomDetails>(`${environment.apiBaseUrl}chat/room/${id}/`, roomDetails);
  }

  public getMembers(roomId: string): Observable<RoomMembership[]> {
    return this.httpClient.get<RoomMembership[]>(`${environment.apiBaseUrl}chat/members/${roomId}/`);
  }

  public createMember(membership: RoomMembership): Observable<RoomMembership> {
    return this.httpClient.post<RoomMembership>(`${environment.apiBaseUrl}chat/members/`, membership);
  }

  public getUserAssociatedRooms(userId: string): Observable<RoomMembership[]> {
    return this.httpClient.get<RoomMembership[]>(`${environment.apiBaseUrl}chat/members/`);
  }

}
