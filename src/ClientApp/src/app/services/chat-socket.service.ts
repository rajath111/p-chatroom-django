import { MessageType } from './../models/message';
import { Constants } from './../constants/constants';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { webSocket, WebSocketSubject } from 'rxjs/webSocket';

@Injectable()
export class ChatSocketService {

  private connection$?: WebSocketSubject<any>;
  private socketUrl = 'ws://localhost:8000/ws/chat/'

  constructor() { }

  public connect(roomName: string): WebSocketSubject<any> {
    if(!this.connection$) {
      const access_token = sessionStorage.getItem(Constants.accessToken);
      const url = `${this.socketUrl}${roomName}/?access_token=${access_token}`
      this.connection$ = webSocket(url,);
    }
    return this.connection$;
  }

  public send(message: string) {
    this.connection$?.next({
      'messageType': MessageType.USER_MESSAGE,
      'data': {
        'message': message,
      }
    });
  }
}
