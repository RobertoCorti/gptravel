import { NextRequest, NextResponse } from 'next/server';
import { TravelFormData, TravelPlanResponse } from '@/types/travel';

export async function POST(request: NextRequest) {
  try {
    const rawFormData = await request.json();
    
    // Convert string dates back to Date objects
    const formData: TravelFormData = {
      ...rawFormData,
      departureDate: new Date(rawFormData.departureDate),
      returnDate: new Date(rawFormData.returnDate),
    };
    
    // Validate required fields
    if (!formData.openaiKey || !formData.departure || !formData.destination) {
      return NextResponse.json(
        { error: 'Missing required fields' },
        { status: 400 }
      );
    }

    // Validate dates
    if (isNaN(formData.departureDate.getTime()) || isNaN(formData.returnDate.getTime())) {
      return NextResponse.json(
        { error: 'Invalid date format' },
        { status: 400 }
      );
    }

    // Calculate number of days
    const timeDiff = formData.returnDate.getTime() - formData.departureDate.getTime();
    const daysDiff = Math.ceil(timeDiff / (1000 * 60 * 60 * 24));
    
    if (daysDiff < 0) {
      return NextResponse.json(
        { error: 'Return date must be after departure date' },
        { status: 400 }
      );
    }

    const nDays = daysDiff + 1; // Include both departure and return days

    // For now, we'll create a mock response that matches your Python backend structure
    // This will be replaced with actual Python backend calls
    const mockTravelPlan: TravelPlanResponse = {
      departure_place: formData.departure,
      destination_place: formData.destination,
      n_days: nDays,
      travel_plan: generateMockItinerary(formData.destination, nDays, formData.travelReason),
      weighted_score: Math.floor(Math.random() * 20) + 80 // Random score between 80-100
    };

    // Simulate API processing time
    await new Promise(resolve => setTimeout(resolve, 2000));

    return NextResponse.json({
      success: true,
      data: mockTravelPlan
    });

  } catch (error) {
    console.error('Travel API Error:', error);
    return NextResponse.json(
      { error: 'Failed to generate travel plan' },
      { status: 500 }
    );
  }
}

function generateMockItinerary(destination: string, nDays: number, travelReason?: string): Record<string, Record<string, string[]>> {
  const itinerary: Record<string, Record<string, string[]>> = {};
  
  // Base activities by travel reason
  const baseActivities = {
    Business: [
      "Attend business meetings",
      "Network with local professionals", 
      "Visit business districts",
      "Explore coworking spaces"
    ],
    Romantic: [
      "Enjoy romantic dinner at local restaurant",
      "Take sunset walk in scenic area",
      "Visit couples spa",
      "Explore romantic viewpoints"
    ],
    Solo: [
      "Solo exploration of main attractions",
      "Visit local museums and galleries",
      "Try street food and local cuisine",
      "Join walking tours to meet people"
    ],
    Friends: [
      "Group activities and adventures",
      "Visit local bars and nightlife",
      "Try group sports or activities",
      "Explore entertainment districts"
    ],
    Family: [
      "Visit family-friendly attractions",
      "Explore parks and outdoor spaces",
      "Find kid-friendly restaurants",
      "Visit local markets and shops"
    ]
  };

  const generalActivities = [
    "Explore the city center and main attractions",
    "Visit top-rated museums and cultural sites",
    "Try authentic local cuisine",
    "Take guided walking tour",
    "Shop at local markets",
    "Visit historical landmarks",
    "Enjoy local entertainment",
    "Relax at popular cafes"
  ];

  for (let day = 1; day <= nDays; day++) {
    const dayKey = `Day ${day}`;
    const activities: string[] = [];
    
    if (day === 1) {
      activities.push("Arrive and check into accommodation");
    }
    
    // Add reason-specific activities
    if (travelReason && baseActivities[travelReason as keyof typeof baseActivities]) {
      activities.push(...baseActivities[travelReason as keyof typeof baseActivities].slice(0, 2));
    }
    
    // Add general activities
    const remainingSlots = Math.max(3 - activities.length, 1);
    const shuffledGeneral = [...generalActivities].sort(() => 0.5 - Math.random());
    activities.push(...shuffledGeneral.slice(0, remainingSlots));
    
    if (day === nDays) {
      activities.push("Departure preparations and travel to airport");
    }
    
    itinerary[dayKey] = {
      [destination]: activities
    };
  }
  
  return itinerary;
}

// TODO: Replace mock with actual Python backend integration
// This will involve:
// 1. Starting your Python backend server
// 2. Making HTTP requests to Python endpoints
// 3. Handling Python response data
// 4. Error handling and retries 
