#!/usr/bin/env python3
"""
Генератор настоящих full-stack приложений
Создает React/Next.js проекты с backend, базой данных и развертыванием
"""

import os
import json
import uuid
import zipfile
import tempfile
import shutil
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import subprocess
import requests

@dataclass
class FullStackProject:
    """Структура full-stack проекта"""
    project_id: str
    name: str
    type: str
    framework: str  # 'nextjs', 'react', 'vue'
    description: str
    frontend_files: Dict[str, str]
    backend_files: Dict[str, str]
    database_schema: Dict[str, Any]
    env_variables: Dict[str, str]
    package_json: Dict[str, Any]
    deployment_config: Dict[str, Any]
    created_at: str
    github_repo: Optional[str] = None
    deployed_url: Optional[str] = None

class FullStackGenerator:
    """Генератор полноценных full-stack приложений"""
    
    def __init__(self):
        self.projects_dir = os.path.join(os.path.dirname(__file__), 'fullstack_projects')
        self.ensure_projects_dir()
        
        # Шаблоны для разных типов проектов
        self.project_templates = {
            'ecommerce': self._generate_ecommerce_project,
            'blog': self._generate_universal_project,
            'dashboard': self._generate_universal_project,
            'landing': self._generate_universal_project,
            'portfolio': self._generate_universal_project,
            'todo': self._generate_universal_project,
            'chat': self._generate_universal_project,
            'crm': self._generate_universal_project,
            'fitness': self._generate_universal_project,
            'game': self._generate_universal_project
        }
        
    def ensure_projects_dir(self):
        """Создает директорию для проектов если её нет"""
        if not os.path.exists(self.projects_dir):
            os.makedirs(self.projects_dir, exist_ok=True)
            
    def generate_fullstack_project(self, description: str, project_name: str, project_type: str = 'auto') -> FullStackProject:
        """Главный метод генерации full-stack проекта"""
        
        print(f"🚀 Создаю full-stack проект: {project_name}")
        print(f"📝 Описание: {description}")
        print(f"🎯 Тип: {project_type}")
        
        # Определяем тип проекта если auto
        if project_type == 'auto':
            project_type = self._detect_project_type(description)
            
        # Генерируем ID проекта
        project_id = f"fs_{uuid.uuid4().hex[:12]}"
        
        # Выбираем фреймворк на основе типа проекта
        framework = self._select_framework(project_type, description)
        
        print(f"🔧 Фреймворк: {framework}")
        
        # Генерируем проект
        if project_type in self.project_templates:
            project = self.project_templates[project_type](
                project_id, project_name, description, framework
            )
        else:
            # Fallback к универсальному шаблону
            project = self._generate_universal_project(
                project_id, project_name, description, framework, project_type
            )
        
        # Сохраняем проект на диск
        self._save_project_to_disk(project)
        
        print(f"✅ Full-stack проект создан: {project.project_id}")
        return project
        
    def _detect_project_type(self, description: str) -> str:
        """Определяет тип проекта по описанию"""
        description_lower = description.lower()
        
        type_keywords = {
            'ecommerce': ['магазин', 'shop', 'интернет-магазин', 'продажа', 'товары', 'корзина', 'заказ'],
            'blog': ['блог', 'blog', 'статьи', 'новости', 'публикации', 'cms'],
            'dashboard': ['админка', 'dashboard', 'панель', 'аналитика', 'управление'],
            'landing': ['лендинг', 'landing', 'сайт-визитка', 'промо', 'одностраничник'],
            'portfolio': ['портфолио', 'portfolio', 'резюме', 'галерея работ'],
            'todo': ['todo', 'задачи', 'планировщик', 'список дел'],
            'chat': ['чат', 'мессенджер', 'общение', 'сообщения'],
            'crm': ['crm', 'клиенты', 'продажи', 'менеджмент'],
            'fitness': ['фитнес', 'тренировки', 'спорт', 'здоровье'],
            'game': ['игра', 'game', 'развлечение', 'геймплей']
        }
        
        for project_type, keywords in type_keywords.items():
            if any(keyword in description_lower for keyword in keywords):
                return project_type
                
        return 'landing'  # default
        
    def _select_framework(self, project_type: str, description: str) -> str:
        """Выбирает оптимальный фреймворк для проекта"""
        
        # Для разных типов проектов разные фреймворки
        framework_mapping = {
            'ecommerce': 'nextjs',  # Нужен SSR и API routes
            'blog': 'nextjs',       # SEO важен
            'dashboard': 'react',   # SPA подходит
            'landing': 'nextjs',    # SEO критичен
            'portfolio': 'nextjs',  # SEO важен
            'todo': 'react',        # Простое SPA
            'chat': 'nextjs',       # Нужен real-time
            'crm': 'nextjs',        # Комплексная система
            'fitness': 'react',     # Интерактивность
            'game': 'react'         # Интерактивность
        }
        
        return framework_mapping.get(project_type, 'nextjs')
        
    def _generate_ecommerce_project(self, project_id: str, name: str, description: str, framework: str) -> FullStackProject:
        """Генерирует полноценный интернет-магазин"""
        
        # Frontend файлы
        frontend_files = {
            'pages/index.js': self._generate_ecommerce_home_page(name, description),
            'pages/products/[id].js': self._generate_product_page(),
            'pages/cart.js': self._generate_cart_page(),
            'pages/checkout.js': self._generate_checkout_page(),
            'pages/api/products.js': self._generate_products_api(),
            'pages/api/orders.js': self._generate_orders_api(),
            'components/ProductCard.js': self._generate_product_card(),
            'components/Cart.js': self._generate_cart_component(),
            'components/Header.js': self._generate_header_component(),
            'styles/globals.css': self._generate_global_styles(),
            'styles/Home.module.css': self._generate_home_styles(),
            'public/favicon.ico': '# Favicon placeholder',
            'README.md': self._generate_readme(name, description, 'ecommerce'),
            'next.config.js': self._generate_nextjs_config()
        }
        
        # Backend API routes уже включены в Next.js
        backend_files = {}
        
        # Схема базы данных
        database_schema = {
            'products': {
                'id': 'uuid primary key default gen_random_uuid()',
                'name': 'text not null',
                'description': 'text',
                'price': 'decimal(10,2) not null',
                'image_url': 'text',
                'category': 'text',
                'stock': 'integer default 0',
                'created_at': 'timestamp default now()'
            },
            'orders': {
                'id': 'uuid primary key default gen_random_uuid()',
                'user_email': 'text not null',
                'total': 'decimal(10,2) not null',
                'status': 'text default \'pending\'',
                'created_at': 'timestamp default now()'
            },
            'order_items': {
                'id': 'uuid primary key default gen_random_uuid()',
                'order_id': 'uuid references orders(id)',
                'product_id': 'uuid references products(id)',
                'quantity': 'integer not null',
                'price': 'decimal(10,2) not null'
            }
        }
        
        # Environment variables
        env_variables = {
            'NEXT_PUBLIC_SUPABASE_URL': 'your-supabase-url',
            'NEXT_PUBLIC_SUPABASE_ANON_KEY': 'your-supabase-anon-key',
            'SUPABASE_SERVICE_KEY': 'your-supabase-service-key',
            'STRIPE_SECRET_KEY': 'your-stripe-secret-key',
            'NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY': 'your-stripe-publishable-key'
        }
        
        # Package.json
        package_json = {
            'name': name.lower().replace(' ', '-'),
            'version': '0.1.0',
            'private': True,
            'scripts': {
                'dev': 'next dev',
                'build': 'next build',
                'start': 'next start',
                'lint': 'next lint'
            },
            'dependencies': {
                'next': '^14.0.0',
                'react': '^18.0.0',
                'react-dom': '^18.0.0',
                '@supabase/supabase-js': '^2.38.0',
                'stripe': '^14.0.0',
                '@stripe/stripe-js': '^2.0.0'
            },
            'devDependencies': {
                'eslint': '^8.0.0',
                'eslint-config-next': '14.0.0'
            }
        }
        
        # Deployment config
        deployment_config = {
            'platform': 'vercel',
            'build_command': 'npm run build',
            'output_directory': '.next',
            'env_vars_required': list(env_variables.keys())
        }
        
        return FullStackProject(
            project_id=project_id,
            name=name,
            type='ecommerce',
            framework=framework,
            description=description,
            frontend_files=frontend_files,
            backend_files=backend_files,
            database_schema=database_schema,
            env_variables=env_variables,
            package_json=package_json,
            deployment_config=deployment_config,
            created_at=datetime.now().isoformat()
        )
        
    def _generate_universal_project(self, project_id: str, name: str, description: str, framework: str, project_type: str) -> FullStackProject:
        """Генерирует универсальный проект для неопределенных типов"""
        
        frontend_files = {
            'pages/index.js' if framework == 'nextjs' else 'src/App.js': self._generate_universal_home_page(name, description),
            'package.json': json.dumps({
                'name': name.lower().replace(' ', '-'),
                'version': '0.1.0',
                'private': True,
                'scripts': {
                    'dev': 'next dev' if framework == 'nextjs' else 'react-scripts start',
                    'build': 'next build' if framework == 'nextjs' else 'react-scripts build',
                    'start': 'next start' if framework == 'nextjs' else 'serve -s build'
                },
                'dependencies': {
                    'next': '^14.0.0' if framework == 'nextjs' else None,
                    'react': '^18.0.0',
                    'react-dom': '^18.0.0',
                    'react-scripts': '^5.0.1' if framework == 'react' else None
                }
            }, indent=2)
        }
        
        return FullStackProject(
            project_id=project_id,
            name=name,
            type=project_type,
            framework=framework,
            description=description,
            frontend_files=frontend_files,
            backend_files={},
            database_schema={},
            env_variables={},
            package_json={},
            deployment_config={'platform': 'vercel'},
            created_at=datetime.now().isoformat()
        )
        
    def _save_project_to_disk(self, project: FullStackProject):
        """Сохраняет проект на диск в виде zip архива и отдельной папки"""
        
        project_path = os.path.join(self.projects_dir, project.project_id)
        os.makedirs(project_path, exist_ok=True)
        
        # Сохраняем frontend файлы
        for file_path, content in project.frontend_files.items():
            full_path = os.path.join(project_path, file_path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
        # Сохраняем backend файлы
        for file_path, content in project.backend_files.items():
            full_path = os.path.join(project_path, file_path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
        # Сохраняем метаданные проекта
        metadata = {
            'project_id': project.project_id,
            'name': project.name,
            'type': project.type,
            'framework': project.framework,
            'description': project.description,
            'database_schema': project.database_schema,
            'env_variables': project.env_variables,
            'deployment_config': project.deployment_config,
            'created_at': project.created_at
        }
        
        with open(os.path.join(project_path, 'project-metadata.json'), 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
            
        # Создаем zip архив для скачивания
        zip_path = os.path.join(self.projects_dir, f"{project.project_id}.zip")
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(project_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arc_name = os.path.relpath(file_path, project_path)
                    zipf.write(file_path, arc_name)
                    
        print(f"💾 Проект сохранен: {project_path}")
        print(f"📦 Архив создан: {zip_path}")
        
    # Генераторы конкретных файлов
    def _generate_ecommerce_home_page(self, name: str, description: str) -> str:
        return f'''import Head from 'next/head'
import { useState, useEffect } from 'react'
import ProductCard from '../components/ProductCard'
import Header from '../components/Header'

export default function Home() {{
  const [products, setProducts] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {{
    fetchProducts()
  }}, [])

  const fetchProducts = async () => {{
    try {{
      const response = await fetch('/api/products')
      const data = await response.json()
      setProducts(data)
    }} catch (error) {{
      console.error('Error fetching products:', error)
    }} finally {{
      setLoading(false)
    }}
  }}

  return (
    <div>
      <Head>
        <title>{name}</title>
        <meta name="description" content="{description}" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <Header />

      <main style={{{{ padding: '2rem' }}}}>
        <h1 style={{{{ textAlign: 'center', marginBottom: '2rem' }}}}>
          {name}
        </h1>
        
        <p style={{{{ textAlign: 'center', marginBottom: '3rem', fontSize: '1.2rem', color: '#666' }}}}>
          {description}
        </p>

        {{loading ? (
          <div style={{{{ textAlign: 'center' }}}}>Загрузка товаров...</div>
        ) : (
          <div style={{{{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
            gap: '2rem',
            maxWidth: '1200px',
            margin: '0 auto'
          }}}}>
            {{products.map(product => (
              <ProductCard key={{product.id}} product={{product}} />
            ))}}
          </div>
        )}}
      </main>
    </div>
  )
}}'''

    def _generate_product_card(self) -> str:
        return '''import { useState } from 'react'

export default function ProductCard({ product }) {
  const [addingToCart, setAddingToCart] = useState(false)

  const addToCart = async () => {
    setAddingToCart(true)
    try {
      // Логика добавления в корзину
      const cart = JSON.parse(localStorage.getItem('cart') || '[]')
      const existingItem = cart.find(item => item.id === product.id)
      
      if (existingItem) {
        existingItem.quantity += 1
      } else {
        cart.push({...product, quantity: 1})
      }
      
      localStorage.setItem('cart', JSON.stringify(cart))
      alert('Товар добавлен в корзину!')
    } catch (error) {
      console.error('Error adding to cart:', error)
    } finally {
      setAddingToCart(false)
    }
  }

  return (
    <div style={{
      border: '1px solid #ddd',
      borderRadius: '8px',
      padding: '1rem',
      backgroundColor: 'white',
      boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
      transition: 'transform 0.2s',
      cursor: 'pointer'
    }}
    onMouseEnter={e => e.target.style.transform = 'translateY(-2px)'}
    onMouseLeave={e => e.target.style.transform = 'translateY(0)'}
    >
      {product.image_url && (
        <img 
          src={product.image_url} 
          alt={product.name}
          style={{
            width: '100%',
            height: '200px',
            objectFit: 'cover',
            borderRadius: '4px',
            marginBottom: '1rem'
          }}
        />
      )}
      
      <h3 style={{ marginBottom: '0.5rem', color: '#333' }}>{product.name}</h3>
      <p style={{ color: '#666', marginBottom: '1rem', fontSize: '0.9rem' }}>
        {product.description}
      </p>
      
      <div style={{ 
        display: 'flex', 
        justifyContent: 'space-between', 
        alignItems: 'center' 
      }}>
        <span style={{ 
          fontSize: '1.2rem', 
          fontWeight: 'bold', 
          color: '#e74c3c' 
        }}>
          ₽{product.price}
        </span>
        
        <button
          onClick={addToCart}
          disabled={addingToCart}
          style={{
            backgroundColor: '#3498db',
            color: 'white',
            border: 'none',
            padding: '0.5rem 1rem',
            borderRadius: '4px',
            cursor: addingToCart ? 'not-allowed' : 'pointer',
            opacity: addingToCart ? 0.6 : 1
          }}
        >
          {addingToCart ? 'Добавляю...' : 'В корзину'}
        </button>
      </div>
    </div>
  )
}'''

    def _generate_header_component(self) -> str:
        return '''import { useState, useEffect } from 'react'
import Link from 'next/link'

export default function Header() {
  const [cartCount, setCartCount] = useState(0)

  useEffect(() => {
    updateCartCount()
    window.addEventListener('storage', updateCartCount)
    return () => window.removeEventListener('storage', updateCartCount)
  }, [])

  const updateCartCount = () => {
    const cart = JSON.parse(localStorage.getItem('cart') || '[]')
    const count = cart.reduce((total, item) => total + item.quantity, 0)
    setCartCount(count)
  }

  return (
    <header style={{
      backgroundColor: '#2c3e50',
      color: 'white',
      padding: '1rem 2rem',
      boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
    }}>
      <nav style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        maxWidth: '1200px',
        margin: '0 auto'
      }}>
        <Link href="/" style={{ 
          fontSize: '1.5rem', 
          fontWeight: 'bold', 
          textDecoration: 'none', 
          color: 'white' 
        }}>
          🛍️ Магазин
        </Link>
        
        <div style={{ display: 'flex', gap: '2rem', alignItems: 'center' }}>
          <Link href="/" style={{ textDecoration: 'none', color: 'white' }}>
            Главная
          </Link>
          <Link href="/cart" style={{ 
            textDecoration: 'none', 
            color: 'white',
            position: 'relative'
          }}>
            🛒 Корзина
            {cartCount > 0 && (
              <span style={{
                position: 'absolute',
                top: '-8px',
                right: '-8px',
                backgroundColor: '#e74c3c',
                color: 'white',
                borderRadius: '50%',
                width: '20px',
                height: '20px',
                fontSize: '0.7rem',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center'
              }}>
                {cartCount}
              </span>
            )}
          </Link>
        </div>
      </nav>
    </header>
  )
}'''

    def _generate_products_api(self) -> str:
        return '''// pages/api/products.js
import { createClient } from '@supabase/supabase-js'

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL,
  process.env.SUPABASE_SERVICE_KEY
)

export default async function handler(req, res) {
  if (req.method === 'GET') {
    try {
      const { data: products, error } = await supabase
        .from('products')
        .select('*')
        .order('created_at', { ascending: false })

      if (error) throw error

      res.status(200).json(products)
    } catch (error) {
      console.error('Error fetching products:', error)
      res.status(500).json({ error: 'Internal server error' })
    }
  } else if (req.method === 'POST') {
    try {
      const { name, description, price, image_url, category, stock } = req.body

      const { data: product, error } = await supabase
        .from('products')
        .insert([
          { name, description, price, image_url, category, stock }
        ])
        .select()

      if (error) throw error

      res.status(201).json(product[0])
    } catch (error) {
      console.error('Error creating product:', error)
      res.status(500).json({ error: 'Internal server error' })
    }
  } else {
    res.setHeader('Allow', ['GET', 'POST'])
    res.status(405).end(`Method ${req.method} Not Allowed`)
  }
}'''

    def _generate_readme(self, name: str, description: str, project_type: str) -> str:
        return f'''# {name}

{description}

## 🚀 Full-Stack приложение, созданное с помощью Vibecode AI

### Технологии:
- **Frontend**: Next.js + React
- **Backend**: Next.js API Routes
- **База данных**: Supabase (PostgreSQL)
- **Стилизация**: CSS Modules
- **Развертывание**: Vercel

### Возможности:
- ✅ Адаптивный дизайн
- ✅ Real-time база данных
- ✅ API endpoints
- ✅ Готово к продакшену
- ✅ SEO оптимизация

## Установка

```bash
# Клонируйте проект
git clone <repo-url>

# Установите зависимости
npm install

# Настройте environment variables
cp .env.example .env.local

# Запустите в режиме разработки
npm run dev
```

## Environment Variables

Создайте файл `.env.local` и добавьте:

```env
NEXT_PUBLIC_SUPABASE_URL=your-supabase-url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-supabase-anon-key
SUPABASE_SERVICE_KEY=your-supabase-service-key
```

## Развертывание

Проект готов к развертыванию на Vercel:

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new)

## 📱 Возможности проекта

- Полнофункциональный {project_type}
- Интуитивный пользовательский интерфейс
- Мобильная адаптация
- Быстрая загрузка страниц
- SEO дружелюбность

---

💡 **Создано с помощью [Vibecode AI](https://vibecode.ai)** - платформы для создания full-stack приложений через естественный язык.
'''

    def _generate_global_styles(self) -> str:
        return '''html,
body {
  padding: 0;
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Oxygen,
    Ubuntu, Cantarell, Fira Sans, Droid Sans, Helvetica Neue, sans-serif;
  background-color: #f8f9fa;
}

a {
  color: inherit;
  text-decoration: none;
}

* {
  box-sizing: border-box;
}

button {
  font-family: inherit;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

.loading {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 200px;
}

.error {
  color: #e74c3c;
  text-align: center;
  padding: 2rem;
  background: #fdf2f2;
  border: 1px solid #fecaca;
  border-radius: 8px;
  margin: 1rem 0;
}

.success {
  color: #27ae60;
  text-align: center;
  padding: 2rem;
  background: #f0fff4;
  border: 1px solid #9ae6b4;
  border-radius: 8px;
  margin: 1rem 0;
}'''

    def _generate_nextjs_config(self) -> str:
        return '''/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  images: {
    domains: [],
  },
  env: {
    CUSTOM_KEY: process.env.CUSTOM_KEY,
  },
}

module.exports = nextConfig'''

    def _generate_universal_home_page(self, name: str, description: str) -> str:
        return f'''import Head from 'next/head'

export default function Home() {{
  return (
    <div>
      <Head>
        <title>{name}</title>
        <meta name="description" content="{description}" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main style={{{{
        minHeight: '100vh',
        padding: '4rem 2rem',
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        color: 'white',
        textAlign: 'center'
      }}}}>
        <h1 style={{{{
          fontSize: '3rem',
          marginBottom: '2rem',
          textShadow: '0 2px 4px rgba(0,0,0,0.3)'
        }}}}>
          🚀 {name}
        </h1>
        
        <p style={{{{
          fontSize: '1.3rem',
          marginBottom: '3rem',
          maxWidth: '800px',
          margin: '0 auto 3rem auto',
          lineHeight: '1.6',
          opacity: '0.9'
        }}}}>
          {description}
        </p>

        <div style={{{{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
          gap: '2rem',
          maxWidth: '1000px',
          margin: '0 auto'
        }}}}>
          <div style={{{{
            background: 'rgba(255,255,255,0.1)',
            padding: '2rem',
            borderRadius: '12px',
            backdropFilter: 'blur(10px)'
          }}}}>
            <h3 style={{{{ marginBottom: '1rem' }}}}>⚡ Быстро</h3>
            <p>Мгновенная загрузка и отзывчивый интерфейс</p>
          </div>
          
          <div style={{{{
            background: 'rgba(255,255,255,0.1)',
            padding: '2rem',
            borderRadius: '12px',
            backdropFilter: 'blur(10px)'
          }}}}>
            <h3 style={{{{ marginBottom: '1rem' }}}}>🎨 Красиво</h3>
            <p>Современный дизайн и адаптивная верстка</p>
          </div>
          
          <div style={{{{
            background: 'rgba(255,255,255,0.1)',
            padding: '2rem',
            borderRadius: '12px',
            backdropFilter: 'blur(10px)'
          }}}}>
            <h3 style={{{{ marginBottom: '1rem' }}}}>🔧 Функционально</h3>
            <p>Полный набор возможностей из коробки</p>
          </div>
        </div>

        <button style={{{{
          marginTop: '3rem',
          padding: '1rem 2rem',
          fontSize: '1.1rem',
          backgroundColor: '#ff6b6b',
          color: 'white',
          border: 'none',
          borderRadius: '50px',
          cursor: 'pointer',
          transition: 'transform 0.2s'
        }}}}
        onMouseEnter={{e => e.target.style.transform = 'translateY(-2px)'}}
        onMouseLeave={{e => e.target.style.transform = 'translateY(0)'}}
        onClick={{() => alert('Добро пожаловать в ваше новое приложение!')}}
        >
          🚀 Начать использование
        </button>

        <footer style={{{{ marginTop: '4rem', opacity: '0.7' }}}}>
          <p>💡 Создано с помощью Vibecode AI</p>
        </footer>
      </main>
    </div>
  )
}}'''

# Методы для других типов проектов будут добавлены аналогично...

def test_fullstack_generator():
    """Тестирование генератора full-stack проектов"""
    generator = FullStackGenerator()
    
    # Тест генерации интернет-магазина
    project = generator.generate_fullstack_project(
        description="Интернет-магазин одежды с корзиной, каталогом товаров и системой оплаты",
        project_name="Модный Стиль",
        project_type="ecommerce"
    )
    
    print(f"✅ Создан проект: {project.project_id}")
    print(f"📁 Файлов: {len(project.frontend_files)}")
    print(f"🗄️ Таблиц в БД: {len(project.database_schema)}")

if __name__ == "__main__":
    test_fullstack_generator()