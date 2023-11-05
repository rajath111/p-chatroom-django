import { Message } from './../models/message';
import { WebSocketSubject } from 'rxjs/webSocket';
import { ChatSocketService } from './../services/chat-socket.service';
import { Component, OnDestroy, OnInit } from '@angular/core';
import { Subject, takeUntil } from 'rxjs';

@Component({
  selector: 'app-chat-page',
  templateUrl: './chat-page.component.html',
  styleUrls: ['./chat-page.component.scss'],
  providers: [ChatSocketService],
})
export class ChatPageComponent implements OnInit, OnDestroy {
  room_name = 'room1';
  username: string = '';
  message: string = '';
  messages: Message[] = [];

  private destroy$ = new Subject();
  private socketConnection?: WebSocketSubject<any>;

  constructor(private readonly chatSocketService: ChatSocketService) {

  }

  ngOnInit(): void {
    // Make web socket connect to room
    this.socketConnection = this.chatSocketService.connect(this.room_name);

    this.socketConnection.pipe(
      takeUntil(this.destroy$)
    ).subscribe(
      (data: Message) => {
        if(data.messageType === 'username') {
          this.username = data.username;
        }
        else {
          this.addMessage(data);
        }
      },
    );
  }

  ngOnDestroy(): void {
    this.destroy$.next(true);
  }


  public sendMessage(): void {
    if(this.message === null || this.message === undefined) {
      return ;
    }

    // TODO: Send message Via Socket
    // this.addMessage(this.message);
    this.chatSocketService.send(this.message);
    // Clear the message 
    this.clearMessage();
  }


  public onMessageKeyPress(event: KeyboardEvent): void {
    if(this.message === null || this.message === undefined) {
      return ;
    }
    // Check if the key pressed is enter
    if(event.key === 'Enter') {
      // this.addMessage(this.message);
      this.chatSocketService.send(this.message);
      this.clearMessage();
    }
  }


  private addMessage(message: Message) {
    this.messages.push(message);
  }


  private clearMessage() {
    this.message = '';
  }
}
