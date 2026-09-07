import { Component, inject } from '@angular/core';
import { Dashboard, DashboardService } from '../../../services/dashboard/dashboard.service';
import { map, shareReplay } from 'rxjs/operators';
import { Router } from '@angular/router';
import { AsyncPipe } from '@angular/common';

interface CampaniaGrafico {
  estado: string;
  count: number;
  porcentaje: number;
  color: string;
}

interface DonantesGrafico {
  clave: string;
  mes: string;
  donantes: number;
  altura: number;
}

interface DashboardViewModel extends Dashboard {
  campanias_por_tipo: CampaniaGrafico[];
  conicGradient: string;
  meses: DonantesGrafico[];
}

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [AsyncPipe],
  templateUrl: './dashboard.html',
  styleUrls: ['./dashboard.css']
})
export class AdminDashboard {

  private dashboardService = inject(DashboardService);
  private router = inject(Router);

  dashboardData$ = this.dashboardService.obtenerDashboard().pipe(
    map(data => {
      const campanias_por_tipo = this.agruparCampanias(data.campanias_por_estado);
      return {
        ...data,
        campanias_por_tipo,
        conicGradient: this.generarConicGradient(campanias_por_tipo),
        meses: this.transformarDonantesPorMes(data.donantes_por_mes)
      } as DashboardViewModel;
    }),
    shareReplay(1)
  );

  modalAbierto: string | null = null;

  private agruparCampanias(campanias: { estado: string; cantidad: number }[]): CampaniaGrafico[] {
    const cantidadesPorEstado = new Map<string, number>();
    for (const item of campanias) {
      cantidadesPorEstado.set(
        item.estado,
        (cantidadesPorEstado.get(item.estado) || 0) + item.cantidad
      );
    }

    const agrupadas = Array.from(
      cantidadesPorEstado,
      ([estado, cantidad]) => ({ estado, cantidad })
    );
    const total = agrupadas.reduce((suma, item) => suma + item.cantidad, 0);

    return agrupadas.map((item, index) => ({
      estado: item.estado,
      count: item.cantidad,
      porcentaje: total ? Math.round((item.cantidad / total) * 100) : 0,
      color: this.generarColor(index)
    }));
  }

  private transformarDonantesPorMes(serie: { anio: number; mes: number; cantidad: number }[]): DonantesGrafico[] {
    const hoy = new Date();
    const mesActual = new Date(hoy.getFullYear(), hoy.getMonth(), 1);
    const mapa = new Map(serie.map(item => [`${item.anio}-${item.mes}`, item.cantidad]));
    const meses = Array.from({ length: 12 }, (_, index) => {
      const fecha = new Date(mesActual.getFullYear(), mesActual.getMonth() - 11 + index, 1);
      const anio = fecha.getFullYear();
      const mesNumero = fecha.getMonth() + 1;
      const clave = `${anio}-${mesNumero}`;
      const nombre = new Intl.DateTimeFormat('es-AR', {
        month: 'short',
        year: 'numeric'
      }).format(fecha);

      return {
        clave,
        mes: nombre.charAt(0).toUpperCase() + nombre.slice(1),
        donantes: mapa.get(clave) || 0,
        altura: 0
      };
    });
    const maximo = Math.max(...meses.map(item => item.donantes), 0);

    return meses.map(item => ({
      ...item,
      altura: maximo ? (item.donantes / maximo) * 100 : 0
    }));
  }

  private generarColor(index: number): string {
    const colores = [
      '#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8',
      '#F7DC6F', '#BB8FCE', '#85C1E2', '#F8B88B', '#52B788'
    ];
    return colores[index % colores.length];
  }

  private generarConicGradient(campanias_por_tipo: any[]): string {

    let gradiente = 'conic-gradient(';
    let posicion = 0;

    if (!campanias_por_tipo.length) {
      return 'conic-gradient(#e9ecef 0% 100%)';
    }

    campanias_por_tipo.forEach((item, index) => {
      const inicio = posicion;
      const fin = posicion + item.porcentaje;
      gradiente += `${item.color} ${inicio}% ${fin}%`;
      if (index < campanias_por_tipo.length - 1) {
        gradiente += ', ';
      }
      posicion = fin;
    });

    gradiente += ')';
    return gradiente;

  }

  abrirModal(tipo: string): void {
    this.modalAbierto = tipo;
  }

  cerrarModal(): void {
    this.modalAbierto = null;
  }

  crearCampania(): void {
    this.router.navigate(['/admin/campanias/nueva']);
  }

  verTodasCampanias(): void {
    this.router.navigate(['/admin/campanias']);
  }

}
