import { Component, DestroyRef, OnInit, signal } from '@angular/core';
import * as AOS from 'aos';

@Component({
    selector: 'app-quienes-somos',
    templateUrl: './quienes-somos.html',
    styleUrls: ['./quienes-somos.css']
})

export class QuienesSomos implements OnInit {

    constructor(private destroyRef: DestroyRef) {}

    missionTypes: string[] = ['A+', 'B+', 'AB+', 'O+'];
    visionTypes: string[] = ['O-', 'A-', 'B-', 'AB-'];

    currentMissionType = signal('A+');
    currentVisionType = signal('O-');

    private missionIndex = 0;
    private visionIndex = 0;

    ngOnInit(): void {

        AOS.init({
            duration: 1000,
            once: true
        });

        const missionTimer = setInterval(() => {
            this.missionIndex = (this.missionIndex + 1) % this.missionTypes.length;
            this.currentMissionType.set(this.missionTypes[this.missionIndex]);
        }, 2500);

        const visionTimer = setInterval(() => {
            this.visionIndex = (this.visionIndex + 1) % this.visionTypes.length;
            this.currentVisionType.set(this.visionTypes[this.visionIndex]);
        }, 3000);

        this.destroyRef.onDestroy(() => {
            clearInterval(missionTimer);
            clearInterval(visionTimer);
        });
    }

}
