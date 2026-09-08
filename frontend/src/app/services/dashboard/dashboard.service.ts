import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Dashboard } from '../../models/dashboard.model';

@Injectable({
    providedIn: 'root'
})

export class DashboardService {

    private http = inject(HttpClient);

    private apiUrl = 'http://127.0.0.1:8000/dashboard/';

    obtenerDashboard(): Observable<Dashboard> {
        return this.http.get<Dashboard>(this.apiUrl);
    }

}
