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
      const url = `${this.socketUrl}${roomName}/`
      this.connection$ = webSocket(url);
    }
    return this.connection$;
  }

  public send(message: string) {
    this.connection$?.next({
      'message': message,
    });
  }
}
