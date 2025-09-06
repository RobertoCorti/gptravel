'use client';

import { useState, useEffect, useCallback } from 'react';
import { Plane, Clock, MapPin, Users, Calendar, ExternalLink, Loader2, ArrowRight, Filter } from 'lucide-react';
import { FlightSearchParams, FlightSearchResponse, FlightOffer } from '@/types/travel';
import { searchFlightsAPI } from '@/lib/api';
import { motion, AnimatePresence } from 'framer-motion';
import Button from '@/components/ui/Button';

interface FlightSearchProps {
  initialParams?: Partial<FlightSearchParams>;
  onFlightSelect?: (flight: FlightOffer, type: 'outbound' | 'return') => void;
}

const FlightCard = ({ 
  flight, 
  type, 
  onSelect, 
  isSelected = false 
}: { 
  flight: FlightOffer; 
  type: 'outbound' | 'return';
  onSelect?: (flight: FlightOffer, type: 'outbound' | 'return') => void;
  isSelected?: boolean;
}) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className={`bg-white rounded-xl border-2 transition-all duration-200 hover:shadow-lg ${
        isSelected 
          ? 'border-travel-500 bg-travel-50' 
          : 'border-gray-200 hover:border-travel-300'
      }`}
    >
      <div className="p-6">
        {/* Flight Header */}
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-travel-100 rounded-full flex items-center justify-center">
              <Plane className="h-5 w-5 text-travel-600" />
            </div>
            <div>
              <h3 className="font-semibold text-gray-900">{flight.airline}</h3>
              <p className="text-sm text-gray-600">{flight.flightNumber}</p>
            </div>
          </div>
          <div className="text-right">
            <p className="text-2xl font-bold text-gray-900">
              ${flight.price.amount}
            </p>
            <p className="text-sm text-gray-600">{flight.price.currency}</p>
          </div>
        </div>

        {/* Flight Route */}
        <div className="flex items-center justify-between mb-4">
          <div className="text-center">
            <p className="text-lg font-semibold text-gray-900">{flight.departure.time}</p>
            <p className="text-sm text-gray-600">{flight.departure.airport}</p>
            <p className="text-xs text-gray-500">{flight.departure.city}</p>
          </div>
          
          <div className="flex-1 mx-4 relative">
            <div className="flex items-center justify-center">
              <div className="flex-1 h-px bg-gray-300"></div>
              <div className="mx-2 text-center">
                <ArrowRight className="h-4 w-4 text-gray-400 mx-auto mb-1" />
                <p className="text-xs text-gray-500">{flight.duration}</p>
              </div>
              <div className="flex-1 h-px bg-gray-300"></div>
            </div>
            {flight.stops > 0 && (
              <p className="text-xs text-center text-orange-600 mt-1">
                {flight.stops} stop{flight.stops > 1 ? 's' : ''}
              </p>
            )}
          </div>
          
          <div className="text-center">
            <p className="text-lg font-semibold text-gray-900">{flight.arrival.time}</p>
            <p className="text-sm text-gray-600">{flight.arrival.airport}</p>
            <p className="text-xs text-gray-500">{flight.arrival.city}</p>
          </div>
        </div>

        {/* Flight Details */}
        <div className="flex items-center justify-between text-sm text-gray-600 mb-4">
          <div className="flex items-center gap-4">
            <span className="flex items-center gap-1">
              <Calendar className="h-4 w-4" />
              {flight.departure.date}
            </span>
            <span className="flex items-center gap-1">
              <Clock className="h-4 w-4" />
              {flight.duration}
            </span>
            <span className="capitalize">{flight.class}</span>
          </div>
          {flight.stops === 0 && (
            <span className="bg-green-100 text-green-800 px-2 py-1 rounded-full text-xs font-medium">
              Direct
            </span>
          )}
        </div>

        {/* Action Buttons */}
        <div className="flex gap-3">
          {onSelect && (
            <Button
              type="button"
              onClick={() => onSelect(flight, type)}
              variant={isSelected ? "primary" : "secondary"}
              className="flex-1"
            >
              {isSelected ? 'Selected' : 'Select Flight'}
            </Button>
          )}
          {flight.bookingUrl && (
            <Button
              type="button"
              onClick={() => window.open(flight.bookingUrl, '_blank')}
              variant="ghost"
              className="flex items-center gap-2"
            >
              <ExternalLink className="h-4 w-4" />
              Book
            </Button>
          )}
        </div>
      </div>
    </motion.div>
  );
};

