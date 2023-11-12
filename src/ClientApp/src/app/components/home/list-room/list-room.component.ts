import { Router } from '@angular/router';
import { RoomDetails } from './../../../models/room/room-details.mode';
import { RoomService } from './../../../services/room.service';
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-list-room',
  templateUrl: './list-room.component.html',
  styleUrls: ['./list-room.component.scss']
})
export class ListRoomComponent implements OnInit {
  public allRooms?: RoomDetails[];

  constructor(private readonly roomService: RoomService, private readonly router: Router) {
    
  }

  ngOnInit(): void {
    this.refreshRooms();
  }

  public updateStatus(roomId: string, status: string) {
    this.roomService.updateRoomStatus(roomId, status).subscribe((data) => {
      this.refreshRooms();
    });
  }

  public openChatPage(room_id: string): void {
    this.router.navigate(['chat'], {queryParams: {'room_id': room_id} });
  }

  private refreshRooms(): void {
    this.roomService.getAllRooms().subscribe(
      (rooms: RoomDetails[]) => {
        this.allRooms = rooms;
      }
    );
  }
  
}
