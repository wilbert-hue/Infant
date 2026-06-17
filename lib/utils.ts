import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function formatNumber(value: number, decimals: number = 2): string {
  return value.toFixed(decimals)
}

export function formatCurrency(value: number, currency: string = 'USD', unit: string = 'Mn'): string {
  return `${currency} ${value.toFixed(2)} ${unit}`
}

// EUR conversion rate (1 USD = EUR_RATE EUR)
export const EUR_RATE = 0.92

// Get currency symbol based on currency preference
export function getCurrencySymbol(currency: 'USD' | 'EUR'): string {
  return currency === 'EUR' ? '€' : '$'
}

// Format unit based on currency preference
export function formatUnit(unit: string, currency: 'USD' | 'EUR'): string {
  return unit
}

// Apply currency conversion factor
export function getCurrencyConversionFactor(currency: 'USD' | 'EUR'): number {
  return currency === 'EUR' ? EUR_RATE : 1.0
}

// Format number according to Indian number system (lakhs, crores)
export function formatIndianNumber(value: number, decimals: number = 2): string {
  const absValue = Math.abs(value)
  let formatted: string
  
  if (absValue >= 10000000) {
    // Crores (1 crore = 10 million)
    formatted = (value / 10000000).toFixed(decimals) + ' Cr'
  } else if (absValue >= 100000) {
    // Lakhs (1 lakh = 100,000)
    formatted = (value / 100000).toFixed(decimals) + ' L'
  } else {
    formatted = value.toFixed(decimals)
  }
  
  return formatted
}

// Format number with Indian comma system (first 3 digits, then groups of 2)
export function formatIndianNumberWithCommas(value: number, decimals: number = 2): string {
  const parts = value.toFixed(decimals).split('.')
  const integerPart = parts[0]
  const decimalPart = parts[1]
  
  // Indian numbering: first 3 digits, then groups of 2
  let formatted = integerPart
  if (integerPart.length > 3) {
    const lastThree = integerPart.slice(-3)
    const remaining = integerPart.slice(0, -3)
    const groups = remaining.match(/.{1,2}/g) || []
    formatted = groups.join(',') + ',' + lastThree
  }
  
  return decimalPart ? `${formatted}.${decimalPart}` : formatted
}

// Format currency value based on currency preference
export function formatCurrencyValue(value: number, currency: 'USD' | 'EUR', showUnit: boolean = true): string {
  const symbol = currency === 'EUR' ? '€' : '$'
  if (value >= 1000000) {
    return `${symbol} ${(value / 1000000).toFixed(2)} Million`
  }
  return `${symbol} ${value.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`
}

export function formatPercentage(value: number, decimals: number = 2): string {
  return `${value.toFixed(decimals)}%`
}

export function calculateGrowth(startValue: number, endValue: number): number {
  if (startValue === 0) return 0
  return ((endValue - startValue) / startValue) * 100
}

