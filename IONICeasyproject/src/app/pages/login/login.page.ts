import { Component, ComponentFactoryResolver, OnInit } from '@angular/core';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AlertController, LoadingController } from '@ionic/angular';
import { UserloginService } from 'src/app/services/userlogin.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.page.html',
  styleUrls: ['./login.page.scss'],
})
export class LoginPage implements OnInit {

  user: any;
  token: any;
  client: any;
  formularioLogin: FormGroup;

  constructor(public ulService: UserloginService,
    public route: Router,
    public alertController: AlertController,
    public loadingCtrl: LoadingController,
    public fb: FormBuilder) {
    this.formularioLogin = this.fb.group({
      user: new FormControl('', Validators.required),
      password: new FormControl('', Validators.required)
    });
  }

  ngOnInit() {
  }

  async login() {
    if (this.formularioLogin.invalid) {
      this.showAlert('Datos incompletos', 'Tienes que llenar todos los campos');
      return;
    }

    this.ulService.login(this.formularioLogin.value.user, this.formularioLogin.value.password)
      .then((data) => {
        if (this.ulService.error) {
          this.showAlert('Error', this.ulService.error);
        } else {
          this.user = this.ulService.user;
          this.token = this.ulService.token;
          this.client = this.ulService.client;

          if (this.user && this.client && this.token) {
            this.route.navigate(['/projects'])
          } else {
            this.showAlert('Error', 'Se ha producido un error.');
          }
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
