import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { User, Client } from '../interfaces/interface';

@Injectable({
  providedIn: 'root'
})
export class UserloginService {
  token: any;
  id: number;
  user: User;
  client: Client;
  error: any;
  apiUrl = 'http://easyproject.pythonanywhere.com/nucleo/api';

  constructor(private http: HttpClient) { }

  login(myuser: string, mypassword: string) {
    return new Promise(resolve => {
      this.http.post<any>(this.apiUrl + '/token',
        {
          user: myuser,
          password: mypassword
        })
        .subscribe(data => {
          this.token = data.token;
          this.client = data.client;
          this.user = data.user;
          this.error = null
          resolve(data);
        },
          err => {
            this.error = err['error']
            resolve(err);
        });
    });
  }

}
