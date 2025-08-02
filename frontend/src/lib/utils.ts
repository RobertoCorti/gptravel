import { type ClassValue, clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';
import { format, isAfter, isBefore } from 'date-fns';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatDate(date: Date): string {
  return format(date, 'yyyy-MM-dd');
}

export function isValidDateRange(departureDate: Date, returnDate: Date): boolean {
  return isBefore(departureDate, returnDate) || departureDate.getTime() === returnDate.getTime();
}

export function calculateTripDuration(departureDate: Date, returnDate: Date): number {
  const timeDiff = returnDate.getTime() - departureDate.getTime();
  return Math.ceil(timeDiff / (1000 * 3600 * 24)) + 1;
}

export function validateOpenAIKey(key: string): boolean {
  return key.startsWith('sk-') && key.length > 20;
} 
