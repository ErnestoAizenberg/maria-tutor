# Models Summary

## Core Models

### Teacher
- **Purpose**: Teacher/tutor profiles with social links and ratings
- **Key Fields**: name, status, description, avatar, email, social media handles
- **Features**: 
  - Automatic slug generation
  - Social links generation
  - Aggregate rating calculation from reviews
  - Multi-language support (ru/en)
  - JSON fields for education/scientific work

### Page  
- **Purpose**: Dynamic pages with YAML configuration
- **Key Fields**: name, slug, config_yaml, SEO/OpenGraph fields
- **Features**:
  - YAML-based section configuration
  - Navigation/footer display controls
  - Built-in SEO optimization
  - View tracking

### Tariff
- **Purpose**: Pricing plans for teaching services
- **Key Fields**: format_type, program_name, price, price_unit
- **Features**:
  - Group format flagging
  - Teacher-specific filtering
  - Automatic slug generation

## Content Models

### Article
- **Purpose**: Blog articles with tagging
- **Key Fields**: title, content, tags, image_preview
- **Features**:
  - Tag system
  - Auto-generated abstracts
  - Draft/published status

### Publication  
- **Purpose**: Academic publications
- **Key Fields**: title, authors, journal, doi, publication_date
- **Features**:
  - Featured publication highlighting
  - DOI support
  - Automatic URL generation

## Review & Feedback

### Review
- **Purpose**: Student reviews with source tracking
- **Key Fields**: author_name, content, rating, source (profi.ru, google, etc.)
- **Features**:
  - Multiple source types
  - Achievement/results tracking
  - Manual ordering

### Application & ConnectMessage
- **Purpose**: Contact forms and applications
- **Key Fields**: name, email, goal/message, subject
- **Features**: Processing status tracking

## Specialized Components

### LessonCard & LessonFeature
- **Purpose**: Pricing card displays with feature lists
- **Key Fields**: title, price, icon_class, features
- **Features**: Featured flag for promotions

### TutorConsultationRequest  
- **Purpose**: Consultation requests from other tutors
- **Key Fields**: name, email, question, experience_years
- **Features**: Internal notes for admin processing

## Key Relationships
- Teacher → Reviews (One-to-Many)
- Teacher → Pages (One-to-Many) 
- Teacher → Tariffs (One-to-Many)
- Article → Tags (Many-to-Many)
- LessonCard → Features (One-to-Many)

## Common Patterns
- Automatic slug generation
- Created/updated timestamps
- Published/active status flags
- Multi-language support
- SEO optimization fields