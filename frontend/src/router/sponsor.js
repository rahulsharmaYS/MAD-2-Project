import SponsorDashboard from "@/components/sponsor/SponsorDashboard.vue";
import SponsorProfile from "@/components/sponsor/SponsorProfile.vue";
import SponsorFind from "@/components/sponsor/SponsorFind.vue";
import SponsorStats from "@/components/sponsor/SponsorStats.vue";
import SponsorCampaigns from "@/components/sponsor/SponsorCampaigns.vue";

export const sponsor_routes = [
    {path: '/s/:sponsorname/dashboard', component: SponsorDashboard,  name: 'sponsordashboard', props: true, meta: { requiresAuth: true } },
    {path: '/s/:sponsorname/profile', component: SponsorProfile,  name: 'sponsorprofile', props: true, meta: { requiresAuth: true } },
    {path: '/s/:sponsorname/find', component: SponsorFind,  name: 'sponsorfind', props: true, meta: { requiresAuth: true } },
    { path: '/s/:sponsorname/stats', component: SponsorStats, name: 'sponsorstats', props: true, meta: { requiresAuth: true } },
    {path: '/s/:sponsorname/campaigns', component: SponsorCampaigns,  name: 'sponsorcampaigns', props: true, meta: { requiresAuth: true } },
];

export default sponsor_routes;