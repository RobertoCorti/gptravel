// Travel form types
export interface TravelFormData {
  openaiKey: string;
  departure: string;
  destination: string;
  departureDate: Date;
  returnDate: Date;
  travelReason: 'Business' | 'Romantic' | 'Solo' | 'Friends' | 'Family' | '';
}

// Travel plan response types
export interface TravelPlan {
  [day: string]: {
    [city: string]: string[];
  };
}

export interface TravelPlanResponse {
  departure_place: string;
  destination_place: string;
  n_days: number;
  travel_plan: TravelPlan;
  weighted_score?: number;
}

// Location and mapping types
export interface Coordinates {
  lat: number;
  lng: number;
}

export interface LocationInfo {
  name: string;
  coordinates: Coordinates;
  activities?: string[];
}

// API response types
export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
}

// Score types
export interface ScoreMap {
  'Activity Places': {
    recognized_entities: Record<string, Array<{ name: string; url?: string }>> | null;
  };
  'Activities Variety': {
    labeled_activities: Record<string, Record<string, number>> | null;
  };
}

export interface TravelPlanScore {
  weighted_score: number | null;
  score_map: ScoreMap;
}

// UI State types
export interface TravelPlanState {
  isLoading: boolean;
  data: TravelPlanResponse | null;
  error: string | null;
}

// Form validation types
export interface FormErrors {
  openaiKey?: string;
  departure?: string;
  destination?: string;
  departureDate?: string;
  returnDate?: string;
  travelReason?: string;
} 
