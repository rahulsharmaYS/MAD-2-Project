import AdminDashboard from "@/components/admin/AdminDashboard.vue";
// import AdminProfile from "@/components/admin/AdminProfile.vue";
import AdminFind from "@/components/admin/AdminFind.vue";
import AdminStats from "@/components/admin/AdminStats.vue";
import AdminApplications from "@/components/admin/AdminApplications.vue";

export const admin_routes = [
    {path: '/a/dashboard/:username', component: AdminDashboard,  name: 'AdminDashboard', props: true, meta: { requiresAuth: true } },
    // {path: '/admin/profile', component: AdminProfile,  name: 'AdminProfile', props: true, meta: { requiresAuth: true } },
    {path: '/a/:username/find', component: AdminFind,  name: 'AdminFind', props: true, meta: { requiresAuth: true } },
    {path: '/a/:username/stats', component: AdminStats,  name: 'AdminStats', props: true, meta: { requiresAuth: true } },
    {path: '/a/:username/applications', component: AdminApplications,  name: 'Applications', props: true, meta: { requiresAuth: true } },
];

export default admin_routes;