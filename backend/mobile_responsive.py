#!/usr/bin/env python3
"""
Mobile-responsive система и multi-device preview
Конкурирует с Lovable.dev mobile-first approach
"""

import os
import json
import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import uuid

@dataclass
class ResponsiveBreakpoint:
    """Responsive breakpoint configuration"""
    name: str
    width: int
    prefix: str
    description: str

@dataclass
class MobileOptimization:
    """Mobile optimization settings"""
    viewport_meta: str
    touch_friendly: bool
    fast_click: bool
    responsive_images: bool
    mobile_navigation: bool

class MobileResponsiveGenerator:
    """Генератор mobile-first responsive компонентов"""
    
    def __init__(self):
        # Tailwind CSS breakpoints
        self.breakpoints = [
            ResponsiveBreakpoint("mobile", 640, "sm:", "Mobile devices"),
            ResponsiveBreakpoint("tablet", 768, "md:", "Tablets"),
            ResponsiveBreakpoint("desktop", 1024, "lg:", "Desktops"),
            ResponsiveBreakpoint("wide", 1280, "xl:", "Large screens"),
            ResponsiveBreakpoint("ultra", 1536, "2xl:", "Ultra-wide screens")
        ]
        
        self.mobile_optimization = MobileOptimization(
            viewport_meta='<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">',
            touch_friendly=True,
            fast_click=True,
            responsive_images=True,
            mobile_navigation=True
        )
    
    def generate_responsive_component(self, component_name: str, component_type: str = "general") -> str:
        """Генерирует responsive React компонент"""
        
        if component_type == "navigation":
            return self._generate_responsive_navigation()
        elif component_type == "hero":
            return self._generate_responsive_hero()
        elif component_type == "card":
            return self._generate_responsive_card()
        elif component_type == "form":
            return self._generate_responsive_form()
        elif component_type == "grid":
            return self._generate_responsive_grid()
        else:
            return self._generate_responsive_layout(component_name)
    
    def _generate_responsive_navigation(self) -> str:
        """Генерирует responsive навигацию"""
        return '''import React, { useState } from 'react';

const ResponsiveNavigation = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  return (
    <nav className="bg-white shadow-lg sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          {/* Logo */}
          <div className="flex-shrink-0 flex items-center">
            <div className="text-xl font-bold text-gray-900 sm:text-2xl">
              Logo
            </div>
          </div>

          {/* Desktop Menu */}
          <div className="hidden md:flex items-center space-x-8">
            <a href="#" className="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium transition-colors">
              Home
            </a>
            <a href="#" className="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium transition-colors">
              Products
            </a>
            <a href="#" className="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium transition-colors">
              About
            </a>
            <a href="#" className="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium transition-colors">
              Contact
            </a>
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden flex items-center">
            <button
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="text-gray-700 hover:text-blue-600 focus:outline-none focus:text-blue-600 p-2"
              aria-label="Toggle menu"
            >
              <svg className="h-6 w-6 fill-current" viewBox="0 0 24 24">
                {isMenuOpen ? (
                  <path fillRule="evenodd" clipRule="evenodd" d="M18.278 16.864a1 1 0 0 1-1.414 1.414l-4.829-4.828-4.828 4.828a1 1 0 0 1-1.414-1.414l4.828-4.829-4.828-4.828a1 1 0 0 1 1.414-1.414l4.829 4.828 4.828-4.828a1 1 0 1 1 1.414 1.414l-4.828 4.829 4.828 4.828z" />
                ) : (
                  <path fillRule="evenodd" d="M4 5h16a1 1 0 0 1 0 2H4a1 1 0 1 1 0-2zm0 6h16a1 1 0 0 1 0 2H4a1 1 0 0 1 0-2zm0 6h16a1 1 0 0 1 0 2H4a1 1 0 0 1 0-2z" />
                )}
              </svg>
            </button>
          </div>
        </div>

        {/* Mobile Menu */}
        {isMenuOpen && (
          <div className="md:hidden">
            <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3 border-t">
              <a href="#" className="text-gray-700 hover:text-blue-600 block px-3 py-2 rounded-md text-base font-medium">
                Home
              </a>
              <a href="#" className="text-gray-700 hover:text-blue-600 block px-3 py-2 rounded-md text-base font-medium">
                Products
              </a>
              <a href="#" className="text-gray-700 hover:text-blue-600 block px-3 py-2 rounded-md text-base font-medium">
                About
              </a>
              <a href="#" className="text-gray-700 hover:text-blue-600 block px-3 py-2 rounded-md text-base font-medium">
                Contact
              </a>
            </div>
          </div>
        )}
      </div>
    </nav>
  );
};

export default ResponsiveNavigation;'''
    
    def _generate_responsive_hero(self) -> str:
        """Генерирует responsive hero секцию"""
        return '''import React from 'react';

const ResponsiveHero = () => {
  return (
    <section className="bg-gradient-to-r from-blue-500 to-purple-600 text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col lg:flex-row items-center py-12 lg:py-20">
          {/* Text Content */}
          <div className="flex-1 text-center lg:text-left mb-8 lg:mb-0 lg:pr-8">
            <h1 className="text-3xl sm:text-4xl lg:text-5xl xl:text-6xl font-bold leading-tight mb-4">
              Build Amazing 
              <span className="block text-yellow-300">
                Mobile Apps
              </span>
            </h1>
            <p className="text-lg sm:text-xl lg:text-2xl mb-6 opacity-90 max-w-2xl mx-auto lg:mx-0">
              Create responsive, mobile-first applications that work perfectly on any device
            </p>
            
            {/* CTA Buttons */}
            <div className="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start">
              <button className="bg-white text-blue-600 px-6 py-3 sm:px-8 sm:py-4 rounded-lg font-semibold text-sm sm:text-base hover:bg-gray-100 transition-colors shadow-lg">
                Get Started Free
              </button>
              <button className="border-2 border-white text-white px-6 py-3 sm:px-8 sm:py-4 rounded-lg font-semibold text-sm sm:text-base hover:bg-white hover:text-blue-600 transition-colors">
                Watch Demo
              </button>
            </div>
          </div>
          
          {/* Image/Visual */}
          <div className="flex-1 max-w-md lg:max-w-lg">
            <div className="relative">
              <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-6 lg:p-8">
                <div className="bg-white rounded-xl h-48 sm:h-56 lg:h-64 flex items-center justify-center">
                  <div className="text-gray-400 text-center">
                    <div className="w-16 h-16 sm:w-20 sm:h-20 mx-auto mb-4 bg-gray-200 rounded-lg flex items-center justify-center">
                      📱
                    </div>
                    <p className="text-sm sm:text-base">Mobile Preview</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default ResponsiveHero;'''
    
    def _generate_responsive_card(self) -> str:
        """Генерирует responsive карточку"""
        return '''import React from 'react';

const ResponsiveCard = ({ title, description, image, price }) => {
  return (
    <div className="bg-white rounded-xl shadow-lg hover:shadow-xl transition-shadow overflow-hidden">
      {/* Image */}
      <div className="aspect-w-16 aspect-h-9 sm:aspect-h-10 lg:aspect-h-9">
        <img 
          src={image || 'https://images.unsplash.com/photo-1472214103451-9374bd1c798e?w=400&h=300&fit=crop'}
          alt={title}
          className="w-full h-48 sm:h-52 lg:h-48 object-cover"
        />
      </div>
      
      {/* Content */}
      <div className="p-4 sm:p-5 lg:p-6">
        <h3 className="text-lg sm:text-xl font-semibold text-gray-900 mb-2 line-clamp-2">
          {title}
        </h3>
        <p className="text-sm sm:text-base text-gray-600 mb-4 line-clamp-3">
          {description}
        </p>
        
        {/* Footer */}
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
          {price && (
            <div className="text-xl sm:text-2xl font-bold text-blue-600">
              ${price}
            </div>
          )}
          <button className="w-full sm:w-auto bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 sm:px-6 sm:py-2.5 rounded-lg font-medium transition-colors text-sm sm:text-base">
            Learn More
          </button>
        </div>
      </div>
    </div>
  );
};

export default ResponsiveCard;'''
    
    def _generate_responsive_form(self) -> str:
        """Генерирует responsive форму"""
        return '''import React, { useState } from 'react';

const ResponsiveForm = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    message: ''
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Form submitted:', formData);
  };

  return (
    <div className="max-w-2xl mx-auto p-4 sm:p-6 lg:p-8">
      <div className="bg-white rounded-xl shadow-lg p-6 sm:p-8">
        <h2 className="text-2xl sm:text-3xl font-bold text-gray-900 mb-2 text-center sm:text-left">
          Get In Touch
        </h2>
        <p className="text-gray-600 mb-6 text-center sm:text-left">
          We'd love to hear from you. Send us a message and we'll respond as soon as possible.
        </p>
        
        <form onSubmit={handleSubmit} className="space-y-4 sm:space-y-6">
          {/* Name Field */}
          <div>
            <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-2">
              Full Name
            </label>
            <input
              type="text"
              id="name"
              name="name"
              value={formData.name}
              onChange={handleChange}
              className="w-full px-3 py-2 sm:px-4 sm:py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors text-sm sm:text-base"
              placeholder="Enter your full name"
              required
            />
          </div>
          
          {/* Email Field */}
          <div>
            <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">
              Email Address
            </label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              className="w-full px-3 py-2 sm:px-4 sm:py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors text-sm sm:text-base"
              placeholder="Enter your email"
              required
            />
          </div>
          
          {/* Message Field */}
          <div>
            <label htmlFor="message" className="block text-sm font-medium text-gray-700 mb-2">
              Message
            </label>
            <textarea
              id="message"
              name="message"
              value={formData.message}
              onChange={handleChange}
              rows="4"
              className="w-full px-3 py-2 sm:px-4 sm:py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors text-sm sm:text-base resize-vertical"
              placeholder="Tell us about your project..."
              required
            />
          </div>
          
          {/* Submit Button */}
          <button
            type="submit"
            className="w-full sm:w-auto sm:min-w-[150px] bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 sm:px-8 sm:py-4 rounded-lg font-semibold transition-colors text-sm sm:text-base shadow-lg hover:shadow-xl"
          >
            Send Message
          </button>
        </form>
      </div>
    </div>
  );
};

export default ResponsiveForm;'''
    
    def _generate_responsive_grid(self) -> str:
        """Генерирует responsive сетку"""
        return '''import React from 'react';

const ResponsiveGrid = ({ items = [] }) => {
  const defaultItems = [
    { id: 1, title: 'Item 1', description: 'Description for item 1' },
    { id: 2, title: 'Item 2', description: 'Description for item 2' },
    { id: 3, title: 'Item 3', description: 'Description for item 3' },
    { id: 4, title: 'Item 4', description: 'Description for item 4' },
    { id: 5, title: 'Item 5', description: 'Description for item 5' },
    { id: 6, title: 'Item 6', description: 'Description for item 6' }
  ];

  const displayItems = items.length > 0 ? items : defaultItems;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12">
      {/* Header */}
      <div className="text-center mb-8 sm:mb-12">
        <h2 className="text-2xl sm:text-3xl lg:text-4xl font-bold text-gray-900 mb-4">
          Responsive Grid Layout
        </h2>
        <p className="text-sm sm:text-base lg:text-lg text-gray-600 max-w-3xl mx-auto">
          This grid automatically adapts to different screen sizes for optimal viewing experience
        </p>
      </div>

      {/* Responsive Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 sm:gap-6 lg:gap-8">
        {displayItems.map((item) => (
          <div key={item.id} className="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow overflow-hidden">
            {/* Image placeholder */}
            <div className="aspect-w-16 aspect-h-9 bg-gradient-to-br from-blue-400 to-purple-500">
              <div className="w-full h-32 sm:h-36 lg:h-32 flex items-center justify-center text-white text-xl sm:text-2xl font-bold">
                {item.id}
              </div>
            </div>
            
            {/* Content */}
            <div className="p-3 sm:p-4 lg:p-5">
              <h3 className="text-base sm:text-lg lg:text-xl font-semibold text-gray-900 mb-2">
                {item.title}
              </h3>
              <p className="text-xs sm:text-sm lg:text-base text-gray-600 line-clamp-3">
                {item.description}
              </p>
              
              {/* Action */}
              <div className="mt-3 sm:mt-4">
                <button className="w-full sm:w-auto bg-blue-600 hover:bg-blue-700 text-white px-3 py-2 sm:px-4 sm:py-2 rounded-md text-xs sm:text-sm font-medium transition-colors">
                  View Details
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Load More */}
      <div className="text-center mt-8 sm:mt-12">
        <button className="bg-gray-200 hover:bg-gray-300 text-gray-800 px-6 py-3 sm:px-8 sm:py-4 rounded-lg font-medium text-sm sm:text-base transition-colors">
          Load More Items
        </button>
      </div>
    </div>
  );
};

export default ResponsiveGrid;'''
    
    def _generate_responsive_layout(self, component_name: str) -> str:
        """Генерирует общий responsive layout"""
        return f'''import React from 'react';

const {component_name} = ({{ children }}) => {{
  return (
    <div className="min-h-screen bg-gray-50">
      {{/* Mobile-first responsive container */}}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {{/* Header */}}
        <header className="py-4 sm:py-6 lg:py-8">
          <h1 className="text-xl sm:text-2xl lg:text-3xl xl:text-4xl font-bold text-gray-900 text-center sm:text-left">
            {component_name.replace("Component", "")}
          </h1>
        </header>

        {{/* Main Content */}}
        <main className="py-4 sm:py-6 lg:py-8">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-4 sm:gap-6 lg:gap-8">
            
            {{/* Sidebar */}}
            <aside className="lg:col-span-3">
              <div className="bg-white rounded-lg shadow p-4 sm:p-6">
                <h3 className="text-base sm:text-lg font-semibold text-gray-900 mb-3 sm:mb-4">
                  Navigation
                </h3>
                <nav className="space-y-2">
                  <a href="#" className="block px-3 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded transition-colors">
                    Dashboard
                  </a>
                  <a href="#" className="block px-3 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded transition-colors">
                    Products
                  </a>
                  <a href="#" className="block px-3 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded transition-colors">
                    Orders
                  </a>
                  <a href="#" className="block px-3 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded transition-colors">
                    Settings
                  </a>
                </nav>
              </div>
            </aside>

            {{/* Main Content Area */}}
            <section className="lg:col-span-9">
              <div className="bg-white rounded-lg shadow p-4 sm:p-6 lg:p-8">
                {{children || (
                  <div className="text-center py-8 sm:py-12">
                    <div className="text-4xl sm:text-5xl lg:text-6xl mb-4">📱</div>
                    <h2 className="text-lg sm:text-xl lg:text-2xl font-semibold text-gray-900 mb-2">
                      Mobile-First Design
                    </h2>
                    <p className="text-sm sm:text-base text-gray-600 max-w-md mx-auto">
                      This component is optimized for mobile devices and scales beautifully to larger screens.
                    </p>
                  </div>
                )}}
              </div>
            </section>

          </div>
        </main>

        {{/* Footer */}}
        <footer className="py-6 sm:py-8 mt-8 sm:mt-12 border-t border-gray-200">
          <div className="text-center text-xs sm:text-sm text-gray-500">
            <p>© 2024 Vibecode AI. Mobile-optimized and responsive.</p>
          </div>
        </footer>

      </div>
    </div>
  );
}};

export default {component_name};'''
    
    def generate_mobile_styles(self) -> str:
        """Генерирует CSS стили для мобильной оптимизации"""
        return '''/* Mobile-First Responsive Styles */

/* Base mobile styles (default) */
.container {
  padding: 16px;
  max-width: 100%;
}

.text-responsive {
  font-size: 16px;
  line-height: 1.5;
}

.button-responsive {
  padding: 12px 16px;
  font-size: 14px;
  width: 100%;
  min-height: 44px; /* Touch target minimum */
}

/* Small devices (landscape phones, 640px and up) */
@media (min-width: 640px) {
  .container {
    padding: 24px;
    max-width: 640px;
    margin: 0 auto;
  }
  
  .text-responsive {
    font-size: 18px;
  }
  
  .button-responsive {
    width: auto;
    padding: 12px 24px;
  }
}

/* Medium devices (tablets, 768px and up) */
@media (min-width: 768px) {
  .container {
    padding: 32px;
    max-width: 768px;
  }
  
  .text-responsive {
    font-size: 20px;
  }
}

/* Large devices (desktops, 1024px and up) */
@media (min-width: 1024px) {
  .container {
    padding: 40px;
    max-width: 1024px;
  }
  
  .text-responsive {
    font-size: 22px;
  }
}

/* Extra large devices (large desktops, 1280px and up) */
@media (min-width: 1280px) {
  .container {
    max-width: 1280px;
  }
  
  .text-responsive {
    font-size: 24px;
  }
}

/* Touch-friendly interactions */
@media (hover: none) and (pointer: coarse) {
  .hover-effect:hover {
    /* Disable hover effects on touch devices */
    background-color: inherit;
  }
  
  .touch-target {
    min-height: 44px;
    min-width: 44px;
  }
}

/* Print styles */
@media print {
  .no-print {
    display: none !important;
  }
  
  .print-break {
    page-break-before: always;
  }
}

/* Reduced motion for accessibility */
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}

/* High contrast mode */
@media (prefers-contrast: high) {
  .button-responsive {
    border: 2px solid;
  }
}'''
    
    def generate_viewport_config(self) -> Dict[str, str]:
        """Генерирует конфигурацию viewport для мобильных устройств"""
        return {
            'meta_viewport': self.mobile_optimization.viewport_meta,
            'next_config': '''/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  
  // Mobile optimizations
  experimental: {
    optimizeCss: true,
    scrollRestoration: true,
  },
  
  // Image optimization
  images: {
    deviceSizes: [640, 750, 828, 1080, 1200, 1920, 2048, 3840],
    imageSizes: [16, 32, 48, 64, 96, 128, 256, 384],
    formats: ['image/webp', 'image/avif'],
  },
  
  // PWA configuration
  pwa: {
    dest: 'public',
    register: true,
    skipWaiting: true,
    disable: process.env.NODE_ENV === 'development'
  }
}

module.exports = nextConfig''',
            'tailwind_config': '''/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    screens: {
      'xs': '475px',
      'sm': '640px',
      'md': '768px',
      'lg': '1024px',
      'xl': '1280px',
      '2xl': '1536px',
    },
    extend: {
      // Mobile-first spacing
      spacing: {
        'safe-top': 'env(safe-area-inset-top)',
        'safe-bottom': 'env(safe-area-inset-bottom)',
        'safe-left': 'env(safe-area-inset-left)',
        'safe-right': 'env(safe-area-inset-right)',
      },
      
      // Touch-friendly sizes
      minHeight: {
        'touch': '44px',
      },
      minWidth: {
        'touch': '44px',
      },
      
      // Mobile typography
      fontSize: {
        'xs-mobile': ['12px', '16px'],
        'sm-mobile': ['14px', '20px'],
        'base-mobile': ['16px', '24px'],
        'lg-mobile': ['18px', '28px'],
      }
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
    require('@tailwindcss/aspect-ratio'),
    require('@tailwindcss/line-clamp'),
  ],
}'''
        }

