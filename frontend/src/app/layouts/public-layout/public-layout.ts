import { Component } from '@angular/core';
import { Router, RouterModule, NavigationEnd } from '@angular/router';
import { Location } from '@angular/common';
import { filter } from 'rxjs/operators';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';

@Component({
  selector: 'app-public-layout',
  imports: [RouterModule],
  templateUrl: './public-layout.html',
  styleUrls: ['./public-layout.css']
})
export class PublicLayout {

  isHome = true;

  constructor(private router: Router, private location: Location) {
    this.isHome = this.router.url === '/';
    this.router.events.pipe(
      filter(e => e instanceof NavigationEnd)
    ).pipe(
      takeUntilDestroyed()
    ).subscribe((e: NavigationEnd) => {
      this.isHome = e.urlAfterRedirects === '/';
    });
  }

  isLoggedIn(): boolean {
    return !!localStorage.getItem('access_token');
  }

  logout() {
    localStorage.clear();
    this.router.navigate(['/']);
  }

  goBack() {
    this.location.back();
  }

}