const FlightSearchForm = ({ 
  onSearch, 
  initialParams, 
  isLoading 
}: { 
  onSearch: (params: FlightSearchParams) => void;
  initialParams?: Partial<FlightSearchParams>;
  isLoading: boolean;
}) => {
  const [params, setParams] = useState<FlightSearchParams>({
    departure: initialParams?.departure || '',
    destination: initialParams?.destination || '',
    departureDate: initialParams?.departureDate || new Date(),
    returnDate: initialParams?.returnDate,
    passengers: initialParams?.passengers || 1,
    class: initialParams?.class || 'economy'
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSearch(params);
  };

  return (
    <form onSubmit={handleSubmit} className="bg-white rounded-xl border border-gray-200 p-6 space-y-4">
      <h3 className="text-lg font-semibold text-gray-900 flex items-center gap-2">
        <Plane className="h-5 w-5 text-travel-600" />
        Search Flights
      </h3>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">From</label>
          <input
            type="text"
            value={params.departure}
            onChange={(e) => setParams(prev => ({ ...prev, departure: e.target.value }))}
            placeholder="Departure city"
            className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-travel-500 focus:border-transparent"
            required
          />
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">To</label>
          <input
            type="text"
            value={params.destination}
            onChange={(e) => setParams(prev => ({ ...prev, destination: e.target.value }))}
            placeholder="Destination city"
            className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-travel-500 focus:border-transparent"
            required
          />
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Departure Date</label>
          <input
            type="date"
            value={params.departureDate.toISOString().split('T')[0]}
            onChange={(e) => setParams(prev => ({ ...prev, departureDate: new Date(e.target.value) }))}
            className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-travel-500 focus:border-transparent"
            required
          />
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Return Date (Optional)</label>
          <input
            type="date"
            value={params.returnDate?.toISOString().split('T')[0] || ''}
            onChange={(e) => setParams(prev => ({ 
              ...prev, 
              returnDate: e.target.value ? new Date(e.target.value) : undefined 
            }))}
            className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-travel-500 focus:border-transparent"
          />
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Passengers</label>
          <select
            value={params.passengers}
            onChange={(e) => setParams(prev => ({ ...prev, passengers: parseInt(e.target.value) }))}
            className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-travel-500 focus:border-transparent"
          >
            {[1, 2, 3, 4, 5, 6].map(num => (
              <option key={num} value={num}>{num} passenger{num > 1 ? 's' : ''}</option>
            ))}
          </select>
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Class</label>
          <select
            value={params.class}
            onChange={(e) => setParams(prev => ({ ...prev, class: e.target.value as 'economy' | 'business' | 'first' }))}
            className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-travel-500 focus:border-transparent"
          >
            <option value="economy">Economy</option>
            <option value="business">Business</option>
            <option value="first">First Class</option>
          </select>
        </div>
      </div>
      
      <Button
        type="submit"
        variant="primary"
        className="w-full"
        isLoading={isLoading}
        disabled={isLoading || !params.departure || !params.destination}
      >
        {isLoading ? 'Searching...' : 'Search Flights'}
      </Button>
    </form>
  );
};

export default function FlightSearch({ initialParams, onFlightSelect }: FlightSearchProps) {
  const [searchResults, setSearchResults] = useState<FlightSearchResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [selectedFlights, setSelectedFlights] = useState<{
    outbound?: FlightOffer;
    return?: FlightOffer;
  }>({});
  const [hasAutoSearched, setHasAutoSearched] = useState(false);

  const handleSearch = async (params: FlightSearchParams) => {
    setIsLoading(true);
    setError(null);
    
    try {
      const results = await searchFlightsAPI(params);
      setSearchResults(results);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to search flights');
    } finally {
      setIsLoading(false);
    }
  };

  const handleFlightSelect = useCallback((flight: FlightOffer, type: 'outbound' | 'return') => {
    setSelectedFlights(prev => ({
      ...prev,
      [type]: flight
    }));
    onFlightSelect?.(flight, type);
  }, [onFlightSelect]);

  // Auto-search if initial params are provided (only once)
  useEffect(() => {
    if (!hasAutoSearched && initialParams?.departure && initialParams?.destination && initialParams?.departureDate) {
      setHasAutoSearched(true);
      handleSearch({
        departure: initialParams.departure,
        destination: initialParams.destination,
        departureDate: initialParams.departureDate,
        returnDate: initialParams.returnDate,
        passengers: initialParams.passengers || 1,
        class: initialParams.class || 'economy'
      });
    }
  }, [
    hasAutoSearched,
    initialParams?.departure,
    initialParams?.destination,
    initialParams?.departureDate?.toISOString(),
    initialParams?.returnDate?.toISOString(),
    initialParams?.passengers,
    initialParams?.class
  ]);

  return (
    <div className="space-y-6">
      {/* Search Form */}
      <FlightSearchForm
        onSearch={handleSearch}
        initialParams={initialParams}
        isLoading={isLoading}
      />

      {/* Error Message */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-xl p-4">
          <p className="text-red-800">{error}</p>
        </div>
      )}

      {/* Loading State */}
      {isLoading && (
        <div className="flex items-center justify-center py-12">
          <Loader2 className="h-8 w-8 animate-spin text-travel-600" />
          <span className="ml-3 text-gray-600">Searching for flights...</span>
        </div>
      )}

      {/* Search Results */}
      {searchResults && !isLoading && (
        <div className="space-y-8">
          {/* Outbound Flights */}
          <div>
            <h3 className="text-xl font-semibold text-gray-900 mb-4 flex items-center gap-2">
              <Plane className="h-5 w-5 text-travel-600" />
              Outbound Flights
              <span className="text-sm font-normal text-gray-600">
                ({searchResults.outbound.length} options)
              </span>
            </h3>
            <div className="grid gap-4">
              {searchResults.outbound.map((flight) => (
                <FlightCard
                  key={flight.id}
                  flight={flight}
                  type="outbound"
                  onSelect={handleFlightSelect}
                  isSelected={selectedFlights.outbound?.id === flight.id}
                />
              ))}
            </div>
          </div>

          {/* Return Flights */}
          {searchResults.return && (
            <div>
              <h3 className="text-xl font-semibold text-gray-900 mb-4 flex items-center gap-2">
                <Plane className="h-5 w-5 text-travel-600 rotate-180" />
                Return Flights
                <span className="text-sm font-normal text-gray-600">
                  ({searchResults.return.length} options)
                </span>
              </h3>
              <div className="grid gap-4">
                {searchResults.return.map((flight) => (
                  <FlightCard
                    key={flight.id}
                    flight={flight}
                    type="return"
                    onSelect={handleFlightSelect}
                    isSelected={selectedFlights.return?.id === flight.id}
                  />
                ))}
              </div>
            </div>
          )}

          {/* Selection Summary */}
          {(selectedFlights.outbound || selectedFlights.return) && (
            <div className="bg-travel-50 border border-travel-200 rounded-xl p-6">
              <h4 className="font-semibold text-travel-900 mb-4">Selected Flights</h4>
              <div className="space-y-3">
                {selectedFlights.outbound && (
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-travel-700">
                      Outbound: {selectedFlights.outbound.airline} {selectedFlights.outbound.flightNumber}
                    </span>
                    <span className="font-semibold text-travel-900">
                      ${selectedFlights.outbound.price.amount}
                    </span>
                  </div>
                )}
                {selectedFlights.return && (
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-travel-700">
                      Return: {selectedFlights.return.airline} {selectedFlights.return.flightNumber}
                    </span>
                    <span className="font-semibold text-travel-900">
                      ${selectedFlights.return.price.amount}
                    </span>
                  </div>
                )}
                <div className="border-t border-travel-200 pt-3 flex items-center justify-between">
                  <span className="font-semibold text-travel-900">Total</span>
                  <span className="text-xl font-bold text-travel-900">
                    ${(selectedFlights.outbound?.price.amount || 0) + (selectedFlights.return?.price.amount || 0)}
                  </span>
                </div>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}