import { Constants } from './../../constants/constants';
import { environment } from './../../../environments/environment';
import { UserLoginModel } from './../../models/user-login.model';
import { Component } from '@angular/core';
import { AbstractControl, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { AuthService } from 'src/app/services/auth.service';
import { passwordValidator } from 'src/app/validators/password.validator';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent {
  form: FormGroup;
  message: string = '';
  errorMessage: string = '';

  constructor(
    private readonly fromBuilder: FormBuilder, 
    private readonly authService: AuthService, 
    private readonly router: Router,
    private readonly activatedRoute: ActivatedRoute,
    ) {
    this.form = fromBuilder.group({
      'username': fromBuilder.control('', { validators: [
        Validators.required, 
        // Validators.email
      ] }),
      'password': fromBuilder.control('', { validators: [Validators.required, Validators.minLength(6)] }),
    }, );

    if(activatedRoute.snapshot.queryParams[Constants.registeredUserQueryParam]) {
      this.message = `User ${activatedRoute.snapshot.queryParams[Constants.registeredUserQueryParam]} registered successfully. Please login.`;
    }
  }


  public login(): void {
    // Check if form is valid
    if(this.form.invalid) {
      return ;
    }

    // Create post payload
    const loginData: UserLoginModel = {
      username: this.form.value['username'],
      password: this.form.value['password'],
    };

    this.message = '';

    // Make API call
    this.authService.login(loginData).subscribe(
      // On Success store bearer key and redirect to home
      data => {
        sessionStorage.setItem(Constants.accessToken, data['token']);
        this.router.navigate(['home']);
      },
      // Show error message
      error => {
        this.errorMessage = 'Login failed. Please try again';
      },
    );

  }

  
  public get username(): AbstractControl {
    return this.form.controls['username'];
  }

  public get password(): AbstractControl {
    return this.form.controls['password'];
  }

}
