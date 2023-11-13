import { UserDetails } from './../../models/user_details.model';
import { UserService } from './../../services/user.service';
import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit{

  public userDetails?: UserDetails;

  constructor(private readonly userService: UserService, private readonly router: Router) {

  }

  ngOnInit(): void {
    this.userService.getUserDetails().subscribe(
      data => {
        this.userDetails = data;
      },
    );
  }

  public addRoomClick(): void {
    this.router.navigate(['home', 'add']);
  }

}
