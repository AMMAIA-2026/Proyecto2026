import { Routes } from '@angular/router';
import { PublicLayout } from './layouts/public-layout/public-layout';
import { AdminLayout } from './layouts/admin-layout/admin-layout';
import { Landing } from './pages/public/home/landing';
import { QuienesSomos } from './pages/public/quienes-somos/quienes-somos';
import { AdminDashboard } from './pages/admin/dashboard/dashboard';
import { AdminCampanias } from './pages/admin/campanias/campanias';
import { AdminInscripciones } from './pages/admin/inscripciones/inscripciones';
import { Login } from './pages/public/login/login';
import { Campanias } from './pages/public/campanias/campanias';
import { Usuarios } from './pages/admin/usuarios/usuarios';
import { CampaniaDetalle } from './pages/public/campania-detalle/campania-detalle';
import { Registro } from './pages/public/registro/registro';
import { Informate } from './pages/public/informate/informate';
import { authGuard } from './guards/auth-guard';
import { CampaniaForm } from './pages/admin/campanias/campania-form/campania-form';
import { RecuperarPassword } from './pages/public/recuperar-password/recuperar-password';
import { ContactosAdmin } from './pages/admin/contactos/contactos';
import { Contactanos } from './pages/public/contactanos/contactanos';



export const routes: Routes = [

    // Rutas públicas
    {
        path: '',
        component: PublicLayout,
        children: [
            { path: '', component: Landing },
            { path: 'quienes-somos', component: QuienesSomos },
            { path: 'login', component: Login },
            { path: 'recuperar-password', component: RecuperarPassword },
            { path: 'campanias', component: Campanias },
            { path: 'campanias/:id', component: CampaniaDetalle },
            { path: 'registro', component: Registro },
            { path: 'informate', component: Informate },
            { path: 'contactanos', component: Contactanos },

        ]
    },

    // Rutas del administrador
        {
        path: 'admin',
        component: AdminLayout,
        canActivate: [authGuard],   
        children: [
            { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
            { path: 'dashboard', component: AdminDashboard },
            { path: 'campanias', component: AdminCampanias },
            { path: 'inscripciones', component: AdminInscripciones },
            { path: 'usuarios', component: Usuarios},
            { path: 'campanias/nueva', component: CampaniaForm },
            { path: 'campanias/editar/:id', component: CampaniaForm },
            { path: 'contactos', component: ContactosAdmin },
        ]
    },

    { path: '**', redirectTo: '' }

];
