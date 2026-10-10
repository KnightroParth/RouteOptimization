// Standalone Mock/Demo Data for MR Route Optimization
// Allows full interactive demo on Vercel preview even when backend is offline

export const mockUsers = {
  mr: {
    access_token: 'demo-mr-jwt-token-xyz',
    user: {
      id: 1,
      mr_id: 1,
      name: 'Rahul Sharma (MR)',
      email: 'mr@demo.com',
      role: 'mr',
      territory: 'Central & South Mumbai',
    },
  },
  manager: {
    access_token: 'demo-manager-jwt-token-abc',
    user: {
      id: 2,
      name: 'Dr. Suresh Mehta (Manager)',
      email: 'manager@demo.com',
      role: 'manager',
      territory: 'Western Region',
    },
  },
};

export const mockDoctors = [
  { id: 1, name: 'Dr. Ananya Roy', specialty: 'Cardiology', hospital: 'Lilavati Hospital', territory: 'Bandra West, Mumbai', lat: 19.0519, lng: 72.8295, window: '09:30 - 11:30', duration: 25, priority: 'High', visit_frequency: 'Weekly' },
  { id: 2, name: 'Dr. Rajesh Verma', specialty: 'Orthopedics', hospital: 'Hinduja Healthcare', territory: 'Khar West, Mumbai', lat: 19.0705, lng: 72.8339, window: '11:00 - 13:00', duration: 20, priority: 'High', visit_frequency: 'Bi-weekly' },
  { id: 3, name: 'Dr. Priya Nair', specialty: 'Pediatrics', hospital: 'Nanavati Super Speciality', territory: 'Vile Parle, Mumbai', lat: 19.0988, lng: 72.8427, window: '13:30 - 15:00', duration: 30, priority: 'Medium', visit_frequency: 'Monthly' },
  { id: 4, name: 'Dr. Amit Kulkarni', specialty: 'Neurology', hospital: 'Kokilaben Hospital', territory: 'Andheri West, Mumbai', lat: 19.1312, lng: 72.8252, window: '15:30 - 17:30', duration: 25, priority: 'High', visit_frequency: 'Bi-weekly' },
  { id: 5, name: 'Dr. Sunita Deshmukh', specialty: 'General Medicine', hospital: 'Cooper Hospital', territory: 'Juhu, Mumbai', lat: 19.1077, lng: 72.8361, window: '10:00 - 12:00', duration: 15, priority: 'Medium', visit_frequency: 'Bi-weekly' },
  { id: 6, name: 'Dr. Vikram Joshi', specialty: 'Oncology', hospital: 'Tata Memorial Centre', territory: 'Parel, Mumbai', lat: 19.0044, lng: 72.8429, window: '14:00 - 16:30', duration: 30, priority: 'Low', visit_frequency: 'Monthly' },
  { id: 7, name: 'Dr. Meera Iyer', specialty: 'Dermatology', hospital: 'Skin Excellence Clinic', territory: 'Santacruz, Mumbai', lat: 19.0833, lng: 72.8397, window: '11:30 - 13:30', duration: 20, priority: 'Medium', visit_frequency: 'Monthly' },
  { id: 8, name: 'Dr. Rohan Patel', specialty: 'Diabetology', hospital: 'Endocrine Care Clinic', territory: 'Dadar West, Mumbai', lat: 19.0222, lng: 72.8431, window: '16:00 - 18:00', duration: 20, priority: 'High', visit_frequency: 'Weekly' },
];

export const mockMRDashboard = {
  total_visits: 8,
  completed_visits: 3,
  pending_visits: 5,
  high_priority_visits: 4,
  planned_distance_km: 21.8,
  estimated_travel_min: 75,
  efficiency_score: 94.2,
  on_time_rate: 98.0,
};

