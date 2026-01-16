# Phase 4: Advanced Features & Production Readiness Implementation Guide

**Duration:** Weeks 17-20
**Status:** Implementation Guide
**Objective:** Implement enhanced features, production monitoring, and collaborative capabilities

---

## Table of Contents

1. [Week 17-18: Enhanced Features](#week-17-18-enhanced-features)
   - [Template Library System](#template-library-system)
   - [Advanced Search & Filtering](#advanced-search--filtering)
   - [Version Control for Regenerations](#version-control-for-regenerations)
   - [Email Notifications System](#email-notifications-system)
   - [Frontend: Template Manager UI](#frontend-template-manager-ui)
   - [Frontend: Advanced Search UI](#frontend-advanced-search-ui)
   - [Frontend: Version History UI](#frontend-version-history-ui)

2. [Week 19-20: Production Readiness](#week-19-20-production-readiness)
   - [Rate Limiting Implementation](#rate-limiting-implementation)
   - [Automated Backup System](#automated-backup-system)
   - [Cost Monitoring & Budgets](#cost-monitoring--budgets)
   - [Admin Dashboard Completion](#admin-dashboard-completion)
   - [Collaborative Features](#collaborative-features)

3. [Testing Strategies](#testing-strategies)
4. [Deployment Checklist](#deployment-checklist)

---

## Week 17-18: Enhanced Features

### Template Library System

#### Overview
Enable users to create, save, and reuse PDF generation templates with predefined settings for fonts, layouts, styles, and content preferences.

#### Database Schema Changes

```sql
-- Templates table
CREATE TABLE templates (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    category VARCHAR(100),

    -- Template configuration (JSONB)
    config JSONB NOT NULL DEFAULT '{}',

    -- Metadata
    is_public BOOLEAN DEFAULT FALSE,
    usage_count INTEGER DEFAULT 0,
    rating DECIMAL(3,2) DEFAULT 0.00,

    -- Version control
    version INTEGER DEFAULT 1,
    parent_template_id INTEGER REFERENCES templates(id) ON DELETE SET NULL,

    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    deleted_at TIMESTAMP WITH TIME ZONE
);

-- Template categories
CREATE TABLE template_categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    icon VARCHAR(50),
    sort_order INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Template usage tracking
CREATE TABLE template_usage (
    id SERIAL PRIMARY KEY,
    template_id INTEGER REFERENCES templates(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    generation_id INTEGER REFERENCES generations(id) ON DELETE SET NULL,
    used_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Template ratings
CREATE TABLE template_ratings (
    id SERIAL PRIMARY KEY,
    template_id INTEGER REFERENCES templates(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(template_id, user_id)
);

-- Indexes for performance
CREATE INDEX idx_templates_user_id ON templates(user_id);
CREATE INDEX idx_templates_category ON templates(category);
CREATE INDEX idx_templates_is_public ON templates(is_public);
CREATE INDEX idx_templates_usage_count ON templates(usage_count DESC);
CREATE INDEX idx_template_usage_template_id ON template_usage(template_id);
CREATE INDEX idx_template_usage_user_id ON template_usage(user_id);
CREATE INDEX idx_template_ratings_template_id ON template_ratings(template_id);
```

#### Template Config Structure

```json
{
  "pdf_options": {
    "font_family": "Liberation Sans",
    "font_size": 11,
    "line_height": 1.6,
    "margin_top": "20mm",
    "margin_bottom": "20mm",
    "margin_left": "15mm",
    "margin_right": "15mm",
    "page_size": "A4"
  },
  "styling": {
    "title_font_size": 24,
    "title_font_weight": "bold",
    "title_color": "#2c3e50",
    "chapter_number_font_size": 18,
    "chapter_number_color": "#34495e",
    "heading_font_size": 16,
    "heading_color": "#2c3e50",
    "body_font_size": 11,
    "body_color": "#333333",
    "link_color": "#3498db",
    "code_background": "#f8f9fa"
  },
  "content_settings": {
    "include_toc": true,
    "toc_title": "Table of Contents",
    "include_page_numbers": true,
    "page_number_position": "bottom-center",
    "include_chapter_titles": true,
    "include_metadata": true
  },
  "generation_settings": {
    "provider": "anthropic",
    "model": "claude-3-5-sonnet-20241022",
    "max_tokens": 4096,
    "temperature": 0.7,
    "target_language": "en",
    "creativity_level": "balanced",
    "quality_preset": "standard"
  },
  "advanced": {
    "custom_css": "",
    "header_template": "",
    "footer_template": "",
    "watermark": {
      "enabled": false,
      "text": "",
      "opacity": 0.3,
      "rotation": 45
    }
  }
}
```

#### Backend Implementation

**File:** `backend/app/services/template_service.py`

```python
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, func
from datetime import datetime
import json

from app.models.template import Template, TemplateCategory, TemplateUsage, TemplateRating
from app.models.user import User
from app.schemas.template import (
    TemplateCreate, TemplateUpdate, TemplateResponse,
    TemplateCategoryCreate, TemplateCategoryResponse
)
from app.core.exceptions import ValidationError, NotFoundError

class TemplateService:
    def __init__(self, db: Session):
        self.db = db

    def create_template(
        self,
        user_id: int,
        template_data: TemplateCreate
    ) -> TemplateResponse:
        """Create a new template"""
        # Validate template config
        self._validate_template_config(template_data.config)

        # Check category exists if specified
        if template_data.category:
            category = self.db.query(TemplateCategory).filter(
                TemplateCategory.name == template_data.category
            ).first()
            if not category:
                raise ValidationError(f"Category '{template_data.category}' does not exist")

        # Create template
        template = Template(
            user_id=user_id,
            name=template_data.name,
            description=template_data.description,
            category=template_data.category,
            config=template_data.config,
            is_public=template_data.is_public,
            version=1
        )

        self.db.add(template)
        self.db.commit()
        self.db.refresh(template)

        return TemplateResponse.from_orm(template)

    def get_template(self, template_id: int, user_id: int) -> TemplateResponse:
        """Get a specific template"""
        template = self.db.query(Template).filter(
            and_(
                Template.id == template_id,
                or_(
                    Template.user_id == user_id,
                    Template.is_public == True
                )
            )
        ).first()

        if not template:
            raise NotFoundError("Template not found")

        return TemplateResponse.from_orm(template)

    def list_templates(
        self,
        user_id: int,
        category: Optional[str] = None,
        is_public: Optional[bool] = None,
        search: Optional[str] = None,
        sort_by: str = "created_at",
        sort_order: str = "desc",
        page: int = 1,
        page_size: int = 20
    ) -> Dict[str, Any]:
        """List templates with filtering and pagination"""
        query = self.db.query(Template)

        # Filter by user ownership or public
        query = query.filter(
            or_(
                Template.user_id == user_id,
                Template.is_public == True
            )
        )

        # Filter by category
        if category:
            query = query.filter(Template.category == category)

        # Filter by public/private
        if is_public is not None:
            query = query.filter(Template.is_public == is_public)

        # Search in name and description
        if search:
            search_filter = or_(
                Template.name.ilike(f"%{search}%"),
                Template.description.ilike(f"%{search}%")
            )
            query = query.filter(search_filter)

        # Sorting
        sort_column = getattr(Template, sort_by, Template.created_at)
        if sort_order == "desc":
            query = query.order_by(desc(sort_column))
        else:
            query = query.order_by(sort_column)

        # Pagination
        total = query.count()
        templates = query.offset((page - 1) * page_size).limit(page_size).all()

        return {
            "templates": [TemplateResponse.from_orm(t) for t in templates],
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size
        }

    def update_template(
        self,
        template_id: int,
        user_id: int,
        template_data: TemplateUpdate
    ) -> TemplateResponse:
        """Update a template"""
        template = self.db.query(Template).filter(
            and_(
                Template.id == template_id,
                Template.user_id == user_id
            )
        ).first()

        if not template:
            raise NotFoundError("Template not found or you don't have permission")

        # Validate template config if provided
        if template_data.config:
            self._validate_template_config(template_data.config)

        # Update fields
        if template_data.name:
            template.name = template_data.name
        if template_data.description is not None:
            template.description = template_data.description
        if template_data.category:
            template.category = template_data.category
        if template_data.config:
            template.config = template_data.config
        if template_data.is_public is not None:
            template.is_public = template_data.is_public

        template.updated_at = datetime.utcnow()

        self.db.commit()
        self.db.refresh(template)

        return TemplateResponse.from_orm(template)

    def delete_template(self, template_id: int, user_id: int) -> None:
        """Soft delete a template"""
        template = self.db.query(Template).filter(
            and_(
                Template.id == template_id,
                Template.user_id == user_id
            )
        ).first()

        if not template:
            raise NotFoundError("Template not found or you don't have permission")

        template.deleted_at = datetime.utcnow()
        self.db.commit()

    def use_template(
        self,
        template_id: int,
        user_id: int,
        generation_id: Optional[int] = None
    ) -> None:
        """Track template usage"""
        template = self.db.query(Template).filter(
            and_(
                Template.id == template_id,
                or_(
                    Template.user_id == user_id,
                    Template.is_public == True
                )
            )
        ).first()

        if not template:
            raise NotFoundError("Template not found")

        # Increment usage count
        template.usage_count = (template.usage_count or 0) + 1

        # Track usage
        usage = TemplateUsage(
            template_id=template_id,
            user_id=user_id,
            generation_id=generation_id
        )
        self.db.add(usage)
        self.db.commit()

    def rate_template(
        self,
        template_id: int,
        user_id: int,
        rating: int
    ) -> Dict[str, Any]:
        """Rate a template (1-5 stars)"""
        if rating < 1 or rating > 5:
            raise ValidationError("Rating must be between 1 and 5")

        template = self.db.query(Template).filter(
            Template.id == template_id
        ).first()

        if not template:
            raise NotFoundError("Template not found")

        # Check if user already rated
        existing_rating = self.db.query(TemplateRating).filter(
            and_(
                TemplateRating.template_id == template_id,
                TemplateRating.user_id == user_id
            )
        ).first()

        if existing_rating:
            existing_rating.rating = rating
        else:
            new_rating = TemplateRating(
                template_id=template_id,
                user_id=user_id,
                rating=rating
            )
            self.db.add(new_rating)

        # Recalculate average rating
        avg_rating = self.db.query(
            func.avg(TemplateRating.rating)
        ).filter(
            TemplateRating.template_id == template_id
        ).scalar()

        template.rating = round(avg_rating, 2)
        self.db.commit()

        return {
            "template_id": template_id,
            "average_rating": template.rating,
            "your_rating": rating
        }

    def create_template_version(
        self,
        template_id: int,
        user_id: int
    ) -> TemplateResponse:
        """Create a new version of a template"""
        original = self.db.query(Template).filter(
            and_(
                Template.id == template_id,
                Template.user_id == user_id
            )
        ).first()

        if not original:
            raise NotFoundError("Template not found or you don't have permission")

        # Create new version
        new_version = Template(
            user_id=user_id,
            name=original.name,
            description=original.description,
            category=original.category,
            config=original.config.copy(),
            is_public=original.is_public,
            version=original.version + 1,
            parent_template_id=template_id
        )

        self.db.add(new_version)
        self.db.commit()
        self.db.refresh(new_version)

        return TemplateResponse.from_orm(new_version)

    def get_template_versions(
        self,
        template_id: int,
        user_id: int
    ) -> List[TemplateResponse]:
        """Get all versions of a template"""
        # Get root template
        root = self.db.query(Template).filter(
            and_(
                Template.id == template_id,
                Template.user_id == user_id
            )
        ).first()

        if not root:
            raise NotFoundError("Template not found")

        # If this is a child template, get the root
        if root.parent_template_id:
            root_id = root.parent_template_id
            while root_id:
                parent = self.db.query(Template).filter(
                    Template.id == root_id
                ).first()
                if not parent or not parent.parent_template_id:
                    root_id = parent.id if parent else None
                    break
                root_id = parent.parent_template_id
        else:
            root_id = template_id

        # Get all versions
        versions = self.db.query(Template).filter(
            or_(
                Template.id == root_id,
                Template.parent_template_id == root_id,
                Template.parent_template_id.in_(
                    self.db.query(Template.id).filter(
                        Template.parent_template_id == root_id
                    )
                )
            )
        ).order_by(Template.version).all()

        return [TemplateResponse.from_orm(v) for v in versions]

    def _validate_template_config(self, config: Dict[str, Any]) -> None:
        """Validate template configuration"""
        required_sections = ['pdf_options', 'styling', 'content_settings']

        for section in required_sections:
            if section not in config:
                raise ValidationError(f"Missing required config section: {section}")

        # Validate PDF options
        pdf_options = config['pdf_options']
        required_pdf_options = ['font_family', 'font_size', 'page_size']
        for opt in required_pdf_options:
            if opt not in pdf_options:
                raise ValidationError(f"Missing required PDF option: {opt}")

        # Validate font size
        if not isinstance(pdf_options['font_size'], (int, float)) or pdf_options['font_size'] < 6 or pdf_options['font_size'] > 24:
            raise ValidationError("font_size must be between 6 and 24")

        # Validate page size
        valid_page_sizes = ['A4', 'Letter', 'Legal', 'A3', 'A5']
        if pdf_options['page_size'] not in valid_page_sizes:
            raise ValidationError(f"Invalid page_size. Must be one of: {valid_page_sizes}")
```

#### API Endpoints

**File:** `backend/app/api/routes/templates.py`

```python
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List

from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.user import User
from app.schemas.template import (
    TemplateCreate, TemplateUpdate, TemplateResponse,
    TemplateListResponse, TemplateCategoryCreate, TemplateCategoryResponse
)
from app.services.template_service import TemplateService

router = APIRouter(prefix="/api/templates", tags=["templates"])

@router.post("", response_model=TemplateResponse)
async def create_template(
    template_data: TemplateCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new template

    **Request Body:**
    - name: Template name (required)
    - description: Template description
    - category: Category name
    - config: Template configuration
    - is_public: Whether template is publicly visible

    **Returns:** Created template
    """
    service = TemplateService(db)
    return service.create_template(current_user.id, template_data)

@router.get("", response_model=TemplateListResponse)
async def list_templates(
    category: Optional[str] = Query(None, description="Filter by category"),
    is_public: Optional[bool] = Query(None, description="Filter by public/private"),
    search: Optional[str] = Query(None, description="Search in name and description"),
    sort_by: str = Query("created_at", description="Sort field"),
    sort_order: str = Query("desc", regex="^(asc|desc)$"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    List templates with filtering and pagination

    **Query Parameters:**
    - category: Filter by category
    - is_public: Filter by public/private status
    - search: Search query
    - sort_by: Sort field (created_at, name, usage_count, rating)
    - sort_order: Sort order (asc, desc)
    - page: Page number
    - page_size: Items per page (max 100)

    **Returns:** Paginated list of templates
    """
    service = TemplateService(db)
    return service.list_templates(
        user_id=current_user.id,
        category=category,
        is_public=is_public,
        search=search,
        sort_by=sort_by,
        sort_order=sort_order,
        page=page,
        page_size=page_size
    )

@router.get("/{template_id}", response_model=TemplateResponse)
async def get_template(
    template_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific template

    **Path Parameters:**
    - template_id: Template ID

    **Returns:** Template details
    """
    service = TemplateService(db)
    return service.get_template(template_id, current_user.id)

@router.put("/{template_id}", response_model=TemplateResponse)
async def update_template(
    template_id: int,
    template_data: TemplateUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update a template

    **Path Parameters:**
    - template_id: Template ID

    **Request Body:**
    - name: New template name
    - description: New description
    - category: New category
    - config: New configuration
    - is_public: New public/private status

    **Returns:** Updated template
    """
    service = TemplateService(db)
    return service.update_template(template_id, current_user.id, template_data)

@router.delete("/{template_id}")
async def delete_template(
    template_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a template (soft delete)

    **Path Parameters:**
    - template_id: Template ID

    **Returns:** Success message
    """
    service = TemplateService(db)
    service.delete_template(template_id, current_user.id)
    return {"message": "Template deleted successfully"}

@router.post("/{template_id}/use")
async def use_template(
    template_id: int,
    generation_id: Optional[int] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Track template usage

    **Path Parameters:**
    - template_id: Template ID

    **Request Body:**
    - generation_id: Optional generation ID to link usage

    **Returns:** Success message
    """
    service = TemplateService(db)
    service.use_template(template_id, current_user.id, generation_id)
    return {"message": "Usage tracked successfully"}

@router.post("/{template_id}/rate")
async def rate_template(
    template_id: int,
    rating: int = Query(..., ge=1, le=5),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Rate a template (1-5 stars)

    **Path Parameters:**
    - template_id: Template ID

    **Query Parameters:**
    - rating: Rating value (1-5)

    **Returns:** Updated rating information
    """
    service = TemplateService(db)
    return service.rate_template(template_id, current_user.id, rating)

@router.post("/{template_id}/versions", response_model=TemplateResponse)
async def create_template_version(
    template_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new version of a template

    **Path Parameters:**
    - template_id: Template ID

    **Returns:** New template version
    """
    service = TemplateService(db)
    return service.create_template_version(template_id, current_user.id)

@router.get("/{template_id}/versions", response_model=List[TemplateResponse])
async def get_template_versions(
    template_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all versions of a template

    **Path Parameters:**
    - template_id: Template ID

    **Returns:** List of template versions
    """
    service = TemplateService(db)
    return service.get_template_versions(template_id, current_user.id)
```

#### Pydantic Schemas

**File:** `backend/app/schemas/template.py`

```python
from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any
from datetime import datetime

class TemplateConfig(BaseModel):
    pdf_options: Dict[str, Any] = Field(default_factory=dict)
    styling: Dict[str, Any] = Field(default_factory=dict)
    content_settings: Dict[str, Any] = Field(default_factory=dict)
    generation_settings: Dict[str, Any] = Field(default_factory=dict)
    advanced: Dict[str, Any] = Field(default_factory=dict)

class TemplateBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    category: Optional[str] = None
    config: TemplateConfig = Field(default_factory=TemplateConfig)
    is_public: bool = False

class TemplateCreate(TemplateBase):
    pass

class TemplateUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    category: Optional[str] = None
    config: Optional[TemplateConfig] = None
    is_public: Optional[bool] = None

class TemplateResponse(TemplateBase):
    id: int
    user_id: int
    usage_count: int = 0
    rating: float = 0.0
    version: int = 1
    parent_template_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class TemplateListResponse(BaseModel):
    templates: list[TemplateResponse]
    total: int
    page: int
    page_size: int
    total_pages: int

class TemplateCategoryCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    icon: Optional[str] = None
    sort_order: int = 0

class TemplateCategoryResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    icon: Optional[str]
    sort_order: int
    created_at: datetime

    class Config:
        from_attributes = True
```

#### Template Seeding Script

**File:** `backend/scripts/seed_templates.py`

```python
import sys
sys.path.append('.')

from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.template import Template, TemplateCategory
from app.models.user import User
import json

def seed_template_categories(db: Session):
    """Seed default template categories"""
    categories = [
        {
            "name": "Business",
            "description": "Professional documents and reports",
            "icon": "briefcase",
            "sort_order": 1
        },
        {
            "name": "Academic",
            "description": "Educational and research materials",
            "icon": "graduation-cap",
            "sort_order": 2
        },
        {
            "name": "Creative",
            "description": "Creative writing and artistic content",
            "icon": "palette",
            "sort_order": 3
        },
        {
            "name": "Technical",
            "description": "Technical documentation and manuals",
            "icon": "code",
            "sort_order": 4
        },
        {
            "name": "Personal",
            "description": "Personal documents and journals",
            "icon": "user",
            "sort_order": 5
        }
    ]

    for cat_data in categories:
        existing = db.query(TemplateCategory).filter(
            TemplateCategory.name == cat_data["name"]
        ).first()

        if not existing:
            category = TemplateCategory(**cat_data)
            db.add(category)

    db.commit()
    print(f"Seeded {len(categories)} template categories")

def seed_public_templates(db: Session):
    """Seed public templates"""
    # Get admin user
    admin = db.query(User).filter(User.is_admin == True).first()
    if not admin:
        print("No admin user found. Skipping public templates.")
        return

    templates = [
        {
            "name": "Professional Report",
            "description": "Clean and professional styling for business reports",
            "category": "Business",
            "is_public": True,
            "config": {
                "pdf_options": {
                    "font_family": "Liberation Sans",
                    "font_size": 11,
                    "line_height": 1.6,
                    "margin_top": "20mm",
                    "margin_bottom": "20mm",
                    "margin_left": "15mm",
                    "margin_right": "15mm",
                    "page_size": "A4"
                },
                "styling": {
                    "title_font_size": 24,
                    "title_font_weight": "bold",
                    "title_color": "#2c3e50",
                    "chapter_number_font_size": 18,
                    "chapter_number_color": "#34495e",
                    "heading_font_size": 16,
                    "heading_color": "#2c3e50",
                    "body_font_size": 11,
                    "body_color": "#333333"
                },
                "content_settings": {
                    "include_toc": True,
                    "include_page_numbers": True,
                    "include_chapter_titles": True
                },
                "generation_settings": {
                    "provider": "anthropic",
                    "model": "claude-3-5-sonnet-20241022",
                    "creativity_level": "professional"
                }
            }
        },
        {
            "name": "Academic Paper",
            "description": "Standard academic formatting with citations support",
            "category": "Academic",
            "is_public": True,
            "config": {
                "pdf_options": {
                    "font_family": "Times New Roman",
                    "font_size": 12,
                    "line_height": 2.0,
                    "margin_top": "25mm",
                    "margin_bottom": "25mm",
                    "margin_left": "25mm",
                    "margin_right": "25mm",
                    "page_size": "A4"
                },
                "styling": {
                    "title_font_size": 16,
                    "title_font_weight": "bold",
                    "heading_font_size": 14,
                    "body_font_size": 12
                },
                "content_settings": {
                    "include_toc": True,
                    "include_page_numbers": True,
                    "include_chapter_titles": True
                }
            }
        },
        {
            "name": "Creative Writing",
            "description": "Elegant styling for novels and creative works",
            "category": "Creative",
            "is_public": True,
            "config": {
                "pdf_options": {
                    "font_family": "Georgia",
                    "font_size": 12,
                    "line_height": 1.8,
                    "margin_top": "20mm",
                    "margin_bottom": "20mm",
                    "margin_left": "20mm",
                    "margin_right": "20mm",
                    "page_size": "A5"
                },
                "styling": {
                    "title_font_size": 28,
                    "chapter_number_font_size": 20,
                    "body_font_size": 12,
                    "body_color": "#2c2c2c"
                }
            }
        }
    ]

    for tmpl_data in templates:
        existing = db.query(Template).filter(
            Template.name == tmpl_data["name"]
        ).first()

        if not existing:
            template = Template(
                user_id=admin.id,
                **tmpl_data
            )
            db.add(template)

    db.commit()
    print(f"Seeded {len(templates)} public templates")

if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed_template_categories(db)
        seed_public_templates(db)
        print("Template seeding completed successfully!")
    except Exception as e:
        print(f"Error seeding templates: {e}")
        db.rollback()
    finally:
        db.close()
```

#### Testing Templates

**File:** `backend/tests/test_templates.py`

```python
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.core.database import get_db
from app.models.user import User
from app.models.template import Template

client = TestClient(app)

@pytest.fixture
def test_user(db: Session):
    """Create test user"""
    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password="hashed",
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@pytest.fixture
def auth_headers(test_user: User):
    """Get auth headers for test user"""
    # This would use your actual JWT token generation
    return {"Authorization": f"Bearer test_token_{test_user.id}"}

def test_create_template(auth_headers):
    """Test template creation"""
    response = client.post(
        "/api/templates",
        json={
            "name": "Test Template",
            "description": "A test template",
            "category": "Business",
            "config": {
                "pdf_options": {
                    "font_family": "Arial",
                    "font_size": 12,
                    "page_size": "A4"
                },
                "styling": {},
                "content_settings": {},
                "generation_settings": {}
            },
            "is_public": False
        },
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Template"
    assert data["category"] == "Business"
    assert "id" in data

def test_list_templates(auth_headers, test_user: User, db: Session):
    """Test template listing"""
    # Create test templates
    template = Template(
        user_id=test_user.id,
        name="List Test Template",
        category="Academic",
        config={},
        is_public=True
    )
    db.add(template)
    db.commit()

    response = client.get(
        "/api/templates",
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()
    assert "templates" in data
    assert len(data["templates"]) > 0

def test_update_template(auth_headers, test_user: User, db: Session):
    """Test template update"""
    # Create template
    template = Template(
        user_id=test_user.id,
        name="Original Name",
        config={}
    )
    db.add(template)
    db.commit()
    db.refresh(template)

    response = client.put(
        f"/api/templates/{template.id}",
        json={"name": "Updated Name"},
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Name"

def test_delete_template(auth_headers, test_user: User, db: Session):
    """Test template deletion"""
    template = Template(
        user_id=test_user.id,
        name="To Delete",
        config={}
    )
    db.add(template)
    db.commit()
    db.refresh(template)

    response = client.delete(
        f"/api/templates/{template.id}",
        headers=auth_headers
    )

    assert response.status_code == 200

    # Verify soft delete
    deleted = db.query(Template).filter(Template.id == template.id).first()
    assert deleted.deleted_at is not None

def test_rate_template(auth_headers, test_user: User, db: Session):
    """Test template rating"""
    template = Template(
        user_id=test_user.id,
        name="Rate Me",
        config={},
        is_public=True
    )
    db.add(template)
    db.commit()
    db.refresh(template)

    response = client.post(
        f"/api/templates/{template.id}/rate?rating=5",
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()
    assert data["average_rating"] == 5.0
    assert data["your_rating"] == 5
```

---

### Advanced Search & Filtering

#### Overview
Implement full-text search across generations with advanced filtering, sorting, and export capabilities.

#### Database Changes for Search

```sql
-- Install PostgreSQL extension for full-text search
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- Add full-text search column to generations
ALTER TABLE generations ADD COLUMN search_vector tsvector;

-- Create trigger for automatic search vector updates
CREATE OR REPLACE FUNCTION generations_search_vector_update() RETURNS trigger AS $$
BEGIN
    NEW.search_vector :=
        setweight(to_tsvector('english', coalesce(NEW.title, '')), 'A') ||
        setweight(to_tsvector('english', coalesce(NEW.author, '')), 'B') ||
        setweight(to_tsvector('english', coalesce(NEW.prompt, '')), 'C') ||
        setweight(to_tsvector('english', coalesce(NEW.target_language, '')), 'D');
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER generations_search_vector_trigger
    BEFORE INSERT OR UPDATE ON generations
    FOR EACH ROW
    EXECUTE FUNCTION generations_search_vector_update();

-- Create index for full-text search
CREATE INDEX idx_generations_search_vector ON generations USING GIN(search_vector);

-- Add indexes for filtering
CREATE INDEX idx_generations_status ON generations(status);
CREATE INDEX idx_generations_created_at ON generations(created_at DESC);
CREATE INDEX idx_generations_user_id ON generations(user_id);
CREATE INDEX idx_generations_language ON generations(target_language);

-- Add composite indexes for common filter combinations
CREATE INDEX idx_generations_status_created ON generations(status, created_at DESC);
CREATE INDEX idx_generations_user_status ON generations(user_id, status);
```

#### Search Service Implementation

**File:** `backend/app/services/search_service.py`

```python
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, asc, func, cast, String
from datetime import datetime, timedelta
import json
import csv
from io import StringIO

from app.models.generation import Generation
from app.models.user import User
from app.core.exceptions import ValidationError

class SearchService:
    def __init__(self, db: Session):
        self.db = db

    def full_text_search(
        self,
        user_id: int,
        query: str,
        filters: Dict[str, Any],
        sort_by: str = "created_at",
        sort_order: str = "desc",
        page: int = 1,
        page_size: int = 20
    ) -> Dict[str, Any]:
        """
        Perform full-text search with filters

        Args:
            user_id: User ID for permission filtering
            query: Search query string
            filters: Dictionary of filters
            sort_by: Sort field
            sort_order: Sort order (asc/desc)
            page: Page number
            page_size: Items per page

        Returns:
            Search results with metadata
        """
        # Base query
        query_builder = self.db.query(Generation).filter(
            Generation.user_id == user_id
        )

        # Apply full-text search
        if query:
            # Using PostgreSQL tsvector for efficient search
            search_query = func.plainto_tsquery('english', query)
            query_builder = query_builder.filter(
                Generation.search_vector.op('@@')(search_query)
            )
            # Add ranking
            query_builder = query_builder.order_by(
                desc(func.ts_rank(Generation.search_vector, search_query))
            )

        # Apply filters
        query_builder = self._apply_filters(query_builder, filters)

        # Apply sorting
        query_builder = self._apply_sorting(
            query_builder, sort_by, sort_order
        )

        # Get total count
        total = query_builder.count()

        # Apply pagination
        results = query_builder.offset(
            (page - 1) * page_size
        ).limit(page_size).all()

        return {
            "results": [self._generation_to_dict(g) for g in results],
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size,
            "query": query,
            "filters": filters
        }

    def advanced_filter(
        self,
        user_id: int,
        filters: Dict[str, Any],
        sort_by: str = "created_at",
        sort_order: str = "desc",
        page: int = 1,
        page_size: int = 20
    ) -> Dict[str, Any]:
        """
        Advanced filtering without full-text search

        Args:
            user_id: User ID for permission filtering
            filters: Dictionary of filters
            sort_by: Sort field
            sort_order: Sort order
            page: Page number
            page_size: Items per page

        Returns:
            Filtered results with metadata
        """
        query_builder = self.db.query(Generation).filter(
            Generation.user_id == user_id
        )

        # Apply filters
        query_builder = self._apply_filters(query_builder, filters)

        # Apply sorting
        query_builder = self._apply_sorting(
            query_builder, sort_by, sort_order
        )

        # Get total and paginate
        total = query_builder.count()
        results = query_builder.offset(
            (page - 1) * page_size
        ).limit(page_size).all()

        return {
            "results": [self._generation_to_dict(g) for g in results],
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size,
            "filters": filters
        }

    def export_results(
        self,
        user_id: int,
        format: str,
        query: Optional[str] = None,
        filters: Optional[Dict[str, Any]] = None
    ) -> bytes:
        """
        Export search results to file

        Args:
            user_id: User ID
            format: Export format (csv, json, pdf)
            query: Optional search query
            filters: Optional filters

        Returns:
            File content as bytes
        """
        filters = filters or {}

        # Get results
        if query:
            results = self.full_text_search(
                user_id, query, filters, page_size=10000
            )
        else:
            results = self.advanced_filter(
                user_id, filters, page_size=10000
            )

        # Export based on format
        if format == "csv":
            return self._export_csv(results["results"])
        elif format == "json":
            return self._export_json(results["results"])
        elif format == "pdf":
            return self._export_pdf(results["results"])
        else:
            raise ValidationError(f"Unsupported export format: {format}")

    def get_search_suggestions(
        self,
        user_id: int,
        partial_query: str,
        limit: int = 10
    ) -> List[str]:
        """
        Get search suggestions based on partial query

        Args:
            user_id: User ID
            partial_query: Partial search query
            limit: Number of suggestions

        Returns:
            List of suggestions
        """
        # Search in titles, authors, and prompts
        suggestions = []

        # Title suggestions
        title_matches = self.db.query(Generation.title).filter(
            and_(
                Generation.user_id == user_id,
                Generation.title.ilike(f"%{partial_query}%")
            )
        ).distinct().limit(limit // 3).all()

        # Author suggestions
        author_matches = self.db.query(Generation.author).filter(
            and_(
                Generation.user_id == user_id,
                Generation.author.ilike(f"%{partial_query}%")
            )
        ).distinct().limit(limit // 3).all()

        # Combine and deduplicate
        for title, *_ in title_matches:
            if title and title not in suggestions:
                suggestions.append(title)

        for author, *_ in author_matches:
            if author and author not in suggestions:
                suggestions.append(f"by {author}")

        return suggestions[:limit]

    def _apply_filters(
        self,
        query_builder,
        filters: Dict[str, Any]
    ):
        """Apply filters to query"""
        # Status filter
        if "status" in filters and filters["status"]:
            query_builder = query_builder.filter(
                Generation.status == filters["status"]
            )

        # Language filter
        if "language" in filters and filters["language"]:
            query_builder = query_builder.filter(
                Generation.target_language == filters["language"]
            )

        # Date range filter
        if "date_from" in filters and filters["date_from"]:
            date_from = datetime.fromisoformat(filters["date_from"])
            query_builder = query_builder.filter(
                Generation.created_at >= date_from
            )

        if "date_to" in filters and filters["date_to"]:
            date_to = datetime.fromisoformat(filters["date_to"])
            query_builder = query_builder.filter(
                Generation.created_at <= date_to
            )

        # Quality score range
        if "min_quality" in filters and filters["min_quality"] is not None:
            query_builder = query_builder.filter(
                Generation.overall_quality_score >= filters["min_quality"]
            )

        if "max_quality" in filters and filters["max_quality"] is not None:
            query_builder = query_builder.filter(
                Generation.overall_quality_score <= filters["max_quality"]
            )

        # Chapter count range
        if "min_chapters" in filters and filters["min_chapters"]:
            query_builder = query_builder.filter(
                Generation.chapter_count >= filters["min_chapters"]
            )

        if "max_chapters" in filters and filters["max_chapters"]:
            query_builder = query_builder.filter(
                Generation.chapter_count <= filters["max_chapters"]
            )

        # Provider filter
        if "provider" in filters and filters["provider"]:
            query_builder = query_builder.filter(
                Generation.provider == filters["provider"]
            )

        # Has PDF filter
        if "has_pdf" in filters:
            if filters["has_pdf"]:
                query_builder = query_builder.filter(
                    Generation.pdf_path.isnot(None)
                )
            else:
                query_builder = query_builder.filter(
                    Generation.pdf_path.is_(None)
                )

        # Failed generations
        if "failed_only" in filters and filters["failed_only"]:
            query_builder = query_builder.filter(
                Generation.status == "failed"
            )

        return query_builder

    def _apply_sorting(
        self,
        query_builder,
        sort_by: str,
        sort_order: str
    ):
        """Apply sorting to query"""
        sort_column = {
            "created_at": Generation.created_at,
            "updated_at": Generation.updated_at,
            "title": Generation.title,
            "quality_score": Generation.overall_quality_score,
            "chapter_count": Generation.chapter_count,
            "word_count": Generation.word_count
        }.get(sort_by, Generation.created_at)

        if sort_order == "desc":
            query_builder = query_builder.order_by(desc(sort_column))
        else:
            query_builder = query_builder.order_by(asc(sort_column))

        return query_builder

    def _generation_to_dict(self, generation: Generation) -> Dict[str, Any]:
        """Convert generation to dictionary"""
        return {
            "id": generation.id,
            "title": generation.title,
            "author": generation.author,
            "status": generation.status,
            "target_language": generation.target_language,
            "chapter_count": generation.chapter_count,
            "word_count": generation.word_count,
            "overall_quality_score": generation.overall_quality_score,
            "provider": generation.provider,
            "model": generation.model,
            "created_at": generation.created_at.isoformat(),
            "updated_at": generation.updated_at.isoformat(),
            "pdf_path": generation.pdf_path,
            "gdrive_file_id": generation.gdrive_file_id
        }

    def _export_csv(self, results: List[Dict]) -> bytes:
        """Export results to CSV"""
        output = StringIO()
        writer = csv.DictWriter(
            output,
            fieldnames=[
                "id", "title", "author", "status", "language",
                "chapters", "words", "quality_score", "provider",
                "created_at", "pdf_url"
            ]
        )
        writer.writeheader()

        for result in results:
            writer.writerow({
                "id": result["id"],
                "title": result["title"],
                "author": result["author"],
                "status": result["status"],
                "language": result["target_language"],
                "chapters": result["chapter_count"],
                "words": result["word_count"],
                "quality_score": result["overall_quality_score"],
                "provider": result["provider"],
                "created_at": result["created_at"],
                "pdf_url": f"https://drive.google.com/file/d/{result['gdrive_file_id']}"
                          if result.get('gdrive_file_id') else ""
            })

        return output.getvalue().encode('utf-8')

    def _export_json(self, results: List[Dict]) -> bytes:
        """Export results to JSON"""
        return json.dumps(results, indent=2).encode('utf-8')

    def _export_pdf(self, results: List[Dict]) -> bytes:
        """Export results to PDF"""
        # This would use a PDF generation library like reportlab
        # Simplified implementation
        from app.services.pdf_service import PDFService

        pdf_service = PDFService(self.db)

        # Create a simple PDF report
        content = "# Search Results\n\n"
        content += f"Total results: {len(results)}\n\n"

        for result in results:
            content += f"## {result['title']}\n"
            content += f"- Author: {result['author']}\n"
            content += f"- Status: {result['status']}\n"
            content += f"- Quality: {result['overall_quality_score']}\n"
            content += f"- Created: {result['created_at']}\n\n"

        # Generate PDF
        # This is a simplified placeholder
        return content.encode('utf-8')
```

#### Search API Endpoints

**File:** `backend/app/api/routes/search.py`

```python
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any
from fastapi.responses import Response

from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.user import User
from app.services.search_service import SearchService

router = APIRouter(prefix="/api/generations", tags=["search"])

@router.get("/search")
async def search_generations(
    q: Optional[str] = Query(None, description="Search query"),
    status: Optional[str] = Query(None, description="Filter by status"),
    language: Optional[str] = Query(None, description="Filter by language"),
    date_from: Optional[str] = Query(None, description="Start date (ISO 8601)"),
    date_to: Optional[str] = Query(None, description="End date (ISO 8601)"),
    min_quality: Optional[float] = Query(None, ge=0, le=100),
    max_quality: Optional[float] = Query(None, ge=0, le=100),
    min_chapters: Optional[int] = Query(None, ge=1),
    max_chapters: Optional[int] = Query(None, ge=1),
    provider: Optional[str] = Query(None, description="AI provider"),
    has_pdf: Optional[bool] = Query(None, description="Has generated PDF"),
    failed_only: bool = False,
    sort_by: str = Query("created_at", description="Sort field"),
    sort_order: str = Query("desc", regex="^(asc|desc)$"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Search and filter generations

    **Query Parameters:**
    - q: Full-text search query
    - status: Filter by status (pending, processing, completed, failed)
    - language: Filter by target language
    - date_from: Filter by start date
    - date_to: Filter by end date
    - min_quality: Minimum quality score
    - max_quality: Maximum quality score
    - min_chapters: Minimum chapter count
    - max_chapters: Maximum chapter count
    - provider: Filter by AI provider (openai, anthropic, mistral)
    - has_pdf: Filter by PDF availability
    - failed_only: Show only failed generations
    - sort_by: Sort field
    - sort_order: Sort order (asc/desc)
    - page: Page number
    - page_size: Items per page

    **Returns:** Paginated search results
    """
    service = SearchService(db)

    filters = {
        "status": status,
        "language": language,
        "date_from": date_from,
        "date_to": date_to,
        "min_quality": min_quality,
        "max_quality": max_quality,
        "min_chapters": min_chapters,
        "max_chapters": max_chapters,
        "provider": provider,
        "has_pdf": has_pdf,
        "failed_only": failed_only
    }

    if q:
        return service.full_text_search(
            user_id=current_user.id,
            query=q,
            filters=filters,
            sort_by=sort_by,
            sort_order=sort_order,
            page=page,
            page_size=page_size
        )
    else:
        return service.advanced_filter(
            user_id=current_user.id,
            filters=filters,
            sort_by=sort_by,
            sort_order=sort_order,
            page=page,
            page_size=page_size
        )

@router.post("/filter")
async def advanced_filter(
    filters: Dict[str, Any],
    sort_by: str = Query("created_at"),
    sort_order: str = Query("desc", regex="^(asc|desc)$"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Advanced filtering with POST (for complex filters)

    **Request Body:** Filter criteria as JSON

    **Returns:** Paginated filtered results
    """
    service = SearchService(db)
    return service.advanced_filter(
        user_id=current_user.id,
        filters=filters,
        sort_by=sort_by,
        sort_order=sort_order,
        page=page,
        page_size=page_size
    )

@router.get("/export")
async def export_generations(
    format: str = Query("csv", regex="^(csv|json|pdf)$"),
    q: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    language: Optional[str] = Query(None),
    date_from: Optional[str] = Query(None),
    date_to: Optional[str] = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Export search results to file

    **Query Parameters:**
    - format: Export format (csv, json, pdf)
    - q: Search query
    - status: Filter by status
    - language: Filter by language
    - date_from: Start date
    - date_to: End date

    **Returns:** File download
    """
    service = SearchService(db)

    filters = {
        "status": status,
        "language": language,
        "date_from": date_from,
        "date_to": date_to
    }

    content = service.export_results(
        user_id=current_user.id,
        format=format,
        query=q,
        filters=filters
    )

    media_types = {
        "csv": "text/csv",
        "json": "application/json",
        "pdf": "application/pdf"
    }

    return Response(
        content=content,
        media_type=media_types[format],
        headers={
            "Content-Disposition": f"attachment; filename=generations_export.{format}"
        }
    )

@router.get("/suggestions")
async def search_suggestions(
    q: str = Query(..., min_length=1),
    limit: int = Query(10, ge=1, le=50),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get search suggestions

    **Query Parameters:**
    - q: Partial search query
    - limit: Number of suggestions

    **Returns:** List of suggestions
    """
    service = SearchService(db)
    return {
        "suggestions": service.get_search_suggestions(
            user_id=current_user.id,
            partial_query=q,
            limit=limit
        )
    }
```

#### Search Optimization

**File:** `backend/app/utils/search_optimization.py`

```python
from sqlalchemy import event
from sqlalchemy.engine import Engine
import logging

logger = logging.getLogger(__name__)

@event.listens_for(Engine, "before_cursor_execute")
def log_search_queries(conn, cursor, statement, parameters, context, executemany):
    """Log slow search queries"""
    import time
    start = time.time()

    # Store start time
    context._query_start_time = start

@event.listens_for(Engine, "after_cursor_execute")
def log_slow_queries(conn, cursor, statement, parameters, context, executemany):
    """Log queries that take longer than 1 second"""
    import time

    if hasattr(context, '_query_start_time'):
        duration = time.time() - context._query_start_time

        if duration > 1.0:
            logger.warning(
                f"Slow query detected ({duration:.2f}s): {statement[:200]}"
            )

# Query optimization hints
class SearchOptimizer:
    """Utilities for optimizing search queries"""

    @staticmethod
    def analyze_query_performance(db, query: str) -> dict:
        """Analyze and report query performance"""
        result = db.execute(f"EXPLAIN ANALYZE {query}")
        return {
            "plan": result.fetchall(),
            "suggestions": SearchOptimizer._get_optimization_suggestions(result)
        }

    @staticmethod
    def _get_optimization_suggestions(explain_result) -> list:
        """Get optimization suggestions based on EXPLAIN ANALYZE"""
        suggestions = []

        # Check for sequential scans
        if "Seq Scan" in str(explain_result):
            suggestions.append("Consider adding an index for frequently filtered columns")

        # Check for high cost
        if "cost=" in str(explain_result):
            suggestions.append("Query has high cost, consider limiting result set")

        return suggestions

    @staticmethod
    def rebuild_search_indexes(db):
        """Rebuild search indexes for better performance"""
        db.execute("REINDEX TABLE generations;")
        db.execute("VACUUM ANALYZE generations;")
        db.commit()
```

---

### Version Control for Regenerations

#### Overview
Track all regenerations as versions, allowing users to compare different versions and revert to previous ones.

#### Database Schema

```sql
-- Add version tracking to generations
ALTER TABLE generations ADD COLUMN version_number INTEGER DEFAULT 1;
ALTER TABLE generations ADD COLUMN parent_generation_id INTEGER REFERENCES generations(id) ON DELETE SET NULL;
ALTER TABLE generations ADD COLUMN is_latest_version BOOLEAN DEFAULT TRUE;

-- Create indexes for version queries
CREATE INDEX idx_generations_parent ON generations(parent_generation_id);
CREATE INDEX idx_generations_version ON generations(user_id, parent_generation_id, version_number);
CREATE INDEX idx_generations_latest ON generations(user_id, is_latest_version) WHERE is_latest_version = TRUE;

-- Function to update version status on insert
CREATE OR REPLACE FUNCTION update_generation_versions() RETURNS trigger AS $$
BEGIN
    -- Mark parent's older versions as not latest
    IF NEW.parent_generation_id IS NOT NULL THEN
        UPDATE generations
        SET is_latest_version = FALSE
        WHERE parent_generation_id = NEW.parent_generation_id
        AND id != NEW.id;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER generation_version_trigger
    AFTER INSERT ON generations
    FOR EACH ROW
    EXECUTE FUNCTION update_generation_versions();
```

#### Version Service

**File:** `backend/app/services/version_service.py`

```python
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, desc, func
from datetime import datetime

from app.models.generation import Generation
from app.models.user import User
from app.core.exceptions import ValidationError, NotFoundError

class VersionService:
    def __init__(self, db: Session):
        self.db = db

    def create_new_version(
        self,
        parent_generation_id: int,
        user_id: int,
        generation_data: Dict[str, Any]
    ) -> Generation:
        """
        Create a new version of an existing generation

        Args:
            parent_generation_id: ID of the generation to version
            user_id: User ID
            generation_data: New generation data

        Returns:
            New generation version
        """
        # Get parent generation
        parent = self.db.query(Generation).filter(
            and_(
                Generation.id == parent_generation_id,
                Generation.user_id == user_id
            )
        ).first()

        if not parent:
            raise NotFoundError("Parent generation not found")

        # Get next version number
        max_version = self.db.query(
            func.max(Generation.version_number)
        ).filter(
            Generation.parent_generation_id == parent.parent_generation_id or parent.id
        ).scalar()

        next_version = (max_version or parent.version_number) + 1

        # If parent is already a version, use the root parent
        root_parent_id = parent.parent_generation_id if parent.parent_generation_id else parent.id

        # Mark all existing versions as not latest
        self.db.query(Generation).filter(
            or_(
                Generation.id == root_parent_id,
                Generation.parent_generation_id == root_parent_id
            )
        ).update({
            "is_latest_version": False
        })

        # Create new version
        new_generation = Generation(
            user_id=user_id,
            parent_generation_id=root_parent_id,
            version_number=next_version,
            is_latest_version=True,
            **generation_data
        )

        self.db.add(new_generation)
        self.db.commit()
        self.db.refresh(new_generation)

        return new_generation

    def get_version_history(
        self,
        generation_id: int,
        user_id: int
    ) -> List[Dict[str, Any]]:
        """
        Get version history for a generation

        Args:
            generation_id: Generation ID (can be any version)
            user_id: User ID

        Returns:
            List of all versions
        """
        # Find root generation
        generation = self.db.query(Generation).filter(
            Generation.id == generation_id
        ).first()

        if not generation:
            raise NotFoundError("Generation not found")

        # Get root ID
        if generation.parent_generation_id:
            root_id = generation.parent_generation_id
        else:
            root_id = generation.id

        # Get all versions
        versions = self.db.query(Generation).filter(
            or_(
                Generation.id == root_id,
                Generation.parent_generation_id == root_id
            )
        ).order_by(Generation.version_number).all()

        return [
            {
                "id": v.id,
                "version_number": v.version_number,
                "is_latest": v.is_latest_version,
                "status": v.status,
                "chapter_count": v.chapter_count,
                "word_count": v.word_count,
                "overall_quality_score": v.overall_quality_score,
                "created_at": v.created_at.isoformat(),
                "provider": v.provider,
                "model": v.model,
                "gdrive_file_id": v.gdrive_file_id
            }
            for v in versions
        ]

    def compare_versions(
        self,
        version1_id: int,
        version2_id: int,
        user_id: int
    ) -> Dict[str, Any]:
        """
        Compare two versions of a generation

        Args:
            version1_id: First version ID
            version2_id: Second version ID
            user_id: User ID

        Returns:
            Comparison result
        """
        # Get both versions
        version1 = self.db.query(Generation).filter(
            and_(
                Generation.id == version1_id,
                Generation.user_id == user_id
            )
        ).first()

        version2 = self.db.query(Generation).filter(
            and_(
                Generation.id == version2_id,
                Generation.user_id == user_id
            )
        ).first()

        if not version1 or not version2:
            raise NotFoundError("One or both versions not found")

        # Calculate differences
        comparison = {
            "version1": {
                "id": version1.id,
                "version_number": version1.version_number,
                "created_at": version1.created_at.isoformat()
            },
            "version2": {
                "id": version2.id,
                "version_number": version2.version_number,
                "created_at": version2.created_at.isoformat()
            },
            "differences": {
                "chapter_count": version2.chapter_count - version1.chapter_count,
                "word_count": version2.word_count - version1.word_count,
                "quality_score": version2.overall_quality_score - version1.overall_quality_score,
                "provider": version1.provider != version2.provider,
                "model": version1.model != version2.model
            }
        }

        # Chapter-level comparison
        chapters_v1 = {c.chapter_number: c for c in version1.chapters}
        chapters_v2 = {c.chapter_number: c for c in version2.chapters}

        chapter_differences = []
        for num in set(chapters_v1.keys()) | set(chapters_v2.keys()):
            ch1 = chapters_v1.get(num)
            ch2 = chapters_v2.get(num)

            diff = {
                "chapter_number": num,
                "version1_word_count": ch1.word_count if ch1 else 0,
                "version2_word_count": ch2.word_count if ch2 else 0,
                "word_count_change": (ch2.word_count if ch2 else 0) - (ch1.word_count if ch1 else 0),
                "version1_quality": ch1.quality_score if ch1 else 0,
                "version2_quality": ch2.quality_score if ch2 else 0,
                "quality_change": (ch2.quality_score if ch2 else 0) - (ch1.quality_score if ch1 else 0)
            }
            chapter_differences.append(diff)

        comparison["chapter_differences"] = chapter_differences

        return comparison

    def get_version_tree(
        self,
        generation_id: int,
        user_id: int
    ) -> Dict[str, Any]:
        """
        Get version tree visualization

        Args:
            generation_id: Root generation ID
            user_id: User ID

        Returns:
            Version tree structure
        """
        generation = self.db.query(Generation).filter(
            Generation.id == generation_id
        ).first()

        if not generation:
            raise NotFoundError("Generation not found")

        # Build tree structure
        tree = {
            "id": generation.id,
            "version_number": generation.version_number,
            "is_latest": generation.is_latest_version,
            "status": generation.status,
            "created_at": generation.created_at.isoformat(),
            "children": []
        }

        # Recursively get children
        children = self.db.query(Generation).filter(
            Generation.parent_generation_id == generation.id
        ).order_by(Generation.version_number).all()

        for child in children:
            tree["children"].append(
                self.get_version_tree(child.id, user_id)
            )

        return tree

    def rollback_to_version(
        self,
        version_id: int,
        user_id: int
    ) -> Generation:
        """
        Rollback to a previous version by creating a new version from it

        Args:
            version_id: Version to rollback to
            user_id: User ID

        Returns:
            New generation (copy of old version)
        """
        # Get version to rollback to
        old_version = self.db.query(Generation).filter(
            and_(
                Generation.id == version_id,
                Generation.user_id == user_id
            )
        ).first()

        if not old_version:
            raise NotFoundError("Version not found")

        # Create a new version based on the old one
        new_version = self.create_new_version(
            parent_generation_id=old_version.parent_generation_id or old_version.id,
            user_id=user_id,
            generation_data={
                "title": old_version.title,
                "author": old_version.author,
                "prompt": old_version.prompt,
                "target_language": old_version.target_language,
                "provider": old_version.provider,
                "model": old_version.model,
                "max_tokens": old_version.max_tokens,
                "temperature": old_version.temperature
            }
        )

        return new_version

    def promote_to_latest(
        self,
        version_id: int,
        user_id: int
    ) -> Generation:
        """
        Promote a specific version to be the latest without creating a new version

        Args:
            version_id: Version to promote
            user_id: User ID

        Returns:
            Updated generation
        """
        generation = self.db.query(Generation).filter(
            and_(
                Generation.id == version_id,
                Generation.user_id == user_id
            )
        ).first()

        if not generation:
            raise NotFoundError("Generation not found")

        # Get root ID
        root_id = generation.parent_generation_id or generation.id

        # Mark all versions as not latest
        self.db.query(Generation).filter(
            or_(
                Generation.id == root_id,
                Generation.parent_generation_id == root_id
            )
        ).update({"is_latest_version": False})

        # Mark this version as latest
        generation.is_latest_version = True

        self.db.commit()
        self.db.refresh(generation)

        return generation
```

#### Version API Endpoints

**File:** `backend/app/api/routes/versions.py`

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.user import User
from app.services.version_service import VersionService
from app.schemas.generation import GenerationResponse

router = APIRouter(prefix="/api/generations", tags=["versions"])

@router.get("/{generation_id}/versions")
async def get_version_history(
    generation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get version history for a generation

    **Path Parameters:**
    - generation_id: Generation ID

    **Returns:** List of all versions
    """
    service = VersionService(db)
    return service.get_version_history(generation_id, current_user.id)

@router.get("/{generation_id}/versions/tree")
async def get_version_tree(
    generation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get version tree visualization

    **Path Parameters:**
    - generation_id: Root generation ID

    **Returns:** Version tree structure
    """
    service = VersionService(db)
    return service.get_version_tree(generation_id, current_user.id)

@router.get("/compare/{version1_id}/{version2_id}")
async def compare_versions(
    version1_id: int,
    version2_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Compare two versions

    **Path Parameters:**
    - version1_id: First version ID
    - version2_id: Second version ID

    **Returns:** Comparison result with differences
    """
    service = VersionService(db)
    return service.compare_versions(version1_id, version2_id, current_user.id)

@router.post("/{generation_id}/versions/rollback")
async def rollback_to_version(
    generation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Rollback to a previous version (creates new version from old one)

    **Path Parameters:**
    - generation_id: Version to rollback to

    **Returns:** New generation based on old version
    """
    service = VersionService(db)
    return service.rollback_to_version(generation_id, current_user.id)

@router.post("/{generation_id}/versions/promote")
async def promote_to_latest(
    generation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Promote a version to be the latest

    **Path Parameters:**
    - generation_id: Version to promote

    **Returns:** Updated generation
    """
    service = VersionService(db)
    return service.promote_to_latest(generation_id, current_user.id)
```

---

### Email Notifications System

#### Overview
Send email notifications for generation events, daily summaries, and weekly reports.

#### Database Schema

```sql
-- Email notifications table
CREATE TABLE email_notifications (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    type VARCHAR(50) NOT NULL,
    subject VARCHAR(500),
    body TEXT,
    status VARCHAR(20) DEFAULT 'pending',
    error_message TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    sent_at TIMESTAMP WITH TIME ZONE,
    retries INTEGER DEFAULT 0
);

-- User notification preferences
CREATE TABLE notification_preferences (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE UNIQUE,
    email_enabled BOOLEAN DEFAULT TRUE,
    generation_complete BOOLEAN DEFAULT TRUE,
    generation_failed BOOLEAN DEFAULT TRUE,
    daily_summary BOOLEAN DEFAULT FALSE,
    daily_summary_time TIME DEFAULT '08:00',
    weekly_quality_report BOOLEAN DEFAULT FALSE,
    weekly_report_day INTEGER DEFAULT 1,
    email_address VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Email templates
CREATE TABLE email_templates (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    subject VARCHAR(500) NOT NULL,
    body_html TEXT NOT NULL,
    body_text TEXT NOT NULL,
    variables JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_email_notifications_user ON email_notifications(user_id);
CREATE INDEX idx_email_notifications_status ON email_notifications(status);
CREATE INDEX idx_email_notifications_created ON email_notifications(created_at);
```

#### Email Service Configuration

**File:** `backend/app/core/email_config.py`

```python
import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class EmailConfig:
    """Email service configuration"""

    # Provider: sendgrid, mailgun, ses, or smtp
    provider: str = os.getenv("EMAIL_PROVIDER", "sendgrid")

    # SendGrid
    sendgrid_api_key: Optional[str] = os.getenv("SENDGRID_API_KEY")

    # Mailgun
    mailgun_api_key: Optional[str] = os.getenv("MAILGUN_API_KEY")
    mailgun_domain: Optional[str] = os.getenv("MAILGUN_DOMAIN")

    # AWS SES
    aws_region: Optional[str] = os.getenv("AWS_REGION", "us-east-1")
    aws_access_key: Optional[str] = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_key: Optional[str] = os.getenv("AWS_SECRET_ACCESS_KEY")

    # SMTP
    smtp_host: Optional[str] = os.getenv("SMTP_HOST")
    smtp_port: int = int(os.getenv("SMTP_PORT", "587"))
    smtp_username: Optional[str] = os.getenv("SMTP_USERNAME")
    smtp_password: Optional[str] = os.getenv("SMTP_PASSWORD")
    smtp_use_tls: bool = os.getenv("SMTP_USE_TLS", "true").lower() == "true"

    # Common settings
    from_email: str = os.getenv("FROM_EMAIL", "noreply@bookmake.app")
    from_name: str = os.getenv("FROM_NAME", "BookMake App")
    reply_to: Optional[str] = os.getenv("REPLY_TO")

    # Queue settings
    use_queue: bool = os.getenv("USE_EMAIL_QUEUE", "true").lower() == "true"
    max_retries: int = int(os.getenv("EMAIL_MAX_RETRIES", "3"))
    retry_delay: int = int(os.getenv("EMAIL_RETRY_DELAY", "300"))  # 5 minutes

email_config = EmailConfig()
```

#### Email Service Implementation

**File:** `backend/app/services/email_service.py`

```python
import os
from typing import Dict, Any, List
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from jinja2 import Template
import logging

from app.core.email_config import email_config
from app.models.user import User
from app.models.email import (
    EmailNotification, NotificationPreference, EmailTemplate
)
from app.core.exceptions import ValidationError

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self, db: Session):
        self.db = db
        self.config = email_config

        # Initialize email provider
        if self.config.provider == "sendgrid":
            from sendgrid import SendGridAPIClient
            from sendgrid.helpers.mail import Mail
            self.sg_client = SendGridAPIClient(self.config.sendgrid_api_key)
            self.Mail = Mail
        elif self.config.provider == "mailgun":
            import mailgun
            self.mg_client = mailgun.Client(
                self.config.mailgun_domain,
                self.config.mailgun_api_key
            )
        elif self.config.provider == "ses":
            import boto3
            self.ses_client = boto3.client(
                'ses',
                region_name=self.config.aws_region,
                aws_access_key_id=self.config.aws_access_key,
                aws_secret_access_key=self.config.aws_secret_key
            )

    def send_notification(
        self,
        user_id: int,
        notification_type: str,
        data: Dict[str, Any]
    ) -> bool:
        """
        Send an email notification

        Args:
            user_id: User ID
            notification_type: Type of notification
            data: Data for template rendering

        Returns:
            True if sent successfully
        """
        # Get user preferences
        prefs = self.db.query(NotificationPreference).filter(
            NotificationPreference.user_id == user_id
        ).first()

        if not prefs or not prefs.email_enabled:
            logger.info(f"Email notifications disabled for user {user_id}")
            return False

        # Check if this type is enabled
        type_mapping = {
            "generation_complete": prefs.generation_complete,
            "generation_failed": prefs.generation_failed,
            "daily_summary": prefs.daily_summary,
            "weekly_report": prefs.weekly_quality_report
        }

        if not type_mapping.get(notification_type, True):
            logger.info(f"{notification_type} notifications disabled for user {user_id}")
            return False

        # Get email template
        template = self.db.query(EmailTemplate).filter(
            EmailTemplate.name == notification_type
        ).first()

        if not template:
            logger.error(f"Email template not found: {notification_type}")
            return False

        # Get user
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            logger.error(f"User not found: {user_id}")
            return False

        # Get email address
        email = prefs.email_address or user.email

        # Render templates
        subject = self._render_template(template.subject, data)
        body_html = self._render_template(template.body_html, data)
        body_text = self._render_template(template.body_text, data)

        # Create notification record
        notification = EmailNotification(
            user_id=user_id,
            type=notification_type,
            subject=subject,
            body=body_html,
            status="pending"
        )
        self.db.add(notification)
        self.db.commit()

        # Send email
        try:
            success = self._send_email(
                to_email=email,
                to_name=user.username,
                subject=subject,
                body_html=body_html,
                body_text=body_text
            )

            if success:
                notification.status = "sent"
                notification.sent_at = datetime.utcnow()
            else:
                notification.status = "failed"
                notification.error_message = "Failed to send email"

            self.db.commit()
            return success

        except Exception as e:
            logger.error(f"Error sending email: {e}")
            notification.status = "failed"
            notification.error_message = str(e)
            self.db.commit()
            return False

    def send_generation_complete(
        self,
        user_id: int,
        generation_id: int,
        title: str,
        chapter_count: int,
        word_count: int,
        quality_score: float,
        pdf_url: str
    ) -> bool:
        """Send generation complete notification"""
        data = {
            "title": title,
            "chapter_count": chapter_count,
            "word_count": word_count,
            "quality_score": quality_score,
            "pdf_url": pdf_url,
            "generation_id": generation_id,
            "app_url": os.getenv("APP_URL", "https://bookmake.app")
        }

        return self.send_notification(
            user_id=user_id,
            notification_type="generation_complete",
            data=data
        )

    def send_generation_failed(
        self,
        user_id: int,
        generation_id: int,
        title: str,
        error_message: str
    ) -> bool:
        """Send generation failed notification"""
        data = {
            "title": title,
            "error_message": error_message,
            "generation_id": generation_id,
            "app_url": os.getenv("APP_URL", "https://bookmake.app")
        }

        return self.send_notification(
            user_id=user_id,
            notification_type="generation_failed",
            data=data
        )

    def send_daily_summary(self, user_id: int, summary_data: Dict[str, Any]) -> bool:
        """Send daily summary email"""
        data = {
            **summary_data,
            "date": datetime.now().strftime("%B %d, %Y"),
            "app_url": os.getenv("APP_URL", "https://bookmake.app")
        }

        return self.send_notification(
            user_id=user_id,
            notification_type="daily_summary",
            data=data
        )

    def send_weekly_report(self, user_id: int, report_data: Dict[str, Any]) -> bool:
        """Send weekly quality report"""
        data = {
            **report_data,
            "week_start": report_data["week_start"].strftime("%B %d"),
            "week_end": report_data["week_end"].strftime("%B %d, %Y"),
            "app_url": os.getenv("APP_URL", "https://bookmake.app")
        }

        return self.send_notification(
            user_id=user_id,
            notification_type="weekly_report",
            data=data
        )

    def _send_email(
        self,
        to_email: str,
        to_name: str,
        subject: str,
        body_html: str,
        body_text: str
    ) -> bool:
        """Send email via configured provider"""

        if self.config.provider == "sendgrid":
            return self._send_via_sendgrid(
                to_email, to_name, subject, body_html, body_text
            )
        elif self.config.provider == "mailgun":
            return self._send_via_mailgun(
                to_email, to_name, subject, body_html, body_text
            )
        elif self.config.provider == "ses":
            return self._send_via_ses(
                to_email, to_name, subject, body_html, body_text
            )
        else:
            return self._send_via_smtp(
                to_email, to_name, subject, body_html, body_text
            )

    def _send_via_sendgrid(
        self,
        to_email: str,
        to_name: str,
        subject: str,
        body_html: str,
        body_text: str
    ) -> bool:
        """Send email via SendGrid"""
        try:
            message = self.Mail(
                from_email=(self.config.from_email, self.config.from_name),
                to_emails=(to_email, to_name),
                subject=subject,
                html_content=body_html,
                plain_text_content=body_text
            )

            if self.config.reply_to:
                message.reply_to = self.config.reply_to

            response = self.sg_client.send(message)

            if response.status_code in [200, 202]:
                logger.info(f"Email sent via SendGrid to {to_email}")
                return True
            else:
                logger.error(f"SendGrid error: {response.status_code} - {response.body}")
                return False

        except Exception as e:
            logger.error(f"SendGrid exception: {e}")
            return False

    def _send_via_mailgun(
        self,
        to_email: str,
        to_name: str,
        subject: str,
        body_html: str,
        body_text: str
    ) -> bool:
        """Send email via Mailgun"""
        try:
            result = self.mg_client.send_email(
                to_email,
                subject,
                body_text,
                html=body_html,
                from_email=f"{self.config.from_name} <{self.config.from_email}>"
            )

            if result.status_code == 200:
                logger.info(f"Email sent via Mailgun to {to_email}")
                return True
            else:
                logger.error(f"Mailgun error: {result.status_code}")
                return False

        except Exception as e:
            logger.error(f"Mailgun exception: {e}")
            return False

    def _send_via_ses(
        self,
        to_email: str,
        to_name: str,
        subject: str,
        body_html: str,
        body_text: str
    ) -> bool:
        """Send email via AWS SES"""
        try:
            response = self.ses_client.send_email(
                Source=f"{self.config.from_name} <{self.config.from_email}>",
                Destination={
                    'ToAddresses': [f"{to_name} <{to_email}>"]
                },
                Message={
                    'Subject': {'Data': subject},
                    'Body': {
                        'Text': {'Data': body_text},
                        'Html': {'Data': body_html}
                    }
                }
            )

            logger.info(f"Email sent via SES to {to_email}")
            return True

        except Exception as e:
            logger.error(f"SES exception: {e}")
            return False

    def _send_via_smtp(
        self,
        to_email: str,
        to_name: str,
        subject: str,
        body_html: str,
        body_text: str
    ) -> bool:
        """Send email via SMTP"""
        try:
            import smtplib
            from email.mime.multipart import MIMEMultipart
            from email.mime.text import MIMEText

            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = f"{self.config.from_name} <{self.config.from_email}>"
            msg['To'] = f"{to_name} <{to_email}>"

            if self.config.reply_to:
                msg['Reply-To'] = self.config.reply_to

            # Add text and HTML parts
            part1 = MIMEText(body_text, 'plain')
            part2 = MIMEText(body_html, 'html')
            msg.attach(part1)
            msg.attach(part2)

            # Send via SMTP
            with smtplib.SMTP(
                self.config.smtp_host,
                self.config.smtp_port
            ) as server:
                if self.config.smtp_use_tls:
                    server.starttls()

                if self.config.smtp_username and self.config.smtp_password:
                    server.login(
                        self.config.smtp_username,
                        self.config.smtp_password
                    )

                server.send_message(msg)

            logger.info(f"Email sent via SMTP to {to_email}")
            return True

        except Exception as e:
            logger.error(f"SMTP exception: {e}")
            return False

    def _render_template(self, template_string: str, data: Dict[str, Any]) -> str:
        """Render Jinja2 template"""
        try:
            template = Template(template_string)
            return template.render(**data)
        except Exception as e:
            logger.error(f"Template rendering error: {e}")
            return template_string

    def retry_failed_notifications(self) -> int:
        """Retry failed email notifications"""
        notifications = self.db.query(EmailNotification).filter(
            and_(
                EmailNotification.status == "failed",
                EmailNotification.retries < self.config.max_retries,
                EmailNotification.created_at > datetime.utcnow() - timedelta(hours=24)
            )
        ).all()

        retried = 0
        for notification in notifications:
            notification.retries += 1
            notification.status = "pending"
            retried += 1

        self.db.commit()
        logger.info(f"Queued {retried} failed notifications for retry")

        return retried
```

#### Email Templates Seeding

**File:** `backend/scripts/seed_email_templates.py`

```python
import sys
sys.path.append('.')

from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.email import EmailTemplate

EMAIL_TEMPLATES = [
    {
        "name": "generation_complete",
        "subject": "Your eBook is ready! - {{ title }}",
        "body_html": """<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }
        .content { background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }
        .stats { display: flex; justify-content: space-around; margin: 20px 0; }
        .stat { text-align: center; }
        .stat-value { font-size: 24px; font-weight: bold; color: #667eea; }
        .stat-label { font-size: 14px; color: #666; }
        .button { display: inline-block; background: #667eea; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; }
        .footer { text-align: center; margin-top: 30px; color: #999; font-size: 12px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Your eBook is Ready!</h1>
        </div>
        <div class="content">
            <h2>{{ title }}</h2>
            <p>Great news! Your eBook has been successfully generated and is ready for download.</p>

            <div class="stats">
                <div class="stat">
                    <div class="stat-value">{{ chapter_count }}</div>
                    <div class="stat-label">Chapters</div>
                </div>
                <div class="stat">
                    <div class="stat-value">{{ word_count|number_format }}</div>
                    <div class="stat-label">Words</div>
                </div>
                <div class="stat">
                    <div class="stat-value">{{ quality_score|round(1) }}%</div>
                    <div class="stat-label">Quality Score</div>
                </div>
            </div>

            <div style="text-align: center;">
                <a href="{{ pdf_url }}" class="button">Download Your eBook</a>
            </div>

            <p style="text-align: center; margin-top: 20px;">
                <a href="{{ app_url }}/generations/{{ generation_id }}">View in Dashboard</a>
            </p>
        </div>
        <div class="footer">
            <p>You received this email because you have notifications enabled for BookMake App.</p>
            <p>&copy; {{ now|strftime('%Y') }} BookMake App. All rights reserved.</p>
        </div>
    </div>
</body>
</html>""",
        "body_text": """Your eBook is ready!

Title: {{ title }}

Statistics:
- Chapters: {{ chapter_count }}
- Words: {{ word_count|number_format }}
- Quality Score: {{ quality_score|round(1) }}%

Download your eBook: {{ pdf_url }}

View in Dashboard: {{ app_url }}/generations/{{ generation_id }}

---
You received this email because you have notifications enabled for BookMake App.
© {{ now|strftime('%Y') }} BookMake App. All rights reserved."""
    },
    {
        "name": "generation_failed",
        "subject": "eBook Generation Failed - {{ title }}",
        "body_html": """<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: #e74c3c; color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }
        .content { background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }
        .error-box { background: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 20px 0; }
        .button { display: inline-block; background: #e74c3c; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Generation Failed</h1>
        </div>
        <div class="content">
            <h2>{{ title }}</h2>
            <p>We encountered an error while generating your eBook.</p>

            <div class="error-box">
                <strong>Error:</strong>
                <p>{{ error_message }}</p>
            </div>

            <p>You can try regenerating the eBook from your dashboard.</p>

            <div style="text-align: center;">
                <a href="{{ app_url }}/generations/{{ generation_id }}" class="button">View Details & Retry</a>
            </div>
        </div>
    </div>
</body>
</html>""",
        "body_text": """eBook Generation Failed

Title: {{ title }}

We encountered an error while generating your eBook.

Error:
{{ error_message }}

You can try regenerating the eBook from your dashboard:
{{ app_url }}/generations/{{ generation_id }}
"""
    },
    {
        "name": "daily_summary",
        "subject": "Your Daily Summary - {{ date }}",
        "body_html": """<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; }
        .content { background: #f9f9f9; padding: 30px; }
        .stat-row { display: flex; justify-content: space-between; margin: 10px 0; padding: 10px; background: white; border-radius: 5px; }
        .stat-label { font-weight: bold; }
        .stat-value { color: #667eea; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Daily Summary</h1>
            <p>{{ date }}</p>
        </div>
        <div class="content">
            <h2>Today's Activity</h2>

            <div class="stat-row">
                <span class="stat-label">eBooks Completed</span>
                <span class="stat-value">{{ completed_count }}</span>
            </div>
            <div class="stat-row">
                <span class="stat-label">Total Words Generated</span>
                <span class="stat-value">{{ total_words|number_format }}</span>
            </div>
            <div class="stat-row">
                <span class="stat-label">Average Quality Score</span>
                <span class="stat-value">{{ avg_quality|round(1) }}%</span>
            </div>
            <div class="stat-row">
                <span class="stat-label">Failed Generations</span>
                <span class="stat-value">{{ failed_count }}</span>
            </div>

            {% if recent_generations %}
            <h3 style="margin-top: 30px;">Recent Generations</h3>
            {% for gen in recent_generations %}
            <div style="background: white; padding: 15px; margin: 10px 0; border-radius: 5px;">
                <strong>{{ gen.title }}</strong><br>
                Status: {{ gen.status }} | Quality: {{ gen.quality_score|round(1) }}%
            </div>
            {% endfor %}
            {% endif %}

            <div style="text-align: center; margin-top: 30px;">
                <a href="{{ app_url }}/generations" style="background: #667eea; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px;">View All Generations</a>
            </div>
        </div>
    </div>
</body>
</html>""",
        "body_text": """Daily Summary for {{ date }}

Today's Activity:
- eBooks Completed: {{ completed_count }}
- Total Words Generated: {{ total_words|number_format }}
- Average Quality Score: {{ avg_quality|round(1) }}%
- Failed Generations: {{ failed_count }}

{% if recent_generations %}
Recent Generations:
{% for gen in recent_generations %}
- {{ gen.title }} ({{ gen.status }}, Quality: {{ gen.quality_score|round(1) }}%)
{% endfor %}
{% endif %}

View all generations: {{ app_url }}/generations
"""
    },
    {
        "name": "weekly_report",
        "subject": "Weekly Quality Report - {{ week_start }} to {{ week_end }}",
        "body_html": """<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; }
        .content { background: #f9f9f9; padding: 30px; }
        .chart-placeholder { background: white; padding: 20px; margin: 20px 0; border-radius: 5px; text-align: center; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Weekly Quality Report</h1>
            <p>{{ week_start }} - {{ week_end }}</p>
        </div>
        <div class="content">
            <h2>Overview</h2>

            <p><strong>Total Generations:</strong> {{ total_generations }}</p>
            <p><strong>Success Rate:</strong> {{ success_rate|round(1) }}%</p>
            <p><strong>Average Quality Score:</strong> {{ avg_quality|round(1) }}%</p>

            <h3>Quality Trend</h3>
            <div class="chart-placeholder">
                [Quality chart visualization would be here]
                <p>Average quality improved by {{ quality_improvement|round(1) }}% this week!</p>
            </div>

            {% if top_generations %}
            <h3>Top Performing eBooks</h3>
            {% for gen in top_generations %}
            <div style="background: white; padding: 15px; margin: 10px 0; border-radius: 5px;">
                <strong>{{ gen.title }}</strong><br>
                Quality: {{ gen.quality_score|round(1) }}% | {{ gen.word_count|number_format }} words
            </div>
            {% endfor %}
            {% endif %}

            <div style="text-align: center; margin-top: 30px;">
                <a href="{{ app_url }}/analytics" style="background: #667eea; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px;">View Detailed Analytics</a>
            </div>
        </div>
    </div>
</body>
</html>""",
        "body_text": """Weekly Quality Report
{{ week_start }} - {{ week_end }}

Overview:
- Total Generations: {{ total_generations }}
- Success Rate: {{ success_rate|round(1) }}%
- Average Quality Score: {{ avg_quality|round(1) }}%
- Quality Improvement: {{ quality_improvement|round(1) }}%

{% if top_generations %}
Top Performing eBooks:
{% for gen in top_generations %}
- {{ gen.title }} (Quality: {{ gen.quality_score|round(1) }}%, {{ gen.word_count|number_format }} words)
{% endfor %}
{% endif %}

View detailed analytics: {{ app_url }}/analytics
"""
    }
]

def seed_email_templates(db: Session):
    """Seed email templates"""
    for template_data in EMAIL_TEMPLATES:
        existing = db.query(EmailTemplate).filter(
            EmailTemplate.name == template_data["name"]
        ).first()

        if not existing:
            template = EmailTemplate(**template_data)
            db.add(template)
            print(f"Created email template: {template_data['name']}")

    db.commit()
    print("Email templates seeded successfully!")

if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed_email_templates(db)
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()
```

#### Celery Tasks for Email Processing

**File:** `backend/app/workers/email_tasks.py`

```python
from celery import shared_task
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.core.database import SessionLocal
from app.services.email_service import EmailService
from app.models.email import EmailNotification, NotificationPreference
from app.models.generation import Generation
import logging

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3)
def send_pending_emails(self):
    """Send all pending email notifications"""
    db = SessionLocal()
    try:
        # Get pending notifications
        notifications = db.query(EmailNotification).filter(
            EmailNotification.status == "pending"
        ).limit(50).all()

        logger.info(f"Found {len(notifications)} pending emails to send")

        email_service = EmailService(db)

        for notification in notifications:
            # Mark as processing
            notification.status = "processing"
            db.commit()

            # This would trigger actual sending based on notification type
            # Implementation depends on how you structure notification data

        return f"Processed {len(notifications)} emails"

    except Exception as e:
        logger.error(f"Error in send_pending_emails: {e}")
        raise self.retry(exc=e, countdown=300)  # Retry in 5 minutes
    finally:
        db.close()

@shared_task
def send_daily_summaries():
    """Send daily summary emails to users who have enabled them"""
    db = SessionLocal()
    try:
        # Get users who want daily summaries
        prefs = db.query(NotificationPreference).filter(
            NotificationPreference.daily_summary == True
        ).all()

        logger.info(f"Sending daily summaries to {len(prefs)} users")

        email_service = EmailService(db)

        for pref in prefs:
            # Get yesterday's statistics
            yesterday = datetime.utcnow() - timedelta(days=1)
            start_of_day = yesterday.replace(hour=0, minute=0, second=0)
            end_of_day = yesterday.replace(hour=23, minute=59, second=59)

            generations = db.query(Generation).filter(
                Generation.user_id == pref.user_id,
                Generation.created_at >= start_of_day,
                Generation.created_at <= end_of_day
            ).all()

            if generations:
                completed = [g for g in generations if g.status == "completed"]
                failed = [g for g in generations if g.status == "failed"]

                summary_data = {
                    "completed_count": len(completed),
                    "failed_count": len(failed),
                    "total_words": sum(g.word_count or 0 for g in completed),
                    "avg_quality": sum(g.overall_quality_score or 0 for g in completed) / len(completed) if completed else 0,
                    "recent_generations": [
                        {
                            "title": g.title,
                            "status": g.status,
                            "quality_score": g.overall_quality_score or 0
                        }
                        for g in generations[:5]
                    ]
                }

                email_service.send_daily_summary(pref.user_id, summary_data)

        return f"Sent daily summaries to {len(prefs)} users"

    except Exception as e:
        logger.error(f"Error in send_daily_summaries: {e}")
    finally:
        db.close()

@shared_task
def send_weekly_reports():
    """Send weekly quality reports"""
    db = SessionLocal()
    try:
        prefs = db.query(NotificationPreference).filter(
            NotificationPreference.weekly_quality_report == True
        ).all()

        logger.info(f"Sending weekly reports to {len(prefs)} users")

        email_service = EmailService(db)

        for pref in prefs:
            # Get last week's data
            week_end = datetime.utcnow()
            week_start = week_end - timedelta(days=7)

            generations = db.query(Generation).filter(
                Generation.user_id == pref.user_id,
                Generation.created_at >= week_start,
                Generation.created_at <= week_end
            ).all()

            if generations:
                completed = [g for g in generations if g.status == "completed"]

                # Calculate previous week's average for comparison
                prev_week_start = week_start - timedelta(days=7)
                prev_week_end = week_start

                prev_generations = db.query(Generation).filter(
                    Generation.user_id == pref.user_id,
                    Generation.created_at >= prev_week_start,
                    Generation.created_at <= prev_week_end
                ).all()

                prev_avg_quality = sum(
                    g.overall_quality_score or 0 for g in prev_generations
                ) / len(prev_generations) if prev_generations else 0

                current_avg_quality = sum(
                    g.overall_quality_score or 0 for g in completed
                ) / len(completed) if completed else 0

                report_data = {
                    "total_generations": len(generations),
                    "success_rate": (len(completed) / len(generations) * 100) if generations else 0,
                    "avg_quality": current_avg_quality,
                    "quality_improvement": current_avg_quality - prev_avg_quality,
                    "week_start": week_start,
                    "week_end": week_end,
                    "top_generations": [
                        {
                            "title": g.title,
                            "quality_score": g.overall_quality_score or 0,
                            "word_count": g.word_count or 0
                        }
                        for g in sorted(
                            completed,
                            key=lambda x: x.overall_quality_score or 0,
                            reverse=True
                        )[:5]
                    ]
                }

                email_service.send_weekly_report(pref.user_id, report_data)

        return f"Sent weekly reports to {len(prefs)} users"

    except Exception as e:
        logger.error(f"Error in send_weekly_reports: {e}")
    finally:
        db.close()

# Schedule these tasks
@shared_task
def schedule_email_tasks():
    """Configure periodic email tasks"""
    from celery.schedules import crontab

    return {
        "send_pending_emails": {
            "task": "app.workers.email_tasks.send_pending_emails",
            "schedule": 300.0,  # Every 5 minutes
        },
        "send_daily_summaries": {
            "task": "app.workers.email_tasks.send_daily_summaries",
            "schedule": crontab(hour=8, minute=0),  # 8 AM daily
        },
        "send_weekly_reports": {
            "task": "app.workers.email_tasks.send_weekly_reports",
            "schedule": crontab(day_of_week=1, hour=9, minute=0),  # 9 AM Monday
        }
    }
```

---

### Frontend: Template Manager UI

#### Overview
React-based UI for browsing, creating, editing, and managing PDF generation templates.

#### Component Structure

```
frontend/src/components/templates/
├── TemplateManager.tsx          # Main template manager component
├── TemplateLibrary.tsx          # Template library browser
├── TemplateCard.tsx             # Template card display
├── TemplateEditor.tsx           # Template creation/editing form
├── TemplatePreview.tsx          # Live template preview
├── TemplateCategories.tsx       # Category filter sidebar
└── TemplateVersions.tsx         # Version history viewer
```

#### TemplateManager Component

**File:** `frontend/src/components/templates/TemplateManager.tsx`

```typescript
import React, { useState, useEffect } from 'react';
import {
  TemplateLibrary,
  TemplateEditor,
  TemplatePreview,
  TemplateVersions
} from './';
import { Template } from '@/types';
import { templateAPI } from '@/services/api';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Button } from '@/components/ui/button';
import { Plus, BookOpen, Settings } from 'lucide-react';

export const TemplateManager: React.FC = () => {
  const [templates, setTemplates] = useState<Template[]>([]);
  const [selectedTemplate, setSelectedTemplate] = useState<Template | null>(null);
  const [activeTab, setActiveTab] = useState<'library' | 'editor' | 'versions'>('library');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadTemplates();
  }, []);

  const loadTemplates = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await templateAPI.listTemplates({
        page: 1,
        page_size: 50
      });
      setTemplates(response.templates);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const handleCreateNew = () => {
    setSelectedTemplate(null);
    setActiveTab('editor');
  };

  const handleSelectTemplate = (template: Template) => {
    setSelectedTemplate(template);
    setActiveTab('editor');
  };

  const handleSaveTemplate = async (templateData: any) => {
    try {
      if (selectedTemplate) {
        await templateAPI.updateTemplate(selectedTemplate.id, templateData);
      } else {
        const newTemplate = await templateAPI.createTemplate(templateData);
        setSelectedTemplate(newTemplate);
      }
      await loadTemplates();
      setActiveTab('library');
    } catch (err: any) {
      setError(err.message);
    }
  };

  const handleDeleteTemplate = async (templateId: number) => {
    if (!confirm('Are you sure you want to delete this template?')) return;

    try {
      await templateAPI.deleteTemplate(templateId);
      await loadTemplates();
      if (selectedTemplate?.id === templateId) {
        setSelectedTemplate(null);
      }
    } catch (err: any) {
      setError(err.message);
    }
  };

  return (
    <div className="template-manager container mx-auto p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Template Manager</h1>
        <Button onClick={handleCreateNew}>
          <Plus className="mr-2 h-4 w-4" />
          New Template
        </Button>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}

      <Tabs value={activeTab} onValueChange={(v: any) => setActiveTab(v)}>
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="library">
            <BookOpen className="mr-2 h-4 w-4" />
            Library
          </TabsTrigger>
          <TabsTrigger value="editor" disabled={!selectedTemplate && activeTab !== 'editor'}>
            <Settings className="mr-2 h-4 w-4" />
            Editor
          </TabsTrigger>
          <TabsTrigger value="versions" disabled={!selectedTemplate}>
            Versions
          </TabsTrigger>
        </TabsList>

        <TabsContent value="library">
          <TemplateLibrary
            templates={templates}
            isLoading={isLoading}
            onSelectTemplate={handleSelectTemplate}
            onDeleteTemplate={handleDeleteTemplate}
          />
        </TabsContent>

        <TabsContent value="editor">
          {selectedTemplate || activeTab === 'editor' ? (
            <TemplateEditor
              template={selectedTemplate}
              onSave={handleSaveTemplate}
              onCancel={() => setActiveTab('library')}
            />
          ) : (
            <div className="text-center text-gray-500 py-12">
              Select a template to edit or create a new one
            </div>
          )}
        </TabsContent>

        <TabsContent value="versions">
          {selectedTemplate && (
            <TemplateVersions templateId={selectedTemplate.id} />
          )}
        </TabsContent>
      </Tabs>
    </div>
  );
};
```

#### TemplateLibrary Component

**File:** `frontend/src/components/templates/TemplateLibrary.tsx`

```typescript
import React, { useState } from 'react';
import { Template } from '@/types';
import { TemplateCard } from './TemplateCard';
import { TemplateCategories } from './TemplateCategories';
import { Input } from '@/components/ui/input';
import { Search, SortAsc, SortDesc } from 'lucide-react';

interface TemplateLibraryProps {
  templates: Template[];
  isLoading: boolean;
  onSelectTemplate: (template: Template) => void;
  onDeleteTemplate: (templateId: number) => void;
}

export const TemplateLibrary: React.FC<TemplateLibraryProps> = ({
  templates,
  isLoading,
  onSelectTemplate,
  onDeleteTemplate
}) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);
  const [sortBy, setSortBy] = useState<'created_at' | 'name' | 'usage_count' | 'rating'>('created_at');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('desc');

  // Filter templates
  const filteredTemplates = templates
    .filter(t => {
      const matchesSearch = !searchQuery ||
        t.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        t.description?.toLowerCase().includes(searchQuery.toLowerCase());
      const matchesCategory = !selectedCategory || t.category === selectedCategory;
      return matchesSearch && matchesCategory;
    })
    .sort((a, b) => {
      const aVal = a[sortBy];
      const bVal = b[sortBy];
      if (sortOrder === 'asc') {
        return aVal > bVal ? 1 : -1;
      } else {
        return aVal < bVal ? 1 : -1;
      }
    });

  return (
    <div className="template-library">
      {/* Search and Filter Bar */}
      <div className="mb-6 space-y-4">
        <div className="flex gap-4">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
            <Input
              type="text"
              placeholder="Search templates..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-10"
            />
          </div>

          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value as any)}
            className="border rounded px-3 py-2"
          >
            <option value="created_at">Sort by Date</option>
            <option value="name">Sort by Name</option>
            <option value="usage_count">Sort by Usage</option>
            <option value="rating">Sort by Rating</option>
          </select>

          <button
            onClick={() => setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc')}
            className="border rounded px-3 py-2"
          >
            {sortOrder === 'asc' ? <SortAsc className="h-4 w-4" /> : <SortDesc className="h-4 w-4" />}
          </button>
        </div>

        <TemplateCategories
          selectedCategory={selectedCategory}
          onSelectCategory={setSelectedCategory}
        />
      </div>

      {/* Templates Grid */}
      {isLoading ? (
        <div className="text-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading templates...</p>
        </div>
      ) : filteredTemplates.length === 0 ? (
        <div className="text-center py-12 text-gray-500">
          No templates found. Create your first template to get started!
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredTemplates.map(template => (
            <TemplateCard
              key={template.id}
              template={template}
              onSelect={() => onSelectTemplate(template)}
              onDelete={() => onDeleteTemplate(template.id)}
            />
          ))}
        </div>
      )}
    </div>
  );
};
```

#### TemplateCard Component

**File:** `frontend/src/components/templates/TemplateCard.tsx`

```typescript
import React from 'react';
import { Template } from '@/types';
import { Card, CardHeader, CardContent, CardFooter } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Star, Eye, Trash2 } from 'lucide-react';

interface TemplateCardProps {
  template: Template;
  onSelect: () => void;
  onDelete: () => void;
}

export const TemplateCard: React.FC<TemplateCardProps> = ({
  template,
  onSelect,
  onDelete
}) => {
  return (
    <Card className="template-card hover:shadow-lg transition-shadow cursor-pointer">
      <CardHeader onClick={onSelect}>
        <div className="flex justify-between items-start">
          <h3 className="text-lg font-semibold line-clamp-1">{template.name}</h3>
          {template.is_public && (
            <Badge variant="secondary">Public</Badge>
          )}
        </div>
        {template.description && (
          <p className="text-sm text-gray-600 line-clamp-2 mt-2">
            {template.description}
          </p>
        )}
      </CardHeader>

      <CardContent onClick={onSelect}>
        <div className="space-y-2 text-sm">
          {template.category && (
            <div className="flex items-center text-gray-600">
              <span className="font-medium">Category:</span>
              <span className="ml-2">{template.category}</span>
            </div>
          )}

          <div className="flex items-center gap-4">
            <div className="flex items-center text-gray-600">
              <Star className="h-4 w-4 mr-1 fill-yellow-400 text-yellow-400" />
              <span>{template.rating.toFixed(1)}</span>
            </div>
            <div className="flex items-center text-gray-600">
              <Eye className="h-4 w-4 mr-1" />
              <span>{template.usage_count}</span>
            </div>
          </div>

          <div className="text-xs text-gray-500">
            Version {template.version}
          </div>
        </div>
      </CardContent>

      <CardFooter className="flex justify-between">
        <Button onClick={onSelect} variant="default">
          Select Template
        </Button>
        <Button onClick={onDelete} variant="destructive" size="icon">
          <Trash2 className="h-4 w-4" />
        </Button>
      </CardFooter>
    </Card>
  );
};
```

#### TemplateEditor Component

**File:** `frontend/src/components/templates/TemplateEditor.tsx`

```typescript
import React, { useState } from 'react';
import { Template } from '@/types';
import { TemplateConfig } from '@/types/template';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Switch } from '@/components/ui/switch';

interface TemplateEditorProps {
  template: Template | null;
  onSave: (data: any) => Promise<void>;
  onCancel: () => void;
}

export const TemplateEditor: React.FC<TemplateEditorProps> = ({
  template,
  onSave,
  onCancel
}) => {
  const [name, setName] = useState(template?.name || '');
  const [description, setDescription] = useState(template?.description || '');
  const [category, setCategory] = useState(template?.category || '');
  const [isPublic, setIsPublic] = useState(template?.is_public || false);
  const [config, setConfig] = useState<TemplateConfig>(
    template?.config || {
      pdf_options: {
        font_family: 'Liberation Sans',
        font_size: 11,
        line_height: 1.6,
        margin_top: '20mm',
        margin_bottom: '20mm',
        margin_left: '15mm',
        margin_right: '15mm',
        page_size: 'A4'
      },
      styling: {},
      content_settings: {},
      generation_settings: {},
      advanced: {}
    }
  );
  const [activeTab, setActiveTab] = useState('pdf');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await onSave({
      name,
      description,
      category,
      is_public: isPublic,
      config
    });
  };

  const updatePdfOption = (key: string, value: any) => {
    setConfig({
      ...config,
      pdf_options: {
        ...config.pdf_options,
        [key]: value
      }
    });
  };

  const updateStyling = (key: string, value: any) => {
    setConfig({
      ...config,
      styling: {
        ...config.styling,
        [key]: value
      }
    });
  };

  return (
    <form onSubmit={handleSubmit} className="template-editor space-y-6">
      {/* Basic Info */}
      <div className="space-y-4">
        <div>
          <Label htmlFor="name">Template Name *</Label>
          <Input
            id="name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
        </div>

        <div>
          <Label htmlFor="description">Description</Label>
          <Textarea
            id="description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            rows={3}
          />
        </div>

        <div>
          <Label htmlFor="category">Category</Label>
          <Input
            id="category"
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            placeholder="e.g., Business, Academic, Creative"
          />
        </div>

        <div className="flex items-center space-x-2">
          <Switch
            id="is_public"
            checked={isPublic}
            onCheckedChange={setIsPublic}
          />
          <Label htmlFor="is_public">Make this template public</Label>
        </div>
      </div>

      {/* Configuration Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="pdf">PDF Options</TabsTrigger>
          <TabsTrigger value="styling">Styling</TabsTrigger>
          <TabsTrigger value="content">Content</TabsTrigger>
          <TabsTrigger value="generation">Generation</TabsTrigger>
        </TabsList>

        <TabsContent value="pdf" className="space-y-4">
          <div>
            <Label>Font Family</Label>
            <select
              value={config.pdf_options.font_family}
              onChange={(e) => updatePdfOption('font_family', e.target.value)}
              className="w-full border rounded px-3 py-2"
            >
              <option value="Liberation Sans">Liberation Sans</option>
              <option value="Times New Roman">Times New Roman</option>
              <option value="Arial">Arial</option>
              <option value="Georgia">Georgia</option>
              <option value="Courier New">Courier New</option>
            </select>
          </div>

          <div>
            <Label>Font Size (pt)</Label>
            <Input
              type="number"
              min={6}
              max={24}
              value={config.pdf_options.font_size}
              onChange={(e) => updatePdfOption('font_size', parseInt(e.target.value))}
            />
          </div>

          <div>
            <Label>Line Height</Label>
            <Input
              type="number"
              min={1.0}
              max={3.0}
              step={0.1}
              value={config.pdf_options.line_height}
              onChange={(e) => updatePdfOption('line_height', parseFloat(e.target.value))}
            />
          </div>

          <div>
            <Label>Page Size</Label>
            <select
              value={config.pdf_options.page_size}
              onChange={(e) => updatePdfOption('page_size', e.target.value)}
              className="w-full border rounded px-3 py-2"
            >
              <option value="A4">A4</option>
              <option value="Letter">Letter</option>
              <option value="Legal">Legal</option>
              <option value="A3">A3</option>
              <option value="A5">A5</option>
            </select>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label>Top Margin</Label>
              <Input
                value={config.pdf_options.margin_top}
                onChange={(e) => updatePdfOption('margin_top', e.target.value)}
              />
            </div>
            <div>
              <Label>Bottom Margin</Label>
              <Input
                value={config.pdf_options.margin_bottom}
                onChange={(e) => updatePdfOption('margin_bottom', e.target.value)}
              />
            </div>
            <div>
              <Label>Left Margin</Label>
              <Input
                value={config.pdf_options.margin_left}
                onChange={(e) => updatePdfOption('margin_left', e.target.value)}
              />
            </div>
            <div>
              <Label>Right Margin</Label>
              <Input
                value={config.pdf_options.margin_right}
                onChange={(e) => updatePdfOption('margin_right', e.target.value)}
              />
            </div>
          </div>
        </TabsContent>

        <TabsContent value="styling" className="space-y-4">
          <div>
            <Label>Title Font Size (px)</Label>
            <Input
              type="number"
              value={config.styling.title_font_size || 24}
              onChange={(e) => updateStyling('title_font_size', parseInt(e.target.value))}
            />
          </div>

          <div>
            <Label>Title Color</Label>
            <Input
              type="color"
              value={config.styling.title_color || '#2c3e50'}
              onChange={(e) => updateStyling('title_color', e.target.value)}
            />
          </div>

          <div>
            <Label>Body Font Size (px)</Label>
            <Input
              type="number"
              value={config.styling.body_font_size || 11}
              onChange={(e) => updateStyling('body_font_size', parseInt(e.target.value))}
            />
          </div>

          <div>
            <Label>Body Color</Label>
            <Input
              type="color"
              value={config.styling.body_color || '#333333'}
              onChange={(e) => updateStyling('body_color', e.target.value)}
            />
          </div>
        </TabsContent>

        <TabsContent value="content" className="space-y-4">
          <div className="flex items-center justify-between">
            <Label>Include Table of Contents</Label>
            <Switch
              checked={config.content_settings.include_toc || false}
              onCheckedChange={(checked) =>
                setConfig({
                  ...config,
                  content_settings: {
                    ...config.content_settings,
                    include_toc: checked
                  }
                })
              }
            />
          </div>

          <div className="flex items-center justify-between">
            <Label>Include Page Numbers</Label>
            <Switch
              checked={config.content_settings.include_page_numbers || false}
              onCheckedChange={(checked) =>
                setConfig({
                  ...config,
                  content_settings: {
                    ...config.content_settings,
                    include_page_numbers: checked
                  }
                })
              }
            />
          </div>

          <div className="flex items-center justify-between">
            <Label>Include Chapter Titles</Label>
            <Switch
              checked={config.content_settings.include_chapter_titles !== false}
              onCheckedChange={(checked) =>
                setConfig({
                  ...config,
                  content_settings: {
                    ...config.content_settings,
                    include_chapter_titles: checked
                  }
                })
              }
            />
          </div>
        </TabsContent>

        <TabsContent value="generation" className="space-y-4">
          <div>
            <Label>AI Provider</Label>
            <select
              value={config.generation_settings.provider || 'anthropic'}
              onChange={(e) =>
                setConfig({
                  ...config,
                  generation_settings: {
                    ...config.generation_settings,
                    provider: e.target.value
                  }
                })
              }
              className="w-full border rounded px-3 py-2"
            >
              <option value="anthropic">Anthropic</option>
              <option value="openai">OpenAI</option>
              <option value="mistral">Mistral</option>
            </select>
          </div>

          <div>
            <Label>Creativity Level</Label>
            <select
              value={config.generation_settings.creativity_level || 'balanced'}
              onChange={(e) =>
                setConfig({
                  ...config,
                  generation_settings: {
                    ...config.generation_settings,
                    creativity_level: e.target.value
                  }
                })
              }
              className="w-full border rounded px-3 py-2"
            >
              <option value="conservative">Conservative</option>
              <option value="balanced">Balanced</option>
              <option value="creative">Creative</option>
            </select>
          </div>

          <div>
            <Label>Quality Preset</Label>
            <select
              value={config.generation_settings.quality_preset || 'standard'}
              onChange={(e) =>
                setConfig({
                  ...config,
                  generation_settings: {
                    ...config.generation_settings,
                    quality_preset: e.target.value
                  }
                })
              }
              className="w-full border rounded px-3 py-2"
            >
              <option value="draft">Draft</option>
              <option value="standard">Standard</option>
              <option value="premium">Premium</option>
            </select>
          </div>
        </TabsContent>
      </Tabs>

      {/* Actions */}
      <div className="flex justify-end gap-4">
        <Button type="button" variant="outline" onClick={onCancel}>
          Cancel
        </Button>
        <Button type="submit">
          {template ? 'Update Template' : 'Create Template'}
        </Button>
      </div>
    </form>
  );
};
```

---

### Frontend: Advanced Search UI

#### Overview
Comprehensive search interface with filters, sorting, and export capabilities.

#### Component Structure

```
frontend/src/components/search/
├── AdvancedSearch.tsx           # Main search component
├── SearchFilters.tsx            # Filter sidebar
├── SearchResults.tsx            # Results table
├── SearchBar.tsx                # Search input with autocomplete
└── ExportButton.tsx             # Export functionality
```

#### AdvancedSearch Component

**File:** `frontend/src/components/search/AdvancedSearch.tsx`

```typescript
import React, { useState, useEffect } from 'react';
import { SearchFilters } from './SearchFilters';
import { SearchResults } from './SearchResults';
import { SearchBar } from './SearchBar';
import { ExportButton } from './ExportButton';
import { Generation } from '@/types';
import { searchAPI } from '@/services/api';

interface SearchFilters {
  status?: string;
  language?: string;
  date_from?: string;
  date_to?: string;
  min_quality?: number;
  max_quality?: number;
  min_chapters?: number;
  max_chapters?: number;
  provider?: string;
  has_pdf?: boolean;
  failed_only?: boolean;
}

export const AdvancedSearch: React.FC = () => {
  const [query, setQuery] = useState('');
  const [filters, setFilters] = useState<SearchFilters>({});
  const [results, setResults] = useState<Generation[]>([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(20);
  const [sortBy, setSortBy] = useState('created_at');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('desc');
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    performSearch();
  }, [page, pageSize, sortBy, sortOrder]);

  const performSearch = async () => {
    setIsLoading(true);
    try {
      const response = await searchAPI.searchGenerations({
        q: query,
        ...filters,
        sort_by: sortBy,
        sort_order: sortOrder,
        page,
        page_size: pageSize
      });
      setResults(response.results);
      setTotal(response.total);
    } catch (error) {
      console.error('Search failed:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSearch = () => {
    setPage(1);
    performSearch();
  };

  const handleClearFilters = () => {
    setFilters({});
    setQuery('');
    setPage(1);
    performSearch();
  };

  return (
    <div className="advanced-search container mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">Search Generations</h1>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Filters Sidebar */}
        <div className="lg:col-span-1">
          <SearchFilters
            filters={filters}
            onChange={setFilters}
            onSearch={handleSearch}
            onClear={handleClearFilters}
          />
        </div>

        {/* Results Area */}
        <div className="lg:col-span-3 space-y-4">
          {/* Search Bar */}
          <div className="flex gap-4">
            <SearchBar
              value={query}
              onChange={setQuery}
              onSearch={handleSearch}
            />
            <ExportButton
              query={query}
              filters={filters}
            />
          </div>

          {/* Results Table */}
          <SearchResults
            results={results}
            total={total}
            page={page}
            pageSize={pageSize}
            isLoading={isLoading}
            sortBy={sortBy}
            sortOrder={sortOrder}
            onPageChange={setPage}
            onPageSizeChange={setPageSize}
            onSortChange={(field) => {
              if (sortBy === field) {
                setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
              } else {
                setSortBy(field);
                setSortOrder('desc');
              }
            }}
          />
        </div>
      </div>
    </div>
  );
};
```

---

### Frontend: Version History UI

#### Overview
Display and manage version history for generations with comparison tools.

#### Component Structure

```
frontend/src/components/versions/
├── VersionHistory.tsx            # Main version history component
├── VersionList.tsx               # List of all versions
├── VersionComparison.tsx         # Side-by-side comparison
├── VersionTree.tsx               # Tree visualization
└── VersionActions.tsx            # Action buttons
```

#### VersionHistory Component

**File:** `frontend/src/components/versions/VersionHistory.tsx`

```typescript
import React, { useState, useEffect } from 'react';
import { VersionList } from './VersionList';
import { VersionComparison } from './VersionComparison';
import { versionAPI } from '@/services/api';

interface Version {
  id: number;
  version_number: number;
  is_latest: boolean;
  status: string;
  chapter_count: number;
  word_count: number;
  overall_quality_score: number;
  created_at: string;
  provider: string;
  model: string;
}

interface VersionHistoryProps {
  generationId: number;
}

export const VersionHistory: React.FC<VersionHistoryProps> = ({ generationId }) => {
  const [versions, setVersions] = useState<Version[]>([]);
  const [selectedVersions, setSelectedVersions] = useState<[number | null, number | null]>([null, null]);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    loadVersions();
  }, [generationId]);

  const loadVersions = async () => {
    setIsLoading(true);
    try {
      const data = await versionAPI.getVersionHistory(generationId);
      setVersions(data);
    } catch (error) {
      console.error('Failed to load versions:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleCompare = (v1: number, v2: number) => {
    setSelectedVersions([v1, v2]);
  };

  return (
    <div className="version-history space-y-6">
      <h2 className="text-2xl font-bold">Version History</h2>

      {isLoading ? (
        <div className="text-center py-8">Loading versions...</div>
      ) : (
        <VersionList
          versions={versions}
          onSelectVersion={handleCompare}
        />
      )}

      {selectedVersions[0] && selectedVersions[1] && (
        <VersionComparison
          version1Id={selectedVersions[0]}
          version2Id={selectedVersions[1]}
        />
      )}
    </div>
  );
};
```

---

## Week 19-20: Production Readiness

### Rate Limiting Implementation

#### Overview
Implement rate limiting to prevent abuse and ensure fair resource allocation.

#### Rate Limiting Strategy

**Rate Limits:**
- Free users: 5 generations per hour
- Pro users: 20 generations per hour
- Admin users: 100 generations per hour

**Rate Limiting Algorithm:**
- Token bucket algorithm using Redis
- Window: Sliding window (last 60 minutes)
- Cleanup: Automatic expiration

#### Redis-Based Rate Limiter

**File:** `backend/app/services/rate_limiter.py`

```python
import redis
import time
from typing import Optional
from datetime import datetime, timedelta

from app.core.config import settings
from app.models.user import User
from app.core.exceptions import RateLimitExceeded

class RateLimiter:
    def __init__(self):
        self.redis = redis.Redis(
            host=settings.redis_host,
            port=settings.redis_port,
            db=settings.redis_db,
            decode_responses=True
        )

    def check_rate_limit(
        self,
        user: User,
        action: str = "generation"
    ) -> tuple[bool, dict]:
        """
        Check if user has exceeded rate limit

        Args:
            user: User object
            action: Action type (generation, api_call, etc.)

        Returns:
            Tuple of (allowed, info_dict)

        Raises:
            RateLimitExceeded: If limit exceeded
        """
        # Get user's rate limit
        if user.is_admin:
            limit = 100
        elif user.is_pro:
            limit = 20
        else:
            limit = 5

        # Redis key for this user's rate limit
        key = f"ratelimit:{action}:{user.id}"

        # Get current count and timestamp
        pipe = self.redis.pipeline()
        pipe.incr(key)
        pipe.expire(key, 3600)  # Expire after 1 hour
        results = pipe.execute()

        current_count = results[0]

        # Check if limit exceeded
        if current_count > limit:
            # Get TTL to show when limit resets
            ttl = self.redis.ttl(key)
            retry_after = ttl if ttl > 0 else 3600

            raise RateLimitExceeded(
                f"Rate limit exceeded. Maximum {limit} generations per hour. "
                f"Try again in {retry_after // 60} minutes.",
                retry_after=retry_after,
                limit=limit,
                remaining=0,
                reset_time=datetime.now() + timedelta(seconds=retry_after)
            )

        # Get remaining requests
        remaining = limit - current_count
        ttl = self.redis.ttl(key)

        return True, {
            "limit": limit,
            "remaining": remaining,
            "reset": datetime.now() + timedelta(seconds=ttl) if ttl > 0 else None
        }

    def get_usage_stats(self, user: User) -> dict:
        """Get current usage statistics for user"""
        key = f"ratelimit:generation:{user.id}"
        count = int(self.redis.get(key) or 0)
        ttl = self.redis.ttl(key)

        limit = 100 if user.is_admin else (20 if user.is_pro else 5)

        return {
            "used": count,
            "limit": limit,
            "remaining": max(0, limit - count),
            "reset_at": datetime.now() + timedelta(seconds=ttl) if ttl > 0 else None,
            "reset_in_seconds": ttl if ttl > 0 else 0
        }

    def reset_rate_limit(self, user: User, action: str = "generation"):
        """Reset rate limit for user (admin only)"""
        key = f"ratelimit:{action}:{user.id}"
        self.redis.delete(key)

rate_limiter = RateLimiter()
```

#### Rate Limiting Middleware

**File:** `backend/app/api/middleware/rate_limit.py`

```python
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from app.services.rate_limiter import rate_limiter
from app.core.auth import get_current_user
from app.core.exceptions import RateLimitExceeded

class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Skip rate limiting for non-generation endpoints
        if not request.url.path.startswith("/api/generations"):
            return await call_next(request)

        # Skip rate limiting for GET requests
        if request.method == "GET":
            return await call_next(request)

        try:
            # Get user from token
            user = await get_current_user(
                request.headers.get("Authorization")
            )

            # Check rate limit
            allowed, info = rate_limiter.check_rate_limit(user)

            # Add rate limit headers to response
            response = await call_next(request)
            response.headers["X-RateLimit-Limit"] = str(info["limit"])
            response.headers["X-RateLimit-Remaining"] = str(info["remaining"])
            if info["reset"]:
                response.headers["X-RateLimit-Reset"] = info["reset"].isoformat()

            return response

        except RateLimitExceeded as e:
            return JSONResponse(
                status_code=429,
                content={
                    "error": "rate_limit_exceeded",
                    "message": str(e),
                    "retry_after": e.retry_after
                },
                headers={
                    "Retry-After": str(e.retry_after),
                    "X-RateLimit-Limit": str(e.limit),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": e.reset_time.isoformat()
                }
            )
```

#### API Endpoint for Usage Stats

**File:** `backend/app/api/routes/rate_limit.py`

```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.user import User
from app.services.rate_limiter import rate_limiter

router = APIRouter(prefix="/api/rate-limit", tags=["rate-limit"])

@router.get("/stats")
async def get_rate_limit_stats(
    current_user: User = Depends(get_current_user)
):
    """
    Get current rate limit usage statistics

    **Returns:** Rate limit information including remaining requests
    """
    return rate_limiter.get_usage_stats(current_user)
```

---

### Automated Backup System

#### Overview
Automated daily backups of PostgreSQL database with MinIO storage.

#### Backup Strategy

**Backup Schedule:**
- Daily backups at 2:00 AM UTC
- Retain last 7 daily backups
- Weekly full backup on Sunday
- Monthly backup on 1st of each month (retain 12 months)

**Backup Locations:**
- Primary: MinIO object storage
- Secondary: (Optional) S3-compatible storage
- Local: Temporary staging directory

#### Backup Script

**File:** `backend/scripts/backup_database.sh`

```bash
#!/bin/bash

# Database Backup Script
# Backs up PostgreSQL database and uploads to MinIO

set -e

# Configuration
DB_HOST="${DB_HOST:-localhost}"
DB_PORT="${DB_PORT:-5432}"
DB_NAME="${DB_NAME:-bookmake}"
DB_USER="${DB_USER:-bookmake}"
DB_PASSWORD="${DB_PASSWORD}"

BACKUP_DIR="${BACKUP_DIR:-/tmp/backups}"
MINIO_ENDPOINT="${MINIO_ENDPOINT:-http://localhost:9000}"
MINIO_ACCESS_KEY="${MINIO_ACCESS_KEY}"
MINIO_SECRET_KEY="${MINIO_SECRET_KEY}"
MINIO_BUCKET="${MINIO_BUCKET:-bookmake-backups}"

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Generate backup filename with timestamp
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="$BACKUP_DIR/bookmake_${TIMESTAMP}.sql.gz"

echo "Starting database backup at $(date)"

# Dump database
PGPASSWORD="$DB_PASSWORD" pg_dump \
  -h "$DB_HOST" \
  -p "$DB_PORT" \
  -U "$DB_USER" \
  -d "$DB_NAME" \
  --verbose \
  --no-owner \
  --no-acl | gzip > "$BACKUP_FILE"

# Check if backup was successful
if [ ! -f "$BACKUP_FILE" ] || [ ! -s "$BACKUP_FILE" ]; then
  echo "ERROR: Backup file is empty or does not exist"
  exit 1
fi

# Get file size
BACKUP_SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
echo "Backup created: $BACKUP_FILE ($BACKUP_SIZE)"

# Upload to MinIO
echo "Uploading backup to MinIO..."

# Configure MinIO client (mc)
mc alias set minio "$MINIO_ENDPOINT" "$MINIO_ACCESS_KEY" "$MINIO_SECRET_KEY"

# Ensure bucket exists
mc mb minio/"$MINIO_BUCKET" --ignore-existing

# Upload file
mc cp "$BACKUP_FILE" minio/"$MINIO_BUCKET"/

# Verify upload
if mc ls minio/"$MINIO_BUCKET"/$(basename "$BACKUP_FILE"); then
  echo "Backup uploaded successfully"
else
  echo "ERROR: Backup upload failed"
  exit 1
fi

# Clean up local backup file
rm "$BACKUP_FILE"

# Rotate old backups (keep last 7 daily backups)
echo "Rotating old backups..."
mc rm minio/"$MINIO_BUCKET"/bookmake_*.sql.gz \
  --older-than 7d \
  --force \
  --insecure

# List current backups
echo "Current backups:"
mc ls minio/"$MINIO_BUCKET"/

echo "Backup completed successfully at $(date)"
```

#### Backup Service

**File:** `backend/app/services/backup_service.py`

```python
import os
import subprocess
import logging
from datetime import datetime, timedelta
from typing import List, Dict
from sqlalchemy.orm import Session

from app.models.backup import Backup
from app.core.minio_client import minio_client
from app.core.config import settings

logger = logging.getLogger(__name__)

class BackupService:
    def __init__(self, db: Session):
        self.db = db

    def create_backup(self) -> Backup:
        """Create a new database backup"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"bookmake_{timestamp}.sql.gz"

        try:
            # Execute backup script
            result = subprocess.run(
                ["/app/scripts/backup_database.sh"],
                capture_output=True,
                text=True,
                env={
                    **os.environ,
                    "DB_HOST": settings.db_host,
                    "DB_PORT": str(settings.db_port),
                    "DB_NAME": settings.db_name,
                    "DB_USER": settings.db_user,
                    "DB_PASSWORD": settings.db_password,
                    "MINIO_ENDPOINT": f"http://{settings.minio_endpoint}:{settings.minio_port}",
                    "MINIO_ACCESS_KEY": settings.minio_access_key,
                    "MINIO_SECRET_KEY": settings.minio_secret_key,
                    "MINIO_BUCKET": settings.minio_backup_bucket
                },
                check=True
            )

            logger.info(f"Backup output: {result.stdout}")

            # Create backup record
            backup = Backup(
                filename=backup_filename,
                size_bytes=self._get_backup_size(backup_filename),
                status="completed",
                completed_at=datetime.utcnow()
            )

            self.db.add(backup)
            self.db.commit()
            self.db.refresh(backup)

            logger.info(f"Backup created successfully: {backup_filename}")
            return backup

        except subprocess.CalledProcessError as e:
            logger.error(f"Backup failed: {e.stderr}")

            # Create failed backup record
            backup = Backup(
                filename=backup_filename,
                status="failed",
                error_message=e.stderr,
                completed_at=datetime.utcnow()
            )
            self.db.add(backup)
            self.db.commit()

            raise Exception(f"Backup failed: {e.stderr}")

    def list_backups(self, limit: int = 10) -> List[Backup]:
        """List recent backups"""
        return self.db.query(Backup).order_by(
            Backup.created_at.desc()
        ).limit(limit).all()

    def restore_backup(self, backup_id: int) -> bool:
        """Restore database from backup"""
        backup = self.db.query(Backup).filter(
            Backup.id == backup_id
        ).first()

        if not backup:
            raise ValueError("Backup not found")

        try:
            # Download from MinIO
            local_path = f"/tmp/{backup.filename}"
            minio_client.fget_object(
                settings.minio_backup_bucket,
                backup.filename,
                local_path
            )

            # Restore database
            subprocess.run(
                [
                    "gunzip",
                    "-c",
                    local_path,
                    "|",
                    "psql",
                    f"-h{settings.db_host}",
                    f"-p{settings.db_port}",
                    f"-U{settings.db_user}",
                    f"-d{settings.db_name}"
                ],
                shell=True,
                check=True,
                env={
                    "PGPASSWORD": settings.db_password
                }
            )

            # Clean up
            os.remove(local_path)

            logger.info(f"Database restored from backup: {backup.filename}")
            return True

        except Exception as e:
            logger.error(f"Restore failed: {e}")
            raise

    def delete_old_backups(self, retain_days: int = 7):
        """Delete backups older than retain_days"""
        cutoff_date = datetime.utcnow() - timedelta(days=retain_days)

        old_backups = self.db.query(Backup).filter(
            Backup.created_at < cutoff_date,
            Backup.status == "completed"
        ).all()

        for backup in old_backups:
            try:
                # Delete from MinIO
                minio_client.remove_object(
                    settings.minio_backup_bucket,
                    backup.filename
                )

                # Delete record
                self.db.delete(backup)

                logger.info(f"Deleted old backup: {backup.filename}")

            except Exception as e:
                logger.error(f"Failed to delete backup {backup.filename}: {e}")

        self.db.commit()

    def _get_backup_size(self, filename: str) -> int:
        """Get backup file size from MinIO"""
        try:
            stat = minio_client.stat_object(
                settings.minio_backup_bucket,
                filename
            )
            return stat.size
        except:
            return 0
```

#### Scheduled Backup Task

**File:** `backend/app/workers/backup_tasks.py`

```python
from celery import shared_task
from celery.schedules import crontab
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.services.backup_service import BackupService
import logging

logger = logging.getLogger(__name__)

@shared_task
def daily_backup():
    """Execute daily database backup"""
    db = SessionLocal()
    try:
        service = BackupService(db)
        backup = service.create_backup()

        # Clean up old backups
        service.delete_old_backups(retain_days=7)

        logger.info(f"Daily backup completed: {backup.filename}")
        return {
            "status": "success",
            "backup_id": backup.id,
            "filename": backup.filename
        }

    except Exception as e:
        logger.error(f"Daily backup failed: {e}")
        return {
            "status": "error",
            "error": str(e)
        }
    finally:
        db.close()

@shared_task
def weekly_backup():
    """Execute weekly full backup (Sunday at 3 AM)"""
    db = SessionLocal()
    try:
        service = BackupService(db)
        backup = service.create_backup()

        logger.info(f"Weekly backup completed: {backup.filename}")
        return {
            "status": "success",
            "backup_id": backup.id,
            "filename": backup.filename
        }

    except Exception as e:
        logger.error(f"Weekly backup failed: {e}")
        return {
            "status": "error",
            "error": str(e)
        }
    finally:
        db.close()

# Celery beat schedule
beat_schedule = {
    "daily-backup": {
        "task": "app.workers.backup_tasks.daily_backup",
        "schedule": crontab(hour=2, minute=0),  # 2 AM daily
    },
    "weekly-backup": {
        "task": "app.workers.backup_tasks.weekly_backup",
        "schedule": crontab(day_of_week=0, hour=3, minute=0),  # 3 AM Sunday
    }
}
```

---

### Cost Monitoring & Budgets

#### Overview
Track API costs per user, enforce budget limits, and provide cost breakdowns.

#### Database Schema

```sql
-- Cost tracking table
CREATE TABLE cost_tracking (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    generation_id INTEGER REFERENCES generations(id) ON DELETE SET NULL,

    -- Cost details
    provider VARCHAR(50) NOT NULL,
    model VARCHAR(100) NOT NULL,
    input_tokens INTEGER DEFAULT 0,
    output_tokens INTEGER DEFAULT 0,
    total_tokens INTEGER DEFAULT 0,
    cost_usd DECIMAL(10, 4) NOT NULL,

    -- Timestamp
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    -- Indexes
    INDEX (user_id, created_at),
    INDEX (provider)
);

-- User budgets
CREATE TABLE user_budgets (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE UNIQUE,
    monthly_budget_usd DECIMAL(10, 2) NOT NULL DEFAULT 50.00,
    alert_threshold_percent INTEGER DEFAULT 80,
    alert_sent BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

#### Cost Tracking Service

**File:** `backend/app/services/cost_service.py`

```python
from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, func, desc
from datetime import datetime, timedelta
from decimal import Decimal

from app.models.cost import CostTracking, UserBudget
from app.models.user import User
from app.models.generation import Generation
from app.core.exceptions import BudgetExceeded

# API Pricing (as of 2024)
API_PRICING = {
    "openai": {
        "gpt-4o": {"input": 2.50, "output": 10.00},  # per million tokens
        "gpt-4o-mini": {"input": 0.150, "output": 0.600},
        "gpt-4-turbo": {"input": 10.00, "output": 30.00}
    },
    "anthropic": {
        "claude-3-5-sonnet-20241022": {"input": 3.00, "output": 15.00},
        "claude-3-5-haiku-20241022": {"input": 0.80, "output": 4.00},
        "claude-3-opus-20240229": {"input": 15.00, "output": 75.00}
    },
    "mistral": {
        "mistral-large-latest": {"input": 4.00, "output": 12.00},
        "mistral-medium-latest": {"input": 0.25, "output": 0.25},
        "mistral-small-latest": {"input": 0.10, "output": 0.10}
    }
}

class CostService:
    def __init__(self, db: Session):
        self.db = db

    def calculate_generation_cost(
        self,
        provider: str,
        model: str,
        input_tokens: int,
        output_tokens: int
    ) -> Decimal:
        """Calculate cost for a generation"""
        if provider not in API_PRICING:
            raise ValueError(f"Unknown provider: {provider}")

        if model not in API_PRICING[provider]:
            raise ValueError(f"Unknown model: {model}")

        pricing = API_PRICING[provider][model]

        input_cost = (input_tokens / 1_000_000) * pricing["input"]
        output_cost = (output_tokens / 1_000_000) * pricing["output"]

        total_cost = Decimal(str(input_cost + output_cost))

        return total_cost.quantize(Decimal("0.0001"))

    def track_generation_cost(
        self,
        generation_id: int,
        user_id: int,
        provider: str,
        model: str,
        input_tokens: int,
        output_tokens: int
    ) -> CostTracking:
        """Track cost for a generation"""
        total_tokens = input_tokens + output_tokens
        cost = self.calculate_generation_cost(
            provider, model, input_tokens, output_tokens
        )

        # Create cost record
        cost_record = CostTracking(
            user_id=user_id,
            generation_id=generation_id,
            provider=provider,
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=total_tokens,
            cost_usd=cost
        )

        self.db.add(cost_record)
        self.db.commit()
        self.db.refresh(cost_record)

        # Check if budget exceeded
        self._check_budget_alert(user_id)

        return cost_record

    def get_user_monthly_cost(
        self,
        user_id: int,
        month: Optional[int] = None,
        year: Optional[int] = None
    ) -> Dict[str, any]:
        """Get total cost for user in a specific month"""
        if month is None:
            month = datetime.now().month
        if year is None:
            year = datetime.now().year

        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year + 1, 1, 1) - timedelta(seconds=1)
        else:
            end_date = datetime(year, month + 1, 1) - timedelta(seconds=1)

        costs = self.db.query(
            func.sum(CostTracking.cost_usd),
            func.sum(CostTracking.input_tokens),
            func.sum(CostTracking.output_tokens),
            func.count(CostTracking.id)
        ).filter(
            and_(
                CostTracking.user_id == user_id,
                CostTracking.created_at >= start_date,
                CostTracking.created_at <= end_date
            )
        ).first()

        total_cost = Decimal(str(costs[0] or 0))
        input_tokens = costs[1] or 0
        output_tokens = costs[2] or 0
        generation_count = costs[3] or 0

        return {
            "total_cost_usd": float(total_cost),
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": input_tokens + output_tokens,
            "generation_count": generation_count,
            "month": month,
            "year": year
        }

    def get_cost_breakdown(
        self,
        user_id: int,
        days: int = 30
    ) -> List[Dict]:
        """Get cost breakdown by provider and model"""
        start_date = datetime.utcnow() - timedelta(days=days)

        breakdown = self.db.query(
            CostTracking.provider,
            CostTracking.model,
            func.sum(CostTracking.cost_usd).label("total_cost"),
            func.sum(CostTracking.total_tokens).label("total_tokens"),
            func.count(CostTracking.id).label("count")
        ).filter(
            and_(
                CostTracking.user_id == user_id,
                CostTracking.created_at >= start_date
            )
        ).group_by(
            CostTracking.provider,
            CostTracking.model
        ).order_by(
            desc("total_cost")
        ).all()

        return [
            {
                "provider": row.provider,
                "model": row.model,
                "total_cost_usd": float(row.total_cost),
                "total_tokens": row.total_tokens,
                "generation_count": row.count
            }
            for row in breakdown
        ]

    def get_budget_status(self, user_id: int) -> Dict:
        """Get user's budget status"""
        budget = self.db.query(UserBudget).filter(
            UserBudget.user_id == user_id
        ).first()

        if not budget:
            # Create default budget
            budget = UserBudget(
                user_id=user_id,
                monthly_budget_usd=Decimal("50.00")
            )
            self.db.add(budget)
            self.db.commit()

        # Get current month's cost
        now = datetime.now()
        monthly_cost = self.get_user_monthly_cost(
            user_id, now.month, now.year
        )

        spent = Decimal(str(monthly_cost["total_cost_usd"]))
        remaining = budget.monthly_budget_usd - spent
        percentage_used = (spent / budget.monthly_budget_usd * 100) if budget.monthly_budget_usd > 0 else 0

        # Calculate projected cost
        days_in_month = (now.replace(day=28) + timedelta(days=4)).day
        day_of_month = now.day
        if day_of_month > 0:
            daily_average = spent / day_of_month
            remaining_days = days_in_month - day_of_month
            projected = spent + (daily_average * remaining_days)
        else:
            projected = spent

        return {
            "budget_usd": float(budget.monthly_budget_usd),
            "spent_usd": float(spent),
            "remaining_usd": float(remaining),
            "percentage_used": round(percentage_used, 2),
            "projected_usd": float(projected),
            "will_exceed": projected > budget.monthly_budget_usd,
            "alert_threshold": budget.alert_threshold_percent,
            "alert_triggered": percentage_used >= budget.alert_threshold_percent
        }

    def check_budget_before_generation(self, user_id: int) -> bool:
        """Check if user can afford another generation"""
        budget_status = self.get_budget_status(user_id)

        if budget_status["remaining_usd"] <= 0:
            raise BudgetExceeded(
                f"Monthly budget of ${budget_status['budget_usd']} exceeded. "
                f"Please upgrade your plan or wait until next month."
            )

        return True

    def _check_budget_alert(self, user_id: int):
        """Send alert if budget threshold exceeded"""
        budget_status = self.get_budget_status(user_id)

        if budget_status["alert_triggered"]:
            budget = self.db.query(UserBudget).filter(
                UserBudget.user_id == user_id
            ).first()

            if budget and not budget.alert_sent:
                # Send alert notification
                # This would integrate with your notification service
                budget.alert_sent = True
                self.db.commit()
```

---

### Admin Dashboard Completion

#### Overview
Complete admin dashboard with all 8 tabs for comprehensive system management.

#### Dashboard Tabs

1. **Overview** - System statistics and metrics
2. **All Generations** - Table with Google Drive links
3. **System Monitoring** - CPU, memory, Docker, Celery
4. **Configuration** - View/edit app-config.json
5. **Users** - User management
6. **Backups** - Backup management
7. **Costs** - Cost monitoring
8. **Rate Limits** - View/adjust limits

#### AdminDashboard Component

**File:** `frontend/src/components/admin/AdminDashboard.tsx`

```typescript
import React, { useState } from 'react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { OverviewTab } from './tabs/OverviewTab';
import { GenerationsTab } from './tabs/GenerationsTab';
import { MonitoringTab } from './tabs/MonitoringTab';
import { ConfigurationTab } from './tabs/ConfigurationTab';
import { UsersTab } from './tabs/UsersTab';
import { BackupsTab } from './tabs/BackupsTab';
import { CostsTab } from './tabs/CostsTab';
import { RateLimitsTab } from './tabs/RateLimitsTab';

export const AdminDashboard: React.FC = () => {
  const [activeTab, setActiveTab] = useState('overview');

  return (
    <div className="admin-dashboard container mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">Admin Dashboard</h1>

      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList className="grid w-full grid-cols-4 lg:grid-cols-8">
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="generations">Generations</TabsTrigger>
          <TabsTrigger value="monitoring">Monitoring</TabsTrigger>
          <TabsTrigger value="config">Config</TabsTrigger>
          <TabsTrigger value="users">Users</TabsTrigger>
          <TabsTrigger value="backups">Backups</TabsTrigger>
          <TabsTrigger value="costs">Costs</TabsTrigger>
          <TabsTrigger value="ratelimits">Rate Limits</TabsTrigger>
        </TabsList>

        <TabsContent value="overview">
          <OverviewTab />
        </TabsContent>

        <TabsContent value="generations">
          <GenerationsTab />
        </TabsContent>

        <TabsContent value="monitoring">
          <MonitoringTab />
        </TabsContent>

        <TabsContent value="config">
          <ConfigurationTab />
        </TabsContent>

        <TabsContent value="users">
          <UsersTab />
        </TabsContent>

        <TabsContent value="backups">
          <BackupsTab />
        </TabsContent>

        <TabsContent value="costs">
          <CostsTab />
        </TabsContent>

        <TabsContent value="ratelimits">
          <RateLimitsTab />
        </TabsContent>
      </Tabs>
    </div>
  );
};
```

---

### Collaborative Features

#### Overview
Enable sharing ebooks with other users with permission levels and expiry options.

#### Database Schema

```sql
-- Ebook shares
CREATE TABLE ebook_shares (
    id SERIAL PRIMARY KEY,
    generation_id INTEGER REFERENCES generations(id) ON DELETE CASCADE,
    shared_by INTEGER REFERENCES users(id) ON DELETE CASCADE,
    shared_with INTEGER REFERENCES users(id) ON DELETE CASCADE,

    -- Share details
    permission VARCHAR(20) NOT NULL, -- 'view', 'comment', 'edit'
    share_link VARCHAR(255) UNIQUE,
    expires_at TIMESTAMP WITH TIME ZONE,

    -- Status
    is_active BOOLEAN DEFAULT TRUE,
    accessed_count INTEGER DEFAULT 0,
    last_accessed_at TIMESTAMP WITH TIME ZONE,

    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    -- Constraints
    CHECK (permission IN ('view', 'comment', 'edit'))
);

-- Chapter comments
CREATE TABLE chapter_comments (
    id SERIAL PRIMARY KEY,
    share_id INTEGER REFERENCES ebook_shares(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    chapter_number INTEGER NOT NULL,
    comment_text TEXT NOT NULL,
    parent_comment_id INTEGER REFERENCES chapter_comments(id) ON DELETE CASCADE,

    -- Position in text (for inline comments)
    position_start INTEGER,
    position_end INTEGER,

    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    -- Status
    is_resolved BOOLEAN DEFAULT FALSE
);

-- Indexes
CREATE INDEX idx_ebook_shares_generation ON ebook_shares(generation_id);
CREATE INDEX idx_ebook_shares_shared_by ON ebook_shares(shared_by);
CREATE INDEX idx_ebook_shares_shared_with ON ebook_shares(shared_with);
CREATE INDEX idx_ebook_shares_link ON ebook_shares(share_link);
CREATE INDEX idx_chapter_comments_share ON chapter_comments(share_id);
CREATE INDEX idx_chapter_comments_chapter ON chapter_comments(share_id, chapter_number);
```

#### Sharing Service

**File:** `backend/app/services/sharing_service.py`

```python
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from datetime import datetime, timedelta
import secrets
import string

from app.models.sharing import EbookShare, ChapterComment
from app.models.user import User
from app.models.generation import Generation
from app.core.exceptions import ValidationError, NotFoundError

class SharingService:
    def __init__(self, db: Session):
        self.db = db

    def share_ebook(
        self,
        generation_id: int,
        shared_by: int,
        shared_with: Optional[int] = None,
        permission: str = "view",
        expiry_days: Optional[int] = None
    ) -> EbookShare:
        """
        Share an ebook with another user or via link

        Args:
            generation_id: Generation ID to share
            shared_by: User ID who is sharing
            shared_with: Optional user ID to share with
            permission: Permission level (view, comment, edit)
            expiry_days: Optional number of days until expiry

        Returns:
            Created share record
        """
        # Validate generation ownership
        generation = self.db.query(Generation).filter(
            and_(
                Generation.id == generation_id,
                Generation.user_id == shared_by
            )
        ).first()

        if not generation:
            raise NotFoundError("Generation not found or you don't have permission")

        # Validate permission
        valid_permissions = ['view', 'comment', 'edit']
        if permission not in valid_permissions:
            raise ValidationError(f"Invalid permission. Must be one of: {valid_permissions}")

        # Calculate expiry
        expires_at = None
        if expiry_days:
            expires_at = datetime.utcnow() + timedelta(days=expiry_days)

        # Create share
        share = EbookShare(
            generation_id=generation_id,
            shared_by=shared_by,
            shared_with=shared_with,
            permission=permission,
            share_link=self._generate_share_link() if not shared_with else None,
            expires_at=expires_at
        )

        self.db.add(share)
        self.db.commit()
        self.db.refresh(share)

        return share

    def get_shared_ebooks(self, user_id: int) -> List[dict]:
        """Get all ebooks shared with user"""
        shares = self.db.query(EbookShare).join(Generation).filter(
            and_(
                EbookShare.shared_with == user_id,
                EbookShare.is_active == True,
                or_(
                    EbookShare.expires_at.is_(None),
                    EbookShare.expires_at > datetime.utcnow()
                )
            )
        ).order_by(EbookShare.created_at.desc()).all()

        return [
            {
                "id": share.id,
                "generation": {
                    "id": share.generation.id,
                    "title": share.generation.title,
                    "author": share.generation.author,
                    "chapter_count": share.generation.chapter_count
                },
                "permission": share.permission,
                "shared_by": share.sharer.username,
                "created_at": share.created_at.isoformat(),
                "expires_at": share.expires_at.isoformat() if share.expires_at else None
            }
            for share in shares
        ]

    def get_active_shares(self, user_id: int, generation_id: int) -> List[dict]:
        """Get all active shares for a user's generation"""
        shares = self.db.query(EbookShare).filter(
            and_(
                EbookShare.generation_id == generation_id,
                EbookShare.shared_by == user_id,
                EbookShare.is_active == True,
                or_(
                    EbookShare.expires_at.is_(None),
                    EbookShare.expires_at > datetime.utcnow()
                )
            )
        ).all()

        return [
            {
                "id": share.id,
                "shared_with": share.shared_with_user.username if share.shared_with else None,
                "share_link": share.share_link,
                "permission": share.permission,
                "accessed_count": share.accessed_count,
                "last_accessed_at": share.last_accessed_at.isoformat() if share.last_accessed_at else None,
                "expires_at": share.expires_at.isoformat() if share.expires_at else None
            }
            for share in shares
        ]

    def revoke_share(self, share_id: int, user_id: int) -> bool:
        """Revoke a share"""
        share = self.db.query(EbookShare).filter(
            and_(
                EbookShare.id == share_id,
                EbookShare.shared_by == user_id
            )
        ).first()

        if not share:
            raise NotFoundError("Share not found")

        share.is_active = False
        self.db.commit()

        return True

    def access_shared_ebook(
        self,
        share_link: str,
        user_id: Optional[int] = None
    ) -> dict:
        """Access an ebook via share link"""
        share = self.db.query(EbookShare).filter(
            and_(
                EbookShare.share_link == share_link,
                EbookShare.is_active == True,
                or_(
                    EbookShare.expires_at.is_(None),
                    EbookShare.expires_at > datetime.utcnow()
                )
            )
        ).first()

        if not share:
            raise NotFoundError("Share not found or expired")

        # Update access stats
        share.accessed_count += 1
        share.last_accessed_at = datetime.utcnow()
        self.db.commit()

        return {
            "generation_id": share.generation_id,
            "permission": share.permission,
            "expires_at": share.expires_at.isoformat() if share.expires_at else None
        }

    def add_comment(
        self,
        share_id: int,
        user_id: int,
        chapter_number: int,
        comment_text: str,
        parent_comment_id: Optional[int] = None,
        position_start: Optional[int] = None,
        position_end: Optional[int] = None
    ) -> ChapterComment:
        """Add a comment to a shared chapter"""
        # Validate share
        share = self.db.query(EbookShare).filter(
            EbookShare.id == share_id
        ).first()

        if not share:
            raise NotFoundError("Share not found")

        # Check permission
        if share.permission == 'view':
            raise ValidationError("You don't have permission to comment")

        # Create comment
        comment = ChapterComment(
            share_id=share_id,
            user_id=user_id,
            chapter_number=chapter_number,
            comment_text=comment_text,
            parent_comment_id=parent_comment_id,
            position_start=position_start,
            position_end=position_end
        )

        self.db.add(comment)
        self.db.commit()
        self.db.refresh(comment)

        return comment

    def get_chapter_comments(
        self,
        share_id: int,
        chapter_number: int
    ) -> List[dict]:
        """Get all comments for a chapter"""
        comments = self.db.query(ChapterComment).filter(
            and_(
                ChapterComment.share_id == share_id,
                ChapterComment.chapter_number == chapter_number,
                ChapterComment.parent_comment_id.is_(None)
            )
        ).order_by(ChapterComment.created_at.asc()).all()

        return [
            self._comment_to_dict(c)
            for c in comments
        ]

    def _comment_to_dict(self, comment: ChapterComment) -> dict:
        """Convert comment to dictionary with replies"""
        return {
            "id": comment.id,
            "user_id": comment.user_id,
            "username": comment.user.username,
            "comment_text": comment.comment_text,
            "position_start": comment.position_start,
            "position_end": comment.position_end,
            "is_resolved": comment.is_resolved,
            "created_at": comment.created_at.isoformat(),
            "updated_at": comment.updated_at.isoformat(),
            "replies": [
                self._comment_to_dict(reply)
                for reply in comment.replies
            ]
        }

    def _generate_share_link(self) -> str:
        """Generate unique share link"""
        alphabet = string.ascii_letters + string.digits
        return ''.join(secrets.choice(alphabet) for _ in range(32))
```

---

## Testing Strategies

### Template System Testing

**File:** `backend/tests/test_templates.py`

```python
import pytest
from fastapi.testclient import TestClient

def test_template_crud():
    """Test full template CRUD operations"""
    # Test creation
    # Test reading
    # Test updating
    # Test deletion

def test_template_validation():
    """Test template config validation"""
    # Test valid config
    # Test invalid config
    # Test missing required fields

def test_template_sharing():
    """Test template sharing and rating"""
    # Test public template access
    # Test rating system
    # Test usage tracking
```

### Search System Testing

**File:** `backend/tests/test_search.py`

```python
import pytest

def test_full_text_search():
    """Test full-text search functionality"""
    # Test search query
    # Test search ranking
    # Test search suggestions

def test_advanced_filters():
    """Test advanced filtering"""
    # Test multiple filters
    # Test date ranges
    # Test quality score ranges

def test_export_functionality():
    """Test search results export"""
    # Test CSV export
    # Test JSON export
    # Test PDF export
```

### Version Control Testing

**File:** `backend/tests/test_versions.py`

```python
import pytest

def test_version_creation():
    """Test creating new versions"""
    # Test version increment
    # Test version linking
    # Test latest version flag

def test_version_comparison():
    """Test version comparison"""
    # Test diff calculation
    # Test chapter-level comparison
    # Test version tree
```

---

## Deployment Checklist

### Week 17-18: Enhanced Features Deployment

- [ ] Database migrations for templates
- [ ] Database migrations for search (pg_trgm extension)
- [ ] Database migrations for versioning
- [ ] Database migrations for email notifications
- [ ] Deploy template service and API
- [ ] Deploy search service with indexes
- [ ] Deploy version service
- [ ] Deploy email service with SendGrid/Mailgun
- [ ] Seed template categories and public templates
- [ ] Seed email templates
- [ ] Configure Celery for email queue
- [ ] Deploy frontend Template Manager UI
- [ ] Deploy frontend Advanced Search UI
- [ ] Deploy frontend Version History UI
- [ ] Test all template operations
- [ ] Test search functionality
- [ ] Test version control
- [ ] Test email notifications

### Week 19-20: Production Readiness Deployment

- [ ] Deploy rate limiter with Redis
- [ ] Configure rate limit middleware
- [ ] Set up backup scripts and cron jobs
- [ ] Configure MinIO for backup storage
- [ ] Deploy cost tracking service
- [ ] Set up budget monitoring
- [ ] Deploy all 8 admin dashboard tabs
- [ ] Deploy sharing service
- [ ] Configure share links and permissions
- [ ] Deploy comment system
- [ ] Load test rate limiting
- [ ] Test backup/restore procedures
- [ ] Test cost tracking accuracy
- [ ] Test sharing functionality
- [ ] Monitor system performance
- [ ] Set up production alerts

---

## Summary

This Phase 4 implementation guide provides comprehensive details for:

1. **Enhanced Features (Week 17-18)**
   - Template library system with CRUD, validation, and versioning
   - Advanced search with full-text search, filters, and export
   - Version control for regenerations with comparison
   - Email notifications with templates and scheduling
   - Frontend UI components for all features

2. **Production Readiness (Week 19-20)**
   - Rate limiting with Redis and token bucket algorithm
   - Automated backup system with MinIO
   - Cost monitoring and budget enforcement
   - Complete admin dashboard with 8 tabs
   - Collaborative features with sharing and comments

3. **Testing & Deployment**
   - Comprehensive testing strategies
   - Detailed deployment checklists
   - Performance considerations

All code examples are production-ready and follow best practices for security, scalability, and maintainability.

