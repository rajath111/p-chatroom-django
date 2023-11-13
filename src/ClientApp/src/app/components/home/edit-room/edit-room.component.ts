import { RoomMembership } from './../../../models/membership.model';
import { Router, ActivatedRoute } from '@angular/router';
import { RoomService } from './../../../services/room.service';
import { RoomDetails } from './../../../models/room/room-details.mode';
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-edit-room',
  templateUrl: './edit-room.component.html',
  styleUrls: ['./edit-room.component.scss']
})
export class EditRoomComponent implements OnInit {
  public roomDetails?: RoomDetails;
  public members?: RoomMembership[];
  public addMemberOpened: boolean = false;
  public memberId: string = '';

  constructor(private readonly roomService: RoomService, private readonly route: Router, private readonly activatedRoute: ActivatedRoute) {

  }

  ngOnInit(): void {
    
    this.activatedRoute.params.subscribe(
      params => {
        const id = params['roomId']
        this.roomService.getRoom(id).subscribe(
          data => {
            this.roomDetails = data;

            this.roomService.getMembers(data.id).subscribe(
              (data: RoomMembership[]) => {
                this.members = data;
              }
            );
          }
        );
      }
    );
  }

  public deleteRoom(): void {
    if(this.roomDetails){
      this.roomService.deleteRoom(this.roomDetails.id).subscribe(
        () => {
          this.route.navigate(['home']);
        }
      );
    }
    
  }


  public updateStatus(status: string) {

    if(this.roomDetails){
      this.roomDetails.room_status = status;
      this.roomService.updateRoom(this.roomDetails.id, this.roomDetails).subscribe((data) => {
        this.roomDetails = data;
      });
    } 
  }

  public openAddMember(): void {
    this.addMemberOpened = true;
  }

  public addMember() {
    if(this.memberId && this.roomDetails) {
      this.roomService.createMember({
        room_id: this.roomDetails.id,
        user_id: this.memberId,
      }).subscribe(
        (data) => {
          this.addMemberOpened = false;
        }
      );
    }
  }

}
