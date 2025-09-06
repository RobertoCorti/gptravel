import { NextRequest, NextResponse } from 'next/server';
import { FlightSearchParams, FlightSearchResponse, FlightOffer } from '@/types/travel';

// Amadeus API configuration (server-side only)
const AMADEUS_BASE_URL = process.env.NEXT_PUBLIC_AMADEUS_BASE_URL || 'https://test.api.amadeus.com';
const AMADEUS_API_KEY = process.env.NEXT_PUBLIC_AMADEUS_API_KEY;
const AMADEUS_API_SECRET = process.env.AMADEUS_API_SECRET;

// Token management
let accessToken: string | null = null;
let tokenExpiry: number = 0;

interface AmadeusAuthResponse {
  access_token: string;
  expires_in: number;
  token_type: string;
}

interface AmadeusFlightOffer {
  id: string;
  source: string;
  instantTicketingRequired: boolean;
  nonHomogeneous: boolean;
  oneWay: boolean;
  lastTicketingDate: string;
  numberOfBookableSeats: number;
  itineraries: Array<{
    duration: string;
    segments: Array<{
      departure: {
        iataCode: string;
        terminal?: string;
        at: string;
      };
      arrival: {
        iataCode: string;
        terminal?: string;
        at: string;
      };
      carrierCode: string;
      number: string;
      aircraft: {
        code: string;
      };
      operating?: {
        carrierCode: string;
      };
      duration: string;
      id: string;
      numberOfStops: number;
      blacklistedInEU: boolean;
    }>;
  }>;
  price: {
    currency: string;
    total: string;
    base: string;
    fees: Array<{
      amount: string;
      type: string;
    }>;
    grandTotal: string;
  };
  pricingOptions: {
    fareType: string[];
    includedCheckedBagsOnly: boolean;
  };
  validatingAirlineCodes: string[];
  travelerPricings: Array<{
    travelerId: string;
    fareOption: string;
    travelerType: string;
    price: {
      currency: string;
      total: string;
      base: string;
    };
    fareDetailsBySegment: Array<{
      segmentId: string;
      cabin: string;
      fareBasis: string;
      class: string;
      includedCheckedBags: {
        quantity: number;
      };
    }>;
  }>;
}

interface AmadeusFlightResponse {
  meta: {
    count: number;
    links?: {
      self: string;
    };
  };
  data: AmadeusFlightOffer[];
  dictionaries: {
    locations: Record<string, {
      cityCode: string;
      countryCode: string;
    }>;
    aircraft: Record<string, string>;
    currencies: Record<string, string>;
    carriers: Record<string, string>;
  };
}

/**
 * Get access token from Amadeus API
 */
async function getAccessToken(): Promise<string> {
  // Return cached token if still valid
  if (accessToken && Date.now() < tokenExpiry) {
    return accessToken;
  }

  if (!AMADEUS_API_KEY || !AMADEUS_API_SECRET) {
    throw new Error('Amadeus API credentials not configured');
  }

  const response = await fetch(`${AMADEUS_BASE_URL}/v1/security/oauth2/token`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: new URLSearchParams({
      grant_type: 'client_credentials',
      client_id: AMADEUS_API_KEY,
      client_secret: AMADEUS_API_SECRET,
    }),
  });

  if (!response.ok) {
    const errorData = await response.text();
    throw new Error(`Authentication failed: ${response.status} ${errorData}`);
  }

  const data: AmadeusAuthResponse = await response.json();
  
  // Cache the token
  accessToken = data.access_token;
  tokenExpiry = Date.now() + (data.expires_in * 1000) - 60000; // Refresh 1 minute before expiry

  return accessToken;
}

/**
 * Get airport code from city name
 */
function getAirportCode(city: string): string {
  const cityAirportMap: Record<string, string> = {
    'new york': 'NYC',
    'london': 'LON',
    'paris': 'PAR',
    'tokyo': 'TYO',
    'los angeles': 'LAX',
    'chicago': 'CHI',
    'frankfurt': 'FRA',
    'amsterdam': 'AMS',
    'dubai': 'DXB',
    'singapore': 'SIN',
    'madrid': 'MAD',
    'rome': 'ROM',
    'barcelona': 'BCN',
    'milan': 'MIL',
    'munich': 'MUC',
    'miami': 'MIA',
    'san francisco': 'SFO',
    'boston': 'BOS',
    'toronto': 'YTO',
    'vancouver': 'YVR',
    'sydney': 'SYD',
    'melbourne': 'MEL',
    'bangkok': 'BKK',
    'hong kong': 'HKG',
    'seoul': 'SEL',
    'beijing': 'BJS',
    'shanghai': 'SHA',
    'istanbul': 'IST',
    'moscow': 'MOW',
    'cairo': 'CAI',
    'johannesburg': 'JNB',
    'sao paulo': 'SAO',
    'rio de janeiro': 'RIO',
    'mexico city': 'MEX',
    'mumbai': 'BOM',
    'delhi': 'DEL',
    'bangalore': 'BLR',
  };

  const normalizedCity = city.toLowerCase().trim();
  return cityAirportMap[normalizedCity] || city.substring(0, 3).toUpperCase();
}

/**
 * Convert Amadeus flight offer to our FlightOffer format
 */
