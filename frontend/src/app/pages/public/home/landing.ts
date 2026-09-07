import { Component, OnInit,ChangeDetectorRef } from '@angular/core';
import { RouterModule } from '@angular/router';
import { CampaniaService, Campania } from '../../../services/campanias/campania.service';



@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterModule],
  templateUrl: './landing.html',
  styleUrl: './landing.css',
})
export class Landing implements OnInit {
  campanias: Campania[] = [];
  cargando: boolean = true;
  error: string = '';

  constructor(
    private campaniaService: CampaniaService,
    private cdr: ChangeDetectorRef
  ) {}
  
  ngOnInit(): void {
    this.campaniaService.getCampanias().subscribe({
      next: (datos: Campania[]) => {
        const hoy = new Date();
        this.campanias = datos.filter(c => {
          const [yf, mf, df] = c.fecha_fin.split('-').map(Number);
          const fin = new Date(yf, mf - 1, df);
          return hoy <= fin;
        });

        this.cargando = false;
        this.cdr.detectChanges();
      },
      error: (err) => {
        this.error = 'No se pudieron cargar las campañas.';
        this.cargando = false;
        this.cdr.detectChanges();
      }
    });
  }
  formatearFecha(fecha: string): string {
      return new Date(fecha).toLocaleDateString('es-AR', {
        day: 'numeric', month: 'long'
      });
    }
}
