import { RoomDetails } from './../../../models/room/room-details.mode';
import { RoomService } from './../../../services/room.service';
import { FormGroup, FormBuilder, Validators, AbstractControl } from '@angular/forms';
import { Component, EventEmitter, Output } from '@angular/core';

@Component({
  selector: 'app-add-room',
  templateUrl: './add-room.component.html',
  styleUrls: ['./add-room.component.scss']
})
export class AddRoomComponent {
  public form: FormGroup;
  public message: string = '';
  public errorMessage: string = '';

  @Output('roomAdded')
  public roomAdded: EventEmitter<boolean>;

  constructor(private readonly fromBuilder: FormBuilder, private readonly roomService: RoomService) {
    this.roomAdded = new EventEmitter<boolean>();

    this.form = fromBuilder.group({
      'room_name': fromBuilder.control('', {validators: [Validators.required, Validators.minLength(6)]}),

    });
  }

  public createRoom(): void {
    if(this.form?.invalid) {
      return ;
    }

    this.roomService.createRoom(this.form?.value['room_name']).subscribe(
      (data: RoomDetails) => {
        this.message = `Room(${this.form?.value['room_name']}) added successfully!!`;
        this.form.reset();
        this.roomAdded.next(true);
      },
      error => {
        this.errorMessage = 'Failed to create the room. Please try again.';
      }
    );
  }


  public get roomName(): AbstractControl {
    return this.form.controls['room_name'];
  }
  
}
 