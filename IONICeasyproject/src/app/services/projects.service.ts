import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Projects, Project } from '../interfaces/interface';

@Injectable({
  providedIn: 'root'
})
export class ProjectsService {
  projects: any[];
  error: any;

  apiUrl = 'http://easyproject.pythonanywhere.com/nucleo/api';

  constructor(private http: HttpClient) { }

  async get_projects(userId: number, token: string) { 
    return new Promise(resolve => {
      this.http.get<any>(this.apiUrl + '/myprojects/' + userId,{
        headers: new HttpHeaders().set('Authorization', 'Token ' + token)
      })
      .subscribe(data => {
        resolve(data);
        this.projects = data.projects;
        this.error = null;
      },
        err => {
          this.error = err['error']['detail']
          resolve(err);
        }
      );
    });
  };
}