export const mockVisits = [
  { id: 101, doctor_id: 1, doctor_name: 'Dr. Ananya Roy', specialty: 'Cardiology', hospital: 'Lilavati Hospital', time_slot: '09:30 - 10:00', priority: 'High', status: 'completed', lat: 19.0519, lng: 72.8295, notes: 'Detailed discussion on new Beta-Blocker formulation.' },
  { id: 102, doctor_id: 2, doctor_name: 'Dr. Rajesh Verma', specialty: 'Orthopedics', hospital: 'Hinduja Healthcare', time_slot: '10:45 - 11:15', priority: 'High', status: 'completed', lat: 19.0705, lng: 72.8339, notes: 'Sample kit delivered. Positive feedback on joint supplement.' },
  { id: 103, doctor_id: 5, doctor_name: 'Dr. Sunita Deshmukh', specialty: 'General Medicine', hospital: 'Cooper Hospital', time_slot: '11:45 - 12:15', priority: 'Medium', status: 'completed', lat: 19.1077, lng: 72.8361, notes: 'Follow-up regarding clinical trial brochure.' },
  { id: 104, doctor_id: 3, doctor_name: 'Dr. Priya Nair', specialty: 'Pediatrics', hospital: 'Nanavati Super Speciality', time_slot: '13:30 - 14:00', priority: 'Medium', status: 'in-progress', lat: 19.0988, lng: 72.8427, notes: 'En route to clinic.' },
  { id: 105, doctor_id: 4, doctor_name: 'Dr. Amit Kulkarni', specialty: 'Neurology', hospital: 'Kokilaben Hospital', time_slot: '15:30 - 16:00', priority: 'High', status: 'pending', lat: 19.1312, lng: 72.8252, notes: 'Key opinion leader meeting scheduled.' },
  { id: 106, doctor_id: 7, doctor_name: 'Dr. Meera Iyer', specialty: 'Dermatology', hospital: 'Skin Excellence Clinic', time_slot: '16:30 - 17:00', priority: 'Medium', status: 'pending', lat: 19.0833, lng: 72.8397, notes: 'Topical anti-fungal product showcase.' },
  { id: 107, doctor_id: 8, doctor_name: 'Dr. Rohan Patel', specialty: 'Diabetology', hospital: 'Endocrine Care Clinic', time_slot: '17:30 - 18:00', priority: 'High', status: 'pending', lat: 19.0222, lng: 72.8431, notes: 'Reviewing quarterly prescription metrics.' },
  { id: 108, doctor_id: 6, doctor_name: 'Dr. Vikram Joshi', specialty: 'Oncology', hospital: 'Tata Memorial Centre', time_slot: '18:30 - 19:00', priority: 'Low', status: 'pending', lat: 19.0044, lng: 72.8429, notes: 'General relationship check-in.' },
];

export const mockGeneratedRoute = {
  route_id: 'ROUTE-OPT-20261010-01',
  date: new Date().toISOString().split('T')[0],
  status: 'optimized',
  total_distance_km: 21.8,
  total_travel_time_min: 75,
  total_service_time_min: 170,
  algorithm: 'Google OR-Tools VRPTW + Random Forest ML Priority',
  stops: [
    { stop_number: 1, doctor_name: 'Dr. Ananya Roy', specialty: 'Cardiology', eta: '09:30 AM', etd: '09:55 AM', priority: 'High', lat: 19.0519, lng: 72.8295, address: 'Bandra West' },
    { stop_number: 2, doctor_name: 'Dr. Rajesh Verma', specialty: 'Orthopedics', eta: '10:45 AM', etd: '11:10 AM', priority: 'High', lat: 19.0705, lng: 72.8339, address: 'Khar West' },
    { stop_number: 3, doctor_name: 'Dr. Sunita Deshmukh', specialty: 'General Medicine', eta: '11:45 AM', etd: '12:05 PM', priority: 'Medium', lat: 19.1077, lng: 72.8361, address: 'Juhu' },
    { stop_number: 4, doctor_name: 'Dr. Priya Nair', specialty: 'Pediatrics', eta: '01:30 PM', etd: '02:00 PM', priority: 'Medium', lat: 19.0988, lng: 72.8427, address: 'Vile Parle' },
    { stop_number: 5, doctor_name: 'Dr. Amit Kulkarni', specialty: 'Neurology', eta: '03:30 PM', etd: '04:00 PM', priority: 'High', lat: 19.1312, lng: 72.8252, address: 'Andheri West' },
    { stop_number: 6, doctor_name: 'Dr. Meera Iyer', specialty: 'Dermatology', eta: '04:30 PM', etd: '04:55 PM', priority: 'Medium', lat: 19.0833, lng: 72.8397, address: 'Santacruz' },
    { stop_number: 7, doctor_name: 'Dr. Rohan Patel', specialty: 'Diabetology', eta: '05:30 PM', etd: '05:55 PM', priority: 'High', lat: 19.0222, lng: 72.8431, address: 'Dadar West' },
    { stop_number: 8, doctor_name: 'Dr. Vikram Joshi', specialty: 'Oncology', eta: '06:30 PM', etd: '07:00 PM', priority: 'Low', lat: 19.0044, lng: 72.8429, address: 'Parel' },
  ],
};

export const mockManagerDashboard = {
  total_mrs: 14,
  active_mrs_today: 12,
  total_doctors: 184,
  total_planned_visits: 112,
  completed_visits: 89,
  team_completion_rate: 79.4,
  high_priority_coverage_rate: 96.2,
  total_distance_saved_km: 184.6,
  mr_summaries: [
    { mr_id: 1, name: 'Rahul Sharma', territory: 'Mumbai Central', planned: 8, completed: 3, pending: 5, compliance: 100 },
    { mr_id: 2, name: 'Vikram Seth', territory: 'South Mumbai', planned: 9, completed: 8, pending: 1, compliance: 95 },
    { mr_id: 3, name: 'Neha Gupta', territory: 'Western Suburbs', planned: 10, completed: 9, pending: 1, compliance: 98 },
    { mr_id: 4, name: 'Arjun Das', territory: 'Navi Mumbai', planned: 7, completed: 6, pending: 1, compliance: 92 },
  ],
};
