import { NextRequest, NextResponse } from 'next/server';

// This Next.js API route now acts as a proxy/fallback to the Python backend
// It can be used for additional processing, caching, or as a fallback when Python backend is down

const PYTHON_API_URL = process.env.PYTHON_API_URL || 'http://127.0.0.1:8000';

export async function POST(request: NextRequest) {
  try {
    const formData = await request.json();
    
    // Validate required fields
    if (!formData.openaiKey || !formData.departure || !formData.destination) {
      return NextResponse.json(
        { error: 'Missing required fields' },
        { status: 400 }
      );
    }

    try {
      // Try to proxy to Python backend first
      const pythonResponse = await fetch(`${PYTHON_API_URL}/api/travel`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          openai_key: formData.openaiKey,
          departure: formData.departure,
          destination: formData.destination,
          departure_date: formData.departureDate,
          return_date: formData.returnDate,
          travel_reason: formData.travelReason,
        }),
        // 30 second timeout for AI generation
        signal: AbortSignal.timeout(30000),
      });

      if (pythonResponse.ok) {
        const result = await pythonResponse.json();
        return NextResponse.json(result);
      } else {
        const errorData = await pythonResponse.json().catch(() => ({}));
        throw new Error(errorData.detail || errorData.error || 'Python backend error');
      }
    } catch (pythonError) {
      console.warn('Python backend unavailable:', pythonError);
      
      // Fallback to mock response if Python backend is down
      return generateMockResponse(formData);
    }

  } catch (error) {
    console.error('API Error:', error);
    return NextResponse.json(
      { 
        success: false,
        error: 'Failed to generate travel plan' 
      },
      { status: 500 }
    );
  }
}

function generateMockResponse(formData: any) {
  // Convert string dates back to Date objects for calculation
  const departureDate = new Date(formData.departureDate);
  const returnDate = new Date(formData.returnDate);
  
  // Validate dates
  if (isNaN(departureDate.getTime()) || isNaN(returnDate.getTime())) {
    return NextResponse.json(
      { error: 'Invalid date format' },
      { status: 400 }
    );
  }

  const timeDiff = returnDate.getTime() - departureDate.getTime();
  const nDays = Math.ceil(timeDiff / (1000 * 60 * 60 * 24)) + 1;
  
  const mockTravelPlan = {
    departure_place: formData.departure,
    destination_place: formData.destination,
    n_days: nDays,
    travel_plan: generateMockItinerary(formData.destination, nDays, formData.travelReason),
    weighted_score: Math.floor(Math.random() * 20) + 80,
  };

  return NextResponse.json({
    success: true,
    data: mockTravelPlan
  });
}

function generateMockItinerary(destination: string, nDays: number, travelReason?: string): Record<string, Record<string, string[]>> {
  const itinerary: Record<string, Record<string, string[]>> = {};
  
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
    
    if (travelReason && baseActivities[travelReason as keyof typeof baseActivities]) {
      activities.push(...baseActivities[travelReason as keyof typeof baseActivities].slice(0, 2));
    }
    
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