function convertAmadeusOffer(
  amadeusOffer: AmadeusFlightOffer,
  dictionaries: AmadeusFlightResponse['dictionaries']
): FlightOffer {
  const firstItinerary = amadeusOffer.itineraries[0];
  const firstSegment = firstItinerary.segments[0];
  const lastSegment = firstItinerary.segments[firstItinerary.segments.length - 1];
  
  const departureDate = new Date(firstSegment.departure.at);
  const arrivalDate = new Date(lastSegment.arrival.at);
  
  const carrierCode = firstSegment.carrierCode;
  const airlineName = dictionaries.carriers[carrierCode] || carrierCode;
  
  return {
    id: amadeusOffer.id,
    airline: airlineName,
    flightNumber: `${carrierCode}${firstSegment.number}`,
    departure: {
      airport: firstSegment.departure.iataCode,
      city: dictionaries.locations[firstSegment.departure.iataCode]?.cityCode || firstSegment.departure.iataCode,
      time: departureDate.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: false }),
      date: departureDate.toISOString().split('T')[0],
    },
    arrival: {
      airport: lastSegment.arrival.iataCode,
      city: dictionaries.locations[lastSegment.arrival.iataCode]?.cityCode || lastSegment.arrival.iataCode,
      time: arrivalDate.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: false }),
      date: arrivalDate.toISOString().split('T')[0],
    },
    duration: firstItinerary.duration.replace('PT', '').replace('H', 'h ').replace('M', 'm'),
    price: {
      amount: parseFloat(amadeusOffer.price.total),
      currency: amadeusOffer.price.currency,
    },
    stops: firstItinerary.segments.length - 1,
    class: amadeusOffer.travelerPricings[0]?.fareDetailsBySegment[0]?.cabin.toLowerCase() || 'economy',
    bookingUrl: `https://www.amadeus.com/booking/${amadeusOffer.id}`,
  };
}

/**
 * Check if Amadeus API is configured
 */
function isAmadeusConfigured(): boolean {
  return !!(AMADEUS_API_KEY && AMADEUS_API_SECRET);
}

export async function POST(request: NextRequest) {
  try {
    // Check if Amadeus is configured
    if (!isAmadeusConfigured()) {
      return NextResponse.json(
        { 
          error: 'Amadeus API not configured',
          configured: false 
        },
        { status: 400 }
      );
    }

    const params: FlightSearchParams = await request.json();
    
    const token = await getAccessToken();
    
    const originCode = getAirportCode(params.departure);
    const destinationCode = getAirportCode(params.destination);
    
    // Format dates for Amadeus API (YYYY-MM-DD)
    const departureDate = new Date(params.departureDate).toISOString().split('T')[0];
    const returnDate = params.returnDate ? new Date(params.returnDate).toISOString().split('T')[0] : undefined;
    
    // Build query parameters
    const searchParams = new URLSearchParams({
      originLocationCode: originCode,
      destinationLocationCode: destinationCode,
      departureDate: departureDate,
      adults: (params.passengers || 1).toString(),
      max: '10',
      currencyCode: 'USD',
    });
    
    if (returnDate) {
      searchParams.append('returnDate', returnDate);
    }
    
    if (params.class && params.class !== 'economy') {
      searchParams.append('travelClass', params.class.toUpperCase());
    }

    const response = await fetch(
      `${AMADEUS_BASE_URL}/v2/shopping/flight-offers?${searchParams.toString()}`,
      {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      }
    );

    if (!response.ok) {
      const errorData = await response.text();
      console.error('Amadeus API error:', errorData);
      throw new Error(`Flight search failed: ${response.status}`);
    }

    const data: AmadeusFlightResponse = await response.json();
    
    if (!data.data || data.data.length === 0) {
      return NextResponse.json({
        outbound: [],
        return: undefined,
        searchParams: params,
      });
    }

    // Convert outbound flights
    const outbound = data.data
      .map(offer => convertAmadeusOffer(offer, data.dictionaries))
      .sort((a, b) => a.price.amount - b.price.amount);

    // For return flights, make a separate search if needed
    let returnFlights: FlightOffer[] | undefined;
    
    if (returnDate && params.returnDate) {
      try {
        const returnSearchParams = new URLSearchParams({
          originLocationCode: destinationCode,
          destinationLocationCode: originCode,
          departureDate: returnDate,
          adults: (params.passengers || 1).toString(),
          max: '10',
          currencyCode: 'USD',
        });

        const returnResponse = await fetch(
          `${AMADEUS_BASE_URL}/v2/shopping/flight-offers?${returnSearchParams.toString()}`,
          {
            method: 'GET',
            headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json',
            },
          }
        );

        if (returnResponse.ok) {
          const returnData: AmadeusFlightResponse = await returnResponse.json();
          returnFlights = returnData.data
            .map(offer => convertAmadeusOffer(offer, returnData.dictionaries))
            .sort((a, b) => a.price.amount - b.price.amount);
        }
      } catch (error) {
        console.warn('Failed to fetch return flights:', error);
      }
    }

    const result: FlightSearchResponse = {
      outbound,
      return: returnFlights,
      searchParams: params,
    };

    return NextResponse.json(result);

  } catch (error) {
    console.error('Flight search error:', error);
    return NextResponse.json(
      { 
        error: error instanceof Error ? error.message : 'Flight search failed',
        configured: isAmadeusConfigured()
      },
      { status: 500 }
    );
  }
}