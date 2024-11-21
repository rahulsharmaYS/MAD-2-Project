import InfluencerDashboard from "@/components/influencer/InfluencerDashboard.vue";
import Profile from "@/components/influencer/InfluencerProfile.vue";
import Find from "@/components/influencer/InfluencerFind.vue";
import Stats from "@/components/influencer/InfluencerStats.vue";
import InfluencerCampaigns from "@/components/influencer/InfluencerCampaigns.vue";

export const influencer_routes = [
    {path: '/u/dashboard/:username', component: InfluencerDashboard,  name: 'dashboard', props: true, meta: { requiresAuth: true } },
    {path: '/u/:username/profile', component: Profile,  name: 'Profile', props: true, meta: { requiresAuth: true } },
    {path: '/u/:username/find', component: Find,  name: 'Find', props: true, meta: { requiresAuth: true } },
    {path: '/u/:username/stats', component: Stats,  name: 'Stats', props: true, meta: { requiresAuth: true } },
    {path: '/u/:username/findcampaigns', component: InfluencerCampaigns,  name: 'Campaigns', props: true, meta: { requiresAuth: true } },
];


export default influencer_routes;
