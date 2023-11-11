import { Constants } from './../../constants/constants';
import { UserRegisterationModel } from './../../models/user-registeration.model';
import { AuthService } from './../../services/auth.service';
import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators, AbstractControl } from '@angular/forms';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { passwordValidator } from 'src/app/validators/password.validator';
import { Router } from '@angular/router';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss']
})
export default class RegisterComponent {
  form: FormGroup;
  errorMessage: string = '';

  constructor(private readonly fromBuilder: FormBuilder, private readonly authService: AuthService, private readonly router: Router) {
    this.form = fromBuilder.group({
      'username': fromBuilder.control('', { validators: [Validators.required, Validators.email] }),
      'password': fromBuilder.control('', { validators: [Validators.required, Validators.minLength(6)] }),
      'confirm_password': fromBuilder.control('', { validators: [Validators.required] }),
      'first_name': fromBuilder.control('', { validators: [Validators.required] }),
      'last_name': fromBuilder.control('', { validators: [Validators.required] }),
      'age': fromBuilder.control('', { validators: [Validators.required, Validators.min(18), Validators.max(120)], }),
    }, { validators: [passwordValidator]});
  }

  public register(): void {
    if(this.form.valid) {
      this.authService.registerUser(this.getUserRegisterationModel()).subscribe(
        (data: UserRegisterationModel) => {
          this.router.navigate(['login'], {queryParams: {
            registeredUser: data.username,
          }});
        },
        error => {
          this.errorMessage = 'User registration failed. Please try again';
        },
      )
    }
  }

  private getUserRegisterationModel(): UserRegisterationModel {
    return {
      username: this.form.value['username'],
      password: this.form.value['password'],
      age: this.form.value['age'],
      first_name: this.form.value['first_name'],
      last_name: this.form.value['last_name'],
    };
  }


  public get username(): AbstractControl {

    return this.form.controls['username'];
  }

  public get first_name(): AbstractControl {
    return this.form.controls['first_name'];
  }

  public get last_name(): AbstractControl {
    return this.form.controls['last_name'];
  }

  public get age(): AbstractControl {
    return this.form.controls['age'];
  }

  public get password(): AbstractControl {
    return this.form.controls['password'];
  }

  public get confirm_password(): AbstractControl {
    return this.form.controls['confirm_password'];
  }
  
}
