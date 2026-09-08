import { Component } from '@angular/core';
import { RouterOutlet, RouterLink, RouterLinkActive, Router  } from '@angular/router';

@Component({
    selector: 'app-admin-layout',
    imports: [
        RouterOutlet, 
        RouterLink, 
        RouterLinkActive
    ],
    templateUrl: './admin-layout.html',
    styleUrl: './admin-layout.css'
})  

export class AdminLayout {

    constructor(private router: Router) {}
    mostrarModalLogout = false;

    abrirModalLogout(): void {
        this.mostrarModalLogout = true;
    }

    cancelarLogout(): void {
        this.mostrarModalLogout = false;
    }

    confirmarLogout(): void {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('rol');
        this.router.navigate(['/login']);
    }

    isSidebarOpen = false;
    toggleSidebar() {
        this.isSidebarOpen = !this.isSidebarOpen;
    }

}
