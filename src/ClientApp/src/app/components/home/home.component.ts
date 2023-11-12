import { UserDetails } from './../../models/user_details.model';
import { UserService } from './../../services/user.service';
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit{

  public userDetails?: UserDetails;
  public addRoomEnabled: boolean = false;

  constructor(private readonly userService: UserService) {

  }

  ngOnInit(): void {
    this.userService.getUserDetails().subscribe(
      data => {
        this.userDetails = data;
      },
    );
  }

  public addRoomClick(): void {
    this.addRoomEnabled = true;
  }

  public afterRoomAdded(value: boolean): void {
    this.addRoomEnabled = false;
  }

}
