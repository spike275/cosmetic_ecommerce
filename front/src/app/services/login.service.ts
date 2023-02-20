import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { catchError, Observable, tap, throwError } from 'rxjs';

// @Injectable({
//   providedIn: 'root',
// })
// export class LoginService {
//   access = '';
//   current_user_id = 0;
//   myServer = 'http://127.0.0.1:8000/login/';
//   constructor(private srv: HttpClient) {}

//   do_login(cred: any): Observable<any> {
//     console.log('User Logged in');
//     return this.srv.post<any>(this.myServer, cred);
//   }
// }

//Liron changed the above code to:

@Injectable({
  providedIn: 'root',
})
export class LoginService {
  access = '';
  current_user_id = 0;
  myServer = 'http://127.0.0.1:8000/login/';
  constructor(private srv: HttpClient) {}

  do_login(cred: any): Observable<any> {
    console.log('Making login request with credentials:', cred);
    return this.srv.post<any>(this.myServer, cred).pipe(
      tap((response: any) => console.log('Login response:', response)),
      catchError(error => {
        console.error('Login error:', error);
        return throwError(error);
      })
    );
  }
}
//Liron changed end