class DevicePreviewGenerator:
    """Генератор preview для разных устройств"""
    
    def __init__(self):
        self.devices = {
            'mobile': {'width': 375, 'height': 667, 'name': 'iPhone SE'},
            'tablet': {'width': 768, 'height': 1024, 'name': 'iPad'},
            'desktop': {'width': 1440, 'height': 900, 'name': 'Desktop'},
            'wide': {'width': 1920, 'height': 1080, 'name': 'Wide Screen'}
        }
    
    def generate_preview_interface(self) -> str:
        """Генерирует интерфейс для preview разных устройств"""
        return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Multi-Device Preview</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f5f5f7;
            height: 100vh;
            overflow: hidden;
        }
        
        .preview-container {
            display: flex;
            flex-direction: column;
            height: 100vh;
        }
        
        .device-selector {
            background: white;
            padding: 16px 24px;
            border-bottom: 1px solid #e5e5e7;
            display: flex;
            align-items: center;
            gap: 16px;
            flex-wrap: wrap;
        }
        
        .device-btn {
            padding: 8px 16px;
            border: 2px solid #007AFF;
            background: transparent;
            color: #007AFF;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 500;
            transition: all 0.2s ease;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .device-btn.active {
            background: #007AFF;
            color: white;
        }
        
        .device-btn:hover {
            background: #007AFF;
            color: white;
        }
        
        .preview-frame {
            flex: 1;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 24px;
            position: relative;
        }
        
        .device-frame {
            background: white;
            border-radius: 12px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            overflow: hidden;
            transition: all 0.3s ease;
            position: relative;
        }
        
        .device-frame::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 60px;
            background: #f8f9fa;
            border-bottom: 1px solid #e9ecef;
            z-index: 10;
        }
        
        .frame-header {
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 60px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 16px;
            background: #f8f9fa;
            border-bottom: 1px solid #e9ecef;
            z-index: 20;
            font-size: 12px;
            color: #666;
        }
        
        .frame-info {
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .frame-controls {
            display: flex;
            gap: 8px;
        }
        
        .control-btn {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            border: none;
            cursor: pointer;
        }
        
        .control-btn.close { background: #ff5f57; }
        .control-btn.minimize { background: #ffbd2e; }
        .control-btn.maximize { background: #28ca42; }
        
        .device-iframe {
            width: 100%;
            height: 100%;
            border: none;
            margin-top: 60px;
        }
        
        /* Device-specific styles */
        .device-mobile {
            width: 375px;
            height: 667px;
        }
        
        .device-tablet {
            width: 768px;
            height: 1024px;
        }
        
        .device-desktop {
            width: 1200px;
            height: 800px;
        }
        
        .device-wide {
            width: 1440px;
            height: 900px;
        }
        
        /* Responsive adjustments */
        @media (max-width: 1600px) {
            .device-wide {
                width: 1200px;
                height: 750px;
            }
        }
        
        @media (max-width: 1280px) {
            .device-desktop {
                width: 1000px;
                height: 650px;
            }
        }
        
        @media (max-width: 1024px) {
            .device-tablet {
                width: 600px;
                height: 800px;
            }
        }
        
        @media (max-width: 768px) {
            .device-mobile {
                width: 320px;
                height: 568px;
            }
            
            .device-selector {
                padding: 12px 16px;
                gap: 12px;
            }
            
            .device-btn {
                padding: 6px 12px;
                font-size: 12px;
            }
        }
    </style>
</head>
<body>
    <div class="preview-container">
        <div class="device-selector">
            <div class="frame-info">
                <strong>Multi-Device Preview</strong>
                <span id="currentDevice">Mobile</span>
            </div>
            
            <div style="display: flex; gap: 12px; flex-wrap: wrap;">
                <button class="device-btn active" data-device="mobile">
                    📱 Mobile
                </button>
                <button class="device-btn" data-device="tablet">
                    📟 Tablet
                </button>
                <button class="device-btn" data-device="desktop">
                    🖥️ Desktop
                </button>
                <button class="device-btn" data-device="wide">
                    📺 Wide
                </button>
            </div>
            
            <div style="margin-left: auto;">
                <button class="device-btn" onclick="refreshPreview()">
                    🔄 Refresh
                </button>
            </div>
        </div>
        
        <div class="preview-frame">
            <div class="device-frame device-mobile" id="deviceFrame">
                <div class="frame-header">
                    <div class="frame-info">
                        <span id="deviceName">iPhone SE</span>
                        <span id="deviceDimensions">375×667</span>
                    </div>
                    <div class="frame-controls">
                        <button class="control-btn close"></button>
                        <button class="control-btn minimize"></button>
                        <button class="control-btn maximize"></button>
                    </div>
                </div>
                <iframe 
                    class="device-iframe" 
                    id="previewIframe"
                    src="about:blank">
                </iframe>
            </div>
        </div>
    </div>

    <script>
        const devices = {
            mobile: { width: 375, height: 667, name: 'iPhone SE', icon: '📱' },
            tablet: { width: 768, height: 1024, name: 'iPad', icon: '📟' },
            desktop: { width: 1200, height: 800, name: 'Desktop', icon: '🖥️' },
            wide: { width: 1440, height: 900, name: 'Wide Screen', icon: '📺' }
        };
        
        let currentDevice = 'mobile';
        let previewUrl = '';
        
        // Initialize
        document.addEventListener('DOMContentLoaded', function() {
            setupDeviceButtons();
            updateDeviceFrame('mobile');
        });
        
        function setupDeviceButtons() {
            document.querySelectorAll('.device-btn[data-device]').forEach(btn => {
                btn.addEventListener('click', function() {
                    const device = this.dataset.device;
                    switchDevice(device);
                });
            });
        }
        
        function switchDevice(device) {
            if (!devices[device]) return;
            
            // Update active button
            document.querySelectorAll('.device-btn[data-device]').forEach(btn => {
                btn.classList.remove('active');
            });
            document.querySelector(`[data-device="${device}"]`).classList.add('active');
            
            // Update device frame
            updateDeviceFrame(device);
            currentDevice = device;
        }
        
        function updateDeviceFrame(device) {
            const deviceInfo = devices[device];
            const frame = document.getElementById('deviceFrame');
            
            // Remove all device classes
            frame.className = 'device-frame';
            // Add new device class
            frame.classList.add(`device-${device}`);
            
            // Update info
            document.getElementById('currentDevice').textContent = deviceInfo.name;
            document.getElementById('deviceName').textContent = deviceInfo.name;
            document.getElementById('deviceDimensions').textContent = `${deviceInfo.width}×${deviceInfo.height}`;
        }
        
        function refreshPreview() {
            const iframe = document.getElementById('previewIframe');
            iframe.src = iframe.src;
        }
        
        function loadPreview(url) {
            previewUrl = url;
            document.getElementById('previewIframe').src = url;
        }
        
        // Expose functions globally
        window.switchDevice = switchDevice;
        window.loadPreview = loadPreview;
        window.refreshPreview = refreshPreview;
    </script>
</body>
</html>'''

def test_mobile_responsive():
    """Тестирование mobile-responsive системы"""
    
    generator = MobileResponsiveGenerator()
    device_preview = DevicePreviewGenerator()
    
    print("🧪 Тестирование Mobile-Responsive системы:")
    
    # Тестируем генерацию компонентов
    components = ['navigation', 'hero', 'card', 'form', 'grid']
    
    for component_type in components:
        component_code = generator.generate_responsive_component(
            f"Responsive{component_type.capitalize()}", 
            component_type
        )
        print(f"✅ Сгенерирован responsive {component_type}: {len(component_code)} символов")
    
    # Тестируем конфигурации
    viewport_config = generator.generate_viewport_config()
    mobile_styles = generator.generate_mobile_styles()
    preview_interface = device_preview.generate_preview_interface()
    
    print(f"✅ Viewport конфигурация: {len(viewport_config)} элементов")
    print(f"✅ Mobile стили: {len(mobile_styles)} символов") 
    print(f"✅ Preview интерфейс: {len(preview_interface)} символов")
    
    print("\n🎉 Mobile-Responsive система готова!")

if __name__ == "__main__":
    test_mobile_responsive()