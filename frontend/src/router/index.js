import { createRouter, createWebHistory } from 'vue-router';
import LoginComponent from '../components/LoginComponent.vue';
import RegisterComponent from '../components/RegisterComponent.vue';
import SponsorLoginComponent from '../components/SponsorLoginComponent.vue';
import BannedUserComponent from '../components/BannedUserComponent.vue';
import BannedSponsorComponent from '../components/BannedSponsorComponent.vue';
import ConfirmationComponent from '../components/ConfirmationComponent.vue';
import SponsorConfirmComponent from '@/components/SponsorConfirmComponent.vue';
import SponsorRegisterComponent from '../components/SponsorRegisterComponent.vue';
import WelcomeComponent from '../components/WelcomeComponent.vue';
import influencer_routes from './influencer';
import sponsor_routes from './sponsor';
import admin_routes from './admin';

const routes = [
    { path: '/', component: LoginComponent },
    { path: '/login', component: LoginComponent },
    { path: '/register', component: RegisterComponent },
    { path: '/sponsorlogin', component: SponsorLoginComponent },
    { path: '/confirmation/:sponsorname', name: 'Confirmation', component: ConfirmationComponent },
    { path: '/banned/:username', component: BannedUserComponent, name: 'BannedUser'},
    { path: '/banned/:sponsorname', component: BannedSponsorComponent, name: 'BannedSponsor'},
    { path: '/logout', component: WelcomeComponent },
    {path: '/sponsorregister',name: 'SponsorRegister',component: SponsorRegisterComponent},
    {path: '/sponsorconfirm',name: 'SponsorConfirm',component: SponsorConfirmComponent,},
    ...influencer_routes,
    ...sponsor_routes,
    ...admin_routes,
];

const router = createRouter({
    history: createWebHistory('/'),
    routes,
});

export default router;