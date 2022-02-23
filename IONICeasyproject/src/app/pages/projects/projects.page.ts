import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { AlertController, LoadingController } from '@ionic/angular';
import { ProjectsService } from 'src/app/services/projects.service';
import { UserloginService } from 'src/app/services/userlogin.service';

@Component({
  selector: 'app-projects',
  templateUrl: './projects.page.html',
  styleUrls: ['./projects.page.scss'],
})
export class ProjectsPage implements OnInit {

  projects: any[];

  constructor(public ulService: UserloginService,
    public prService: ProjectsService,
    public route: Router,
    public alertController: AlertController,
    public loadingCtrl: LoadingController,) { }

  ngOnInit() {
    this.prService.get_projects(this.ulService.user.id, this.ulService.token)
      .then(data => {
        if (this.prService.error) {
          this.route.navigate(['/login'])
          this.showAlert('Error', this.prService.error);
        } else {
          this.projects = this.prService.projects;
        }
      });
  }

  async showAlert(myHeader, myMessage) {

    const alert = await this.alertController.create({
      header: myHeader,
      message: myMessage,
      buttons: ['Aceptar'],
    });

    await alert.present();
  }

}
