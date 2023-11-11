import { Constants } from './../constants/constants';
import { Router } from '@angular/router';
import { environment } from './../../environments/environment';
import { Injectable } from '@angular/core';
import {
  HttpEvent, HttpInterceptor, HttpHandler, HttpRequest, HttpErrorResponse
} from '@angular/common/http';

import { catchError, Observable, throwError, tap } from 'rxjs';

/** Pass untouched request through to the next request handler. */
@Injectable()
export class AuthInterceptor implements HttpInterceptor {

  constructor(private readonly router: Router) {

  }

  intercept(req: HttpRequest<any>, next: HttpHandler):
    Observable<HttpEvent<any>> {
    // Allow auth related API calls with out Access token
    console.log('Intercepted', req);
    console.log('Url', req.url);
    const match = req.url.match('^.+/auth/.+$');
    console.log(match, match?.length);
    
    if(match && match.length > 0) {
      // Redirect to login if no access token
      return next.handle(req);
    }

    const token: string | null = sessionStorage.getItem(Constants.accessToken);
    if(token == null) {
      this.redirectLogin();
    }

    return next.handle(req).pipe(
      tap((data) => {
        console.log('Tapped response:', data);
      }),
      catchError((error: HttpErrorResponse, data) => {
        if(error.status === 401) {
          this.redirectLogin();
        }
        console.log('Cought error', error, data);
        return throwError(() => {
          console.log('Error occoured')
        })
      }),
      
    );
  }

  redirectLogin(): void {
    this.router.navigate(['login']);
  }
}