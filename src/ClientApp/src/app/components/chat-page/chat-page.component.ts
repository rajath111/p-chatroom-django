import { MessageService } from './../../services/message.service';
import { BroadcastData } from './../../models/message';
import { ActivatedRoute } from '@angular/router';
import { Message, MessageType, UsernameData } from '../../models/message';
import { WebSocketSubject } from 'rxjs/webSocket';
import { ChatSocketService } from '../../services/chat-socket.service';
import { Component, OnDestroy, OnInit } from '@angular/core';
import { lastValueFrom, Subject, takeUntil } from 'rxjs';

@Component({
  selector: 'app-chat-page',
  templateUrl: './chat-page.component.html',
  styleUrls: ['./chat-page.component.scss'],
  providers: [ChatSocketService],
})
export class ChatPageComponent implements OnInit, OnDestroy {
  room_id = '';
  username: string = '';
  message: string = '';
  messages: BroadcastData[] = [];

  private destroy$ = new Subject();
  private socketConnection?: WebSocketSubject<any>;

  constructor(
    private readonly chatSocketService: ChatSocketService, 
    private readonly activatedRoute: ActivatedRoute,
    private readonly messageService: MessageService) {

  }

  async ngOnInit(): Promise<void> {
    
    this.room_id = this.activatedRoute.snapshot.queryParams['room_id'];

    // Load Initial messages
    // this.messages = await lastValueFrom(this.messageService.getMessagesByRoom(this.room_id));

    this.messageService.getMessagesByRoom(this.room_id).subscribe(
      data => {
        this.messages = data;
      }
    )

    // Make web socket connect to room
    this.socketConnection = this.chatSocketService.connect(this.room_id);

    this.socketConnection.pipe(
      takeUntil(this.destroy$)
    ).subscribe(
      (data: Message) => {
        if(data.messageType === MessageType.USERNAME) {
          const usernameData = data.data as UsernameData;
          this.username = usernameData.username;
        }
        else {
          this.addMessage(data.data as BroadcastData);
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


  private addMessage(message: BroadcastData) {
    this.messages.push(message);
  }


  private clearMessage() {
    this.message = '';
  }
}
